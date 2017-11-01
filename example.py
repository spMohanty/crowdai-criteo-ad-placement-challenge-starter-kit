#!/usr/bin/env python
from __future__ import print_function
import json

from criteo_dataset import CriteoDataset

train = CriteoDataset("data/cntk_small.txt.gz", isTest=False)

for _impression in train:
    print(_impression)
    """
        {
          "propensity": 336.294857951,
          "cost": 0.999,
          "id": "68965824",
          "candidates": [
            {
              0: 300,
              1: 600,
              2: 1,
              3: 1,
              4: 1,
              5: 1,
              6: 1,
              7: 1,
              8: 1,
              9: 1,
              10: 1,
              11: 1,
              12: 1,
              13: 1,
              14: 1,
              15: 1,
              16: 1,
              17: 1,
              18: 1,
              19: 1,
              20: 1
            },
            ...
            ...
            ...
          ]
        }
    """

train.close()
