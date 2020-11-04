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
        self.populationSize = 20
        self.maxTime = 60
        self.crossoverPoint = 3
        self.newPopulation = []
        self.mutationProbability = 0.01
        self.initial = state
        self.population = self.generatePopulation()
        self.fitnessValues = []
        self.file = open("results.txt","a")
        self.iterations = 20
        self.avgFit = []
        self.stdFit = []
    
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
        for idx in range(self.iterations):
            file = open("results.txt","a")
            for genome in self.population:
                for light in genome:
                    print(light)
                self.fitnessValues.append(runSimulation(genome))
                                
            file.write("RUN {} of {} \n".format(idx + 1, self.iterations))
            
            # order the the chromosomes from high to low based on their fitness
            population = [idx for _,idx in sorted(zip(self.fitnessValues, self.population), reverse = True)]  
            
            # order the fitness from high to low
            self.fitnessValues = sorted(self.fitnessValues, reverse = True)
            prob = [(element / sum(self.fitnessValues)) for element in self.fitnessValues]
            
            file.write("Avg. Fitness:{} sd {} \n".format(np.mean(self.fitnessValues), np.std(self.fitnessValues)))
            
            self.avgFit.append(np.mean(self.fitnessValues))
            self.stdFit.append(np.std(self.fitnessValues))
            
            elite = int(self.populationSize * 10 / 100)         # 10%    
            for pop_index in range(elite):                      # copy the best chromosomes into the new population
                self.newPopulation.append(population[pop_index])

            while len(self.newPopulation) < self.populationSize:
                p1 = np.random.choice(self.populationSize, 1, p = prob)[0]
                p2 = np.random.choice(self.populationSize, 1, p = prob)[0]
                
                parent1 = population[p1]
                parent2 = population[p2]
                self.crossover(parent1, parent2)
                if len(self.newPopulation) > self.populationSize:
                    self.newPopulation.pop()
                
            self.population = self.newPopulation
            self.fitnessValues = []
            self.newPopulation = []
            file.close()
        file = open("results.txt","a")
        file.write("Average deviation: \n")
        for element in self.avgFit:
            file.write(str(element)+" ")
        file.write("\n Standard deviation: \n")
        for element in self.stdFit:
            file.write(str(element)+" ")
        file.write("BEST CONFIGURATION \n")
        file.write(str(self.population[0]))
        file.close()            
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
          
    # function that modifies the times of a chromosomes    
    def mutation(self, chromosome):
        if np.random.random() <= self.mutationProbability:
            newChromosome = []                                          # time
            for idx in range(len(self.initial)):
                newChromosome.append((randint(1, 60), self.initial[idx][1], self.initial[idx][2]))
            return newChromosome
        return chromosome
