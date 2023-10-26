class MetaPipeline:
    def __init__(self, pipelines: list, close: bool = True):
        for p in pipelines:
            p.pipeline(close=close)
