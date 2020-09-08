import pytest
import json

from stop import Stop
from route import Route
from all_routes import AllRoutes

STOP_TEMPLATE = """
    {
      "id": "STOP_ID",
      "attributes": {
        "name": "STOP_NAME" 
      },
      "links": "dummy",
      "relationships": "dummy",
      "type": "dummy"
    }
    """

ROUTE_TEMPLATE = """
    {
      "id": "ROUTE_ID",
      "attributes": {
        "long_name": "ROUTE_LONG_NAME"
      },
      "links": "dummy",
      "relationships": "dummy",
      "type": "dummy"
    }
    """

@pytest.fixture
def stop_1():
    return Stop.from_json(json.loads(
        STOP_TEMPLATE.replace("STOP_ID", "stop_1").replace("STOP_NAME", "first stop")
    ))

@pytest.fixture
def stop_2():
    return Stop.from_json(json.loads(
        STOP_TEMPLATE.replace("STOP_ID", "stop_2").replace("STOP_NAME", "second stop")
    ))

@pytest.fixture
def stop_3():
    return Stop.from_json(json.loads(
        STOP_TEMPLATE.replace("STOP_ID", "stop_3").replace("STOP_NAME", "third stop")
    ))

@pytest.fixture
def stop_4():
    return Stop.from_json(json.loads(
        STOP_TEMPLATE.replace("STOP_ID", "stop_4").replace("STOP_NAME", "fourth stop")
    ))

@pytest.fixture
def stop_5():
    return Stop.from_json(json.loads(
        STOP_TEMPLATE.replace("STOP_ID", "stop_5").replace("STOP_NAME", "fifth stop")
    ))

@pytest.fixture
def stop_6():
    return Stop.from_json(json.loads(
        STOP_TEMPLATE.replace("STOP_ID", "stop_6").replace("STOP_NAME", "sixth stop")
    ))

@pytest.fixture
def stop_7():
    return Stop.from_json(json.loads(
        STOP_TEMPLATE.replace("STOP_ID", "stop_7").replace("STOP_NAME", "seventh stop")
    ))

@pytest.fixture
def route_a(stop_1, stop_2):
    r = Route.from_json(json.loads(
        ROUTE_TEMPLATE.replace("ROUTE_ID", "route_1").replace("ROUTE_LONG_NAME", "best route")
    ))
    r._cached_stops = [stop_1, stop_2]
    return r

@pytest.fixture
def route_b(stop_2, stop_3, stop_4):
    r = Route.from_json(json.loads(
        ROUTE_TEMPLATE.replace("ROUTE_ID", "route_2").replace("ROUTE_LONG_NAME", "worst route")
    ))
    r._cached_stops = [stop_2, stop_3, stop_4]
    return r


@pytest.fixture
def route_c(stop_4, stop_5, stop_6, stop_7):
    r = Route.from_json(json.loads(
        ROUTE_TEMPLATE.replace("ROUTE_ID", "route_3").replace("ROUTE_LONG_NAME", "risky route")
    ))
    r._cached_stops = [stop_4, stop_5, stop_6, stop_7]
    return r

@pytest.fixture
def all_routes(route_a, route_b, route_c):
    routes = [route_a, route_b, route_c]
    return AllRoutes(routes)


def test_get_route_names(all_routes):
    assert all_routes.get_route_names() == ["best route", "worst route", "risky route"]


def test_get_route_with_max_stops(all_routes, route_c):
    assert all_routes.get_route_with_max_stops().id == route_c.id


def test_get_route_with_max_stops(all_routes, route_c):
    assert all_routes.get_route_with_max_stops().id == route_c.id


def test_get_route_with_min_stops(all_routes, route_a):
    assert all_routes.get_route_with_min_stops().id == route_a.id


def test_get_route_intersections(all_routes):
    expected = [
        {'name': "second stop", 'routes': ['route_1', 'route_2'], 'routes_count': 2, 'stop_id': 'stop_2'},
        {'name': "fourth stop", 'routes': ['route_2', 'route_3'], 'routes_count': 2, 'stop_id': 'stop_4'}
    ]
    assert all_routes._get_route_intersections() == expected


def test_build_graph(all_routes):
    expected = {'route_1': {'route_2'}, 'route_2': {'route_3', 'route_1'}, 'route_3': {'route_2'}}
    assert all_routes._build_graph() == expected


def test_suggest_routes_multi_steps(all_routes):
    expected = ['route_1', 'route_2', 'route_3']
    assert all_routes.suggest_routes("first stop", "seventh stop") == expected


def test_suggest_routes_single_step(all_routes):
    expected = ['route_1']
    assert all_routes.suggest_routes("first stop", "second stop") == expected
