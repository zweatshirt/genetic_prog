# Author: Zachery Linscott

# Program purpose:
# This program takes a fastas file as input.
# The fasta file contains sequences which are peaks
# of whatever biosample was teested.
# These peaks indicate where the genome of the biosample
# is accessible.

# Starting at index 0 (not 1),
# every even line contains the 'metadata' of the sequence:
# The chromosome it comes from and the range of the feature of interest.
# Every odd line contains the actual nitrogenous bases of the sequence.

import os, sys
from pathlib import Path
import mod_seqs, file_mgmt, constants


def main():
    fasta_file = sys.argv[1]
    arg2 = sys.argv[2]
    fasta = fasta_file.split('/')[-1].split('.')[0]
    neg_file_name = f"{fasta}_negatives.bed"
    neg_file_name_two = f"{fasta}_clean_negatives.txt"
    pos_file_name = f"{fasta}_clean_positives.txt"

    # read the lines of the file passed in to arg 1
    seq_data = file_mgmt.read_file(fasta_file)
 
    # if the 2nd argument is 'pos' for positive, we want to clean the positive file and get info for the negative bed file.
    if arg2 == 'pos':

        print("Cleaning the data and finding the mean length of the accessible regions' sequences") 
        seqs, mean_seq_length = mod_seqs.clean_seq_data(seq_data)

        print("Trimming the sequences by the mean length")
        trimmed_seqs = mod_seqs.trim_sequences(seqs, mean_seq_length)

        # find the ranges between the positive/open/peak areas
        print("Finding the region between the positive ranges, which are innacessible")
        print("Additionally, chopping these regions to the length of the accessible regions' mean")
        negative_ranges = mod_seqs.grab_negative_ranges(seqs, mean_seq_length)

        neg_path = os.path.join(constants.NEG_BEDS_DIR, neg_file_name)
        print(f"The mean of {fasta} is {mean_seq_length}\n")
        #specifically create the negative fastas file
        file_mgmt.create_file(neg_path, negative_ranges)

        # cleaned positive sequences
        pos_path = os.path.join(constants.POS_CLEAN_DIR, pos_file_name)
        file_mgmt.create_file(pos_path, trimmed_seqs)

        mean_file = constants.PATH + f"/{fasta}_{constants.MEAN}"
        file_mgmt.write_file(mean_file, [str(mean_seq_length)])
    
    # if arg2 is the mean val printed above, 
    # we know to clean the negatives fastas file 
    # and chop the means to the same as the positive sequences.
    if arg2 == constants.MEAN:
        print("Trimming the negative sequences to the same length as the positive sequences.\n")
        mean = int(file_mgmt.read_file(f"{fasta}_{constants.MEAN}")[0])
        os.remove(f"{fasta}_{constants.MEAN}")
        seqs, neg_mean_seq_length = mod_seqs.clean_seq_data(seq_data)
        trimmed_seqs = mod_seqs.trim_sequences(seqs, mean)
        clean_negs_path = os.path.join(constants.NEG_CLEAN_DIR, neg_file_name_two)
        file_mgmt.create_file(clean_negs_path, trimmed_seqs)


if __name__ == "__main__":
    main()