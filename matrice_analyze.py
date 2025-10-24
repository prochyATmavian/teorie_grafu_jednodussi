from src.parser import parse_graph
from src.graph import create_graph_from_data
from src.properties import GraphPropertyDetector, print_graph_properties
from src.neighborhoods import NeighborhoodCalculator, print_node_degrees, print_node_relationships, print_node_neighborhoods
from src.matrices import GraphMatrixGenerator, print_all_matrices, print_individual_matrices, print_matrix_element, interactive_matrix_explorer, print_adjacency_power_element
from src.exporter import GraphExporter, export_all_data_to_csv, export_specific_matrix_to_csv, export_adjacency_power_to_csv

"""
=== DOSTUPNÉ MATICE V SYSTÉMU ===

1. MATICE SOUSEDNOSTI (Adjacency Matrix)
   - Klíč: 'adjacency'
   - Popis: Element [i,j] obsahuje váhu nebo počet hran mezi uzly i a j
   - Použití: print_matrix_element(graph, 'adjacency')

2. ZNAMÉNKOVÁ MATICE (Sign Matrix) 
   - Klíč: 'sign'
   - Popis: Element [i,j] obsahuje +1, -1 nebo 0 podle orientace hrany
   - Použití: print_matrix_element(graph, 'sign')

3. MATICE INCIDENCE (Incidence Matrix)
   - Klíč: 'incidence' 
   - Popis: Řádky = uzly, sloupce = hrany, hodnoty +1/-1/0 podle incidence
   - Použití: print_matrix_element(graph, 'incidence')

4. MATICE VZDÁLENOSTÍ (Distance Matrix)
   - Klíč: 'distance'
   - Popis: Element [i,j] obsahuje nejkratší vzdálenost mezi uzly i a j
   - Použití: print_matrix_element(graph, 'distance')

5. MATICE PŘEDCHŮDCŮ (Predecessor Matrix)
   - Klíč: 'predecessor'
   - Popis: Element [i,j] obsahuje předchůdce uzlu j na nejkratší cestě z uzlu i
   - Použití: print_matrix_element(graph, 'predecessor')

6. MOCNINY MATICE SOUSEDNOSTI (Adjacency Matrix Powers)
   - Funkce: print_adjacency_power_element(graph, power)
   - Popis: Element [i,j] obsahuje počet cest délky 'power' z uzlu i do uzlu j
   - Použití: print_adjacency_power_element(graph, 3)  # 3. mocnina

=== FUNKCE PRO PRÁCI S MATICEMI ===

1. print_all_matrices(graph) - Vypíše všechny matice najednou
2. print_individual_matrices(graph) - Interaktivní výběr jednotlivých matic
3. print_matrix_element(graph, matrix_type) - Celá matice
4. print_matrix_element(graph, matrix_type, row, col) - Konkrétní element
5. print_matrix_element(graph, matrix_type, row='A') - Celý řádek
6. print_matrix_element(graph, matrix_type, col='B') - Celý sloupec
7. interactive_matrix_explorer(graph) - Kompletní interaktivní průzkumník
8. print_adjacency_power_element(graph, power) - Práce s mocninami matice sousednosti

=== PŘÍKLADY POUŽITÍ ===
print_matrix_element(graph, 'adjacency')  # Celá matice sousednosti
print_matrix_element(graph, 'distance', 'A', 'B')  # Vzdálenost A->B
print_matrix_element(graph, 'adjacency', row='A')  # Řádek pro uzel A
print_matrix_element(graph, 'distance', col='H')  # Sloupec pro uzel H

# Práce s mocninami matice sousednosti:
print_adjacency_power_element(graph, 2)  # Celá matice sousednosti^2
print_adjacency_power_element(graph, 3, 'A', 'B')  # Počet cest délky 3 z A do B
print_adjacency_power_element(graph, 4, row='A')  # Řádek pro uzel A v matici^4
print_adjacency_power_element(graph, 5, col='H')  # Sloupec pro uzel H v matici^5

=== EXPORT DO CSV ===

1. Export všech dat:
export_all_data_to_csv(graph, "my_graph")

2. Export konkrétní matice:
export_specific_matrix_to_csv(graph, 'adjacency', 'adjacency_matrix.csv')
export_specific_matrix_to_csv(graph, 'sign', 'sign_matrix.csv')
export_specific_matrix_to_csv(graph, 'incidence', 'incidence_matrix.csv')
export_specific_matrix_to_csv(graph, 'distance', 'distance_matrix.csv')
export_specific_matrix_to_csv(graph, 'predecessor', 'predecessor_matrix.csv')

3. Export mocnin matice sousednosti:
export_adjacency_power_to_csv(graph, 2, 'adjacency_power2.csv')
export_adjacency_power_to_csv(graph, 3, 'adjacency_power3.csv')
export_adjacency_power_to_csv(graph, 4, 'adjacency_power4.csv')

4. Použití GraphExporter třídy:
exporter = GraphExporter(graph)
exporter.export_specific_matrix('adjacency', 'custom_adjacency.csv')
exporter.export_adjacency_matrix_power(3, 'custom_power3.csv')
"""


