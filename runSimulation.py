# EDIT HERE PARAMETERS OF EXPERIMENTS

import os
import traci
from sumolib import checkBinary
from random import randint
from tlscontroller import TlsController

if 'SUMO_HOME' in os.environ :
    SUMO_BINARY = checkBinary('sumo')           # for Win
else :
    SUMO_BINARY = "/usr/bin/sumo"               # for Unix

SUMO_COMMAND = [SUMO_BINARY, "-c", "quadintersection/quad.sumocfg"]
numroutes = 55

def getActivity():
    waiting = 0
    driving = 0

    vehicles = traci.vehicle.getIDList()
    for veh in vehicles:
        if traci.vehicle.getSpeed(veh) < 0.1:
            waiting += 1
        else:
            driving += 1

    return (waiting, driving)

def runSimulation(chromosome):
    step = 0
    
    # Experiment options
    numveh = 100               # How many vehicles to add to the simulation
    timeOut = 50000             # When should the simulation timeout    
    
    waiting = 0
    driving = 0
    
    traci.start(SUMO_COMMAND)
    
    traci.vehicle.add("newVeh_{}".format(0), "trip_{}".format(randint(0, numroutes - 1)), "default_bicycle")
    traci.vehicle.add("newVeh_{}".format(1), "trip_{}".format(randint(0, numroutes - 1)), "default_car")
    numveh -= 2
    traci.simulationStep()

    nw_controller = TlsController("junc_nw", True)
    ne_controller = TlsController("junc_ne", True)
    sw_controller = TlsController("junc_sw", True)
    se_controller = TlsController("junc_se", True)

    nw_controller.modify_states(chromosome)
    ne_controller.modify_states(chromosome)
    sw_controller.modify_states(chromosome)
    se_controller.modify_states(chromosome)

    while traci.vehicle.getIDCount() > 0 and step < timeOut:

        nw_controller.update()
        ne_controller.update()
        sw_controller.update()
        se_controller.update()

        if step % 10 == 0 and numveh:
            traci.vehicle.add("newVeh_{}".format(numveh + 0), "trip_{}".format(randint(0, numroutes - 1)), "default_bicycle")
            traci.vehicle.add("newVeh_{}".format(numveh + 1), "trip_{}".format(randint(0, numroutes - 1)), "default_car")
            numveh -= 2
        step += 1
        (w, d) = getActivity()
        waiting += w
        driving += d
        traci.simulationStep()
        
    fitnessValue = driving / waiting 
    traci.close()     
    return fitnessValue
