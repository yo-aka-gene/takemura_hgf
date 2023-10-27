def metapipeline(pipelines: list, close: bool = True):
    for p in pipelines:
        p.pipeline(close=close)
