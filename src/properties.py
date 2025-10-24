"""
Properties module for graph recognition system.
Implements graph property detection algorithms (a-j).
"""

from collections import deque
from .graph import Graph


class GraphPropertyDetector:
    """Detector for various graph properties."""
    
    def __init__(self, graph):
        """
        Initialize the property detector.
        
        Args:
            graph (Graph): The graph to analyze
        """
        self.graph = graph
    
    def is_weighted(self):
        """
        a) Ohodnocený (weighted) - Check if graph has weighted edges.
        
        Returns:
            bool: True if graph has weighted edges
        """
        return self.graph.is_weighted()
    
    def is_directed(self):
        """
        b) Orientovaný (directed) - Check if graph has directed edges.
        
        Returns:
            bool: True if graph has directed edges
        """
        return self.graph.is_directed()
    
    def is_strongly_connected(self):
        """
        c) Silně souvislý (strongly connected) - Check if graph is strongly connected.
        For directed graphs: there's a path from every node to every other node.
        For undirected graphs: same as weakly connected.
        
        Returns:
            bool: True if graph is strongly connected
        """
        if self.graph.node_count() == 0:
            return True
        
        # For undirected graphs, strongly connected is the same as weakly connected
        if not self.is_directed():
            return self.is_weakly_connected()
        
        # For directed graphs, check if every node can reach every other node
        node_list = list(self.graph.nodes())
        
        for start_node in node_list:
            if not self._can_reach_all_nodes(start_node.identifier, node_list):
                return False
        
        return True
    
    def is_weakly_connected(self):
        """
        c) Slabě souvislý (weakly connected) - Check if graph is weakly connected.
        Treat directed graph as undirected and check connectivity.
        
        Returns:
            bool: True if graph is weakly connected
        """
        if self.graph.node_count() == 0:
            return True
        
        # Use BFS to check connectivity
        start_node = list(self.graph.nodes())[0]
        visited = set()
        queue = deque([start_node.identifier])
        visited.add(start_node.identifier)
        
        while queue:
            current = queue.popleft()
            # Get all neighbors (treating all edges as undirected)
            neighbors = self._get_all_neighbors(current)
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return len(visited) == self.graph.node_count()
    
    def is_simple_no_multiedges(self):
        """
        d) Prostý (simple - no multi-edges) - Check if graph has no multiple edges.
        
        Returns:
            bool: True if graph has no multiple edges
        """
        return not self.graph.has_multiple_edges()
    
    def is_simple(self):
        """
        e) Jednoduchý (simple - no loops or multi-edges) - Check if graph has no loops or multiple edges.
        
        Returns:
            bool: True if graph has no loops and no multiple edges
        """
        return not self.graph.has_self_loops() and not self.graph.has_multiple_edges()
    
    def is_planar(self):
        """
        f) Rovinný (planar) - Check if graph is planar.
        Uses Euler's formula: V - E + F = 2 for connected planar graphs.
        For disconnected graphs: V - E + F = C + 1, where C is number of components.
        
        Returns:
            bool: True if graph is planar
        """
        # Simple planar check using Kuratowski's theorem conditions
        # A graph is planar if it doesn't contain K5 or K3,3 as minors
        
        # Basic checks
        if self.graph.node_count() < 5:
            return True
        
        # Check for K5 (complete graph with 5 vertices)
        if self._has_k5_subgraph():
            return False
        
        # Check for K3,3 (complete bipartite graph with 3 vertices in each partition)
        if self._has_k33_subgraph():
            return False
        
        # Additional planar condition: |E| <= 3|V| - 6 for connected graphs
        if self.is_weakly_connected():
            return self.graph.edge_count() <= 3 * self.graph.node_count() - 6
        
        # For disconnected graphs, check each component
        return self._check_planar_components()
    
    def is_finite(self):
        """
        g) Konečný (finite) - Check if graph is finite.
        Always true for our implementation.
        
        Returns:
            bool: Always True
        """
        return True
    
    def is_complete(self):
        """
        h) Úplný (complete) - Check if graph is complete.
        Every node is connected to every other node.
        
        Returns:
            bool: True if graph is complete
        """
        n = self.graph.node_count()
        if n <= 1:
            return True
        
        # For complete graph, we need n*(n-1)/2 edges for undirected
        # or n*(n-1) edges for directed
        expected_edges = n * (n - 1) // 2 if not self.is_directed() else n * (n - 1)
        
        return self.graph.edge_count() == expected_edges
    
    def is_regular(self):
        """
        i) Regulární (regular) - Check if graph is regular.
        All nodes have the same degree.
        
        Returns:
            bool: True if graph is regular
        """
        if self.graph.node_count() <= 1:
            return True
        
        degrees = []
        from .neighborhoods import NeighborhoodCalculator
        calc = NeighborhoodCalculator(self.graph)
        for node in self.graph.nodes():
            degrees.append(calc.degree(node.identifier))
        
        return all(degree == degrees[0] for degree in degrees)
    
    def is_bipartite(self):
        """
        j) Bipartitní (bipartite) - Check if graph is bipartite.
        Uses BFS coloring to detect odd-length cycles.
        
        Returns:
            bool: True if graph is bipartite
        """
        if self.graph.node_count() == 0:
            return True
        
        # Color nodes with two colors (0 and 1)
        color = {}
        node_list = list(self.graph.nodes())
        
        # Check each connected component
        for start_node in node_list:
            if start_node.identifier not in color:
                if not self._is_bipartite_component(start_node.identifier, color):
                    return False
        
        return True
    
    def _can_reach_all_nodes(self, start_identifier, all_nodes):
        """
        Check if a node can reach all other nodes in the graph.
        
        Args:
            start_identifier (str): Starting node identifier
            all_nodes (list): List of all nodes in the graph
            
        Returns:
            bool: True if can reach all nodes
        """
        visited = set()
        queue = deque([start_identifier])
        visited.add(start_identifier)
        
        while queue:
            current = queue.popleft()
            # Get successors (for directed reachability)
            successors = self.graph.get_successors(current)
            
            for successor in successors:
                if successor.identifier not in visited:
                    visited.add(successor.identifier)
                    queue.append(successor.identifier)
        
        return len(visited) == len(all_nodes)
    
    def _get_all_neighbors(self, node_identifier):
        """
        Get all neighbors treating all edges as undirected.
        
        Args:
            node_identifier (str): Node identifier
            
        Returns:
            list: List of neighbor identifiers
        """
        neighbors = set()
        incident_edges = self.graph.get_incident_edges(node_identifier)
        
        for edge in incident_edges:
            if edge.source.identifier == node_identifier:
                neighbors.add(edge.target.identifier)
            else:
                neighbors.add(edge.source.identifier)
        
        return list(neighbors)
    
    def _has_k5_subgraph(self):
        """
        Check if graph contains K5 as a subgraph.
        
        Returns:
            bool: True if contains K5
        """
        nodes = list(self.graph.nodes())
        
        # Check all combinations of 5 nodes
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                for k in range(j + 1, len(nodes)):
                    for l in range(k + 1, len(nodes)):
                        for m in range(l + 1, len(nodes)):
                            if self._is_complete_5(nodes[i], nodes[j], nodes[k], nodes[l], nodes[m]):
                                return True
        
        return False
    
    def _is_complete_5(self, n1, n2, n3, n4, n5):
        """
        Check if 5 nodes form a complete subgraph.
        
        Args:
            n1, n2, n3, n4, n5: Node objects
            
        Returns:
            bool: True if they form K5
        """
        nodes = [n1, n2, n3, n4, n5]
        
        # Check all pairs
        for i in range(5):
            for j in range(i + 1, 5):
                if not self.graph.get_edge(nodes[i].identifier, nodes[j].identifier):
                    return False
        
        return True
    
    def _has_k33_subgraph(self):
        """
        Check if graph contains K3,3 as a subgraph.
        
        Returns:
            bool: True if contains K3,3
        """
        nodes = list(self.graph.nodes())
        
        # Check all combinations of 6 nodes split into two groups of 3
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                for k in range(j + 1, len(nodes)):
                    for l in range(k + 1, len(nodes)):
                        for m in range(l + 1, len(nodes)):
                            for n in range(m + 1, len(nodes)):
                                if self._is_k33(nodes[i], nodes[j], nodes[k], nodes[l], nodes[m], nodes[n]):
                                    return True
        
        return False
    
    def _is_k33(self, a1, a2, a3, b1, b2, b3):
        """
        Check if 6 nodes form K3,3 bipartite graph.
        
        Args:
            a1, a2, a3, b1, b2, b3: Node objects
            
        Returns:
            bool: True if they form K3,3
        """
        partition_a = [a1, a2, a3]
        partition_b = [b1, b2, b3]
        
        # Check that all nodes in partition A connect to all nodes in partition B
        for a_node in partition_a:
            for b_node in partition_b:
                if not self.graph.get_edge(a_node.identifier, b_node.identifier):
                    return False
        
        # Check that no nodes within the same partition are connected
        for i in range(3):
            for j in range(i + 1, 3):
                if self.graph.get_edge(partition_a[i].identifier, partition_a[j].identifier):
                    return False
                if self.graph.get_edge(partition_b[i].identifier, partition_b[j].identifier):
                    return False
        
        return True
    
    def _check_planar_components(self):
        """
        Check planarity for disconnected graph components.
        
        Returns:
            bool: True if all components are planar
        """
        # Find connected components
        components = self._find_connected_components()
        
        for component in components:
            # Create subgraph for component
            component_graph = self._create_subgraph(component)
            detector = GraphPropertyDetector(component_graph)
            
            if not detector.is_planar():
                return False
        
        return True
    
    def _find_connected_components(self):
        """
        Find all connected components in the graph.
        
        Returns:
            list: List of components, each containing node identifiers
        """
        visited = set()
        components = []
        
        for node in self.graph.nodes():
            if node.identifier not in visited:
                component = []
                self._dfs_component(node.identifier, visited, component)
                components.append(component)
        
        return components
    
    def _dfs_component(self, start, visited, component):
        """
        DFS to find connected component.
        
        Args:
            start (str): Starting node identifier
            visited (set): Set of visited nodes
            component (list): Component being built
        """
        visited.add(start)
        component.append(start)
        
        neighbors = self._get_all_neighbors(start)
        for neighbor in neighbors:
            if neighbor not in visited:
                self._dfs_component(neighbor, visited, component)
    
    def _create_subgraph(self, node_identifiers):
        """
        Create subgraph with given nodes.
        
        Args:
            node_identifiers (list): List of node identifiers
            
        Returns:
            Graph: Subgraph
        """
        from .graph import Graph
        
        subgraph = Graph()
        
        # Add nodes
        for node_id in node_identifiers:
            node = self.graph.get_node(node_id)
            if node:
                subgraph.add_node(node)
        
        # Add edges
        for edge in self.graph.edges():
            if (edge.source.identifier in node_identifiers and 
                edge.target.identifier in node_identifiers):
                subgraph.add_edge(edge)
        
        return subgraph
    
    def _is_bipartite_component(self, start_identifier, color):
        """
        Check if a connected component is bipartite using BFS coloring.
        
        Args:
            start_identifier (str): Starting node identifier
            color (dict): Color dictionary to fill
            
        Returns:
            bool: True if component is bipartite
        """
        queue = deque([start_identifier])
        color[start_identifier] = 0
        
        while queue:
            current = queue.popleft()
            neighbors = self._get_all_neighbors(current)
            
            for neighbor in neighbors:
                if neighbor not in color:
                    color[neighbor] = 1 - color[current]
                    queue.append(neighbor)
                elif color[neighbor] == color[current]:
                    return False
        
        return True
    
    def detect_all_properties(self):
        """
        Detect all graph properties.
        
        Returns:
            dict: Dictionary containing all property detection results
        """
        return {
            'a) ohodnocený (weighted)': self.is_weighted(),
            'b) orientovaný (directed)': self.is_directed(),
            'c) silně souvislý (strongly connected)': self.is_strongly_connected(),
            'c) slabě souvislý (weakly connected)': self.is_weakly_connected(),
            'd) prostý (simple - no multi-edges)': self.is_simple_no_multiedges(),
            'e) jednoduchý (simple - no loops or multi-edges)': self.is_simple(),
            'f) rovinný (planar)': self.is_planar(),
            'g) konečný (finite)': self.is_finite(),
            'h) úplný (complete)': self.is_complete(),
            'i) regulární (regular)': self.is_regular(),
            'j) bipartitní (bipartite)': self.is_bipartite()
        }
    
    def print_properties(self):
        """
        Print all graph properties in a formatted way.
        """
        properties = self.detect_all_properties()
        
        print("Graph Properties:")
        print("=" * 50)
        
        for property_name, value in properties.items():
            status = "YES" if value else "NO"
            print(f"{property_name}: {status}")
        
        print("=" * 50)


def detect_all_properties(graph):
    """
    Convenience function to detect all properties of a graph.
    
    Args:
        graph (Graph): The graph to analyze
        
    Returns:
        dict: Dictionary containing all property detection results
    """
    detector = GraphPropertyDetector(graph)
    return detector.detect_all_properties()


def print_graph_properties(graph):
    """
    Convenience function to print all properties of a graph.
    
    Args:
        graph (Graph): The graph to analyze
    """
    detector = GraphPropertyDetector(graph)
    detector.print_properties()


# Example usage and testing
if __name__ == "__main__":
    from .parser import parse_graph
    from .graph import create_graph_from_data
    
    # Test with a sample graph file
    try:
        # Parse a graph file
        data = parse_graph("../grafy/01.tg")
        graph = create_graph_from_data(data)
        
        # Create property detector
        detector = GraphPropertyDetector(graph)
        
        # Print all properties
        detector.print_properties()
        
    except Exception as e:
        print(f"Error: {e}")
