import matplotlib.pyplot as plt
import matplotlib.patches as patch
import numpy as np
import pandas as pd
import seaborn as sns
from tools import kwarg_savefig


def base_scheme(ax: plt.Axes) -> None:
    dat = pd.DataFrame({
        "x": np.array(([0] * 4 + [1] * 4) * 2) + np.tile(0.1 * np.cos(np.pi * np.linspace(1/6, 10/6, 4)), 4),
        "y": np.array([0] * 8 + [1] * 8) + np.tile(0.1 * np.sin(np.pi * np.linspace(1/6, 10/6, 4)), 4),
        "day": np.array((["2"] * 4 + ["7"] * 4) * 2),
        "HGF": np.array(["–"] * 8 + ["+"] * 8)
    })
    sns.scatterplot(dat, x="x", y="y", hue="HGF", style="day", s=100, ax=ax)
    ax.set_xlim([-.3, 1.3]), ax.set_ylim([-.3, 1.3])
    ax.set(xlabel="Time Cource", ylabel="Experimental Condition")
    ax.set_xticks([0, 1], ["day2", "day7"])
    ax.set_yticks([0, 1], ["control", "HGF+"])
    ax.get_legend().remove()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)


def schematic(
    layout: tuple,
    figsize: tuple,
    wspace: float
) -> tuple:
    fig, ax = plt.subplots(*layout, figsize=figsize)
    plt.subplots_adjust(wspace=wspace)
    [base_scheme(a) for a in ax];

    as1 = {
        "arrowstyle": "<->",
        "connectionstyle": "arc3", 
        "facecolor": ".2",
        "edgecolor": ".2"
    }

    as2 = {
        "arrowstyle": "-|>",
        "connectionstyle": "arc3"
    }

    ax[0].add_patch(patch.Circle(xy=(.35, .8), radius=.2, ec="r", fc="r", alpha=.3))
    ax[0].add_patch(patch.Circle(xy=(.35, .2), radius=.2, ec="b", fc="b", alpha=.3))
    ax[0].add_patch(patch.Rectangle(xy=(.5, .65), width=np.sqrt(2)/5, height=np.sqrt(2)/5, rotation_point="center", angle=45, ec="r", fc="r", alpha=.3))
    ax[0].add_patch(patch.Rectangle(xy=(.5, .05), width=np.sqrt(2)/5, height=np.sqrt(2)/5, rotation_point="center", angle=45, ec="b", fc="b", alpha=.3))
    ax[0].add_patch(patch.Circle(xy=(0, .5), radius=.05, ec=".2", fc=".2", alpha=1))
    ax[0].add_patch(patch.Rectangle(xy=(.957, .46), width=.13/np.sqrt(2), height=.13/np.sqrt(2), rotation_point="center", angle=45, ec=".2", fc=".2"))
    ax[0].annotate('', xy=(.65, .8), xytext=(.35, .8), arrowprops={**as2, "color": "r"})
    ax[0].annotate('', xy=(.65, .2), xytext=(.35, .2), arrowprops={**as2, "color": "b"})
    ax[0].annotate('', xy=(0, .2), xytext=(0, .8), arrowprops=as1)
    ax[0].annotate('', xy=(1, .2), xytext=(1, .8), arrowprops=as1)
    ax[0].text(.5, 1.1, "upregulated", horizontalalignment="center", verticalalignment="center", c="r")
    ax[0].text(.5, -.1, "downregulated", horizontalalignment="center", verticalalignment="center", c="b")
    ax[0].text(.5, .5, "longitudal transition", horizontalalignment="center", verticalalignment="center", c=".2")
    ax[0].set(title="Temporal Changes of HGF's Effect")


    ax[1].add_patch(patch.Circle(xy=(.2, .65), radius=.2, ec="b", fc="b", alpha=.3))
    ax[1].add_patch(patch.Circle(xy=(.2, .35), radius=.2, ec="b", fc="b", alpha=.3))
    ax[1].add_patch(patch.Rectangle(xy=(.655, .50), width=np.sqrt(2)/5, height=np.sqrt(2)/5, rotation_point="center", angle=45, ec="r", fc="r", alpha=.3))
    ax[1].add_patch(patch.Rectangle(xy=(.655, .22), width=np.sqrt(2)/5, height=np.sqrt(2)/5, rotation_point="center", angle=45, ec="r", fc="r", alpha=.3))
    ax[1].annotate('', xy=(.2, 0), xytext=(.8, 0), arrowprops=as1)
    ax[1].annotate('', xy=(.2, 1), xytext=(.8, 1), arrowprops=as1)
    ax[1].annotate('', xy=(.2, .49), xytext=(.2, .65), arrowprops={**as2, "color": "b"})
    ax[1].annotate('', xy=(.2, .51), xytext=(.2, .35), arrowprops={**as2, "color": "b"})
    ax[1].annotate('', xy=(.8, .49), xytext=(.8, .65), arrowprops={**as2, "color": "r"})
    ax[1].annotate('', xy=(.8, .51), xytext=(.8, .35), arrowprops={**as2, "color": "r"})
    ax[1].add_patch(patch.Rectangle(xy=(.45, .95), width=.1, height=.1, ec="C1", fc="C1", zorder=3))
    ax[1].add_patch(patch.Rectangle(xy=(.45, -.05), width=.1, height=.1, ec="C0", fc="C0", zorder=4))
    ax[1].text(1.1, .5, "up-\nregulated", horizontalalignment="center", verticalalignment="center", c="r")
    ax[1].text(-.1, .5, "down-\nregulated", horizontalalignment="center", verticalalignment="center", c="b")
    ax[1].text(.5, .5, "baseline\nchanges", horizontalalignment="center", verticalalignment="center", c=".2")
    ax[1].set(title="Consistency of Cellular Dynamics")
    return fig, ax


class Artist:
    def __init__(self, out: str = "/home/jovyan/out", args: dict = {}):
        self.out = out
        self.args = args


    def fetch(self, argname: str, arg):
        return self.args[argname] if argname in self.args else arg


    def comparison_schematic(
        self,
        layout: tuple = (1, 2),
        figsize: tuple = (10, 4),
        wspace: float = .4
    ):
        fig, _ = schematic(layout=layout, figsize=figsize, wspace=wspace)
        fig.savefig(f"{self.out}/comparison_schematic.png", **kwarg_savefig)


    def close(self) -> None:
        plt.close()


    def pipeline(self, pipe: list = ["comparison_schematic"], close: bool = False) -> None:
        pipe = self.fetch("pipe", pipe)
        for operation in pipe:
            eval(f"self.{operation}()")
            self.close() if close else None