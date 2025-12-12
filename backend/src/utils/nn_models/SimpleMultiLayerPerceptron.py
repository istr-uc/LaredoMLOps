import torch

class SimpleMultiLayerPerceptronClassifier(torch.nn.Module):
    def __init__(self, input_size, hidden_sizes, output_size, activation_fn=torch.nn.ReLU, **kwargs):
        super(SimpleMultiLayerPerceptronClassifier, self).__init__()
        layers = []
        in_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.append(torch.nn.Linear(in_size, hidden_size))
            layers.append(activation_fn())
            in_size = hidden_size

        # If it is binary classification, use a single output with sigmoid
        if output_size == 2:
            output_size = 1    
        layers.append(torch.nn.Linear(in_size, output_size))
        if output_size == 1:
            # Binary classification
            layers.append(torch.nn.Sigmoid())
        else:
            # Add a classification head with softmax activation
            layers.append(torch.nn.Softmax(dim=1))
        self.network = torch.nn.Sequential(*layers)
        
    def forward(self, x):
        return self.network(x.to(torch.float32))

class SimpleMultiLayerPerceptronRegressor(torch.nn.Module):
    def __init__(self, input_size, hidden_sizes, output_size=1, activation_fn=torch.nn.ReLU, **kwargs):
        super(SimpleMultiLayerPerceptronRegressor, self).__init__()
        layers = []
        in_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.append(torch.nn.Linear(in_size, hidden_size))
            layers.append(activation_fn())
            in_size = hidden_size
            
        # layers.append(torch.nn.Linear(in_size, output_size))
        layers.append(torch.nn.Linear(in_size, 1))
        self.network = torch.nn.Sequential(*layers)
        
    def forward(self, x):
        return self.network(x.to(torch.float32))