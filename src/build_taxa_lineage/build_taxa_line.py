#!/usr/bin/env python
#!/usr/bin/env python3
"""
Taxonomic Lineage Builder for NCBI TaxIDs using ETE3

This module provides functions to build taxonomic lineages for NCBI taxonomic IDs
using the `ete3.NCBITaxa` interface. It supports both single taxon lookups and
batch lineage mapping with memoization for performance.

---

📌 Example Usage (Pandas):

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

from ete4 import NCBITaxa
from functools import lru_cache

# Define a mapping from NCBI ranks to the desired prefix in the output
rank_prefix = {
    # "superkingdom": "k",  # sometimes 'superkingdom' is used instead of 'kingdom'
    # "kingdom": "k",
    "domain": "d",
    "phylum": "p",
    "class": "c",
    "order": "o",
    "family": "f",
    "genus": "g",
    "species": "s",
}


@lru_cache(maxsize=None)
def build_lineage(taxid: int) -> str | None:
    """
    Returns the taxanomic lineage of the given NCBI taxa id
    """

    try:
        # Initialize the NCBI taxonomy database
        ncbi = NCBITaxa()

        # Get the full lineage list (a list of taxid integers)
        lineage = ncbi.get_lineage(taxid)

        # Get a dictionary mapping taxid to its scientific name
        names = ncbi.get_taxid_translator(lineage)

        # Get the rank information for each taxid in the lineage
        ranks = ncbi.get_rank(lineage)

        # Build the formatted lineage parts
        lineage_parts = []
        for tid in lineage:
            rank = ranks.get(tid)
            if rank in rank_prefix:
                prefix = rank_prefix[rank]
                name = names.get(tid).replace(
                    " ", "_"
                )  # Replace spaces with underscores
                lineage_parts.append(f"{prefix}__{name}")
                # lineage_parts.append(name) # For LEfSe

        # Join parts with "|" to produce the final formatted string
        return "|".join(lineage_parts)

    except Exception as e:
        print(f"Error processing taxid {taxid}: {e}")
        return None


def build_lineage_map(taxids: list[int]) -> dict[int, str]:
    """
    Build a lineage map for a list of taxids using ETE3 in batch.
    Returns a dictionary: taxid -> lineage string
    """
    ncbi = NCBITaxa()
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
    ...
