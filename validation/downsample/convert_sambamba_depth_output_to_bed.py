input_file="/home/aled/Documents/230424_seglhRD_downsampling/min20/NGS531A_08_136819_NA12878_U_WES90SKIN_Pan4940_S8_markdup_min20.depth_output"
output_file="/home/aled/Documents/230424_seglhRD_downsampling/min20/NGS531A_08_136819_NA12878_U_WES90SKIN_Pan4940_S8_markdup_min20.unmerged.bed"
with open(output_file,'w') as output_fh:
	with open (input_file) as input_fh:
		for line in input_fh.readlines()[1:]:
			REF,POS,COV,A,C,G,T,DEL,REFSKIP,SAMPLE = line.split("\t")
			if REF in ["X","Y","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22"]:
				output_fh.write("%s\t%s\t%s\n" % (REF, POS,str(int(POS)+1)))
