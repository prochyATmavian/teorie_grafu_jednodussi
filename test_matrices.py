#!/usr/bin/env python3
"""
Testovací soubor pro demonstraci funkcí pro práci s maticemi.
"""

from src.parser import parse_graph
from src.graph import create_graph_from_data
from src.matrices import (
    print_individual_matrices, 
    print_matrix_element, 
    interactive_matrix_explorer
)

def main():
    # Načtení grafu
    data = parse_graph("./grafy/01.tg")
    graph = create_graph_from_data(data)
    
    print("=== Demonstrace funkcí pro matice ===\n")
    
    # 1. Interaktivní výběr jednotlivých matic
    print("1. Interaktivní výběr jednotlivých matic:")
    print("   Zavolejte: print_individual_matrices(graph)")
    print()
    
    # 2. Výpis konkrétních částí matic
    print("2. Výpis konkrétních částí matic:")
    print("   print_matrix_element(graph, 'adjacency')  # Celá matice")
    print("   print_matrix_element(graph, 'adjacency', 'A', 'B')  # Konkrétní element")
    print("   print_matrix_element(graph, 'adjacency', row='A')  # Celý řádek")
    print("   print_matrix_element(graph, 'adjacency', col='B')  # Celý sloupec")
    print()
    
    # 3. Interaktivní průzkumník
    print("3. Interaktivní průzkumník matic:")
    print("   Zavolejte: interactive_matrix_explorer(graph)")
    print()
    
    # Příklady použití
    print("=== Příklady použití ===")
    
    print("\nAdjacency Matrix:")
    print_matrix_element(graph, 'adjacency')
    
    print("\nElement [E][F] z Distance Matrix:")
    print_matrix_element(graph, 'distance', 'E', 'F')
    
    print("\nŘádek pro uzel E z Adjacency Matrix:")
    print_matrix_element(graph, 'adjacency', row='E')
    
    print("\nSloupec pro uzel H z Distance Matrix:")
    print_matrix_element(graph, 'distance', col='H')

if __name__ == "__main__":
    main()
