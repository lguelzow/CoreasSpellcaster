#!/usr/bin/env python3
"""
This is the main script for the Corsika simulations.
It uses the 3 classes imported from utils

FileWriter class can be used to create and write a Corsika inp file 
    and create "data", "temp", "log", "inp" folders.
    
SimulationMaker class can be used for generating the submission stings and sh executable files. 
    It also has the generator function which yields the keys and string to submit, 
    made via the combinations of file and energies 

Submitter class can be used to spawns subprocesses for multiple instances instead of multiple job submissions.

The args values can be used to specify the desired configuration for the simulation.

How to run:
    python3 MakeCorsikaSim.py 
 if you want to change any configuration from the default once add the [args] after it
 e.g.:
    python3 MakeCorsikaSim.py --user myusername --primary 1 ..... 

@author: Federico Bontempo <federico.bontempo@kit.edu> PhD student KIT Germany
@date: October 2022
"""
import sys
import os 
import numpy as np
import random
import subprocess

from utils.SimulationMaker import SimulationMaker
from utils.Submitter import Submitter

def __checkInputs(args):
    """
    This function should check some basic things before the starting the simulation.
        energyEnd > energyStart
        energyEnd <= 10_000 otherwise the numbering is not unique anymore 
        primary is in the keys of the pimIdDict
        check if the corsika given is correct 
        maybe a warning if seed value is over 900_000_000
        
    seedValue = int((runNumber + self.primIdDict[self.primary]*1_000_000) % 900_000_001) 
    """
    # if not args.energyEnd > args.energyStart:
    #     sys.exit('The energy End value MUST be greater (nor equal) then the starting one!!')
    
    # if not args.energyEnd <= 10_000:
    #     sys.exit('The energy End value MUST be less then 10.000!! The seed number is not unique otherwise!')
    
    if args.primary not in args.primIdDict.keys():
        sys.exit('The primary chosen is not in the primIdDict in the mainCorsikaSim. \nBe sure that the --primary is correct.\
            \nIf so, update the args.primIdDict in the mainCorsikaSim.')
    
    if not os.path.isfile(f"{args.pathCorsika}/{args.corsikaExe}"): 
        sys.exit('The corsikaExe does not exist or the pathCorsika is wrong.\
            \nCheck them, please!')
    
    if args.primIdDict[args.primary]*1_000_000 > 900_000_001:
        import warnings
        warnings.warn("The program is not stopped, \
            but aware that the Corsika seed number is exceeding 900.000.000 (the max allowed value)")
    return


def mainCorsikaSim(args):
    """
    Some Documentation of the main function for the Corsika Simulator
    
    Defines the indexing of the primaries. This can be updated if needed in the future. 
    Checks if the inputs given are consistent with the script 
    Defines the energy range
    Calls a bunch of classes 
    Finally: 
    start spawning and checking multiple simulations.
    """
    # This is a dictionary, with keys the Corsika numbering of primary, 
    # and values the arbitrary numbering used in this script for all primary particle. 
    # In principle this can be expanded with all primaries that one wants     
    args.primIdDict = {
        1:    0,      # Gammas (photons)
        14:   1,      # Protons (H)
        402:  2,      # Helium (He)
        1608: 3,      # Oxygen (O)
        5626: 4,      # Iron (Fe)
        2814: 5,      # Silicon (Si)
                }

    # Checks if the input given are consistent with the structure of the script
    __checkInputs(args)
    
    # Defines the energy range given the start, end and step 
    energies = np.around( # Need to round the numpy array otherwise the floating is wrong
                    args.energyStart,
                    # np.arange(
                    #     args.energyStart, # energy starting point
                    #     args.energyEnd + args.energyStep, # energy end point plus one step in order to include last step
                    #     args.energyStep, # step in energies
                        # ),
                decimals=1 # the rounding has to have one single decimal point for the folder. 
    )
    

    simMaker = SimulationMaker(
        pathCorsika = args.pathCorsika,
        corsikaExe = args.corsikaExe,
    )

    submitter = Submitter(
        MakeKeySubString=simMaker.generator,
        logDir=args.logDirProcesses,
        parallel_sim=args.parallelSim,
    )

    # Starts the spawn of the simulations
    submitter.startProcesses()
    # Loops over the running processes and checks if any process is complete.
    # If so, it will spawn the next one
    submitter.checkRunningProcesses()
    


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Inputs for the Corsika Simulation Maker"
    )

    parser.add_argument(
        "--username", 
        type=str, 
        default="bg5912", 
        help="your user name on server"
    )
    parser.add_argument(
        "--dirSimulations",
        type=str,
        default="/home/hk-project-radiohfi/bg5912/work/sims/Max/",
        help="Directory where the simulation are stored",
    )
    parser.add_argument(
        "--pathCorsika",
        type=str,
        default="/home/hk-project-radiohfi/bg5912/work/soft/corsika-77420/run/",
        help="the /run directory where the executable of corsika is located",
    )
    parser.add_argument(
        "--corsikaExe",
        type=str,
        default="corsika77420Linux_SIBYLL_urqmd_thin_coreas",
        help="the name of the executable of corsika located in the /run directory",
    )

    parser.add_argument(
        "--logDirProcesses",
        type=str,
        default="/home/hk-project-radiohfi/bg5912/work/sims/Max/logs/",
        help="Directory where log files of the multiple subProcesses are stored",
    )
    parser.add_argument(
        "--parallelSim",
        type=int,
        default=1,
        help="Number of parallel simulation processes - DO NOT USE WITH MPI",
    )

    args = parser.parse_args()
    mainCorsikaSim(args)

    print("Final incantation complete: All cosmic portals explored, program's journey ends...")
    # subprocess.run("rm -r {options.dirSimulations}/temp/", check=True)
    # subprocess.run("rm -r {options.dirSimulations}/starshapes/", check=True)
    
    print("-------------------- Program finished --------------------")