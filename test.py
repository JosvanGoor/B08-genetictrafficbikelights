import traci
import os
from sumolib import checkBinary
from random import randint
from tlscontroller import TlsController

# This makes sure that it works on both Windows and Unix
if 'SUMO_HOME' in os.environ :
    SUMO_BINARY = checkBinary('sumo-gui')       # for Win
else :
    SUMO_BINARY = "/usr/bin/sumo"           # for Unix

SUMO_COMMAND = [SUMO_BINARY, "-c", "quadintersection/quad.sumocfg"]
numroutes = 0

traci.start(SUMO_COMMAND)
step = 0

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
            numroutes += 1



generate_routes()
traci.vehicle.add("newVeh_{}".format(0), "trip_{}".format(randint(0, numroutes - 1)), "default_bicycle")
traci.vehicle.add("newVeh_{}".format(1), "trip_{}".format(randint(0, numroutes - 1)), "default_car")
numveh = 2


nw_controller = TlsController("junc_nw", True)
ne_controller = TlsController("junc_ne", False)
sw_controller = TlsController("junc_sw", True)
se_controller = TlsController("junc_se", False)

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


## Do stuff
# links = traci.trafficlight.getControlledLinks("junc_nw")
# for link in links:
#     print(link)

# from util import transition_program
# print(transition_program(controller.states[1], controller.states[1]))

traci.close()