# MBTA Route Tool

MBTA route tool is a command-line utility for various route lookups.
 
# Setup
 
Requirements:
```
* python3 (3.6.8+)
* pip3
* python3-venv (optional)
```
 
 
1.  Clone repository to local environment (alternatively, download zip and extract).

1.  Optionally, use venv to create clean python3 environment.
 
     ```
     python3 -m venv ./.venv
     source ./.venv/bin/activate
     ```
 
1. Install requirements
    ```
    pip3 install -r requirements.txt
    ```
 
# How to use
 
1. List of route long names for light rail" type=0 or "heavy rail" type=1 routes (subway routes)
    ```
    python3 mbta.py 1
    ```

2. Stop utility
    - The name of the subway route with the most stops as well as a count of its stops.
    - The name of the subway route with the fewest stops as well as a count of its stops.
    - A list of the stops that connect two or more subway routes along with the relevant route
names for each of those stops.
    ```
    python3 mbta.py 2
    ```

3. A list of rail routes you could travel to get from one stop to the other.
The stop names must match be exact match to MBTA's API.

    - Example start and end options: Davis, Kendall/MIT, Ashmont, Arlington 
    ```
    python3 mbta.py 3 --start Ashmont --end Arlington
    ```
 
# Development

Run `python3 -m pytest.py` to test.
 
    
 