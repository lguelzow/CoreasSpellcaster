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
                --dirSimulations "/hkfs/work/workspace/scratch/bj4908-corsika_sims/DC2_test" \
                --pathCorsika "/home/hk-project-radiohfi/bj4908/software/corsika-77550/run/" \
                --pathAntennas "/home/hk-project-radiohfi/bj4908/software/CoreasSpellcaster/utils/GP300-80_june2024.dat" \
                --corsikaExe "/mpi_corsika77550Linux_SIBYLL_urqmd_thin_coreas_parallel_runner" \
                --simAmount 1000 \
                --startNumber 0 \
                --endNumber 1 \
                --energyStart 9.0 \
                --energyEnd 11.0 \
                --energyStep 0 \
                --zenithStart 65 \
                --zenithEnd 85 \
                --obslev 126554.24 \

                 

# proton 14, iron 5626
# obslev GP300 126554.24 cm 
# if startNumber is 0, endnumber equals number of sims per bin 
# energy in log10 of GeV
# start and end numbers do not matter if energyStep=0, since then the simAmount parameter governs the continuously generated simulation amount