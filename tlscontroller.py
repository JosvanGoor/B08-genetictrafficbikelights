import traci
from util import transition_program

class Lane:
    
    def __init__(self, name):
        self.name = name
        self.tl_indices = []
        self.outlanes = []
        self.vialanes = []
        
        allowed = traci.lane.getAllowed(self.name)
        self.bikelane = "bicycle" in allowed


    def print(self):
        print("{}{} controlling {} to {}, via {} respectively".format(
            "(bikelane)" if self.bikelane else "",
            self.name,
            self.tl_indices,
            self.outlanes,
            self.vialanes
        ))

class TlsController:

    # Sets up lane info & tls programs, controllable interface
    def __init__(self, tls_id, group_bikelanes = False):
        print ("--- init tlscontroller {} ---".format(tls_id))
        self.tls_id = tls_id
        self.states = []
        
        self.__init_lanes()
        self.__init_bike_states(group_bikelanes)
        self.__init_car_states()

        self.current_state = self.states[0]
        self.transitioning = False
        self.timer = self.current_state[0]
        traci.trafficlight.setRedYellowGreenState(self.tls_id, self.current_state[1])

        self.density_sets = [self.states]

        # print("- Lights")
        # for lane in self.lanes:
        #     lane.print()

        # print("- States")
        # for state in self.states:
        #     print(state)
        # print ("--- done tlscontroller {} ---\n".format(tls_id))


    def read_confs(self, low, med, high):
        self.density_sets = [self.read_conf(low), self.read_conf(med), self.read_conf(high)]
        self.states = self.density_sets[1] # assume medium

    def read_conf(self, filename):
        states = []

        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                values = line.split(" ")
                values[0] = int(values[0])
                values[2] = int(values[2])
                states.append((values[0], values[1], values[2]))
        
        return states


    def adjust_to_density(self, density):
        # limits, 0 - ?? = low, ?? - ??? = med. ???+ = high
        if density == -1:
            print("-- default state")
            #self.signal_density(3)
        elif density < 35:
            print("-- low density detected")
            self.signal_density(0)
        elif density > 75:
            print("-- med density detected")
            self.signal_density(2)
        else:
            print("-- high density detected")
            self.signal_density(1)


    # Accepts 0 (low), 1 (medium), 2(high)
    def signal_density(self, level):
        if level < 0 or level >= len(self.density_sets):
            raise "Density level not supported"
        self.states = self.density_sets[level]

    
    def update(self):
        if not self.timer == 0:
            self.timer -= 1
            return

        if self.timer == 0:
            if not self.transitioning: # we are going to now
                next = self.states[self.current_state[2]]
                
                trans = transition_program(self.current_state[1], next[1])
                if trans:
                    self.transitioning = True
                    self.timer = 3
                    traci.trafficlight.setRedYellowGreenState(self.tls_id, trans)
                    return

            self.current_state = self.states[self.current_state[2]]
            self.timer = self.current_state[0]
            self.transitioning = False
            traci.trafficlight.setRedYellowGreenState(self.tls_id, self.current_state[1])

    def modify_states(self, state):
        self.states = state
        self.current_state = self.states[0]
        self.transitioning = False
        self.timer = self.current_state[0]
        traci.trafficlight.setRedYellowGreenState(self.tls_id, self.current_state[1])
    
    # Initialized tls programs for bikes
    def __init_bike_states(self, group):
        bikelanes = []
        for lane in self.lanes:
            if lane.bikelane:
                bikelanes.append(lane)

        if group:
            self.__gen_state(bikelanes)
        else:
            for lane in bikelanes:
                self.__gen_state([lane])


    def __init_car_states(self):
        targets = \
        [
            [("north", ["south", "east"]), ("north", ["south", "west"])],
            [("north", ["south", "west"]), ("south", ["north", "east"])],
            [("east", ["north", "west"]), ("east", ["south", "west"])],
            [("east", ["south", "west"]), ("west", ["north", "east"])],
            [("south", ["north", "west"]), ("south", ["north", "east"])],
            [("west", ["north", "east"]), ("west", ["south", "east"])]
        ]

        for target in targets:
            lanes = []
            for lane in target:
                lanes.append(self.find_lane(lane[0], lane[1])[0])
            self.__gen_state(lanes)

    
    # Generates (green) program for given set of lanes
    def __gen_state(self, lanes):
        state = ["r"] * self.numlights

        for lane in lanes:
            for idx in lane.tl_indices:
                state[idx] = "G"

        self.states.append((20, "".join(state), len(self.states) - 1))


    # Gathers lane info, groups lights
    def __init_lanes(self):
        links = traci.trafficlight.getControlledLinks(self.tls_id)
        self.numlights = len(links)

        if len(links) == 0:
            return

        self.lanes = []
        for idx in range(len(links)):
            if len(self.lanes) == 0 or not (self.lanes[-1].name == links[idx][0][0]):
                self.lanes.append(Lane(links[idx][0][0]))
            self.lanes[-1].tl_indices.append(idx)
            self.lanes[-1].outlanes.append(links[idx][0][1])
            self.lanes[-1].vialanes.append(links[idx][0][2])


    def __in_any_of(self, key, lanes):
        for lane in lanes:
            if key in lane:
                return True
        return False


    def find_lane(self, start, ends, allow_bikes = False):
        starters = []
        target = []

        for lane in self.lanes:
            if start in lane.name and lane.bikelane == allow_bikes:
                starters.append(lane)

        for starter in starters:
            valid = True
            for end in ends:
                if not self.__in_any_of(end, starter.outlanes):
                    valid = False
                    break

            if valid:
                target.append(starter)

        return target

