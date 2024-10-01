#!/bin/bash

# Directory to search for .reas files that didn't run

# change to your parent directory of simulation output
DIRECTORY=/hkfs/work/workspace/scratch/bj4908-corsika_sims/china_stshps/

# Check if directory is provided
if [ -z "$DIRECTORY" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# check amount of .sub files and amount of .long files to check how many have not run
# write numbers as output
echo "Number of .sub files in subdirectories:"

find $DIRECTORY -type f -name "SIM[0-9][0-9][0-9][0-9][0-9][0-9].sub"  -printf x | wc -c

# write second part of result
echo "Number of finished simulations in subdirectories:"

find $DIRECTORY -type f -name "DAT[0-9][0-9][0-9][0-9][0-9][0-9].long"  -printf x | wc -c

# change mode for hdf5 or tar.gz search
echo "Number of processsed files (hdf5 or tar.gz):"
# find $DIRECTORY -type f -name "SIM[0-9][0-9][0-9][0-9][0-9][0-9]_50-100_highlevel.hdf5"  -printf x | wc -c
find $DIRECTORY -type f -name "[0-9][0-9][0-9][0-9][0-9][0-9].tar.gz"  -printf x | wc -c

# Find all directories that have .sub files that didn't run
find $DIRECTORY -type f -name "SIM[0-9][0-9][0-9][0-9][0-9][0-9].sub" | sed -r 's|/[^/]+$||' | while read -r SUB_FILE; do
    # only rerun the sub files that haven't run before and whose directories don't have simulation output
    if [ ! -e $SUB_FILE/DAT[0-9][0-9][0-9][0-9][0-9][0-9].long ]; then
        # submit script that didn't run
        # echo "No simulation results in $SUB_FILE!"
        # sbatch -p cpuonly -A hk-project-p0022320 $SUB_FILE/*.sub
    fi
done
