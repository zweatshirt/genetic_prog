# Author: Zachery Linscott

# Program purpose:
# This is essentially main 2.0
# This takes the files main.py produces whcih are full of cleaned and chopped sequences,
# then it finds the means for each of these files, and chops all of the sequences 
# from every file by the mean of these means.
# Next, the sequences are shuffled and added to a single text file.
# Will add one-hot-encoding.

import os, random
import file_mgmt, mod_seqs, prompts, constants


def prep_seqs():

        # Make data directory for test, train, and validation files if it failed to happen in prep.sh
        if not os.path.isdir(constants.DATA):
                os.mkdir(constants.DATA)
        
        pos_data = []
        negs_data = []
        pos_dir = os.listdir(os.path.join(os.getcwd(), constants.POS_CLEAN_DIR))
        negs_dir = os.listdir(os.path.join(os.getcwd(), constants.NEG_CLEAN_DIR))

        mean_lst = [] # collect mean length of each file

        # these are necessary to get the mean of the means of the sequences'py lengths
        mean_sum = 0 # summation of the means for all files
        num_files = 0 # num files 

        print("This may take a while...")
        for file in pos_dir:
                pos_from_file = file_mgmt.read_file(os.path.join(constants.POS_CLEAN_DIR, file))
                # grab mean for each file
                mean_of_file = len(pos_from_file[0])      
                
                mean_sum += mean_of_file # add that mean to a running sum
        
                # add the means to a list to save for later eval
                mean_lst.append(mean_of_file) 
                # used to get the mean of means (i.e. the mean of means = means / num_files)
                num_files += 1 

                pos_data.extend(pos_from_file) # extend values from file to pos_data list   

        for file in negs_dir:
                negs_data.extend(file_mgmt.read_file(os.path.join(constants.NEG_CLEAN_DIR, file)))
        
        # get mean of means of all the files
        mean_of_means = int(mean_sum / num_files)

        trim_val = prompts.user_prompt(mean_of_means, mean_lst)
        print(f"Trimming the sequences by the value: {trim_val}")
        
        # trim positives
        pos_data = mod_seqs.trim_composite(pos_data, trim_val)

        # label positives
        pos_data = mod_seqs.add_labels(pos_data, positive=True)

        # trim negatives
        negs_data = mod_seqs.trim_composite(negs_data, trim_val)

        # label negatives
        negs_data = mod_seqs.add_labels(negs_data, positive=False)

        # chop whichever list is longer
        pos_data, negs_data = mod_seqs.equalize_lengths(pos_data, negs_data)
        print(f"Length of positive and negative data{len(pos_data), len(negs_data)}")
        
        # get validation data to ensure it doesn't leak with the rest of the data
        validation_pos = pos_data[int(.95 * len(pos_data)) : ]
        validation_neg = negs_data[int(.95 * len(negs_data)) : ]
        print(f"percent of positive data the validation pos is: {len(validation_pos) / len(pos_data)}")
        print(f"percent of negative data the validation neg is: {len(validation_pos) / len(pos_data)}")
        validation_pos.extend(validation_neg)

        print("Shuffling validation data")
        random.shuffle(validation_pos)

        to_write_valid = mod_seqs.str_join(validation_pos)
        
        # Removing validation data from the data to be tested and trained
        print(f"Removing validation data from test and train data")
        pos_data = pos_data[: int(.95 * len(pos_data))]
        negs_data = negs_data[: int(.95 * len(negs_data))]

        # combine the two files together to randomize for the CNN
        pos_data.extend(negs_data)
        
        # # convert list of lists to list of strs
        # to_write = mod_seqs.str_join(pos_data)

        print("Shuffling le data")
        # shuffle the data
        random.shuffle(pos_data)
  
        # bypassing:
        # write the shuffled, trimmed data
        # file_mgmt.write_file(constants.PREPPED_FILE, to_write)
        # print(f"Reading data from {constants.PREPPED_FILE}")
        # data = file_mgmt.read_file(constants.PREPPED_FILE)
        #print("Putting data in a list")
        # data = [line.split() for line in data]

        to_write = mod_seqs.str_join(pos_data)
        # Determine the amts by percentage to split the data set
        train_data_amt = int(len(to_write) * .80)
        # test_data_amt = int(len(to_write) * .25)
        # validation_amt = int(len(to_write) * .05)

        # split data set by the above amounts
        print("Splitting data into train and test")
        train_data = to_write[ : train_data_amt]
        test_data = to_write[train_data_amt : ]

        # validation_data = to_write[train_data_amt + test_data_amt + 1 : ]

        print("Writing the train, test, and validation files.")
        # writing files
        file_mgmt.write_file(constants.TRAIN, train_data)
        file_mgmt.write_file(constants.TEST, test_data)
        file_mgmt.write_file(constants.VALID, to_write_valid)

        print(f"Done. Train data in {constants.TRAIN}. Test data in {constants.TEST}. Validation data in {constants.VALID}")


prep_seqs()