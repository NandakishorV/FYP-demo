import torch
import pandas as pd
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data
import torch.optim as optim
from torch_geometric.nn import GCNConv
from torch.utils.data import DataLoader
import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt

# Set random seed for reproducibility
seed = 42
torch.manual_seed(seed)
np.random.seed(seed)
random.seed(seed)

class NodeScorer(nn.Module):
    def __init__(self, node_input_dim, hidden_dim, output_dim):
        super(NodeScorer, self).__init__()
        self.conv1 = GCNConv(node_input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, output_dim)
        self.fc = nn.Linear(output_dim, 1)

        # Initialize weights and biases
        self.reset_parameters()

    def reset_parameters(self):
        # Manually set weight tensor to desired values
        weight_value = torch.ones_like(self.fc.weight)
        self.fc.weight.data.copy_(weight_value)

        # Manually set bias tensor to desired values
        bias_value = torch.zeros_like(self.fc.bias)
        self.fc.bias.data.copy_(bias_value)

    def forward(self, data):
        x, edge_index, _ = data.x, data.edge_index, data.edge_attr

        # Perform message passing with GCN layers using node features only
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        x = F.relu(x)  # Apply ReLU activation

        # Compute scores for each node
        scores = self.fc(x).squeeze(dim=-1)

        return scores, x  # Return both scores and node embeddings
    
def initializing(nodes_df,edges_df):
  # Mapping node names to indices
  node_name_to_index = {name: index for index, name in enumerate(nodes_df['Node'])}

  # Convert node features to PyTorch tensor
  node_features = torch.tensor(nodes_df.drop(columns=['Node']).values, dtype=torch.float)
  edge_indices = torch.tensor(
      [
          [node_name_to_index[child], node_name_to_index[parent]]
          for parent, child in zip(edges_df['Source'], edges_df['Target'])
      ],
      dtype=torch.long
  )

  # Create PyG Data object
  graph_data = Data(x = node_features, edge_index=edge_indices.t().contiguous())
  return graph_data

def saveAsCSV(nodes_df,scores,filename):
  scores = scores.detach().cpu().numpy().tolist()
  df = pd.DataFrame({'Node': nodes_df['Node'], 'Score': scores})
  df.to_excel(filename, index=False)

def score_nodes(node_file, edge_file):
    nodes_df = pd.read_csv(node_file)
    edges_df = pd.read_csv(edge_file)
    graph_data = initializing(nodes_df,edges_df)
    model = NodeScorer(node_input_dim=graph_data.num_node_features, hidden_dim=16, output_dim=8)
    scores, x = model(graph_data)

    saveAsCSV(nodes_df,scores,'score.csv')