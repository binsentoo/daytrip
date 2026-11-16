from django.test import SimpleTestCase
from . import planner

class DistanceMatrixTests(SimpleTestCase):
    def line_stops(self):
        return [
            {"id": "A", "name": "A", "lat": 0.0, "lng": 0.0, "duration_min": 30},
            {"id": "C", "name": "C", "lat": 0.0, "lng": 0.02, "duration_min": 30},
            {"id": "B", "name": "B", "lat": 0.0, "lng": 0.01, "duration_min": 30},
        ]

    def test_identical_stops(self):
        p = {"lat": 20.9, "lng": -121.3}
        self.assertEqual(planner.straight_line_matrix([p, p], 30), [[0, 0], [0, 0]])

    def test_different_stops(self): # 0.01 degrees lng apart, 1.11 km delta
        stops = self.line_stops()
        pair = [stops[0], stops[2]] # A and B
        matrix = planner.straight_line_matrix(pair, 60)
        self.assertEqual(matrix, [[0, 2], [2, 0]])


    def test_every_equal_index_is_zero(self):
        matrix = planner.straight_line_matrix(self.line_stops(), 60)
        self.assertTrue(all(matrix[i][i] == 0 for i in range(len(matrix))))

    def test_stops_return_valid_matrix(self):
        matrix = planner.straight_line_matrix(self.line_stops(), 60)
        self.assertTrue(all(len(matrix[row]) == 3 for row in range(len(matrix))))
        self.assertTrue(len(matrix) == 3)

    def test_empty_list_returns_empty_matrix(self):
        self.assertEqual(planner.straight_line_matrix([], 60), [])

    def test_full_matrix_for_three_stops(self):
        # At 60 km/h, kilometers equal minutes, then round up.
        # A-C is 0.02 degrees (about 2.22 km), so 3.
        # A-B and C-B are 0.01 degrees apart (about 1.11 km), so 2.
        matrix = planner.straight_line_matrix(self.line_stops(), 60)
        self.assertEqual(
            matrix,
            [
                [0, 3, 2],  # from A
                [3, 0, 2],  # from C
                [2, 2, 0],  # from B
            ],
        )

    def test_matrix_is_symmetric(self):
        matrix = planner.straight_line_matrix(self.line_stops(), 60)
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                self.assertEqual(matrix[i][j], matrix[j][i])


def make_stop(stop_id, priority="WANT", duration=60, opens=None, closes=None):
    return {
        "id": stop_id,
        "priority": priority,
        "name": f"Stop {stop_id}",
        "duration_min": duration,
        "opens_min": opens,
        "closes_min": closes,
    }

def flat_matrix(n, minutes):
    """Every trip between different stops takes the same number of minutes."""
    return [[0 if i == j else minutes for j in range(n)] for i in range(n)]

