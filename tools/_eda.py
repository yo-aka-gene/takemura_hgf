import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from ._cohens_d import cohens_d, gene_selection
from ._data_loader import SuematsuData
from ._preference import kwarg_savefig


class EDA:
    def __init__(self, data: SuematsuData, out: str = "/home/jovyan/out") -> None:
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
        flip: bool = False,
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
                "cohens_d": cohens_d(self.data.data, self.data.group, regex=regex, flip=flip).fillna(0),
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
                v for v in self.data.data.groupby(self.data.group).count().filter(axis=0, regex=regex).index
            ])
        )
        ax.legend()
        return ax


    def butterfly_plot(
        self,
        set_labels: tuple = ("day2", "day7"),
        layout: tuple = (2, 1),
        figsize: tuple = (6, 6),
        hspace: float = .4,
        d: float = .8,
        flip: bool = False,
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
                regex=r, ax=a, d=d, flip=flip, dim_idx=dim_idx,
                idx_starts_with=idx_starts_with,
                palette=palette, s=s, alpha=alpha
            ) for r, a in zip(set_labels, ax)
        ]
        fig.savefig(f"{self.out}/butterfly_plot_{set_labels[0]}_{set_labels[1]}.png", **kwarg_savefig)


    def gr_venn(
        self,
        set_labels: tuple,
        ax: plt.Axes = None,
        d: float = .8,
        neg: bool = False,
        flip: bool = False,
        set_colors: tuple = ("C0", "C2", "C1")
    ) -> None:
        if ax is None:
            _, ax = plt.subplots()
        a_genes = gene_selection(
            self.data.data, self.data.group,
            regex=set_labels[0], d=d, neg=neg, flip=flip
        ).index
        b_genes = gene_selection(
            self.data.data, self.data.group,
            regex=set_labels[1], d=d, neg=neg, flip=flip
        ).index
        n_intersection = len([v for v in a_genes if v in b_genes])
        v = venn2(
            subsets=(len(a_genes) - n_intersection, len(b_genes) - n_intersection, n_intersection),
            set_labels = set_labels,
            ax=ax
        )
        [v.get_patch_by_id(p).set_color(c) for p, c in zip(["10", "01", "11"], set_colors)]
        ax.set(title=f"{'down' if neg else 'up'}regulated genes")
        return ax


    def gene_regulation_venn_diagram(
        self,
        layout: tuple = (1, 2),
        figsize: tuple = (6, 3),
        set_labels: tuple = ("day2", "day7"),
        set_colors: tuple = ("m", "y", "grey"),
        flip: bool = False
    ) -> None:
        fig, ax = plt.subplots(*layout, figsize=figsize)
        self.gr_venn(set_labels=set_labels, ax=ax[0], set_colors=set_colors, flip=flip)
        self.gr_venn(set_labels=set_labels, ax=ax[1], neg=True, set_colors=set_colors, flip=flip)
        fig.savefig(f"{self.out}/venn_{set_labels[0]}_{set_labels[1]}.png", **kwarg_savefig)


    def close(self) -> None:
        plt.close()


    def pipeline(
        self,
        pipe: list = [
            "scatter_plot",
            "component_plot",
            "butterfly_plot", 
            "gene_regulation_venn_diagram"
        ], 
        close: bool = False
    ) -> None:
        for operation in pipe:
            eval(f"self.{operation}()")
            self.close() if close else None
