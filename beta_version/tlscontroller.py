import traci

class TrafficLight:

    def __init__(self, state):
        self.state = state
        self.nextstate = None
        self.timer = None


    def update(self):
        if self.timer and self.timer == 1:
            self.state = self.nextstate
            self.timer = None
        
        if self.timer:
            self.timer -= 1


    def set_state(self, newstate, newnext = None, timer = None):
        self.state = newstate
        self.nextstate = newnext
        self.timer = timer



class TlsController:
    
    def __init__(self, tlsid, orange_time = 4):
        self.tls_id = tlsid
        self.orange_time = 4 #4 seconds

        states = traci.trafficlight.getRedYellowGreenState(tlsid)
        self.lights = [TrafficLight(states[idx]) for idx in range(len(states))]


    def get_state_string(self):
        state = ""
        for light in self.lights:
            state += light.state
        return state


    def update(self):
        for light in self.lights:
            light.update()


    def update_states(self, states):
        for idx in range(len(states)):
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

        
        return
        for idx in range(len(self.lights)):
            # go to yellow and schedule red
            if not states[idx]:
                if self.lights[idx].state == "g":
                    self.lights[idx].set_state("y", "r", self.orange_time)
                elif self.lights[idx].state == "y":
                    pass # ignore already yellow lights
                else: self.lights[idx].set_state("r")
            # schedule green after yellows went red
            elif states[idx] and self.lights[idx].state == "r":
                print("red->green")
                self.lights[idx].set_state("r", "g", self.orange_time)
            # else its something else so we just force it
            else:

                print("last chance setting {}".format("g" if states[idx] else "r"))
                self.lights[idx].set_state("g" if states[idx] else "r")