#!/usr/bin/env python
from __future__ import print_function
import utils

class CriteoDataset:
    def __init__(self, filepath, isTest=False, debug=False):
        self.fp = open(filepath, "r")
        self.debug = debug
        self.isTest = isTest
        self.line_buffer = []

    def __iter__(self):
        return self

    def next(self):
        next_block = self.get_next_impression_block()
        if next_block:
            return next_block
        else:
            raise StopIteration


    def get_next_line(self):
        try:
            return self.fp.readline()
        except StopIteration:
            return False

    def get_next_impression_block(self):
        current_position = self.fp.tell()
        # Obtain the first line of an impression block
        if len(self.line_buffer) == 0:
            line = self.get_next_line()
            if not line:
                return False
        else:
            line = self.line_buffer.pop()

        block_impression_id = utils.extract_impression_id(line, True)
        cost, propensity = utils.extract_cost_propensity(line)

        candidate_features = [utils.extract_features(line, self.debug)]

        while True:
            line = self.get_next_line()
            if not line: #EOF
                break

            line_impression_id = utils.extract_impression_id(line)
            candidate_features.append(utils.extract_features(line, debug=self.debug))

            if line_impression_id != block_impression_id:
                # Save the line in the line_buffer
                self.line_buffer.append(line)
                break

        return  {
                    "id": block_impression_id ,
                    "cost": cost,
                    "propensity": propensity,
                    "candidates": candidate_features
                }

    def close(self):
        self.__del__()

    def __del__(self):
        self.fp.close()
