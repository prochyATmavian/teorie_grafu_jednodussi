"""
Neighborhoods module for graph recognition system.
Implements functions for calculating node and edge neighborhoods and degrees.
"""

from .graph import Graph


class NeighborhoodCalculator:
    """Calculator for various node and edge neighborhoods."""
    
    def __init__(self, graph):
        """
        Initialize the neighborhood calculator.
        
        Args:
            graph (Graph): The graph to analyze
        """
        self.graph = graph
    
    def successors(self, node_identifier):
        """
        U+(F) - Successors of node F.
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            list: List of successor Node objects
        """
        return self.graph.get_successors(node_identifier)
    
    def predecessors(self, node_identifier):
        """
        U-(F) - Predecessors of node F.
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            list: List of predecessor Node objects
        """
        return self.graph.get_predecessors(node_identifier)
    
    def neighbors(self, node_identifier):
        """
        U(F) - Neighbors of node F (all predecessors and successors).
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            list: List of neighboring Node objects (without duplicates)
        """
        predecessors = self.predecessors(node_identifier)
        successors = self.successors(node_identifier)
        
        # Combine and remove duplicates
        all_neighbors = predecessors.copy()
        for neighbor in successors:
            if neighbor not in all_neighbors:
                all_neighbors.append(neighbor)
        
        return all_neighbors
    
    def outgoing_edges(self, node_identifier):
        """
        H+(C) - Outgoing edges from node C.
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            list: List of outgoing Edge objects
        """
        return self.graph.get_outgoing_edges(node_identifier)
    
    def incoming_edges(self, node_identifier):
        """
        H-(C) - Incoming edges to node C.
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            list: List of incoming Edge objects
        """
        return self.graph.get_incoming_edges(node_identifier)
    
    def incident_edges(self, node_identifier):
        """
        H(C) - All edges incident to node C.
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            list: List of all incident Edge objects
        """
        return self.graph.get_incident_edges(node_identifier)
    
    def out_degree(self, node_identifier):
        """
        d+(A) - Out-degree of node A.
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            int: Out-degree of the node
        """
        return len(self.outgoing_edges(node_identifier))
    
    def in_degree(self, node_identifier):
        """
        d-(A) - In-degree of node A.
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            int: In-degree of the node
        """
        return len(self.incoming_edges(node_identifier))
    
    def degree(self, node_identifier):
        """
        d(A) - Total degree of node A.
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            int: Total degree of the node
        """
        return len(self.incident_edges(node_identifier))
    
    def get_all_neighborhoods(self, node_identifier):
        """
        Get all neighborhood information for a node.
        
        Args:
            node_identifier (str): Identifier of the node
            
        Returns:
            dict: Dictionary containing all neighborhood information
        """
        return {
            'successors': self.successors(node_identifier),
            'predecessors': self.predecessors(node_identifier),
            'neighbors': self.neighbors(node_identifier),
            'outgoing_edges': self.outgoing_edges(node_identifier),
            'incoming_edges': self.incoming_edges(node_identifier),
            'incident_edges': self.incident_edges(node_identifier),
            'out_degree': self.out_degree(node_identifier),
            'in_degree': self.in_degree(node_identifier),
            'degree': self.degree(node_identifier)
        }
    
    def get_all_degrees(self):
        """
        Get degree information for all nodes in the graph.
        
        Returns:
            dict: Dictionary mapping node identifiers to degree information
        """
        degrees = {}
        for node in self.graph.nodes():
            degrees[node.identifier] = {
                'out_degree': self.out_degree(node.identifier),
                'in_degree': self.in_degree(node.identifier),
                'degree': self.degree(node.identifier)
            }
        return degrees
    
    def print_neighborhoods(self, node_identifier):
        """
        Print all neighborhood information for a node in a formatted way.
        
        Args:
            node_identifier (str): Identifier of the node
        """
        if self.graph.get_node(node_identifier) is None:
            print(f"Node '{node_identifier}' not found in graph")
            return
        
        neighborhoods = self.get_all_neighborhoods(node_identifier)
        
        print(f"Neighborhood information for node '{node_identifier}':")
        print(f"  U+({node_identifier}) - Successors: {[n.identifier for n in neighborhoods['successors']]}")
        print(f"  U-({node_identifier}) - Predecessors: {[n.identifier for n in neighborhoods['predecessors']]}")
        print(f"  U({node_identifier}) - Neighbors: {[n.identifier for n in neighborhoods['neighbors']]}")
        print(f"  H+({node_identifier}) - Outgoing edges: {len(neighborhoods['outgoing_edges'])} edges")
        print(f"  H-({node_identifier}) - Incoming edges: {len(neighborhoods['incoming_edges'])} edges")
        print(f"  H({node_identifier}) - Incident edges: {len(neighborhoods['incident_edges'])} edges")
        print(f"  d+({node_identifier}) - Out-degree: {neighborhoods['out_degree']}")
        print(f"  d-({node_identifier}) - In-degree: {neighborhoods['in_degree']}")
        print(f"  d({node_identifier}) - Total degree: {neighborhoods['degree']}")
        
        # Print edge details
        if neighborhoods['outgoing_edges']:
            print(f"    Outgoing edges:")
            for edge in neighborhoods['outgoing_edges']:
                weight_info = f" (weight: {edge.weight})" if edge.weight is not None else ""
                label_info = f" [label: {edge.label}]" if edge.label is not None else ""
                print(f"      {edge.source.identifier} -> {edge.target.identifier}{weight_info}{label_info}")
        
        if neighborhoods['incoming_edges']:
            print(f"    Incoming edges:")
            for edge in neighborhoods['incoming_edges']:
                weight_info = f" (weight: {edge.weight})" if edge.weight is not None else ""
                label_info = f" [label: {edge.label}]" if edge.label is not None else ""
                print(f"      {edge.source.identifier} -> {edge.target.identifier}{weight_info}{label_info}")


