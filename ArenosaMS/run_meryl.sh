#!/bin/sh
#SBATCH --account=${ACCOUNT}
#SBATCH --job-name=meryl
#SBATCH --time=04:00:00   # meryl takes about 35 minutes
#SBATCH --mem-per-cpu=4G  # 16 GB total
#SBATCH --cpus-per-task=4  # 4 cpu is optimal for 4 threads
set -o errexit # exit on errors
#savefile *.db

echo MODULES
module --force purge
module load StdEnv 
module load GCC/11.3.0
module load canu/2.2-GCCcore-11.3.0
# Would conflict with Bowtie: Python/3.10.8-GCCcore-12.2.0 SAMtools/1.17-GCC-12.2.0
module list

echo
echo meryl version
which meryl

echo
echo LD_LIBRARY_PATH $LD_LIBRARY_PATH
echo

THREADS=4
echo THREADS $THREADS

date
INITIALDIR=`pwd`
echo INITIALDIR ${INITIALDIR}
echo
ls -l
echo

R1=*_R1_*.fq.gz
R2=*_R2_*.fq.gz
echo R1 ${R1}
echo R2 ${R2}
echo

echo run meryl all
meryl count k=16 threads=4 ${R1} ${R2} output meryl_all.db
echo -n $?
echo " exit status"
date

echo run meryl all
meryl greater-than 1 threads=4 meryl_all.db output meryl_distinct.db
echo -n $?
echo " exit status"
date

echo reports
meryl statistics meryl_all.db > all.stats
meryl statistics meryl_distinct.db > distinct.stats

ls -l
echo DONE

# TO DO: do away with meryl_all ?
