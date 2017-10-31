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

def dump_feature(feature):
    """
        Gets a single feature as a dictionary, and returns it rendered as a string
    """
    s = "|f "
    for _key in sorted(feature.keys()):
        s += "{}:{} ".format(_key, feature[_key])
    return s

def dump_impression(_impression, test_mode=False, debug=False):
    """
        Expects an impression block, and renders it out in the CNTK format
        {'propensity': 18.1513997361, 'cost': 0.999, 'candidates': [{0: 980, 1: 240, 2: 1, 5: 1, 28039: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 11797: 1, 2839: 1, 2841: 1, 282: 1, 42: 1, 965: 1, 969: 1, 8523: 1, 8524: 1, 8525: 1, 80: 1, 5476: 1, 229: 1, 1264: 1}, {0: 980, 1: 240, 2: 1, 5: 1, 28039: 1, 12: 1, 14: 1, 21: 1, 964: 3, 282: 1, 1308: 1, 1309: 1, 1313: 1, 49: 1, 51: 3, 52: 1, 1306: 1, 580: 3, 2126: 3, 208: 1, 722: 1, 91: 1, 5476: 1, 229: 1, 1264: 1, 11797: 1}, {0: 980, 1: 240, 2: 1, 5: 1, 28039: 1, 11: 1, 13: 1, 1296: 1, 1297: 1, 21: 1, 22: 1, 24: 4, 282: 1, 32: 2, 185: 4, 589: 1, 5476: 1, 229: 1, 5481: 1, 1642: 1, 11797: 1, 1264: 1, 3063: 4, 149: 1}, {0: 980, 1: 240, 2: 1, 5: 1, 28039: 1, 11: 1, 13: 1, 1296: 1, 1297: 1, 11797: 1, 22: 1, 24: 2, 282: 1, 1574: 2, 313: 1, 449: 1, 589: 1, 185: 2, 229: 1, 5476: 1, 6117: 1, 1264: 1, 21: 1}, {0: 980, 1: 240, 2: 1, 772: 1, 5: 1, 28039: 1, 11: 1, 13: 1, 1296: 1, 1297: 1, 21: 1, 22: 1, 24: 5, 26: 3, 282: 1, 3845: 5, 185: 5, 1376: 1, 5476: 1, 229: 1, 5480: 1, 11797: 1, 1264: 1, 149: 1}, {0: 980, 1: 240, 2: 1, 5: 1, 28039: 1, 11: 1, 13: 1, 1296: 1, 1297: 1, 11797: 1, 22: 1, 23: 1, 24: 1, 282: 1, 185: 1, 187: 1, 313: 1, 5476: 1, 229: 1, 1264: 1, 1270: 1, 21: 1}, {0: 980, 1: 240, 2: 1, 644: 1, 5: 1, 28039: 1, 147: 1, 21: 1, 22: 1, 24: 3, 282: 1, 1585: 3, 1067: 1, 1068: 1, 49: 1, 313: 1, 836: 1, 185: 3, 227: 1, 5476: 1, 229: 1, 6118: 1, 106: 1, 619: 1, 1264: 1, 5494: 1, 1273: 1, 11797: 1}], 'id': '70893571'}
    """

    impression_id = _impression["id"]
    has_cost = 'cost' in _impression.keys()
    has_propensity = 'propensity' in _impression.keys()
    lines = []
    for _idx, candidate in enumerate(_impression["candidates"]):
        _line = str(impression_id)+" "

        if not test_mode and has_cost and has_propensity and _idx==0:
            _line += "|l {} ".format(_impression['cost'])
            _line += "|p {}".format(_impression["propensity"])

        _line += dump_feature(candidate)
        lines.append(_line)

    return "\n".join(lines)
