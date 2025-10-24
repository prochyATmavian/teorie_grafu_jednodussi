"""
CSV Operations module for graph recognition system.
Handles CSV export and import functionality for matrices and graph data.
"""

from .exporter import (
    GraphExporter, GraphImporter, 
    export_all_data_to_csv, export_specific_matrix_to_csv, export_adjacency_power_to_csv,
    import_matrix_from_csv, import_adjacency_matrix_from_csv, import_distance_matrix_from_csv,
    import_incidence_matrix_from_csv, import_sign_matrix_from_csv, import_predecessor_matrix_from_csv,
    import_adjacency_list_from_csv
)
from .matrices import GraphMatrixGenerator


# === CSV EXPORT FUNCTIONS ===

def export_graph_matrices_to_csv(graph, prefix="graph"):
    """
    Exportuje všechny matice grafu do CSV souborů.
    
    Args:
        graph: Graf objekt
        prefix (str): Prefix pro názvy souborů
        
    Returns:
        list: Seznam cest k exportovaným souborům
    """
    print(f"Exportujem matice grafu do CSV s prefixem '{prefix}'...")
    
    exporter = GraphExporter(graph)
    exported_files = exporter.export_all_matrices(prefix)
    
    print(f"Exportováno {len(exported_files)} souborů:")
    for file_path in exported_files:
        print(f"  - {file_path}")
    
    return exported_files

def export_specific_matrix_to_csv_file(graph, matrix_type, filename):
    """
    Exportuje konkrétní matici do CSV souboru.
    
    Args:
        graph: Graf objekt
        matrix_type (str): Typ matice ('adjacency', 'sign', 'incidence', 'distance', 'predecessor')
        filename (str): Název CSV souboru
        
    Returns:
        str: Cesta k exportovanému souboru
    """
    print(f"Exportujem {matrix_type} matici do '{filename}'...")
    
    file_path = export_specific_matrix_to_csv(graph, matrix_type, filename)
    print(f"Matice exportována do: {file_path}")
    
    return file_path

def export_adjacency_power_to_csv_file(graph, power, filename):
    """
    Exportuje mocninu matice sousednosti do CSV souboru.
    
    Args:
        graph: Graf objekt
        power (int): Mocnina matice sousednosti
        filename (str): Název CSV souboru
        
    Returns:
        str: Cesta k exportovanému souboru
    """
    print(f"Exportujem matici sousednosti^{power} do '{filename}'...")
    
    file_path = export_adjacency_power_to_csv(graph, power, filename)
    print(f"Matice exportována do: {file_path}")
    
    return file_path

# === CSV IMPORT FUNCTIONS ===

def load_matrix_from_csv(filepath, matrix_type="matrix", has_labels=True):
    """
    Načte matici z CSV souboru.
    
    Args:
        filepath (str): Cesta k CSV souboru
        matrix_type (str): Typ matice pro validaci
        has_labels (bool): Zda CSV obsahuje popisky řádků/sloupců
        
    Returns:
        tuple: (matice, popisky_řádků, popisky_sloupců)
    """
    print(f"Načítám {matrix_type} matici z '{filepath}'...")
    
    try:
        matrix, row_labels, col_labels = import_matrix_from_csv(filepath, matrix_type, has_labels)
        
        print(f"Matice načtena: {len(matrix)}x{len(matrix[0]) if matrix else 0}")
        if row_labels:
            print(f"Popisky řádků: {row_labels}")
        if col_labels:
            print(f"Popisky sloupců: {col_labels}")
        
        return matrix, row_labels, col_labels
        
    except Exception as e:
        print(f"Chyba při načítání matice: {e}")
        return None, None, None

def load_adjacency_matrix_from_csv_file(filepath, has_labels=True):
    """
    Načte matici sousednosti z CSV souboru.
    
    Args:
        filepath (str): Cesta k CSV souboru
        has_labels (bool): Zda CSV obsahuje popisky
        
    Returns:
        tuple: (matice, popisky_uzlů)
    """
    print(f"Načítám matici sousednosti z '{filepath}'...")
    
    try:
        matrix, node_labels = import_adjacency_matrix_from_csv(filepath, has_labels)
        
        print(f"Matice sousednosti načtena: {len(matrix)}x{len(matrix[0])}")
        print(f"Popisky uzlů: {node_labels}")
        
        return matrix, node_labels
        
    except Exception as e:
        print(f"Chyba při načítání matice sousednosti: {e}")
        return None, None

