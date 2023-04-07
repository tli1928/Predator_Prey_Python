
"""
Teng Li, Ryan Huang, Eric Wu, Anthony Gemma
DS3500 / rabbits.py
Homework 5: Rabbits vs. Foxes: Modeling Ecosystems
April 6, 2023 / April 14, 2023
"""

import random as rnd
import copy

WRAP = False  # Does the field wrap around on itself when rabbits move?


class Rabbit:
    """ A furry creature roaming a field in search of grass to eat.
    Mr. Rabbit must eat enough to reproduce, otherwise he will starve. """

    def __init__(self, size):
        self.size = size
        self.x = rnd.randrange(0, size)
        self.y = rnd.randrange(0, size)
        self.eaten = 0

    def reproduce(self):
        """ Make a new rabbit at the same location.
         Reproduction is hard work! Each reproducing
         rabbit's eaten level is reset to zero. """
        self.eaten = 0
        return copy.deepcopy(self)

    def eat(self, amount):
        """ Feed the rabbit some grass """
        self.eaten += amount

    def move(self):
        """ Move up, down, left, right randomly by one block """
        if WRAP:
            self.x = (self.x + rnd.choice([-1, 0, 1])) % self.size
            self.y = (self.y + rnd.choice([-1, 0, 1])) % self.size
        else:
            self.x = min(self.size - 1, max(0, (self.x + rnd.choice([-1, 0, 1]))))
            self.y = min(self.size - 1, max(0, (self.y + rnd.choice([-1, 0, 1]))))
