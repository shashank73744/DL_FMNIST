import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim
import pandas as pd
from torch.utils.data import DataLoader, Dataset
torch.set_printoptions(linewidth=120)
torch.set_grad_enabled(True)
class Network(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=6, kernel_size =5)
        self.conv2 = nn.Conv2d(in_channels=6, out_channels=12, kernel_size =5)
        
        self.fc1 = nn.Linear(in_features = 12*4*4, out_features=120)
        self.fc2 = nn.Linear(in_features=120, out_features=60)
        self.out = nn.Linear(in_features=60, out_features=10)
        
    def forward(self,t):
        # (1) input layer
        t = t
        
        # (2) hidden conv Layer
        t = self.conv1(t)
        t = F.relu(t)
        t = F.max_pool2d(t,kernel_size=2, stride =2)
        
        # (3) hidden conv Layer
        t = self.conv2(t)
        t = F.relu(t)
        t = F.max_pool2d(t, kernel_size=2, stride = 2)
        
        # (4) hidden Linear Layer
        t = t.reshape(-1,12*4*4)
        t = self.fc1(t)
        t = F.relu(t)
        
        # (5) hidden Linear Layer
        t = self.fc2(t)
        t = F.relu(t)
        
        #(5) output_layer
        t = self.out(t)
        
        return t
network = Network()
def get_num_correct(preds,labels):
    return preds.argmax(dim = 1).eq(labels).sum()

train_set = torchvision.datasets.FashionMNIST(
    root ='./data/FashionMNIST'
    ,train=True
    ,download=True
    ,transform=transforms.Compose([
            transforms.ToTensor()
        ])
)

test_set = torchvision.datasets.FashionMNIST(
    root ='./data/FashionMNIST'
    ,train=False
    ,download=True
    ,transform=transforms.Compose([
            transforms.ToTensor()
        ])
)

print(len(train_set))
print(len(test_set))

network = Network()
train_loader = torch.utils.data.DataLoader(train_set,batch_size=100)
optimizer = optim.Adam(network.parameters(),lr=0.01)

epochs = 4

for epoch in range(epochs):
    total_loss = 0
    total_correct = 0
    for batch in train_loader:
        images,labels = batch

        preds = network(images)# Pass Batch
        loss = F.cross_entropy(preds,labels)# Calculate Loss

        optimizer.zero_grad()
        loss.backward()# Calculate Gradients
        optimizer.step()# Update Weights
        
        total_loss += loss.item()
        total_correct += get_num_correct(preds,labels)
    print("epoch:", epoch, "total_correct", total_correct, "loss", total_loss)

print('Percentage_of_correct_prediction{}'.format(total_correct/len(train_set)))
