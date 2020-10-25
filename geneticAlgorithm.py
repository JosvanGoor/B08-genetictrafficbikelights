import numpy as np
from random import randint
class gene:
    def __init__(self, time, nextGenome):
        self.time = time
        self.next = nextGenome
        
class genetic:
    def __init__(self, population):
        self.population = population
        self.crossoverPoint = 4
        self.newPopulation = []
        self.mutationProbability = 0.01
    
    def calculateFitness(self, population):
        pass
    
    # perform 1-point crossover to produce 2 new offsprings
    def crossover(self, genome1, genome2):
        newGenome1 = []
        newGenome2 = []
        # copy genes from first parent
        for idx in range(0, self.crossoverPoint):
            newGenome1[idx] = genome1[idx]
            newGenome2[idx] = genome2[idx]
        # copy gene from second parent
        for idx in range(self.crossoverPoint + 1, len(genome2)):
            newGenome2[idx] = genome2[idx]
            newGenome1[idx] = genome1[idx]

        # add the offsprings to the new population 
        # we also try to mutate them
        self.newPopulation.append(mutation(newGenome1))
        self.newPopulation.append(mutation(newGenome2))
    
    # function to try and mutate the genome by changing one its genes
    # in our case this means selecting a random traffic light and changing its
    # time and also the next light that is going to be green    
    def mutation(self, genome):
        if np.random.random() < self.mutationProbability:
            gene = genome[randint(0, 8)]
            gene[0] += randint(1, 60)
            gene[2] = randint(0, 8)
        else:
            pass            
    
    
        
            
        