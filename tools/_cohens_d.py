import numpy as np
import pandas as pd


def cohens_d(data: pd.DataFrame, group: pd.Series, regex: str):
    df_group = data.groupby(group)
    n = df_group.count().filter(axis=0, regex=regex)
    s = df_group.std(ddof=0).filter(axis=0, regex=regex)
    xbar = df_group.mean().filter(axis=0, regex=regex)
    return xbar.iloc[::-1, :].diff().iloc[1, :] / np.sqrt((n * s).sum() / n.sum())


def gene_selection(data: pd.DataFrame, group: pd.Series, regex: str, d: float = .8, neg: bool = False):
    ret = cohens_d(data=data, group=group, regex=regex).dropna().sort_values(ascending=neg)
    return ret[ret > d] if not neg else ret[ret < -d]
