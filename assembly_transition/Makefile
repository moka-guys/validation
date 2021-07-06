# installation makefile

DOWNLOAD=resources

# reference download 
genome: human_g1k_v37.fasta human_g1k_v37.fasta.fai

human_g1k_v37.fasta:
	cd $(DOWNLOAD) && \
	wget -qO- ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/human_g1k_v37.fasta.gz | \
	gzip -dcq | cat > human_g1k_v37.fasta && rm -f human_g1k_v37.fasta.gz

human_g1k_v37.fasta.fai:
	cd $(DOWNLOAD) && \
	wget -c ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/human_g1k_v37.fasta.fai

GCA_00001405.15_GRCh38_no_alt_analysis_set.fasta:
	cd $(DOWNLOAD) && \
	wget -qO- ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz | \
	gzip -dcq | cat > GCA_00001405.15_GRCh38_no_alt_analysis_set.fasta && rm -f GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz



# BWA indexing
genome-index: human_g1k_v37.bowtie.MANIFEST

human_g1k_v37.bowtie.MANIFEST:
	cd $(ZIPPYRESOURCES) && \
	bowtie2-build human_g1k_v37.fasta human_g1k_v37.bowtie && \
	ls -l human_g1k_v37.bowtie.* > human_g1k_v37.bowtie.MANIFEST



# dbSNP atuff
annotation: 00-common_all.vcf.gz 00-common_all.vcf.gz.tbi refGene

00-common_all.vcf.gz:
	cd $(ZIPPYRESOURCES) && \
	wget -c ftp.ncbi.nlm.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/VCF/00-common_all.vcf.gz

00-common_all.vcf.gz.tbi:
	cd $(ZIPPYRESOURCES) && \
	wget -c ftp.ncbi.nlm.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/VCF/00-common_all.vcf.gz.tbi



# refGene (GRCh37)
refGene:
	cd $(ZIPPYRESOURCES) && \
	mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -N -D hg19 -P 3306 \
	 -e "SELECT DISTINCT r.bin,CONCAT(r.name,'.',i.version),c.ensembl,r.strand, r.txStart,r.txEnd,r.cdsStart,r.cdsEnd,r.exonCount,r.exonStarts,r.exonEnds,r.score,r.name2,r.cdsStartStat,r.cdsEndStat,r.exonFrames FROM refGene as r, hgFixed.gbCdnaInfo as i, ucscToEnsembl as c WHERE r.name=i.acc AND c.ucsc = r.chrom ORDER BY r.bin;" > refGene
