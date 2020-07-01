![GitHub](https://img.shields.io/github/license/Gram21/BERT4DAT?style=plastic)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gram21/BERT4DAT/)

# BERT4DAT

Supplementary material for the paper "Does BERT Understand Code? -- An Exploratory Study on the Detection of Architectural Tactics in Code" by Jan Keim, Angelika Kaplan, Anne Koziolek, and Mehdi Mirakhorli for the [14th European Conference on Software Architecture (ECSA 2020)](https://ecsa2020.disim.univaq.it/).

Note that we are not able to provide the actual models that were used to produce the results of the paper.
The results may still be reproduced with the supplied notebooks and correct configurations.

The original data sets can be found in at [SoftwareDesignLab/Archie](https://github.com/SoftwareDesignLab/Archie).


## How to cite
```
@InProceedings{Keim2020,
author={Keim, Jan and Kaplan, Angelika and Koziolek, Anne and Mirakhorli, Mehdi},
title={Does {BERT} Understand Code? -- An Exploratory Study on the Detection of Architectural Tactics in Code},
booktitle={14th European Conference on Software Architecture (ECSA 2020)},
year={2020},
publisher={Springer International Publishing},
}

```

This repository can be cited as:
```
@software{keim2020_3925166,
  author       = {Jan Keim and Angelika Kaplan and Anne Koziolek and Mehdi Mirakhorli},
  title        = {Gram21/BERT4DAT},
  month        = jul,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {v1.0},
  doi          = {10.5281/zenodo.3925165},
  url          = {https://doi.org/10.5281/zenodo.3925165}
}
```

## How to use
The artifacts can be downloaded from [Zenodo](https://doi.org/10.5281/zenodo.3925165).

We recommend you to [open this repository in Google Colab](https://colab.research.google.com/github/Gram21/BERT4DAT/) (this link opens the submission repository directly in Colab and allows you to open one of the notebooks).
With Colab, you should be able to open the notebooks, set the preferred configuration parameters and run all cells (CTRL+F9 or Runtime -> Run All).
A GPU as hardware accelerator should already be used by Colab.
We have a cell that checks if a GPU is used; if it turns out that none is used, please enable the GPU (in Colab: Edit -> Notebook settings -> Hardware accelerator: GPU).

If you plan on running locally, you need to install [Jupyter](https://jupyter.org/install).
Furthermore, you might have to install further python dependencies than the ones installed in the notebooks (first cell) depending on your python installation.
You have to make sure that you installed all python libraries that are imported in the second cell via pip.
It is neccessary to install [PyTorch](https://pytorch.org/get-started/locally/#start-locally).
You will need a machine with a very potent GPU (at least 12GB GPU RAM for the large models) as the pretrained BERT model is very memory hungry.
Also, you have to make sure that your GPU and drivers support CUDA.
We recommend Ubuntu as operating system.
Moreover, some parts of the notebooks are coded and designed for Colab; there might be some differences in appearance.
There should be no problems regarding the code, but there is still the possibility that you might experience some issues (regarding your installation, system, setup etc.).

Each notebook has a cell with the configuration that can be adapted and allows tuning hyperparameters and configure experiment set-ups like sampling or folding strategy.
Details on the hyperparameters and settings are outlined in the respective [Notebooks](./notebooks/).

This repository contains the code used in the paper, as well as additional results:

* [notebooks](./notebooks/) contains the python notebooks (code):
	- [BERT4DAT_eval.ipynb](./notebooks/BERT4DAT_eval.ipynb): Notebook to perform 10-fold classification
	- [BERT4DAT_trainAndUse.ipynb](./notebooks/BERT4DAT_trainAndUse.ipynb): Notebook to train the model and then use it on a given evaluation data set
* [scripts](./scripts/) contains various scripts:
	- [prepareInput.py](./scripts/prepareInput.py): Script to preprocess the data
	- [eval.py](./scripts/eval.py): Script used to proces the log produced for evaluation and calculate the metrics
* [eval](./eval/) contains the results of all tested hyperparameter configurations for each task
* [data](./data/) contains the already preprocessed data to be directly used in the notebooks.

## Attribution
The preprocessed datasets are based on the original dataset that can be found at [SoftwareDesignLab/Archie](https://github.com/SoftwareDesignLab/Archie). These datasets are used in the following papers:
- Mirakhorli, M., & Cleland-Huang, J. (2016). Detecting, Tracing, and Monitoring Architectural Tactics in Code. IEEE Annals of the History of Computing, (03), 205-220.
- Mirakhorli, M., Shin, Y., Cleland-Huang, J., & Cinar, M. (2012, June). A tactic-centric approach for automating traceability of quality concerns. In 2012 34th international conference on software engineering (ICSE) (pp. 639-649). IEEE.