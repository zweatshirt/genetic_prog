import torch
import torchvision.transforms as transforms
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F

# Author: Caleb Bayles
# This a network based mostly/almost entirely off of AlexNet. 

class AlexNet(torch.nn.Module):
    def __init__(self):
        # result size = ((size - kernelSize + 2 * padding) / stride) + 1
        super().__init__()

        self.conv1 = torch.nn.Conv1d(in_channels=4, out_channels=64, kernel_size=11) # ((726 - 11 + 2 * 0) / 1) + 1 = 716

        self.pool2 = torch.nn.MaxPool1d(kernel_size=3, stride=2) # ((716 - 3 + 2 * 0) / 2) + 1 = 358

        self.conv3 = torch.nn.Conv1d(in_channels=64, out_channels=192, kernel_size=5, padding=2) # ((358 - 5 + 2 * 2) / 1) + 1 = 358

        self.pool4 = torch.nn.MaxPool1d(kernel_size=3, stride=2) # ((358 - 3 + 2 * 0) / 2) + 1 = 179

        self.conv5 = torch.nn.Conv1d(in_channels=192, out_channels=384, kernel_size=3, padding=1) # ((179 - 3 + 2 * 1) / 1) + 1 = 179

        self.conv6 = torch.nn.Conv1d(in_channels=384, out_channels=256, kernel_size=3, padding=1) # ((179 - 3 + 2 * 1) / 1) + 1 = 179

        self.conv7 = torch.nn.Conv1d(in_channels=256, out_channels=256, kernel_size=3, padding=1) # ((179 - 3 + 2 * 1) / 1) + 1 = 179

        self.pool8 = torch.nn.MaxPool1d(kernel_size=3, stride=2) # ((179 - 3 + 2 * 0) / 2) + 1 = 89

        self.pool9 = torch.nn.AdaptiveAvgPool1d(6) # like max pooling, but output size is specified instead of kernel size and stride

        self.fc1 = torch.nn.Linear(in_features=(6 * 256), out_features=1024)

        self.fc2 = torch.nn.Linear(in_features=1024, out_features=1024)

        self.fc3 = torch.nn.Linear(in_features=1024, out_features=2)

    def forward(self, x):
        x = F.relu(self.conv1(x))

        x = self.pool2(x)

        x = F.relu(self.conv3(x))

        x = self.pool4(x)

        x = F.relu(self.conv5(x))

        x = F.relu(self.conv6(x))

        x = F.relu(self.conv7(x))

        x = self.pool8(x)

        x = self.pool9(x)

        x = torch.flatten(x, 1)

        x = F.dropout(x, 0.5)

        x = F.relu(self.fc1(x))

        x = F.dropout(x, 0.5)

        x = F.relu(self.fc2(x))
        
        x = self.fc3(x)
        return x