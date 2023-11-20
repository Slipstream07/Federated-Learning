from collections import OrderedDict  # Import OrderedDict for maintaining ordered dictionary of model parameters
import flwr as fl
import torch

from centralized import load_data, load_model, train, test

# Function to set parameters received from the server to the model
def set_parameters(model, parameters):
    params_dict = zip(model.state_dict().keys(), parameters) # Zip model's state dictionary keys with the received parameters
    state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict}) # Create an ordered dictionary from the zipped pairs and convert parameters to Torch tensors
    model.load_state_dict(state_dict, strict=True) # Load the state dictionary into the model's state, ensuring strict matching of keys and sizes

# Load the pre-trained model and the data loaders for training and testing
net = load_model()
trainloader, testloader = load_data()

# Define a custom Flower client extending fl.client.NumPyClient
class FlowerClient(fl.client.NumPyClient):
    # Function to get parameters from the client
    def get_parameters(self, config):
        return [val.cpu().numpy() for _, val in net.state_dict().items()] # Convert model's parameters to NumPy arrays and return as a list
    
    # Function to perform a single round of training with received parameters
    def fit(self, parameters, config):
        set_parameters(net, parameters) # Set received parameters to the model
        train(net, trainloader, epochs=1) # Perform training for one epoch using the loaded training data
        return self.get_parameters({}), len(trainloader.dataset), {} # Return updated parameters, number of samples trained, and an empty dictionary

    # Function to evaluate the model with received parameters
    def evaluate(self, parameters, config):
        set_parameters(net, parameters) # Set received parameters to the model
        loss, accuracy = test(net, testloader) # Evaluate the model on the test data and obtain loss and accuracy
        return float(loss), len(testloader.dataset), {"accuracy": accuracy} # Return loss, number of samples tested, and a dictionary containing accuracy
    
# Start the Flower client with the specified server address and custom FlowerClient
fl.client.start_numpy_client(
    server_address="127.0.0.1:8080",  # Server address where Flower server is hosted
    client=FlowerClient(),  # Initialize the custom FlowerClient
)
