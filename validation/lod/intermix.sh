#!/usr/bin/sh

# Intermixes two pairs of fastq files

F1R1=${1}
F1R2=${2}
F2R1=${3}
F2R2=${4}
OUT=${5}
STEP=${6:-10}
SIZE=${7:-1000000}

mkdir -p $OUT

for s in $(seq -w 0 ${STEP})
do
	#PROP=$(bc -l <<< "${SIZE}*${s}/${STEP}")
	# have octal error when reach step > 07 so prefix $s with 10# to force bash to consider as decimal
	PROP1=$((${SIZE}*10#${s}/${STEP}))
	PROP2=$((${SIZE}-${PROP1}))
	echo "*** STEP ${s} *** (${PROP1} ${PROP2})"
	OR1="${OUT}/MIX${s}_S${s}_L001_R1_001.fastq"
	OR2="${OUT}/MIX${s}_S${s}_L001_R2_001.fastq"
	rm -f $OR1 $OR2
	./sampleFastq.sh $F1R1 $F1R2 $OR1 $OR2 $PROP1
	./sampleFastq.sh $F2R1 $F2R2 $OR1 $OR2 $PROP2
	bgzip $OR1
	bgzip $OR2
done
