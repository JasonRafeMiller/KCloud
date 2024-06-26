#!/bin/sh
module --force purge
module load StdEnv 
module load GCC/11.3.0
module load canu/2.2-GCCcore-11.3.0
module list

echo
echo meryl version
which meryl

date
echo meryl greater than
meryl greater-than 1 [difference meryl_first.db meryl_second.db] output meryl_diff.db
echo -n $?
echo " exit status"
echo meryl statistics
meryl statistics meryl_diff.db > difference.stats
echo -n $?
echo " exit status"

date
echo Done