#načtení grafu
data = parse_graph("./grafy/01.tg")
graph = create_graph_from_data(data)

# Získání informací o uzlu A
print_node_relationships(graph, "A")
print("\n" + "="*60 + "\n")

#okolí vstupující do uzlu A a práce s ním
print_node_neighborhoods(graph, "A")

#vlastnosti grafu
print_graph_properties(graph)

print("\n" + "="*60 + "\n")
print("=== Test jednotlivých matic ===")

# Test jednotlivých matic
print_matrix_element(graph, 'adjacency')

print_matrix_element(graph, 'sign', "A")

print_matrix_element(graph, 'distance', "A", "B")

print_matrix_element(graph, 'predecessor')


# 1. Export všech dat najednou
print("\n=== TEST EXPORTŮ DO CSV ===")
exported_files = export_all_data_to_csv(graph, "example_graph")
print(f"Exportováno {len(exported_files)} souborů:")

# 2. Export konkrétních matic
print("\n=== EXPORT KONKRÉTNÍCH MATIC ===")
file_path = export_specific_matrix_to_csv(graph, 'adjacency', 'example_adjacency.csv')
print(f"Adjacency matrix: {file_path}")

file_path = export_specific_matrix_to_csv(graph, 'sign', 'example_sign.csv')
print(f"Sign matrix: {file_path}")

file_path = export_specific_matrix_to_csv(graph, 'distance', 'example_distance.csv')
print(f"Distance matrix: {file_path}")

# 3. Export mocnin matice sousednosti power == mocnina
print("\n=== EXPORT MOCNIN MATICE SOUSEDNOSTI ===")
power = 2
file_path = export_adjacency_power_to_csv(graph, power, f'example_adjacency_power_{power}.csv')
print(f"Adjacency matrix^{power}: {file_path}")

power = 3
file_path = export_adjacency_power_to_csv(graph, power, f'example_adjacency_power_{power}.csv')
print(f"Adjacency matrix^{power}: {file_path}")

# 4. Použití GraphExporter třídy
print("\n=== POUŽITÍ GraphExporter TŘÍDY ===")
exporter = GraphExporter(graph)
file_path = exporter.export_specific_matrix('incidence', 'example_incidence_exporter.csv')
print(f"Incidence matrix: {file_path}")

file_path = exporter.export_specific_matrix('predecessor', 'example_predecessor_exporter.csv')
print(f"Predecessor matrix: {file_path}")

file_path = exporter.export_adjacency_list('example_adjacency_list.csv')
print(f"Adjacency list: {file_path}")

file_path = exporter.export_graph_properties('example_properties.csv')
print(f"Graph properties: {file_path}")

file_path = exporter.export_node_degrees('example_degrees.csv')
print(f"Node degrees: {file_path}")


# Celá matice sousednosti^2
print_adjacency_power_element(graph, 2)

# Konkrétní element - počet cest délky 3 z A do B
print_adjacency_power_element(graph, 3, 'A', 'B')

# Řádek pro uzel E v matici^4
print_adjacency_power_element(graph, 4, row='E')

# Sloupec pro uzel H v matici^5
print_adjacency_power_element(graph, 5, col='H')


