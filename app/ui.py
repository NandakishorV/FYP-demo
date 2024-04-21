from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QGridLayout, QInputDialog, QFileDialog,  QTableWidget, QTableWidgetItem, QDialog, QHBoxLayout
from PyQt5.QtCore import Qt
from graph import GraphManager
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv
import nodeScorer

class GraphUI(QWidget):
    def __init__(self):
        super().__init__()

        self.graph_manager = GraphManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('FYP DEMO')

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

        # Show Custom Graph Button
        show_mm_graph_button = QPushButton('Show Media-microservices Graph')
        show_mm_graph_button.clicked.connect(self.show_mm_graph)
        layout.addWidget(show_mm_graph_button)

        show_rs_graph_button = QPushButton('Show Robot shop Graph')
        show_rs_graph_button.clicked.connect(self.show_rs_graph)
        layout.addWidget(show_rs_graph_button)

        show_tt_graph_button = QPushButton('Show Train ticket Graph')
        show_tt_graph_button.clicked.connect(self.show_tt_graph)
        layout.addWidget(show_tt_graph_button)

        # Save Features Button
        save_features_button = QPushButton('Save Features to CSV')
        save_features_button.clicked.connect(self.save_features_to_csv)
        layout.addWidget(save_features_button)

        open_csv_button = QPushButton('Open CSV')
        open_csv_button.clicked.connect(self.open_csv)
        layout.addWidget(open_csv_button)

        score_nodes_button = QPushButton('Score nodes')
        score_nodes_button.clicked.connect(self.show_score_buttons)
        layout.addWidget(score_nodes_button)

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

    def show_mm_graph(self):
        image_path = "pre-built/mm/Graph.png"

        # Load the PNG image using matplotlib
        img = mpimg.imread(image_path)

        # Display the image using matplotlib
        plt.imshow(img)
        plt.title('MEDIA-MICROSERFVICE')
        plt.axis('off')  # Hide the axis if you want
        plt.show()

    def show_rs_graph(self):
        image_path = "pre-built/rs/Graph.png"

        # Load the PNG image using matplotlib
        img = mpimg.imread(image_path)

        # Display the image using matplotlib
        plt.imshow(img)
        plt.title('ROBOT SHOP')
        plt.axis('off')  # Hide the axis if you want
        plt.show()

    def show_tt_graph(self):
        image_path = "pre-built/tt/Graph.png"

        # Load the PNG image using matplotlib
        img = mpimg.imread(image_path)

        # Display the image using matplotlib
        plt.imshow(img)
        plt.title('TRAIN TICKET')
        plt.axis('off')  # Hide the axis if you want
        plt.show()

    def save_features_to_csv(self):
        # Get the graph
        graph = self.graph_manager.get_graph()

        # Save node features to node.csv
        with open('csv/Nodes.csv', 'w', newline='') as node_csv:
            node_writer = csv.writer(node_csv)

            # Convert NodeDataView to list and get the first node and its features
            nodes_data = list(graph.nodes(data=True))
            if nodes_data:
                first_node_id, first_node_features = nodes_data[0]
                column_headers = ['Service'] + list(first_node_features.keys())
                node_writer.writerow(column_headers)

                # Write nodes data
                for node_id, features in nodes_data:
                    row = [node_id] + [features.get(header, '') for header in column_headers[1:]]
                    node_writer.writerow(row)

        # Save edge features to edges.csv
        with open('csv/Edges.csv', 'w', newline='') as edge_csv:
            edge_writer = csv.writer(edge_csv)

            # Convert EdgeDataView to list and get the first edge and its features
            edges_data = list(graph.edges(data=True))
            print(edges_data)
            if edges_data:
                source, destination, first_edge_features = edges_data[0]
                column_headers = ['Source', 'Destination'] + list(first_edge_features.keys())
                edge_writer.writerow(column_headers)

                # Write edges data
                for source, destination, features in edges_data:
                    row = [source, destination] + [features.get(header, '') for header in column_headers[2:]]
                    edge_writer.writerow(row)

        print("Node features saved to node.csv")
        print("Edge features saved to edges.csv")

    def open_csv(self):
        # Prompt the user to select a CSV file to open
        csv_file_path, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)')

        # Check if a file path was provided
        if not csv_file_path:
            print("No file path provided")
            return

        print(f"CSV file selected: {csv_file_path}")

        # Create a QTableWidget to display the CSV data
        table_widget = QTableWidget()

        try:
            # Open the CSV file and read its contents
            with open(csv_file_path, newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                
                # Read the header row to determine the number of columns
                header = next(csv_reader)
                if header is None:
                    print("Header is empty or not found")
                    return
                
                num_columns = len(header)
                print(f"Header: {header}")
                print(f"Number of columns: {num_columns}")
                
                # Set up the table widget with the correct number of rows and columns
                table_widget.setColumnCount(num_columns)
                table_widget.setHorizontalHeaderLabels(header)
                
                # Read the data rows and populate the table widget
                for row_index, row_data in enumerate(csv_reader):
                    print(f"Row {row_index}: {row_data}")
                    table_widget.insertRow(row_index)
                    for col_index, col_value in enumerate(row_data):
                        item = QTableWidgetItem(col_value)
                        table_widget.setItem(row_index, col_index, item)

            # Adjust the size of the table widget's columns to fit the content
            table_widget.resizeColumnsToContents()
            # Show the pop-up window

            csv_window = QWidget()
            csv_window.setWindowTitle('CSV Data')

            # Create a layout for the window and add the QTableWidget
            layout = QVBoxLayout()
            layout.addWidget(table_widget)
            csv_window.setLayout(layout)

            # Show the new window
            csv_window.show()

        except Exception as e:
            print(f"An error occurred: {e}")

    def show_score_buttons(self):
        # Create a new dialog for the score buttons
        dialog = QDialog(self)
        dialog.setWindowTitle('Select graph')

        # Create a layout for the dialog
        dialog_layout = QHBoxLayout()

        # Create buttons b1, b2, b3, and b4
        b1_button = QPushButton('Media-microservices')
        b1_button.clicked.connect(lambda : nodeScorer.score_nodes("pre-built/mm/Nodes.csv","pre-built/mm/Edges.csv"))
        dialog_layout.addWidget(b1_button)

        b2_button = QPushButton('Robot shop')
        b2_button.clicked.connect(lambda : nodeScorer.score_nodes("pre-built/rs/Nodes.csv","pre-built/rs/Edges.csv"))
        dialog_layout.addWidget(b2_button)

        b3_button = QPushButton('Train ticket')
        b3_button.clicked.connect(lambda : nodeScorer.score_nodes("pre-built/tt/Nodes.csv","pre-built/tt/Edges.csv"))
        dialog_layout.addWidget(b3_button)

        b4_button = QPushButton('Custom graph')
        b4_button.clicked.connect(lambda : nodeScorer.score_nodes("pre-built/csv/Nodes.csv","pre-built/rs/Edges.csv"))
        dialog_layout.addWidget(b4_button)

        # Set the dialog layout
        dialog.setLayout(dialog_layout)

        # Show the dialog
        dialog.exec_()

    def on_score_button_clicked(self, button_label):
        # Print which button was clicked
        print(f'Button {button_label} clicked!')