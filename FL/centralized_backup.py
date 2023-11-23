import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.transforms import Compose, ToTensor, Normalize
from torch.utils.data import DataLoader
from torchvision.datasets import CIFAR10

# Runs on the GPU if available otherwise it runs it on the CPU
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Model architecture 
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # Convolutional layers
        self.conv1 = nn.Conv2d(3, 6, 5) # 3 input channels, 6 output channels, 5x5 kernel size
        self.pool = nn.MaxPool2d(2, 2) # Max pooling with a 2x2 kernel and stride of 2
        self.conv2 = nn.Conv2d(6, 16, 5) # 6 input channels, 16 output channels, 5x5 kernel size
        # Fully connected layers
        self.fc1 = nn.Linear(16 * 5 * 5, 120) # 16 * 5 * 5 input features, 120 output features
        self.fc2 = nn.Linear(120, 84) # 120 input features, 84 output features
        self.fc3 = nn.Linear(84, 10) # 84 input features, 10 output features (for classification)
    
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x))) # Apply convolution, activation, and pooling
        x = self.pool(F.relu(self.conv2(x))) # Apply convolution, activation, and pooling
        x = x.view(-1, 16 * 5 * 5) # Reshape the tensor for the fully connected layers
        x = F.relu(self.fc1(x)) # Apply activation function to the first fully connected layer
        x = F.relu(self.fc2(x)) # Apply activation function to the first fully connected layer
        return self.fc3(x) # Return the output (logits) from the third fully connected layer

# Training function; trains the model for a given number of epochs with a given trainset
def train(net, trainloader, epochs):
    criterion = torch.nn.CrossEntropyLoss() # Define the loss function (criterion) for classification problems
    # Define the optimization algorithm (SGD with momentum) for updating network weights
    optimizer = torch.optim.SGD(net.parameters(), lr=0.001, momentum=0.9) 
    for _ in range(epochs):
        for images, labels in trainloader: # Zero the gradients to prevent accumulation from previous iterations
            optimizer.zero_grad() # Forward pass: Compute predictions (logits) using the neural network
            criterion(net(images.to(DEVICE)), labels.to(DEVICE)).backward() # Computes the forward pass and backward pass through the neural network.
            optimizer.step() 

# Evaluates the function and computes the loss and accuracy on a given testset
def test(net, testloader):
    criterion = torch.nn.CrossEntropyLoss() # Define the Cross Entropy Loss
    correct, total, loss = 0, 0, 0.0 # Initialize variables for calculating accuracy and loss
    with torch.no_grad(): # Disable gradient computation during testing
        for images, labels in testloader:
            outputs = net(images.to(DEVICE)) # Forward pass: Compute predictions using the neural network
            loss += criterion(outputs, labels.to(DEVICE)).item() # Calculate the loss between predicted outputs and actual labels
            total += labels.size(0) # Update total number of samples
            correct += (torch.max(outputs.data, 1)[1] == labels).sum().item() # Calculate the number of correctly predicted samples
    return loss / len(testloader.dataset), correct / total # Compute average loss and accuracy

# Utility functions
# Return the dataloaders(trainset and testset)
def load_data():
    trf = Compose([ToTensor(), Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    trainset = CIFAR10("./data", train=True, download=True, transform=trf)
    testset = CIFAR10("./data", train=False, download=True, transform=trf)
    return DataLoader(trainset, batch_size=32, shuffle=True), DataLoader(testset)

# Return the model
def load_model():
    return Net().to(DEVICE)

if __name__ == "__main__":
    net = load_model()
    trainloader, testloader = load_data()
    train(net, trainloader, 5)
    loss, accuracy = test(net, testloader)
    print(f"Loss: {loss:.5f}, Accuracy: {accuracy:.3f}")


    
