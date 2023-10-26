from ._cohens_d import cohens_d, gene_selection
from ._data_loader import SuematsuData
from ._go import go, gprofiler
from ._preference import kwarg_savefig
from ._eda import EDA


__all__ = [
    "SuematsuData",
    "kwarg_savefig",
    "go",
    "gprofiler",
    "cohens_d",
    "gene_selection",
    "EDA", 
]
