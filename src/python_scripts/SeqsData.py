# Author: Zachery Linscott

# This class serves as a container for the labels and data 
# that is meant to be passed into the DataLoader object
# This is a necessary step in the process of preparing the data for the CNN

from torch.utils.data import Dataset
import torch

class SeqsData(Dataset):
    def __init__(self, seqs):
        tensor_seqs = [torch.tensor(seq[1]).float() for seq in seqs]
        tensor_labels = [torch.tensor(seqs[0]).long() for seqs in seqs]
        self.data = torch.stack(tensor_seqs)
        self.labels= torch.stack(tensor_labels)
        

    def __len__(self):
        return len(self.data)
    
    
    def __getitem__(self, id):
        data_set=self.data[id]
        labels=self.labels[id]

        return data_set, labels
