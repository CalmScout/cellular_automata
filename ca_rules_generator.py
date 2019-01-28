"""
Class for cellular automata rules generation.
"""
import numpy as np
from constants import neighb_rad, num_of_cell_states
from useful_functions import cartesian_product, nth_term


class RulesGenerator1DNoMem:
    """
    Generates all rules for given neighborhood radius and number of cell states.
    """
    def __init__(self, neighb_rad=neighb_rad, num_of_cell_states=num_of_cell_states):
        """
        Generate rules and saves into 'data_path/rules/' dir.
        """
        # save constants for current CA rules class
        self.n = 2 * neighb_rad + 1     # size of neighborhood
        # total number of possible CA neighborhood conditions
        self.num_of_possible_inputs = np.power(num_of_cell_states, self.n)
        # array we will use to generate generators for input and output data
        self.cell_states_arr = np.arange(num_of_cell_states, dtype=np.uint8)
        # number of cellular automata
        self.num_of_ca = np.power(num_of_cell_states, self.num_of_possible_inputs)

    def _generate_inputs(self):
        """
        Generates inputs.
        :return: generator consisting of all possible neighborhoods
        """
        return cartesian_product(self.cell_states_arr, repeat=self.n)

    def _generate_outputs(self):
        """
        Generates all possible outputs for all possible inputs.
        :return: generator consisting of all possible outputs for all possible neighborhoods
        """
        return cartesian_product(self.cell_states_arr, repeat=self.num_of_possible_inputs)

    def get_idx_boundaries(self):
        """
        :return: string '[min_idx_value, max_idx_value]'
        """
        return "[{}, {}]".format(0, self.num_of_ca - 1)

    def get_rule_by_idx(self, idx):
        """
        Generates all rules and returns one with index 'idx' in form of the dictionary.
        :param idx: index of rule to return
        :return: dictionary 'neighborhood' -> state; tuple -> np.uint8
        """
        # check if we have appropriate index
        if idx < 0 or idx > self.num_of_ca - 1:
            raise ValueError("Index of CA must be in range: [0, {}]".format(self.num_of_ca - 1))
        # generate all rules
        gen_1 = self._generate_inputs()
        gen_2 = self._generate_outputs()
        # combine result into dict
        res = dict()
        for key, val in zip(gen_1, nth_term(gen_2, idx)):
            res[key] = val
        return res


if __name__ == "__main__":
    generator = RulesGenerator1DNoMem(neighb_rad=1, num_of_cell_states=2)
    # min max values of idx
    print(generator.get_idx_boundaries())
    # get rule in the form of the list
    rule = generator.get_rule_by_idx(42)
    tmp = [0] * len(rule)
    for idx, el in enumerate(rule):
        tmp[idx] = rule[el]
    print(tmp)

