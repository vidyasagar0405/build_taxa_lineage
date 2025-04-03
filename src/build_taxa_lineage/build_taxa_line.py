#!/usr/bin/env python
"""

Builds the taxanomic lineage from NCBI taxa id

Example usage:

    delimiter = ","
    # Load your CSV file into a DataFrame
    df = pd.read_csv(in_file, sep=delimiter)
    df["ncbi_taxon_id"] = df["ncbi_taxon_id"].fillna(-1).astype(int)
    df["ncbi_taxon_id"] = df["ncbi_taxon_id"].apply(build_lineage)
    df.to_csv(out_file, index=False, sep=delimiter)

"""

from ete3 import NCBITaxa

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


if __name__ == "__main__":
    ...
