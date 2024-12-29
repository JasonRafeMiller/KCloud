#!/bin/sh

replicate() {
    REP=$1
    cd ${REP}
    pwd
    sbatch --account=${ACCOUNT} ../make_fasta.sh SxM_${REP} 
    sbatch --account=${ACCOUNT} ../make_fasta.sh MxS_${REP} 
    cd ..
}

replicate "BR1"
replicate "BR2"
replicate "BR3"
replicate "BR4"

