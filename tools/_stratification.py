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
        up2 = gene_selection(data.data, data.group, regex="day2", d=d)
        up7 = gene_selection(data.data, data.group, regex="day7", d=d)
        down2 = gene_selection(data.data, data.group, regex="day2", d=d, neg=True)
        down7 = gene_selection(data.data, data.group, regex="day7", d=d, neg=True)
        return {
            "day2": {
                "up": up2.loc[[v for v in up2.index if v not in down2.index]],
                "up & down": up2.loc[[v for v in up2.index if v in down2.index]],
                "down": down2.loc[[v for v in down2.index if v not in up2.index]],
            },
            "day7": {
                "up": up7.loc[[v for v in up7.index if v not in down7.index]],
                "up & down": up7.loc[[v for v in up7.index if v in down7.index]],
                "down": down7.loc[[v for v in down7.index if v not in up7.index]],
            },
        } if split_by_days else {
            "up": {
                "day2": up2.loc[[v for v in up2.index if v not in up7.index]],
                "day2 & day7": up2.loc[[v for v in up2.index if v in up7.index]],
                "day7": up7.loc[[v for v in up7.index if v not in up2.index]],
            },
            "down": {
                "day2": down2.loc[[v for v in down2.index if v not in down7.index]],
                "day2 & day7": down2.loc[[v for v in down2.index if v in down7.index]],
                "day7": down7.loc[[v for v in down7.index if v not in down2.index]],
            },
        }


    def palette_setter(self, palettes: tuple, split_by_days: bool = False) -> dict:
        return {
            "day2": palettes[0],
            "day7": palettes[1],
        } if split_by_days else {
            "up": palettes[0],
            "down": palettes[1],
        }


    def title_setter(self, split_by_days: bool = False) -> dict:
        return {
            "day2": "GO terms",
            "day7": "Go terms",
        } if split_by_days else {
            "up": "upregulated GO terms",
            "down": "downregulated GO terms",
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
        self.palette = self.palette_setter(palettes=palettes, split_by_days=split_by_days)
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

        ax.set_ylim(-.5, top + .5)
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
