#!/bin/sh
#SBATCH --account=${ACCOUNT}
#SBATCH --job-name=makefast
#SBATCH --time=2:00:00   
#SBATCH --mem-per-cpu=4G  
#SBATCH --cpus-per-task=1  
set -o errexit # exit on errors
#savefile *.gz

# Submit this like this:
# cd BR3; sbatch --account=${ACCOUNT} ../make_fasta.sh MxS_BR3

echo $0 $@
echo "Expect read filename prefix like MxS_BR1."
if [[ $# -eq 0 ]] ; then
    echo "Filename required."
    exit 1
fi

READ_NAME=$1
echo "Filename ${READ_NAME}"

FASTQ_DIR=/cluster/projects/nn9525k/hybrids/jasonrm/Arenosa/Trimming/reads_combined
R1_FQ_FILE=${READ_NAME}_R1_trim.fq.gz
R2_FQ_FILE=${READ_NAME}_R2_trim.fq.gz
R1_FA_FILE=${READ_NAME}_R1.fasta
R2_FA_FILE=${READ_NAME}_R2.fasta

echo "Reading from..."
ls -l ${FASTQ_DIR}/${R1_FQ_FILE}

date
echo "Writing ${R1_FA_FILE} ..."
gunzip -c ${FASTQ_DIR}/${R1_FQ_FILE} | awk '{c++; if (c==1){print ">" substr($1,2);} if (c==2) {print $1;} if (c==4) c=0; }' > ${R1_FA_FILE}

date
echo "Writing ${R2_FA_FILE} ..."
gunzip -c ${FASTQ_DIR}/${R2_FQ_FILE} | awk '{c++; if (c==1){print ">" substr($1,2);} if (c==2) {print $1;} if (c==4) c=0; }' > ${R2_FA_FILE}

echo "zip..."
gzip --fast -v ${R1_FA_FILE}
gzip --fast -v ${R2_FA_FILE}

date
echo "Done"
