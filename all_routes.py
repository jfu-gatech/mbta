from route import Route
from mta_api import MtaApi
import util

class AllRoutes:
    """
    models a list of MBTA Routes
    https://api-v3.mbta.com/docs/swagger/index.html#/Route/ApiWeb_RouteController_index
    """
    _cached_intersection_stops = None

    def __init__(self, routes):
        self.routes = routes

    @property
    def intersection_stops(self):
        if not self._cached_intersection_stops:
            self._cached_intersection_stops = self._get_route_intersections()
        return self._cached_intersection_stops

    def get_route_names(self):
        return [r.long_name for r in self.routes]

    def get_route_with_max_stops(self):
        return max(self.routes, key=lambda r: len(r.stops))

    def get_route_with_min_stops(self):
        return min(self.routes, key=lambda r: len(r.stops))

    def _get_route_intersections(self):
        srm = {}  # srm = stop routes mapping
        intersection_stops = []  # only contains stops with multiple routes
        for route in self.routes:
            for stop in route.stops:
                if stop.id not in srm:  # initialize srm dictionary
                    srm[stop.id] = {}
                    srm[stop.id]["name"] = stop.name
                    srm[stop.id]["stop_id"] = stop.id
                    srm[stop.id]["routes"] = []
                    srm[stop.id]["routes_count"] = 0
                srm[stop.id]["routes"].append(route.id)
                srm[stop.id]["routes_count"] += 1
                if srm[stop.id]["routes_count"] == 2:  # only append first time routes exceeds threshold
                    intersection_stops.append(srm[stop.id])
        return intersection_stops

    def _build_graph(self):
        # convert `stops and their routes` to `routes and their connecting routes`
        # so the data is represented as a graph for graph search algorithms
        graph = {}  # dictionary of sets (key: route, value: array of connecting routes)

        for node in self.intersection_stops:
            routes = node["routes"]
            for i in range(0, len(routes)):
                for j in range(0, len(routes)):
                    if i != j:
                        if routes[i] not in graph:
                            graph[routes[i]] = set()
                        graph[routes[i]].add(routes[j])

        return graph

    def suggest_routes(self, start_stop_name, end_stop_name):
        # Use graph search algorithm to find how to traverse from route A to B
        #
        # Approach:
        #   Treat routes as nodes in a graph with special case where a person can be on
        # multiple nodes at the same time.
        #
        # Note:
        # Returns shortest route.  Since the requirement is to suggest any path,
        # there is no prioritization in case with multiple shortest routes.
        # TODO: add parameter documentation

        # based on start and end stop_id, collect all potential start and stop route_ids
        starts = []
        ends = []
        for r in self.routes:
            if any([s for s in r.stops if start_stop_name == s.name]):
                starts.append(r.id)
            if any([s for s in r.stops if end_stop_name == s.name]):
                ends.append(r.id)

        if len(starts) == 0:
            print("Unable to find starting stop name")
            return

        if len(ends) == 0:
            print("Unable to find ending stop name")
            return


        # get graph data based on nodes = route
        graph = self._build_graph()

        # for each start and end combination, print out potential paths
        for s in starts:
            for e in ends:
                path = util.breadth_first_search(graph, s, e)
                if path:
                    return path

    @classmethod
    def from_json(cls, data):
        if "data" not in data:
            print(data)
        routes = list(map(Route.from_json, data["data"]))
        return cls(routes)

    @classmethod
    def from_api(cls):
        data = MtaApi.get_subway_routes()
        return cls.from_json(data)
