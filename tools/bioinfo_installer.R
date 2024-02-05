### bioinfo_installer.R ###

install.packages("BiocManager", repos="http://cran.ism.ac.jp/")
BiocManager::install("clusterProfiler")
BiocManager::install("AnnotationDbi")
BiocManager::install("org.Hs.eg.db")
BiocManager::install("org.Mm.eg.db")
BiocManager::install("org.Rn.eg.db")
BiocManager::install("GO.db")
install.packages("optparse", repos="http://cran.ism.ac.jp/")
install.packages("gprofiler2", repos="http://cran.ism.ac.jp/")
