# Downsampling to assess performance of variant caller

This is commonly done to provide some evidence to assert that any cutoffs,such as a requirement for a region to be covered at 20X to pass QC is valid.

There are a few approaches that have been taken historically, such as using reported variants in a sample and using the read depth at that site to determine the downsample rate (1 variant per sample) or by using NA12878, downsampling at a generic level and then working out which variants have the required depth.

This repository contains some code which could be used/repurposed for future experiments. They should not be expected to work out the box, but (hopefully) limited modifications are required.

## overview of steps commonly performed.
* Downsample BAM - (calculate downsample rate)
* Call variants
* Confirm depth matches expected
* Benchmark results
* Assess benchmarking result

## seglh_rd downsample process
* Downsample BAM
* run senteion variant calling
* Calculate sambamba depth base on downsampled BAMs to create a BED file with the regions that have the target coverage (convert_sambamba_depth_output_to_bed.py)
* run benchmarking tool
* Assess benchmarking outputs

### Investigating false negatives
It should be remembered that WES samples do not have 100% sensitivity.


## scripts
### check_coverage_for_FN_calls.py:

Takes 4 args:
-b = benchmarking vcf
-s = sambamba depth output
-f = path for annotated VCF output 
-c = path for count summary output

For each FN in benchmarking VCF it will grep for that coordinate in sambamba_depth_output file.
It will produce a VCF with each variant annotated with the counts of each allele.

It also outputs a variant count, with 2 columns, first column is the read depth and the second column is the count of variants with that depth. This is reported for each of TP_SNVs, FN_SNVs, TP_SNVs, FN_indels 

### Compare_vcfs:
Compares FN from one downsampling experiment with another VCF (eg without any downsampling) to assess if variant is consistently missed
Note this is probably best compared with the VCF from NA12878 sample without any downsampling.

### Convert_sambamba_depth_output_to_bed.py
Converts the sambamba_depth_output file into a BED file for use with benchmarking tool.

### assess_FN_at_higherRD.py
Not sure this script was ever finished/tested. I think it takes the annotated FN vcf (from check_coverage_for_FN_calls.py) and identifies if it was found in the original benchmarking result  (230424_seglhRD_downsampling/original/benchmarking_with_no_BEDfile)
