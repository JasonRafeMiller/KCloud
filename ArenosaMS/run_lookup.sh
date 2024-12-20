#!/bin/sh

DATABASE1=/cluster/work/users/jasonrm/Arenosa/Oct24.KCloud/BR1/IntersectMxS_MminusS/meryl_intersect.db
DATABASE2=/cluster/work/users/jasonrm/Arenosa/Oct24.KCloud/BR1/IntersectMxS_SminusM/meryl_intersect.db

INPUT=MxS_BR1_R1.fasta
OUTPUT=MxS_BR1_R1.tab

date; meryl-lookup -existence -threads 4 -sequence ${INPUT} -output ${OUTPUT} -mers ${DATABASE1} ${DATABASE2}
echo -n $!; echo " exit status"; date

INPUT=MxS_BR1_R2.fasta
OUTPUT=MxS_BR1_R2.tab

date; meryl-lookup -existence -threads 4 -sequence ${INPUT} -output ${OUTPUT} -mers ${DATABASE1} ${DATABASE2}
echo -n $!; echo " exit status"; date

echo Done
