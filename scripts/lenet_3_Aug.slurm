#!/bin/bash
# Created by the University of Melbourne job script generator for SLURM
# Wed Oct 04 2023 21:44:14 GMT+1100 (Australian Eastern Daylight Time)

# Partition for the job:
#SBATCH --partition=gpu-a100

# Multithreaded (SMP) job: must run on one node
#SBATCH --nodes=1

# The name of the job:
#SBATCH --job-name="mallacoota-bushfire-cnn"

#SBATCH --output=lenet_3_Aug.txt

# The project ID which this job should run under:
#SBATCH --account="punim2110"

# Maximum number of tasks/CPU cores used by the job:
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

# Number of GPUs requested per node:
#SBATCH --gres=gpu:1
# The amount of memory in megabytes per node:
#SBATCH --mem=51200

# Use this email address:
#SBATCH --mail-user=zmu1@student.unimelb.edu.au

# Send yourself an email when the job:
# aborts abnormally (fails)
#SBATCH --mail-type=FAIL
# ends successfully
#SBATCH --mail-type=END

# The maximum running time of the job in days-hours:mins:sec
#SBATCH --time=00:30:00

# check that the script is launched with sbatch
if [ "x$SLURM_JOB_ID" == "x" ]; then
   echo "You need to submit your job to the queuing system with sbatch"
   exit 1
fi

# Run the job from the directory where it was launched (default)

moudle purge

# The modules to load:
module load Python/3.10.4
module load GCCcore/11.3.0
module load Pillow/9.1.1
module load TensorFlow/2.11.0-CUDA-11.7.0

source ~/venvs/venv-3.10.4/bin/activate

# The job command(s):
python lenet_3_Aug.py

##DO NOT ADD/EDIT BEYOND THIS LINE##
##Job monitor command to list the resource usage
my-job-stats -a -n -s
