from ._cohens_d import cohens_d, gene_selection
from ._data_loader import SuematsuData
from ._go import go, gprofiler, get_go
from ._preference import kwarg_savefig, eda_longitudal_args, sgoa_longitudal_args
from ._eda import EDA
from ._stratification import StratifiedGOAnalysis
from ._schematic import Artist
from ._meta_pipeline import metapipeline


__all__ = [
    "SuematsuData",
    "eda_longitudal_args",
    "kwarg_savefig",
    "sgoa_longitudal_args",
    "get_go",
    "go",
    "gprofiler",
    "cohens_d",
    "gene_selection",
    "EDA",
    "StratifiedGOAnalysis",
    "metapipeline",
    "Artist",
]
