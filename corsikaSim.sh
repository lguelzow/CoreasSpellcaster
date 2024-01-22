#!/bin/bash

# for Horeka, make sure these exact modules are loaded:
# module load compiler/gnu/10.2
# module load mpi/openmpi/4.1
PYTHON=/home/hk-project-radiohfi/bg5912/virtual_env/bin/python3
SCRIPT=/home/hk-project-radiohfi/bg5912/CoreasSpellcaster/MakeCorsikaSim.py

#TODO Make sure this is the right corsika path
cd /home/hk-project-radiohfi/bg5912/work/soft/corsika-77420/run/

#TODO Make sure to change the parameters correctly. Documentation in the args of MakeCorsikaSim.py
# specifically:
#TODO check paths in dirSimulations and logDirProcesses
#TODO check corsikaExe

$PYTHON $SCRIPT \
                --username nikos \
                --primary 5626 \
                --dirSimulations "/hkfs/work/workspace/scratch/bg5912-mysims/GP300/proton/run01/sim_storage/" \
                --pathCorsika "/home/hk-project-radiohfi/bg5912/work/soft/corsika-77420/run/" \
                --corsikaExe "/mpi_corsika77420Linux_SIBYLL_urqmd_thin_coreas_parallel_runner" \
                --startNumber 0 \
                --endNumber 100 \
                --energyStart 6.0 \
                --energyEnd 6.0 \
                --energyStep 0.0 \
                --zenithStart 0 \
                --zenithEnd 0 \
                --obslev 0 \
                --logDirProcesses "/hkfs/work/workspace/scratch/bg5912-mysims/GP300/proton/run01/logs/" \

# proton 14, iron 5626
# obslev Dunhuang 120000 m 