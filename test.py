import traci
import os
from sumolib import checkBinary
from random import randint
from tlscontroller import TlsController

# This makes sure that it works on both Windows and Unix
if 'SUMO_HOME' in os.environ :
    SUMO_BINARY = checkBinary('sumo')       # for Win
else :
    SUMO_BINARY = "/usr/bin/sumo"               # for Unix

SUMO_COMMAND = [SUMO_BINARY, "-c", "quadintersection/quad.sumocfg"]
numroutes = 55


def generate_routes():
    global numroutes

    edges = traci.edge.getIDList()
    startedges = []
    endedges = []

    for edge in edges:
        if "start" in edge:
            startedges.append(edge)
        elif "end" in edge:
            endedges.append(edge)

    for start in range(len(startedges)):
        for end in range(len(endedges)):
            if start == end:
                continue
            traci.route.add("trip_{}".format(numroutes), [startedges[start], endedges[end]])
            print("<route edges=\"{}\" id=\"trip_{}\"/>".format((startedges[start], endedges[end]),numroutes))
            numroutes += 1

# generate_routes()

def getDensity(edgeID):
    num = traci.edge.getLastStepVehicleNumber(edgeID)
    density = num/traci.lane.getLength(edgeID + "_0")/1000
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
        

def runSimulation(geneticState):
    traci.start(SUMO_COMMAND)
    step = 0
    traci.vehicle.add("newVeh_{}".format(0), "trip_{}".format(randint(0, numroutes - 1)), "default_bicycle")
    traci.vehicle.add("newVeh_{}".format(1), "trip_{}".format(randint(0, numroutes - 1)), "default_car")
    numveh = 2

    #to be filled in by Jos, the arrays of the lanes that lead to the junction
    nw_lanes = []
    ne_lanes = []
    sw_lanes = []
    se_lanes = []

    nw_controller = TlsController("junc_nw", True)
    ne_controller = TlsController("junc_ne", False)
    sw_controller = TlsController("junc_sw", True)
    se_controller = TlsController("junc_se", False)

    #get densities of the junctions
    nw_density = getJunctionDensity(nw_lanes)
    ne_density = getJunctionDensity(ne_lanes)
    sw_density = getJunctionDensity(sw_lanes)
    se_density = getJunctionDensity(se_lanes)

    nw_controller = geneticState
    ne_controller = geneticState
    sw_controller = geneticState
    se_controller = geneticState
        
    while step < 1000:
        traci.simulationStep()

        nw_controller.update()
        ne_controller.update()
        sw_controller.update()
        se_controller.update()

        if step % 5 == 0:
            traci.vehicle.add("newVeh_{}".format(numveh + 0), "trip_{}".format(randint(0, numroutes - 1)), "default_bicycle")
            traci.vehicle.add("newVeh_{}".format(numveh + 1), "trip_{}".format(randint(0, numroutes - 1)), "default_car")
            numveh += 2
        step += 1
    traci.close()

## Do stuff
# links = traci.trafficlight.getControlledLinks("junc_nw")
# for link in links:
#     print(link)

# from util import transition_program
# print(transition_program(controller.states[1], controller.states[1]))

