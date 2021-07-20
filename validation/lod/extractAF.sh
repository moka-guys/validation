#!/bin/sh

# input data must be representative of the variants considered for clinical interpretation (PASS, on target, coverage reuqirement)

# processed vcf and creates CSV table for R
# - decompose variants
# - filter for PASS variants
# - index
# - merge
# - extract AF
# - convert to CSV

VCFS=$@

ALL=()
SAMPLES=()

AF="AF"

# decompose and filter
for f in $VCFS
do
	PROCESSED=$f.gz
	vt decompose $f | bcftools view -f PASS -o $PROCESSED -Oz
	tabix -f -p vcf $PROCESSED
	ALL+=("$PROCESSED")
	SAMPLE=$(grep "^#CHROM" $f | cut -f10)
	SAMPLES+=("$SAMPLE")
done

# Sort samples and join
IFS=$'\n' SORTED=($(sort <<<"${SAMPLES[*]}"));unset IFS
function join_by { local IFS="$1"; shift; echo "$*"; }
SAMPLESTRING=$(join_by , "${SORTED[@]}")

bcftools merge -m none -Ob ${ALL[@]} | \
	bcftools annotate -x "INFO,^FORMAT/${AF}" | \
	bcftools view -s $SAMPLESTRING | \
	grep -v "^##" | \
	awk 'BEGIN {OFS="\t"}{print $1":"$2":"$4":"$5,$0}' | \
	cut -f1,11-
