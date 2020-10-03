

class SUMOsim:
    def __init__(self):
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("please declare environment variable 'SUMO_HOME'")

        import traci
        from sumolib import checkBinary  # noqa
            optParser = optparse.OptionParser()
            optParser.add_option("--nogui", action="store_true",
                            default=False, help="run the commandline version of sumo")
            options, args = optParser.parse_args()
        if options.nogui:
            sumoBinary = checkBinary('sumo')
        else:
            sumoBinary = checkBinary('sumo-gui')

if __name__ == "__main__":
    conn = SUMOsim()
        
