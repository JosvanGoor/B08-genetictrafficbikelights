import traci

# Simple structure for storing state for a single TL
class TrafficLight:

    def __init__(self, state):
        self.state = state
        self.nextstate = None
        self.timer = None


    # timed updater
    def update(self):
        if self.timer and self.timer == 1:
            self.state = self.nextstate
            self.timer = None
        
        if self.timer:
            self.timer -= 1


    # shorthand for state update
    def set_state(self, newstate, newnext = None, timer = None):
        self.state = newstate
        self.nextstate = newnext
        self.timer = timer


# Simple controller that ensures that traffic lights go from
# green to red via yellow without the underlying algorithm having
# to worry about that
class TlsController:
    
    def __init__(self, tlsid, orange_time = 4):
        self.tls_id = tlsid
        self.orange_time = orange_time #4 seconds

        states = traci.trafficlight.getRedYellowGreenState(tlsid)
        self.lights = [TrafficLight(states[idx]) for idx in range(len(states))]
        ids = traci.trafficlight.getIDList()
        for id in ids:
            print(traci.)

    # Generates state string required for setRedYellowGreen
    def get_state_string(self):
        state = ""
        for light in self.lights:
            state += light.state
        return state


    # runs timer updates
    def update(self):
        for light in self.lights:
            light.update()


    # sets new TL states
    def update_states(self, states):
        for idx in range(len(states)):
            print(idx)
            if states[idx]:
                # lane should turn green
                if self.lights[idx].state == "g": continue
                if self.lights[idx].nextstate == "g": continue
                # set green after oranges went red
                self.lights[idx].set_state(self.lights[idx].state, "g", self.orange_time)
            else:
                # lane should turn red
                if self.lights[idx].state == "r" or self.lights[idx].state == "y":
                    continue # already transitioning or red
                self.lights[idx].set_state("y", "r", self.orange_time)