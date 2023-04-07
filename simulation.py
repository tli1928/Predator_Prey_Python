"""
Teng Li, Ryan Huang, Eric Wu, Anthony Gemma
DS3500 / simulation.py
Homework 5: Rabbits vs. Foxes: Modeling Ecosystems
April 6, 2023 / April 14, 2023
"""

from foxes import Fox
from rabbits import Rabbit
from field import Field
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import argparse


def animate(i, field, im, size):

    # Call generation method to continue the simulation
    field.generation()
    grass = field.field
    rabbits = field.get_rabbits()
    foxes = field.get_foxes()

    # Custom color map for the field
    cmap = plt.cm.get_cmap('PiYG')
    cmap_list = [cmap(i) for i in range(cmap.N)]
    # Set first color (grass) to white
    cmap_list[0] = (1.0, 1.0, 1.0, 1.0)
    cmap = cmap.from_list('Custom cmap', cmap_list, cmap.N)

    # Set the color of each patch
    colors = np.zeros((size, size, 4))
    colors[:, :, 1] = grass * 0.8  # Set grass color (green)
    colors[:, :, 3] = 0.5  # Set all patches to have 50% opacity
    colors[:, :, 0] = foxes * 0.8  # Set fox color (black)
    colors[:, :, 2] = rabbits * 0.8  # Set rabbit color (red)
    colors[:, :, 1][foxes > 0] = 0  # Set blue channel to 0 for foxes

    # Update the image
    im.set_array(colors)
    plt.title("generation = " + str(i))
    return im,


def main():

    # Command line arguments
    parser = argparse.ArgumentParser(description='Simulation of a predator-prey ecosystem')
    parser.add_argument('-s', '--size', type=int, default=400, help='Size of the grass field', required=False)
    parser.add_argument('-r', '--rabbits', type=int, default=1000, help='Number of initial rabbits', required=False)
    parser.add_argument('-f', '--foxes', type=int, default=1500, help='Number of initial foxes', required=False)
    parser.add_argument('-sp', '--speed', type=float, default=1, help='Speed of the simulation', required=False)
    parser.add_argument('-ggr', '--grass_growth_rate', type=float, default=0.025,
                        help='The probability that grass grows back', required=False)
    parser.add_argument('-k', '--k', type=int, default=10, help='Number of steps Foxes can go without eating', required=False)
    args = parser.parse_args()

    # Parser argument for the probability that grass grows back at any location in the next season
    if args.grass_growth_rate:
        grass_rate = args.grass_growth_rate
    else:
        grass_rate = 0.25

    # Parser argument for the size for field size
    if args.size:
        size = args.size
    else:
        size = 100

    # Parser argument for the initial number of rabbits
    if args.rabbits:
        num_rabbits = args.rabbits
    else:
        num_rabbits = 1

    # Parser argument for the initial number of foxes
    if args.foxes:
        num_foxes = args.foxes
    else:
        num_foxes = 20

    # Parser argument for the speed of the simulation
    if args.speed:
        speed = args.speed
    else:
        speed = 4

    # Parser argument for the k value of foxes
    if args.k:
        k = args.k
    else:
        k = 30

    # Create the ecosystem
    field = Field(size, grass_rate)

    # Spawn the corresponding number of rabbits and foxes
    for _ in range(num_rabbits):
        field.add_rabbit(Rabbit(size))
    for _ in range(num_foxes):
        field.add_fox(Fox(size, k))

    # Set up the image plot
    array = np.ones(shape=(size, size), dtype=int)
    fig = plt.figure(figsize=(10, 10))
    im = plt.imshow(array, cmap='PiYG', interpolation='hamming', aspect='auto', vmin=0, vmax=1)

    # Set up the animation
    anim = animation.FuncAnimation(fig, animate, fargs=(field, im, size), frames=1000000, interval=speed, repeat=True)
    plt.show()

    # Plot the change of population of grass vs. rabbits vs. foxes over time
    field.plot_pop()


if __name__ == '__main__':
    main()
