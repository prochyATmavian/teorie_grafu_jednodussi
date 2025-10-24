"""
Graph data structure module for graph recognition system.
Implements Node, Edge, and Graph classes with iterators.
"""

from collections import defaultdict


class Node:
    """Represents a node in the graph."""
    
    def __init__(self, identifier, weight=None):
        """
        Initialize a node.
        
        Args:
            identifier (str): Unique identifier for the node
            weight (float/int, optional): Weight of the node
        """
        self.identifier = identifier
        self.weight = weight
    
    def __str__(self):
        return f"Node({self.identifier})"
    
    def __repr__(self):
        return f"Node(identifier='{self.identifier}', weight={self.weight})"
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.identifier == other.identifier
        return False
    
    def __hash__(self):
        return hash(self.identifier)


class Edge:
    """Represents an edge in the graph."""
    
    def __init__(self, source, target, weight=None, label=None, edge_type='undirected'):
        """
        Initialize an edge.
        
        Args:
            source (Node): Source node
            target (Node): Target node
            weight (float/int, optional): Weight of the edge
            label (str, optional): Label of the edge
            edge_type (str): Type of edge ('directed', 'undirected')
        """
        self.source = source
        self.target = target
        self.weight = weight
        self.label = label
        self.edge_type = edge_type
    
    def __str__(self):
        direction = "->" if self.edge_type == 'directed' else "-"
        return f"Edge({self.source.identifier}{direction}{self.target.identifier})"
    
    def __repr__(self):
        return (f"Edge(source={self.source.identifier}, target={self.target.identifier}, "
                f"weight={self.weight}, label={self.label}, type={self.edge_type})")
    
    def __eq__(self, other):
        if isinstance(other, Edge):
            return (self.source == other.source and 
                    self.target == other.target and
                    self.edge_type == other.edge_type)
        return False
    
    def __hash__(self):
        return hash((self.source.identifier, self.target.identifier, self.edge_type))
    
    def connects(self, node):
        """
        Check if this edge connects to the given node.
        
        Args:
            node (Node): Node to check
            
        Returns:
            bool: True if edge connects to the node
        """
        return self.source == node or self.target == node
    
    def other_end(self, node):
        """
        Get the other end of the edge from the given node.
        
        Args:
            node (Node): One end of the edge
            
        Returns:
            Node: The other end of the edge
            
        Raises:
            ValueError: If the given node is not part of this edge
        """
        if self.source == node:
            return self.target
        elif self.target == node:
            return self.source
        else:
            raise ValueError(f"Node {node.identifier} is not part of this edge")


