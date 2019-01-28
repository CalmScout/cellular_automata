"""
Contains classes for cellular automata behaviour simulation.
"""
import numpy as np
import os
import matplotlib.pyplot as plt     # auxiliary module, only for demo is used
from useful_functions import load_obj, generate_rules_rand_1d_no_memory
from constants import data_path_no_memory, size, steps, neighb_rad, num_of_cell_states


class CA:
    """
    Simulate 1D CA with cyclic boundary conditions.
    """
    def __init__(self, path=data_path_no_memory, size=size, steps=steps,
                 neighb_radius=neighb_rad, states=num_of_cell_states):
        self.path = path
        self.size = size
        self.steps = steps
        self.neighb_radius = neighb_radius
        self.num_of_cell_states = states
        self.rules = None
        self.x = None
        self.id_str = None
        if len(os.listdir(self.path)) == 0:
            generate_rules_rand_1d_no_memory(self)
        else:
            # should be redone for random '.pkl' file
            self.rules = load_obj(self.path, "L2I5ZK")
            self.id_str = "L2I5ZK"

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

    def evolve(self):
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

    def show_generated_image(self):
        im = np.load(self.path + self.id_str + ".npy")
        plt.imshow(im, cmap=plt.cm.binary)
        plt.show()

    def print_rules(self):
        print(self.rules)


if __name__ == "__main__":
    g = CA()
    g.evolve()
    g.show_generated_image()
    g.print_rules()
