#!/usr/bin/env bash

# Author: Zachery Linscott

# This file serves multiple (too many) functions.
# 1st: 
# It checks if miniconda3 is installed,
# and if it isn't, it calls env_setup.sh which initializes 
# the required conda env
#
# 2nd:
# The script attempts reinstalls bedtools due to a package issue
#
# 3rd: 
# The reference genome dir is removed if it exists 
# and copied to the working directory.
# 4th:
# The script runs the primary functions of creating clean, 
# equal length positive and negative files.

# 5th: It cleans the positive and negative sequence files to put them into train, test, validation files

# Example link to use: https://www.encodeproject.org/files/ENCFF870FOG/@@download/ENCFF870FOG.bed.gz

# initialize vars
bf="beds"
fastas="fastas"
positives="pos_clean"
bed_negatives="negs_beds"
fastas_negatives="negs_fastas"
negatives="negs_clean"
ref_origin="/proj/SIUE-CS590-490/reference/"
rf="reference"
mean="mean.txt"
drive="~/drive/zach" # necessary to get more space, worry about later 

if [ ! -d "../miniconda3" ]; then
    echo "Running env_setup.sh"
    source env_setup.sh
fi

# For some reason this has to be reran for the packages manager to recognize that bedtools has been installed.
echo "Runing sudo apt-get update again to ensure bedtools and gunzip can be installed correctly"
sudo apt-get install bedtools
sudo apt-get update

# the reference file can become corrupt, best to delete and recopy
if [ -d $rf ]; then
    rm -rf $rf
fi

# get the reference file. This can be improved
echo "Attempting to either cp the reference file if it exists or to download it. This may take a while..."
if cp -r $ref_origin .; then
    echo "cp of reference worked"
else
    echo "Unable to copy reference, need to download it..."
    mkdir reference && cd $_
    wget http://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz;
    gunzip hg38.fa.gz;
    cd ..;
fi



echo "Making directories..." 
mkdir $fastas $positives $bed_negatives $fastas_negatives $negatives data

if [ ! -d $bf ]; then
    echo "There is no bed files to read from, perhaps you forgot to run get_beds.sh"
    echo "Cleaning project space for next try..."
    rm -rf $file $fastas/$fasta_file $bed_negatives/$bed_negs_file $fastas_negatives/$fastas_negs_file $mean
    rm -rf $bf $fastas $bed_negatives $fastas_negatives reference
    rm -rf $positives $negatives
    echo "Bye."
    exit 1
fi


# get fasta files from the bed files
# I really wanted to do this in the prev loop, but gunzip doesn't provide the new name to stdout
for file in $bf/*; do
    # remove path from filename
    filename=$(basename "$file")
    echo "Working on ${filename%.*}"

    # create fastas filename and touch
    fasta_file="${filename%.*}.fa"
    touch $fastas/$fasta_file

    # taken care of by python script:
    # create clean positives filename and touch
    # positive_file="${filename%.*}_clean_positives.txt"
    # touch $positives/$positive_file

    # create negative bed filename
    bed_negs_file="${filename%.*}_negatives.bed"
    # the file is written by the python script, no need to touch
    # but we need the name for bedtools

    # convert bed file to fastas
    echo "Converting bed $file to a fasta file"
    bedtools getfasta -fi $rf/hg38.fa -bed $file -fo $fastas/$fasta_file
      
    # run py script to clean peak fastas data and get negative ranges 
    # writes the positive clean file and writes the negative bed file
    echo "Cleaning the $fasta_file and returning the mean"
    python3 python_scripts/main.py $fastas/$fasta_file pos

    # create neg. fasta file name and touch
    fastas_negs_file="${filename%.*}.fa"
    touch $fastas_negatives/$fastas_negs_file
    
    # get the negative fastas file given the negative bed file
    echo "Running getfasta on $bed_negs_file and sending to $fastas_negatives/$fastas_negs_file"
    bedtools getfasta -fi $rf/hg38.fa -bed $bed_negatives/$bed_negs_file -fo $fastas_negatives/$fastas_negs_file
    echo "Cleaning the $fastas_negs_file"
    python3 python_scripts/main.py $fastas_negatives/$fastas_negs_file $mean

    # saves space, discard these unneeded files asap
    rm -rf $file $fastas/$fasta_file $bed_negatives/$bed_negs_file $fastas_negatives/$fastas_negs_file $mean
done

python3 python_scripts/prep_seqs.py

# clean directory
rm -rf $bf $fastas $bed_negatives $fastas_negatives $rf

# python3 prep_seqs.py

# rm -rf $positives $negatives
