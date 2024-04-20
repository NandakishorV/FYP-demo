from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QGridLayout, QInputDialog, QFileDialog
from graph import GraphManager
import networkx as nx
import matplotlib.pyplot as plt
import csv

class GraphUI(QWidget):
    def __init__(self):
        super().__init__()

        self.graph_manager = GraphManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Graph Application')

        # Main layout
        layout = QVBoxLayout()

        # Grid layout for adding and removing nodes/edges
        grid_layout = QGridLayout()
        
        # Add Node
        self.node_id_input = QLineEdit()
        add_node_button = QPushButton('Add Node')
        add_node_button.clicked.connect(self.add_node)
        grid_layout.addWidget(QLabel('Node ID:'), 0, 0)
        grid_layout.addWidget(self.node_id_input, 0, 1)
        grid_layout.addWidget(add_node_button, 0, 2)

        # Add Edge
        self.node1_input = QLineEdit()
        self.node2_input = QLineEdit()
        add_edge_button = QPushButton('Add Edge')
        add_edge_button.clicked.connect(self.add_edge)
        grid_layout.addWidget(QLabel('Node 1:'), 1, 0)
        grid_layout.addWidget(self.node1_input, 1, 1)
        grid_layout.addWidget(QLabel('Node 2:'), 1, 2)
        grid_layout.addWidget(self.node2_input, 1, 3)
        grid_layout.addWidget(add_edge_button, 1, 4)

        # Remove Node
        remove_node_button = QPushButton('Remove Node')
        remove_node_button.clicked.connect(self.remove_node)
        grid_layout.addWidget(remove_node_button, 0, 3)

        # Remove Edge
        remove_edge_button = QPushButton('Remove Edge')
        remove_edge_button.clicked.connect(self.remove_edge)
        grid_layout.addWidget(remove_edge_button, 1, 5)

        layout.addLayout(grid_layout)

        # Show Graph Button
        show_graph_button = QPushButton('Show Graph')
        show_graph_button.clicked.connect(self.show_graph)
        layout.addWidget(show_graph_button)

        # Save Features Button
        save_features_button = QPushButton('Save Features to CSV')
        save_features_button.clicked.connect(self.save_features_to_csv)
        layout.addWidget(save_features_button)

        # Set the layout
        self.setLayout(layout)

    def add_node(self):
        node_id = self.node_id_input.text().strip()
        if node_id:
            # Prompt for node features
            features = {}
            feature_name = 1
            while True:
                feature_value, ok = QInputDialog.getText(self, 'Add Feature', f'Enter value for f{feature_name}:')
                if not feature_value:
                    break
                if ok:
                    features["f"+str(feature_name)] = feature_value
                feature_name+=1
            self.graph_manager.add_node(node_id, **features)

    def add_edge(self):
        node1 = self.node1_input.text().strip()
        node2 = self.node2_input.text().strip()
        if node1 and node2:
            # Prompt for edge features
            features = {}
            feature_name = 1
            while True:
                feature_value, ok = QInputDialog.getText(self, 'Add Feature', f'Enter value for f{feature_name}:')
                if not feature_value:
                    break
                if ok:
                    features["f"+str(feature_name)] = feature_value
                feature_name+=1
            self.graph_manager.add_edge(node1, node2, **features)

    def remove_node(self):
        node_id = self.node_id_input.text().strip()
        if node_id:
            self.graph_manager.remove_node(node_id)

    def remove_edge(self):
        node1 = self.node1_input.text().strip()
        node2 = self.node2_input.text().strip()
        if node1 and node2:
            self.graph_manager.remove_edge(node1, node2)

    def show_graph(self):
        # Get the graph
        graph = self.graph_manager.get_graph()

        # Draw the graph using matplotlib and networkx
        pos = nx.spring_layout(graph)  # Position the nodes using spring layout

        # Draw nodes
        nx.draw_networkx_nodes(graph, pos, node_color='lightblue', node_size=500)

        # Draw edges
        nx.draw_networkx_edges(graph, pos)

        # Draw node labels
        nx.draw_networkx_labels(graph, pos, font_size=10)

        # Retrieve edge attributes and draw edge labels
        edge_labels = nx.get_edge_attributes(graph, None)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        nodes = self.graph_manager.get_nodes()
        edges = self.graph_manager.get_edges()
        print('Nodes:', nodes)
        print('Edges:', edges)
        # Show the plot
        plt.title('Graph')
        plt.show()

    def save_features_to_csv(self):
        # Get the graph
        graph = self.graph_manager.get_graph()

        # Save node features to node.csv
        with open('csv/nodes.csv', 'w', newline='') as node_csv:
            node_writer = csv.writer(node_csv)

            # Convert NodeDataView to list and get the first node and its features
            nodes_data = list(graph.nodes(data=True))
            if nodes_data:
                first_node_id, first_node_features = nodes_data[0]
                column_headers = ['nodeid'] + list(first_node_features.keys())
                node_writer.writerow(column_headers)

                # Write nodes data
                for node_id, features in nodes_data:
                    row = [node_id] + [features.get(header, '') for header in column_headers[1:]]
                    node_writer.writerow(row)

        # Save edge features to edges.csv
        with open('csv/edges.csv', 'w', newline='') as edge_csv:
            edge_writer = csv.writer(edge_csv)

            # Convert EdgeDataView to list and get the first edge and its features
            edges_data = list(graph.edges(data=True))
            print(edges_data)
            if edges_data:
                source, destination, first_edge_features = edges_data[0]
                column_headers = ['source', 'destination'] + list(first_edge_features.keys())
                edge_writer.writerow(column_headers)

                # Write edges data
                for source, destination, features in edges_data:
                    row = [source, destination] + [features.get(header, '') for header in column_headers[2:]]
                    edge_writer.writerow(row)

        print("Node features saved to node.csv")
        print("Edge features saved to edges.csv")
