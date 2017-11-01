#!/usr/bin/env python
from __future__ import print_function
from criteo_dataset import CriteoDataset
import numpy as np
import gzip
import argparse

parser = argparse.ArgumentParser(description='Submit the result to crowdAI')
parser.add_argument('--test_set', dest='test_set', action='store', required=True)
parser.add_argument('--output_path', dest='output_path', action='store', required=True)
args = parser.parse_args()

data = CriteoDataset(args.test_set)

output = gzip.open(args.output_path, "wb")

for _impression in data:
    num_of_candidates = len(_impression["candidates"])
    predictions = np.random.rand(num_of_candidates)*10
    predictions = ["{}:{}".format(idx, p) for idx, p in enumerate(predictions)]
    predictionline = "{};{}".format(_impression["id"], ",".join(predictions))
    output.write(predictionline+"\n")
    print(predictionline)

output.close()
print("Successfully Wrote predictions file to : ",args.output_path)
