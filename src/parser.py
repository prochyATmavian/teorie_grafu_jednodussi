"""
Parser module for graph recognition system.
Parses .tg files into structured data for graph construction.
"""

import re
import os


class ParseError(Exception):
    """Custom exception for parsing errors."""
    pass


def parse_graph(file_path):
    """
    Parse a .tg file and return structured data for graph construction.
    
    Args:
        file_path (str): Path to the .tg file
        
    Returns:
        dict: Dictionary with 'nodes' and 'edges' keys containing parsed data
        
    Raises:
        ParseError: If file cannot be parsed or contains invalid syntax
        FileNotFoundError: If file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Graph file not found: {file_path}")
    
    nodes = {}
    edges = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Parse node definition: u identifier [weight];
                if line.startswith('u '):
                    node_data = _parse_node(line, line_num)
                    nodes[node_data['identifier']] = node_data
                
                # Parse edge definition: h node1 (<|-|>) node2 [weight] [:label];
                elif line.startswith('h '):
                    edge_data = _parse_edge(line, line_num, nodes)
                    edges.append(edge_data)
                
                else:
                    raise ParseError(f"Line {line_num}: Invalid syntax - line must start with 'u ' or 'h '")
    
    except ParseError:
        raise
    except Exception as e:
        raise ParseError(f"Error reading file: {e}")
    
    return {'nodes': nodes, 'edges': edges}


def _parse_node(line, line_num):
    """
    Parse a node definition line.
    
    Args:
        line (str): Line to parse
        line_num (int): Line number for error reporting
        
    Returns:
        dict: Dictionary with 'identifier' and 'weight' keys
    """
    # Pattern: u identifier [weight];
    pattern = r'^u\s+(\S+?)\s*(?:\s+([+-]?\d*\.?\d+))?\s*;?\s*$'
    match = re.match(pattern, line)
    
    if not match:
        raise ParseError(f"Line {line_num}: Invalid node syntax: {line}")
    
    identifier = match.group(1)
    weight_str = match.group(2)
    
    weight = None
    if weight_str:
        try:
            weight = float(weight_str)
            # Convert to int if it's a whole number
            if weight.is_integer():
                weight = int(weight)
        except ValueError:
            raise ParseError(f"Line {line_num}: Invalid node weight: {weight_str}")
    
    return {
        'identifier': identifier,
        'weight': weight
    }


def _parse_edge(line, line_num, nodes):
    """
    Parse an edge definition line.
    
    Args:
        line (str): Line to parse
        line_num (int): Line number for error reporting
        nodes (dict): Dictionary of existing nodes to validate against
        
    Returns:
        dict: Dictionary with edge data
    """
    # Pattern: h node1 (<|-|>) node2 [weight] [:label];
    pattern = r'^h\s+(\S+)\s+(<|>|-)\s+(\S+)\s*(?:\s+([+-]?\d*\.?\d+))?\s*(?::(\S+?))?\s*;?\s*$'
    match = re.match(pattern, line)
    
    if not match:
        raise ParseError(f"Line {line_num}: Invalid edge syntax: {line}")
    
    source = match.group(1)
    direction = match.group(2)
    target = match.group(3)
    weight_str = match.group(4)
    label = match.group(5)
    
    # Validate that nodes exist (they might be defined later, so we'll check during graph construction)
    
    weight = None
    if weight_str:
        try:
            weight = float(weight_str)
            # Convert to int if it's a whole number
            if weight.is_integer():
                weight = int(weight)
        except ValueError:
            raise ParseError(f"Line {line_num}: Invalid edge weight: {weight_str}")
    
    # Determine edge type
    if direction == '>':
        edge_type = 'directed'
    elif direction == '<':
        edge_type = 'directed'
        # Swap source and target for '<' direction
        source, target = target, source
    elif direction == '-':
        edge_type = 'undirected'
    else:
        raise ParseError(f"Line {line_num}: Invalid edge direction: {direction}")
    
    return {
        'source': source,
        'target': target,
        'weight': weight,
        'label': label,
        'type': edge_type
    }


def validate_graph_data(nodes, edges):
    """
    Validate that all edges reference existing nodes.
    
    Args:
        nodes (dict): Dictionary of nodes
        edges (list): List of edges
        
    Raises:
        ParseError: If any edge references non-existent nodes
    """
    node_ids = set(nodes.keys())
    
    for i, edge in enumerate(edges):
        if edge['source'] not in node_ids:
            raise ParseError(f"Edge {i+1}: Source node '{edge['source']}' not defined")
        if edge['target'] not in node_ids:
            raise ParseError(f"Edge {i+1}: Target node '{edge['target']}' not defined")


# Example usage and testing
if __name__ == "__main__":
    # Test with one of the example files
    test_file = "../grafy/01.tg"
    try:
        data = parse_graph(test_file)
        print("Parsed nodes:", len(data['nodes']))
        print("Parsed edges:", len(data['edges']))
        
        # Print first few nodes and edges
        for i, (node_id, node_data) in enumerate(data['nodes'].items()):
            if i < 3:
                print(f"Node: {node_id}, weight: {node_data['weight']}")
        
        for i, edge in enumerate(data['edges']):
            if i < 3:
                print(f"Edge: {edge['source']} -> {edge['target']}, weight: {edge['weight']}, type: {edge['type']}")
                
    except Exception as e:
        print(f"Error: {e}")
