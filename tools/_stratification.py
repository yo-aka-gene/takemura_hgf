import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from ._cohens_d import gene_selection
from ._data_loader import SuematsuData
from ._go import gprofiler
from ._preference import kwarg_savefig


class StratifiedGOAnalysis:
    def data_setter(self, data: SuematsuData, d: float, split_by_days: bool = False) -> dict:
        upa = gene_selection(data.data, data.group, regex="HGF+" if split_by_days else "day2", d=d)
        upb = gene_selection(data.data, data.group, regex="control" if split_by_days else "day7", d=d)
        downa = gene_selection(data.data, data.group, regex="HGF+" if split_by_days else "day2", d=d, neg=True)
        downb = gene_selection(data.data, data.group, regex="control" if split_by_days else "day7", d=d, neg=True)
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
        self.title = self.title_setter(split_by_days=split_by_days)
        self.out = out


    def go_plot(
        self,
        data: pd.DataFrame,
        ax: plt.Axes = None,
        top: int = None,
        palette: str = None
    ):
        top = min(len(data), top) if isinstance(top, int) else len(data)
        if ax is None:
            ysize = (lambda x: max(5, int(x / 5)))(top)
            _, ax = plt.subplots(figsize=(5, ysize))
        
        res = gprofiler(data).iloc[:top, :].iloc[::-1, :]
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
                    data=self.data[category][subcategory],
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
                    data=self.data[category][subcategory],
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


    def pipeline(
        self, 
        pipe: list = ["silent_enrichment_analysis"],
        close: bool = False
    ) -> None:
        for operation in pipe:
            eval(f"self.{operation}()")
            self.close() if close else None
