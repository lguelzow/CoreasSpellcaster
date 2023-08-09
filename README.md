# CoreasSpellcaster
Unleash the magic of simultaneous shower simulations with this Coreas generator.

### Author
Jelena Köhler @jelenakhlr\
@date: August 2023

original version by @fedbont94\
forked from https://github.com/fedbont94/Horeka

## Before you start
1. Select the proper branch\
_"radio-mpi"_ for the mpi version\
_"radio-non-mpi"_ for the non-mpi version

2. Compile the version of Corsika you need\
for mpi: Make sure to use the **PARALLEL** option and to compile with **MPILIBRARY**\
(do not use these for non-mpi)\
\
For more info, see the **Corsika** manual: https://web.iap.kit.edu/corsika/usersguide/usersguide.pdf \
and the **Coreas** manual: https://web.ikp.kit.edu/huege/downloads/coreas-manual.pdf

4. Download **miniradiotools** from https://github.com/jelenakhlr/miniradiotools

5. Check paths:\
When using these scripts, make sure to modify paths, usernames, etc. in these files:\
\
*SubFile.sub*\
*corsikaSim.sh*\
*ExecuteSubfile.sh*\
*utils/FileWriter.py*\
*MakeCorsikaSim.py*\
\
Also check if you need to modify things in\
\
*RadioFilesGenerator.py*\
*SimulationMaker.py*

## How to run
Once you have set all paths and input values according to your needs, run

./ExecuteSubFile.sh


## General Information
by @fedbont94

_ExecuteSubFile.sh_ - Is an executable that submits on slurm (Horeka cluster) the SubFile.sub \
_SubFile.sub_ -       Contains all the requests in terms of memory, time, node... for the cluster\
                    It loads .bashrc (can be taken out if not necessary)\
                    It cd in the corsika/run/ folder, you may need to change the path\
                    It calls the python script with all arguments that need to be passed and MUST be adapted to your interests.

_MakeCorsikaSim.py_ - Is the main script that for Corsika air shower simulation (more documentation in the script)
_MakeDetectorResponse.py_ - Is the main script that for detector response simulation (more documentation in the script)


_utils/FileWriter.py_ -       Contains a class that can be used to create and write a Corsika inp file and create "data", "temp", "log", "inp" folders. \
                            (more documentation in the script)

                            
_utils/SimulationMaker.py_ -  Contains a class that can be used for generating the submission stings and sh executable files. \
                            It also has the generator function which yields the keys and string to submit, 
                            made via the combinations of file and energies \
                            (more documentation in the script)

                            
_utils/Submitter.py_ -        Contains a class that can be used to spawns subprocesses for multiple instances instead of multiple job submissions.
                            (more documentation in the script)\
                            

_utils/DetectorSimulator.py_ - Contains a class that can be used to simulate the detector response for a given corsika file. \
                            (more documentation in the script)
                            
                            
_utils/MultiProcesses.py_ -   Contains a class that can be used to spawn multiple processes for the detector response simulation. \
                            (more documentation in the script)
