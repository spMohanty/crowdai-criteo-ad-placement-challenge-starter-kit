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

**NOTE** : The actual test set is `criteo_test_release.txt.gz`; the example above is provided to quickly introduce the participants to the problem, and the your submissions will only appear on the leaderboard if you submit a solution for the full test set. Clarification is provided in the [dry-run-mode](#dry-run-mode) section.

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

We have provided a simple parser for the dataset in this starter kit. A simple example can be found here in [parser_example.py](parser_example.py)


# Task & Evaluation

Your task is to build a function `_policy` which takes `M` candidates, each represented by a `74000-dimensional vector`, and outputs scores for each of the candidates between 1 and M.

```
data = CriteoDataset("PATH_TO_TEST_SET", isTest=True)

def _policy(candidates):
    num_of_candidates = len(candidates)
    predictions = np.random.rand(num_of_candidates)*10
    return predictions

for _idx, _impression in enumerate(data):
    predictions = _policy(_impression["candidates"])
    predictionline = _format_predictions(predictions)
    output.write(predictionline+"\n")
    if _idx % 500 == 0:
        print("Processed {} impressions...".format(_idx))

```

The reward for an individual impression is, did the selected candidate get clicked _(reward = 1)_ or not _(reward = 0)_? The reward for function `_policy` is the aggregate reward over all impressions on a held out test set of impressions.

We will be using an unbiased estimate of the aggregate reward using inverse propensity scoring (see [ the companion paper ](http://www.cs.cornell.edu/~adith/Criteo/NIPS16_Benchmark.pdf) for details).

The starter kit involves the final score computing function which is used by grader to evaluate submissions. You can score a prediction file by :
```
import compute_score
compute_score.grade_predictions("<PATH_TO_YOUR_PREDICTIONS_FILE>", "<PATH_TO_THE_CORRESPONDING_GOLD_LABELS>", _debug=True)
```

# Predictions

The final predictions file that is to be submitted is a gzipped file, which contains one line each for each impression in the test set.
And each of these lines should follow the following format :
`impression_id`;`candidate_index_0`:`candidate_score_0`,`candidate_index_1`:`candidate_score_1`,`candidate_index_2`:`candidate_score_2`...and so on.

An example line looks like follows:
```
896678244;0:5.2,1:4.81,2:4.87,3:3.90,4:8.68,5:2.8140,6:0.5032,7:7.4315,8:0.663,9:7.78398,10:1.4687811
```
We provide a parser for the prediction files, and it can be accessed [here](criteo_prediction.py).

The grader only accepts gzipped version of the prediction file (even if the parser supports non gzipped version of the prediction file).

[generate_random_predictions.py](generate_random_predictions.py) generates a sample prediction file as expected by the grader.

# Dry Run Mode

As the Test set is large, and the computation of the score takes a considerable amount of time, we have also provided smaller versions of the train and test sets for the participants to verify the grading pipeline.
The files can be downloaded in the [datasets section](https://www.crowdai.org/challenges/nips-17-workshop-criteo-ad-placement-challenge/dataset_files) of the challenge page. And when submitting a solution, it can be submitted by passing the `small_test=True` parameter to `challenge.submit` function, as done in the [provided sample scripts](submit_random_predictions.py).
These scores from these submissions (with `small_test=True`) will not be reflected on the leaderboard.

If you wish to make a submission against the full test set, then you will have to submit with `small_test=False`, as described here : https://github.com/crowdAI/crowdai-criteo-ad-placement-challenge-starter-kit/blob/master/submit_random_predictions.py#L19

# Contact:
* Technical issues : [https://gitter.im/crowdAI/NIPS17-Criteo-Ad-Placement-Challenge](https://gitter.im/crowdAI/NIPS17-Criteo-Ad-Placement-Challenge)
* Discussion Forum : [https://www.crowdai.org/challenges/nips-17-workshop-criteo-ad-placement-challenge/topics](https://www.crowdai.org/challenges/nips-17-workshop-criteo-ad-placement-challenge/topics)

#  Author
S.P. Mohanty <sharada.mohanty@epfl.ch>
