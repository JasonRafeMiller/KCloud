#!/bin/sh

# TO DO: use parameter for which BR

# expect parmeter like BR1 or BR2
BIOREP=$1
echo Replicate: ${BIOREP}
cd ${BIOREP}

# expect input files like distinct_mers.txt and SxM_BR1_R1_trim.fq.gz

sbatch --account=${ACCOUNT} ../individual_mer_filter.sh \
    SxM \
    IntersectSxM_SminusM/distinct_mers.txt \
    IntersectSxM_MminusS/distinct_mers.txt \
    SxM/SxM_${BIOREP}_R1_trim.fq.gz \
    SxM/SxM_${BIOREP}_R2_trim.fq.gz

sbatch --account=${ACCOUNT} ../individual_mer_filter.sh \
    MxS \
    IntersectMxS_MminusS/distinct_mers.txt \
    IntersectMxS_SminusM/distinct_mers.txt \
    MxS/MxS_${BIOREP}_R1_trim.fq.gz \
    MxS/MxS_${BIOREP}_R2_trim.fq.gz 

cd ..

echo 'Done'

