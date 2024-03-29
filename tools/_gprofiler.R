### _gprofiler.R ###

suppressPackageStartupMessages({
    library(gprofiler2)
})


gene_loader <- function(path){
    stopifnot(is.character(path))
    return(rownames(read.csv(path, header=T, row.names=1)))
}


egost <- function(
    gene,
    organism="rnorvegicus",
    correction_method="fdr", 
    user_threshold=0.05, 
    domain_scope="annotated",
    sources="GO"
){
    stopifnot(is.vector(gene))
    stopifnot(is.character(gene))
    stopifnot(is.character(organism))
    stopifnot(is.character(correction_method))
    stopifnot(is.numeric(user_threshold))
    return(
        gost(
            query=gene,
            organism=organism,
            correction_method=correction_method,
            user_threshold=user_threshold,
            domain_scope=domain_scope,
            sources=sources
        )
    )
}
