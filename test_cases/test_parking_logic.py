"""
Unit tests for Smart Parking System detection logic.

Run from the project root:
    python -m unittest discover -s test_cases
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SIMULATION_DIR = PROJECT_ROOT / "simulation"
sys.path.insert(0, str(SIMULATION_DIR))

from smart_parking_simulation import (  # noqa: E402
    SmartParkingController,
    UltrasonicSensor,
)


class SmartParkingLogicTests(unittest.TestCase):
    def build_state(self, distances_cm: list[float]):
        controller = SmartParkingController()
        for sensor, distance in zip(controller.sensors, distances_cm):
            sensor.set_distance(distance)
        return controller.update()

    def test_all_slots_free(self) -> None:
        state = self.build_state([50.0, 50.0, 50.0, 50.0])
        self.assertEqual(state.free_count, 4)
        self.assertEqual(state.occupied_count, 0)
        self.assertFalse(state.parking_full)
        self.assertFalse(state.buzzer_on)
        self.assertTrue(state.gate_open)

    def test_single_slot_occupied(self) -> None:
        state = self.build_state([7.0, 50.0, 50.0, 50.0])
        self.assertEqual(state.free_count, 3)
        self.assertEqual(state.occupied_count, 1)
        self.assertEqual(state.statuses[0].label, "OCCUPIED")

    def test_parking_full_alert(self) -> None:
        state = self.build_state([7.0, 9.0, 10.0, 12.0])
        self.assertEqual(state.free_count, 0)
        self.assertEqual(state.occupied_count, 4)
        self.assertTrue(state.parking_full)
        self.assertTrue(state.buzzer_on)
        self.assertFalse(state.gate_open)

    def test_threshold_boundary_is_free(self) -> None:
        state = self.build_state([15.0, 50.0, 50.0, 50.0])
        self.assertEqual(state.statuses[0].label, "FREE")

    def test_invalid_echo_is_reported(self) -> None:
        controller = SmartParkingController()
        controller.sensors[0].invalid_enabled = True
        state = controller.update()
        self.assertEqual(state.invalid_count, 1)
        self.assertEqual(state.statuses[0].label, "ERROR")
        self.assertFalse(state.parking_full)

    def test_echo_time_formula(self) -> None:
        sensor = UltrasonicSensor(sensor_id=1, initial_distance_cm=10.0)
        reading = sensor.read_distance()
        self.assertTrue(reading.is_valid)
        self.assertAlmostEqual(reading.echo_time_us, 583.09, places=1)


if __name__ == "__main__":
    unittest.main()

