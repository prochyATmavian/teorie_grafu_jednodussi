#!/usr/bin/env python3
"""
Main entry point for the Graph Recognition System.
Provides CLI interface and example usage for graph analysis.
"""

import sys
import os
import argparse
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.parser import parse_graph
from src.graph import create_graph_from_data
from src.properties import GraphPropertyDetector, print_graph_properties
from src.neighborhoods import NeighborhoodCalculator, print_node_degrees
from src.matrices import GraphMatrixGenerator, print_all_matrices
from src.exporter import GraphExporter, export_all_data_to_csv, export_specific_matrix_to_csv, export_adjacency_power_to_csv


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Graph Recognition System - Analyze graph properties and generate matrices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 run.py analyze grafy/01.tg                    # Analyze graph properties
  python3 run.py matrices grafy/01.tg                   # Generate all matrices
  python3 run.py neighborhoods grafy/01.tg A            # Get neighborhoods for node A
  python3 run.py export grafy/01.tg --prefix my_graph   # Export all data to CSV
  python3 run.py export-matrix grafy/01.tg --type adjacency  # Export specific matrix
  python3 run.py export-power grafy/01.tg --power 3     # Export adjacency matrix^3
  python3 run.py interactive                            # Interactive mode
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze graph properties')
    analyze_parser.add_argument('file', help='Path to .tg graph file')
    
    # Matrices command
    matrices_parser = subparsers.add_parser('matrices', help='Generate graph matrices')
    matrices_parser.add_argument('file', help='Path to .tg graph file')
    matrices_parser.add_argument('--power', type=int, default=2, help='Power for adjacency matrix (default: 2)')
    
    # Neighborhoods command
    neighborhoods_parser = subparsers.add_parser('neighborhoods', help='Get node neighborhoods')
    neighborhoods_parser.add_argument('file', help='Path to .tg graph file')
    neighborhoods_parser.add_argument('node', help='Node identifier')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export graph data to CSV')
    export_parser.add_argument('file', help='Path to .tg graph file')
    export_parser.add_argument('--prefix', default='graph', help='Prefix for output files (default: graph)')
    
    # Export specific matrix command
    export_matrix_parser = subparsers.add_parser('export-matrix', help='Export specific matrix to CSV')
    export_matrix_parser.add_argument('file', help='Path to .tg graph file')
    export_matrix_parser.add_argument('--type', required=True, 
                                     choices=['adjacency', 'sign', 'incidence', 'distance', 'predecessor'],
                                     help='Type of matrix to export')
    export_matrix_parser.add_argument('--filename', help='Output filename (optional)')
    
    # Export adjacency power command
    export_power_parser = subparsers.add_parser('export-power', help='Export adjacency matrix power to CSV')
    export_power_parser.add_argument('file', help='Path to .tg graph file')
    export_power_parser.add_argument('--power', type=int, required=True, help='Power to raise adjacency matrix to')
    export_power_parser.add_argument('--filename', help='Output filename (optional)')
    
    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Interactive mode')
    interactive_parser.add_argument('--file', help='Initial graph file to load')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demo with sample graphs')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        analyze_graph(args.file)
    elif args.command == 'matrices':
        generate_matrices(args.file, args.power)
    elif args.command == 'neighborhoods':
        show_neighborhoods(args.file, args.node)
    elif args.command == 'export':
        export_graph_data(args.file, args.prefix)
    elif args.command == 'export-matrix':
        export_specific_matrix_cli(args.file, args.type, args.filename)
    elif args.command == 'export-power':
        export_adjacency_power_cli(args.file, args.power, args.filename)
    elif args.command == 'interactive':
        interactive_mode(args.file)
    elif args.command == 'demo':
        run_demo()
    else:
        parser.print_help()


def analyze_graph(file_path):
    """Analyze graph properties."""
    try:
        print(f"Analyzing graph: {file_path}")
        print("=" * 50)
        
        # Parse and create graph
        data = parse_graph(file_path)
        graph = create_graph_from_data(data)
        
        print(f"Graph loaded: {graph.node_count()} nodes, {graph.edge_count()} edges")
        print()
        
        # Analyze properties
        print_graph_properties(graph)
        
        # Print basic statistics
        print(f"\nBasic Statistics:")
        print(f"  Nodes: {graph.node_count()}")
        print(f"  Edges: {graph.edge_count()}")
        print(f"  Directed: {'Yes' if graph.is_directed() else 'No'}")
        print(f"  Weighted: {'Yes' if graph.is_weighted() else 'No'}")
        
    except Exception as e:
        print(f"Error analyzing graph: {e}")


