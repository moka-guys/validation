---
title: "Limit of detection"
author: "David Brawand"
date: "07/04/2021"
output:
  pdf_document:
    toc: true
    highlight: zenburn
---

# Limit of detection

LOD is measured with a virtual sample titration approach. Any samples can be used, as long as their variation content is significantly disparate (non-overlapping).

There is no requirement for a truth set in this assay as it relies on repeatability of variant detection within the same methodology rather than orthogonal testing.

## Suggested approach
Select one or more standardised read depths (total read counts).

## Procedure

1. Intermix samples at a selected resolution (eg 10% steps)
2. Process through secondary analysis
3. Merge VCF files and create input data
4. Plot Series of VAF for each variant in union of two samples
5. Define LOD

### Intermix
Intermix 2 samples with the `intermix.sh` script.
Eg. `./intermix.sh s1_R1.fastq.gz s1_R2.fastq.gz s2_R1.fastq.gz s2_R2.fastq.gz test 10 1000000`
This will create a folder `test` with the intermixed FASTQ files in 1/10 dilutions and 1000000 read pairs each.

### Process through secondary analysis
Process those intermixed samples through the secondary analysis pipelines

### Merge VCF
merge all VCF output into a single file and extract the AF matrix with the `extractAF.py` script.
Eg. `find data -name "*.vcf" | xargs ./extractAF.sh | sed 's/\t\./\tNA/g' > data.tsv`

### R analysis
Run the `lod.R` script which will run the LOD analysis. It will impute missing AF which allow to derive a LOD AF at the given read depth.
The data is saved in `lod.RData` (this file will be overwritten if the analysis is rerun).

Make sure to specific a minimum average read depth for the included variants.



