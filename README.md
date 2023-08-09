# CoreasSpellcaster
Unleash the magic of simultaneous shower simulations with this Coreas generator.

### Author
Jelena Köhler @jelenakhlr\
@date: August 2023

original version by @fedbont94\
forked from https://github.com/fedbont94/Horeka

## Before you start
1. Download **miniradiotools** from https://github.com/jelenakhlr/miniradiotools

2. Check paths:\
When using these scripts, make sure to modify paths, usernames, etc. in these files:

*SubFile.sub*\
*corsikaSim.sh*\
*ExecuteSubfile.sh*\
*utils/FileWriter.py*\
*MakeCorsikaSim.py*\

Also check if you need to modify things in

*RadioFilesGenerator.py*\
*SimulationMaker.py*

3. Compile the version of Corsika you need (and make sure to include that in the paths above)
Make sure to use the PARALLEL option and to compile with MPILIBRARY when using the radio-mpi branch of this repository

## How to run
Once you have set all paths and input values according to your needs, run

./ExecuteSubFile.sh


## General Information
This folder contains all the necessary scripts to run a multiple corsika simulations and detector response simulations in a single submission.

How to submit a job to the cluster:\
./ExecuteSubFile.sh

How to run the corsika simulation python script:\
python3 MakeCorsikaSim.py [--args] # as shown in SubFile.sub

How to run the detector resposne simulation python script:\
python3 MakeDetectorResponse.py [--args] # as shown in SubFile.sub

Summary:\
README.md -         This file

ExecuteSubFile.sh - Is an executable that submits on slurm (Horeka cluster) the SubFile.sub \
SubFile.sub -       Contains all the requests in terms of memory, time, node... for the cluster\
                    It loads .bashrc (can be taken out if not necessary)\
                    It cd in the corsika/run/ folder, you may need to change the path\
                    It calls the python script with all arguments that need to be passed and MUST be adapted to your interests.

MakeCorsikaSim.py - Is the main script that for Corsika air shower simulation (more documentation in the script)
MakeDetectorResponse.py - Is the main script that for detector response simulation (more documentation in the script)


utils/FileWriter.py -       Contains a class that can be used to create and write a Corsika inp file and create "data", "temp", "log", "inp" folders. \
                            (more documentation in the script)
utils/SimulationMaker.py -  Contains a class that can be used for generating the submission stings and sh executable files. \
                            It also has the generator function which yields the keys and string to submit, 
                            made via the combinations of file and energies \
                            (more documentation in the script)
utils/Submitter.py -        Contains a class that can be used to spawns subprocesses for multiple instances instead of multiple job submissions.
                            (more documentation in the script)

utils/DetectorSimulator.py - Contains a class that can be used to simulate the detector response for a given corsika file. \
                            (more documentation in the script)
utils/MultiProcesses.py -   Contains a class that can be used to spawn multiple processes for the detector response simulation. \
                            (more documentation in the script)
