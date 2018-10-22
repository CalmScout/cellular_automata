import numpy as np
import matplotlib.pyplot as plt


class CA:
    """
    Class that encapsulates behaviour of CA we want to predict.
    CA has 2D grid.
    """

    def __init__(self, n=100, m=100, t=200, threshold_ones_init=0.15):
        self.n = n  # Sizes of the grid
        self.m = m
        self.t = t  # The maximum number of generations

        # Set up random initial configuration of the grid
        self.old_grid = (np.random.uniform(low=0.0, high=1.0, size=(n, m)) <= threshold_ones_init).astype(int)
        self.new_grid = np.zeros(n * m, dtype='i').reshape(n, m)

    def count_alive_neighbours(self, i, j):     # SHOULD BE REWRITTEN WITH THE USAGE OF NUMPY SLICES
        """
        Returns the number of alive neighbours around point (i, j)
        """
        counter = 0  # The total number of live neighbours.
        # Loop over all the neighbours.
        for x in [i - 1, i, i + 1]:
            for y in [j - 1, j, j + 1]:
                if x == i and y == j:
                    continue  # Skip the current point itself - we only want to count the neighbours!
                if x != self.n and y != self.m:
                    counter += self.old_grid[x][y]
                # The remaining branches handle the case where the neighbour is off the end of the grid.
                # In this case, we loop back round such that the grid becomes a "toroidal array".
                elif x == self.n and y != self.m:
                    counter += self.old_grid[0][y]
                elif x != self.n and y == self.m:
                    counter += self.old_grid[x][0]
                else:
                    counter += self.old_grid[0][0]
        return counter

    def play(self):     # SHOULD BE REWRITTEN WITH UTILIZING THE GENERAL CELLULAR AUTOMATA FRAMEWORK
        """
        Play Conway's Game of Life
        """
        # Write the initial configuration to file.
        plt.pcolormesh(self.old_grid)
        plt.colorbar()
        plt.savefig("generation0.png")

        time = 1  # Current time level
        write_frequency = 1  # How frequently we want to output a grid configuration.
        while time <= self.t:  # Evolve!
            print("At time level %d", time)

            # Loop over each cell of the grid and apply Conway's rules.
            for i in range(self.n):
                for j in range(self.m):
                    live = self.count_alive_neighbours(i, j)
                    if self.old_grid[i][j] == 1 and live < 2:
                        self.new_grid[i][j] = 0  # Dead from starvation.
                    elif self.old_grid[i][j] == 1 and (live == 2 or live == 3):
                        self.new_grid[i][j] = 1  # Continue living.
                    elif self.old_grid[i][j] == 1 and live > 3:
                        self.new_grid[i][j] = 0  # Dead from overcrowding.
                    elif self.old_grid[i][j] == 0 and live == 3:
                        self.new_grid[i][j] = 1  # Alive from reproduction.

            # Output the new configuration.
            if time % write_frequency == 0:
                plt.pcolormesh(self.new_grid)
                plt.savefig("generation%d.png" % time)

            # The new configuration becomes the old configuration for the next generation.
            self.old_grid = self.new_grid.copy()

            # Move on to the next time level
            time += 1


if __name__ == "__main__":
    game = CA(n=100, m=100)
    game.play()