def calculate_neighborhoods(graph, node_identifier):
    """
    Convenience function to calculate all neighborhoods for a node.
    
    Args:
        graph (Graph): The graph to analyze
        node_identifier (str): Identifier of the node
        
    Returns:
        dict: Dictionary containing all neighborhood information
    """
    calculator = NeighborhoodCalculator(graph)
    return calculator.get_all_neighborhoods(node_identifier)


def calculate_all_degrees(graph):
    """
    Convenience function to calculate degrees for all nodes.
    
    Args:
        graph (Graph): The graph to analyze
        
    Returns:
        dict: Dictionary mapping node identifiers to degree information
    """
    calculator = NeighborhoodCalculator(graph)
    return calculator.get_all_degrees()


def print_node_degrees(graph):
    """
    Print degree information for all nodes in the graph.
    
    Args:
        graph (Graph): The graph to analyze
    """
    calculator = NeighborhoodCalculator(graph)
    degrees = calculator.get_all_degrees()
    
    print("Degree information for all nodes:")
    print("Node\tOut-degree\tIn-degree\tTotal degree")
    print("-" * 45)
    
    for node_id, degree_info in degrees.items():
        print(f"{node_id}\t{degree_info['out_degree']}\t\t{degree_info['in_degree']}\t\t{degree_info['degree']}")


def print_node_relationships(graph, node_identifier):
    """
    Vypíše počet a seznam sousedů, předchůdců a následovníků pro daný uzel.
    
    Args:
        graph (Graph): Graf objekt
        node_identifier (str): Identifikátor uzlu
    """
    print(f"=== Vztahy pro uzel '{node_identifier}' ===")
    
    # Získání všech sousedů
    neighbors = graph.get_neighbors(node_identifier)
    print(f"\nSousedé ({len(neighbors)}):")
    if neighbors:
        neighbor_ids = [node.identifier for node in neighbors]
        print(f"  {neighbor_ids}")
    else:
        print("  Žádní sousedé")
    
    # Získání předchůdců (pouze pro orientované grafy)
    predecessors = graph.get_predecessors(node_identifier)
    print(f"\nPředchůdci ({len(predecessors)}):")
    if predecessors:
        predecessor_ids = [node.identifier for node in predecessors]
        print(f"  {predecessor_ids}")
    else:
        print("  Žádní předchůdci")
    
    # Získání následovníků (pouze pro orientované grafy)
    successors = graph.get_successors(node_identifier)
    print(f"\nNásledovníci ({len(successors)}):")
    if successors:
        successor_ids = [node.identifier for node in successors]
        print(f"  {successor_ids}")
    else:
        print("  Žádní následovníci")
    
    # Dodatečné informace
    print(f"\nDodatečné informace:")
    print(f"  Celkový stupeň: {len(neighbors)}")
    print(f"  Vstupní stupeň: {len(predecessors)}")
    print(f"  Výstupní stupeň: {len(successors)}")


