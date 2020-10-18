import traci

end_nodes = ["edge_center_north", "edge_center_east", "edge_center_south", "edge_center_west"]
start_nodes = ["edge_north_center", "edge_east_center", "edge_south_center", "edge_west_center"]
routes_generated = False
routes = []

class Route:

    def __init__(self, start, end):
        global routes
        self.name = "route_{}".format(len(routes))
        self.start = start
        self.end = end
        traci.route.add(self.name, [self.start, self.end])


def init_routes():
    global end_nodes, start_nodes, routes_generated, routes

    for start in range(len(start_nodes)):
        for end in range(len(end_nodes)):
            if start == end:
                continue
            routes.append(Route(start_nodes[start], end_nodes[end]))
    
    routes_generated = True


class FlowController:
    
    # Flow is the amount of vehicles spawned per tick
    #   2 = 2/tick, 0.2 = 1 every 5 ticks
    # fill types:
    #   random (spawn on random route)
    #   balanced (spawn same amount per route)
    def __init__(self, vehicle_type, routes, flow = 0.2, fill_type = "random"):
        self.routes = routes
        self.vehicle_type = vehicle_type