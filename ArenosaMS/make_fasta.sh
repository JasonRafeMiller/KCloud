#!/bin/sh

echo "Expect read filename prefix like MxS_BR1"

READ_NAME=$1
echo "Found ${READ_NAME}"

FASTQ_DIR=/cluster/projects/nn9525k/hybrids/jasonrm/Arenosa/IRP_run/Trimmed
R1_FQ_FILE=${READ_NAME}_R1_trim.fq.gz
R2_FQ_FILE=${READ_NAME}_R2_trim.fq.gz
R1_FA_FILE=${READ_NAME}_R1.fasta
R2_FA_FILE=${READ_NAME}_R2.fasta

date
echo "Writing ${R1_FA_FILE} ..."
gunzip -c ${FASTQ_DIR}/${R1_FQ_FILE} | awk '{c++; if (c==1){print ">" substr($1,2);} if (c==2) {print $1;} if (c==4) c=0; }' > ${R1_FA_FILE}

date
echo "Writing ${R2_FA_FILE} ..."
gunzip -c ${FASTQ_DIR}/${R2_FQ_FILE} | awk '{c++; if (c==1){print ">" substr($1,2);} if (c==2) {print $1;} if (c==4) c=0; }' > ${R2_FA_FILE}

date
echo "Done"
