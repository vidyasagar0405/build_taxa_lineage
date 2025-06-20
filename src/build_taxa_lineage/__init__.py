# SPDX-FileCopyrightText: 2025-present vidyasagar0405 <vidyasagar0405@gmail.com>
#
# SPDX-License-Identifier: MIT
######################################################################
# Main app information.
__author__ = "Vidyasagar"
__copyright__ = "Copyright 2025, Vidyasagar"
__credits__ = ["Vidyasagar"]
__maintainer__ = "Vidyasagar"
__version__ = "0.0.6"
__licence__ = "MIT"

##############################################################################
# Local imports.

from build_taxa_lineage.build_taxa_line import (
    build_lineage,
    build_lineage_map,
)

##############################################################################
# Export the imports.

__all__ = ["build_lineage", "build_lineage_map"]

### __init__.py ends here