class WalkTests(SimpleTestCase):
    def test_waits_until_stop_opens(self):
        # Day starts at 9:00 (540). The stop opens at 10:00 (600) and takes 60 minutes.
        stops = [make_stop("A", duration=60, opens=600)]
        result = planner.walk([0], stops, flat_matrix(1, 10), 540, 1260)

        finish, legs = result
        self.assertEqual(finish, 660)
        self.assertEqual(legs[0]["arrive_time"], 540)
        self.assertEqual(legs[0]["start_time"], 600)
        self.assertEqual(legs[0]["depart_time"], 660)

    def test_stop_with_no_hours_works(self):
        stops = [make_stop("A", duration=60, opens=None, closes=None)]
        result = planner.walk([0], stops, flat_matrix(1, 10), 540, 1260)

        finish, legs = result
        self.assertEqual(finish, 600)
        self.assertEqual(legs[0]["arrive_time"], 540)
        self.assertEqual(legs[0]["start_time"], 540)
        self.assertEqual(legs[0]["depart_time"], 600)

    def test_no_wait_if_stop_is_open(self):
        stops = [make_stop("A", duration=60, opens=500)]
        result = planner.walk([0], stops, flat_matrix(1, 10), 540, 1260)

        finish, legs = result
        self.assertEqual(finish, 600)
        self.assertEqual(legs[0]["arrive_time"], 540)
        self.assertEqual(legs[0]["start_time"], 540)
        self.assertEqual(legs[0]["depart_time"], 600)

    def test_no_stop_if_closes_early(self):
        stops = [make_stop("A", duration=60, opens=500, closes=560)]
        result = planner.walk([0], stops, flat_matrix(1, 10), 540, 1260)

        self.assertIsNone(result)

    def test_visit_may_end_exactly_at_closing_time(self):
        stops = [make_stop("A", duration=60, opens=500, closes=600)]
        result = planner.walk([0], stops, flat_matrix(1, 10), 540, 1260)

        finish, legs = result
        self.assertEqual(finish, 600)
        self.assertEqual(legs[0]["arrive_time"], 540)
        self.assertEqual(legs[0]["start_time"], 540)
        self.assertEqual(legs[0]["depart_time"], 600)

    def test_runs_past_EOD(self):
        stops = [make_stop("A", duration=800)]
        result = planner.walk([0], stops, flat_matrix(1, 10), 540, 1260)

        self.assertIsNone(result)

    def test_travel_time_between_stops(self):
        stops = [make_stop("A", duration=30, opens=500, closes=1000), make_stop("B", duration=30, opens=500, closes=1000)]
        result = planner.walk([0, 1], stops, flat_matrix(2, 10), 540, 1260)

        finish, legs = result

        
        self.assertEqual(legs[0]["arrive_time"], 540)
        self.assertEqual(legs[0]["start_time"], 540)
        self.assertEqual(legs[0]["depart_time"], 570)

        self.assertEqual(finish, 610)
        self.assertEqual(legs[1]["arrive_time"], 580)
        self.assertEqual(legs[1]["start_time"], 580)
        self.assertEqual(legs[1]["depart_time"], 610)

    def test_order_changes_feasibility(self):
        stops = [make_stop("A", duration=30, opens=500, closes=600), make_stop("B", duration=30)]

        feasibleResult = planner.walk([0, 1], stops, flat_matrix(2, 10), 540, 1260)
        finish, legs = feasibleResult

        self.assertEqual(finish, 610)

        nonfeasibleResult = planner.walk([1, 0], stops, flat_matrix(2, 10), 540, 1260)
        self.assertIsNone(nonfeasibleResult)

    def test_wait_carries_into_next_stop(self):
        stops = [make_stop("A", duration=30, opens=600), make_stop("B", duration=30)]

        result = planner.walk([0, 1], stops, flat_matrix(2, 10), 540, 1260)

        finish, legs = result

        self.assertEqual(legs[0]["arrive_time"], 540)
        self.assertEqual(legs[0]["start_time"], 600)
        self.assertEqual(legs[0]["depart_time"], 630)

        self.assertEqual(legs[1]["arrive_time"], 640)
        self.assertEqual(legs[1]["start_time"], 640)
        self.assertEqual(legs[1]["depart_time"], 670)
        self.assertEqual(finish, 670)

    def test_travel_time_direction_matters(self):
        # Going from stop 0 to stop 1 takes 5 minutes, but 1 to 0 takes 20.
        stops = [make_stop("A", duration=30), make_stop("B", duration=30)]
        matrix = [[0, 5], [20, 0]]

        # A then B: A departs 570, B arrives 570 + 5 = 575, departs 605.
        finish, legs = planner.walk([0, 1], stops, matrix, 540, 1260)
        self.assertEqual(legs[1]["arrive_time"], 575)
        self.assertEqual(finish, 605)

        # B then A: B departs 570, A arrives 570 + 20 = 590, departs 620.
        finish, legs = planner.walk([1, 0], stops, matrix, 540, 1260)
        self.assertEqual(legs[1]["arrive_time"], 590)
        self.assertEqual(finish, 620)

    def test_empty_route(self):
        result = planner.walk([], [], [], 540, 1260)

        finish, legs = result
        self.assertEqual(finish, 540)
        self.assertEqual(legs, [])

    def test_visit_may_end_exactly_at_end_of_day(self):
        stops = [make_stop("A", duration=720)]
        result = planner.walk([0], stops, flat_matrix(1, 10), 540, 1260)

        finish, legs = result
        self.assertEqual(finish, 1260)

