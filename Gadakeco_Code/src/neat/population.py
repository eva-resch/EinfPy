from src.neat.network import Network
from time import time
from pickle import dump, load
from copy import deepcopy
import math
import random


class Population:
    """
    Class representing a whole population of 'Network' instances, each belonging to a certain generation.
    Between generations there is: selection of the fittest networks; mutation of those selected networks.

    Methods
    -------
        load_from_file(filename):
            Gets the path 'filename' for a pickeled file, then unpickles it to get the saved population.
        save_to_file(filename):
            Pickles the current population and saves it to the path 'filename'.
        create_next_generation(self): list(Network)
            Takes current generation 'self', selects and mutates to get new generation 'list(Network)'.
    """
    def __init__(self, seed, size):
        """
        Initialise a new population of 'size'=n elements of 'Network', all of which will be directly mutated by adding
        an edge.
        There are the attributes 'seed' for the random generator, 'generation_count' and an identifying 'name',
        the current time stamp.

        Parameters
        ----------
            seed: int
                For the random generator
            size: int
                The amount of instances of 'Network', that will make up the population
        """
        self.seed = seed
        self.size = size

        self.name = str(time())
        # The attribute 'generation_count' will be incremented automatically by the game Gadakeco.
        self.generation_count = 1

        self.current_generation = []
        for i in range(size):
            new = Network()
            mutated = new.edge_mutation()
            self.current_generation.append(mutated)

    @staticmethod
    def load_from_file(filename):
        pickle_in = open(filename, 'rb')
        file = load(pickle_in)
        print("called load_from_file")
        return file

    def save_to_file(self, filename):
        with open(filename, 'wb') as pickle_file:
            dump(self, pickle_file)
        print("called save_to_file")

    def create_next_generation(self):
        """
        Step 1: Take list 'current_generation', sort in descending order by return values of given 'key'-function, in
                this case by fitness value
                Since in the first generations most networks will have a similar fitness, we try to randomize the chosen
                networks.
        Step 2: Take the first 10% of the ordered 'current_generation' to use it unmodified for new generation
                -> 'new_10'
        Step 3: Make 8 deepcopies of 'new_10' for the 80% mutated by adding a new edge and use 'edge_mutation'
                Make a deepcopy of 'new_10' for the 10% mutated by adding a new node and use 'node_mutation'

        Returns
        -------
            new_generation: list(Network)
                    new generation with best networks and mutations
        """

        # TODO: Auch nach Kantenanzahl sortieren?
        # Step 1

        ordered_current_generation = sorted(self.current_generation, reverse=True, key=Network.get_fitness)
        current_size = len(ordered_current_generation)

        # Find index up to which the fitness remains unchanged
        index = 0
        max_fitness = ordered_current_generation[0].get_fitness()
        while ordered_current_generation[index+1].get_fitness() == max_fitness:
            index += 1

        # If many networks have the same fitness, shuffle them
        if index >= self.size * 0.1:
            ordered_current_generation = ordered_current_generation[:index]
            random.shuffle(ordered_current_generation)

        # Step 2

        # Keep the number of networks in a generation roughly the same by rounding up or down
        if current_size >= self.size:
            percent = math.floor(0.1 * current_size)
        else:
            percent = math.ceil(0.1 * current_size)

        # Take the needed networks to build a new generation
        new_10 = ordered_current_generation[:percent]
        new_generation = deepcopy(new_10)

        # Step 3

        for i in range(8):
            for net in new_10:
                net_copy = deepcopy(net)
                new_generation.append(net_copy.edge_mutation())

        for net in new_10:
            net_copy = deepcopy(net)
            new_generation.append(net_copy.node_mutation())

        self.current_generation = new_generation

        return self
