import math
from haversine import haversine

MUST = "MUST"
WANT = "WANT"
OPT = "OPT"

PRIORITY_WEIGHT = {
    WANT: 3,
    OPT: 1,
}

# returns (lat, lng) tuple for haversine package
def stop_point(stop):
    return (stop["lat"], stop["lng"])

# travel minutes between every pair of stops
def straight_line_matrix(stops, speed_kmh):
    n = len(stops)
    matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                km = haversine(stop_point(stops[i]), stop_point(stops[j]))
                matrix[i][j] = math.ceil(km / speed_kmh * 60)
    return matrix

# given day logistics and list of stops, return if given order allows for feasibility
def walk(order, stops, matrix, day_start, day_end):
    clock = day_start
    legs = []
    prev_stop_index = None

    for index in order:
        stop = stops[index]

        travel_time = 0
        if prev_stop_index is not None:
            travel_time = matrix[prev_stop_index][index]

        arrival = clock + travel_time
        start = arrival
        if stop['opens_min'] is not None:
            start = max(start, stop['opens_min'])

        depart = start + stop['duration_min']

        if stop['closes_min'] is not None and depart > stop['closes_min']:
            return None

        if depart > day_end:
            return None

        legs.append({
            'arrive_time': arrival,
            'start_time': start,
            'depart_time': depart
        })

        clock = depart
        prev_stop_index = index

    return (clock, legs)

# given route (list of index), try candidate_index at every position, 
# return (position, finish) if possible, else None
def best_insertion(route, candidate_index, stops, matrix, day_start, day_end):
    best = None
    for position in range(len(route) + 1):
        new_route = route[:position] + [candidate_index] + route[position:]
        result = walk(new_route, stops, matrix, day_start, day_end)

        if result is None: # skip if infeasible
            continue

        finish, _ = result

        if best is None or finish < best[1]:
            best = (position, finish)

    return best
"""
The range. Inserting into a route of length 3 has more than 3 possible positions. Count them, including both ends, and write the upper bound of range to match. The empty route must give exactly one position.
Never edit route. Slicing builds a new list each time (route[:position] and route[position:]), so the caller’s list stays untouched.
The tie rule. A strict “less than” when you compare against the best so far keeps the first of several equal positions. Think about what <= would do instead.
What walk gives you. It returns None or (finish, legs), so you need to unpack it before comparing finish times.

Step 2: a helper, best_insertion

Write this one first and test it by hand. 
Given the current route (a list of indexes) and one candidate index, 
it tries the candidate at every position, from the front to the back. 
For each position it builds that ordering and calls walk. 
It returns the feasible position with the earliest finish, 
along with that finish time, or None if no position works.

Three details:

Build a new list for each attempt (route[:pos] + [candidate] + route[pos:]),
    and never edit the route you were given.
Break ties deterministically. 
If two positions finish at the same time, 
keep the earlier one by using a strict “less than” when you compare.
The empty route has to work. Trying position 0 on [] should give you the one-stop route.

Step 3: the must-dos

Collect the MUST indexes and sort them by closing time, with None (no closing time) last.
For each one, call best_insertion. If you get a position, insert it. If you get None, add it to unplaced.

Think about why closing time is the sort key. It only changes the outcome when two musts compete for the same space.

Step 4: the rest, one at a time

Repeat this loop until a pass adds nothing:

For every remaining non-must stop, call best_insertion. Skip it if the answer is None.
The score is its weight divided by the extra minutes, where extra means (finish with it) minus (the current route’s finish). The finish of an empty route is day_start, and walk([]) already gives you that.
Guard against a zero or negative extra before dividing. A stop can add no time at all (a free gap before a late-opening stop), and dividing by zero would crash.
Insert the highest-scoring stop, and keep the first one on a tie, so results are the same every run.
When no remaining stop has a feasible insertion, stop.

Whatever is left, plus any musts that failed, is unplaced.

Step 5: return (order, unplaced)

Both are lists of indexes into the original stops. The invariant to keep in mind: every index appears in exactly one of the two lists, which is what test_every_stop_is_placed_or_reported checks."""