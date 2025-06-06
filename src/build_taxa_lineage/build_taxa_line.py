#!/usr/bin/env python
"""
Taxonomic Lineage Builder for NCBI TaxIDs using ETE4

This module provides functions to build taxonomic lineages for NCBI taxonomic IDs
using the `ete3.NCBITaxa` interface. It supports both single taxon lookups and
batch lineage mapping with memoization for performance.

---

## Example Usage (Pandas):

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
"""
from ete3 import NCBITaxa
from functools import lru_cache
from typing import Optional

# Mapping from NCBI ranks to prefixes
rank_prefix = {
    "domain": "d",
    "phylum": "p",
    "class": "c",
    "order": "o",
    "family": "f",
    "genus": "g",
    "species": "s",
}


@lru_cache(maxsize=None)
def build_lineage(taxid: int, dbfile: Optional[str] = None) -> Optional[str]:
    """Return formatted taxonomic lineage for a single taxid."""
    try:
        ncbi = NCBITaxa(dbfile=dbfile)
        lineage = ncbi.get_lineage(taxid)
        names = ncbi.get_taxid_translator(lineage)
        ranks = ncbi.get_rank(lineage)

        lineage_parts = [
            f"{rank_prefix[ranks[tid]]}__{names[tid].replace(' ', '_')}"
            for tid in lineage if ranks.get(tid) in rank_prefix
        ]

        return "|".join(lineage_parts)

    except Exception as e:
        print(f"[ERROR] TaxID {taxid}: {e}")
        return None


def build_lineage_map(taxids: list[int], dbfile: Optional[str] = None) -> dict[int, Optional[str]]:
    """Build a lineage dictionary for a list of taxids."""
    ncbi = NCBITaxa(dbfile=dbfile)
    lineage_map = {}

    for taxid in taxids:
        try:
            lineage = ncbi.get_lineage(taxid)
            names = ncbi.get_taxid_translator(lineage)
            ranks = ncbi.get_rank(lineage)

            lineage_parts = [
                f"{rank_prefix[ranks[tid]]}__{names[tid].replace(' ', '_')}"
                for tid in lineage if ranks.get(tid) in rank_prefix
            ]

            lineage_map[taxid] = "|".join(lineage_parts)
        except Exception as e:
            print(f"[WARN] Failed for taxid {taxid}: {e}")
            lineage_map[taxid] = None

    return lineage_map


if __name__ == "__main__":
    pass  # Or test/debug code here
