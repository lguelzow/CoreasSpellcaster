#!/bin/bash
#SBATCH --job-name=compress_library
#SBATCH --account="hk-project-p0022320"
#SBATCH --output=/hkfs/work/workspace/scratch/bj4908-corsika_sims/china_stshps/logs/compression_log%j.out
#SBATCH --error=/hkfs/work/workspace/scratch/bj4908-corsika_sims/china_stshps/logs/compression_log%j.err
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=08:00:00
#SBATCH --tasks=1
######SBATCH --mem=50gb
######SBATCH --export=NONE
#######################SBATCH --gres=gpu:4

# Directory to search for subdirectories
TARGET_DIR="/hkfs/work/workspace/scratch/bj4908-corsika_sims/china_stshps/5626/"

echo "Searching in: $TARGET_DIR"

# Find all directories exactly two levels deeper than TARGET_DIR
find "$TARGET_DIR" -mindepth 3 -maxdepth 3 -type d | while read -r dir; do
  # Get the base name of the directory
  dir_name=$(basename "$dir")

  # Get the parent directory of the current directory
  parent_dir=$(dirname "$dir")

  # Print the current directory being processed
  echo "Processing directory: $dir"

  # Create a tar.gz archive of the directory contents and place it in the parent directory
  echo "Compressing ${dir} and placing tarball in ${parent_dir}..."
  tar -czf "${parent_dir}/${dir_name}.tar.gz" -C "$dir" .
done