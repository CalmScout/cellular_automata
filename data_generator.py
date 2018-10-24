"""
Data generator for 1D, deterministic, 2 state CA with a symmetric neighbourhood of radius r and periodic boundary
condition
Code adapted from "IPython Interactive Computing and Visualization Cookbook", 2nd edition, by Cyrille Rossant
https://github.com/ipython-books/cookbook-2nd/blob/master/chapter12_deterministic/02_cellular.md
"""
import numpy as np
import matplotlib.pyplot as plt # auxiliary module, only for demo is used


class GenerateByWolframCode:
    """
    Class for generating Wolfram based cellular automatas datasets.
    """
    def __init__(self, path="data/", size=100, steps=100, prob_of_ones_lst=[0.05, 0.3, 0.5, 0.7, 0.95]):
        """
        Generates
        :param path: path where generated data-sets would be saved
        :param size: the size of 1D CA
        :param steps: number of evolutionary steps
        :param prob_of_ones_lst: probability with which 'ones' are generated in initial random conditions
        """
        self.path = path
        self.prob_of_ones_lst = prob_of_ones_lst
        # vector is used to obtain numbers written in binary representation
        self.u = np.array([[4], [2], [1]])
        self.num_of_rules = 255
        self.size = size
        self.steps = steps

    def _step(self, x, rule_b):
        """Compute a single stet of an elementary cellular
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

    def _demo(self):
        """
        Auxiliary method.
        """
        fig, axes = plt.subplots(3, 3, figsize=(8, 8))
        rules = [3, 18, 30,
                 90, 106, 110,
                 158, 154, 184]
        for ax, rule in zip(axes.flat, rules):
            x = self._evolve(rule)
            ax.imshow(x, interpolation='none',
                      cmap=plt.cm.binary)
            ax.set_axis_off()
            ax.set_title(str(rule))
        plt.show()

    def _show_generated_image(self, rule, prob):
        im = np.load(self.path + "rule_{}_{}.npy".format(rule, prob))
        plt.imshow(im, cmap=plt.cm.binary)
        plt.show()

    def generate_dataset(self):
        """
        Generates data-set and save to 'path'dir in the form of .npy files
        """
        for rule in range(self.num_of_rules):
            for prob_of_one_init in self.prob_of_ones_lst:
                x = self._evolve(rule, prob_of_one_init)
                np.save(self.path + "rule_{}_{}.npy".format(rule, prob_of_one_init), x)


if __name__ == "__main__":
    # generateByWolframCode = GenerateByWolframCode()
    # generateByWolframCode._demo()
    g = GenerateByWolframCode()
    # g.generate_dataset()
    g._show_generated_image(120, 0.5)