class BuildRouteTests(SimpleTestCase):
    def test_budget_keeps_must_and_higher_priority(self):
        # Only two stops fit in 540 to 680: 540-600, travel, 610-670.
        stops = [
            make_stop("A", priority="OPT"),
            make_stop("B", priority="MUST"),
            make_stop("C", priority="WANT"),
        ]
        matrix = flat_matrix(3, 10)
        order, unplaced = planner.build_route(stops, matrix, 540, 680)

        self.assertEqual(sorted(order), [1, 2])
        self.assertEqual(unplaced, [0])
        self.assertIsNotNone(planner.walk(order, stops, matrix, 540, 680))

    def test_add_all_stops(self):
        stops = [
            make_stop("A", priority="WANT"),
            make_stop("B", priority="WANT"),
            make_stop("C", priority="WANT"),
        ]
        matrix = flat_matrix(3, 10)
        order, unplaced = planner.build_route(stops, matrix, 540, 1260)

        self.assertEqual(sorted(order), [0, 1, 2])
        self.assertEqual(unplaced, [])
        self.assertIsNotNone(planner.walk(order, stops, matrix, 540, 1260))

    def test_dropped_must_is_reported(self):
        # 540 + 120 = 660, past the day's end at 620.
        stops = [make_stop("A", duration=120, priority="MUST")]
        matrix = flat_matrix(1, 10)
        order, unplaced = planner.build_route(stops, matrix, 540, 620)

        self.assertEqual(order, [])
        self.assertEqual(unplaced, [0])

    def test_must_that_closes_too_early_is_reported(self):
        # The visit would end at 600, but the stop closes at 560.
        stops = [make_stop("A", duration=60, closes=560, priority="MUST")]
        matrix = flat_matrix(1, 10)
        order, unplaced = planner.build_route(stops, matrix, 540, 1260)

        self.assertEqual(order, [])
        self.assertEqual(unplaced, [0])

    def test_always_prioritize_musts(self):
        # The MUST (100 min) plus one 30-minute WANT fit: 540-640, travel, 650-680.
        # Two WANTs first (540-570, 580-610) would leave the MUST ending at 720.
        stops = [
            make_stop("A", priority="MUST", duration=100),
            make_stop("B", priority="WANT", duration=30),
            make_stop("C", priority="WANT", duration=30),
        ]
        matrix = flat_matrix(3, 10)
        order, unplaced = planner.build_route(stops, matrix, 540, 680)

        self.assertIn(0, order)
        self.assertEqual(len(order), 2)
        self.assertEqual(len(unplaced), 1)
        self.assertIsNotNone(planner.walk(order, stops, matrix, 540, 680))

    def test_opening_hours_change_order(self):
        # [B, A]: B 540-600, A arrives 610 (open), ends 670.
        # [A, B]: A waits until 600, ends 660, B arrives 670, ends 730.
        stops = [
            make_stop("A", priority="WANT", duration=60, opens=600, closes=720),
            make_stop("B", priority="WANT", duration=60),
        ]
        matrix = flat_matrix(2, 10)
        order, unplaced = planner.build_route(stops, matrix, 540, 1260)

        self.assertEqual(order, [1, 0])
        self.assertEqual(unplaced, [])
        self.assertIsNotNone(planner.walk(order, stops, matrix, 540, 1260))

    def test_stop_that_can_never_fit_is_left_out(self):
        # Stop 1 opens at 1300, after the day ends at 1260, so it can never be visited.
        stops = [
            make_stop("A", priority="WANT"),
            make_stop("B", priority="WANT", opens=1300),
        ]
        matrix = flat_matrix(2, 10)
        order, unplaced = planner.build_route(stops, matrix, 540, 1260)

        self.assertEqual(order, [0])
        self.assertEqual(unplaced, [1])
        self.assertIsNotNone(planner.walk(order, stops, matrix, 540, 1260))

    def test_every_stop_is_placed_or_reported(self):
        # Nothing is lost or counted twice.
        # A (MUST) goes in first. D closes at 560 and cannot be reached in time.
        # Of B (WANT) and C (OPT), only one fits, and WANT wins on score.
        stops = [
            make_stop("A", priority="MUST"),
            make_stop("B", priority="WANT"),
            make_stop("C", priority="OPT"),
            make_stop("D", priority="WANT", closes=560),
        ]
        matrix = flat_matrix(4, 10)
        order, unplaced = planner.build_route(stops, matrix, 540, 680)

        self.assertEqual(sorted(order + unplaced), [0, 1, 2, 3])
        self.assertEqual(sorted(order), [0, 1])
        self.assertEqual(sorted(unplaced), [2, 3])
        self.assertIsNotNone(planner.walk(order, stops, matrix, 540, 680))

    def test_empty_input(self):
        order, unplaced = planner.build_route([], [], 540, 1260)

        self.assertEqual(order, [])
        self.assertEqual(unplaced, [])