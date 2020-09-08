import requests
import json

# TODO: credentials/keys should never be checked into code base, but
# including here to keep this program simple
MBTA_ROUTES_URL = "https://api-v3.mbta.com/routes?api_key=354c104c610b457fafa1dcf89e8408c1&filter[type]=0,1"
ROUTE_STOPS_URL = "https://api-v3.mbta.com/stops?filter[route]={route_id}&api_key=354c104c610b457fafa1dcf89e8408c1"


class MtaApi:
    @classmethod
    def get_subway_routes(cls):
        # TODO: error handling for throttling and unexpected results
        request_response = requests.get(url=MBTA_ROUTES_URL)
        data = json.loads(request_response.text)
        return data

    @classmethod
    def get_stops_for_route(cls, route_id):
        # TODO: error handling for throttling and unexpected results
        request_response = requests.get(url=ROUTE_STOPS_URL.format(route_id=route_id))
        data = json.loads(request_response.text)
        return data