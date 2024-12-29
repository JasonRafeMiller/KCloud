#!/bin/sh

# The minus order must be maternal paternal.

replicate() {
    REP=$1
    cd ${REP}
    pwd
    sbatch --account=${ACCOUNT} ../run_combine.sh SxM ${REP} 
    sbatch --account=${ACCOUNT} ../run_combine.sh MxS ${REP} 
    cd ..
}

replicate "BR1"
replicate "BR2"
replicate "BR3"
replicate "BR4"

