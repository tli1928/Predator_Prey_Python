"""
Teng Li, Ryan Huang, Eric Wu, Anthony Gemma
DS3500 / foxes.py
Homework 5: Rabbits vs. Foxes: Modeling Ecosystems
April 6, 2023 / April 14, 2023
"""

import random as rnd
import copy

WRAP = False  # Does the field wrap around on itself when rabbits move?


class Fox:
    """ A sleek predator prowling through the grass field in search of rabbits to hunt.
    Mrs. Fox must catch enough rabbits to survive and reproduce her young, otherwise she will also starve """

    def __init__(self, size, k):
        self.size = size
        self.x = rnd.randrange(0, size)
        self.y = rnd.randrange(0, size)
        self.eaten = 0
        self.steps_without_eaten = 0
        self.steps_since_last_reproduce = 0
        self.k = k

    def move(self):
        """ Move in four directions in a random mannor """
        if WRAP:
            self.x = (self.x + rnd.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4])) % self.size
            self.y = (self.y + rnd.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4])) % self.size
        else:
            self.x = min(self.size - 1, max(0, (self.x + rnd.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4]))))
            self.y = min(self.size - 1, max(0, (self.y + rnd.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4]))))

        self.steps_without_eaten += 1
        self.steps_since_last_reproduce += 1

    def reproduce(self):
        """ Reproduce one offspring fox and reset some counter variables """
        self.eaten = 0
        self.steps_since_last_reproduce = 0
        return copy.deepcopy(self)

    def eat(self, amount):
        """ Eat one rabbit, and reset and increment some counter variables """
        self.eaten += amount
        self.steps_without_eaten = 0
        self.steps_since_last_reproduce += 1

    def can_reproduce(self):
        """ Returns True if the fox can reproduce """
        return self.eaten > 0

    def starve(self):
        """ Returns True if the fox starves """
        return self.steps_without_eaten >= self.k
