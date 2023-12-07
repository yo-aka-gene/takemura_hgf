from ._cohens_d import cohens_d, gene_selection
from ._data_loader import SuematsuData
from ._go import go, gprofiler, get_go
from ._preference import (
    kwarg_savefig, eda_longitudinal_args, sgoa_longitudinal_args, 
    venn3_palette1, venn3_palette2, venn3_palette_alias,
    artist_pipeline_adgile, eda_pipeline_adgile, sgoa_pipeline_adgile,
    is_skippable
)
from ._eda import EDA
from ._stratification import StratifiedGOAnalysis
from ._schematic import Artist
from ._meta_pipeline import metapipeline


__all__ = [
    "SuematsuData",
    "eda_longitudinal_args",
    "kwarg_savefig",
    "sgoa_longitudinal_args",
    "venn3_palette1",
    "venn3_palette2",
    "venn3_palette_alias",
    "artist_pipeline_adgile",
    "eda_pipeline_adgile",
    "sgoa_pipeline_adgile",
    "is_skippable",
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

__author__ = """Yuji Okano"""
__version__ = "presubmission"
