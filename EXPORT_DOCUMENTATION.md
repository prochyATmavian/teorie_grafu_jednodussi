# Rozšířené možnosti exportu matic

Tento dokument popisuje nové funkce pro export konkrétních matic a vyšších mocnin matice sousednosti do CSV souborů.

## Nové funkce

### 1. Export konkrétní matice

Můžete nyní exportovat pouze konkrétní typ matice místo všech matic najednou.

#### CLI příkazy:
```bash
# Export matice sousednosti
python3 run.py export-matrix grafy/01.tg --type adjacency

# Export znaménkové matice
python3 run.py export-matrix grafy/01.tg --type sign

# Export matice incidence
python3 run.py export-matrix grafy/01.tg --type incidence

# Export matice vzdáleností
python3 run.py export-matrix grafy/01.tg --type distance

# Export matice předchůdců
python3 run.py export-matrix grafy/01.tg --type predecessor

# S vlastním názvem souboru
python3 run.py export-matrix grafy/01.tg --type adjacency --filename moje_matice.csv
```

#### Programové použití:
```python
from src.exporter import export_specific_matrix_to_csv

# Export konkrétní matice
file_path = export_specific_matrix_to_csv(graph, 'adjacency', 'custom_name.csv')
```

### 2. Export vyšších mocnin matice sousednosti

Můžete exportovat matici sousednosti umocněnou na libovolnou mocninu.

#### CLI příkazy:
```bash
# Export matice sousednosti na 2. mocninu
python3 run.py export-power grafy/01.tg --power 2

# Export matice sousednosti na 5. mocninu
python3 run.py export-power grafy/01.tg --power 5

# S vlastním názvem souboru
python3 run.py export-power grafy/01.tg --power 3 --filename mocnina3.csv
```

#### Programové použití:
```python
from src.exporter import export_adjacency_power_to_csv

# Export matice sousednosti na 3. mocninu
file_path = export_adjacency_power_to_csv(graph, 3, 'power3.csv')
```

### 3. Interaktivní mód

V interaktivním módu jsou k dispozici nové příkazy:

```bash
python3 run.py interactive
```

#### Nové příkazy v interaktivním módu:
- `export-matrix` - Interaktivní export konkrétní matice
- `export-power` - Interaktivní export mocniny matice sousednosti

## Dostupné typy matic

1. **adjacency** - Matice sousednosti
2. **sign** - Znaménková matice
3. **incidence** - Matice incidence
4. **distance** - Matice vzdáleností
5. **predecessor** - Matice předchůdců

## Formát výstupních souborů

Všechny exportované soubory jsou uloženy v adresáři `csv_files/` a obsahují:

1. **Hlavičku** s názvem typu matice
2. **Prázdný řádek**
3. **Záhlaví sloupců** s identifikátory uzlů
4. **Data matice** s řádkovými popisky

### Příklad výstupu:
```csv
ADJACENCY MATRIX MATRIX

,A,B,C,D,E,F,G,H
A,0,1,0,2,0,0,0,0
B,0,0,1,0,0,0,0,0
C,0,0,0,0,3,4,0,0
...
```

## Testování

Pro testování nových funkcí můžete použít:

```bash
# Spustit testovací skript
python3 test_export.py

# Nebo použít CLI příkazy
python3 run.py export-matrix grafy/01.tg --type adjacency
python3 run.py export-power grafy/01.tg --power 3
```

## Poznámky

- Mocniny matice sousednosti počítají počet cest dané délky mezi uzly
- Matice předchůdců obsahuje identifikátory uzlů místo indexů
- Matice incidence má sloupce označené identifikátory hran
- Všechny soubory jsou uloženy v adresáři `csv_files/`
