![GitHub](https://img.shields.io/github/license/Gram21/BERT4DAT?style=plastic)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gram21/BERT4DAT/)

# BERT4DAT

Supplementary material for the paper "Does BERT Understand Code? -- An Exploratory Study on the Detection of Architectural Tactics in Code" by Jan Keim, Angelika Kaplan, Anne Koziolek, and Mehdi Mirakhorli for the [14th European Conference on Software Architecture (ECSA 2020)](https://ecsa2020.disim.univaq.it/).

Note that we are not able to provide the actual models that were used to produce the results of the paper.
The results may still be reproduced with the supplied notebooks and correct configurations.


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

## How to use
The artifacts can be downloaded from Zenodo: TODO

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
