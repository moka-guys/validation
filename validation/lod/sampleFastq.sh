#!/bin/bash

# subsamples two fastq files in varying proportion
# ================================================
# - uses reservoir sampling
# - output .gz writes new file else appends uncompressed

R1=${1}
R2=${2}
OUT1=${3}
OUT2=${4}
SZ=${5}

echo READ1 $R1
echo READ2 $R2
echo SIZE  $SZ

paste <(zcat ${R1}) <(zcat ${R2}) | awk \
	'{
		printf("%s",$0);
		n++;
		if(n%4==0) {
			printf("\n");
		} else { 
			printf("\t");
		}
	}' | awk -v k=${SZ} \
	'BEGIN {
		srand(systime() + PROCINFO["pid"]);
	}
	{
		s = x++ < k ? x-1 : int(rand() * x);
		if (s<k) {
			R[s]=$0;
		}
	}
	END {
		for(i in R) {
			print R[i];
		}
	}' | awk -F"\t" -v O1=${OUT1} -v O2=${OUT2} \
	'BEGIN {
		out1= O1 ~ /\.gz$/ ? "bgzip >"O1 : "cat >>"O1
		out2= O2 ~ /\.gz$/ ? "bgzip >"O2 : "cat >>"O2
	}
	{
		print $1"\n"$3"\n"$5"\n"$7 | out1
		print $2"\n"$4"\n"$6"\n"$8 | out2
	}'
