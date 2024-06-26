#!/bin/sh

# Process a homozygous parent.
# Expect bam files that map homozygous reads to genes, best 1 per read.
# Expect map substrate was reference transcripts, not pilon consensus.
# Expect bam files ordered by read pair, so each read ID occurs twice.

# Expect parent names are MxM and SxS.
# Expect subdirectory like BR1 or BR2.
# Expect bam directory names like MxM_BR1 or SxS_BR2.
# Expect samtools is in the path.

analyze() {
    date
    BIOREP=$1
    PARENT=$2
    INPUT="HomozygousMap/${PARENT}_${BIOREP}/Primary.bam"
    OUTPUT="${BIOREP}/map_${PARENT}.csv"
    echo "input $INPUT output $OUTPUT"
    samtools view $INPUT | cut -f 1-3 | awk '{if ($1 != P) {P=$1; print $1 "," $3;}}' > $OUTPUT
    echo -n "exit status "; echo $?
}
analyze BR1 MxM 
analyze BR1 SxS
analyze BR2 MxM 
analyze BR2 SxS
analyze BR3 MxM 
analyze BR3 SxS
analyze BR4 MxM 
analyze BR4 SxS

date
echo "Done"
