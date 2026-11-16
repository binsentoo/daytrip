import math
from haversine import haversine

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

