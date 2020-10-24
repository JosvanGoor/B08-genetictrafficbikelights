from tlscontroller import TlsController
#from SUMOsim import SUMOsim
import traci
import math


class Genetic:
    def __init__(self,state):
        #TLS = TlsController()
        self.state = state
        #connection = SUMOsim()
        #self.configname = [sumoBinary, "-c","Dutch.sumocfg"]
        #connection.traci.start(self.configname)
        self.tlights = traci.trafficlight.getIDList()
        self.lanes = {tl:traci.trafficlight.getControlledLanes(tl) for tl in self.tlights}
    
    def setGenome(self,state):
        pass

    def getFitnessFunction(self,state):
        fitness = 0
        #state = self.state
        self.setGenome(state)
        #print(traci.simulation.getCollidingVehiclesNumber())
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
        if fitness == 0:
            return 100
        else:
            return 1/math.log(fitness,10)

    #Cross 2 models randomly to get final model
    def crossover(model1,model2):
        duration_1,state_1 = model1
        duration_2,state_2 = model2
        duration_final = []
        state_final = []
        for idx in range(len(duration_1)):
            if np.random.uniform() < 0.5:
                duration_final.append(duration_1[i])
            else:
                duration_final.append(duration_2[i])
        for idx in range(len(state_1)):
            if np.random.uniform() < 0.5:
                duration_final.append(state_1[i])
            else:
                duration_final.append(state_2[i])
        return duration_final,state_final
            
    def mutation(durations, states, n_duration = duration_mutation_rate, n_state = states_mutation_rate, strength = duration_mutation_strengths):
        duration_cp = list(durations)
        state_cp = list(states)
        length = len(states)
        ran_idx = np.where(np.random.uniform(size = length)<n_duration)[0]
        for idx in ran_idx:
            duration_cp[idx] += np.random.normal(scale = strength)
        for idx in range(length):
            state = list(state_cp[idx])
            for num in np.where(np.random.uniform(size = length) < n_state)[0]:
                state = np.random.choice([0,1])  
            state_cp[idx] = state
        return duration_cp,state_cp




