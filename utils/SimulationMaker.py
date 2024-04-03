#!/usr/bin/env python3
"""
This class can be used for generating the submission stings and sh executable files. 
It also has the generator function which yields the keys and string to submit, 
made via the combinations of file and energies 

@author: Federico Bontempo <federico.bontempo@kit.edu> PhD student KIT Germany
@date: October 2022

edited for serial radio by 
@author: Jelena
@date: April 2024

"""
import numpy as np
import os
import stat
import sys

class SimulationMaker:
    """
    This class has two useful functions. 
        generator: which yields a key and a string to submit 
        makeStringToSubmit: which writes a temporary file and a string to submit
    
    Parameters:
        pathCorsika:    the path where Corsika is installed
        corsikaExe:     the name of the Corsika executable that needs to be used
        dirSimulations: the main directory. Inside, there is one directory per runIndex.
    
    """
    def __init__(self, 
                 pathCorsika, 
                 corsikaExe,
                 dirSimulations
    ):
        
        self.pathCorsika = pathCorsika
        self.corsikaExe = corsikaExe
        self.dirSimulations = dirSimulations



    def generator(self):
        """
        The yield function returns every time a different value as the for loop proceeds
        """ 
        print(f"Path specified as {self.dirSimulations}")
        for folder in os.scandir(self.dirSimulations): # Efficiently scan directories
            if folder.is_dir():  # Check for subdirectories (simulations)
                print(f"Found {folder}...")
                runNumber = folder.name  # Extract run number from folder name
                print(f"RunNumber: {runNumber}")
                if len(runNumber) == 6 and runNumber.isdigit():  # Validate format
                    key = f"{runNumber}"
                    stringToSubmit = self.makeStringToSubmit(runNumber)
                    yield (key, stringToSubmit)



    def makeStringToSubmit(self, runNumber):
        # A few paths to files are defined. 
        inpFile = f"{self.dirSimulations}/{runNumber}/RUN{runNumber}.inp" # input file
        logFile = f"{self.dirSimulations}/{runNumber}/DAT{runNumber}.log" # log file 
        listFile = f"{self.dirSimulations}/{runNumber}/SIM{runNumber}.list" # list file
        gdasFile = f"{self.dirSimulations}/{runNumber}/GDAS{runNumber}.dat" #GDAS file
        
        # Makes a temp file for submitting the jobs.
        tempFile = f"{self.dirSimulations}/{runNumber}/temp_{runNumber}.sh"
        print(f"Creating temp file for {runNumber}")
        with open(tempFile, "w") as f:
            f.write(r"#!/bin/sh") # This shows that the file is an executable
            f.write(
                f"\n"
                # + "rm the corsika file \n"
                + f"{self.pathCorsika}/{self.corsikaExe} {inpFile} > {logFile}\n" # run corsika
                + f"rm {tempFile}\n"
                + f"\n"
            )


        # Make the file executable
        st = os.stat(tempFile)
        os.chmod(tempFile, st.st_mode | stat.S_IEXEC)

        # The stringToSubmit is basically the execution of the temporary sh file
        subString = tempFile
        return subString

