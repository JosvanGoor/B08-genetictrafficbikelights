from tlscontroller import TlsController
from SUMOsim import SUMOsim

class Genetic():
    def __init__(self,state):
        self.state = TlsController.get_state_string
        connection = SUMOsim()
        self.configname = [sumoBinary, "-c","Dutch.sumocfg"]
        connection.traci.start(self.configname)
    
    def setGenome(self,state):
        pass

    def getFitnessFunction(self):
        fitness = 0
        state = self.state
        self.setGenome(State)
        if connection.traci.getCollidingVehiclesNumber() > 0:
			# break the current simulation and penalize the genome's fitness
            collision_penalty = connection.traci.getCollidingVehiclesNumber()
			fitness += collision_penalty
			break
        timeWaiting = 0
        timeWaiting = connection.traci.getWaitingTime()
        fitness += timeWaiting
        fitness = 1/fitness
        return fitness


