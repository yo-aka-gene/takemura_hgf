### _get_go.R ###

suppressPackageStartupMessages({
    library(clusterProfiler)
    library(optparse)
    source("/home/jovyan/tools/_go.R")
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

go.result <- goid2sym(
    goid=read.csv(
        paste0(opts$tempdir, "/data.csv"), header=T, row.names=1
    )$term_id
)

write.csv(as.data.frame(go.result), paste0(opts$tempdir, "/genelist.csv"))
