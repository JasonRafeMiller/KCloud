#!/bin/sh
IRP=/cluster/work/users/jasonrm/Arenosa/HeterozygousDiff2
MER=/cluster/work/users/jasonrm/Arenosa/MerCounts/predictions


analyze() {
    DATA=$1
    echo $DATA
    FILE1=sorted.${DATA}.IDs.txt
    FILE2=sorted.${DATA}.IDs.txt
    #FILE1=`echo ${FILE1} | sed 's\.BR\_BR\g' ` 
    echo IRP
    echo $FILE1
    wc -l ${IRP}/${FILE1}
    echo KPart
    echo $FILE2
    wc -l ${MER}/${FILE2}
    echo InCommon
    comm -1 -2 ${IRP}/${FILE1} ${MER}/${FILE2} | wc -l
}    

analyze 'SxM_BR1.mat'
analyze 'SxM_BR1.pat'
analyze 'SxM_BR2.mat'
analyze 'SxM_BR2.pat'
analyze 'SxM_BR3.mat'
analyze 'SxM_BR3.pat'
analyze 'SxM_BR4.mat'
analyze 'SxM_BR4.pat'

analyze 'MxS_BR1.mat'
analyze 'MxS_BR1.pat'
analyze 'MxS_BR2.mat'
analyze 'MxS_BR2.pat'
analyze 'MxS_BR3.mat'
analyze 'MxS_BR3.pat'
analyze 'MxS_BR4.mat'
analyze 'MxS_BR4.pat'

echo done
