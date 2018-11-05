"""
Data generator for 1D, deterministic, 2 state CA with a symmetric neighbourhood of radius r and periodic boundary
condition
Code adapted from "IPython Interactive Computing and Visualization Cookbook", 2nd edition, by Cyrille Rossant
https://github.com/ipython-books/cookbook-2nd/blob/master/chapter12_deterministic/02_cellular.md
"""
import numpy as np
import os
import matplotlib.pyplot as plt     # auxiliary module, only for demo is used
from useful_functions import cartesian_product, id_generator, save_obj, load_obj
from constants import data_path_wolfram, size_wolfram, steps_wolfram, prob_of_ones_tpl_wolfram
from constants import data_path_no_memory, size_no_memory, steps_no_memory, neighb_radius_no_memory, num_of_cell_states


class GenerateDatasetByWolframCode:
    """
    Class for generating Wolfram based cellular automatas datasets.
    """
    def __init__(self, path=data_path_wolfram, size=size_wolfram, steps=steps_wolfram,
                 prob_of_ones_tpl=prob_of_ones_tpl_wolfram):
        """
        Generates
        :param path: path where generated data-sets would be saved
        :param size: the size of 1D CA
        :param steps: number of evolutionary steps
        :param prob_of_ones_tpl: probability with which 'ones' are generated in initial random conditions
        """
        self.path = path
        self.prob_of_ones_tpl = prob_of_ones_tpl
        # vector is used to obtain numbers written in binary representation
        self.u = np.array([[4], [2], [1]])
        self.num_of_rules = 255
        self.size = size
        self.steps = steps

    def _step(self, x, rule_b):
        """Compute a single step of an elementary cellular
        automaton."""
        # The columns contains the L, C, R values
        # of all cells.
        y = np.vstack((np.roll(x, 1), x,
                       np.roll(x, -1))).astype(np.int8)
        # We get the LCR pattern numbers between 0 and 7.
        z = np.sum(y * self.u, axis=0).astype(np.int8)
        # We get the patterns given by the rule.
        return rule_b[7 - z]

    def _evolve(self, rule, prob_of_one_init):
        """Simulate an elementary cellular automaton given
        its rule (number between 0 and 255)."""
        # Compute the binary representation of the rule.
        rule_b = np.array(
            [int(_) for _ in np.binary_repr(rule, 8)],
            dtype=np.int8)
        x = np.zeros((self.steps, self.size), dtype=np.int8)
        # Random initial state.
        x[0, :] = np.random.rand(self.size) < prob_of_one_init
        # Apply the step function iteratively.
        for i in range(self.steps - 1):
            x[i + 1, :] = self._step(x[i, :], rule_b)
        return x

    def _show_generated_image(self, rule, prob):
        im = np.load(self.path + "rule_{}_{}.npy".format(rule, prob))
        plt.imshow(im, cmap=plt.cm.binary)
        plt.show()

    def generate_dataset(self):
        """
        Generates data-set and save to 'path'dir in the form of .npy files
        """
        for rule in range(self.num_of_rules):
            for prob_of_one_init in self.prob_of_ones_tpl:
                x = self._evolve(rule, prob_of_one_init)
                np.save(self.path + "rule_{}_{}.npy".format(rule, prob_of_one_init), x)


class GenerateNoMemory:
    """
    Simulate 1D CA with cyclic boundary conditions.
    """
    def __init__(self, path=data_path_no_memory, size=size_no_memory, steps=steps_no_memory,
                 neighb_radius=neighb_radius_no_memory, states=num_of_cell_states):
        self.path = path
        self.size = size
        self.steps = steps
        self.neighb_radius = neighb_radius
        self.num_of_cell_states = states
        self.rules = None
        self.x = None
        self.id_str = None
        if len(os.listdir(self.path)) == 0:
            self._generate_rules()
        else:
            # should be redone for random '.pkl' file
            self.rules = load_obj(self.path, "DDF9PD")
            self.id_str = "DDF9PD"

    def _generate_rules(self):
        """
        Generates dictionary of rules and save it to file.
        """
        cell_states_arr = np.array(range(self.num_of_cell_states))
        # number of cells in the neighborhood configuration
        n = 2 * self.neighb_radius + 1
        # temporary array for all vectors of which we want to compute cartesian product
        my_arr = []
        for i in range(n):
            my_arr.append(cell_states_arr)
        my_arr = np.array(my_arr)
        # all neighborhoods
        neighb_all = cartesian_product(*my_arr)
        self.rules = {}
        for i in range(len(neighb_all)):
            # generate new random state for center cell of the neighbourhood
            new_state = np.random.randint(low=0, high=self.num_of_cell_states, dtype=np.int16)
            # remove brackets '[' and ']'
            self.rules[str(neighb_all[i])[1:-1]] = new_state
        # save dictionary to file for further comparison with identified rules
        self.id_str = id_generator()
        save_obj(self.rules, path='data/no_memory/', name=self.id_str)

    def _step(self, x_column):
        # generate temporary array of neighborhoods
        lst = []
        for r_curr in range(self.neighb_radius, -self.neighb_radius - 1, -1):
            lst.append(np.roll(x_column, r_curr))
        neighb_arr = np.vstack(lst).astype(np.int16)
        # compute next condition of all cells
        res = np.zeros(shape=x_column.shape, dtype=np.int16)
        for i in range(len(x_column)):
            res[i] = self.rules[str(neighb_arr[:, i])[1:-1]]
        return res

    def _evolve(self):
        """
        Simulate a CA.
        """
        self.x = np.zeros((self.steps, self.size), dtype=np.int16)
        # random initial states
        self.x[0, :] = np.random.randint(low=0, high=self.num_of_cell_states, size=self.size, dtype=np.int16)
        # Apply the step function iteratively
        for i in range(self.steps - 1):
            self.x[i + 1, :] = self._step(self.x[i, :])
        # save result of the evolution to file
        np.save(self.path + "{}.npy".format(self.id_str), self.x)
        return self.x

    def _show_generated_image(self):
        im = np.load(self.path + self.id_str + ".npy")
        plt.imshow(im, cmap=plt.cm.binary)
        plt.show()

    def _show_rules(self):
        print(self.rules)


if __name__ == "__main__":
    # g = GenerateDatasetByWolframCode()
    # # g.generate_dataset()
    # g._show_generated_image(120, 0.5)
    g = GenerateNoMemory()
    g._evolve()
    g._show_generated_image()
    # g._show_rules()
