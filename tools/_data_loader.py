import io
import requests
import pandas as pd
from typing import NamedTuple


class Data(NamedTuple):
    data: pd.DataFrame
    meta: pd.DataFrame


class SuematsuData:
    def __init__(
            self, 
            data_path: str = "https://drive.google.com/file/d/1-CyJhEb3kkkcM6pvJ7Hg5PGt7Abn2jON/view?usp=drive_link",
            meta_path: str = "https://drive.google.com/file/d/1-7DJJQLLEaOyzmoLpw8jRz8ZgX8-Gnzb/view?usp=drive_link"
    ) -> None:
        preffix = "https://drive.google.com/uc?id="
        invalid_preffix = "https://drive.google.com/file/d/"
        fmt = lambda x: x if preffix in x else preffix + x.split(invalid_preffix)[1].split("/")[0]
        data_req, meta_req = requests.get(fmt(data_path)), requests.get(fmt(meta_path))
        self.structure = Data(
            data=pd.read_csv(io.BytesIO(data_req.content), sep=",", index_col=0),
            meta=pd.read_csv(io.BytesIO(meta_req.content), sep=",", index_col=0),
        )
        self.data = self.structure.data
        self.meta = self.structure.meta
        self.req = {"data": fmt(data_path), "meta": fmt(meta_path)}
        self.index = self.data.index
        self.columns = self.data.columns
        self.shape = self.data.shape
