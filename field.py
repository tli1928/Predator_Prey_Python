"""
Teng Li, Ryan Huang, Eric Wu, Anthony Gemma
DS3500 / field.py
Homework 5: Rabbits vs. Foxes: Modeling Ecosystems
April 6, 2023 / April 14, 2023
"""

import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import seaborn as sns


RABBIT_OFFSPRING = 4  # Max offspring when a rabbit reproduces


class Field:
    """ A field is a patch of grass with 0 or more rabbits hopping around
    in search of grass and 0 or more foxes crawling around in search of rabbits """

    def __init__(self, size, grass_rate):
        """ Create a patch of grass with dimensions SIZE x SIZE
        and initially no rabbits or foxes """
        self.size = size
        self.rabbits = []
        self.foxes = []
        self.field = np.ones(shape=(self.size, self.size), dtype=int)
        self.nrabbits = []
        self.nfoxes = []
        self.ngrass = []
        self.grass_rate = grass_rate

    def add_rabbit(self, rabbit):
        """ A new rabbit is added to the field """
        self.rabbits.append(rabbit)

    def add_fox(self, fox):
        """ A new fox is added to the field """
        self.foxes.append(fox)

    def move(self):
        """ Have both rabbits and foxes move """

        # rabbits move
        for r in self.rabbits:
            r.move()

        # foxes move
        for f in self.foxes:
            f.move()

    def eat(self):
        """ Have both rabbits and foxes eat their beloved food """

        # Rabbits eat (if they find grass where they are)
        for rabbit in self.rabbits:
            rabbit.eat(self.field[rabbit.x, rabbit.y])
            self.field[rabbit.x, rabbit.y] = 0

        # Rabbits are eaten by foxes (if they find rabbits where they are)
        for fox in self.foxes:
            # if the current location has a rabbit, EAT IT
            prey = [r for r in self.rabbits if r.x == fox.x and r.y == fox.y]
            if len(prey) > 0:
                rabbit = rnd.choice(prey)
                fox.eat(1)
                self.rabbits.remove(rabbit)

        # remove rabbits that have been eaten
        self.rabbits = [r for r in self.rabbits if r.eaten > 0]

    def survive(self):
        """ Rabbits who eat some grass live to eat another day """
        self.rabbits = [r for r in self.rabbits if r.eaten > 0]

        for fox in self.foxes:
            if fox.starve():
                self.foxes.remove(fox)
            elif fox.can_reproduce():
                self.foxes.append(fox.reproduce())

    def reproduce(self):
        """ Have both rabbits and foxes to reproduce if conditions satisfied """

        # Rabbits reproduce like rabbits.
        born_rabbits = []
        for rabbit in self.rabbits:
            for _ in range(rnd.randint(1, RABBIT_OFFSPRING)):
                born_rabbits.append(rabbit.reproduce())
        self.rabbits += born_rabbits

        # Foxes reproduce like foxes, however, they only reproduce one offspring at a time.
        born_foxes = []
        for fox in self.foxes:
            if fox.can_reproduce():
                born_foxes.append(fox.reproduce())
                fox.eaten = 0
                fox.steps_since_last_reproduce = 0
        self.foxes += born_foxes

        # Capture field state for tracking and graphing purposes in plot_pop method
        self.nrabbits.append(self.num_rabbits())
        self.nfoxes.append(self.num_foxes())
        self.ngrass.append(self.amount_of_grass())

    def grow(self):
        """ Grass grows back with some probability """
        growloc = (np.random.rand(self.size, self.size) < self.grass_rate) * 1

        self.field = np.maximum(self.field, growloc)

    def get_rabbits(self):
        """ Return a list full of rabbits. """
        rabbits = np.zeros(shape=(self.size, self.size), dtype=int)
        for r in self.rabbits:
            rabbits[r.x, r.y] = 1
        return rabbits

    def get_foxes(self):
        """ Return a list full of foxes. """
        foxes = np.zeros(shape=(self.size, self.size), dtype=int)
        for f in self.foxes:
            foxes[f.x, f.y] = 2
        return foxes

    def num_rabbits(self):
        """ Getter function to get the current number of rabbits """
        return len(self.rabbits)

    def num_foxes(self):
        """ Getter function to get the current number of foxes """
        return len(self.foxes)

    def amount_of_grass(self):
        """ Getter function to get the current number of grass """
        return self.field.sum()

    def generation(self):
        """ Run one generation of rabbits """
        self.move()
        self.eat()
        self.survive()
        self.reproduce()
        self.grow()

    def plot_pop(self):
        """ Plot the change of population of foxes vs. rabbits vs. grass """
        # Use seaborn for better quality plot
        sns.set_style('dark')

        # Initialize plot
        f, ax = plt.subplots(figsize=(8, 6))

        # Plot all three populations
        plt.plot(self.nrabbits, color="slateblue", label="Rabbits")
        plt.plot(self.ngrass, color="forestgreen", label="Grass")
        plt.plot(self.nfoxes, color="firebrick", label="Foxes")

        # Extra details to spice up the plot
        plt.grid()
        plt.xlim(0, len(self.nrabbits))
        plt.xlabel("Generations")
        plt.ylabel("Number of Organisms")
        plt.title("Organism Population Dynamics Over Time: GROW_RATE =" + str(self.grass_rate))
        plt.legend()

        plt.savefig("plot_pop.png", bbox_inches='tight')
        plt.show()