class Graph:
    """Represents a graph with nodes and edges."""
    
    def __init__(self):
        """Initialize an empty graph."""
        self._nodes = {}  # identifier -> Node
        self._edges = []  # list of Edge objects
        self._adjacency = defaultdict(list)  # node -> list of connected edges
        self._in_edges = defaultdict(list)  # node -> list of incoming edges (for directed)
        self._out_edges = defaultdict(list)  # node -> list of outgoing edges (for directed)
    
    def add_node(self, node):
        """
        Add a node to the graph.
        
        Args:
            node (Node): Node to add
            
        Returns:
            bool: True if node was added, False if it already exists
        """
        if node.identifier in self._nodes:
            return False
        
        self._nodes[node.identifier] = node
        self._adjacency[node.identifier] = []
        self._in_edges[node.identifier] = []
        self._out_edges[node.identifier] = []
        return True
    
    def add_edge(self, edge):
        """
        Add an edge to the graph.
        
        Args:
            edge (Edge): Edge to add
            
        Returns:
            bool: True if edge was added, False if it already exists
        """
        # Check if edge already exists
        if edge in self._edges:
            return False
        
        # Ensure both nodes exist
        if edge.source.identifier not in self._nodes:
            self.add_node(edge.source)
        if edge.target.identifier not in self._nodes:
            self.add_node(edge.target)
        
        self._edges.append(edge)
        
        # Update adjacency lists
        self._adjacency[edge.source.identifier].append(edge)
        if edge.edge_type == 'directed':
            self._out_edges[edge.source.identifier].append(edge)
            self._in_edges[edge.target.identifier].append(edge)
        else:
            # For undirected edges, add to both nodes
            self._adjacency[edge.target.identifier].append(edge)
        
        return True
    
    def get_node(self, identifier):
        """
        Get a node by its identifier.
        
        Args:
            identifier (str): Node identifier
            
        Returns:
            Node: The node with the given identifier, or None if not found
        """
        return self._nodes.get(identifier)
    
    def get_edge(self, source, target, edge_type='undirected'):
        """
        Get an edge between two nodes.
        
        Args:
            source (str): Source node identifier
            target (str): Target node identifier
            edge_type (str): Type of edge to look for
            
        Returns:
            Edge: The edge between the nodes, or None if not found
        """
        for edge in self._edges:
            if (edge.source.identifier == source and 
                edge.target.identifier == target and 
                edge.edge_type == edge_type):
                return edge
            elif (edge.edge_type == 'undirected' and
                  edge.source.identifier == target and 
                  edge.target.identifier == source):
                return edge
        return None
    
    def nodes(self):
        """Return an iterator over all nodes."""
        return iter(self._nodes.values())
    
    def edges(self):
        """Return an iterator over all edges."""
        return iter(self._edges)
    
    def node_count(self):
        """Return the number of nodes in the graph."""
        return len(self._nodes)
    
    def edge_count(self):
        """Return the number of edges in the graph."""
        return len(self._edges)
    
    def get_neighbors(self, node_identifier):
        """
        Get all neighbors of a node.
        For directed graphs, this returns the union of predecessors and successors.
        For undirected graphs, this returns all adjacent nodes.
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            list: List of neighboring Node objects
        """
        if node_identifier not in self._nodes:
            return []
        
        # For directed graphs, neighbors are union of predecessors and successors
        if self.is_directed():
            predecessors = self.get_predecessors(node_identifier)
            successors = self.get_successors(node_identifier)
            
            # Combine and remove duplicates
            neighbors = predecessors.copy()
            for successor in successors:
                if successor not in neighbors:
                    neighbors.append(successor)
            
            return neighbors
        else:
            # For undirected graphs, use adjacency list
            neighbors = []
            for edge in self._adjacency[node_identifier]:
                other = edge.other_end(self._nodes[node_identifier])
                if other not in neighbors:
                    neighbors.append(other)
            
            return neighbors
    
    def get_incident_edges(self, node_identifier):
        """
        Get all edges incident to a node.
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            list: List of Edge objects incident to the node
        """
        return self._adjacency.get(node_identifier, [])
    
    def get_outgoing_edges(self, node_identifier):
        """
        Get all outgoing edges from a node.
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            list: List of outgoing Edge objects
        """
        return self._out_edges.get(node_identifier, [])
    
    def get_incoming_edges(self, node_identifier):
        """
        Get all incoming edges to a node.
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            list: List of incoming Edge objects
        """
        return self._in_edges.get(node_identifier, [])
    
    def get_successors(self, node_identifier):
        """
        Get all successor nodes of a node (for directed edges).
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            list: List of successor Node objects
        """
        successors = []
        for edge in self._out_edges[node_identifier]:
            if edge.target.identifier != node_identifier:
                successors.append(edge.target)
            else:
                successors.append(edge.source)
        return successors
    
    def get_predecessors(self, node_identifier):
        """
        Get all predecessor nodes of a node (for directed edges).
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            list: List of predecessor Node objects
        """
        predecessors = []
        for edge in self._in_edges[node_identifier]:
            if edge.source.identifier != node_identifier:
                predecessors.append(edge.source)
            else:
                predecessors.append(edge.target)
        return predecessors
    
    def is_directed(self):
        """
        Check if the graph contains any directed edges.
        
        Returns:
            bool: True if graph contains directed edges
        """
        return any(edge.edge_type == 'directed' for edge in self._edges)
    
    def is_weighted(self):
        """
        Check if the graph contains any weighted edges.
        
        Returns:
            bool: True if graph contains weighted edges
        """
        return any(edge.weight is not None for edge in self._edges)
    
    def has_self_loops(self):
        """
        Check if the graph contains any self-loops.
        
        Returns:
            bool: True if graph contains self-loops
        """
        return any(edge.source == edge.target for edge in self._edges)
    
    def has_multiple_edges(self):
        """
        Check if the graph contains multiple edges between the same nodes.
        
        Returns:
            bool: True if graph contains multiple edges
        """
        edge_pairs = set()
        for edge in self._edges:
            # Create a canonical representation of the edge
            pair = tuple(sorted([edge.source.identifier, edge.target.identifier]))
            edge_pairs.add(pair)
        
        return len(edge_pairs) < len(self._edges)
    
    def __str__(self):
        return f"Graph({self.node_count()} nodes, {self.edge_count()} edges)"
    
    def __repr__(self):
        return f"Graph(nodes={self.node_count()}, edges={self.edge_count()})"


def create_graph_from_data(parsed_data):
    """
    Create a Graph object from parsed data.
    
    Args:
        parsed_data (dict): Dictionary with 'nodes' and 'edges' keys from parser
        
    Returns:
        Graph: The constructed graph
        
    Raises:
        ValueError: If parsed data is invalid
    """
    graph = Graph()
    
    # Add all nodes
    for node_data in parsed_data['nodes'].values():
        node = Node(node_data['identifier'], node_data['weight'])
        graph.add_node(node)
    
    # Add all edges
    for edge_data in parsed_data['edges']:
        source = graph.get_node(edge_data['source'])
        target = graph.get_node(edge_data['target'])
        
        if source is None or target is None:
            raise ValueError(f"Edge references non-existent nodes: {edge_data}")
        
        edge = Edge(source, target, edge_data['weight'], edge_data['label'], edge_data['type'])
        graph.add_edge(edge)
    
    return graph


# Example usage and testing
if __name__ == "__main__":
    # Create a simple test graph
    graph = Graph()
    
    # Add nodes
    node_a = Node('A')
    node_b = Node('B')
    node_c = Node('C')
    
    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_node(node_c)
    
    # Add edges
    edge1 = Edge(node_a, node_b, weight=1, edge_type='directed')
    edge2 = Edge(node_b, node_c, weight=2, edge_type='directed')
    edge3 = Edge(node_a, node_c, weight=3, edge_type='undirected')
    
    graph.add_edge(edge1)
    graph.add_edge(edge2)
    graph.add_edge(edge3)
    
    print(f"Graph: {graph}")
    print(f"Nodes: {list(graph.nodes())}")
    print(f"Edges: {list(graph.edges())}")
    print(f"Is directed: {graph.is_directed()}")
    print(f"Is weighted: {graph.is_weighted()}")
