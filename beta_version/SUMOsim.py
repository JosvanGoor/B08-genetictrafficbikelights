# from __future__ import absolute_import
# from __future__ import print_function
import os
import sys
import numpy as np
import optparse
from random import randint

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), 'tools'))
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


import traci
from genetic import Genetic
from sumolib import checkBinary  # noqa
from tlscontroller import TlsController

from traci import StepListener


num_routes = 0
veh_num = 0

def generate_routes():
    global num_routes

    for start in range(len(start_nodes)):
        for end in range(len(end_nodes)):
            if start == end:
                continue
            traci.route.add("trip_{}".format(num_routes), [start_nodes[start], end_nodes[end]])
            num_routes += 1

def add_vehicle(veh_type):
    global veh_num
    route = "trip_{}".format(randint(0, num_routes - 1))
    traci.vehicle.add("{}".format("vehicle_{}".format(veh_num)), route, veh_type)
    veh_num += 1

def run():
    """execute the TraCI control loop"""
    step = 0
    state = [0] * 28
    TLS = TlsController("tls_center")
    GN = Genetic(state)
    
    generate_routes()
    for _ in range(3):
        add_vehicle("default_bicycle")
        add_vehicle("default_car")

    while traci.simulation.getMinExpectedNumber() > 0:
        #We do things here to get the flow going
        if step % 12 == 0: # atm we change every 12 steps, this is a stub
            state = []
            for _ in range(28):
                state.append(randint(0, 1) == 0)
            TLS.update_states(state)
        
        if step % 5 == 0:
            add_vehicle("default_bicycle")
            add_vehicle("default_car")

        TLS.update()
        traci.trafficlight.setRedYellowGreenState("tls_center", TLS.get_state_string())
        print(GN.getFitnessFunction(state))
        traci.simulationStep()
        step += 1
        print("Step #{}".format(step))

    print ("Simulation ended.")
    traci.close()
    sys.stdout.flush()


if __name__ == "__main__":
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action = "store_true", default = False, help = "run the commandline version of sumo")
    options, args = optParser.parse_args()
    
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    traci.start([sumoBinary, "-c","intersection.sumocfg"])

run()


