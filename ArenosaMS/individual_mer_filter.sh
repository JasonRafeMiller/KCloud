#!/bin/sh
#SBATCH --account=${ACCOUNT}
#SBATCH --job-name=merfilter
#SBATCH --time=24:00:00   # Jobs require over 12 hr
#SBATCH --mem-per-cpu=8G  # Usually 3-6
#SBATCH --cpus-per-task=1  #
set -o errexit # exit on errors
# Our python will generate smaller Aligned.bam which we keep.
#savefile *.txt
#savefile *.out

echo MODULES
module --force purge
module load StdEnv 
module load GCC/11.3.0
#module load Bowtie2/2.4.5-GCC-11.3.0
#module load SAMtools/1.16.1-GCC-11.3.0
module load Python/3.10.4-GCCcore-11.3.0
module list

echo
echo LD_LIBRARY_PATH $LD_LIBRARY_PATH
echo

date
INITIALDIR=`pwd`
echo INITIALDIR ${INITIALDIR}
echo

date
python --version
pwd

# TO DO: accomplish mat and pat in one step

echo
echo Filter Reads
echo $1
echo $2
echo $3
echo $4
echo $5
ls -l ../mer_filter_reads.py
ls -l
date
python ../mer_filter_reads.py $1 $2 $3 $4 $5

echo -n $?
echo ' exit status'
ls -l
date

# TO DO: verify the two sets of IDs have null intersection.

echo Done

