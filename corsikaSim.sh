#!/bin/bash

# for Horeka, make sure these exact modules are loaded:
# module load compiler/gnu/10.2
# module load mpi/openmpi/4.1
PYTHON=/usr/bin/python
SCRIPT=/home/hk-project-radiohfi/bj4908/software/CoreasSpellcaster/MakeCorsikaSim.py

#TODO Make sure this is the right corsika path
cd /home/hk-project-radiohfi/bj4908/software/corsika-77550/run/

#TODO Make sure to change the parameters correctly. Documentation in the args of MakeCorsikaSim.py
# specifically:
#TODO check corsikaExe

$PYTHON $SCRIPT \
                --username bj4908 \
                --primary 14 \
                --dirSimulations "/hkfs/work/workspace/scratch/bj4908-corsika_sims/china_stshps/" \
                --pathCorsika "/home/hk-project-radiohfi/bj4908/software/corsika-77550/run/" \
                --corsikaExe "/mpi_corsika77550Linux_SIBYLL_urqmd_thin_coreas_parallel_runner" \
                --startNumber 3 \
                --endNumber 4 \
                --energyStart 9.4 \
                --energyEnd 11.2 \
                --energyStep 0.2 \
                --zenithStart 65 \
                --zenithEnd 85 \
                --obslev 114200 \

                 

# proton 14, iron 5626
# obslev Dunhuang 1.2 km -> 1200 m -> 120000 cm 
# if startNumber is 0, endnumber equals number of sims per bin 
# energy in log10 of GeV