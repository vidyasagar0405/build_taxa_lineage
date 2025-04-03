from build_taxa_lineage.build_taxa_line import build_lineage
import sys

if __name__ == "__main__":
    for i in sys.argv:
        print(build_lineage(int(i)))