def print_node_neighborhoods(graph, node_identifier):
    """
    Vypíše vstupní a výstupní okolí pro konkrétní uzel.
    
    Args:
        graph (Graph): Graf objekt
        node_identifier (str): Identifikátor uzlu
    """
    print(f"=== Vstupní a výstupní okolí pro uzel '{node_identifier}' ===")
    
    # Získání příchozích hran
    incoming_edges = graph.get_incoming_edges(node_identifier)
    print(f"\nVstupní okolí ({len(incoming_edges)} hran):")
    if incoming_edges:
        for edge in incoming_edges:
            weight_info = f" (váha: {edge.weight})" if edge.weight is not None else ""
            label_info = f" [popisek: {edge.label}]" if edge.label is not None else ""
            print(f"  {edge.source.identifier} -> {edge.target.identifier}{weight_info}{label_info}")
    else:
        print("  Žádné příchozí hrany")
    
    # Získání odchozích hran
    outgoing_edges = graph.get_outgoing_edges(node_identifier)
    print(f"\nVýstupní okolí ({len(outgoing_edges)} hran):")
    if outgoing_edges:
        for edge in outgoing_edges:
            weight_info = f" (váha: {edge.weight})" if edge.weight is not None else ""
            label_info = f" [popisek: {edge.label}]" if edge.label is not None else ""
            print(f"  {edge.source.identifier} -> {edge.target.identifier}{weight_info}{label_info}")
    else:
        print("  Žádné odchozí hrany")
    
    # Získání všech incidentních hran (kombinace příchozích a odchozích)
    all_incident_edges = incoming_edges + outgoing_edges
    print(f"\nVšechny incidentní hrany ({len(all_incident_edges)} hran):")
    if all_incident_edges:
        for edge in all_incident_edges:
            weight_info = f" (váha: {edge.weight})" if edge.weight is not None else ""
            label_info = f" [popisek: {edge.label}]" if edge.label is not None else ""
            direction = "->" if edge.edge_type == 'directed' else "-"
            print(f"  {edge.source.identifier} {direction} {edge.target.identifier}{weight_info}{label_info}")
    else:
        print("  Žádné incidentní hrany")
    
    # Souhrnné informace
    print(f"\nSouhrnné informace:")
    print(f"  Počet příchozích hran: {len(incoming_edges)}")
    print(f"  Počet odchozích hran: {len(outgoing_edges)}")
    print(f"  Celkový počet incidentních hran: {len(all_incident_edges)}")


# Example usage and testing
if __name__ == "__main__":
    from .parser import parse_graph
    from .graph import create_graph_from_data
    
    # Test with a sample graph file
    try:
        # Parse a graph file
        data = parse_graph("grafy/01.tg")
        graph = create_graph_from_data(data)
        
        # Create neighborhood calculator
        calc = NeighborhoodCalculator(graph)
        
        # Test with node A
        print("Testing neighborhoods for node A:")
        calc.print_neighborhoods('A')
        
        print("\nDegree information for all nodes:")
        print_node_degrees(graph)
        
        print("\n" + "="*60)
        print("Testing print_node_relationships function:")
        print_node_relationships(graph, 'A')
        
        print("\n" + "="*60)
        print("Testing print_node_neighborhoods function:")
        print_node_neighborhoods(graph, 'A')
        
    except Exception as e:
        print(f"Error: {e}")
