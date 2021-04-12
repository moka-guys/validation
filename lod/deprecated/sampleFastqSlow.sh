#!/bin/sh

### This very ugly and inefficiecnt script resamples entires from a pair of fastq files

FQ1=${1}
FQ1R=${2}
FQ2=${3}
FQ2R=${4}
LINES=${5}

# set intermediary files
echo "-- RESAMPLING COMPRESSED FASTQ PAIR TO ${LINES} --"
echo "   ${FQ1} -> ${FQ1R}"
echo "   ${FQ1} -> ${FQ1R}"
echo
echo "Decompressing..."
gunzip -c "${FQ1}" > ${FQ1R%.*}
gunzip -c "${FQ2}" > ${FQ2R%.*}

echo "Downsampling to ${LINES}..."
paste ${FQ1R%.*} ${FQ2R%.*} |
awk '{ printf("%s",$0); n++; if(n%4==0) { printf("\n");} else { printf("\t\t");} }' |
shuf |
head -n $LINES |
perl -pe 's/\t\t/\n/g' |
awk -F '\t' '{print $1 > "'${FQ1R%.*}.tmp'"; print $2 > "'${FQ2R%.*}.tmp'"}'

##check if success
if [ -f "${FQ1R%.*}.tmp" ] && [ -f "${FQ2R%.*}.tmp" ];then
	mv ${FQ1R%.*}.tmp ${FQ1R%.*}
	mv ${FQ2R%.*}.tmp ${FQ2R%.*}

	echo "Compressing..."
	gzip -f ${FQ1R%.*} ${FQ2R%.*}

	echo "DONE"
	exit 0
else
	rm -f ${FQ1R%.*} ${FQ2R%.*}
	echo "FATAL: Failed to resample fastq files"
	exit 1
fi
