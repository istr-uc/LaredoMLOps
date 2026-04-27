import torch

class RNNClassifier(torch.nn.Module):
    def __init__(self, input_size, hidden_sizes, seq_length, output_size, activation_fn=torch.nn.ReLU, **kwargs):
        super(RNNClassifier, self).__init__()
        layers = []
        # The input size is passed as features * seq_length, so we need to adjust accordingly
        in_size = input_size // seq_length
        self.seq_length = seq_length
        for hidden_size in hidden_sizes:
            layers.append(torch.nn.RNN(in_size, hidden_size, batch_first=True))
            layers.append(activation_fn())
            in_size = hidden_size
            
        self.rnn = torch.nn.Sequential(layers)
        self.classification_head = torch.nn.Sequential([torch.nn.Linear(output_size, output_size), torch.nn.Softmax(dim=1)])
        
    def forward(self, x):
        # Reshape 2D input (batch_size,features*seq_length) to (batch_size, seq_length, features)
        x = x.view(-1, self.seq_length, x.size(1) // self.seq_length)
        # Get the output from the RNN network
        x, _ = self.rnn(x)
        # Apply the classification head to last rnn output
        x = self.classification_head(x[:, -1, :])
        return x

class RNNRegressor(torch.nn.Module):
    def __init__(self, input_size, hidden_sizes, seq_length, output_size, activation_fn=torch.nn.ReLU, **kwargs):
        super(RNNRegressor, self).__init__()
        layers = []
        in_size = input_size
        self.seq_length = seq_length
        for hidden_size in hidden_sizes:
            layers.append(torch.nn.RNN(in_size, hidden_size, batch_first=True))
            layers.append(activation_fn())
            in_size = hidden_size
            
        layers.append(torch.nn.Linear(in_size, output_size))
        self.rnn = torch.nn.Sequential(layers)
        self.regression_head = torch.nn.Linear(output_size, 1)
        
    def forward(self, x):
        # Reshape 2D input (batch_size,features*seq_length) to (batch_size, seq_length, features)
        x = x.view(-1, self.seq_length, x.size(1) // self.seq_length)
        # Get the output from the RNN network
        x, _ = self.rnn(x)
        # Apply the regression head to last rnn output
        x = self.regression_head(x[:, -1, :])
        return x