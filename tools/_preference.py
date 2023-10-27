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
    "set_colors": ("C0", "C1", "C2"),
    "pipe": ["butterfly_plot", "gene_regulation_venn_diagram"]
}


sgoa_longitudal_args = {
    "palettes": ("magma", "cividis"),
    "split_by_days": True
}


venn3_palette1 = {
    # matplotlib-like theme
    "100": "#1f77b4",
    "010": "#2ca02c",
    "001": "#ff7f0e",
    "110": "#2ca0b4",
    "011": "#b4b40e",
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
