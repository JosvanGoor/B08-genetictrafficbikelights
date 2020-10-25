import traci
import os
from random import randint
from beta_version import tlscontroller as tlsc
from sumolib import checkBinary

# This makes sure that it works on both Windoews and Unix
if 'SUMO_HOME' in os.environ :
    SUMO_BINARY = checkBinary('sumo')       # for Win
else :
    SUMO_BINARY = "/usr/bin/sumo"           # for Unix

SUMO_COMMAND = [SUMO_BINARY, "-c", "quadintersection/quad.sumocfg"]
# end_nodes = ["edge_center_north", "edge_center_east", "edge_center_south", "edge_center_west"]
# start_nodes = ["edge_north_center", "edge_east_center", "edge_south_center", "edge_west_center"]
end_nodes = ["edge_sw_leftexit", "edge_sw_bottomexit", "edge_se_bottomexit", "edge_se_rightexit", "edge_ne_rightexit", "edge_ne_topexit", "edge_nw_topexit", "edge_nw_leftexit"]
start_nodes = ["edge_sw_leftentry", "edge_sw_bottomentry", "edge_se_bottomentry", "edge_se_rightentry", "edge_ne_rightentry", "edge_ne_topentry", "edge_nw_topentry", "edge_nw_leftentry"]
detection_lanes = ["edge_ne_nw", "edge_nw_ne", "edge_sw_nw", "edge_nw_sw", "edge_se_ne", "edge_ne_se", "edge_se_sw", "edge_sw_se"]
numroutes = 0

def generate_routes():
    global numroutes

    for start in range(len(start_nodes)):
        for end in range(len(end_nodes)):
            if start == end:
                continue
            traci.route.add("trip_{}".format(numroutes), [start_nodes[start], end_nodes[end]])
            numroutes += 1

def numcars_on_edge(edge_name):
    return traci.edge.getLastStepVehicleNumber(edge_name)

def close_empty_lanes(controller):
    # lanes = traci.trafficlight.getControlledLanes("tls_center")
    links = traci.trafficlight.getControlledLinks("tls_center")
    # state = traci.trafficlight.getRedYellowGreenState("tls_center")

    tls = [None] * 32
    for idx in range(32):
        tls[idx] = [False, links[idx][0][0], links[idx][0][1], links[idx][0][2]]
    
    vehicles = traci.vehicle.getIDList()
    for vehicle in vehicles:
        lane = traci.vehicle.getLaneID(vehicle)

        for idx in range(32):
            if tls[idx][1] == lane:
                print("setting it to true")
                tls[idx][0] = True

    states = []
    for idx in range(32):
        states.append(tls[idx][0])
    print("states: {}".format(states))
    controller.update_states(states)
    traci.trafficlight.setRedYellowGreenState(controller.tls_id, controller.get_state_string())
    

# try:
traci.start(SUMO_COMMAND)
step = 0

generate_routes()
# controller = tlsc.TlsController("tls_center")
# print(traci.trafficlight.getPhase("tls_center"))

vehnum = 0
while step < 10000:
    # controller.update()
    if step % 5 == 0:
        traci.vehicle.add("newVeh_{}".format(vehnum), "trip_{}".format(randint(0, numroutes - 1)), "default_bicycle")
        traci.vehicle.add("newVeh_{}".format(vehnum + 1), "trip_{}".format(randint(0, numroutes - 1)), "default_car")
        vehnum += 2

    for lane in detection_lanes:
        print ("{} has {} vehicles".format(lane, numcars_on_edge(lane)))

    # if traci.simulation.getMinExpectedNumber() == 0:
    #     traci.vehicle.add("newVeh", "trip_{}".format(randint(0, numroutes - 1)))
    #     traci.vehicle.add("newVeh2", "trip_{}".format(randint(0, numroutes - 1)))
    
    # close_empty_lanes(controller)

    traci.simulationStep()
    step += 1

# except Exception as e:
#     print("Caught exception: {}".format(e))W

traci.close()