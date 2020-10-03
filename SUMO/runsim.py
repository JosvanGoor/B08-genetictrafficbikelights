from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import numpy as np
import optparse

class SumoEnv:
    place_len = 7.5
    place_offset = 8.50
    lane_len = 10
    lane_ids = ['-gneE4_0', '-gneE4_1','-gneE4_2', '-gneE4_3','-gneE5_0', '-gneE5_1','-gneE5_2', '-gneE5_3','-gneE6_0', '-gneE6_1','-gneE6_2', '-gneE6_3','-gneE7_0', '-gneE7_1','-gneE7_2', '-gneE7_3']

    def __init__(self, label='default', gui_f=False):
        self.label = label
        self.wt_last = 0.
        self.ncars = 0
        self.nbikes = 0

        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("please declare environment variable 'SUMO_HOME'")

        exe = 'sumo-gui' if gui_f else 'sumo'
        sumoBinary = os.path.join(os.environ['SUMO_HOME'], 'bin', exe)
        self.sumoCmd = [sumoBinary, '-c', 'Dutch.sumocfg']

        return

    def get_state_d(self):
        state = np.zeros(self.lane_len * 8 + 5, dtype=np.float32)

        for ilane in range(0, 8):
            lane_id = self.lane_ids[ilane]
            ncars = traci.lane.getLastStepVehicleNumber(lane_id)
            print (ncars)
            cars = traci.lane.getLastStepVehicleIDs(lane_id)
            for icar in cars:
                xcar, ycar = traci.vehicle.getPosition(icar)
                if ilane < 2:
                    pos = (ycar - self.place_offset) / self.place_len
                    print (pos)
                elif ilane < 4:
                    pos = (xcar - self.place_offset) / self.place_len
                    print (pos)
                elif ilane < 6:
                    pos = (-ycar - self.place_offset) / self.place_len
                    print (pos)
                else:
                    pos = (-xcar - self.place_offset) / self.place_len
                    print (pos)
                if pos > self.lane_len - 1.:
                    continue
                pos = np.clip(pos, 0., self.lane_len - 1. - 1e-6)
                ipos = int(pos)
                state[int(ilane * self.lane_len + ipos)] += 1. - pos + ipos
                state[int(ilane * self.lane_len + ipos + 1)] += pos - ipos
            state[self.lane_len * 8:self.lane_len * 8+5] = np.eye(5)[traci.trafficlight.getPhase('gneJ10')]
        return state

    def step_d(self, action):
        done = False
        traci.switch(self.label)

        action = np.squeeze(action)
        traci.trafficlight.setPhase('gneJ10', action)

        traci.simulationStep()
        traci.simulationStep()

        self.ncars += traci.simulation.getDepartedNumber()

        state = self.get_state_d()

        wt = 0
        for ilane in range(0, 8):
            lane_id = self.lane_ids[ilane]
            wt += traci.lane.getWaitingTime(lane_id)
        reward = - (wt - self.wt_last)*0.004

        if self.ncars > 250:
            done = True

        return state, reward, done, np.array([[reward]])


    def run(self):
        """execute the TraCI control loop"""
        step = 0
        # we start with phase 2 where EW has green
        # I dont know what the traffic light ID is

        #print (traci.trafficlight.getIDList)
        traci.trafficlight.setPhase("gneJ10", 2)
        while traci.simulation.getMinExpectedNumber() > 0:
            #print(traci.simulation.getMinExpectedNumber())
            traci.simulationStep()
            if traci.trafficlight.getPhase("gneJ10") == 2:
                # we are not already switching
                #if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
                    # there is a vehicle from the north, switch
                    #traci.trafficlight.setPhase("0", 3)
                #else:
                    # otherwise try to keep green for EW
                traci.trafficlight.setPhase("gneJ10", 4)
            elif traci.trafficlight.getPhase("gneJ10") ==4:
                traci.trafficlight.setPhase("gneJ10", 3)
            elif traci.trafficlight.getPhase("gneJ10") ==3:
                traci.trafficlight.setPhase("gneJ10", 2)
            print(traci.trafficlight.getPhase("gneJ10")) 
            
            step += 1
            print (self.get_state_d())
        traci.close()
        sys.stdout.flush()

    def reset(self):
        self.wt_last = 0.
        self.ncars = 0
        self.nbikes = 0
        traci.start(self.sumoCmd, label=self.label)
        traci.trafficlight.setProgram('gneJ10', '0')
        traci.simulationStep()
        #return self.get_state_d()

    def close(self):
        traci.close()


if __name__ == "__main__":
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")

    import traci
    from sumolib import checkBinary  # noqa
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    #generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c","Dutch.sumocfg"])
    s = SumoEnv()
    s.run()
