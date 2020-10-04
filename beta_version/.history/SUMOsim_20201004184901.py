from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import numpy as np
import optparse
import random

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), 'tools'))
else:
    print("it works")
    sys.path.append(os.path.join(
        'C:\Program Files (x86)\Eclipse\Sumo', 'tools'))


import traci
from genetic import Genetic
from sumolib import checkBinary  # noqa
from tlscontroller import TlsController



def run():
    """execute the TraCI control loop"""
    step = 0
    state = [0]*32
    TLS = TlsController("tls_center")
    GN = Genetic(state)

    while traci.simulation.getMinExpectedNumber() > 0:
        #We do things here to get the flow going
        if step % 12 == 0: # atm we change every 12 steps, this is a stub
            state = []
            for i in range(32):
                state.append(random.randint(0, 1) == 0)
            TLS.update_states(state)
        
        TLS.update()
        traci.trafficlight.setRedYellowGreenState("tls_center", TLS.get_state_string())
        print(GN.getFitnessFunction(state))
        traci.simulationStep()
        step += 1

    traci.close()
    sys.stdout.flush()


if __name__ == "__main__":
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action = "store_true",default = False, help = "run the commandline version of sumo")
    options, args = optParser.parse_args()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

        # first, generate the route file for this simulation
        #generate_routefile()

        # this is the normal way of using traci. sumo is started as a
        # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c","intersection.sumocfg"])


run()


