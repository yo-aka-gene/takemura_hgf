import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import numpy as np
import pandas as pd
import seaborn as sns
from ._cohens_d import gene_selection
from ._data_loader import SuematsuData
from ._go import gprofiler
from ._preference import kwarg_savefig, venn3_palette_alias


class StratifiedGOAnalysis:
    def data_setter(self, data: SuematsuData, d: float, split_by_days: bool = False) -> dict:
        upa = gene_selection(
            data.data, data.group, regex="HGF+" if split_by_days else "day2", 
            d=d, flip=split_by_days
        )
        upb = gene_selection(
            data.data, data.group, regex="control" if split_by_days else "day7",
            d=d, flip=split_by_days
        )
        downa = gene_selection(
            data.data, data.group, regex="HGF+" if split_by_days else "day2",
            d=d, neg=True, flip=split_by_days
        )
        downb = gene_selection(
            data.data, data.group, regex="control" if split_by_days else "day7",
            d=d, neg=True, flip=split_by_days
        )
        return {
            "up": {
                "HGF+": upa.loc[[v for v in upa.index if v not in upb.index]],
                "HGF+ & control": upa.loc[[v for v in upa.index if v in upb.index]],
                "control": upb.loc[[v for v in upb.index if v not in upa.index]],
            },
            "down": {
                "HGF+": downa.loc[[v for v in downa.index if v not in downb.index]],
                "HGF+ & control": downa.loc[[v for v in downa.index if v in downb.index]],
                "control": downb.loc[[v for v in downb.index if v not in downa.index]],
            },
        } if split_by_days else {
            "up": {
                "day2": upa.loc[[v for v in upa.index if v not in upb.index]],
                "day2 & day7": upa.loc[[v for v in upa.index if v in upb.index]],
                "day7": upb.loc[[v for v in upb.index if v not in upa.index]],
            },
            "down": {
                "day2": downa.loc[[v for v in downa.index if v not in downb.index]],
                "day2 & day7": downa.loc[[v for v in downa.index if v in downb.index]],
                "day7": downb.loc[[v for v in downb.index if v not in downa.index]],
            },
        }


    def title_setter(self, split_by_days: bool = False) -> dict:
        return {
            "up": "upregulated GO terms through time cource",
            "down": "downregulated GO terms through time cource"
        } if split_by_days else {
            "up": "upregulated GO terms by HGF",
            "down": "downregulated GO terms by HGF"
        }


    def __init__(
            self,
            data: SuematsuData,
            d: float = .8,
            out: str = "/home/jovyan/out",
            palettes: tuple = ("plasma", "viridis"),
            split_by_days: bool = False
        ) -> None:
        self.data = self.data_setter(data=data, d=d, split_by_days=split_by_days)
        self.palette = {"up": palettes[0], "down": palettes[1]}
        self.venn3_palette = "palette1" if split_by_days else "palette2"
        self.title = self.title_setter(split_by_days=split_by_days)
        self.out = out
        self.result = {"up": {}, "down": {}}
        for category in self.data:
            for subcategory in self.data[category]:
                self.result[category] = {
                    **self.result[category], 
                    subcategory: gprofiler(self.data[category][subcategory])
                }


    def go_plot(
        self,
        category: str,
        subcategory: str,
        ax: plt.Axes = None,
        top: int = None,
        palette: str = None
    ):
        data = self.result[category][subcategory]
        top = min(len(data), top) if isinstance(top, int) else len(data)
        if ax is None:
            ysize = (lambda x: max(5, int(x / 5)))(top)
            _, ax = plt.subplots(figsize=(5, ysize))
        res = data.iloc[:top, :].iloc[::-1, :]
        res = pd.DataFrame({
            "term_name": res.term_name,
            "$-\log_{10}Pval.$": -np.log10(res.p_value),
            "Intersection size" :res.intersection_size,
            "gene_ratio": res.intersection_size / res.term_size
        })

        sns.scatterplot(
            data=res, 
            x="gene_ratio", 
            y="term_name", 
            size="Intersection size", 
            hue="$-\log_{10}Pval.$", 
            palette=palette,
            **{"edgecolor": ".2", "linewidth":.5}
        )

        ax.set_ylim(-.5, min(len(res), top) + .5)
        ax.set(ylabel="", xlabel="Gene Ratio")
        ax.legend(loc="center left", bbox_to_anchor=(1, .5))
        
        return ax


    def close(self) -> None:
        plt.close()


    def enrichment_analysis(
        self,
        figsize: tuple = None,
        top: int = 30
    ):
        for category in self.data:
            for subcategory in self.data[category]:
                fig, ax = plt.subplots(figsize=figsize)
                self.go_plot(
                    category=category,
                    subcategory=subcategory,
                    ax=ax,
                    top=top,
                    palette=self.palette[category]
                )
                ax.set_title(f"{self.title[category]} ({subcategory})")
                fig.savefig(
                    f"../out/go_{category}_{subcategory.replace(' & ', '+')}.png",
                    **kwarg_savefig
                )


    def silent_enrichment_analysis(
        self,
        figsize: tuple = None,
        top: int = 30
    ):
        for category in self.data:
            for subcategory in self.data[category]:
                fig, ax = plt.subplots(figsize=figsize)
                self.go_plot(
                    category=category,
                    subcategory=subcategory,
                    ax=ax,
                    top=top,
                    palette=self.palette[category]
                )
                ax.set_title(f"{self.title[category]} ({subcategory})")
                fig.savefig(
                    f"../out/go_{category}_{subcategory.replace(' & ', '+')}.png",
                    **kwarg_savefig
                )
                self.close()


    def go_venn_base(
        self,
        category: str,
        top: int = None,
        ax: plt.Axes = None,
        palette: str = None
    ) -> None:
        if ax is None:
            _, ax = plt.subplots()
        database = self.result[category]
        top = 100000 if top is None else top
        res = pd.concat(
            [
                pd.DataFrame(
                    (10 ** i) * np.ones(len(database[key])), 
                    index=database[key].term_name
                ).iloc[:top, :] for i, key in enumerate(database)
            ],
            axis=1
        ).fillna(0).sum(axis=1).value_counts().sort_index()
        v = venn3(
            subsets=[res[i] if i in res.index else 0 for i in [1, 10, 11, 100, 101, 110, 111]],
            set_labels = database.keys(),
            ax=ax
        )
        palette = venn3_palette_alias[2] if palette is None else venn3_palette_alias[palette]
        [v.get_patch_by_id(p).set_color(c) for p, c in palette.items() if v.get_patch_by_id(p) is not None]


    def top_go_venn(
        self,
        layout: tuple = (1, 2),
        figsize: tuple = (6, 3),
        top: int = 30
    ) -> None:
        fig, ax = plt.subplots(*layout, figsize=figsize)
        self.go_venn_base(category="up", top=top, ax=ax[0], palette=self.venn3_palette)
        self.go_venn_base(category="down", top=top, ax=ax[1], palette=self.venn3_palette)
        [a.set(title=f"{k}regulated GO terms (top{top})") for a, k in zip(ax, self.result)]
        suffix = "_".join(list(self.result["up"].keys())[::2])
        fig.savefig(f"{self.out}/go_venn_top{top}_{suffix}.png", **kwarg_savefig)


    def go_venn(
        self,
        layout: tuple = (1, 2),
        figsize: tuple = (6, 3),
        top: int = None
    ) -> None:
        fig, ax = plt.subplots(*layout, figsize=figsize)
        self.go_venn_base(category="up", top=top, ax=ax[0], palette=self.venn3_palette)
        self.go_venn_base(category="down", top=top, ax=ax[1], palette=self.venn3_palette)
        [a.set(title=f"{k}regulated GO terms (all)") for a, k in zip(ax, self.result)]
        suffix = "_".join(list(self.result["up"].keys())[::2])
        fig.savefig(f"{self.out}/go_venn_all_{suffix}.png", **kwarg_savefig)


    def pipeline(
        self, 
        pipe: list = [
            "silent_enrichment_analysis",
            "top_go_venn",
            "go_venn"
        ],
        close: bool = False
    ) -> None:
        for operation in pipe:
            eval(f"self.{operation}()")
            self.close() if close else None
