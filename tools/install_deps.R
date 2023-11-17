### install_deps.R ###

deps <- read.csv("./tools/requirements_r.csv", row.names=1)
"%notin%" <- Negate("%in%")
current_pkg <- installed.packages()

for(package in rownames(deps)) {
    if (package %notin% rownames(current_pkg)) {
        remotes::install_version(package, version = deps[package,"Version"], repos="http://cran.ism.ac.jp/")
    } else if (deps[package,"Version"] != current_pkg[package,"Version"]) {
        remotes::install_version(package, version = deps[package,"Version"], repos="http://cran.ism.ac.jp/")
    } else {
        print(sprintf("Requirement is already satisfied: %s (version==%s)", package, deps[package,"Version"]))
    }
}
