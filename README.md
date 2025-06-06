# build_taxa_lineage

Taxonomic Lineage Builder for NCBI TaxIDs using ETE3

This module provides functions to build taxonomic lineages for NCBI taxonomic IDs
using the `ete3.NCBITaxa` interface. It supports both single taxon lookups and
batch lineage mapping with memoization for performance.

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

```console
pip install git+https://github.com/vidyasagar0405/build_taxa_lineage.git#egg=build_taxa_lineage
```
## Usage

Example Usage:

1. build_lineage

```python
from build_taxa_lineage import build_lineage

taxid = 9606 # Homo sapiens

# Build lineages
lineage = build_lineage(taxid)
print(lineage)
```

2. build_lineage_map

```python
from build_taxa_lineage import build_lineage_map

taxid_list = [562, 9606, 12345678]  # Escherichia coli, Homo sapiens, invalid taxid

# Build lineages
lineage_dict = build_lineage_map(taxid_list)

# Print or merge with tabular data
for taxid, lineage in lineage_dict.items():
    print(f"{taxid} → {lineage}")
```

3. Pandas

```python
import pandas as pd
from build_taxa_lineage import build_lineage, build_lineage_map

df = pd.read_csv("input.tsv", sep="\t")
df["ncbi_tax_id"] = df["ncbi_tax_id"].fillna(-1).astype(int)

# For small dataframes (slower)
df["lineage"] = df["ncbi_tax_id"].apply(build_lineage)

# OR for better performance on large unique taxid sets
taxid_list = df["ncbi_tax_id"].unique().tolist()
lineage_map = build_lineage_map(taxid_list)
df["lineage"] = df["ncbi_tax_id"].map(lineage_map)
df.to_csv("output.tsv", sep="\t", index=False)
```

4. Polars

```python
import polars as pl
from build_taxa_lineage import build_lineage_map

df = pl.read_csv("input.tsv", separator="\t")
taxid_list = df.select("ncbi_tax_id").unique().to_series().to_list()
lineage_map = build_lineage_map(taxid_list)

lineage_df = pl.DataFrame({
    "ncbi_tax_id": list(lineage_map.keys()),
    "lineage": list(lineage_map.values())
})

df = df.join(lineage_df, on="ncbi_tax_id", how="left")
df.write_csv("output_with_lineage.tsv")
```
