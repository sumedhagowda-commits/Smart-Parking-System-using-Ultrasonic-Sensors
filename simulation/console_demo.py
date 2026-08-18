"""
Console demo for the Smart Parking System simulation.

Run from the project root:
    python simulation/console_demo.py

This is useful when tkinter GUI windows are unavailable or when you want
quick terminal proof that the parking logic works.
"""

from __future__ import annotations

from smart_parking_simulation import SmartParkingController


SCENARIOS = {
    "All slots free": [50.0, 50.0, 50.0, 50.0],
    "Slot 1 occupied": [7.0, 50.0, 50.0, 50.0],
    "Two slots occupied": [7.0, 9.0, 50.0, 50.0],
    "Parking full": [7.0, 9.0, 10.0, 12.0],
    "One vehicle leaves": [7.0, 9.0, 50.0, 12.0],
}


def run_scenario(name: str, distances_cm: list[float]) -> None:
    controller = SmartParkingController()

    for sensor, distance in zip(controller.sensors, distances_cm):
        sensor.set_distance(distance)

    state = controller.update()
    print(f"\n{name}")
    print("-" * len(name))

    for status in state.statuses:
        print(
            f"Slot {status.slot_id}: {status.label:<8} "
            f"distance={status.distance_cm:.1f} cm "
            f"echo={status.echo_time_us:.1f} us"
        )

    print(f"Available slots: {state.free_count}")
    print(f"Occupied slots : {state.occupied_count}")
    print(f"Buzzer         : {'ON' if state.buzzer_on else 'OFF'}")
    print(f"Gate           : {'OPEN' if state.gate_open else 'CLOSED'}")


def main() -> None:
    print("Smart Parking System using Ultrasonic Sensors - Console Simulation")
    print("Logic: distance < 15 cm means OCCUPIED, otherwise FREE")

    for name, distances_cm in SCENARIOS.items():
        run_scenario(name, distances_cm)


if __name__ == "__main__":
    main()

