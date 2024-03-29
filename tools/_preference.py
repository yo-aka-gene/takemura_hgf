from typing import Union
import glob
import numpy as np


kwarg_savefig = {
    "facecolor": "white",
    "dpi": 300,
    "bbox_inches": "tight",
    "pad_inches": 0.05,
    "transparent": True,
}


eda_longitudinal_args = {
    "split_by_days": True,
    "set_labels": ("HGF+", "control"),
    "dim_idx": 0,
    "flip": True,
    "set_colors": ("C1", "C0", "C2"),
    "pipe": ["butterfly_plot", "gene_regulation_venn_diagram"]
}


sgoa_longitudinal_args = {
    "palettes": ("magma", "cividis"),
    "split_by_days": True
}


venn3_palette1 = {
    # matplotlib-like theme
    "100": "#ff7f0e",
    "010": "#2ca02c",
    "001": "#1f77b4",
    "110": "#b4b40e",
    "011": "#2ca0b4",
    "101": "#ffa0b4",
    "111": "#eeeeee"
}


venn3_palette2 = {
    # seurat-like theme
    "100": "#bbbb11",
    "010": "#777777",
    "001": "#bb11bb",
    "110": "#bbaa77",
    "011": "#aa77bb",
    "101": "#bbaabb",
    "111": "#eeeeee"
}


venn3_palette_alias = {
    "palette1": venn3_palette1,
    "palette2": venn3_palette2,
    "venn3_palette1": venn3_palette1,
    "venn3_palette2": venn3_palette2,
    1: venn3_palette1,
    2: venn3_palette2
}


def intersection_name(arg: Union[tuple, bool]) -> str:
    assert isinstance(arg, (bool, tuple)), \
        f"Invalid input type: expected tuple or bool, got {arg}[{type(arg)}]"
    namespace = [
        "Const.", #intersection of day2 and day7
        "com.", #intersection of HGF+ and control
    ]
    arg = "HGF+" in "".join(arg) if isinstance(arg, tuple) else arg
    return namespace[arg]


def path_exists(regex: str, require: int = None) -> bool:
    return (
        len(glob.glob(regex)) != 0
    ) if require is None else (
        len(glob.glob(regex)) == require
    )


def is_skippable(adgile_dict: dict, *args) -> bool:
    return np.all([b for b in {k: v(*args) for k, v in adgile_dict.items()}.values()])


artist_pipeline_adgile = {
    "comparison_schematic": lambda o: path_exists(
        regex=f"{o}/comparison_schematic.png"
    ),
    "time_variation": lambda o: path_exists(
        regex=f"{o}/time_variation.png"
    ),
    "analogical_schematic": lambda o: path_exists(
        regex=f"{o}/analogical_schematic.png"
    ),
}


eda_pipeline_outputs = {
    "scatter_plot": lambda o, _: f"{o}/pca.png",
    "component_plot": lambda o, _: f"{o}/components.png",
    "butterfly_plot": lambda o, c: f"{o}/butterfly_plot_{c}.png",
    "gene_regulation_venn_diagram": lambda o, c: f"{o}/venn_{c}.png",
}


eda_pipeline_args = {
    "scatter_plot": lambda _: (None,),
    "component_plot": lambda _: (None,),
    "butterfly_plot": lambda spbd: ("H*",) if spbd else ("day*",),
    "gene_regulation_venn_diagram": lambda spbd: ("H*",) if spbd else ("day*",),
}


eda_pipeline_adgile = {
    "scatter_plot": lambda o, spbd: path_exists(
        regex=eda_pipeline_outputs["scatter_plot"](
            o, *eda_pipeline_args["scatter_plot"](spbd)
        )
    ),
    "component_plot": lambda o, spbd: path_exists(
        regex=eda_pipeline_outputs["component_plot"](
            o, *eda_pipeline_args["component_plot"](spbd)
        )
    ),
    "butterfly_plot": lambda o, spbd: path_exists(
        regex=eda_pipeline_outputs["butterfly_plot"](
            o, *eda_pipeline_args["butterfly_plot"](spbd)
        )
    ),
    "gene_regulation_venn_diagram": lambda o, spbd: path_exists(
        regex=eda_pipeline_outputs["gene_regulation_venn_diagram"](
            o, *eda_pipeline_args["gene_regulation_venn_diagram"](spbd)
        )
    ),
}


sgoa_pipeline_outputs = {
    "silent_enrichment_analysis": lambda o, sc: f"{o}/go_[ud]*_{sc}.png",
    "top_go_venn": lambda o, suf: f"{o}/go_venn_top*_{suf}.png",
    "go_venn": lambda o, suf: f"{o}/go_venn_all_{suf}.png",
    "silent_go2gene_barplot": lambda o, fid, t, suf: f"{o}/go_barplot_[ud]*_{fid}_{t}_{suf}.png"
}


sgoa_pipeline_args = {
    "silent_enrichment_analysis": lambda spbd: (("[Hc]*",) if spbd else ("[dC]*",)),
    "top_go_venn": lambda spbd: (("H*",) if spbd else ("day*",)),
    "go_venn": lambda spbd: (("H*",) if spbd else ("day*",)),
    "silent_go2gene_barplot": lambda spbd: ((10, "top30", "H*") if spbd else (111, "top30", "day*"))
}


sgoa_pipeline_adgile = {
    "silent_enrichment_analysis": lambda o, spbd: path_exists(
        regex=sgoa_pipeline_outputs["silent_enrichment_analysis"](
            o, *sgoa_pipeline_args["silent_enrichment_analysis"](spbd)
        ),
        require=6
    ),
    "top_go_venn": lambda o, spbd: path_exists(
        regex=sgoa_pipeline_outputs["top_go_venn"](
            o, *sgoa_pipeline_args["top_go_venn"](spbd)
        ),
        require=None
    ),
    "go_venn": lambda o, spbd: path_exists(
        regex=sgoa_pipeline_outputs["go_venn"](
            o, *sgoa_pipeline_args["go_venn"](spbd)
        ),
        require=None
    ),
    "silent_go2gene_barplot": lambda o, spbd: path_exists(
        regex=sgoa_pipeline_outputs["silent_go2gene_barplot"](
            o, *sgoa_pipeline_args["silent_go2gene_barplot"](spbd)
        ),
        require=2
    )
}
