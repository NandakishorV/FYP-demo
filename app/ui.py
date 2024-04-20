from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QGridLayout, QInputDialog
from graph import GraphManager
import networkx as nx
import matplotlib.pyplot as plt

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

        # Set the layout
        self.setLayout(layout)

    def add_node(self):
        node_id = self.node_id_input.text().strip()
        if node_id:
            # Prompt for node features
            features = {}
            while True:
                feature_name, ok = QInputDialog.getText(self, 'Add Feature', 'Enter feature name (or leave blank to stop):')
                if not ok or not feature_name:
                    break
                feature_value, ok = QInputDialog.getText(self, 'Add Feature', f'Enter value for {feature_name}:')
                if ok:
                    features[feature_name] = feature_value
            self.graph_manager.add_node(node_id, **features)

    def add_edge(self):
        node1 = self.node1_input.text().strip()
        node2 = self.node2_input.text().strip()
        if node1 and node2:
            # Prompt for edge features
            features = {}
            while True:
                feature_name, ok = QInputDialog.getText(self, 'Add Feature', 'Enter feature name (or leave blank to stop):')
                if not ok or not feature_name:
                    break
                feature_value, ok = QInputDialog.getText(self, 'Add Feature', f'Enter value for {feature_name}:')
                if ok:
                    features[feature_name] = feature_value
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

        # Retrieve edge attributes (specify the attribute you want to display)
        # For example, if you want to display the 'weight' attribute, use:
        # edge_labels = nx.get_edge_attributes(graph, 'weight')
        # To display all edge attributes, pass None or leave it empty:
        edge_labels = nx.get_edge_attributes(graph, None)

        # Draw edge labels
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

        # Show the plot
        plt.title('Graph')
        plt.show()
