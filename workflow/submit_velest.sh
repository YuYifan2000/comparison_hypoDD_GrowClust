#!/usr/bin/bash
#SBATCH --job-name=velest
#SBATCH --output=%j.out
#SBATCH --error=%j.err
#SBATCH --time=1:30:00
#SBATCH -p serc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=16GB
velest
