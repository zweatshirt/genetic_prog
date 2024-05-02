# Author: Zachery Linscott
# This file serves as a collection of useful functions
# that are utilized by main.py and prep_seqs.py
# the two primary driver files for the cleaning process.
import constants
import numpy as np
from prompts import print_progress


# UPDATED:
# Trims the sequences for each bedfile that are larger than the mean,
# and discards any sequence that is shorter than the mean
def trim_sequences(seqs, mean_seq_length):
    trimmed_seqs = []
 
    for seq in seqs:
        # discard/continue if the sequence's length is less than the mean
        if seq[3] < mean_seq_length:
            continue
        # if the sequence's length is greater than or equal to the mean
        if seq[3] >= mean_seq_length:
            # if it is equal, append and continue
            if seq[3] == mean_seq_length:
                trimmed_seqs.append(seq)
                continue
            # if the seq length is greater than the mean,
            # chop the sequence to the mean length
            seq[3] = mean_seq_length
            seq[4] = seq[4][:mean_seq_length]
            trimmed_seqs.append(seq)

    return trimmed_seqs


def grab_negative_ranges(seqs, pos_mean):
    ranges = []
    for i in range(1, len(seqs)):
        # e.g. if seqs[i - 1] is from chr1, and seqs[i] is from chr2
        # we want to continue
        if seqs[i - 1][0] != seqs[i][0]:
            continue
        # start of negative range is end + 1 of current peak
        # end of negative range is start - 1 of next peak
        start = seqs[i - 1][2] + 1
        end = seqs[i][1] - 1
        if start >= end: # avoids invalid ranges
            continue
        # chops the end if it is greater than the mean length
        # mostly for optimization purposes
        if end > start + pos_mean:
            end = start + pos_mean
        ranges.append([seqs[i][0], start, end])
        
    return ranges


# get sequences and sequence lengths
def clean_seq_data(lines):
    seqs = [None]
    line_count = 0
    # Every two lines in the file is info about one sequence
    # 1st line: chromosome number and range of the peak
    # 2nd line: actual sequence
    seq_count = 0
    # running sum of all the lengths of the peaks
    length_sum = 0
    for line in lines:
        if line_count % 2 == 0:
            seq_info, length_sum = grab_seq_info(line, length_sum)
            if line_count == 0:
                seqs[line_count] = seq_info
            else:
                seqs.append(seq_info)
            seq_count += 1
        else: 
	    # we want to keep the line and its info together.
            seqs[seq_count - 1].append(line)
        line_count += 1
    return seqs, length_sum // seq_count    


# returns a list of info about the passed in sequence/peak
def grab_seq_info(line, length_sum):
    line = line.split(':')
    chromosome_num = line[0].replace('>', '') # e.g. chr1, chr2, chrX, chrY
    region = line[1].split('-') # region of the feature of interest
    start = int(region[0]) # start of feature region
    end = int(region[1]) # end of feature region
    length = end - start # lenght of the feature's region
    length_sum += length #used for calculating mean of region lengths
    return [chromosome_num, start, end, length], length_sum


# very similar to the trim_sequences method,
# however the shape of the data is just slightly different
# if I had hindsight, I would get rid of the other trim_sequences function
# If the length of a sequence is greater than the mean, chop it to equal
# the length of the mean
# else discard the sequence
def trim_composite(seqs, mean_of_means):   
        trimmed_seqs = []
        for seq in seqs:
            if len(seq) < mean_of_means:
                continue
            if len(seq) > mean_of_means:
                seq = seq[:mean_of_means]
                trimmed_seqs.append(seq)
        
        return trimmed_seqs


# joins the sequence and its label into one string for file writing
# only necessary in writing to shuffled_data.txt
# bad code, change to: return ["\t".join(seq) for seq in seqs]
def str_join(seqs):
        to_write = []
        [to_write.append("\t".join(seq)) for seq in seqs]

        return to_write


# adds labels to the data
# 1 means the sequence is positive (from an accessible region in a genome)
# 0 means the sequence is negative (from an innaccessible region in a genome)
def add_labels(sequences, positive=True):
        # 1 for positives
        if positive:
            return [["1", seq] for seq in sequences]
        # 0 for negatives
        return [["0", seq] for seq in sequences]


def equalize_lengths(lst1, lst2):
        # write code to chop whichever list is longer
        if len(lst1) > len(lst2):
            lst1 = lst1[:len(lst2)]
        else: 
            lst2 = lst2[:len(lst1)]
        return lst1, lst2


# convert from lists to numpy arrs
def one_hot_encode(sequences):
    # sequence data takes the form [label, sequence]
    nucleos = ['A', 'T', 'C', 'G'] # bases
    seq_length = len(sequences[0][1])
    seqs_len = len(sequences)
    new_sequences = np.empty(shape=(seqs_len, 2), dtype=object) # label, sequence
    for idx, seq in enumerate(sequences):
        new_sequence = np.empty(shape=(4, seq_length), dtype=np.float32)
        for nidx, n in enumerate(nucleos):
            for cnt, nucleo in enumerate(seq[1]):
                if nucleo.casefold() == n.casefold():
                    new_sequence[nidx][cnt] = 1
                else:
                    new_sequence[nidx][cnt] = 0
        new_sequences[idx] = [np.float32(seq[0]), new_sequence]
        print_progress(idx, seqs_len - 1)
    return new_sequences


def percentage(idx, length):
    print(f"{round((idx / length) * 100, 2)}%")
   
    
