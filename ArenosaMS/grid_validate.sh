#!/bin/sh

# Process a homozygous parent like a heterozygous cross.
# Expect 100% of reads are mat (or pat).

# Required parameter is directory name like BR1.
# Expect current directory has the scripts and B1.
# Scripts will run in BR1 and use SxS and MxM subdirectories.
# Expect output files in the BR1 directory.

# Full runs can take > 24 hours.
# Instead, sample down to temp files.
# Prior to running this, create the "partial" fq files.

# expect parmeter like BR1 or BR2
echo Script name: $0
echo $# arguments 
if [ "$#" -ne 1 ]; then
    echo "Missing parameter like BR1"
    exit 1
fi
BIOREP=$1
echo Biological Replicate: ${BIOREP}
cd ${BIOREP}

# expect input files like distinct_mers.txt and SxS_BR1_R1_trim.fq.gz

# The five parameters: RUN_NAME MAT_KMERS PAT_KMERS FASTQ1 FASTQ2')

sbatch --account=${ACCOUNT} ../individual_mer_filter.sh \
    S_SxM \
    IntersectSxM_SminusM/distinct_mers.txt \
    IntersectSxM_MminusS/distinct_mers.txt \
    SxS/partial.SxS_${BIOREP}_R1_trim.fq.gz \
    SxS/partial.SxS_${BIOREP}_R2_trim.fq.gz

sbatch --account=${ACCOUNT} ../individual_mer_filter.sh \
    M_SxM \
    IntersectSxM_SminusM/distinct_mers.txt \
    IntersectSxM_MminusS/distinct_mers.txt \
    MxM/partial.MxM_${BIOREP}_R1_trim.fq.gz \
    MxM/partial.MxM_${BIOREP}_R2_trim.fq.gz 

sbatch --account=${ACCOUNT} ../individual_mer_filter.sh \
    S_MxS \
    IntersectMxS_MminusS/distinct_mers.txt \
    IntersectMxS_SminusM/distinct_mers.txt \
    SxS/partial.SxS_${BIOREP}_R1_trim.fq.gz \
    SxS/partial.SxS_${BIOREP}_R2_trim.fq.gz

sbatch --account=${ACCOUNT} ../individual_mer_filter.sh \
    M_MxS \
    IntersectMxS_MminusS/distinct_mers.txt \
    IntersectMxS_SminusM/distinct_mers.txt \
    MxM/partial.MxM_${BIOREP}_R1_trim.fq.gz \
    MxM/partial.MxM_${BIOREP}_R2_trim.fq.gz 

cd ..

echo 'Done'

