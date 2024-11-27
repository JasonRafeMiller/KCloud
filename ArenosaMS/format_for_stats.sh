#!/bin/sh

# Provide a parameter like BR1
REPLICATE=$1
echo "Biological Replicate: ${REPLICATE}"

# Assume python script is in same directory as shell script.
# Run this from a subdirectory such as BR1.

SSFILE=SxM_${REPLICATE}.mat.gene_counts.tsv
MMFILE=SxM_${REPLICATE}.pat.gene_counts.tsv
python ../format_for_stats.py $SSFILE $MMFILE SxM_${REPLICATE}.tsv

SSFILE=MxS_${REPLICATE}.pat.gene_counts.tsv
MMFILE=MxS_${REPLICATE}.mat.gene_counts.tsv
python ../format_for_stats.py $SSFILE $MMFILE MxS_${REPLICATE}.tsv

echo "done"
