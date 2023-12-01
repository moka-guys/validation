## step 1 - pull out false negatives where the read depth was between 10 and 20.
## step 2 - exclude variants that were also not called in the non-downsampled benchmarking result
## step 3 - calculate coverage of variants
## step 4 - look to see if the remaining variants were detected when the read depth was > 20

import argparse
import sys
def get_args(args):
	parser = argparse.ArgumentParser()
	parser.add_argument('--benchmarking_results','-b',help='original_benchmarking_VCF')
	#parser.add_argument('--sambamba_depth_results','-s',help='sambamba_depth_results')
	parser.add_argument('--FN_VCF','-f',help='output VCF for annotated false negative calls')
	#parser.add_argument('--coverage_counts_output','-c',help='variant count at each coverage level')
	return parser.parse_args(args)

parsed_args=get_args(sys.argv[1:])
original_benchmarking_VCF = parsed_args.benchmarking_results
#sambamba_depth_results = parsed_args.sambamba_depth_results
FN_output_VCF = parsed_args.FN_VCF
#coverage_counts_output = parsed_args.coverage_counts_output

false_negative_variants = {}
with open(FN_output_VCF) as fn_vcf:
	for line in fn_vcf.readlines():
		if not line.startswith("#"):
			  CHROM,POS,ID,REF,ALT,QUAL,FILTER,INFO,FORMAT,TRUTH,QUERY = line.rstrip().split("\t")
			  false_negative_variants[(CHROM,POS)] = {"CHROM":CHROM,"POS":POS,"ID":ID,"REF":REF,"ALT":ALT,"QUAL":QUAL,"FILTER":FILTER,"INFO":INFO,"FORMAT":FORMAT,"TRUTH":TRUTH,"QUERY":QUERY}
print false_negative_variants


for FN_variant in false_negative_variants:
	fn_chrom,fn_pos=FN_variant
	print(FN_variant)
	benchmark_line_dict={}
	found=False
	with open(original_benchmarking_VCF) as benchmarked_vcf:
		for line in benchmarked_vcf.readlines():
			if not line.startswith("#"):
				CHROM,POS,ID,REF,ALT,QUAL,FILTER,INFO,FORMAT,TRUTH,QUERY = line.rstrip().split("\t")
				if str(fn_chrom) == str(CHROM) and int(fn_pos)==int(POS):
					found=True
					# print (FN_variant, "match")
					keys=FORMAT.split(":")
					for element,value in enumerate(keys):
						benchmark_line_dict[value] = QUERY.split(":")[element]
						# print(value,QUERY.split(":")[element])
		
	if found:
		print (fn_chrom,fn_pos,benchmark_line_dict["BD"])
	else:
		print ("FN variant %s:%s not found in original benchmarking" % (fn_chrom,fn_pos))