def generate_matrices(file_path, power=2):
    """Generate and display graph matrices."""
    try:
        print(f"Generating matrices for: {file_path}")
        print("=" * 50)
        
        # Parse and create graph
        data = parse_graph(file_path)
        graph = create_graph_from_data(data)
        
        print(f"Graph loaded: {graph.node_count()} nodes, {graph.edge_count()} edges")
        
        # Generate matrices
        generator = GraphMatrixGenerator(graph)
        
        # Print all matrices
        print_all_matrices(graph)
        
        # Show adjacency matrix power
        if power > 1:
            print(f"\nAdjacency Matrix to power {power}:")
            print("=" * 30)
            power_matrix = generator.adjacency_matrix_power(power)
            node_labels = [node.identifier for node in graph.nodes()]
            generator.print_matrix(power_matrix, f"Adjacency Matrix^{power}", node_labels)
        
    except Exception as e:
        print(f"Error generating matrices: {e}")


def show_neighborhoods(file_path, node_identifier):
    """Show neighborhoods for a specific node."""
    try:
        print(f"Neighborhoods for node '{node_identifier}' in: {file_path}")
        print("=" * 60)
        
        # Parse and create graph
        data = parse_graph(file_path)
        graph = create_graph_from_data(data)
        
        print(f"Graph loaded: {graph.node_count()} nodes, {graph.edge_count()} edges")
        
        # Show neighborhoods
        calculator = NeighborhoodCalculator(graph)
        calculator.print_neighborhoods(node_identifier)
        
    except Exception as e:
        print(f"Error showing neighborhoods: {e}")


def export_graph_data(file_path, prefix):
    """Export graph data to CSV files."""
    try:
        print(f"Exporting graph data from: {file_path}")
        print("=" * 50)
        
        # Parse and create graph
        data = parse_graph(file_path)
        graph = create_graph_from_data(data)
        
        print(f"Graph loaded: {graph.node_count()} nodes, {graph.edge_count()} edges")
        
        # Export all data
        exported_files = export_all_data_to_csv(graph, prefix)
        
        print(f"\nExported {len(exported_files)} files:")
        for file_path in exported_files:
            print(f"  - {file_path}")
        
    except Exception as e:
        print(f"Error exporting graph data: {e}")


