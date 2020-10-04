from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import numpy as np
import optparse

from tlscontroller import TlsController


if __name__ == "__main__":
    if 'SUMO_HOME' in os.environ:
        sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), 'tools'))
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")

    import traci
    from sumolib import checkBinary  # noqa
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

        # first, generate the route file for this simulation
        #generate_routefile()

        # this is the normal way of using traci. sumo is started as a
        # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c","intersection.sumocfg"])



