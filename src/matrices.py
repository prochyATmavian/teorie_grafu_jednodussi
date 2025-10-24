"""
Matrices module for graph recognition system.
Implements various matrix representations of graphs.
"""

import math
from .graph import Graph


class GraphMatrixGenerator:
    """Generator for various graph matrix representations."""
    
    def __init__(self, graph):
        """
        Initialize the matrix generator.
        
        Args:
            graph (Graph): The graph to generate matrices for
        """
        self.graph = graph
        self._node_list = list(graph.nodes())
        self.node_to_index = {node.identifier: i for i, node in enumerate(self._node_list)}
        self._edge_list = list(graph.edges())
    
    def adjacency_matrix(self):
        """
        a) Generate adjacency matrix.
        Entry (i,j) = edge weight or count of edges between nodes i and j.
        
        Returns:
            list: 2D list representing the adjacency matrix
        """
        n = len(self._node_list)
        matrix = [[0] * n for _ in range(n)]
        
        for edge in self._edge_list:
            i = self.node_to_index[edge.source.identifier]
            j = self.node_to_index[edge.target.identifier]
            
            # Use weight if available, otherwise 1
            value = edge.weight if edge.weight is not None else 1
            
            if edge.edge_type == 'directed':
                matrix[i][j] += value
            else:
                # Undirected edge - symmetric
                matrix[i][j] += value
                matrix[j][i] += value
        
        return matrix
    
    def sign_matrix(self):
        """
        b) Generate sign matrix based on adjacency matrix.
        Entry (i,j) = sign of adjacency matrix entry.
        
        Returns:
            list: 2D list representing the sign matrix
        """
        adj_matrix = self.adjacency_matrix()
        n = len(adj_matrix)
        sign_matrix = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if adj_matrix[i][j] > 0:
                    sign_matrix[i][j] = 1
                elif adj_matrix[i][j] < 0:
                    sign_matrix[i][j] = -1
                else:
                    sign_matrix[i][j] = 0
        
        return sign_matrix
    
    def adjacency_matrix_power(self, power):
        """
        c) Generate power of adjacency matrix.
        Used for counting paths of specific length.
        
        Args:
            power (int): Power to raise the adjacency matrix to
            
        Returns:
            list: 2D list representing the powered matrix
        """
        adj_matrix = self.adjacency_matrix()
        n = len(adj_matrix)
        
        if power == 0:
            # Identity matrix
            return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        elif power == 1:
            return adj_matrix
        else:
            result = adj_matrix
            for _ in range(power - 1):
                result = self._matrix_multiply(result, adj_matrix)
            return result
    
    def incidence_matrix(self):
        """
        d) Generate incidence matrix.
        Rows represent nodes, columns represent edges.
        
        Returns:
            tuple: (incidence_matrix, node_labels, edge_labels)
        """
        n = len(self._node_list)
        m = len(self._edge_list)
        matrix = [[0] * m for _ in range(n)]
        
        node_labels = [node.identifier for node in self._node_list]
        edge_labels = []
        
        for col, edge in enumerate(self._edge_list):
            i = self.node_to_index[edge.source.identifier]
            j = self.node_to_index[edge.target.identifier]
            
            if edge.edge_type == 'directed':
                matrix[i][col] = 1  # Outgoing
                matrix[j][col] = -1  # Incoming
            else:
                matrix[i][col] = 1  # Undirected
                matrix[j][col] = 1
            
            edge_label = edge.label if edge.label else f"{edge.source.identifier}-{edge.target.identifier}"
            edge_labels.append(edge_label)
        
        return matrix, node_labels, edge_labels
    
    def distance_matrix(self):
        """
        e) Generate distance matrix using Floyd-Warshall algorithm.
        Entry (i,j) = shortest path distance from node i to node j.
        
        Returns:
            list: 2D list representing the distance matrix
        """
        n = len(self._node_list)
        
        # Initialize distance matrix with infinity
        dist = [[math.inf] * n for _ in range(n)]
        
        # Distance from node to itself is 0
        for i in range(n):
            dist[i][i] = 0
        
        # Initialize with edge weights
        for edge in self._edge_list:
            i = self.node_to_index[edge.source.identifier]
            j = self.node_to_index[edge.target.identifier]
            
            weight = edge.weight if edge.weight is not None else 1
            
            if edge.edge_type == 'directed':
                dist[i][j] = weight
            else:
                # Undirected edge - symmetric
                dist[i][j] = weight
                dist[j][i] = weight
        
        # Floyd-Warshall algorithm
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        
        return dist
    
    def predecessor_matrix(self):
        """
        f) Generate predecessor matrix for shortest path reconstruction.
        
        Returns:
            list: 2D list representing the predecessor matrix
        """
        n = len(self._node_list)
        
        # Initialize predecessor matrix
        pred = [[None] * n for _ in range(n)]
        
        # Initialize distance matrix with infinity
        dist = [[math.inf] * n for _ in range(n)]
        
        # Distance from node to itself is 0
        for i in range(n):
            dist[i][i] = 0
            pred[i][i] = i
        
        # Initialize with edge weights and predecessors
        for edge in self._edge_list:
            i = self.node_to_index[edge.source.identifier]
            j = self.node_to_index[edge.target.identifier]
            
            weight = edge.weight if edge.weight is not None else 1
            
            if edge.edge_type == 'directed':
                dist[i][j] = weight
                pred[i][j] = i
            else:
                # Undirected edge - symmetric
                dist[i][j] = weight
                dist[j][i] = weight
                pred[i][j] = i
                pred[j][i] = j
        
        # Floyd-Warshall algorithm with predecessor tracking
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        pred[i][j] = pred[k][j]
        
        return pred
    
    def adjacency_list(self):
        """
        g) Generate adjacency list representation.
        
        Returns:
            dict: Dictionary mapping node identifiers to lists of neighbors
        """
        adj_list = {}
        
        for node in self._node_list:
            adj_list[node.identifier] = []
            
            # Get all incident edges
            incident_edges = self.graph.get_incident_edges(node.identifier)
            
            for edge in incident_edges:
                neighbor = edge.other_end(node)
                weight_info = f" (weight: {edge.weight})" if edge.weight is not None else ""
                direction_info = " ->" if edge.edge_type == 'directed' and edge.source == node else ""
                
                adj_list[node.identifier].append(f"{neighbor.identifier}{weight_info}{direction_info}")
        
        return adj_list
    
    def node_list(self):
        """
        h) Generate list of nodes.
        
        Returns:
            list: List of node information
        """
        nodes = []
        for node in self.graph.nodes():
            node_info = {
                'identifier': node.identifier,
                'weight': node.weight
            }
            nodes.append(node_info)
        return nodes
    
    def edge_list(self):
        """
        h) Generate list of edges.
        
        Returns:
            list: List of edge information
        """
        edges = []
        for edge in self.graph.edges():
            edge_info = {
                'source': edge.source.identifier,
                'target': edge.target.identifier,
                'weight': edge.weight,
                'label': edge.label,
                'type': edge.edge_type
            }
            edges.append(edge_info)
        return edges
    
    def _matrix_multiply(self, matrix_a, matrix_b):
        """
        Multiply two matrices.
        
        Args:
            matrix_a (list): First matrix
            matrix_b (list): Second matrix
            
        Returns:
            list: Result matrix
        """
        n = len(matrix_a)
        result = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += matrix_a[i][k] * matrix_b[k][j]
        
        return result
    
    def print_matrix(self, matrix, title, labels=None):
        """
        Print a matrix in a formatted way.
        
        Args:
            matrix (list): Matrix to print
            title (str): Title for the matrix
            labels (list): Optional labels for rows/columns
        """
        print(f"\n{title}:")
        print("=" * len(title))
        
        if labels:
            # Print column headers
            print("  ", end="")
            for label in labels:
                print(f"{label:>8}", end="")
            print()
            
            # Print rows with row labels
            for i, row in enumerate(matrix):
                print(f"{labels[i]:>2}", end="")
                for value in row:
                    if isinstance(value, float) and math.isinf(value):
                        print("     inf", end="")
                    else:
                        print(f"{value:>8}", end="")
                print()
        else:
            # Print without labels
            for row in matrix:
                for value in row:
                    if isinstance(value, float) and math.isinf(value):
                        print("     inf", end="")
                    else:
                        print(f"{value:>8}", end="")
                print()
    
    def generate_all_matrices(self):
        """
        Generate all matrix representations.
        
        Returns:
            dict: Dictionary containing all matrices
        """
        node_labels = [node.identifier for node in self._node_list]
        
        matrices = {
            'adjacency_matrix': self.adjacency_matrix(),
            'sign_matrix': self.sign_matrix(),
            'incidence_matrix': self.incidence_matrix(),
            'distance_matrix': self.distance_matrix(),
            'predecessor_matrix': self.predecessor_matrix(),
            'adjacency_list': self.adjacency_list(),
            'node_labels': node_labels
        }
        
        return matrices
    
    def print_all_matrices(self):
        """
        Print all matrix representations.
        """
        matrices = self.generate_all_matrices()
        node_labels = matrices['node_labels']
        
        # Print adjacency matrix
        self.print_matrix(matrices['adjacency_matrix'], "Adjacency Matrix", node_labels)
        
        # Print sign matrix
        self.print_matrix(matrices['sign_matrix'], "Sign Matrix", node_labels)
        
        # Print incidence matrix
        incidence_matrix, inc_node_labels, edge_labels = matrices['incidence_matrix']
        print(f"\nIncidence Matrix:")
        print("=" * 15)
        print("  ", end="")
        for edge_label in edge_labels:
            print(f"{edge_label:>8}", end="")
        print()
        for i, row in enumerate(incidence_matrix):
            print(f"{inc_node_labels[i]:>2}", end="")
            for value in row:
                print(f"{value:>8}", end="")
            print()
        
        # Print distance matrix
        self.print_matrix(matrices['distance_matrix'], "Distance Matrix", node_labels)
        
        # Print adjacency list
        print(f"\nAdjacency List:")
        print("=" * 14)
        for node_id, neighbors in matrices['adjacency_list'].items():
            print(f"{node_id}: {neighbors}")
        
        # Print node and edge lists
        print(f"\nNode List:")
        print("=" * 10)
        node_list = self.node_list()
        for node in node_list:
            print(f"Node: {node['identifier']}, Weight: {node['weight']}")
        
        print(f"\nEdge List:")
        print("=" * 10)
        edge_list = self.edge_list()
        for edge in edge_list:
            print(f"Edge: {edge['source']} -> {edge['target']}, Weight: {edge['weight']}, Type: {edge['type']}")


