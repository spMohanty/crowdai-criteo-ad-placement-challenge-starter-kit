![CrowdAI-Logo](https://github.com/crowdAI/crowdai/raw/master/app/assets/images/misc/crowdai-logo-smile.svg?sanitize=true)
# crowdai-criteo-ad-placement-challenge-starter-kit

Starter kit for the [Criteo Ad Placement Challenge](https://www.crowdai.org/challenges/nips-17-workshop-criteo-ad-placement-challenge) on [CrowdAI](https://www.crowdai.org/).

# Installation

```
git clone https://github.com/spMohanty/crowdai-criteo-ad-placement-challenge-starter-kit criteo_starter_kit
pip install --upgrade crowdai
```
**NOTE** : Please ensure that you have at least version `1.0.9` of `crowdai`

# Test your First Submission
```
cd criteo_starter_kit
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
"""
* Download `criteo_test_release_small.txt.gz` from the CrowdAI datasets page of the challenge.
* Save it in the `data/` folder.
"""
python generate_random_predictions.py --test_set=data/criteo_test_release_small.txt.gz --output_path=data/predictions.gz
python submit_random_predictions.py --api_key=<YOUR_CROWDAI_API_KEY> --predictions=data/predictions.gz
```

# About
Consider a display advertising scenario: a user arrives at a website where we have an advertisement slot (“an impression”). We have a pool of potential products to advertise during that impression (“a candidate set”). A “policy” chooses which product to display so as to maximize the number of clicks by the users.

The goal of the challenge is to find a good policy that, knowing the candidate set and impression context, chooses products to display such that the aggregate click-through-rate (“CTR”) from deploying the policy is maximized.

To enable you to find a good policy, [Criteo](https://www.criteo.com/) has generously donated several gigabytes of `<user impression, candidate set, selected product, click/no-click>` logs from a randomized version of their in-production policy! Go to the [Dataset section](https://www.crowdai.org/challenges/nips-17-workshop-criteo-ad-placement-challenge/dataset_files) of the challenge to access the dataset.

# Dataset

In the dataset, each impression is represented by `M` lines where `M` is the number of candidate ads. Each line has feature information for every other candidate ad.
In addition, the first line corresponds to the candidate that was displayed by the logging policy, an indicator whether the displayed product was clicked by the user ("click" encoded as `0.001`, "no-click" encoded as `0.999`), and the **inverse propensity** of the stochastic logging policy to pick that specific candidate (see the  [ companion paper ](http://www.cs.cornell.edu/~adith/Criteo/). for details).
Each `<user context-candidate product>` pair is described using **33 categorical (multi-set) features and 2 numeric features**. Of these, 10 features are only-context-dependent while the remaining 25 features depend on both the context and the candidate product. These categorical feature representations have been post-processed to a 74000-dimensional vector with sparse one-hot encoding for each categorical feature. **The semantics behind the features will not be disclosed**.

These post-processed dataset files are available [ here ](https://www.crowdai.org/challenges/nips-17-workshop-criteo-ad-placement-challenge/dataset_files
).

# Evaluation

Your task is to build a function `f` which takes `M` candidates, each represented by a `74000-dimensional vector`, and outputs scores for each of the candidates between 1 and M.

The reward for an individual impression is, did the selected candidate get clicked _(reward = 1)_ or not _(reward = 0)_? The reward for function `f` is the aggregate reward over all impressions on a held out test set of impressions.

We will be using an unbiased estimate of the aggregate reward using inverse propensity scoring (see [ the companion paper ](http://www.cs.cornell.edu/~adith/Criteo/NIPS16_Benchmark.pdf) for details).


# Parser

```
from criteo_dataset import CriteoDataset

"""
 * Download `criteo_train_small.txt.gz` from the CrowdAI datasets page of the challenge.
"""

# Instantiate a CriteoDataset object by passing the path to the relevant file
train = CriteoDataset("data/criteo_train_small.txt.gz", isTest=False)

"""
Arguments:
* `isTest` : Boolean
The `isTest` parameter is used to determine if its a test set (one which does not have cost/propensity information for every impression)
Hence in case of the training data, `isTest` should be `False`.
"""

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

#  Author
S.P. Mohanty <sharada.mohanty@epfl.ch>
