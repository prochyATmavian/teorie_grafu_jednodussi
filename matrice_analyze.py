from src.parser import parse_graph
from src.graph import create_graph_from_data
from src.properties import GraphPropertyDetector, print_graph_properties
from src.neighborhoods import NeighborhoodCalculator, print_node_degrees, print_node_relationships, print_node_neighborhoods
from src.matrices import GraphMatrixGenerator, print_all_matrices, print_individual_matrices, print_matrix_element, interactive_matrix_explorer, print_adjacency_power_element
from src.exporter import GraphExporter, export_all_data_to_csv, export_specific_matrix_to_csv, export_adjacency_power_to_csv


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
print_adjacency_power_element(graph, 2)

# Konkrétní element - počet cest délky 3 z A do B
print_adjacency_power_element(graph, 3, 'A', 'B')

# Řádek pro uzel E v matici^4
print_adjacency_power_element(graph, 4, row='E')

# Sloupec pro uzel H v matici^5
print_adjacency_power_element(graph, 5, col='H')


