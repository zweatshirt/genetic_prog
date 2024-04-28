import os

# Author: Zachery Linscott

# This serves as a global namespace file for any constants.

# current directory
PATH = os.getcwd()
# parent directory
PARENT = os.path.dirname(PATH)

# cleaning pipeline files
NEG_BEDS_DIR = f"{PATH}/negs_beds"
NEG_CLEAN_DIR = f"{PATH}/negs_clean"
POS_CLEAN_DIR = f"{PATH}/pos_clean"
MEAN = "mean.txt"

# train, test, validation files
DATA = f"{PATH}/data"
TEST = f"{DATA}/test.txt"
TRAIN = f"{DATA}/train.txt"
VALID = f"{DATA}/validation.txt"
ONE_HOT_TRAIN = f'{DATA}/hot_train.npy'
ONE_HOT_TEST = f'{DATA}/hot_test.npy'
ONE_HOT_VALID = f'{DATA}/hot_validate.npy'

# Model names (ZachNet is a modified NiN)
ZACHNET = 'zachnet'
ALEXNET = 'alexnet'
