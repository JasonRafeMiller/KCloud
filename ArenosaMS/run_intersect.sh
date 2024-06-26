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
echo meryl greater
meryl greater-than 9 [intersect meryl_first.db meryl_second.db] output meryl_intersect.db
echo -n $?
echo " exit status"
date
echo meryl statistics
meryl statistics meryl_intersect.db > intersection.stats
echo -n $?
echo " exit status"
date
echo meryl print
meryl print meryl_intersect.db > distinct_mers.txt
echo -n $?
echo " exit status"
date

echo Done
