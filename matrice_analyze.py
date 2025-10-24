from src.parser import parse_graph
from src.graph import create_graph_from_data
from src.properties import GraphPropertyDetector, print_graph_properties
from src.neighborhoods import NeighborhoodCalculator, print_node_degrees, print_node_relationships, print_node_neighborhoods
from src.matrices import GraphMatrixGenerator, print_all_matrices, print_individual_matrices, print_matrix_element, interactive_matrix_explorer, print_adjacency_power_element
from src.exporter import GraphExporter, export_all_data_to_csv, export_specific_matrix_to_csv, export_adjacency_power_to_csv
from src.csv_operations import (
    export_graph_matrices_to_csv, export_specific_matrix_to_csv_file, export_adjacency_power_to_csv_file,
    load_matrix_from_csv, load_adjacency_matrix_from_csv_file, load_distance_matrix_from_csv_file,
    load_incidence_matrix_from_csv_file, load_adjacency_list_from_csv_file,
    validate_imported_matrix, compare_matrices,
    demo_csv_export_import, demo_matrix_operations
)

#načtení grafu
data = parse_graph("./grafy/veryBigGraph.tg")
graph = create_graph_from_data(data)

# Získání informací o uzlu node0
print_node_relationships(graph, "node1")
#print_node_relationships(graph, "A")

#okolí vstupující do uzlu node0 a práce s ním
print_node_neighborhoods(graph, "node0")

#vlastnosti grafu - jednotlivě pro měření výkonu
import time

detector = GraphPropertyDetector(graph)

print("=== Měření výkonu vlastností grafu ===")
print(f"Graf má {graph.node_count()} uzlů a {graph.edge_count()} hran")
print()

properties_to_test = [
    ("a) ohodnocený (weighted)", detector.is_weighted),
    ("b) orientovaný (directed)", detector.is_directed),
    ("c) silně souvislý (strongly connected)", detector.is_strongly_connected),
    ("c) slabě souvislý (weakly connected)", detector.is_weakly_connected),
    ("d) prostý (simple - no multi-edges)", detector.is_simple_no_multiedges),
    ("e) jednoduchý (simple - no loops or multi-edges)", detector.is_simple),
    #("f) rovinný (planar)", detector.is_planar),
    #("g) konečný (finite)", detector.is_finite),
    ("h) úplný (complete)", detector.is_complete),
    ("i) regulární (regular)", detector.is_regular),
    ("j) bipartitní (bipartite)", detector.is_bipartite)
]

for prop_name, prop_func in properties_to_test:
    start_time = time.time()
    try:
        result = prop_func()
        end_time = time.time()
        duration = end_time - start_time
        status = "YES" if result else "NO"
        print(f"{prop_name}: {status} (čas: {duration:.4f}s)")
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"{prop_name}: CHYBA - {e} (čas: {duration:.4f}s)")


print("\n" + "="*60 + "\n")
print("=== Test jednotlivých matic ===")

# Test jednotlivých matic
"""
print_matrix_element(graph, 'binary_adjacency')
print_matrix_element(graph, 'weighted_adjacency')

print_matrix_element(graph, 'sign', "A")

print_matrix_element(graph, 'distance', "A", "B")

print_matrix_element(graph, 'predecessor')

print_matrix_element(graph, 'incidence')
"""

# 1. Export všech dat najednou
"""
exported_files = export_all_data_to_csv(graph, "example_graph")
"""

# 2. Export konkrétních matic
"""
file_path = export_specific_matrix_to_csv(graph, 'adjacency', 'example_adjacency.csv')
file_path = export_specific_matrix_to_csv(graph, 'sign', 'example_sign.csv')
file_path = export_specific_matrix_to_csv(graph, 'distance', 'example_distance.csv')
"""


# 3. Export mocnin matice sousednosti power == mocnina
"""
power = 3
file_path = export_adjacency_power_to_csv(graph, power, f'example_adjacency_power_{power}.csv')
"""

# 4. Použití GraphExporter třídy
"""
exporter = GraphExporter(graph)
file_path = exporter.export_specific_matrix('incidence', 'example_incidence_exporter.csv')
file_path = exporter.export_specific_matrix('predecessor', 'example_predecessor_exporter.csv')
file_path = exporter.export_adjacency_list('example_adjacency_list.csv')
file_path = exporter.export_graph_properties('example_properties.csv')
file_path = exporter.export_node_degrees('example_degrees.csv')
"""


# Celá matice sousednosti^2
#print_adjacency_power_element(graph, 2)

# Konkrétní element - počet cest délky 3 z A do B
#print_adjacency_power_element(graph, 3, 'A', 'B')

# Řádek pro uzel E v matici^4
#print_adjacency_power_element(graph, 4, row='E')

# Sloupec pro uzel H v matici^5
#print_adjacency_power_element(graph, 5, col='H')


print("\n" + "="*60 + "\n")
print("=== CSV Export/Import Test ===")

# === CSV OPERATIONS ===
# Všechny CSV funkce jsou nyní v src/csv_operations.py

# Export všech matic do CSV
# exported_files = export_graph_matrices_to_csv(graph, "example_graph")

# Export konkrétní matice
# adj_file = export_specific_matrix_to_csv_file(graph, 'adjacency', 'example_adjacency.csv')
# dist_file = export_specific_matrix_to_csv_file(graph, 'distance', 'example_distance.csv')

# Export mocniny matice sousednosti
# power_file = export_adjacency_power_to_csv_file(graph, 2, 'example_power2.csv')

# Import matic z CSV
# matrix, labels = load_adjacency_matrix_from_csv_file('example_adjacency.csv')
# dist_matrix, dist_labels = load_distance_matrix_from_csv_file('example_distance.csv')

# Validace importovaných matic
# is_valid = validate_imported_matrix(matrix, 'adjacency')

# Porovnání matic
# are_same = compare_matrices(original_matrix, imported_matrix, "sousednosti")

# === DEMO FUNCTIONS ===
# Odkomentujte pro spuštění demo funkcí:

# Kompletní demo export/import workflow
# demo_csv_export_import(graph)

# Demo práce s načtenými maticemi
# demo_matrix_operations()
