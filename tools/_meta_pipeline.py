def metapipeline(
    pipelines: list,
    close: bool = True,
    adgile: bool =True
) -> None:
    for p in pipelines:
        p.pipeline(close=close, adgile=adgile)
