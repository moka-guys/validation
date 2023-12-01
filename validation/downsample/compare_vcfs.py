"""
This script is to look at all the fale negatives from an benhcmarking VCF and look to see if they were also called as FN's in another benchmarking VCF (eg a non-downsapled one to see if it's just generally a difficult variant)
"""

#eg downsampled vcf
query_vcf="/home/aled/Documents/230424_seglhRD_downsampling/downsample_0.05/benchmarking/happy.NGS538A_08_136819_NA12878_U_WES91SKIN_Pan4940_S8_markdup_recalibrated_Haplotyper_FN_annotated_with_RD.vcf"
#original vcf
truth_vcf="/home/aled/Documents/230424_seglhRD_downsampling/no_downsampling/benchmarking/happy.NGS538A_08_136819_NA12878_U_WES91SKIN_Pan4940_S8_markdup_recalibrated_Haplotyper.vcf"

import subprocess
with open(query_vcf) as test_vcf:
	for line in test_vcf.readlines():
		if not line.startswith("#"):
			CHROM,POS,ID,REF,ALT,QUAL,FILTER,INFO,FORMAT,TRUTH,QUERY = line.rstrip().split("\t")
			grep_cmd = "grep -m 1 %s\"$(printf '\\t')\"%s$(printf '\\t') '%s'"
			proc = subprocess.Popen([grep_cmd % (CHROM,POS,truth_vcf)],stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True, executable="/bin/bash")
			out,err =proc.communicate()
			out = out.decode("utf-8")
			if out:
				print out
			# with open(truth_vcf) as truth_vcf_file:
			# 	for truth_line in truth_vcf_file.readlines():
			# 		if not truth_line.startswith("#"):
			# 			truthCHROM,truthPOS,truthID,truthREF,truthALT,truthQUAL,truthFILTER,truthINFO,truthFORMAT,truthTRUTH,truthQUERY = truth_line.rstrip().split("\t")
			# 			if truthCHROM == CHROM and truthPOS == POS:
			# 				print ("\t".join([CHROM,POS,QUERY,truthQUERY]))
						