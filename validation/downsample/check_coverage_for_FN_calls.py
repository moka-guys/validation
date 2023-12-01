import subprocess
import argparse
import sys
def get_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--benchmarking_results','-b',help='benchmarking_VCF')
    parser.add_argument('--sambamba_depth_results','-s',help='sambamba_depth_results')
    parser.add_argument('--FN_output_VCF','-f',help='output VCF for annotated false negative calls')
    parser.add_argument('--coverage_counts_output','-c',help='variant count at each coverage level')
    return parser.parse_args(args)

parsed_args=get_args(sys.argv[1:])
benchmarking_results = parsed_args.benchmarking_results
sambamba_depth_results = parsed_args.sambamba_depth_results
FN_output_VCF = parsed_args.FN_output_VCF
coverage_counts_output = parsed_args.coverage_counts_output

grep_cmd = "grep -m 1 %s\"$(printf '\\t')\"%s$(printf '\\t') '%s'"

coverage_dict= {"FN_SNV":{"unknown":0},"TP_SNV":{"unknown":0},"FN_indel":{"unknown":0},"TP_indel":{"unknown":0}}

with open(benchmarking_results) as fh:
	for line in fh.readlines():
		if not line.startswith("#"):
			CHROM,POS,ID,REF,ALT,QUAL,FILTER,INFO,FORMAT,TRUTH,QUERY = line.rstrip().split("\t")
			query_dict={}
			truth_dict={}
			for x,y in enumerate(FORMAT.split(":")):
				query_dict[y]=QUERY.split(":")[x]
				truth_dict[y]=TRUTH.split(":")[x]
			if truth_dict["BVT"] == "INDEL":
				# sambamba outputs depths with zero based numbering - so to get the correct sambamba depth for SNVs need to do POS -1 - not needed for indels due to left alignment
				sambamba_pos=int(POS)
			else:
				sambamba_pos=int(POS)-1
			#print query_dict["BD"]
			# GT = "Genotype"
			# BD = "Decision for call (TP/FP/FN/N)"
			# BK = "Sub-type for decision (match/mismatch type)"
			# BI = "Additional comparison information"
			# QQ = "Variant quality for ROC creation."
			# BVT = "High-level variant type (SNP|INDEL)."


			if truth_dict["BD"]=="FN":
				with open(FN_output_VCF,'a') as fn_vcf:
					#print(grep_cmd % (CHROM,sambamba_pos,sambamba_depth_results))
					proc = subprocess.Popen([grep_cmd % (CHROM,sambamba_pos,sambamba_depth_results)],stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True, executable="/bin/bash")
					out,err =proc.communicate()
					out = out.decode("utf-8")
					if len(str(out).split("\t")) == 10:
						depth_REF,depth_POS,COV,A,C,G,T,DEL,REFSKIP,SAMPLE=str(out).split("\t")
						QUERY = QUERY+":%s:%s:%s:%s:%s:%s" % (COV,A,C,G,T,DEL)
						if truth_dict["BVT"] == "INDEL":
							if str(COV) not in coverage_dict["FN_indel"]:
								coverage_dict["FN_indel"][str(COV)]=1
							else:
								coverage_dict["FN_indel"][str(COV)]+=1
						else:
							if str(COV) not in coverage_dict["FN_SNV"]:
								coverage_dict["FN_SNV"][str(COV)]=1
							else:
								coverage_dict["FN_SNV"][str(COV)]+=1
					else:			
						QUERY = QUERY+":.:.:.:.:.:."
						if truth_dict["BVT"] == "INDEL":
							coverage_dict["FN_indel"]["unknown"]+=1
						else:
							coverage_dict["FN_SNV"]["unknown"]+=1
					FORMAT = FORMAT +":DP:A:C:G:T:DEL"
					TRUTH = TRUTH+":.:.:.:.:.:."
					fn_vcf.write(("\t".join([CHROM,POS,ID,REF,ALT,QUAL,FILTER,INFO,FORMAT,TRUTH,QUERY+"\n"])))
					

			elif truth_dict["BD"]=="TP":
				#print(grep_cmd % (CHROM,sambamba_pos,sambamba_depth_results))
				proc = subprocess.Popen([grep_cmd % (CHROM,sambamba_pos,sambamba_depth_results)],stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True, executable="/bin/bash")
				out,err =proc.communicate()
				out = out.decode("utf-8")
				try:
					depth_REF,depth_POS,COV,A,C,G,T,DEL,REFSKIP,SAMPLE=str(out).split("\t")
					if truth_dict["BVT"] == "INDEL":
						if str(COV) not in ["TP_indel"]:
							coverage_dict["TP_indel"][str(COV)]=1
						else:
							coverage_dict["TP_indel"][str(COV)]+=1
					else:
						if str(COV) not in ["TP_SNV"]:
							coverage_dict["TP_SNV"][str(COV)]=1
						else:
							coverage_dict["TP_SNV"][str(COV)]+=1
				except:
					if truth_dict["BVT"] == "INDEL":
						coverage_dict["TP_indel"]["unknown"]+=1
					else:
						coverage_dict["TP_SNV"]["unknown"]+=1

with open(coverage_counts_output,'w') as count_file:
	count_file.write("TP SNVs\n")
	for i in coverage_dict["TP_SNV"]:
		count_file.write("%s\t%s\n" %(i,coverage_dict["TP_SNV"][i]))
	count_file.write("FN SNVs\n")
	for i in coverage_dict["FN_SNV"]:
		count_file.write("%s\t%s\n" %(i,coverage_dict["FN_SNV"][i]))
	count_file.write("TP indels\n")
	for i in coverage_dict["TP_indel"]:
		count_file.write("%s\t%s\n" %(i,coverage_dict["TP_indel"][i]))
	count_file.write("FN indels\n")
	for i in coverage_dict["FN_indel"]:
		count_file.write("%s\t%s\n" %(i,coverage_dict["FN_indel"][i]))