def generate_all_matrices(graph):
    """
    Convenience function to generate all matrices for a graph.
    
    Args:
        graph (Graph): The graph to generate matrices for
        
    Returns:
        dict: Dictionary containing all matrices
    """
    generator = GraphMatrixGenerator(graph)
    return generator.generate_all_matrices()


def print_all_matrices(graph):
    """
    Convenience function to print all matrices for a graph.
    
    Args:
        graph (Graph): The graph to generate matrices for
    """
    generator = GraphMatrixGenerator(graph)
    generator.print_all_matrices()


def print_individual_matrices(graph):
    """
    Vypíše každou matici zvlášť s možností výběru.
    
    Args:
        graph (Graph): Graf objekt
    """
    generator = GraphMatrixGenerator(graph)
    node_labels = [node.identifier for node in graph.nodes()]
    
    print("=== Dostupné matice ===")
    print("1. Matice sousednosti (Adjacency Matrix)")
    print("2. Znaménková matice (Sign Matrix)")
    print("3. Matice incidence (Incidence Matrix)")
    print("4. Matice vzdáleností (Distance Matrix)")
    print("5. Matice předchůdců (Predecessor Matrix)")
    print("6. Matice sousednosti na 2. mocninu")
    print("7. Matice sousednosti na 3. mocninu")
    print("8. Všechny matice")
    print()
    
    choice = input("Vyberte matici (1-8): ").strip()
    
    if choice == "1":
        matrix = generator.adjacency_matrix()
        generator.print_matrix(matrix, "Matice sousednosti", node_labels)
    elif choice == "2":
        matrix = generator.sign_matrix()
        generator.print_matrix(matrix, "Znaménková matice", node_labels)
    elif choice == "3":
        matrix = generator.incidence_matrix()
        edge_labels = [f"e{i+1}" for i in range(len(generator._edge_list))]
        generator.print_matrix(matrix, "Matice incidence", node_labels, edge_labels)
    elif choice == "4":
        matrix = generator.distance_matrix()
        generator.print_matrix(matrix, "Matice vzdáleností", node_labels)
    elif choice == "5":
        matrix = generator.predecessor_matrix()
        generator.print_matrix(matrix, "Matice předchůdců", node_labels)
    elif choice == "6":
        matrix = generator.adjacency_matrix_power(2)
        generator.print_matrix(matrix, "Matice sousednosti^2", node_labels)
    elif choice == "7":
        matrix = generator.adjacency_matrix_power(3)
        generator.print_matrix(matrix, "Matice sousednosti^3", node_labels)
    elif choice == "8":
        generator.print_all_matrices()
    else:
        print("Neplatná volba!")


