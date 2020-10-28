# RUN THIS TO RUN EXPERIMENTS

import os
import traci
from sumolib import checkBinary
from random import randint
from tlscontroller import TlsController
from geneticAlgorithm import genetic

# This makes sure that it works on both Windows and Unix
if 'SUMO_HOME' in os.environ :
    SUMO_BINARY = checkBinary('sumo')           # for Win
else :
    SUMO_BINARY = "/usr/bin/sumo"               # for Unix

SUMO_COMMAND = [SUMO_BINARY, "-c", "quadintersection/quad.sumocfg"]

traci.start(SUMO_COMMAND)
initialState = TlsController("junc_nw", True).states
traci.close()

experiment = genetic(initialState)
experiment.run()