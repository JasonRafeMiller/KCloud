#!/bin/sh
#SBATCH --account=${ACCOUNT}
#SBATCH --job-name=mlookup
#SBATCH --time=4:00:00   
#SBATCH --mem-per-cpu=8G  
#SBATCH --cpus-per-task=4  
set -o errexit # exit on errors
#savefile *.tab

# Run this like this:
# cd BR3; sbatch --account=${ACCOUNT} ../run_lookup.sh 

echo $0 $@
echo "Expect 5 parameters like SxM BR3 R1 SminusM MminusS"
echo "Note order: maternal paternal."
if [[ $# -ne 5 ]] ; then
    echo "Parameters not specified."
    exit 1
fi
CROSS=$1
REPLICATE=$2
PAIRNUM=$3
MATERNAL=$4
PATERNAL=$5
echo "Processing ${CROSS}_${REPLICATE}_${PAIRNUM}"

echo "Test that meryl-lookup is installed and on the PATH"
meryl-lookup --version

DATABASE1=/cluster/work/users/jasonrm/Arenosa/Oct24.KCloud/${REPLICATE}/Intersect${CROSS}_${MATERNAL}/meryl_intersect.db
DATABASE2=/cluster/work/users/jasonrm/Arenosa/Oct24.KCloud/${REPLICATE}/Intersect${CROSS}_${PATERNAL}/meryl_intersect.db
echo "DATABASE 1 ${DATABASE1}"
echo "DATABASE 2 ${DATABASE2}"
ls -ld ${DATABASE1}
ls -ld ${DATABASE2}

INPUT=${CROSS}_${REPLICATE}_${PAIRNUM}.fasta.gz
OUTPUT=${CROSS}_${REPLICATE}_${PAIRNUM}.tab
echo "INPUT ${INPUT}"
ls -l ${INPUT}
echo "OUTPUT ${OUTPUT}"

date
meryl-lookup -existence -threads 4 -sequence ${INPUT} -output ${OUTPUT} -mers ${DATABASE1} ${DATABASE2}
echo -n $?; echo " exit status"
date

echo Done
