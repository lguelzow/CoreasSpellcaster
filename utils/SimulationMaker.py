#!/usr/bin/env python3
"""
This class can be used for generating the submission stings and sh executable files. 
It also has the generator function which yields the keys and string to submit, 
made via the combinations of file and energies 

@author: Federico Bontempo <federico.bontempo@kit.edu> PhD student KIT Germany
@date: October 2022

edited for radio by 
@author: Jelena
@date: June 2023

Submitting the sims with this program takes too long with Corsika :(
It's actually better to do one job per shower - for Coreas at least.
So FOR RADIO: use this whole thing to create the input and sh files 
and then run those separately using submit_jobs.py

"""
import numpy as np
import random
import os
import stat
from utils.runNumberGenerator import runNumberGenerator
import sys

class SimulationMaker:
    """
    This class has two useful functions. 
        generator: which yields a key and a string to submit 
        makeStringToSubmit: which writes a temporary file and a string to submit
    
    Parameters:
        startNumber:    the start of the simulation (eg. integer default value 0)
        endNumber:      the end of the simulation (eg. integer default value if startNumber is 0, 
                        it is the total number of simulations.
        energies:       the array binned in energies for the simulation
        fW:             the file writer class. In order to use some of the functions in this class
        pathCorsika:    the path where Corsika is installed
        corsikaExe:     the name of the Corsika executable that needs to be used
    
    """
    def __init__(self, 
                 startNumber, 
                 endNumber, 
                 energies, 
                 fW, 
                 pathCorsika, 
                 corsikaExe, 
                 zenithStart,
                 zenithEnd,
                 primary_particle
    ):
        
        self.startNumber = startNumber
        self.endNumber = endNumber
        self.energies = energies
        self.fW = fW
        self.pathCorsika = pathCorsika
        self.corsikaExe = corsikaExe
        self.zenithStart = zenithStart
        self.zenithEnd = zenithEnd
        self.primary_particle = primary_particle
        self.runNumGen = runNumberGenerator()



    def generator(self):
        """
        This function generates configurations for simulations with various energies, zenith angles, and azimuth angles. 
        It iterates through all possible combinations and yields a unique key and a string 
        required for submitting each simulation job.

        The folder structure for the simulations is created as:
            primary_particle/energy/theta/runNumber/

        Each run will have its own folder within the specified energy and zenith angle subdirectories.
        """
        print("Conjuring energies in log10 GeV of", self.energies)

        # Zenith angle range
        zenith_range = np.arange(self.zenithStart, self.zenithEnd + 0.1, 2.5)  # Creates range with 2.5 increments

        # Number of additional values per step
        num_additional_values = 80

        # Initialize empty list for all zenith values
        all_zenith_values = []
        cos = np.zeros(num_additional_values)
        print("zenith range", zenith_range[0], zenith_range[-1])
        # Calculate cosine values for the current step
        for i in range(1,num_additional_values): # start from 1 to exclude the 0
            start_angle = zenith_range[0]
            end_angle = zenith_range[-1]
            cos_values = np.linspace(1 / np.cos(np.deg2rad(start_angle)), 1 / np.cos(np.deg2rad(end_angle)), 
                                        num_additional_values + 1)[1:]  # Exclude first element (start value)
            int_size  = (end_angle - start_angle)/(num_additional_values - 1)
            cos[i] = start_angle + i * int_size
            all_zenith_values.append(cos[i])

        print("zenith vals", all_zenith_values)

        # Combine original list with generated values
        all_zenith_values.extend(zenith_range.tolist())  # Convert range to list

        # Sort the final zenith list
        zenith_list = sorted(all_zenith_values)
        print("zenith list", zenith_list)


        # loop for as long as there are values inside azimuth_list:
         # loop for as long as there are values inside azimuth_list:
        if zenith_list:
            while zenith_list:
                # This is a loop over all energies and gives the low and high limit values.
                # Eg. 5.0 and 5.1
                for log10_E1, log10_E2 in zip(self.energies[:-1], self.energies[1:]):
                    # loop over all the unique numbers 
                    for runIndex in range(self.startNumber, self.endNumber, 1):
                        #! zenith loop here
                        # Get the next azimuth value from the list
                        zenith = zenith_list.pop(0)
                        print("SimMaker using zenith", zenith)

                        #! random azimuth here
                        # Get random azimuth
                        azimuth = round(random.uniform(0, 360), 2)
                        print("SimMaker using azimuth", azimuth)

                        # print runIndex (as double check)
                        print("runIndex", runIndex)

                        # Create the file name (runNumber) for the simulation
                        particleID = self.runNumGen.getPrimaryID(self.primary_particle)
                        zenithID = self.runNumGen.getZenithID(zenith)
                        azimuthID = self.runNumGen.getAzimuthID(azimuth)
                        energyID = self.runNumGen.getEnergyID(log10_E1)
                        runNumber = format(int(particleID * 1E5 + zenithID * 1E4 + azimuthID * 1E3 + energyID * 1E2 + runIndex), '06d')
                        print("runNumber", runNumber)

                        # Create folders with the structure: primary_particle/energy/theta/runNumber/<files>
                        folder_path = os.path.join(f"{self.primary_particle}/{log10_E1}/{zenith}/{runNumber}/")
                        os.makedirs(folder_path, exist_ok=True)  # Create folders if they don't already exist

                        # Check if the simulation already exists
                        if f"SIM{runNumber}_coreas" not in os.listdir(folder_path):
                            # Write Corsika input file and generate key/string
                            self.fW.writeFile(runNumber, log10_E1, azimuth, zenith)
                            key = f"{log10_E1}_{runNumber}"
                            stringToSubmit = self.makeStringToSubmit(log10_E1, runNumber)
                            yield (key, stringToSubmit)

        else:
            sys.exit("Exiting...")


    #TODO: the temp file is not being used anymore (instead I have SubFilesGenerator.py now), but this part can't simply be removed because of dependency issues (in the function right above)
    def makeStringToSubmit(self, log10_E, runNumber):
        
        # Makes a temp file for submitting the jobs.
        tempFile = f"{self.fW.directories['temp']}/{log10_E}/temp_{runNumber}.sh"
        with open(tempFile, "w") as f:
            f.write(r"#!/bin/sh") # This shows that the file is an executable
            f.write(
                f"\n"
            )


        # Make the file executable
        st = os.stat(tempFile)
        os.chmod(tempFile, st.st_mode | stat.S_IEXEC)

        # The stringToSubmit is basically the execution of the temporary sh file
        subString = tempFile
        return subString

