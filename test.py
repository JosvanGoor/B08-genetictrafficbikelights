
import traci
from random import randint

SUMO_BINARY = "/usr/bin/sumo"
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

# while step < 10000:
#     traci.simulationStep()

#     if step % 5 == 0:
#         traci.vehicle.add("newVeh_{}".format(numveh + 0), "trip_{}".format(randint(0, numroutes - 1)), "default_bicycle")
#         traci.vehicle.add("newVeh_{}".format(numveh + 1), "trip_{}".format(randint(0, numroutes - 1)), "default_car")
#         numveh += 2


## Do stuff
# links = traci.trafficlight.getControlledLinks("junc_nw")
# for link in links:
#     print(link)


from tlscontroller import TlsController
controller = TlsController("junc_nw", True)

from util import transition_program
print(transition_program(controller.programs[1], controller.programs[1]))

traci.close()