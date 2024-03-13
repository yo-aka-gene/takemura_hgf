# README: takemura_hgf
[<img src="https://img.shields.io/badge/DOI-10.1186/s41232--024--00322--9-FAB70C?style=flat&logo=doi">](https://doi.org/10.1186/s41232-024-00322-9)
[<img src="https://img.shields.io/badge/PMID-accepted-326599?style=flat&logo=pubmed">]()
[![Documentation Status](https://readthedocs.org/projects/takemura-hgf/badge/?version=latest)](https://takemura-hgf.readthedocs.io/en/latest/?badge=latest)
[<img src="https://img.shields.io/badge/Documentation-takemura--hgf.rtfd.io-8CA1AF?style=flat&logo=readthedocs">](https://takemura-hgf.readthedocs.io/en/latest/)
[<img src="https://img.shields.io/badge/Code_Examples-Jupyter_Notebook-F37626?style=flat&logo=jupyter">](https://takemura-hgf.readthedocs.io/en/latest/analyses.html)
[<img src="https://img.shields.io/badge/GitHub-yo--aka--gene/takemura__hgf-181717?style=flat&logo=github">](https://github.com/yo-aka-gene/takemura_hgf)

- This is a repository for analysis codes in [Chronological transitions of hepatocyte growth factor treatment effects in spinal cord injury tissue](https://doi.org/10.1186/s41232-024-00322-9)

## Documentation
<img src="https://raw.githubusercontent.com/yo-aka-gene/takemura_hgf/main/docs/_static/logo.png" width="150px"> 

- Documentation and example codes (jupyter notebooks) are available in [https://takemura-hgf.readthedocs.io/en/latest/index.html](https://takemura-hgf.readthedocs.io/en/latest/index.html)

## Start Guide
### 1. Environment Preference
- MacOS
- Docker Desktop
- git

### 2. How to reproduce the virtual env
- clone [this repository](https://github.com/yo-aka-gene/takemura_hgf)
- activate the virtual env by runnning `init.sh` in `takemura_hgf` directory. This shell script will automatically setup the virtual env and connect to it

    ```
    sh init.sh
    ```
    **Note**: Our docker container will occupy `localhost:8008`
- password for the JupyterLab server is `jupyter`
### 3. Run codes
- to reproduce all outputs at a time with a pipeline, run codes in `/home/jovyan/code/experiment_execution.ipynb`
- If you are interested in taking a detailed look at each analysis, we have [online documentation](https://takemura-hgf.readthedocs.io/en/latest/index.html) and the same ipynb files are in `/home/jovyan/code/jupyternb` as well.
