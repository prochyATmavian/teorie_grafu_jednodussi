# Rozšířená funkcionalita pro práci s mocninami matice sousednosti

Tento dokument popisuje nové funkce pro práci s vyššími mocninami matice sousednosti, které umožňují zobrazit celou matici, konkrétní řádek, sloupec nebo hodnotu.

## Nové funkce

### 1. `print_adjacency_power_element(graph, power, row=None, col=None)`

Hlavní funkce pro práci s mocninami matice sousednosti.

**Parametry:**
- `graph`: Graf objekt
- `power`: Mocnina matice sousednosti (kladné celé číslo)
- `row`: Identifikátor uzlu pro řádek (volitelné)
- `col`: Identifikátor uzlu pro sloupec (volitelné)

**Možnosti použití:**

#### Celá matice
```python
print_adjacency_power_element(graph, 2)  # Celá matice sousednosti^2
```

#### Konkrétní element
```python
print_adjacency_power_element(graph, 3, 'A', 'B')  # Počet cest délky 3 z A do B
```

#### Celý řádek
```python
print_adjacency_power_element(graph, 4, row='E')  # Řádek pro uzel E v matici^4
```

#### Celý sloupec
```python
print_adjacency_power_element(graph, 5, col='H')  # Sloupec pro uzel H v matici^5
```

### 2. Rozšířená funkce `print_matrix_element()`

Původní funkce byla rozšířena o podporu mocnin:

```python
print_matrix_element(graph, 'adjacency_power', power=3)  # Celá matice^3
print_matrix_element(graph, 'adjacency_power', 'A', 'B', power=3)  # Element [A][B] v matici^3
```

### 3. Rozšířený interaktivní průzkumník

Interaktivní průzkumník (`interactive_matrix_explorer`) nyní obsahuje novou možnost:

**Možnost 5: Zobrazit mocninu matice sousednosti**
- Uživatel zadá mocninu
- Vybere si, co chce zobrazit (celá matice, element, řádek, sloupec)
- Systém zobrazí požadované informace s vysvětlením

## Význam hodnot v mocninách matice sousednosti

Element `[i][j]` v matici sousednosti umocněné na `k` obsahuje **počet cest délky k** z uzlu `i` do uzlu `j`.

### Příklady interpretace:

- **Matice sousednosti^1**: Počet přímých hran mezi uzly
- **Matice sousednosti^2**: Počet cest délky 2 (přes jeden mezilehlý uzel)
- **Matice sousednosti^3**: Počet cest délky 3 (přes dva mezilehlé uzly)
- **Matice sousednosti^k**: Počet cest délky k

## Praktické příklady

### Příklad 1: Analýza dostupnosti
```python
# Kolik cest délky 2 vede z uzlu A do uzlu E?
print_adjacency_power_element(graph, 2, 'A', 'E')

# Výstup: Element [A][E] = 8
# Interpretace: Existuje 8 různých cest délky 2 z A do E
```

### Příklad 2: Analýza centrality
```python
# Kolik cest délky 3 vede ze všech uzlů do uzlu H?
print_adjacency_power_element(graph, 3, col='H')

# Výstup: Sloupec pro uzel 'H': [0, 28, 105, 0, 0, 0, 0, 0]
# Interpretace: Pouze uzly B a C mají cesty délky 3 do H
```

### Příklad 3: Analýza propojení
```python
# Kolik cest délky 4 vede z uzlu E do všech ostatních uzlů?
print_adjacency_power_element(graph, 4, row='E')

# Výstup: Řádek pro uzel 'E': [710, 1065, 0, 1225, 6, 1783, 2130, 84]
# Interpretace: Uzel E je velmi dobře propojen s ostatními uzly
```

## Použití v matrice_analyze.py

Soubor `matrice_analyze.py` obsahuje kompletní demonstraci všech možností:

```python
# Celá matice sousednosti^2
print_adjacency_power_element(graph, 2)

# Konkrétní element - počet cest délky 3 z A do B
print_adjacency_power_element(graph, 3, 'A', 'B')

# Řádek pro uzel E v matici^4
print_adjacency_power_element(graph, 4, row='E')

# Sloupec pro uzel H v matici^5
print_adjacency_power_element(graph, 5, col='H')
```

## Interaktivní použití

Pro interaktivní práci použijte:

```bash
python3 run.py interactive
```

V interaktivním módu zvolte možnost 5 pro práci s mocninami matice sousednosti.

## Výhody nové funkcionality

1. **Flexibilita**: Možnost zobrazit celou matici, řádek, sloupec nebo konkrétní hodnotu
2. **Vysvětlení**: Každý výstup obsahuje vysvětlení významu hodnot
3. **Konzistence**: Stejné rozhraní jako u ostatních matic
4. **Interaktivnost**: Snadné použití v interaktivním módu
5. **Dokumentace**: Kompletní příklady v matrice_analyze.py

## Technické detaily

- Mocniny se počítají pomocí maticového násobení
- Podporovány jsou všechny kladné celé mocniny
- Výpočet je optimalizován pro efektivitu
- Chybové hlášky pro neplatné uzly a mocniny
- Kompatibilita s existujícím kódem
