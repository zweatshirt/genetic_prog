import torch
import torchvision.transforms as transforms
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F

# Author: Zachery Linscott
# This is a modified NiN network. Implements ReLU as the activation function for most layers. 
# For layer 11, a fully connected linear layer, Sigmoid is used for the activation.

class ZachNet(nn.Module):
    
    def __init__(self):
        
        super().__init__()

        # equation for output size: floor((Input size - filter size + 2*padding)/Stride + 1)
        
        # Layer1
        self.conv1 = nn.Conv1d(in_channels=4, out_channels=96, kernel_size=11, stride=1, padding=1)
        # no pooling in layer 1
        # self.pool1 = nn.MaxPool2d(kernel_size=3,stride=2)

        # Layer2:
        self.conv2 = nn.Conv1d(in_channels=96, out_channels=96, kernel_size=7, padding=1, stride=2) 
        self.local_response2=nn.LocalResponseNorm(size=5,alpha=0.0001,beta=0.75,k=2)

        # Layer3:
        self.conv3 = nn.Conv1d(in_channels=96, out_channels=96, kernel_size=3, stride=1, padding=1)
        self.pool_layer3 = nn.MaxPool1d(kernel_size=7, stride=2)
        self.local_response = nn.LocalResponseNorm(size=5, alpha=0.0001, beta=0.75, k=2)

        # Layer4:
        self.conv4 = nn.Conv1d(in_channels=96, out_channels=96, kernel_size=7, stride=4, padding=2)

        # Layer5:
        self.conv5=nn.Conv1d(in_channels=96, out_channels=96, kernel_size=1, stride=1)

        # Layer6:
        self.conv6=nn.Conv1d(in_channels=96, out_channels=96, kernel_size=1, stride=2)
        self.pool_layer6=nn.MaxPool1d(kernel_size=1, stride=1) # output = 15
        # self.dropout_layer6 = nn.Dropout(p=.5) 
        
        # Layer7:
        self.conv7=nn.Conv1d(in_channels=96, out_channels=96, kernel_size=3, stride=1, padding=1) # output = 15

        # Layer8:
        self.conv8=nn.Conv1d(in_channels=96, out_channels=96, kernel_size=1, stride=1) # output = 15

        # Layer9:
        self.conv9 = nn.Conv1d(in_channels=96, out_channels=96, kernel_size=2, stride=2) # output = 7
        # self.dropout_layer9 = nn.Dropout(p=.5) 
        
        # Layer10:
        self.fc1 = nn.Linear(in_features=(960), out_features=1024)
        
        # Layer11:
        self.fc2 = nn.Linear(in_features=1024, out_features=1024)
                
        # Layer12: (actually this is not a layer but anyways)
        self.fc3 = nn.Linear(in_features=1024, out_features=2)
        
        # self.adapt_avg_pool=nn.AdaptiveAvgPool1d((1, 1))
        
        
    def forward(self, x):
        
        # apply ReLU to layer 1
        x = F.relu(self.conv1(x))

        # apply ReLU to layer 2
        x = F.relu(self.conv2(x))

        # dropout of .5 applied to pooled and ReLU'd convolution 3 (layer 3)
        x = self.pool_layer3(F.relu(self.local_response(self.conv3(x))))
        x = F.dropout(x, .5)

        # apply ReLU to layer 4
        x = F.relu(self.conv4(x))

        # apply ReLU to layer 5
        x = F.relu(self.conv5(x))

        # dropout of .5 applied to pooled and ReLU'd convolution 6 (layer 6)
        # x = self.pool_layer6(F.relu(self.conv6(x)))
        x = F.relu(self.conv6(x))
        x = F.dropout(x, .5)

        # apply ReLU to layer 7
        x = F.relu(self.conv7(x))

        # apply ReLU to layer 8
        x = F.relu(self.conv8(x))

        # dropout of .5 and ReLU applied to layer 9
        x = F.relu(self.conv9(x))
        x = F.dropout(x, .5)

        x = torch.flatten(x, 1) # flatten all dimensions except batch
        
        # apply ReLU to layer 10, dropout of .5
        x = F.relu(self.fc1(x))
        x = F.dropout(x, .5)

        # apply sigmoid to layer 11, dropout of .5
        x = torch.sigmoid(self.fc2(x))
        # x = F.dropout(x, .5)

        x = self.fc3(x)
          
        return x