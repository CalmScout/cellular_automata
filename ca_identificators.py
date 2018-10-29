"""
Contains classes for CA identification.
"""
import numpy as np


class IdentifierWolfram:
    """
    Returns Wolfram's code for '.npy' file.
    """
    code_to_idx = {
        '111': 0,
        '110': 1,
        '101': 2,
        '100': 3,
        '011': 4,
        '010': 5,
        '001': 6,
        '000': 7
    }

    def __init__(self, file):
        self.file = file

    def identify(self):
        im = np.load(self.file)
        # binary representation of rule, initialize by negative values
        res = np.zeros(8, dtype=np.int8) - 1
        # do work until we have negative element
        for t in range(im.shape[0]-1):
            for i in range(im.shape[1]):
                # create neighborhood
                curr_neighborhood = np.zeros(3, dtype=np.int8) - 1
                if i == 0:  # then we deal with the most left element
                    curr_neighborhood[0] = im[t, im.shape[1] - 1]
                    curr_neighborhood[1] = im[t, i]
                    curr_neighborhood[2] = im[t, i + 1]
                elif i == im.shape[1] - 1:  # then we deal with the most right element
                    curr_neighborhood[0] = im[t, i - 1]
                    curr_neighborhood[1] = im[t, i]
                    curr_neighborhood[2] = im[t, 0]
                else:   # all no corner cases
                    curr_neighborhood[0] = im[t, i - 1]
                    curr_neighborhood[1] = im[t, i]
                    curr_neighborhood[2] = im[t, i + 1]
                # convert neighborhood to array code of the result
                code = str(curr_neighborhood[0]) + str(curr_neighborhood[1]) + str(curr_neighborhood[2])
                next_state = im[t+1, i]
                idx_res = self.code_to_idx[code]
                if res[idx_res] == -1:  # if it was not defined yet
                    res[idx_res] = next_state
                elif res[idx_res] != next_state:
                    raise ValueError("Rules conflict!!!")
        # convert numpy arrray to simple string
        res_str = ''
        for el in res:
            res_str += str(el)
        return int(res_str, 2)


if __name__ == "__main__":
    identifierWolfram = IdentifierWolfram('data/rule_4_0.5.npy')
    np.testing.assert_equal(identifierWolfram.identify(), 4)

    identifierWolfram = IdentifierWolfram('data/rule_85_0.95.npy')
    np.testing.assert_equal(identifierWolfram.identify(), 85)

    identifierWolfram = IdentifierWolfram('data/rule_120_0.3.npy')
    np.testing.assert_equal(identifierWolfram.identify(), 120)

    identifierWolfram = IdentifierWolfram('data/rule_173_0.7.npy')
    np.testing.assert_equal(identifierWolfram.identify(), 173)

    identifierWolfram = IdentifierWolfram('data/rule_252_0.05.npy')
    np.testing.assert_equal(identifierWolfram.identify(), 252)
