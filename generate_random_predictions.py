#!/usr/bin/env python
from __future__ import print_function
from criteo_dataset import CriteoDataset
import numpy as np

GOLD_LABEL_PATH = "data/cntk_small.txt.gz"

data = CriteoDataset(GOLD_LABEL_PATH)

for _impression in data:
    num_of_candidates = len(_impression["candidates"])
    predictions = np.random.rand(num_of_candidates)*10
    predictions = ["{}:{}".format(idx, p) for idx, p in enumerate(predictions)]
    predictionline = "{};{}".format(_impression["id"], ",".join(predictions))
    print(predictionline)
