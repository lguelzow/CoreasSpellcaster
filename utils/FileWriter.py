#!/usr/bin/env python3
"""
This class can be used to create and write a Corsika inp file and create "data", "temp", "log", "inp" folders.

@author: Federico Bontempo <federico.bontempo@kit.edu> PhD student KIT Germany
@date: October 2022
"""
import pathlib
import numpy as np
from utils.RadioFilesGenerator import RadioFilesGenerator
from utils.SubFilesGenerator import SubFilesGenerator

class FileWriter:
    """
    This class can be used to create and write a Corsika inp file 
    and create "data", "temp", "log", "inp" folders.
    
    """
    

    def __init__(self,
        username,                       # User name on server
        dirSimulations,                 # Simulations directory where the data temp and log folder will be created
        dirRun,                         # run directory where the corsika executable and atmosphere file are stored
        primary,                        # 1 is gamma, 14 is proton, 402 is He, 1608 is Oxygen, 5626 is Fe
        dataset,                        # changed on 28 Jan 2020 according to IC std: 13000.0 +000 H, +100 He, +200 O, +300 Fe, +400 Gamma
        primIdDict,                     # This is a dictionary, with keys the Corsika numbering of primary, 
                                        # and values the arbitrary numbering used in this script for all primary particle. 
        
        obslev,                         # Observation level in cm
        pathAntennas,                   # Path to antennas
        zenithStart,
        azimuthStart,
    ):
        self.username = username
        self.primary = primary
        self.dirRun = dirRun
        self.directories = {"sim":dirSimulations}
        self.primIdDict= primIdDict
        
        self.zenithStart = zenithStart
        self.azimuthStart = azimuthStart
        self.obslev = obslev
        self.pathAntennas = pathAntennas


    def makeFolders(self, log10_E1): 
        """
        Creates "data", "temp", "log", "inp" folders and energy subfolder
        
        Parameters:
            log10_E1: the log10 of the Energy value for the subfolder creation        
        """
        for folder in ["data", "temp", "log", "inp", "starshapes"]:
            self.directories[folder] = f"{self.directories['sim']}/{folder}/"
            # Creates the required directories in case they are not existing
            pathlib.Path(f"{self.directories[folder]}/{log10_E1}").mkdir(parents=True, exist_ok=True)
        return
    # TODO: get rid of data and temp


    def writeFile(self, runNumber, log10_E1, azimuth, zenith):
        """
        Creates and writes a Corsika inp file that can be used as Corsika input
        """
        en1 = 10**log10_E1  # Lower limit of energy in GeV
        
        # The seed value in Corsika is 1 <= seed <= 900_000_000; 
        # It was decided to adopt the following seed has the form: 
        # pprrrrrr where pp is the primary ID (0, 1, 2...) and rrrrrr is the 6-digit run number
        # The seedValue is % 900.000.000 so that it does not exceed the max allowed seed value in Corsika
        # Note underscore do not change anything in the python numbers, they just make them easier to read
        seedValue = int((int(runNumber) + self.primIdDict[self.primary]*1_000_000) % 900_000_001) 

        # create the SIMxxxxxx ID
        sim = f"SIM{runNumber}"

        # This is the inp file, which gets written into the folder
        inp_name = (f"{self.directories['inp']}/{log10_E1}/{sim}.inp")
        
        seed1 = seedValue  # int(np.random.normal(mu, sigma))#random chosen)  #changed on 28 Jan 2020 according to IC std
        seed2 = seed1 + 1
        seed3 = seed1 + 2
        seed4 = seed1 + 3

        thin1 = 1.000E-06
        
        print("Filewriter using azimuth", azimuth)
        print("Filewriter using zenith", zenith)

        # Opening and writing in the file 
        with open(inp_name, "w") as file:
            # Things that go into the input files for corsika
            file.write(
                f"RUNNR   {runNumber}\n" # Unique run number in the file name of corsika
                + f"EVTNR   1\n"
                + f"SEED    {seed1}    0    0\n"  #
                + f"SEED    {seed2}    0    0\n"  #
                + f"SEED    {seed3}    0    0\n"  #
                + f"SEED    {seed4}    0    0\n"  #
                + f"NSHOW   1\n"
                + f"PRMPAR  {self.primary}\n"
                + f"ERANGE  {en1:.11E}    {en1:.11E}\n"  # in GeV
                + f"THETAP  0    0\n"  
                + f"PHIP    0 0\n"  
                + f"ECUTS   3.0E-01 1.0E-02 2.5E-04 2.5E-04\n"
                + f"ELMFLG  T    T\n"   # Disable NKG since it gets deactivated anyway when CURVED is selected at corsika setup
                + f"THIN    {thin1} 1.0E+0 1.000E+0\n" # ERANGE * THIN1 = THIN2 # {thin1} {thin1 * en1:.11E} 5.000000e+03\n
                + f"STEPFC  1.0\n"
                + f"OBSLEV  {self.obslev}\n"
                + f"ECTMAP  1.E+05\n"
                + f"MUMULT  T\n"
                + f"MUADDI  T\n"
                + f"MAXPRT  1\n"
                + f"MAGNET  50.0    0.0\n"
                + f"PAROUT  T  F\n"
                + f"LONGI   T   5.     T       T\n"
                + f"RADNKG  5.E+05\n"           
                + f"ATMFILE {self.dirRun}/ATMOSPHERE_20170401120000_Dunhuang.DAT\n"
                + f"DIRECT  {self.directories['inp']}/{log10_E1}/\n"
                + f"DATDIR  {self.dirRun}\n"
                + f"USER    {self.username}\n"
                + f"EXIT\n")
        

        # create the radio files
        RadGen = RadioFilesGenerator(
            obslev = self.obslev,
            directory = self.directories["inp"],
            runNumber = runNumber,
            log10_E1 = log10_E1,
            pathAntennas = self.pathAntennas,
            zenith = zenith,
            azimuth = azimuth,
            # azimuthStart = self.azimuthStart,
            # azimuthEnd = self.azimuthEnd,
            # azimuthStep = self.azimuthStep,
        )

        RadGen.writeReasList()


        # create the .sub and .sh file for each shower
        SubGen = SubFilesGenerator(
            inpdir = self.directories["inp"],
            logdir = self.directories["log"],
            runNumber = runNumber,
            log10_E1 = log10_E1,
            zenith = zenith,
            pathCorsika = "/home/hk-project-radiohfi/bg5912/work/soft/corsika-77420/run/",
            corsikaExe = "/mpi_corsika77420Linux_SIBYLL_urqmd_thin_coreas_parallel_runner",
        )

        SubGen.writeSubFiles()