def load_distance_matrix_from_csv_file(filepath, has_labels=True):
    """
    Načte matici vzdáleností z CSV souboru.
    
    Args:
        filepath (str): Cesta k CSV souboru
        has_labels (bool): Zda CSV obsahuje popisky
        
    Returns:
        tuple: (matice, popisky_uzlů)
    """
    print(f"Načítám matici vzdáleností z '{filepath}'...")
    
    try:
        matrix, node_labels = import_distance_matrix_from_csv(filepath, has_labels)
        
        print(f"Matice vzdáleností načtena: {len(matrix)}x{len(matrix[0])}")
        print(f"Popisky uzlů: {node_labels}")
        
        return matrix, node_labels
        
    except Exception as e:
        print(f"Chyba při načítání matice vzdáleností: {e}")
        return None, None

def load_incidence_matrix_from_csv_file(filepath, has_labels=True):
    """
    Načte matici incidence z CSV souboru.
    
    Args:
        filepath (str): Cesta k CSV souboru
        has_labels (bool): Zda CSV obsahuje popisky
        
    Returns:
        tuple: (matice, popisky_uzlů, popisky_hran)
    """
    print(f"Načítám matici incidence z '{filepath}'...")
    
    try:
        matrix, node_labels, edge_labels = import_incidence_matrix_from_csv(filepath, has_labels)
        
        print(f"Matice incidence načtena: {len(matrix)}x{len(matrix[0]) if matrix else 0}")
        print(f"Popisky uzlů: {node_labels}")
        print(f"Popisky hran: {edge_labels}")
        
        return matrix, node_labels, edge_labels
        
    except Exception as e:
        print(f"Chyba při načítání matice incidence: {e}")
        return None, None, None

def load_adjacency_list_from_csv_file(filepath):
    """
    Načte seznam sousednosti z CSV souboru.
    
    Args:
        filepath (str): Cesta k CSV souboru
        
    Returns:
        dict: Slovník seznamu sousednosti
    """
    print(f"Načítám seznam sousednosti z '{filepath}'...")
    
    try:
        adj_list = import_adjacency_list_from_csv(filepath)
        
        print(f"Seznam sousednosti načten: {len(adj_list)} uzlů")
        for node, neighbors in adj_list.items():
            print(f"  {node}: {neighbors}")
        
        return adj_list
        
    except Exception as e:
        print(f"Chyba při načítání seznamu sousednosti: {e}")
        return None

# === VALIDATION FUNCTIONS ===

def validate_imported_matrix(matrix, matrix_type):
    """
    Validuje načtenou matici podle typu.
    
    Args:
        matrix: Matice k validaci
        matrix_type (str): Typ matice
        
    Returns:
        bool: True pokud je matice validní
    """
    if matrix is None:
        print("Matice je None - nelze validovat")
        return False
    
    importer = GraphImporter()
    is_valid = importer.validate_matrix_format(matrix, matrix_type)
    
    if is_valid:
        print(f"Matice typu '{matrix_type}' je validní")
    else:
        print(f"Matice typu '{matrix_type}' není validní")
    
    return is_valid

def compare_matrices(matrix1, matrix2, matrix_type="matrix"):
    """
    Porovná dvě matice a vypíše rozdíly.
    
    Args:
        matrix1: První matice
        matrix2: Druhá matice
        matrix_type (str): Typ matice pro popis
        
    Returns:
        bool: True pokud jsou matice stejné
    """
    if matrix1 is None or matrix2 is None:
        print("Jedna z matic je None - nelze porovnat")
        return False
    
    if len(matrix1) != len(matrix2):
        print(f"Matice mají různý počet řádků: {len(matrix1)} vs {len(matrix2)}")
        return False
    
    if len(matrix1[0]) != len(matrix2[0]):
        print(f"Matice mají různý počet sloupců: {len(matrix1[0])} vs {len(matrix2[0])}")
        return False
    
    differences = []
    for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            if matrix1[i][j] != matrix2[i][j]:
                differences.append((i, j, matrix1[i][j], matrix2[i][j]))
    
    if differences:
        print(f"Nalezeno {len(differences)} rozdílů v {matrix_type} matici:")
        for i, j, val1, val2 in differences[:5]:  # Zobrazit pouze prvních 5 rozdílů
            print(f"  Pozice [{i}][{j}]: {val1} vs {val2}")
        if len(differences) > 5:
            print(f"  ... a dalších {len(differences) - 5} rozdílů")
        return False
    else:
        print(f"{matrix_type} matice jsou identické")
        return True

