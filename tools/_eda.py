import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from ._cohens_d import cohens_d, gene_selection
from ._data_loader import SuematsuData
from ._preference import kwarg_savefig, eda_pipeline_adgile, is_skippable


class EDA:
    def __init__(
        self, data: SuematsuData,
        out: str = "/home/jovyan/out",
        adgile: bool = False,
        args: dict = {}
    ) -> None:
        self.out = out
        self.args = args if "split_by_days" in args else {"split_by_days": False}
        if not (adgile and is_skippable(eda_pipeline_adgile, out, self.args["split_by_days"])):
            self.data = data
            self.model= PCA(random_state=0)
            self.pca = pd.DataFrame(
                self.model.fit_transform(data.data),
                index=data.index,
                columns=[f"PC{i + 1}" for i in range(min(data.shape))]
            )


    def fetch(self, argname: str, arg):
        return self.args[argname] if argname in self.args else arg


    def scatter_plot(self, figsize: tuple = (3, 3), **kwargs) -> None:
        fig, ax = plt.subplots(figsize=figsize)
        sns.scatterplot(
            data=self.pca, x="PC1", y="PC2", 
            style=self.data.meta.day, 
            hue=self.data.meta.condition,
            ax=ax, s=40, **kwargs
        )
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
        ax.set_xlim([min(xlim[0], ylim[0]), max(xlim[1], ylim[1])])
        ax.set_ylim([min(xlim[0], ylim[0]), max(xlim[1], ylim[1])])
        ax.legend(bbox_to_anchor=(1, .5), loc="center left")
        ax.set_xlabel(f"PC1 ({(self.model.explained_variance_ratio_[0] * 100).round(3)}%)")
        ax.set_ylabel(f"PC2 ({(self.model.explained_variance_ratio_[1] * 100).round(3)}%)")
        ax.set(title=r"RNA-seq data ($n=4\times4$)"+"\n(Suematsu Y, et al., $Inflamm\; Regen.$, 2023)")
        fig.savefig(f"{self.out}/pca.png", **kwarg_savefig)


    def component_visualizer(
        self,
        ax: plt.Axes = None,
        top: int = 30,
        show_bottom: bool = False,
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
        title_suffix = f"top{top - top // 2} vs bottom{top // 2}" if show_bottom else f"top{top}"
        top = np.arange(top - top // 2).tolist() + (-np.arange(1, top // 2)).tolist()[::-1] if show_bottom else top
        comp = comp.iloc[top, :] if show_bottom else comp.iloc[:top, :]
        sns.barplot(data=comp, x=comp.index, y=comp.components, ax=ax, color=color)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        ax.set(title=f"PC{dim_idx + idx_starts_with} ({title_suffix})")


    def component_plot(
        self,
        layout: tuple = (1, 2),
        figsize: tuple = (10, 3),
        top: int = 30,
        show_bottom: bool = True,
        idx_starts_with: int = 1,
        color: str = ".2"
    ) -> None:
        fig, ax = plt.subplots(*layout, figsize=figsize)
        [
            self.component_visualizer(
                ax=ax[i], dim_idx=i, color=color, top=top, show_bottom=show_bottom,
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
        pair = [
            v for v in self.data.data.groupby(self.data.group).count().filter(axis=0, regex=regex).index
        ]
        ax.set_xlim(*xlim), ax.set_ylim(*ylim)
        ax.set(
            ylabel=f"PC{dim_idx + idx_starts_with} components", 
            xlabel="Cohen's d",
            title=' vs '.join(pair[::-1] if flip else pair)
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
        set_labels = self.fetch("set_labels", set_labels)
        dim_idx = self.fetch("dim_idx", dim_idx)
        flip = self.fetch("flip", flip)
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
        set_colors: tuple = ("C0", "C2", "C1"),
        footnote: bool = False
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
        if footnote:
            pair = lambda label: [
                v for v in self.data.data.groupby(self.data.group).count().filter(axis=0, regex=label).index
            ]
            footnote = "\n".join([
                f"{l}: {' vs '.join(pair(l)[::-1] if flip else pair(l))}" for l in set_labels
            ])
            ax.text(
                0, -.8, footnote, size="x-small",
                horizontalalignment="center", verticalalignment="center"
            )
        return ax


    def gene_regulation_venn_diagram(
        self,
        layout: tuple = (1, 2),
        figsize: tuple = (6, 3),
        set_labels: tuple = ("day2", "day7"),
        set_colors: tuple = ("y", "m", "grey"),
        flip: bool = False,
        footnote: bool = True
    ) -> None:
        fig, ax = plt.subplots(*layout, figsize=figsize)
        set_labels = self.fetch("set_labels", set_labels)
        set_colors = self.fetch("set_colors", set_colors)
        flip = self.fetch("flip", flip)
        self.gr_venn(set_labels=set_labels, ax=ax[0], set_colors=set_colors, flip=flip, footnote=footnote)
        self.gr_venn(set_labels=set_labels, ax=ax[1], neg=True, set_colors=set_colors, flip=flip, footnote=footnote)
        fig.savefig(f"{self.out}/venn_{set_labels[0]}_{set_labels[1]}.png", **kwarg_savefig)


    def close(self) -> None:
        plt.close()


    def pipeline(
        self,
        pipe: list = eda_pipeline_adgile.keys(), 
        close: bool = False,
        adgile: bool = False,
    ) -> None:
        pipe = self.fetch("pipe", pipe)
        spbd = self.fetch("split_by_days", False)
        for operation in pipe:
            if not (adgile and eda_pipeline_adgile[operation](self.out, spbd)):
                eval(f"self.{operation}()")
                self.close() if close else None
