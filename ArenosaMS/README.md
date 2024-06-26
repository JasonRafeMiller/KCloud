# ArenosaMS
Our initial dataset. Parents M and S. Crosses MxS and SxM. Four biological replicates. Processed with Slurm on Saga.

## Directory Layout
* BR1 (and similar for BR2, BR3, BR4: 4 total)
  * MxM (and similar for SxS, MxS, SxM)
    * MxM_BR1_R1_trim.fq.gz (soft link)
    * MxM_BR1_R2_trim.fq.gz (soft link)
    * meryl_all.db
    * meryl_distinct.db
  * SminusM (and similar for MminusS: 2 total)
    * meryl_first.db -> ../SxS/meryl_distinct.db (soft link)
    * meryl_second.db -> ../MxM/meryl_distinct.db (soft link(
    * meryl_diff.db
  * IntersectSxM_SminusM (and similar for MxS and MminusS: 4 total)
    * meryl_first.db -> ../SxM/meryl_distinct.db (soft link)
    * meryl_second.db -> ../SminusM/meryl_diff.db (soft link)
    * meryl_intersect.db  
