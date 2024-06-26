# KCloud
Targets trio sequencing of same-species crosses.   
Assumes Illumina paired-end RNA-seq data.   
Depends on sequence alignments for assigning reads to genes.   
Depends on k-mer analysis for assigning reads to either parent.   
Uses bam files from e.g. the Bowtie2 sequence aligner.   
Uses samtools to read bam files.   
Uses the k-mer analysis module "meryl" of the Canu genome assembler.  
Generates and uses the meryl.db databases from meryl.   

## ArenosaMS
Our initial dataset.