def print_matrix_element(graph, matrix_type, row=None, col=None, power=None):
    """
    Vypíše konkrétní element, řádek nebo sloupec z matice.
    
    Args:
        graph (Graph): Graf objekt
        matrix_type (str): Typ matice ('adjacency', 'sign', 'incidence', 'distance', 'predecessor', 'adjacency_power')
        row (str, optional): Identifikátor uzlu pro řádek
        col (str, optional): Identifikátor uzlu pro sloupec
        power (int, optional): Mocnina pro adjacency_power matici
    """
    generator = GraphMatrixGenerator(graph)
    node_labels = [node.identifier for node in graph.nodes()]
    
    # Generování matice podle typu
    if matrix_type == 'adjacency':
        matrix = generator.adjacency_matrix()
        title = "Matice sousednosti"
    elif matrix_type == 'sign':
        matrix = generator.sign_matrix()
        title = "Znaménková matice"
    elif matrix_type == 'incidence':
        matrix = generator.incidence_matrix()
        title = "Matice incidence"
    elif matrix_type == 'distance':
        matrix = generator.distance_matrix()
        title = "Matice vzdáleností"
    elif matrix_type == 'predecessor':
        matrix = generator.predecessor_matrix()
        title = "Matice předchůdců"
    elif matrix_type == 'adjacency_power':
        if power is None:
            print("Pro adjacency_power matici musí být zadána mocnina!")
            return
        matrix = generator.adjacency_matrix_power(power)
        title = f"Matice sousednosti^{power}"
    else:
        print(f"Neplatný typ matice: {matrix_type}")
        return
    
    print(f"=== {title} ===")
    
    # Pokud jsou zadány řádek i sloupec - vypíše konkrétní element
    if row and col:
        if row not in generator.node_to_index or col not in generator.node_to_index:
            print(f"Uzel '{row}' nebo '{col}' neexistuje v grafu!")
            return
        
        row_idx = generator.node_to_index[row]
        col_idx = generator.node_to_index[col]
        value = matrix[row_idx][col_idx]
        print(f"Element [{row}][{col}] = {value}")
    
    # Pokud je zadán pouze řádek - vypíše celý řádek
    elif row:
        if row not in generator.node_to_index:
            print(f"Uzel '{row}' neexistuje v grafu!")
            return
        
        row_idx = generator.node_to_index[row]
        print(f"Řádek pro uzel '{row}':")
        print(f"  {[matrix[row_idx][j] for j in range(len(matrix[row_idx]))]}")
        print(f"  Uzly: {node_labels}")
    
    # Pokud je zadán pouze sloupec - vypíše celý sloupec
    elif col:
        if col not in generator.node_to_index:
            print(f"Uzel '{col}' neexistuje v grafu!")
            return
        
        col_idx = generator.node_to_index[col]
        print(f"Sloupec pro uzel '{col}':")
        print(f"  {[matrix[i][col_idx] for i in range(len(matrix))]}")
        print(f"  Uzly: {node_labels}")
    
    # Pokud není zadán ani řádek ani sloupec - vypíše celou matici
    else:
        generator.print_matrix(matrix, title, node_labels)


