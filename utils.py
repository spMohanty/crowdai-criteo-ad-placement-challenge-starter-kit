from __future__ import print_function
import hashlib
import numpy as np

def extract_impression_id(line, assert_first_line=False):
    """
        Extracts the impression_id from a line

        params:
            assert_first_line: `boolean`
                a conditionals to assert if the line is indeed the first line of an impression block
    """
    if assert_first_line:
        assert len(line.split("|")) == 4
    return line[:line.index("|")].strip()

def extract_cost_propensity(line):
    """
        Extracts the cost, propensity value from a line.
        Only the first line in an impression block.

        params:
        line: `string`

    """
    line_items = line.split("|")
    assert len(line_items) == 4
    cost = float(line_items[1].replace("l ","").strip())
    propensity = np.float64(line_items[2].replace("p ","").strip())
    return cost, propensity

def extract_features(line, debug=False):
    features_index = line.index("|f ")
    feature_string = line[features_index:].replace("|f ","")
    feature_set = feature_string.split()
    feature_dict = {}
    for _feature in feature_set:
        _feature = _feature.split(":")
        _feature = [int(x) for x in _feature]
        feature_dict[_feature[0]] = _feature[1] #Store 0:320 1:50 2:1 21:1 22:1 23:1 as key value pairs in feature_dict

    if debug: print(feature_dict)
    return feature_dict
