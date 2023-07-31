#!/usr/bin/bash
#SBATCH --job-name=multi_cores
#SBATCH --output=%j.out
#SBATCH --error=%j.err
#SBATCH --time=1:30:00
#SBATCH -p serc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=20
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=16GB

module load python/3.9.0
module load py-mpi4py/3.1.3_py39
echo  $((SLURM_NTASKS_PER_NODE * SLURM_NNODES))
srun python3 generate_tt.py $((SLURM_NTASKS_PER_NODE * SLURM_NNODES))
