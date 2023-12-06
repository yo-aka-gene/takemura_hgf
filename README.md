# README: takemura_hgf
[![DOI](https://img.shields.io/badge/DOI-InPreparation-blue.svg?longCache=true)]()
[![PMID](https://img.shields.io/badge/PMID-InPreparation-orange.svg?longCache=true)]()
[![Documentation Status](https://readthedocs.org/projects/takemura-hgf/badge/?version=latest)](https://takemura-hgf.readthedocs.io/en/latest/?badge=latest)

- This is a repository for analysis codes in "$article\;in\;preparation$"

## Authors
- Yuji Okano
- Yoshitaka Kase
- [Hideyuki Okano](mailto:hidokano@keio.jp)

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

## Contact
- Corresponding Author: [hidokano@keio.jp](mailto:hidokano@keio.jp)
