import argparse
from argparse import RawTextHelpFormatter
from all_routes import AllRoutes


def question_1(all_routes):
    print("Question 1 - Route Long Names")
    route_names = all_routes.get_route_names()
    route_names.sort()  # sort route names so output maintains order independent of API
    for route in route_names:
        print(route)


def question_2_1(all_routes):
    print("Question 2-1 - Route with most stops")
    route_with_most_stops = all_routes.get_route_with_max_stops()
    print("{} with {} stop(s).".format(route_with_most_stops.long_name, len(route_with_most_stops.stops)))


def question_2_2(all_routes):
    print("Question 2-2 - Route with least stops")
    route_with_least_stops = all_routes.get_route_with_min_stops()
    print("{} with {} stop(s).".format(route_with_least_stops.long_name, len(route_with_least_stops.stops)))


def question_2_3(all_routes):
    print("Question 2-3 - All stops with multiple routes")
    # reduce intersection stops information to just stop name and associated routes
    intersection_stops = all_routes.intersection_stops

    # get longest stop name length to prettify console output
    longest_stop_name_len = max([len(s["name"]) for s in intersection_stops])
    for stop_result in all_routes.intersection_stops:
        stop_result["routes"].sort()  # sort routes so output maintains order independent of API
        print("Stop: {}  Routes: {}".format(
            stop_result["name"].ljust(longest_stop_name_len, ' '),
            stop_result["routes"]
        ))


def question_2(all_routes):
    question_2_1(all_routes)
    question_2_2(all_routes)
    question_2_3(all_routes)


def question_3(all_routes, start_stop, end_stop):
    print("Question 3 - Suggest Routes")
    path = all_routes.suggest_routes(start_stop, end_stop)
    print("{} to {} --> {}".format(start_stop, end_stop, path))


def main(args):
    all_routes = AllRoutes.from_api()

    if args.question == 1:
        question_1(all_routes)
    elif args.question == 2:
        question_2(all_routes)
    elif args.question == 3:
        if args.start is None:
            print("--start is a required argument for question=3")
        elif args.end is None:
            print("--end is a required argument for question=3")
        else:
            question_3(all_routes, args.start, args.end)
    else:
        print("Unsupported question_id mode.  Run program with -h arg for more detail")


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description="""
MBTA command line utility for the following:
Input: question=1
Console Output:
List of route long names where route is
"light rail" type=0 or "heavy rail" type=1 (subway routes)

Input: question=2
Console Output: 
1. The name of the subway route with the most stops as well as a count of its stops.
2. The name of the subway route with the fewest stops as well as a count of its stops.
3. A list of the stops that connect two or more subway routes along with the relevant route
names for each of those stops.

Input: question=3 (example: start=Davis, end=Kendall/MIT)
Console Output:
A list of rail routes you could travel to get from one stop to the other.
The stop names must match be exact match to MBTA's API.

Example start and end options: Davis, Kendall/MIT, Ashmont, Arlington
    """)
    parser.add_argument('question', metavar='question', type=int,
                        help='question', choices=[1, 2, 3])
    parser.add_argument('--start', metavar='stop name', type=str,
                        help='Starting stop, used and required with question=3',
                        required=False)
    parser.add_argument('--end', metavar='end stop', type=str,
                        help='Ending stop, used and required with question=3',
                        required=False)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    main(args)