# === DEMO FUNCTIONS ===

def demo_csv_export_import(graph):
    """
    Demonstruje export a import matic do/z CSV souborů.
    
    Args:
        graph: Graf objekt
    """
    print("\n" + "="*60)
    print("=== DEMO: Export a Import matic do/z CSV ===")
    
    # Export matic
    print("\n1. Export matic do CSV:")
    exported_files = export_graph_matrices_to_csv(graph, "demo_graph")
    
    # Export konkrétní matice
    print("\n2. Export konkrétní matice:")
    adj_file = export_specific_matrix_to_csv_file(graph, 'adjacency', 'demo_adjacency.csv')
    dist_file = export_specific_matrix_to_csv_file(graph, 'distance', 'demo_distance.csv')
    
    # Export mocniny matice sousednosti
    print("\n3. Export mocniny matice sousednosti:")
    power_file = export_adjacency_power_to_csv_file(graph, 2, 'demo_adjacency_power2.csv')
    
    # Import matic zpět
    print("\n4. Import matic zpět z CSV:")
    
    # Import matice sousednosti
    imported_adj, adj_labels = load_adjacency_matrix_from_csv_file(adj_file)
    
    # Import matice vzdáleností
    imported_dist, dist_labels = load_distance_matrix_from_csv_file(dist_file)
    
    # Import obecné matice
    imported_power, power_row_labels, power_col_labels = load_matrix_from_csv(power_file, "adjacency_power", True)
    
    # Validace importovaných matic
    print("\n5. Validace importovaných matic:")
    validate_imported_matrix(imported_adj, 'adjacency')
    validate_imported_matrix(imported_dist, 'distance')
    validate_imported_matrix(imported_power, 'adjacency_power')
    
    # Porovnání s originálními maticemi
    print("\n6. Porovnání s originálními maticemi:")
    
    # Generování originálních matic pro porovnání
    generator = GraphMatrixGenerator(graph)
    original_adj = generator.adjacency_matrix()
    original_dist = generator.distance_matrix()
    original_power = generator.adjacency_matrix_power(2)
    
    compare_matrices(original_adj, imported_adj, "sousednosti")
    compare_matrices(original_dist, imported_dist, "vzdáleností")
    compare_matrices(original_power, imported_power, "sousednosti^2")
    
    print("\n=== DEMO dokončeno ===")

def demo_matrix_operations():
    """
    Demonstruje práci s načtenými maticemi.
    """
    print("\n" + "="*60)
    print("=== DEMO: Práce s načtenými maticemi ===")
    
    # Načtení matice sousednosti
    print("\n1. Načítání matice sousednosti:")
    matrix, labels = load_adjacency_matrix_from_csv_file("csv_files/demo_adjacency.csv")
    
    if matrix is not None:
        print("\n2. Analýza načtené matice:")
        print(f"   Velikost: {len(matrix)}x{len(matrix[0])}")
        print(f"   Uzly: {labels}")
        
        # Najít uzly s nejvyšším stupněm
        degrees = []
        for i, row in enumerate(matrix):
            degree = sum(1 for val in row if val > 0)
            degrees.append((labels[i], degree))
        
        degrees.sort(key=lambda x: x[1], reverse=True)
        print(f"   Uzly podle stupně: {degrees}")
        
        # Najít symetrické páry
        symmetric_pairs = []
        for i in range(len(matrix)):
            for j in range(i+1, len(matrix)):
                if matrix[i][j] == matrix[j][i] and matrix[i][j] > 0:
                    symmetric_pairs.append((labels[i], labels[j]))
        
        print(f"   Symetrické páry: {symmetric_pairs}")
    
    print("\n=== DEMO dokončeno ===")
