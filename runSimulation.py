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

def runSimulation(geneticState):
    step = 0
    
    # Experiment options
    numveh = 100               # How many vehicles to add to the simulation
    timeOut = 200             # When should the simulation timeout    
    
    traci.start(SUMO_COMMAND)
    
    traci.vehicle.add("newVeh_{}".format(0), "trip_{}".format(randint(0, numroutes - 1)), "default_bicycle")
    traci.vehicle.add("newVeh_{}".format(1), "trip_{}".format(randint(0, numroutes - 1)), "default_car")
    numveh -= 2
    traci.simulationStep()

    nw_controller = TlsController("junc_nw", True)
    ne_controller = TlsController("junc_ne", True)
    sw_controller = TlsController("junc_sw", True)
    se_controller = TlsController("junc_se", True)

    nw_controller.modify_states(geneticState)
    ne_controller.modify_states(geneticState)
    sw_controller.modify_states(geneticState)
    se_controller.modify_states(geneticState)

    while traci.vehicle.getIDCount() > 0 and step < timeOut:

        nw_controller.update()
        ne_controller.update()
        sw_controller.update()
        se_controller.update()

        if step % 5 == 0 and numveh:
            traci.vehicle.add("newVeh_{}".format(numveh + 0), "trip_{}".format(randint(0, numroutes - 1)), "default_bicycle")
            traci.vehicle.add("newVeh_{}".format(numveh + 1), "trip_{}".format(randint(0, numroutes - 1)), "default_car")
            numveh -= 2
        step += 1
        traci.simulationStep()
        
    fitnessValue = step / 3600      # How many irl hours did the simulation take
    traci.close()
    return fitnessValue