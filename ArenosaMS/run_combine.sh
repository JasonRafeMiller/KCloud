#!/bin/sh

#SBATCH --account=${ACCOUNT}
#SBATCH --job-name=mcombine
#SBATCH --time=2:00:00   
#SBATCH --mem-per-cpu=4G  
#SBATCH --cpus-per-task=1  
set -o errexit # exit on errors
#savefile *.txt

# Run this like this:
# cd BR3; sbatch --account=${ACCOUNT} ../run_combine.sh SxM BR3

echo $0 $@
echo "Expect 2 parameters like SxM BR3"
if [[ $# -ne 2 ]] ; then
    echo "Parameters not specified."
    exit 1
fi
CROSS=$1
REPLICATE=$2
echo "Processing ${CROSS}_${REPLICATE}"

echo "Assume tab files show mers in common with 2 databases in this order: maternal paternal."

echo "Will run this program:"
ls -ls ../combine_meryl_reads.py

python --version
python ../combine_meryl_reads.py ${CROSS}_${REPLICATE}_R1.tab ${CROSS}_${REPLICATE}_R2.tab ${CROSS}_${REPLICATE}.maternal.txt ${CROSS}_${REPLICATE}.paternal.txt
echo -n $? ; echo " exit status"
echo Done
