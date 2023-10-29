import glob


kwarg_savefig = {
    "facecolor": "white",
    "dpi": 300,
    "bbox_inches": "tight",
    "pad_inches": 0.05,
    "transparent": True,
}


eda_longitudal_args = {
    "set_labels": ("HGF+", "control"),
    "dim_idx": 0,
    "flip": True,
    "set_colors": ("C1", "C0", "C2"),
    "pipe": ["butterfly_plot", "gene_regulation_venn_diagram"]
}


sgoa_longitudal_args = {
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


def path_exists(regex: str, require: int = None) -> bool:
    return (
        len(glob.glob(regex)) != 0
    ) if require is None else (
        len(glob.glob(regex)) == require
    )


sgoa_pipeline_outputs = {
    "silent_enrichment_analysis": lambda o, sc: f"{o}/go_[ud]*_{sc}.png",
    "top_go_venn": lambda o, suf: f"{o}/go_venn_top*_{suf}.png",
    "go_venn": lambda o, suf: f"{o}/go_venn_all_{suf}.png",
    "go2gene_barplot": lambda o, fid, t, suf: f"{o}/go_barplot_[ud]*_{fid}_{t}_{suf}.png"
}


sgoa_pipeline_args = {
    "silent_enrichment_analysis": lambda spbd: (("[Hc]*",) if spbd else ("day*",)),
    "top_go_venn": lambda spbd: (("H*",) if spbd else ("day*",)),
    "go_venn": lambda spbd: (("H*",) if spbd else ("day*",)),
    "go2gene_barplot": lambda spbd: ((10, 30, "H*") if spbd else (111, 30, "day*"))
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
    "go2gene_barplot": lambda o, spbd: path_exists(
        regex=sgoa_pipeline_outputs["go2gene_barplot"](
            o, *sgoa_pipeline_args["go2gene_barplot"](spbd)
        ),
        require=None
    )
}
