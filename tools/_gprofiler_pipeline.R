### _gprofiler_pipeline.R ###

suppressPackageStartupMessages({
    library(optparse)
    source("/home/jovyan/tools/_gprofiler.R")
})

optslist <- list(
    make_option(
        c("-t", "--tempdir"),
        type="character",
        default="/home/jovyan/out",
        help="temporary directory to save intermediate files"
    )
)
parser <- OptionParser(option_list=optslist)
opts <- parse_args(parser)

go.result <- egost(gene=gene_loader(paste0(opts$tempdir, "/data.csv")))

write.csv(as.data.frame(go.result$result[, 1:13]), paste0(opts$tempdir, "/enrichment.csv"))
