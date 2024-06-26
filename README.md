# KCloud
## ArenosaMS
Our initial dataset. Parents M and S. Crosses MxS and SxM. Four biological replicates. Processed with Slurm on Saga.

### Compute the k-mer clouds
* run_meryl.sh - Count k-mers in one parent.
* run_diff.sh - Retain k-mers specific to one parent.
* run_intersect.sh - Retain k-mers from a cross also specific to one parent.

### Classify reads
* grid_mer_filter.sh - Submit a job to the grid for one biological replicate.
* individual_mer_filter.sh - Launch the Python with 5 parameters.
* mer_filter_reads.py - Stream a pair of fastq files, write a pair of IDs lists, one maternal, one paternal. 
