import torch
import torchvision.transforms as transforms
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F

# This doesn't work in its current state.

class MiniCNN(torch.nn.Module):
  def __init__(self):
    super(MiniCNN, self).__init__()
    self.conv1 = torch.nn.Conv1d(4, 1, kernel_size=1) 
    self.pool = torch.nn.MaxPool1d(kernel_size=2, stride=2)  
    self.conv2 = torch.nn.Conv1d(1, 1, kernel_size=1)  
    self.fc1 = torch.nn.Linear(2 * 678, 512)  
    self.fc2 = torch.nn.Linear(512, 2) 

  def forward(self, x):
    x = self.pool(torch.nn.functional.relu(self.conv1(x)))  
    # x = self.pool(torch.nn.functional.relu(self.conv2(x))) 
    # x = x.view(-1,16 * 5 * 5)  
    x = torch.nn.functional.relu(self.fc1(x))  
    x = self.fc2(x)  
    return x