def print_adjacency_power_element(graph, power, row=None, col=None):
    """
    Vypíše konkrétní element, řádek nebo sloupec z mocniny matice sousednosti.
    
    Args:
        graph (Graph): Graf objekt
        power (int): Mocnina matice sousednosti
        row (str, optional): Identifikátor uzlu pro řádek
        col (str, optional): Identifikátor uzlu pro sloupec
    """
    generator = GraphMatrixGenerator(graph)
    node_labels = [node.identifier for node in graph.nodes()]
    
    # Generování mocniny matice sousednosti
    matrix = generator.adjacency_matrix_power(power)
    title = f"Matice sousednosti^{power}"
    
    print(f"=== {title} ===")
    
    # Pokud jsou zadány řádek i sloupec - vypíše konkrétní element
    if row and col:
        if row not in generator.node_to_index or col not in generator.node_to_index:
            print(f"Uzel '{row}' nebo '{col}' neexistuje v grafu!")
            return
        
        row_idx = generator.node_to_index[row]
        col_idx = generator.node_to_index[col]
        value = matrix[row_idx][col_idx]
        print(f"Element [{row}][{col}] = {value}")
        print(f"(Počet cest délky {power} z uzlu {row} do uzlu {col})")
    
    # Pokud je zadán pouze řádek - vypíše celý řádek
    elif row:
        if row not in generator.node_to_index:
            print(f"Uzel '{row}' neexistuje v grafu!")
            return
        
        row_idx = generator.node_to_index[row]
        print(f"Řádek pro uzel '{row}':")
        print(f"  {[matrix[row_idx][j] for j in range(len(matrix[row_idx]))]}")
        print(f"  Uzly: {node_labels}")
        print(f"(Počty cest délky {power} z uzlu {row} do všech ostatních uzlů)")
    
    # Pokud je zadán pouze sloupec - vypíše celý sloupec
    elif col:
        if col not in generator.node_to_index:
            print(f"Uzel '{col}' neexistuje v grafu!")
            return
        
        col_idx = generator.node_to_index[col]
        print(f"Sloupec pro uzel '{col}':")
        print(f"  {[matrix[i][col_idx] for i in range(len(matrix))]}")
        print(f"  Uzly: {node_labels}")
        print(f"(Počty cest délky {power} ze všech uzlů do uzlu {col})")
    
    # Pokud není zadán ani řádek ani sloupec - vypíše celou matici
    else:
        generator.print_matrix(matrix, title, node_labels)
        print(f"(Element [i][j] obsahuje počet cest délky {power} z uzlu i do uzlu j)")


