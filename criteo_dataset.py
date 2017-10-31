#!/usr/bin/env python
from __future__ import print_function
import utils
import hashlib

class CriteoDataset:
    def __init__(self, filepath, isTest=False, salt=False, id_map=False, debug=False):
        self.fp = open(filepath, "r")
        self.debug = debug
        self.isTest = isTest
        """
            `isTest` is a boolean value which signals that this file does not
            have `cost` and `propensity` information available for any impressions
        """
        self.salt = salt
        """
            if a `salt` is provided, then the action
            at the first index of an impression_block (one that is selected by the
            logger policy) should be swapped with another index of the impression_block

            the index with which it is to be swapped is decided by computing an integral hash
            from the string version of the id of the impression_block.
        """

        self.id_map = id_map
        """
            id_map is an optional function which can be used to transform the `impression_id` to another value
            a simple example could be :
            ```
            def _f(x):
                return x+"_postfix"
            ```
        """
        self.line_buffer = []

    def __iter__(self):
        return self

    def next(self):
        next_block = self.get_next_impression_block()
        if next_block:
            return next_block
        else:
            raise StopIteration

    def __next__(self):
        return self.next()

    def get_next_line(self):
        try:
            line = self.fp.readline()
            return line
        except StopIteration:
            return False

    def get_next_impression_block(self):
        # Obtain the first line of an impression block
        assert len(self.line_buffer) <= 1
        if len(self.line_buffer) == 0:
            line = self.get_next_line()
            if not line:
                return False
        else:
            line = self.line_buffer.pop()

        block_impression_id = utils.extract_impression_id(line, True)
        if self.id_map:
            block_impression_id = self.id_map(block_impression_id)

        if not self.isTest:
            cost, propensity = utils.extract_cost_propensity(line)

        candidate_features = [utils.extract_features(line, self.debug)]

        while True:
            line = self.get_next_line()
            if not line: #EOF
                break

            line_impression_id = utils.extract_impression_id(line)
            if self.id_map:
                line_impression_id = self.id_map(line_impression_id)

            if line_impression_id != block_impression_id:
                # Save the line in the line_buffer
                self.line_buffer.append(line)
                break
            else:
                candidate_features.append(utils.extract_features(line, debug=self.debug))

        if self.salt:
            # Compute a deterministic number (deterministic based on a salt) in [0, L)
            # where `L` is the number of candidates
            target_index = self.compute_integral_hash(S=str(block_impression_id) , modulo=len(candidate_features))
            # swap the first element with the element at the target_index
            candidate_features[0], candidate_features[target_index] = candidate_features[target_index], candidate_features[0]

        _response = {}
        _response["id"] = block_impression_id
        _response["candidates"] = candidate_features
        if not self.isTest:
            _response["cost"] = cost
            _response["propensity"] = propensity
        return  {
                    "id": block_impression_id ,
                    "cost": cost,
                    "propensity": propensity,
                    "candidates": candidate_features
                }

    def compute_integral_hash(self,S, modulo):
        S = str(S)
        S += self.salt
        md5 = hashlib.md5(S).hexdigest()
        _ords = [ord(c) for c in md5]
        return (sum(_ords)**7) % modulo

    def close(self):
        self.__del__()

    def __del__(self):
        self.fp.close()
