from tempfile import TemporaryDirectory
import pandas as pd
import subprocess
import os


def go(data: pd.DataFrame):
    tempdir = TemporaryDirectory()
    data.index = data.index.str.upper()
    data.to_csv(f"{tempdir.name}/data.csv", index=True)
    cmd = f"Rscript {os.path.dirname(__file__)}/_go_pipeline.R -t {tempdir.name}"
    subprocess.call(cmd.split())
    ret = pd.read_csv(f"{tempdir.name}/enrichment.csv", index_col=0)
    tempdir.cleanup()
    return ret


def gprofiler(data: pd.DataFrame):
    tempdir = TemporaryDirectory()
    data.to_csv(f"{tempdir.name}/data.csv", index=True)
    cmd = f"Rscript {os.path.dirname(__file__)}/_gprofiler_pipeline.R -t {tempdir.name}"
    subprocess.call(cmd.split())
    ret = pd.read_csv(f"{tempdir.name}/enrichment.csv", index_col=0)
    tempdir.cleanup()
    return ret


def get_go(data: pd.DataFrame):
    tempdir = TemporaryDirectory()
    data.to_csv(f"{tempdir.name}/data.csv", index=True)
    cmd = f"Rscript {os.path.dirname(__file__)}/_get_go.R -t {tempdir.name}"
    subprocess.call(cmd.split())
    ret = pd.read_csv(f"{tempdir.name}/genelist.csv", index_col=0)
    tempdir.cleanup()
    return ret
