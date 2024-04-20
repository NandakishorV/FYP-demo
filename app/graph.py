import networkx as nx

class GraphManager:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node_id, **features):
        self.graph.add_node(node_id, **features)

    def add_edge(self, node1, node2, **features):
        self.graph.add_edge(node1, node2, **features)

    def remove_node(self, node_id):
        self.graph.remove_node(node_id)

    def remove_edge(self, node1, node2):
        self.graph.remove_edge(node1, node2)

    def get_graph(self):
        return self.graph

    def get_nodes(self):
        return self.graph.nodes(data=True)

    def get_edges(self):
        return self.graph.edges(data=True)
