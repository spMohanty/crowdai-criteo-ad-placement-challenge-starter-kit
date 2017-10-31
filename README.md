![CrowdAI-Logo](https://github.com/crowdAI/crowdai/raw/master/app/assets/images/misc/crowdai-logo-smile.svg?sanitize=true)
# crowdai-criteo-ad-placement-challenge-starter-kit

Starter kit for the [Criteo Ad Placement Challenge](https://www.crowdai.org/challenges/nips-17-workshop-criteo-ad-placement-challenge) on [CrowdAI](https://www.crowdai.org/).

# About

# Installation

```
git clone https://github.com/spMohanty/crowdai-criteo-ad-placement-challenge-starter-kit criteo_starter_kit
pip install --upgrade crowdai
```

# Your First Submission
```
# First run the script below to generate a random prediction file
# python generate_random_prediction.py > data/predictions.txt

import crowdai
api_key  = "YOUR-CROWDAI-API-KEY"
challenge = crowdai.Challenge("CriteoAdPlacementNIPS2017", api_key)

scores = challenge.submit("../CriteoAdPlacementChallenge_job_factory/data/predictions.txt")
print scores
"""
{
  "impwt_std": 0.00064745289554913,
  "ips_std": 2.6075584296658,
  "snips": 6603.0581686235,
  "max_instances": 4027,
  "ips": 24.30130041425,
  "impwt": 0.0036803099099937,
  "message": "",
  "snips_std": 17.529346134878,
  "job_state": "CrowdAI.Event.Job.COMPLETE"
}
"""
```

# Usage

```
from criteo_dataset import CriteoDataset

# Instantiate a CriteoDataset object by passing the path to the relevant file
train = CriteoDataset("data/cntk_small.txt", isTest=False)

# Iterate over the impression blocks
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
              .....
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
```

# About


#  Author
S.P. Mohanty <sharada.mohanty@epfl.ch>
