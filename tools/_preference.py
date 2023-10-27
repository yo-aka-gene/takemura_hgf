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
