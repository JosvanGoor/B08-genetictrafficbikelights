#from tlscontroller import TlsController
#from SUMOsim import SUMOsim
import traci



class Genetic:
    def __init__(self,state):
        #TLS = TlsController()
        self.state = state
        #connection = SUMOsim()
        #self.configname = [sumoBinary, "-c","Dutch.sumocfg"]
        #connection.traci.start(self.configname)
        self.tlights = traci.trafficlight.getIDList()
        for tl in self.tlights:
            print(traci.trafficlight.getControlledLanes(tl))
        self.lanes = {tl:traci.trafficlight.getControlledLanes(tl) for tl in self.tlights}
    
    def setGenome(self,state):
        pass

    def getFitnessFunction(self,state):
        fitness = 0
        #state = self.state
        self.setGenome(state)
        print(traci.simulation.getCollidingVehiclesNumber())
        if traci.simulation.getCollidingVehiclesNumber() > 0:
			# break the current simulation and penalize the genome's fitness
            collision_penalty = traci.simulation.getCollidingVehiclesNumber()
            fitness += collision_penalty
            #fitness = 1/fitness
        timeWaiting = 0
        for laneid in self.lanes.values():
            for lane in laneid:
                timeWaiting = traci.lane.getWaitingTime(lane)
                fitness += timeWaiting
        #print(fitness)
        return fitness


