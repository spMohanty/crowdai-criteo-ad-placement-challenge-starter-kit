from __future__ import print_function
import hashlib
import numpy as np
import copy

def extract_impression_id(line, assert_first_line=False):
    """
        Extracts the impression_id from a line
    """
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
    #NOTE That the value after |p in the line is actually inverse propensity
    # Hence, the need for the division by 1
    propensity = 1.0/np.float64(line_items[2].replace("p ","").strip())
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
    """

    impression_id = _impression["id"]
    has_cost = 'cost' in _impression.keys()
    has_propensity = 'propensity' in _impression.keys()
    lines = []
    for _idx, candidate in enumerate(_impression["candidates"]):
        _line = (impression_id.strip("L"))+" "
        if not test_mode and has_cost and has_propensity and _idx==0:
            _line += "|l {} ".format(_impression['cost'])
            _line += "|p {}".format(_impression["propensity"])

        _line += dump_feature(candidate)
        lines.append(_line)

    return "\n".join(lines)

def compute_integral_hash(S, salt, modulo):
    S = str(S)
    S += salt
    md5 = hashlib.md5(S).hexdigest()
    _ords = [ord(c) for c in md5]
    return (sum(_ords)**7) % modulo

def update_progress(context, percent_complete, message=""):
        """
            Internal function for relaying back the scores to the client
        """
        #Register Progress
        _progress_update = {}
        _progress_update["percent_complete"] = percent_complete
        _progress_update["message"] = message
        _progress_update["data_sequence_no"] = context["data_sequence_no"]
        context['redis_conn'].rpush(context['response_channel'], json.dumps(job_progress_update(context, _progress_update, _progress_update["message"])))
