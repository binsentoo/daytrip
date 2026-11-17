from django.test import SimpleTestCase
from apps.daytrips import planner

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

    def test_two_musts_both_fit(self):
        stops = [
            make_stop("A", duration=30, priority="MUST"),
            make_stop("B", duration=30, priority="MUST"),
        ]
        order, unplaced = planner.build_route(stops, flat_matrix(2, 10), 540, 1260)

        self.assertEqual(sorted(order), [0, 1])
        self.assertEqual(unplaced, [])

    def test_tighter_closing_must_wins_a_conflict(self):
        # Day is 540 to 640. Both stops take 60 minutes, so they cannot both fit
        # (the second would end at 670). Stop 1 closes at 600, so it has fewer options
        # and gets placed first: 540-600. Stop 0 then fits nowhere.
        stops = [
            make_stop("A", duration=60, priority="MUST"),
            make_stop("B", duration=60, closes=600, priority="MUST"),
        ]
        order, unplaced = planner.build_route(stops, flat_matrix(2, 10), 540, 640)

        self.assertEqual(order, [1])
        self.assertEqual(unplaced, [0])

    def test_empty_input(self):
        order, unplaced = planner.build_route([], [], 540, 1260)

        self.assertEqual(order, [])
        self.assertEqual(unplaced, [])

class BestInsertionTests(SimpleTestCase):
    def test_empty_route(self):
        stops = [make_stop("A", duration=60)]
        result = planner.best_insertion([], 0, stops, flat_matrix(1, 10), 540, 1260)

        self.assertEqual(result, (0, 600))

    def test_picks_the_earliest_finish(self):
        # Stop 1 opens at 600. Before stop 0: waits, ends 660, then stop 0 ends 730.
        # After stop 0: stop 0 ends 600, stop 1 arrives 610, ends 670.
        stops = [
            make_stop("A", duration=60),
            make_stop("B", duration=60, opens=600),
        ]
        route = [0]
        result = planner.best_insertion(route, 1, stops, flat_matrix(2, 10), 540, 1260)

        self.assertEqual(result, (1, 670))
        self.assertEqual(route, [0])  # the caller's list is untouched

    def test_skips_infeasible_positions(self):
        # Stop 1 closes at 600, so it only works first: 540-600, then stop 0 ends 670.
        stops = [
            make_stop("A", duration=60),
            make_stop("B", duration=60, closes=600),
        ]
        result = planner.best_insertion([0], 1, stops, flat_matrix(2, 10), 540, 1260)

        self.assertEqual(result, (0, 670))

    def test_returns_none_when_nothing_fits(self):
        # Stop 1 closes at 560, but a 60-minute visit starting at 540 ends at 600.
        stops = [
            make_stop("A", duration=60),
            make_stop("B", duration=60, closes=560),
        ]
        result = planner.best_insertion([0], 1, stops, flat_matrix(2, 10), 540, 1260)

        self.assertIsNone(result)

    def test_tie_goes_to_the_earlier_position(self):
        # Two identical stops finish at 670 in either order, so the front wins.
        stops = [make_stop("A", duration=60), make_stop("B", duration=60)]
        result = planner.best_insertion([0], 1, stops, flat_matrix(2, 10), 540, 1260)

        self.assertEqual(result, (0, 670))

