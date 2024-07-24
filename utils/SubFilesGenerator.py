# author: Jelena

import numpy as np
import os
import stat

class SubFilesGenerator:

    def __init__(self,
        runNumber,                  
        log10_E1,
        zenith,
        primary,
        directory,
        folder_path,
        pathCorsika = "/home/hk-project-radiohfi/bg5912/work/soft/corsika-77550/run/",
        corsikaExe = "/mpi_corsika77550Linux_SIBYLL_urqmd_thin_coreas_parallel_runner",
        
    ):
        self.runNumber = runNumber
        self.log10_E1 = log10_E1

        self.zenith = zenith
        self.primary = primary


        self.folder_path = folder_path
        self.directory = directory
        self.pathCorsika = pathCorsika
        self.corsikaExe = corsikaExe


    def subWriter(self):

        # create the SIMxxxxxx ID
        sim = f"SIM{self.runNumber}"
        # create the DATxxxxxx ID
        dat = f"DAT{self.runNumber}"

        # os.makedirs({self.directory}/{self.primary}/{self.log10_E1}/{self.zenith}/{self.runNumber}, exist_ok=True)
        # This is the .sub file, which gets written into the folder
        sub_file = f"{self.folder_path}/{sim}.sub"
        # and the corsika files
        inpFile = f"{self.folder_path}/{sim}.inp" # input file
        logFile = f"{self.folder_path}/{dat}.log" # log file


        # directory containing the simulation files (input + output)
        inpdir = f"{self.folder_path}/"
        logdir = f"{self.folder_path}/"
        # create a directory to move all annoying files to after the sim is completed
        datdir = f"{self.folder_path}/{dat}/"



        # get theta
        theta = self.zenith

        # specify runtime according to theta
        # larger theta require more runtime
        if theta >= 65:
            runtime = "10:00:00"
        elif theta >= 75:
            runtime = "12:00:00"
        elif theta >= 77.5:
            runtime = "16:00:00"
        elif theta >= 80:
            runtime = "30:00:00"
        else:
            runtime = "08:00:00"


        # Opening and writing in the file 
        with open(sub_file, "w") as file:
            ######Things that go into the sub file for Horeka#######
            file.write(""
                + f"#!/bin/bash\n"
                + f"#SBATCH --account=\"hk-project-p0022320\"\n"
                + f"#SBATCH --job-name={self.runNumber}\n"
                + f"#SBATCH --output={logdir}_log%j.out\n"
                + f"#SBATCH --error={logdir}_log%j.err\n"
                + f"#SBATCH --nodes=1\n"
                + f"#SBATCH --ntasks-per-node=76\n"
                + f"#SBATCH --cpus-per-task=1\n"
                + f"#SBATCH --time=2-00:00:00\n" #{self.runtime}
                + f"\n"
                + f"# Load MPI module (if necessary)\n"
                + f"# module load mpi\n"
                + f"# Set the path to your MPI-Corsika executable\n"
                + f"MPI_CORSIKA_EXEC='{self.pathCorsika}/{self.corsikaExe}'\n"
                # CORSIKA_EXEC='{self.pathCorsika}/{self.corsikaExe}'\n"
                + f"\n"
                + f"# Set the path to your input and output files\n"
                + f"INPUT_FILE='{inpFile}'\n"
                + f"LOG_FILE='{logFile}'\n"
                + f"\n"
                + f"echo ======================= Conjuring Cosmic Showers  ====================== \n"
                + f"echo starting job number {self.runNumber} \n"
                + f"echo time: $(date)\n" # print current time
                + f"# Run the MPI-Corsika executable\n"
                + f"mpirun --bind-to core:overload-allowed --map-by core -report-bindings -np $SLURM_NTASKS $MPI_CORSIKA_EXEC $INPUT_FILE > $LOG_FILE\n"
                # $CORSIKA_EXEC < $INPUT_FILE > $LOG_FILE\n d
                + f"\n"
                + f"echo job number {self.runNumber} complete\n"
                + f"echo time: $(date)\n" # print current time
                + f"echo - - - - - - - - - - - - - - Cleansing Cauldron - - - - - - - - - - - - -\n"
                + f"mkdir {datdir}\n" # create datdir directory
                + f"echo created {datdir}\n"
                + f"echo moving binaries and corsika_timetables to {datdir}\n"
                + f"mv {inpdir}/DAT??????-* {datdir}\n" # move all annoying files to datdir
                + f"mv {inpdir}/corsika_timetable-* {datdir}\n"
                # + f"rm -r {inpdir}/../../data/ \n" # remove the obsolete data directory
                # + f"rm -r {inpdir}/../../temp/ \n" # remove the obsolete temp directory
                # + f"rm -r {inpdir}/../../starshapes/ \n" # remove the obsolete starshapes directory # TODO: figure out where this comes from and get rid of it
                + f"echo =================== Enchantment Successfully Executed ==================\n"
            )

        # Make the file executable
        st = os.stat(sub_file)
        os.chmod(sub_file, st.st_mode | stat.S_IEXEC)



    def writeSubFiles(self):
        # define this to make it easier to call the functions

        self.subWriter()
        