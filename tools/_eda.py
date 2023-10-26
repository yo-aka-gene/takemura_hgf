import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from ._cohens_d import cohens_d
from ._data_loader import SuematsuData
from ._preference import kwarg_savefig


class EDA:
    def __init__(self, data: SuematsuData, out: str = "home/jovyan/out") -> None:
        self.data = data
        self.model= PCA(random_state=0)
        self.pca = pd.DataFrame(
            self.model.fit_transform(data.data),
            index=data.index,
            columns=[f"PC{i + 1}" for i in range(min(data.shape))]
        )
        self.out = out

    def scatter_plot(self, figsize: tuple = (3, 3)) -> None:
        fig, ax = plt.subplots(figsize=figsize)
        sns.scatterplot(
            data=self.pca, x="PC1", y="PC2", 
            style=self.data.meta.day, 
            hue=self.data.meta.condition,
            ax=ax, s=15
        )
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
        ax.set_xlim([min(xlim[0], ylim[0]), max(xlim[1], ylim[1])])
        ax.set_ylim([min(xlim[0], ylim[0]), max(xlim[1], ylim[1])])
        ax.legend(bbox_to_anchor=(1, .5), loc="center left")
        ax.set_xlabel(f"PC1 ({(self.model.explained_variance_ratio_[0] * 100).round(3)}%)")
        ax.set_ylabel(f"PC2 ({(self.model.explained_variance_ratio_[1] * 100).round(3)}%)")
        ax.set(title="RNA-seq data\n(Suematsu Y, et al., $Inflamm\; Regener$, 2023)")
        fig.savefig(f"{self.out}/pca.png", **kwarg_savefig)


    def component_visualizer(
        self,
        ax: plt.Axes = None,
        top: int = 30,
        dim_idx: int = 0,
        idx_starts_with: int = 1,
        color: str = None
    ) -> None:
        if ax is None:
            _, ax = plt.subplots()
        comp = pd.DataFrame(
            self.model.components_[dim_idx],
            index=self.data.columns, 
            columns=["components"]
        ).sort_values("components", ascending=False)
        top = min(top, len(comp))
        sns.barplot(data=comp.iloc[:top, :], x=comp.index[:top], y=comp.components[:top], ax=ax, color=color)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        ax.set(title=f"PC{dim_idx + idx_starts_with}")


    def component_plot(
        self,
        layout: tuple = (1, 2),
        figsize: tuple = (10, 3),
        top: int = 30,
        idx_starts_with: int = 1,
        color: str = ".2"
    ) -> None:
        fig, ax = plt.subplots(*layout, figsize=figsize)
        [
            self.component_visualizer(
                ax=ax[i], dim_idx=i, color=color, top=top,
                idx_starts_with=idx_starts_with
            ) for i in range(2)
        ]
        fig.savefig(f"{self.out}/components.png", **kwarg_savefig)


    def comp_by_d(
        self,
        regex: str,
        ax: plt.Axes = None,
        d: float = .8,
        dim_idx: int = 0,
        idx_starts_with: int = 1,
        palette: str = "coolwarm",
        s: float = 5,
        alpha: float = .1,
    ) -> None:
        if ax is None:
            _, ax = plt.subplots()
        dat = pd.DataFrame(
            {
                "cohens_d": cohens_d(self.data.data, self.data.group, regex=regex).fillna(0),
                "components": self.model.components_[dim_idx]
            },
            index=self.data.columns
        )
        sns.scatterplot(
            data=dat, x="cohens_d", y="components", ax=ax, hue="cohens_d",
            palette=palette, s=s, legend=False, edgecolor=".2"
        )
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
        [
            ax.vlines(
                thresh, *ylim, linewidth=1, color=".2", 
                label="$\pm$" + f"{d}" if thresh > 0 else None 
            ) for thresh in [d, -d]
        ]
        [
            ax.fill_between(
                np.linspace(thresh, lim, 1000), *ylim,
                alpha=alpha, zorder=0, color="b" if thresh < 0 else "r",
                label=f"{'up' if thresh > 0 else 'down'} ({(dat.cohens_d > d).sum() if thresh > 0 else (dat.cohens_d < -d).sum()})"
            ) for thresh, lim in zip(xlim, (-d, d))
        ]
        ax.set_xlim(*xlim), ax.set_ylim(*ylim)
        ax.set(
            ylabel=f"PC{dim_idx + idx_starts_with} components", 
            xlabel="Cohen's d",
            title=' vs '.join([
                v for v in self.data.groupby(self.group).count().filter(axis=0, regex=regex).index
            ])
        )
        ax.legend()
        return ax


    def butterfly_plot(
        self,
        layout: tuple = (2, 1),
        figsize: tuple = (6, 6),
        hspace: float = .4,
        d: float = .8,
        dim_idx: int = 1,
        idx_starts_with: int = 1,
        palette: str = "coolwarm",
        s: float = 5,
        alpha: float = .1,
    ) -> None:
        fig, ax = plt.subplots(*layout, figsize=figsize)
        fig.subplots_adjust(hspace=hspace)
        [
            self.comp_by_d(
                regex=f"day{day}", ax=a, d=d, dim_idx=dim_idx,
                idx_starts_with=idx_starts_with,
                palette=palette, s=s, alpha=alpha
            ) for day, a in zip([2, 7], ax)
        ]
        fig.savefig(f"{self.out}/regulation_plot.png", **kwarg_savefig)