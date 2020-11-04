# EDIT HERE PARAMETERS OF EXPERIMENTS

import os
import traci
from sumolib import checkBinary
from random import randint
from tlscontroller import TlsController
import pickle

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


#Density is the number of vehicles per km for estimation of traffic flow
def getDensity(edgeID):
    num = traci.edge.getLastStepVehicleNumber(edgeID)
    density = num / traci.lane.getLength(edgeID + "_0") * 1000
    return density


def getJunctionDensity(listOfEdges):
    density = 0
    for edge in listOfEdges:
        density += getDensity(edge)
    return density/len(listOfEdges)


def getlaneIDs():
    tlights = traci.trafficlight.getIDList()
    lanes = {tl:traci.trafficlight.getControlledLanes(tl) for tl in tlights}
    print(lanes)
        


def runSimulation(chromosome):
    step = 0
    maxim = 0
    # Experiment options
    numveh = 350               # How many vehicles to add to the simulation
    timeOut = 50000             # When should the simulation timeout    
    
    waiting = 0
    driving = 0
    
    traci.start(SUMO_COMMAND)
    
    traci.vehicle.add("newVeh_{}".format(0), "trip_{}".format(randint(0, numroutes - 1)), "default_bicycle")
    traci.vehicle.add("newVeh_{}".format(1), "trip_{}".format(randint(0, numroutes - 1)), "default_car")
    numveh -= 2
    traci.simulationStep()

    nw_lanes = ["in_nw_south", "in_nw_east", "out_sw_north", "out_ne_west"]
    ne_lanes = ["out_nw_east", "in_ne_west", "in_ne_south", "out_se_north"]
    sw_lanes = ["out_nw_south", "in_sw_north", "in_sw_east", "out_se_west"]
    se_lanes = ["out_sw_east", "in_se_west", "out_ne_south", "in_se_north"]

    nw_controller = TlsController("junc_nw", True)
    ne_controller = TlsController("junc_ne", True)
    sw_controller = TlsController("junc_sw", True)
    se_controller = TlsController("junc_se", True)

    nw_controller.modify_states(chromosome)
    ne_controller.modify_states(chromosome)
    sw_controller.modify_states(chromosome)
    se_controller.modify_states(chromosome)

    use_saved = True
    if use_saved:
        nw_controller.read_confs("lowdensity.conf", "mediumdensity.conf", "highdensity.conf")
        ne_controller.read_confs("lowdensity.conf", "mediumdensity.conf", "highdensity.conf")
        sw_controller.read_confs("lowdensity.conf", "mediumdensity.conf", "highdensity.conf")
        se_controller.read_confs("lowdensity.conf", "mediumdensity.conf", "highdensity.conf")
        print ("----- LOADED CONFS -----")

    while traci.vehicle.getIDCount() > 0 and step < timeOut:

        nw_controller.update()
        ne_controller.update()
        sw_controller.update()
        se_controller.update()

        #get densities of the junctions
        nw_density = getJunctionDensity(nw_lanes)
        ne_density = getJunctionDensity(ne_lanes)
        sw_density = getJunctionDensity(sw_lanes)
        se_density = getJunctionDensity(se_lanes)
        
        maxim = max(maxim, nw_density, ne_density, sw_density, se_density)
        if step % 5 == 0 and numveh:
            traci.vehicle.add("newVeh_{}".format(numveh + 0), "trip_{}".format(randint(0, numroutes - 1)), "default_bicycle")
            traci.vehicle.add("newVeh_{}".format(numveh + 1), "trip_{}".format(randint(0, numroutes - 1)), "default_car")
            numveh -= 2
        
        # Twice every minute, adjust to density
        if step % 30 == 0 and use_saved:
            nw_controller.adjust_to_density(getJunctionDensity(nw_lanes))
            ne_controller.adjust_to_density(getJunctionDensity(ne_lanes))
            sw_controller.adjust_to_density(getJunctionDensity(sw_lanes))
            se_controller.adjust_to_density(getJunctionDensity(se_lanes))
        
        step += 1
        (w, d) = getActivity()
        waiting += w
        driving += d
        traci.simulationStep()
        
    fitnessValue = driving / waiting 
    getlaneIDs()
    traci.close()
    file = open("densities.txt","a")
    file.write(str(maxim))
    file.write("\n")
    file.close()     
    return fitnessValue
