#!/bin/sh

# The minus order must be maternal paternal.

replicate() {
    REP=$1
    cd ${REP}
    pwd
    sbatch --account=${ACCOUNT} ../run_lookup.sh SxM ${REP} R1 SminusM MminusS
    sbatch --account=${ACCOUNT} ../run_lookup.sh SxM ${REP} R2 SminusM MminusS
    sbatch --account=${ACCOUNT} ../run_lookup.sh MxS ${REP} R1 MminusS SminusM
    sbatch --account=${ACCOUNT} ../run_lookup.sh MxS ${REP} R2 MminusS SminusM
    cd ..
}

replicate "BR1"
replicate "BR2"
replicate "BR3"
replicate "BR4"