def interactive_mode(initial_file=None):
    """Interactive mode for exploring graphs."""
    print("Graph Recognition System - Interactive Mode")
    print("=" * 50)
    print("Commands:")
    print("  load <file>     - Load a graph file")
    print("  analyze         - Analyze current graph")
    print("  matrices        - Show all matrices")
    print("  neighborhoods <node> - Show neighborhoods for node")
    print("  export [prefix] - Export all data to CSV")
    print("  export-matrix   - Export specific matrix to CSV")
    print("  export-power    - Export adjacency matrix power to CSV")
    print("  help            - Show this help")
    print("  quit            - Exit")
    print()
    
    graph = None
    
    if initial_file:
        try:
            data = parse_graph(initial_file)
            graph = create_graph_from_data(data)
            print(f"Loaded initial graph: {initial_file}")
            print(f"Graph: {graph.node_count()} nodes, {graph.edge_count()} edges")
        except Exception as e:
            print(f"Error loading initial file: {e}")
    
    while True:
        try:
            command = input("\n> ").strip().split()
            if not command:
                continue
            
            cmd = command[0].lower()
            
            if cmd == 'quit' or cmd == 'exit':
                break
            elif cmd == 'help':
                print("Commands: load, analyze, matrices, neighborhoods, export, export-matrix, export-power, help, quit")
            elif cmd == 'load':
                if len(command) < 2:
                    print("Usage: load <file>")
                    continue
                try:
                    data = parse_graph(command[1])
                    graph = create_graph_from_data(data)
                    print(f"Loaded graph: {command[1]}")
                    print(f"Graph: {graph.node_count()} nodes, {graph.edge_count()} edges")
                except Exception as e:
                    print(f"Error loading graph: {e}")
            elif cmd == 'analyze':
                if graph is None:
                    print("No graph loaded. Use 'load <file>' first.")
                    continue
                print_graph_properties(graph)
            elif cmd == 'matrices':
                if graph is None:
                    print("No graph loaded. Use 'load <file>' first.")
                    continue
                print_all_matrices(graph)
            elif cmd == 'neighborhoods':
                if graph is None:
                    print("No graph loaded. Use 'load <file>' first.")
                    continue
                if len(command) < 2:
                    print("Usage: neighborhoods <node>")
                    continue
                calculator = NeighborhoodCalculator(graph)
                calculator.print_neighborhoods(command[1])
            elif cmd == 'export':
                if graph is None:
                    print("No graph loaded. Use 'load <file>' first.")
                    continue
                prefix = command[1] if len(command) > 1 else 'graph'
                exported_files = export_all_data_to_csv(graph, prefix)
                print(f"Exported {len(exported_files)} files")
            elif cmd == 'export-matrix':
                if graph is None:
                    print("No graph loaded. Use 'load <file>' first.")
                    continue
                export_specific_matrix_interactive(graph)
            elif cmd == 'export-power':
                if graph is None:
                    print("No graph loaded. Use 'load <file>' first.")
                    continue
                export_adjacency_power_interactive(graph)
            else:
                print(f"Unknown command: {cmd}. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


def export_specific_matrix_cli(file_path, matrix_type, filename):
    """Export specific matrix via CLI."""
    try:
        print(f"Exporting {matrix_type} matrix from: {file_path}")
        print("=" * 50)
        
        # Parse and create graph
        data = parse_graph(file_path)
        graph = create_graph_from_data(data)
        
        print(f"Graph loaded: {graph.node_count()} nodes, {graph.edge_count()} edges")
        
        # Export specific matrix
        file_path = export_specific_matrix_to_csv(graph, matrix_type, filename)
        
        if file_path:
            print(f"\nMatrix exported successfully to: {file_path}")
        else:
            print("Export failed!")
        
    except Exception as e:
        print(f"Error exporting matrix: {e}")


def export_adjacency_power_cli(file_path, power, filename):
    """Export adjacency matrix power via CLI."""
    try:
        print(f"Exporting adjacency matrix^{power} from: {file_path}")
        print("=" * 50)
        
        # Parse and create graph
        data = parse_graph(file_path)
        graph = create_graph_from_data(data)
        
        print(f"Graph loaded: {graph.node_count()} nodes, {graph.edge_count()} edges")
        
        # Export adjacency matrix power
        file_path = export_adjacency_power_to_csv(graph, power, filename)
        
        if file_path:
            print(f"\nAdjacency matrix^{power} exported successfully to: {file_path}")
        else:
            print("Export failed!")
        
    except Exception as e:
        print(f"Error exporting matrix power: {e}")


def export_specific_matrix_interactive(graph):
    """Interactive export of specific matrix."""
    print("\n=== Export Specific Matrix ===")
    print("Available matrix types:")
    print("1. adjacency - Adjacency Matrix")
    print("2. sign - Sign Matrix")
    print("3. incidence - Incidence Matrix")
    print("4. distance - Distance Matrix")
    print("5. predecessor - Predecessor Matrix")
    
    choice = input("\nSelect matrix type (1-5): ").strip()
    
    matrix_types = {
        '1': 'adjacency',
        '2': 'sign',
        '3': 'incidence',
        '4': 'distance',
        '5': 'predecessor'
    }
    
    if choice not in matrix_types:
        print("Invalid choice!")
        return
    
    matrix_type = matrix_types[choice]
    filename = input(f"Enter filename (or press Enter for default): ").strip()
    
    if not filename:
        filename = None
    
    try:
        file_path = export_specific_matrix_to_csv(graph, matrix_type, filename)
        if file_path:
            print(f"Matrix exported successfully to: {file_path}")
        else:
            print("Export failed!")
    except Exception as e:
        print(f"Error exporting matrix: {e}")


def export_adjacency_power_interactive(graph):
    """Interactive export of adjacency matrix power."""
    print("\n=== Export Adjacency Matrix Power ===")
    
    try:
        power = int(input("Enter power (positive integer): ").strip())
        if power < 1:
            print("Power must be a positive integer!")
            return
    except ValueError:
        print("Invalid power! Must be a positive integer.")
        return
    
    filename = input(f"Enter filename (or press Enter for default): ").strip()
    
    if not filename:
        filename = None
    
    try:
        file_path = export_adjacency_power_to_csv(graph, power, filename)
        if file_path:
            print(f"Adjacency matrix^{power} exported successfully to: {file_path}")
        else:
            print("Export failed!")
    except Exception as e:
        print(f"Error exporting matrix power: {e}")


def run_demo():
    """Run demo with sample graphs."""
    print("Graph Recognition System - Demo")
    print("=" * 50)
    
    # List available graph files
    graph_dir = Path("grafy")
    if not graph_dir.exists():
        print("No 'grafy' directory found with sample graphs.")
        return
    
    graph_files = list(graph_dir.glob("*.tg"))
    if not graph_files:
        print("No .tg files found in 'grafy' directory.")
        return
    
    print(f"Found {len(graph_files)} graph files:")
    for i, file_path in enumerate(graph_files[:10]):  # Show first 10
        print(f"  {i+1}. {file_path.name}")
    
    if len(graph_files) > 10:
        print(f"  ... and {len(graph_files) - 10} more files")
    
    print()
    
    # Demo with first graph file
    demo_file = graph_files[0]
    print(f"Demo with: {demo_file}")
    print("-" * 30)
    
    try:
        # Parse and analyze
        data = parse_graph(str(demo_file))
        graph = create_graph_from_data(data)
        
        print(f"Graph: {graph.node_count()} nodes, {graph.edge_count()} edges")
        print()
        
        # Show properties
        print("Graph Properties:")
        detector = GraphPropertyDetector(graph)
        properties = detector.detect_all_properties()
        
        for prop, value in list(properties.items())[:5]:  # Show first 5 properties
            print(f"  {prop}: {'YES' if value else 'NO'}")
        
        print("  ... (run 'python run.py analyze grafy/01.tg' to see all properties)")
        print()
        
        # Show degrees
        print("Node Degrees (first 5 nodes):")
        calculator = NeighborhoodCalculator(graph)
        degrees = calculator.get_all_degrees()
        
        count = 0
        for node_id, degree_info in degrees.items():
            if count >= 5:
                break
            print(f"  {node_id}: out={degree_info['out_degree']}, in={degree_info['in_degree']}, total={degree_info['degree']}")
            count += 1
        
        print("  ... (run 'python run.py matrices grafy/01.tg' to see all matrices)")
        print()
        
        print("Demo completed! Try these commands:")
        print(f"  python run.py analyze {demo_file}")
        print(f"  python run.py matrices {demo_file}")
        print(f"  python run.py export {demo_file} --prefix demo")
        print("  python run.py interactive")
        
    except Exception as e:
        print(f"Error in demo: {e}")


def example_usage():
    """Show example usage of the library."""
    print("Example Usage:")
    print("=" * 20)
    
    example_code = '''
# Example: Parse and analyze a graph
from src.parser import parse_graph
from src.graph import create_graph_from_data
from src.properties import GraphPropertyDetector

# Parse graph file
data = parse_graph('grafy/01.tg')
graph = create_graph_from_data(data)

# Analyze properties
detector = GraphPropertyDetector(graph)
properties = detector.detect_all_properties()
print(properties)

# Iterate over nodes
for node in graph.nodes():
    print(f"Node: {node.identifier}")

# Iterate over edges
for edge in graph.edges():
    print(f"Edge: {edge.source.identifier} -> {edge.target.identifier}")
'''
    
    print(example_code)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments provided, show help
        print("Graph Recognition System")
        print("=" * 30)
        print("Use --help to see available commands")
        print()
        print("Quick start:")
        print("  python run.py demo                    # Run demo")
        print("  python run.py analyze grafy/01.tg     # Analyze a graph")
        print("  python run.py interactive             # Interactive mode")
        print()
        example_usage()
    else:
        main()
