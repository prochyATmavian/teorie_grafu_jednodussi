#!/usr/bin/env python3
"""
Test script for CSV import/export functionality.
Demonstrates how to export matrices to CSV and import them back.
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.parser import parse_graph
from src.graph import create_graph_from_data
from src.exporter import (
    export_adjacency_matrix_from_csv,
    export_distance_matrix_from_csv,
    import_adjacency_matrix_from_csv,
    import_distance_matrix_from_csv,
    GraphExporter,
    GraphImporter
)


def test_csv_export_import():
    """Test CSV export and import functionality."""
    print("=== Test CSV Export/Import Functionality ===\n")
    
    try:
        # Parse a sample graph
        print("1. Loading graph from file...")
        data = parse_graph("grafy/01.tg")
        graph = create_graph_from_data(data)
        print(f"   Graph loaded: {len(graph.nodes())} nodes, {len(graph.edges())} edges")
        
        # Export matrices to CSV
        print("\n2. Exporting matrices to CSV...")
        exporter = GraphExporter(graph)
        
        # Export adjacency matrix
        adj_file = exporter.export_adjacency_matrix("test_adjacency.csv")
        print(f"   Adjacency matrix exported to: {adj_file}")
        
        # Export distance matrix
        dist_file = exporter.export_distance_matrix("test_distance.csv")
        print(f"   Distance matrix exported to: {dist_file}")
        
        # Import matrices back from CSV
        print("\n3. Importing matrices from CSV...")
        importer = GraphImporter()
        
        # Import adjacency matrix
        adj_matrix, adj_labels = importer.import_adjacency_matrix_from_csv(adj_file)
        print(f"   Adjacency matrix imported: {len(adj_matrix)}x{len(adj_matrix[0])}")
        print(f"   Node labels: {adj_labels}")
        
        # Import distance matrix
        dist_matrix, dist_labels = importer.import_distance_matrix_from_csv(dist_file)
        print(f"   Distance matrix imported: {len(dist_matrix)}x{len(dist_matrix[0])}")
        print(f"   Node labels: {dist_labels}")
        
        # Validate matrices
        print("\n4. Validating imported matrices...")
        adj_valid = importer.validate_matrix_format(adj_matrix, 'adjacency')
        dist_valid = importer.validate_matrix_format(dist_matrix, 'distance')
        
        print(f"   Adjacency matrix valid: {adj_valid}")
        print(f"   Distance matrix valid: {dist_valid}")
        
        # Display sample data
        print("\n5. Sample matrix data:")
        print("   Adjacency matrix (first 3x3):")
        for i in range(min(3, len(adj_matrix))):
            row = adj_matrix[i][:3]
            print(f"     {row}")
        
        print("   Distance matrix (first 3x3):")
        for i in range(min(3, len(dist_matrix))):
            row = dist_matrix[i][:3]
            print(f"     {row}")
        
        print("\n=== Test completed successfully! ===")
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()


def test_matrix_operations():
    """Test matrix operations with imported data."""
    print("\n=== Test Matrix Operations with Imported Data ===\n")
    
    try:
        # Create a simple test matrix
        test_matrix = [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ]
        
        # Export test matrix
        print("1. Creating and exporting test matrix...")
        with open("csv_files/test_matrix.csv", "w") as f:
            f.write(",A,B,C\n")
            f.write("A,0,1,0\n")
            f.write("B,1,0,1\n")
            f.write("C,0,1,0\n")
        print("   Test matrix exported to: csv_files/test_matrix.csv")
        
        # Import test matrix
        print("\n2. Importing test matrix...")
        importer = GraphImporter()
        matrix, row_labels, col_labels = importer.import_matrix_from_csv(
            "csv_files/test_matrix.csv", "adjacency", has_labels=True
        )
        
        print(f"   Matrix size: {len(matrix)}x{len(matrix[0])}")
        print(f"   Row labels: {row_labels}")
        print(f"   Column labels: {col_labels}")
        
        # Display matrix
        print("\n3. Imported matrix:")
        for i, row in enumerate(matrix):
            print(f"   {row_labels[i]}: {row}")
        
        # Validate
        print("\n4. Validation:")
        is_valid = importer.validate_matrix_format(matrix, 'adjacency')
        print(f"   Matrix is valid: {is_valid}")
        
        print("\n=== Matrix operations test completed! ===")
        
    except Exception as e:
        print(f"Error during matrix operations test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Ensure csv_files directory exists
    os.makedirs("csv_files", exist_ok=True)
    
    # Run tests
    test_csv_export_import()
    test_matrix_operations()
