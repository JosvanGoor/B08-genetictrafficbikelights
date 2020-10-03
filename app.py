import traci
from random import randint

SUMO_BINARY = "/usr/bin/sumo-gui"
SUMO_COMMAND = [SUMO_BINARY, "-c", "SUMO/intersection.sumocfg"]
end_nodes = ["edge_center_north", "edge_center_east", "edge_center_south", "edge_center_west"]
start_nodes = ["edge_north_center", "edge_east_center", "edge_south_center", "edge_west_center"]
numroutes = 0

def generate_routes():
    global numroutes

    for start in range(len(start_nodes)):
        for end in range(len(end_nodes)):
            if start == end:
                continue
            traci.route.add("trip_{}".format(numroutes), [start_nodes[start], end_nodes[end]])
            numroutes += 1

def close_empty_lanes():
    # lanes = traci.trafficlight.getControlledLanes("tls_center")
    links = traci.trafficlight.getControlledLinks("tls_center")
    # state = traci.trafficlight.getRedYellowGreenState("tls_center")

    tls = [None] * 32
    for idx in range(32):
        tls[idx] = ["r", links[idx][0][0], links[idx][0][1], links[idx][0][2]]
    
    vehicles = traci.vehicle.getIDList()
    for vehicle in vehicles:
        lane = traci.vehicle.getLaneID(vehicle)

        for idx in range(32):
            if tls[idx][1] == lane:
                tls[idx][0] = "g"

    states = ""
    for idx in range(32):
        states += tls[idx][0]
    print("states: {}".format(states))
    traci.trafficlight.setRedYellowGreenState("tls_center", states)

# try:
traci.start(SUMO_COMMAND)
step = 0

generate_routes()

print(traci.trafficlight.getPhase("tls_center"))

while step < 10000:
    if traci.simulation.getMinExpectedNumber() == 0:
        traci.vehicle.add("newVeh", "trip_{}".format(randint(0, numroutes - 1)))
        traci.vehicle.add("newVeh2", "trip_{}".format(randint(0, numroutes - 1)))
    
    close_empty_lanes()

    traci.simulationStep()
    step += 1

# except Exception as e:
#     print("Caught exception: {}".format(e))

traci.close()