class ImproveRouteTests(SimpleTestCase):
    def test_reversal_shortens_the_day(self):
        # Going from stop 1 to stop 2 takes 50 minutes, but 2 to 1 takes only 10.
        # [0, 1, 2]: 540-570, +10, 580-610, +50, 660-690. Finish 690.
        # [0, 2, 1]: 540-570, +10, 580-610, +10, 620-650. Finish 650.
        stops = [make_stop(name, duration=30) for name in "ABC"]
        matrix = [[0, 10, 10], [10, 0, 50], [10, 10, 0]]
        route = [0, 1, 2]

        result = planner.improve_route(route, stops, matrix, 540, 1260)

        finish, _ = planner.walk(result, stops, matrix, 540, 1260)
        self.assertEqual(finish, 650)
        self.assertEqual(sorted(result), [0, 1, 2])
        self.assertEqual(route, [0, 1, 2])  # the caller's list is untouched

    def test_best_route_is_left_alone(self):
        # [0, 2, 1] already finishes at 650, and no reversal does strictly better.
        stops = [make_stop(name, duration=30) for name in "ABC"]
        matrix = [[0, 10, 10], [10, 0, 50], [10, 10, 0]]

        result = planner.improve_route([0, 2, 1], stops, matrix, 540, 1260)

        self.assertEqual(result, [0, 2, 1])

    def test_infeasible_improvement_is_rejected(self):
        # [1, 0] would finish earlier (605 against 650), but stop A closes at 570,
        # and in [1, 0] it would not be reached until 575.
        stops = [
            make_stop("A", duration=30, closes=570),
            make_stop("B", duration=30),
        ]
        matrix = [[0, 50], [5, 0]]

        result = planner.improve_route([0, 1], stops, matrix, 540, 1260)

        self.assertEqual(result, [0, 1])

    def test_empty_and_single_stop_routes(self):
        self.assertEqual(planner.improve_route([], [], [], 540, 1260), [])

        stops = [make_stop("A")]
        self.assertEqual(
            planner.improve_route([0], stops, flat_matrix(1, 10), 540, 1260), [0]
        )

class PlanDayTests(SimpleTestCase):
    def test_empty(self):
        result = planner.plan_day([], [], 540, 1260)

        self.assertEqual(result, {"plan": [], "dropped": [], "total_travel_min": 0, "finish": 540})

    def test_entry_shows_travel_and_wait(self):
        # A: 540-570. Travel 10, B arrives 580 but opens at 600, so it waits 20 and ends 660.
        stops = [
            make_stop("A", duration=30),
            make_stop("B", duration=60, opens=600),
        ]
        result = planner.plan_day(stops, flat_matrix(2, 10), 540, 1260)

        first, second = result["plan"]
        self.assertEqual((first["travel_min"], first["wait_min"]), (0, 0))
        self.assertEqual(second["travel_min"], 10)
        self.assertEqual(second["arrive_time"], 580)
        self.assertEqual(second["wait_min"], 20)
        self.assertEqual(second["depart_time"], 660)
        self.assertEqual(result["total_travel_min"], 10)
        self.assertEqual(result["finish"], 660)

    def test_reason_when_stop_can_never_fit(self):
        # The visit would end at 600, but the stop closes at 560.
        stops = [make_stop("A", duration=60, closes=560)]
        result = planner.plan_day(stops, flat_matrix(1, 10), 540, 1260)

        self.assertEqual(result["plan"], [])
        self.assertEqual(result["dropped"][0]["id"], "A")
        self.assertIn("opening hours", result["dropped"][0]["reason"])

    def test_reason_when_no_room_left(self):
        # Same budget case as before: only B and C fit in 540 to 680.
        stops = [
            make_stop("A", priority="OPT"),
            make_stop("B", priority="MUST"),
            make_stop("C", priority="WANT"),
        ]
        result = planner.plan_day(stops, flat_matrix(3, 10), 540, 680)

        self.assertEqual([d["id"] for d in result["dropped"]], ["A"])
        self.assertIn("No room", result["dropped"][0]["reason"])

    def test_every_stop_is_planned_or_dropped(self):
        stops = [make_stop(name, priority="WANT") for name in "ABCD"]
        result = planner.plan_day(stops, flat_matrix(4, 10), 540, 700)

        ids = [e["id"] for e in result["plan"]] + [d["id"] for d in result["dropped"]]
        self.assertEqual(sorted(ids), ["A", "B", "C", "D"])

class TimeHelperTests(SimpleTestCase):
    def test_round_trip(self):
        from datetime import time
        self.assertEqual(planner.time_to_minutes(time(9, 30)), 570)
        self.assertIsNone(planner.time_to_minutes(None))
        self.assertEqual(planner.minutes_to_time(570), time(9, 30))