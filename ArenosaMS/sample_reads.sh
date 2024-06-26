#!/bin/sh

COUNT=40000000

rm -v partial.*_trim.fq.gz

echo "Working"
for FILE in *_trim.fq.gz; do
    echo "$FILE"
    gunzip -c ${FILE} | head -n ${COUNT} | gzip > partial.${FILE}
done

echo "Done"
ls -l *.fq.gz

