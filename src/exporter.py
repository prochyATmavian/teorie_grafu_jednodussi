"""
Exporter module for graph recognition system.
Handles CSV export and import functionality for matrices and graph data.
"""

import csv
import os
import math
from .graph import Graph


class GraphExporter:
    """Exporter for graph data to CSV format."""
    
    def __init__(self, graph):
        """
        Initialize the exporter.
        
        Args:
            graph (Graph): The graph to export
        """
        self.graph = graph
    
    def export_matrix_to_csv(self, matrix, filename="matrix.csv", matrix_type="matrix", row_labels=None, col_labels=None):
        """
        Export a matrix to CSV file optimized for Excel processing.
        Each value gets its own cell, simple format without extra headers.
        
        Args:
            matrix (list): 2D matrix to export
            filename (str): Name of the CSV file
            matrix_type (str): Type of matrix for documentation
            row_labels (list): Optional labels for rows
            col_labels (list): Optional labels for columns
            
        Returns:
            str: Path to the exported file
        """
        # Ensure csv_files directory exists
        csv_dir = "csv_files"
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        
        filepath = os.path.join(csv_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write column headers if provided
                if col_labels:
                    header = [''] + col_labels  # Empty cell for row labels
                    writer.writerow(header)
                    
                    # Write rows with row labels
                    for i, row in enumerate(matrix):
                        row_data = [row_labels[i] if row_labels else '']  # Row label
                        for value in row:
                            if isinstance(value, float) and math.isinf(value):
                                row_data.append("inf")
                            elif value is None:
                                row_data.append("")
                            else:
                                row_data.append(str(value))
                        writer.writerow(row_data)
                else:
                    # Write matrix without labels - each value in its own cell
                    for row in matrix:
                        row_data = []
                        for value in row:
                            if isinstance(value, float) and math.isinf(value):
                                row_data.append("inf")
                            elif value is None:
                                row_data.append("")
                            else:
                                row_data.append(str(value))
                        writer.writerow(row_data)
                
                print(f"Matrix exported to: {filepath}")
                return filepath
                
        except Exception as e:
            print(f"Error exporting matrix: {e}")
            return None
    
    def export_adjacency_matrix(self, filename="adjacency_matrix.csv"):
        """
        Export adjacency matrix to CSV.
        
        Args:
            filename (str): Name of the CSV file
            
        Returns:
            str: Path to the exported file
        """
        from .matrices import GraphMatrixGenerator
        
        generator = GraphMatrixGenerator(self.graph)
        matrix = generator.adjacency_matrix()
        node_labels = [node.identifier for node in self.graph.nodes()]
        
        return self.export_matrix_to_csv(matrix, filename, "Adjacency", node_labels, node_labels)
    
    def export_sign_matrix(self, filename="sign_matrix.csv"):
        """
        Export sign matrix to CSV.
        
        Args:
            filename (str): Name of the CSV file
            
        Returns:
            str: Path to the exported file
        """
        from .matrices import GraphMatrixGenerator
        
        generator = GraphMatrixGenerator(self.graph)
        matrix = generator.sign_matrix()
        node_labels = [node.identifier for node in self.graph.nodes()]
        
        return self.export_matrix_to_csv(matrix, filename, "Sign", node_labels, node_labels)
    
    def export_incidence_matrix(self, filename="incidence_matrix.csv"):
        """
        Export incidence matrix to CSV optimized for Excel processing.
        
        Args:
            filename (str): Name of the CSV file
            
        Returns:
            str: Path to the exported file
        """
        from .matrices import GraphMatrixGenerator
        
        generator = GraphMatrixGenerator(self.graph)
        matrix, node_labels, edge_labels = generator.incidence_matrix()
        
        return self.export_matrix_to_csv(matrix, filename, "Incidence", node_labels, edge_labels)
    
    def export_distance_matrix(self, filename="distance_matrix.csv"):
        """
        Export distance matrix to CSV.
        
        Args:
            filename (str): Name of the CSV file
            
        Returns:
            str: Path to the exported file
        """
        from .matrices import GraphMatrixGenerator
        
        generator = GraphMatrixGenerator(self.graph)
        matrix = generator.distance_matrix()
        node_labels = [node.identifier for node in self.graph.nodes()]
        
        return self.export_matrix_to_csv(matrix, filename, "Distance", node_labels, node_labels)
    
    def export_predecessor_matrix(self, filename="predecessor_matrix.csv"):
        """
        Export predecessor matrix to CSV.
        
        Args:
            filename (str): Name of the CSV file
            
        Returns:
            str: Path to the exported file
        """
        from .matrices import GraphMatrixGenerator
        
        generator = GraphMatrixGenerator(self.graph)
        matrix = generator.predecessor_matrix()
        node_labels = [node.identifier for node in self.graph.nodes()]
        
        # Convert predecessor indices to node identifiers
        converted_matrix = []
        for row in matrix:
            converted_row = []
            for pred_index in row:
                if pred_index is not None:
                    converted_row.append(node_labels[pred_index])
                else:
                    converted_row.append("")
            converted_matrix.append(converted_row)
        
        return self.export_matrix_to_csv(converted_matrix, filename, "Predecessor", node_labels, node_labels)
    
    def export_adjacency_list(self, filename="adjacency_list.csv"):
        """
        Export adjacency list to CSV optimized for Excel processing.
        Each neighbor gets its own column for easy Excel analysis.
        
        Args:
            filename (str): Name of the CSV file
            
        Returns:
            str: Path to the exported file
        """
        from .matrices import GraphMatrixGenerator
        
        generator = GraphMatrixGenerator(self.graph)
        adj_list = generator.adjacency_list()
        
        # Ensure csv_files directory exists
        csv_dir = "csv_files"
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        
        filepath = os.path.join(csv_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Find maximum number of neighbors to determine columns
                max_neighbors = max(len(neighbors) for neighbors in adj_list.values()) if adj_list else 0
                
                # Write header row
                header = ["Node"]
                for i in range(max_neighbors):
                    header.append(f"Neighbor_{i+1}")
                writer.writerow(header)
                
                # Write adjacency list - each neighbor in separate column
                for node_id, neighbors in adj_list.items():
                    row_data = [node_id]
                    # Add neighbors, pad with empty strings if needed
                    for i in range(max_neighbors):
                        if i < len(neighbors):
                            # Extract just the neighbor node ID, not the full description
                            neighbor = neighbors[i]
                            if isinstance(neighbor, str) and ' ->' in neighbor:
                                # Extract node ID from format like "B (weight: 1) ->"
                                neighbor = neighbor.split(' ')[0]
                            row_data.append(neighbor)
                        else:
                            row_data.append("")
                    writer.writerow(row_data)
                
                print(f"Adjacency list exported to: {filepath}")
                return filepath
                
        except Exception as e:
            print(f"Error exporting adjacency list: {e}")
            return None
    
    def export_graph_properties(self, filename="graph_properties.csv"):
        """
        Export graph properties to CSV optimized for Excel processing.
        Simple two-column format: Property | Value.
        
        Args:
            filename (str): Name of the CSV file
            
        Returns:
            str: Path to the exported file
        """
        from .properties import GraphPropertyDetector
        
        detector = GraphPropertyDetector(self.graph)
        properties = detector.detect_all_properties()
        
        # Ensure csv_files directory exists
        csv_dir = "csv_files"
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        
        filepath = os.path.join(csv_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header row
                writer.writerow(["Property", "Value"])
                
                # Write properties - each property and value in separate cells
                for property_name, value in properties.items():
                    writer.writerow([property_name, "YES" if value else "NO"])
                
                print(f"Graph properties exported to: {filepath}")
                return filepath
                
        except Exception as e:
            print(f"Error exporting graph properties: {e}")
            return None
    
    def export_node_degrees(self, filename="node_degrees.csv"):
        """
        Export node degrees to CSV optimized for Excel processing.
        Each degree type gets its own column for easy analysis.
        
        Args:
            filename (str): Name of the CSV file
            
        Returns:
            str: Path to the exported file
        """
        from .neighborhoods import NeighborhoodCalculator
        
        calculator = NeighborhoodCalculator(self.graph)
        degrees = calculator.get_all_degrees()
        
        # Ensure csv_files directory exists
        csv_dir = "csv_files"
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        
        filepath = os.path.join(csv_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header row
                writer.writerow(["Node", "Out-degree", "In-degree", "Total degree"])
                
                # Write degrees - each value in separate cell
                for node_id, degree_info in degrees.items():
                    writer.writerow([
                        node_id,
                        degree_info['out_degree'],
                        degree_info['in_degree'],
                        degree_info['degree']
                    ])
                
                print(f"Node degrees exported to: {filepath}")
                return filepath
                
        except Exception as e:
            print(f"Error exporting node degrees: {e}")
            return None
    
    def export_all_matrices(self, prefix="graph"):
        """
        Export all matrices to CSV files.
        
        Args:
            prefix (str): Prefix for filenames
            
        Returns:
            list: List of exported file paths
        """
        exported_files = []
        
        # Export adjacency matrix
        file_path = self.export_adjacency_matrix(f"{prefix}_adjacency_matrix.csv")
        if file_path:
            exported_files.append(file_path)
        
        # Export sign matrix
        file_path = self.export_sign_matrix(f"{prefix}_sign_matrix.csv")
        if file_path:
            exported_files.append(file_path)
        
        # Export incidence matrix
        file_path = self.export_incidence_matrix(f"{prefix}_incidence_matrix.csv")
        if file_path:
            exported_files.append(file_path)
        
        # Export distance matrix
        file_path = self.export_distance_matrix(f"{prefix}_distance_matrix.csv")
        if file_path:
            exported_files.append(file_path)
        
        # Export predecessor matrix
        file_path = self.export_predecessor_matrix(f"{prefix}_predecessor_matrix.csv")
        if file_path:
            exported_files.append(file_path)
        
        # Export adjacency list
        file_path = self.export_adjacency_list(f"{prefix}_adjacency_list.csv")
        if file_path:
            exported_files.append(file_path)
        
        return exported_files
    
    def export_adjacency_matrix_power(self, power, filename=None):
        """
        Export adjacency matrix raised to a specific power to CSV.
        
        Args:
            power (int): Power to raise the adjacency matrix to
            filename (str): Name of the CSV file (optional)
            
        Returns:
            str: Path to the exported file
        """
        from .matrices import GraphMatrixGenerator
        
        generator = GraphMatrixGenerator(self.graph)
        matrix = generator.adjacency_matrix_power(power)
        node_labels = [node.identifier for node in self.graph.nodes()]
        
        if filename is None:
            filename = f"adjacency_matrix_power_{power}.csv"
        
        return self.export_matrix_to_csv(matrix, filename, f"Adjacency Matrix^{power}", node_labels, node_labels)
    
    def export_specific_matrix(self, matrix_type, filename=None, power=None):
        """
        Export a specific matrix type to CSV.
        
        Args:
            matrix_type (str): Type of matrix ('adjacency', 'sign', 'incidence', 'distance', 'predecessor', 'adjacency_power')
            filename (str): Name of the CSV file (optional)
            power (int): Power for adjacency matrix (only used if matrix_type is 'adjacency_power')
            
        Returns:
            str: Path to the exported file
        """
        from .matrices import GraphMatrixGenerator
        
        generator = GraphMatrixGenerator(self.graph)
        node_labels = [node.identifier for node in self.graph.nodes()]
        
        if matrix_type == 'adjacency':
            matrix = generator.adjacency_matrix()
            matrix_title = "Adjacency Matrix"
            if filename is None:
                filename = "adjacency_matrix.csv"
        elif matrix_type == 'sign':
            matrix = generator.sign_matrix()
            matrix_title = "Sign Matrix"
            if filename is None:
                filename = "sign_matrix.csv"
        elif matrix_type == 'incidence':
            matrix, node_labels, edge_labels = generator.incidence_matrix()
            matrix_title = "Incidence Matrix"
            if filename is None:
                filename = "incidence_matrix.csv"
            # Special handling for incidence matrix
            return self.export_matrix_to_csv(matrix, filename, matrix_title, node_labels, edge_labels)
        elif matrix_type == 'distance':
            matrix = generator.distance_matrix()
            matrix_title = "Distance Matrix"
            if filename is None:
                filename = "distance_matrix.csv"
        elif matrix_type == 'predecessor':
            matrix = generator.predecessor_matrix()
            matrix_title = "Predecessor Matrix"
            if filename is None:
                filename = "predecessor_matrix.csv"
            # Convert predecessor indices to node identifiers
            converted_matrix = []
            for row in matrix:
                converted_row = []
                for pred_index in row:
                    if pred_index is not None:
                        converted_row.append(node_labels[pred_index])
                    else:
                        converted_row.append("")
                converted_matrix.append(converted_row)
            matrix = converted_matrix
        elif matrix_type == 'adjacency_power':
            if power is None:
                raise ValueError("Power must be specified for adjacency_power matrix type")
            matrix = generator.adjacency_matrix_power(power)
            matrix_title = f"Adjacency Matrix^{power}"
            if filename is None:
                filename = f"adjacency_matrix_power_{power}.csv"
        else:
            raise ValueError(f"Unknown matrix type: {matrix_type}")
        
        return self.export_matrix_to_csv(matrix, filename, matrix_title, node_labels, node_labels)
    
    def export_all_data(self, prefix="graph"):
        """
        Export all graph data to CSV files.
        
        Args:
            prefix (str): Prefix for filenames
            
        Returns:
            list: List of exported file paths
        """
        exported_files = []
        
        # Export all matrices
        matrix_files = self.export_all_matrices(prefix)
        exported_files.extend(matrix_files)
        
        # Export graph properties
        file_path = self.export_graph_properties(f"{prefix}_properties.csv")
        if file_path:
            exported_files.append(file_path)
        
        # Export node degrees
        file_path = self.export_node_degrees(f"{prefix}_degrees.csv")
        if file_path:
            exported_files.append(file_path)
        
        return exported_files


class GraphImporter:
    """Importer for graph data from CSV format."""
    
    def __init__(self):
        """Initialize the importer."""
        pass
    
    def import_matrix_from_csv(self, filepath, matrix_type="matrix", has_labels=True):
        """
        Import a matrix from CSV file.
        
        Args:
            filepath (str): Path to the CSV file
            matrix_type (str): Type of matrix for validation
            has_labels (bool): Whether the CSV has row/column labels
            
        Returns:
            tuple: (matrix, row_labels, col_labels) or (matrix, None, None) if no labels
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                
                if not rows:
                    raise ValueError("CSV file is empty")
                
                if has_labels:
                    # First row contains column labels
                    col_labels = rows[0][1:] if len(rows[0]) > 1 else []
                    # First column of each row contains row labels
                    row_labels = [row[0] for row in rows[1:]]
                    # Extract matrix data (skip first row and first column)
                    matrix_data = [row[1:] for row in rows[1:]]
                else:
                    # No labels, just matrix data
                    matrix_data = rows
                    row_labels = None
                    col_labels = None
                
                # Convert string values to appropriate types
                matrix = []
                for row in matrix_data:
                    matrix_row = []
                    for value in row:
                        if value == "" or value is None:
                            matrix_row.append(None)
                        elif value.lower() == "inf":
                            matrix_row.append(math.inf)
                        elif value.lower() == "-inf":
                            matrix_row.append(-math.inf)
                        else:
                            try:
                                # Try to convert to float first
                                float_val = float(value)
                                # If it's a whole number, convert to int
                                if float_val.is_integer():
                                    matrix_row.append(int(float_val))
                                else:
                                    matrix_row.append(float_val)
                            except ValueError:
                                # If conversion fails, keep as string
                                matrix_row.append(value)
                    matrix.append(matrix_row)
                
                print(f"Matrix imported from: {filepath}")
                print(f"Matrix size: {len(matrix)}x{len(matrix[0]) if matrix else 0}")
                if row_labels:
                    print(f"Row labels: {row_labels}")
                if col_labels:
                    print(f"Column labels: {col_labels}")
                
                return matrix, row_labels, col_labels
                
        except Exception as e:
            print(f"Error importing matrix from CSV: {e}")
            raise
    
    def import_adjacency_matrix_from_csv(self, filepath, has_labels=True):
        """
        Import adjacency matrix from CSV file.
        
        Args:
            filepath (str): Path to the CSV file
            has_labels (bool): Whether the CSV has row/column labels
            
        Returns:
            tuple: (matrix, node_labels)
        """
        matrix, row_labels, col_labels = self.import_matrix_from_csv(filepath, "adjacency", has_labels)
        
        # Validate that it's a square matrix
        if len(matrix) != len(matrix[0]):
            raise ValueError("Adjacency matrix must be square")
        
        # Validate labels consistency
        if has_labels and row_labels != col_labels:
            print("Warning: Row and column labels don't match, using row labels")
        
        node_labels = row_labels if row_labels else col_labels
        return matrix, node_labels
    
    def import_distance_matrix_from_csv(self, filepath, has_labels=True):
        """
        Import distance matrix from CSV file.
        
        Args:
            filepath (str): Path to the CSV file
            has_labels (bool): Whether the CSV has row/column labels
            
        Returns:
            tuple: (matrix, node_labels)
        """
        matrix, row_labels, col_labels = self.import_matrix_from_csv(filepath, "distance", has_labels)
        
        # Validate that it's a square matrix
        if len(matrix) != len(matrix[0]):
            raise ValueError("Distance matrix must be square")
        
        # Validate diagonal elements are 0
        for i in range(len(matrix)):
            if matrix[i][i] != 0:
                print(f"Warning: Diagonal element [{i}][{i}] is not 0: {matrix[i][i]}")
        
        node_labels = row_labels if row_labels else col_labels
        return matrix, node_labels
    
    def import_incidence_matrix_from_csv(self, filepath, has_labels=True):
        """
        Import incidence matrix from CSV file.
        
        Args:
            filepath (str): Path to the CSV file
            has_labels (bool): Whether the CSV has row/column labels
            
        Returns:
            tuple: (matrix, node_labels, edge_labels)
        """
        matrix, row_labels, col_labels = self.import_matrix_from_csv(filepath, "incidence", has_labels)
        
        node_labels = row_labels
        edge_labels = col_labels
        
        return matrix, node_labels, edge_labels
    
    def import_sign_matrix_from_csv(self, filepath, has_labels=True):
        """
        Import sign matrix from CSV file.
        
        Args:
            filepath (str): Path to the CSV file
            has_labels (bool): Whether the CSV has row/column labels
            
        Returns:
            tuple: (matrix, node_labels)
        """
        matrix, row_labels, col_labels = self.import_matrix_from_csv(filepath, "sign", has_labels)
        
        # Validate that it's a square matrix
        if len(matrix) != len(matrix[0]):
            raise ValueError("Sign matrix must be square")
        
        # Validate values are -1, 0, or 1
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                if value not in [-1, 0, 1]:
                    print(f"Warning: Sign matrix element [{i}][{j}] is not -1, 0, or 1: {value}")
        
        node_labels = row_labels if row_labels else col_labels
        return matrix, node_labels
    
    def import_predecessor_matrix_from_csv(self, filepath, has_labels=True):
        """
        Import predecessor matrix from CSV file.
        
        Args:
            filepath (str): Path to the CSV file
            has_labels (bool): Whether the CSV has row/column labels
            
        Returns:
            tuple: (matrix, node_labels)
        """
        matrix, row_labels, col_labels = self.import_matrix_from_csv(filepath, "predecessor", has_labels)
        
        # Validate that it's a square matrix
        if len(matrix) != len(matrix[0]):
            raise ValueError("Predecessor matrix must be square")
        
        node_labels = row_labels if row_labels else col_labels
        return matrix, node_labels
    
    def import_adjacency_list_from_csv(self, filepath):
        """
        Import adjacency list from CSV file.
        
        Args:
            filepath (str): Path to the CSV file
            
        Returns:
            dict: Adjacency list dictionary
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                
                if not rows:
                    raise ValueError("CSV file is empty")
                
                # First row should be header
                header = rows[0]
                if header[0].lower() != "node":
                    print("Warning: Expected 'Node' as first column header")
                
                adj_list = {}
                for row in rows[1:]:
                    if not row:
                        continue
                    
                    node_id = row[0]
                    neighbors = []
                    
                    # Process neighbor columns
                    for i in range(1, len(row)):
                        if row[i] and row[i].strip():
                            neighbors.append(row[i].strip())
                    
                    adj_list[node_id] = neighbors
                
                print(f"Adjacency list imported from: {filepath}")
                print(f"Number of nodes: {len(adj_list)}")
                
                return adj_list
                
        except Exception as e:
            print(f"Error importing adjacency list from CSV: {e}")
            raise
    
    def validate_matrix_format(self, matrix, matrix_type):
        """
        Validate matrix format based on type.
        
        Args:
            matrix (list): Matrix to validate
            matrix_type (str): Type of matrix
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not matrix:
            return False
        
        # Check if all rows have the same length
        row_lengths = [len(row) for row in matrix]
        if len(set(row_lengths)) > 1:
            print(f"Error: Matrix rows have different lengths: {row_lengths}")
            return False
        
        # Type-specific validations
        if matrix_type in ['adjacency', 'distance', 'sign', 'predecessor']:
            # Should be square
            if len(matrix) != len(matrix[0]):
                print(f"Error: {matrix_type} matrix must be square")
                return False
        
        return True


def import_matrix_from_csv(filepath, matrix_type="matrix", has_labels=True):
    """
    Convenience function to import a matrix from CSV.
    
    Args:
        filepath (str): Path to the CSV file
        matrix_type (str): Type of matrix
        has_labels (bool): Whether the CSV has row/column labels
        
    Returns:
        tuple: (matrix, row_labels, col_labels)
    """
    importer = GraphImporter()
    return importer.import_matrix_from_csv(filepath, matrix_type, has_labels)


def import_adjacency_matrix_from_csv(filepath, has_labels=True):
    """
    Convenience function to import adjacency matrix from CSV.
    
    Args:
        filepath (str): Path to the CSV file
        has_labels (bool): Whether the CSV has row/column labels
        
    Returns:
        tuple: (matrix, node_labels)
    """
    importer = GraphImporter()
    return importer.import_adjacency_matrix_from_csv(filepath, has_labels)


def import_distance_matrix_from_csv(filepath, has_labels=True):
    """
    Convenience function to import distance matrix from CSV.
    
    Args:
        filepath (str): Path to the CSV file
        has_labels (bool): Whether the CSV has row/column labels
        
    Returns:
        tuple: (matrix, node_labels)
    """
    importer = GraphImporter()
    return importer.import_distance_matrix_from_csv(filepath, has_labels)


def import_incidence_matrix_from_csv(filepath, has_labels=True):
    """
    Convenience function to import incidence matrix from CSV.
    
    Args:
        filepath (str): Path to the CSV file
        has_labels (bool): Whether the CSV has row/column labels
        
    Returns:
        tuple: (matrix, node_labels, edge_labels)
    """
    importer = GraphImporter()
    return importer.import_incidence_matrix_from_csv(filepath, has_labels)


def import_sign_matrix_from_csv(filepath, has_labels=True):
    """
    Convenience function to import sign matrix from CSV.
    
    Args:
        filepath (str): Path to the CSV file
        has_labels (bool): Whether the CSV has row/column labels
        
    Returns:
        tuple: (matrix, node_labels)
    """
    importer = GraphImporter()
    return importer.import_sign_matrix_from_csv(filepath, has_labels)


def import_predecessor_matrix_from_csv(filepath, has_labels=True):
    """
    Convenience function to import predecessor matrix from CSV.
    
    Args:
        filepath (str): Path to the CSV file
        has_labels (bool): Whether the CSV has row/column labels
        
    Returns:
        tuple: (matrix, node_labels)
    """
    importer = GraphImporter()
    return importer.import_predecessor_matrix_from_csv(filepath, has_labels)


def import_adjacency_list_from_csv(filepath):
    """
    Convenience function to import adjacency list from CSV.
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        dict: Adjacency list dictionary
    """
    importer = GraphImporter()
    return importer.import_adjacency_list_from_csv(filepath)


def export_matrix_to_csv(graph, matrix, filename="matrix.csv", matrix_type="matrix", row_labels=None, col_labels=None):
    """
    Convenience function to export a matrix to CSV.
    
    Args:
        graph (Graph): The graph
        matrix (list): Matrix to export
        filename (str): Name of the CSV file
        matrix_type (str): Type of matrix
        row_labels (list): Optional labels for rows
        col_labels (list): Optional labels for columns
        
    Returns:
        str: Path to the exported file
    """
    exporter = GraphExporter(graph)
    return exporter.export_matrix_to_csv(matrix, filename, matrix_type, row_labels, col_labels)


def export_all_data_to_csv(graph, prefix="graph"):
    """
    Convenience function to export all graph data to CSV.
    
    Args:
        graph (Graph): The graph to export
        prefix (str): Prefix for filenames
        
    Returns:
        list: List of exported file paths
    """
    exporter = GraphExporter(graph)
    return exporter.export_all_data(prefix)


def export_specific_matrix_to_csv(graph, matrix_type, filename=None, power=None):
    """
    Convenience function to export a specific matrix to CSV.
    
    Args:
        graph (Graph): The graph to export
        matrix_type (str): Type of matrix ('adjacency', 'sign', 'incidence', 'distance', 'predecessor', 'adjacency_power')
        filename (str): Name of the CSV file (optional)
        power (int): Power for adjacency matrix (only used if matrix_type is 'adjacency_power')
        
    Returns:
        str: Path to the exported file
    """
    exporter = GraphExporter(graph)
    return exporter.export_specific_matrix(matrix_type, filename, power)


def export_adjacency_power_to_csv(graph, power, filename=None):
    """
    Convenience function to export adjacency matrix power to CSV.
    
    Args:
        graph (Graph): The graph to export
        power (int): Power to raise the adjacency matrix to
        filename (str): Name of the CSV file (optional)
        
    Returns:
        str: Path to the exported file
    """
    exporter = GraphExporter(graph)
    return exporter.export_adjacency_matrix_power(power, filename)


# Example usage and testing
if __name__ == "__main__":
    from .parser import parse_graph
    from .graph import create_graph_from_data
    
    # Test with a sample graph file
    try:
        # Parse a graph file
        data = parse_graph("../grafy/01.tg")
        graph = create_graph_from_data(data)
        
        # Create exporter
        exporter = GraphExporter(graph)
        
        # Export all data
        exported_files = exporter.export_all_data("test_graph")
        print(f"Exported {len(exported_files)} files:")
        for file_path in exported_files:
            print(f"  - {file_path}")
        
    except Exception as e:
        print(f"Error: {e}")
