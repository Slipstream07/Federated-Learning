import flwr as fl

# Function to calculate weighted average of accuracy based on metrics
def weighted_average(metrics):
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics] # Extract accuracies multiplied by the number of examples from the received metrics
    examples = [num_examples for num_examples, _ in metrics] # Extract number of examples from the metrics
    return {"accuracy": sum(accuracies) / sum(examples)} # Compute the weighted average accuracy based on the weighted sum of accuracies and total examples

# Start the Flower server with specified configuration and strategy
fl.server.start_server(
    server_address="0.0.0.0:8080",  # Server address where Flower server will be hosted
    config=fl.server.ServerConfig(num_rounds=3),  # Configuration for the server (e.g., number of rounds)
    strategy=fl.server.strategy.FedAvg(  # Federated Averaging strategy for model aggregation
        evaluate_metrics_aggregation_fn=weighted_average,  # Custom aggregation function for evaluating metrics
    ),
)
