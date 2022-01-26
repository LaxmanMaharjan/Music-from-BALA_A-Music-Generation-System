import torch
import torch.nn.functional as F

from torch import nn,optim

# Hyperparameters
vocab_size = 100
input_size = vocab_size
num_feats = vocab_size
hidden_size = 256
num_layers = 2

sequence_length = 1
learning_rate = 0.01
batch_size = 2
epochs = 2

device = 'cuda' if torch.cuda.is_available() == True else 'cpu'

class Generator(nn.Module):

    def __init__(self):
        super(Generator, self).__init__()
    
    
        self.hidden_size = hidden_size
        self.num_layers = num_layers
    
        self.fc1 = nn.Linear(in_features=(num_feats*2), out_features=hidden_size)
        self.lstm = nn.LSTM(input_size=hidden_size, hidden_size=hidden_size ,num_layers=2, batch_first=True)
        self.fc2 = nn.Linear(in_features=hidden_size, out_features=num_feats)
        self.dropout = nn.Dropout(p=0.6)
        self.tanh = nn.Tanh()
        #create optimizer, using stochastic gradient descent
        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.01)
    
        #counter and accumulator for progress
        self.counter = 0
        self.progress = []
        self.batch_size = batch_size
    
    def forward(self, x):
        # Set initial hidden and cell states
        h0 = torch.zeros(self.num_layers, self.batch_size, self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers, self.batch_size, self.hidden_size).to(device)
        #print(f'after h0:{h0.shape}')
        # x: (batch_size, seq_len, num_feats)
        
        #batch_size, seq_len, num_feats = x.shape
    
        # split to seq_len * (batch_size * num_feats)
        x = torch.split(x, 1, dim=1)
        x = [x_step.squeeze(dim=1) for x_step in x]
        # create dummy-previous-output for first timestep
        prev_gen = torch.empty([batch_size, num_feats]).uniform_().to(device)
        # manually process each timestep
        gen_feats = []
        for x_step in x:
            # concatenate current input features and previous timestep output features
            concat_in = torch.cat((x_step, prev_gen), dim=-1)
            out1 = F.relu(self.fc1(concat_in))
            out1 = out1.unsqueeze(1)
    
            out2, hidden = self.lstm( out1, (h0,c0))
            out2 = self.dropout(out2) # feature dropout only (no recurrent dropout)
            out3 = self.fc2(out2)
            # prev_gen = F.relu(self.fc_layer2(h2)) #DEBUG
            gen_feats.append(out3)
            #print('after last')
            
        # seq_len * (batch_size * num_feats) -> (batch_size * seq_len * num_feats)
        gen_feats = torch.stack(gen_feats, dim=1).squeeze(1)
        #gen_feats = torch.stack(gen_feats, dim=1)
        final_output = self.tanh(gen_feats)
        return gen_feats
    
    def init_hidden(self, batch_size):
        # Set initial hidden and cell states
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)
    
        return (h0,c0)
    
    def train(self, D, inputs, targets):
        #print('before training G')
        # calculate the output of the network
        g_output = self.forward(inputs)
        # pass onto Discriminator
        d_output = D.forward(g_output)
    
        # calculate error
        loss = D.discriminator_loss(d_output, targets)
        # increase counter and accumulate error every 10
        self.counter += 1
        if (self.counter % 5 == 0):
          self.progress.append(loss.item())
    
        # zero gradients, perform a backward pass, update weights
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
    
    
