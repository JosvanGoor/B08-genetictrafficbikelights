import traci
from random import randint

SUMO_BINARY = "/usr/bin/sumo-gui"
SUMO_COMMAND = [SUMO_BINARY, "-c", "SUMO/intersection.sumocfg"]
end_nodes = \
[
    "edge_center_north",
    "edge_center_east",
    "edge_center_south",
    "edge_center_west"
]

start_nodes = \
[
    "edge_north_center",
    "edge_east_center",
    "edge_south_center",
    "edge_west_center"
]
numroutes = 0

def generate_routes():
    global numroutes

    for start in range(len(start_nodes)):
        for end in range(len(end_nodes)):
            if start == end:
                continue
            traci.route.add("trip_{}".format(numroutes), [start_nodes[start], end_nodes[end]])
            numroutes += 1

def get_traffic_lights(name):

    pass



try:
    traci.start(SUMO_COMMAND)
    step = 0

    generate_routes()

    print(traci.trafficlight.getPhase("tls_center"))
    print(traci.trafficlight.getRedYellowGreenState("tls_center"))

    while step < 100000:
        if traci.simulation.getMinExpectedNumber() == 0:
            traci.vehicle.add("newVeh", "trip_{}".format(randint(0, numroutes - 1)))

        traci.simulationStep()
        step += 1

except Exception as e:
    print("Caught exception: {}".format(e))

traci.close()