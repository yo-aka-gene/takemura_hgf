### _go.R ###

suppressPackageStartupMessages({
    library(AnnotationDbi)
    library(org.Hs.eg.db)
    library(clusterProfiler)
    library(GO.db)
})


gene_loader <- function(path){
    stopifnot(is.character(path))
    return(rownames(read.csv(path, header=T, row.names=1)))
}


sym2eg <- function(symbol){
    stopifnot(is.character(symbol))
    return(c(as.list(org.Hs.egALIAS2EG)[symbol][[1]])[1])
}


sym2goid <- function(symbol){
    stopifnot(is.character(symbol))
    return(names(as.list(org.Hs.egGO)[sym2eg(symbol)][[1]]))
}


gomatrix <- function(symbol){
    gomat_ <- function(arg){
        stopifnot(is.character(arg))
        df <- as.matrix(
            AnnotationDbi::select(
                GO.db,
                keys = sym2goid(arg),
                columns = c("ONTOLOGY","TERM"), 
                keytype = "GOID"
            )
        )
        gene <- data.frame(rep(arg, times=length(df)))
        names(gene) <- "GENE"
        return(cbind(df, gene))
    }
    if (is.vector(symbol)) {
        return(
            do.call(
                rbind, 
                lapply(symbol, gomat_)
            )
        )
    } else {
        return(gomat_(symbol))
    }
}


ego <- function(
    gene,
    OrgDb="org.Hs.eg.db",
    ont="ALL",
    pAdjustMethod="BH", 
    pvalueCutoff=0.05, 
    keyType="SYMBOL",
    readable=FALSE
){
    stopifnot(is.vector(gene))
    stopifnot(is.character(gene))
    stopifnot(is.character(OrgDb))
    stopifnot(is.character(ont))
    stopifnot(is.character(pAdjustMethod))
    stopifnot(is.numeric(pvalueCutoff))
    stopifnot(is.character(keyType))
    stopifnot(is.logical(readable))
    return(
        enrichGO(
            gene=gene,
            OrgDb=OrgDb,
            ont=ont,
            pAdjustMethod=pAdjustMethod, 
            pvalueCutoff=pvalueCutoff, 
            keyType=keyType,
            readable=readable
        )
    )
}