def interactive_matrix_explorer(graph):
    """
    Interaktivní průzkumník matic s možností výběru konkrétních částí.
    
    Args:
        graph (Graph): Graf objekt
    """
    generator = GraphMatrixGenerator(graph)
    node_labels = [node.identifier for node in graph.nodes()]
    
    print("=== Interaktivní průzkumník matic ===")
    print(f"Dostupné uzly: {node_labels}")
    print()
    
    while True:
        print("\nMožnosti:")
        print("1. Zobrazit konkrétní matici")
        print("2. Zobrazit konkrétní element")
        print("3. Zobrazit řádek")
        print("4. Zobrazit sloupec")
        print("5. Zobrazit mocninu matice sousednosti")
        print("6. Ukončit")
        
        choice = input("\nVyberte možnost (1-6): ").strip()
        
        if choice == "1":
            print_individual_matrices(graph)
        
        elif choice == "2":
            matrix_type = input("Typ matice (adjacency/sign/incidence/distance/predecessor): ").strip()
            row = input("Řádek (uzel): ").strip()
            col = input("Sloupec (uzel): ").strip()
            print_matrix_element(graph, matrix_type, row, col)
        
        elif choice == "3":
            matrix_type = input("Typ matice (adjacency/sign/incidence/distance/predecessor): ").strip()
            row = input("Řádek (uzel): ").strip()
            print_matrix_element(graph, matrix_type, row=row)
        
        elif choice == "4":
            matrix_type = input("Typ matice (adjacency/sign/incidence/distance/predecessor): ").strip()
            col = input("Sloupec (uzel): ").strip()
            print_matrix_element(graph, matrix_type, col=col)
        
        elif choice == "5":
            try:
                power = int(input("Zadejte mocninu (kladné celé číslo): ").strip())
                if power < 1:
                    print("Mocnina musí být kladné celé číslo!")
                    continue
                
                print("\nMožnosti pro mocninu matice sousednosti:")
                print("1. Celá matice")
                print("2. Konkrétní element")
                print("3. Řádek")
                print("4. Sloupec")
                
                sub_choice = input("Vyberte možnost (1-4): ").strip()
                
                if sub_choice == "1":
                    print_adjacency_power_element(graph, power)
                elif sub_choice == "2":
                    row = input("Řádek (uzel): ").strip()
                    col = input("Sloupec (uzel): ").strip()
                    print_adjacency_power_element(graph, power, row, col)
                elif sub_choice == "3":
                    row = input("Řádek (uzel): ").strip()
                    print_adjacency_power_element(graph, power, row=row)
                elif sub_choice == "4":
                    col = input("Sloupec (uzel): ").strip()
                    print_adjacency_power_element(graph, power, col=col)
                else:
                    print("Neplatná volba!")
                    
            except ValueError:
                print("Neplatná mocnina! Musí být celé číslo.")
        
        elif choice == "6":
            break
        
        else:
            print("Neplatná volba!")


# Example usage and testing
if __name__ == "__main__":
    from .parser import parse_graph
    from .graph import create_graph_from_data
    
    # Test with a sample graph file
    try:
        # Parse a graph file
        data = parse_graph("../grafy/01.tg")
        graph = create_graph_from_data(data)
        
        # Create matrix generator
        generator = GraphMatrixGenerator(graph)
        
        # Print all matrices
        generator.print_all_matrices()
        
    except Exception as e:
        print(f"Error: {e}")
