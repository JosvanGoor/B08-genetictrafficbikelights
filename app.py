import traci

SUMO_BINARY = "/usr/bin/sumo-gui"
SUMO_COMMAND = [SUMO_BINARY, "-c", "SUMO/intersection.sumocfg"]

try:
    traci.start(SUMO_COMMAND)
    step = 0

    traci.route.add("trip", ["edge_west_center", "edge_center_north"])

    while step < 100000:
        if traci.simulation.getMinExpectedNumber() == 0:
            traci.vehicle.add("newVeh", "trip")

        traci.simulationStep()
        step += 1

except Exception as e:
    print("Caught exception: {}".format(e))

traci.close()