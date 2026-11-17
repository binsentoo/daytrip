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

def build_route(stops, matrix, day_start, day_end):
    order = []
    remaining = []
    unplaced = []

    must_stops = [] # store indices

    for index in range(len(stops)):
        if stops[index]["priority"] == MUST:
            must_stops.append(index)
        else:
            remaining.append(index)

    must_stops.sort(key=lambda i: (stops[i]["closes_min"] is None, stops[i]["closes_min"] or 0))

    # place MUST stops
    for index in must_stops:
        result = best_insertion(order, index, stops, matrix, day_start, day_end)

        if result is None:
            unplaced.append(index)
        else:
            order.insert(result[0], index)

    # attempt to place other stops (using scoring based on extra minutes added. priority_weight/extra minutes)
    while True:
        best = None
        current_finish, _ = walk(order, stops, matrix, day_start, day_end)
        for index in remaining:
            result = best_insertion(order, index, stops, matrix, day_start, day_end)

            if result is None:
                continue

            position, new_finish = result
            extra = max(new_finish - current_finish, 1)
            score = PRIORITY_WEIGHT[stops[index]["priority"]] / extra

            if best is None or score > best[0]:
                best = (score, index, position, new_finish)

        if best is None:
            break

        _, index, position, _ = best
        remaining.remove(index)
        order.insert(position, index)

    unplaced.extend(remaining)
    return (order, unplaced)