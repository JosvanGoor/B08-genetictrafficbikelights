import numpy as np
import traci
import os
from random import randint
from random import choice
from random import shuffle
from sumolib import checkBinary
from tlscontroller import TlsController
from runSimulation import runSimulation

class genetic:
    def __init__(self, state):
        self.populationSize = 10
        self.maxTime = 60
        self.crossoverPoint = 3
        self.newPopulation = []
        self.mutationProbability = 0.5
        self.initial = state
        self.population = self.generatePopulation()
        self.fitnessValues = []
    
    # def ok(self, listToTest):
    #     for idx in range(len(listToTest)):
    #         if listToTest[idx] == idx:
    #             return False
    #     return True
    
    def newGenes(self, genome):
        # lightList = list(range(len(self.initial)))
        # while not self.ok(lightList):
        #     shuffle(lightList)
        for idx in range(len(self.initial)):
            genome.append((randint(1, 60), self.initial[idx][1], self.initial[idx][2]))
        
    # generate a new population
    def generatePopulation(self):
        population = []
        for idx in range(0, self.populationSize):
            newGenome = []
            self.newGenes(newGenome)
            population.append(newGenome)        
        return population
    
    def run(self):
        for idx in range(10):
            for genome in self.population:
                for light in genome:
                    print(light)
                self.fitnessValues.append(runSimulation(genome))
                print(self.fitnessValues)
            print("RUN {} OF 10".format(idx + 1))
               
            population = [idx for _,idx in sorted(zip(self.fitnessValues, self.population))]
            self.fitnessValues = sorted(self.fitnessValues)
            prob = [(element / sum(self.fitnessValues)) for element in self.fitnessValues]
            print(prob)

            elite = self.populationSize * 10 / 100      # 10%

            for pop_index in range(elite):              # copy the best chromosomes into the new population
                self.newPopulation.append(population[pop_index])

            for genome in range(5):
                p1 = np.random.choice(self.populationSize, 1, p = prob)[0]
                p2 = np.random.choice(self.populationSize, 1, p = prob)[0]
                print("PARENT 1 is {}".format(p1))
                print("PARENT 2 is {}".format(p2))
                parent2 = population[p1]
                parent1 = population[p2]
                self.crossover(parent1, parent2)    
                
            self.population = self.newPopulation
            self.fitnessValues = []
            self.newPopulation = []        
            print(len(self.population))
                    
    # perform single-point crossover to produce 2 new offsprings
    def crossover(self, genome1, genome2):
        newGenome1 = []
        newGenome2 = []
        # copy genes from first parent
        for idx in range(0, self.crossoverPoint):
            newGenome1.append(genome1[idx])
            newGenome2.append(genome2[idx])
        # copy gene from second parent
        for idx in range(self.crossoverPoint, len(genome2)):
            newGenome2.append(genome1[idx])
            newGenome1.append(genome2[idx])

        # add the offsprings to the new population 
        # we also try to mutate them
        self.newPopulation.append(self.mutation(newGenome1))
        self.newPopulation.append(self.mutation(newGenome2))
          
    # function to try and mutate the genome by changing one its genes
    # in our case this means selecting a random traffic light configuration 
    # and changing its time and also the next light that is going to be green    
    def mutation(self, genome):
        if np.random.random() <= self.mutationProbability:
            idx = randint(0, len(genome))
            print(idx)
            genome[idx][0] = randint(1, self.maxTime)                   # time
            # gene[2] = randint(0, len(genome))                   # next light
        return genome
