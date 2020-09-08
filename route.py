import json
from stop import Stop
from mta_api import MtaApi


class Route:
    """
    models MBTA's Route endpoint
    https://api-v3.mbta.com/docs/swagger/index.html#/Route/ApiWeb_RouteController_index
    """
    _cached_stops = None

    def __init__(self, id, attributes, links, relationships, type):
        self.id = id
        self.long_name = attributes["long_name"] if "long_name" in attributes else None

    @property
    def stops(self):
        if not self._cached_stops:
            self._cached_stops = self._get_stops()
        return self._cached_stops

    def _get_stops(self):
        data = MtaApi.get_stops_for_route(self.id)
        return list(map(Stop.from_json, data["data"]))

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)