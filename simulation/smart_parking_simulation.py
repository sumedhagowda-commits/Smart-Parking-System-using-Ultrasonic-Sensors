"""
Smart Parking System using Ultrasonic Sensors - Python Simulation

Run in VS Code:
    python simulation/smart_parking_simulation.py

This simulation models the embedded project behavior:
    - 4 ultrasonic sensors
    - distance threshold based slot detection
    - green/red LED indication
    - LCD display output
    - buzzer when parking is full
    - optional entry gate behavior
    - serial monitor style logging

No external Python packages are required. The GUI uses tkinter from the
Python standard library.
"""

from __future__ import annotations

import random
import time
import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import List


SPEED_OF_SOUND_CM_PER_US = 0.0343
DEFAULT_THRESHOLD_CM = 15.0
MAX_VALID_DISTANCE_CM = 400.0
MIN_VALID_DISTANCE_CM = 2.0
TOTAL_SLOTS = 4


@dataclass
class UltrasonicReading:
    distance_cm: float | None
    echo_time_us: float | None
    is_valid: bool
    message: str


class UltrasonicSensor:
    """Simulates an HC-SR04 ultrasonic sensor mounted above one slot."""

    def __init__(self, sensor_id: int, initial_distance_cm: float = 50.0) -> None:
        self.sensor_id = sensor_id
        self.distance_cm = initial_distance_cm
        self.noise_enabled = False
        self.invalid_enabled = False

    def set_distance(self, distance_cm: float) -> None:
        self.distance_cm = distance_cm

    def read_distance(self) -> UltrasonicReading:
        if self.invalid_enabled:
            return UltrasonicReading(
                distance_cm=None,
                echo_time_us=None,
                is_valid=False,
                message="Invalid echo: no pulse received",
            )

        measured_distance = self.distance_cm
        if self.noise_enabled:
            measured_distance += random.uniform(-2.0, 2.0)

        if measured_distance < MIN_VALID_DISTANCE_CM:
            return UltrasonicReading(
                distance_cm=None,
                echo_time_us=None,
                is_valid=False,
                message="Invalid echo: distance below sensor range",
            )

        if measured_distance > MAX_VALID_DISTANCE_CM:
            return UltrasonicReading(
                distance_cm=None,
                echo_time_us=None,
                is_valid=False,
                message="Invalid echo: distance above sensor range",
            )

        echo_time_us = (2 * measured_distance) / SPEED_OF_SOUND_CM_PER_US
        return UltrasonicReading(
            distance_cm=round(measured_distance, 2),
            echo_time_us=round(echo_time_us, 2),
            is_valid=True,
            message="OK",
        )


@dataclass
class ParkingSlotStatus:
    slot_id: int
    distance_cm: float | None
    echo_time_us: float | None
    is_occupied: bool
    is_valid: bool
    message: str

    @property
    def label(self) -> str:
        if not self.is_valid:
            return "ERROR"
        return "OCCUPIED" if self.is_occupied else "FREE"


class ParkingSlot:
    """Combines one ultrasonic sensor with threshold detection logic."""

    def __init__(self, slot_id: int, sensor: UltrasonicSensor) -> None:
        self.slot_id = slot_id
        self.sensor = sensor

    def get_status(self, threshold_cm: float) -> ParkingSlotStatus:
        reading = self.sensor.read_distance()

        if not reading.is_valid:
            return ParkingSlotStatus(
                slot_id=self.slot_id,
                distance_cm=None,
                echo_time_us=None,
                is_occupied=False,
                is_valid=False,
                message=reading.message,
            )

        is_occupied = bool(reading.distance_cm < threshold_cm)
        return ParkingSlotStatus(
            slot_id=self.slot_id,
            distance_cm=reading.distance_cm,
            echo_time_us=reading.echo_time_us,
            is_occupied=is_occupied,
            is_valid=True,
            message=reading.message,
        )


@dataclass
class ParkingSystemState:
    statuses: List[ParkingSlotStatus]
    free_count: int
    occupied_count: int
    invalid_count: int
    parking_full: bool
    buzzer_on: bool
    gate_open: bool


class SmartParkingController:
    """Main controller that represents microcontroller processing logic."""

    def __init__(self, total_slots: int = TOTAL_SLOTS) -> None:
        self.sensors = [
            UltrasonicSensor(sensor_id=i + 1, initial_distance_cm=50.0)
            for i in range(total_slots)
        ]
        self.slots = [
            ParkingSlot(slot_id=i + 1, sensor=self.sensors[i])
            for i in range(total_slots)
        ]
        self.threshold_cm = DEFAULT_THRESHOLD_CM
        self.gate_enabled = True

    def update(self) -> ParkingSystemState:
        statuses = [slot.get_status(self.threshold_cm) for slot in self.slots]
        valid_statuses = [status for status in statuses if status.is_valid]

        occupied_count = sum(1 for status in valid_statuses if status.is_occupied)
        free_count = sum(1 for status in valid_statuses if not status.is_occupied)
        invalid_count = len(statuses) - len(valid_statuses)

        parking_full = free_count == 0 and invalid_count == 0
        buzzer_on = parking_full
        gate_open = self.gate_enabled and free_count > 0

        return ParkingSystemState(
            statuses=statuses,
            free_count=free_count,
            occupied_count=occupied_count,
            invalid_count=invalid_count,
            parking_full=parking_full,
            buzzer_on=buzzer_on,
            gate_open=gate_open,
        )


class SmartParkingApp(tk.Tk):
    """Tkinter user interface for the complete parking system simulation."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Smart Parking System - Ultrasonic Sensor Simulation")
        self.geometry("1120x720")
        self.minsize(980, 640)

        self.controller = SmartParkingController()
        self.auto_mode = tk.BooleanVar(value=False)
        self.status_var = tk.StringVar(value="System ready")
        self.threshold_var = tk.DoubleVar(value=DEFAULT_THRESHOLD_CM)
        self.gate_enabled_var = tk.BooleanVar(value=True)
        self.distance_vars = [
            tk.DoubleVar(value=sensor.distance_cm) for sensor in self.controller.sensors
        ]
        self.noise_vars = [tk.BooleanVar(value=False) for _ in self.controller.sensors]
        self.invalid_vars = [tk.BooleanVar(value=False) for _ in self.controller.sensors]

        self.slot_cards: list[dict[str, object]] = []
        self.lcd_text: tk.Text
        self.serial_text: tk.Text
        self.buzzer_canvas: tk.Canvas
        self.gate_canvas: tk.Canvas
        self.summary_labels: dict[str, ttk.Label] = {}

        self._configure_style()
        self._build_layout()
        self.refresh_system()
        self.after(1000, self._auto_tick)

    def _configure_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f4f7fb")
        style.configure("Header.TFrame", background="#18324a")
        style.configure(
            "Header.TLabel",
            background="#18324a",
            foreground="#ffffff",
            font=("Segoe UI", 18, "bold"),
        )
        style.configure(
            "SubHeader.TLabel",
            background="#18324a",
            foreground="#d8e6f2",
            font=("Segoe UI", 10),
        )
        style.configure("Card.TFrame", background="#ffffff", relief="solid", borderwidth=1)
        style.configure("CardTitle.TLabel", background="#ffffff", font=("Segoe UI", 12, "bold"))
        style.configure("CardText.TLabel", background="#ffffff", font=("Segoe UI", 10))
        style.configure("Good.TLabel", background="#ffffff", foreground="#1b7f38", font=("Segoe UI", 11, "bold"))
        style.configure("Bad.TLabel", background="#ffffff", foreground="#b42318", font=("Segoe UI", 11, "bold"))
        style.configure("Warn.TLabel", background="#ffffff", foreground="#a15c00", font=("Segoe UI", 11, "bold"))
        style.configure("Summary.TLabel", background="#eef3f8", font=("Segoe UI", 12, "bold"))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("TCheckbutton", background="#ffffff", font=("Segoe UI", 9))
        style.configure("TScale", background="#ffffff")

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)

        header = ttk.Frame(self, style="Header.TFrame", padding=(18, 12))
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.columnconfigure(0, weight=1)
        ttk.Label(
            header,
            text="Smart Parking System using Ultrasonic Sensors",
            style="Header.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Python simulation for Arduino/ESP32 project logic",
            style="SubHeader.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(3, 0))

        left = ttk.Frame(self, padding=14)
        left.grid(row=1, column=0, sticky="nsew")
        left.columnconfigure(0, weight=1)
        left.rowconfigure(1, weight=1)

        controls = ttk.Frame(left, style="Card.TFrame", padding=12)
        controls.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        controls.columnconfigure(6, weight=1)

        ttk.Label(controls, text="Threshold (cm)", style="CardText.TLabel").grid(row=0, column=0, sticky="w")
        threshold_spin = ttk.Spinbox(
            controls,
            from_=5,
            to=80,
            increment=1,
            textvariable=self.threshold_var,
            width=8,
            command=self.refresh_system,
        )
        threshold_spin.grid(row=0, column=1, sticky="w", padx=(8, 20))
        threshold_spin.bind("<KeyRelease>", lambda _event: self.refresh_system())

        ttk.Checkbutton(
            controls,
            text="Auto traffic",
            variable=self.auto_mode,
        ).grid(row=0, column=2, sticky="w", padx=(0, 16))

        ttk.Checkbutton(
            controls,
            text="Gate enabled",
            variable=self.gate_enabled_var,
            command=self.refresh_system,
        ).grid(row=0, column=3, sticky="w", padx=(0, 16))

        ttk.Button(controls, text="All Free", command=self.set_all_free).grid(row=0, column=4, padx=4)
        ttk.Button(controls, text="All Occupied", command=self.set_all_occupied).grid(row=0, column=5, padx=4)
        ttk.Button(controls, text="Random Test", command=self.random_test).grid(row=0, column=6, sticky="w", padx=4)

        slots_frame = ttk.Frame(left)
        slots_frame.grid(row=1, column=0, sticky="nsew")
        slots_frame.columnconfigure(0, weight=1)
        slots_frame.columnconfigure(1, weight=1)
        slots_frame.rowconfigure(0, weight=1)
        slots_frame.rowconfigure(1, weight=1)

        for index in range(TOTAL_SLOTS):
            card = self._create_slot_card(slots_frame, index)
            row = index // 2
            column = index % 2
            card["frame"].grid(row=row, column=column, padx=8, pady=8, sticky="nsew")
            self.slot_cards.append(card)

        right = ttk.Frame(self, padding=(0, 14, 14, 14))
        right.grid(row=1, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(3, weight=1)

        summary = ttk.Frame(right, padding=12)
        summary.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        summary.configure(style="Card.TFrame")
        summary.columnconfigure((0, 1, 2), weight=1)
        self.summary_labels["free"] = ttk.Label(summary, text="Free: 4", style="Summary.TLabel")
        self.summary_labels["occupied"] = ttk.Label(summary, text="Occupied: 0", style="Summary.TLabel")
        self.summary_labels["invalid"] = ttk.Label(summary, text="Invalid: 0", style="Summary.TLabel")
        self.summary_labels["free"].grid(row=0, column=0, sticky="ew", padx=4)
        self.summary_labels["occupied"].grid(row=0, column=1, sticky="ew", padx=4)
        self.summary_labels["invalid"].grid(row=0, column=2, sticky="ew", padx=4)

        indicators = ttk.Frame(right, style="Card.TFrame", padding=12)
        indicators.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        indicators.columnconfigure((0, 1), weight=1)
        ttk.Label(indicators, text="Buzzer", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(indicators, text="Gate", style="CardTitle.TLabel").grid(row=0, column=1, sticky="w")

        self.buzzer_canvas = tk.Canvas(indicators, width=150, height=72, bg="#ffffff", highlightthickness=0)
        self.buzzer_canvas.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(8, 0))
        self.gate_canvas = tk.Canvas(indicators, width=150, height=72, bg="#ffffff", highlightthickness=0)
        self.gate_canvas.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(8, 0))

        lcd_frame = ttk.Frame(right, style="Card.TFrame", padding=12)
        lcd_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        lcd_frame.columnconfigure(0, weight=1)
        ttk.Label(lcd_frame, text="LCD / OLED Display", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        self.lcd_text = tk.Text(
            lcd_frame,
            height=7,
            bg="#101820",
            fg="#7CFF7C",
            insertbackground="#7CFF7C",
            relief="flat",
            font=("Consolas", 13, "bold"),
            padx=10,
            pady=10,
        )
        self.lcd_text.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        self.lcd_text.configure(state="disabled")

        serial_frame = ttk.Frame(right, style="Card.TFrame", padding=12)
        serial_frame.grid(row=3, column=0, sticky="nsew")
        serial_frame.columnconfigure(0, weight=1)
        serial_frame.rowconfigure(1, weight=1)
        ttk.Label(serial_frame, text="Serial Monitor", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        self.serial_text = tk.Text(
            serial_frame,
            bg="#0f1720",
            fg="#d6e4f0",
            insertbackground="#d6e4f0",
            relief="flat",
            font=("Consolas", 10),
            padx=8,
            pady=8,
        )
        self.serial_text.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        self.serial_text.configure(state="disabled")

        footer = ttk.Frame(self, padding=(14, 8))
        footer.grid(row=2, column=0, columnspan=2, sticky="ew")
        footer.columnconfigure(0, weight=1)
        ttk.Label(footer, textvariable=self.status_var).grid(row=0, column=0, sticky="w")

    def _create_slot_card(self, parent: ttk.Frame, index: int) -> dict[str, object]:
        slot_number = index + 1
        frame = ttk.Frame(parent, style="Card.TFrame", padding=14)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(6, weight=1)

        title = ttk.Label(frame, text=f"Parking Slot {slot_number}", style="CardTitle.TLabel")
        title.grid(row=0, column=0, columnspan=3, sticky="w")

        led_canvas = tk.Canvas(frame, width=94, height=94, bg="#ffffff", highlightthickness=0)
        led_canvas.grid(row=1, column=0, rowspan=4, sticky="nw", pady=(12, 0), padx=(0, 14))

        status_label = ttk.Label(frame, text="FREE", style="Good.TLabel")
        status_label.grid(row=1, column=1, columnspan=2, sticky="w", pady=(12, 0))

        distance_label = ttk.Label(frame, text="Distance: 50.0 cm", style="CardText.TLabel")
        distance_label.grid(row=2, column=1, columnspan=2, sticky="w", pady=(8, 0))

        echo_label = ttk.Label(frame, text="Echo: 2915.45 us", style="CardText.TLabel")
        echo_label.grid(row=3, column=1, columnspan=2, sticky="w", pady=(4, 0))

        threshold_label = ttk.Label(frame, text="Logic: distance < threshold => occupied", style="CardText.TLabel")
        threshold_label.grid(row=4, column=1, columnspan=2, sticky="w", pady=(4, 0))

        slider = ttk.Scale(
            frame,
            from_=2,
            to=100,
            variable=self.distance_vars[index],
            command=lambda _value, i=index: self.on_distance_change(i),
        )
        slider.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(14, 0))

        slider_labels = ttk.Frame(frame, style="Card.TFrame")
        slider_labels.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(2, 0))
        slider_labels.columnconfigure((0, 1, 2), weight=1)
        ttk.Label(slider_labels, text="Near", style="CardText.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(slider_labels, text="Vehicle distance", style="CardText.TLabel").grid(row=0, column=1)
        ttk.Label(slider_labels, text="Far", style="CardText.TLabel").grid(row=0, column=2, sticky="e")

        options = ttk.Frame(frame, style="Card.TFrame")
        options.grid(row=7, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        ttk.Checkbutton(
            options,
            text="Noise",
            variable=self.noise_vars[index],
            command=self.refresh_system,
        ).grid(row=0, column=0, sticky="w", padx=(0, 14))
        ttk.Checkbutton(
            options,
            text="Invalid echo",
            variable=self.invalid_vars[index],
            command=self.refresh_system,
        ).grid(row=0, column=1, sticky="w")

        return {
            "frame": frame,
            "led_canvas": led_canvas,
            "status_label": status_label,
            "distance_label": distance_label,
            "echo_label": echo_label,
        }

    def on_distance_change(self, index: int) -> None:
        self.controller.sensors[index].set_distance(self.distance_vars[index].get())
        self.refresh_system()

    def set_all_free(self) -> None:
        for index, sensor in enumerate(self.controller.sensors):
            self.distance_vars[index].set(50.0)
            self.noise_vars[index].set(False)
            self.invalid_vars[index].set(False)
            sensor.set_distance(50.0)
        self.status_var.set("Test case: all slots free")
        self.refresh_system()

    def set_all_occupied(self) -> None:
        for index, sensor in enumerate(self.controller.sensors):
            self.distance_vars[index].set(7.0)
            self.noise_vars[index].set(False)
            self.invalid_vars[index].set(False)
            sensor.set_distance(7.0)
        self.status_var.set("Test case: all slots occupied")
        self.refresh_system()

    def random_test(self) -> None:
        for index, sensor in enumerate(self.controller.sensors):
            distance = random.choice([6.0, 9.0, 12.0, 25.0, 40.0, 60.0])
            self.distance_vars[index].set(distance)
            sensor.set_distance(distance)
            self.invalid_vars[index].set(False)
        self.status_var.set("Random test case generated")
        self.refresh_system()

    def refresh_system(self) -> None:
        threshold = self._safe_threshold()
        self.controller.threshold_cm = threshold
        self.controller.gate_enabled = self.gate_enabled_var.get()

        for index, sensor in enumerate(self.controller.sensors):
            sensor.set_distance(self.distance_vars[index].get())
            sensor.noise_enabled = self.noise_vars[index].get()
            sensor.invalid_enabled = self.invalid_vars[index].get()

        state = self.controller.update()
        self._update_slot_cards(state)
        self._update_summary(state)
        self._update_lcd(state)
        self._update_indicators(state)
        self._append_serial_output(state)

    def _safe_threshold(self) -> float:
        try:
            threshold = float(self.threshold_var.get())
        except tk.TclError:
            threshold = DEFAULT_THRESHOLD_CM
        return max(1.0, min(100.0, threshold))

    def _update_slot_cards(self, state: ParkingSystemState) -> None:
        for index, status in enumerate(state.statuses):
            card = self.slot_cards[index]
            led_canvas: tk.Canvas = card["led_canvas"]  # type: ignore[assignment]
            status_label: ttk.Label = card["status_label"]  # type: ignore[assignment]
            distance_label: ttk.Label = card["distance_label"]  # type: ignore[assignment]
            echo_label: ttk.Label = card["echo_label"]  # type: ignore[assignment]

            led_canvas.delete("all")
            if not status.is_valid:
                fill_color = "#f5b942"
                led_text = "ERR"
                label_style = "Warn.TLabel"
            elif status.is_occupied:
                fill_color = "#d92d20"
                led_text = "RED"
                label_style = "Bad.TLabel"
            else:
                fill_color = "#16a34a"
                led_text = "GREEN"
                label_style = "Good.TLabel"

            led_canvas.create_oval(12, 10, 82, 80, fill=fill_color, outline="#1f2937", width=2)
            led_canvas.create_text(47, 45, text=led_text, fill="#ffffff", font=("Segoe UI", 11, "bold"))

            status_label.configure(text=status.label, style=label_style)
            if status.is_valid:
                distance_label.configure(text=f"Distance: {status.distance_cm:.2f} cm")
                echo_label.configure(text=f"Echo: {status.echo_time_us:.2f} us")
            else:
                distance_label.configure(text="Distance: invalid")
                echo_label.configure(text=status.message)

    def _update_summary(self, state: ParkingSystemState) -> None:
        self.summary_labels["free"].configure(text=f"Free: {state.free_count}")
        self.summary_labels["occupied"].configure(text=f"Occupied: {state.occupied_count}")
        self.summary_labels["invalid"].configure(text=f"Invalid: {state.invalid_count}")

    def _update_lcd(self, state: ParkingSystemState) -> None:
        lines = ["SMART PARKING SYSTEM", "-" * 22]

        for status in state.statuses:
            short_status = "ERR"
            if status.is_valid:
                short_status = "OCC" if status.is_occupied else "FREE"
            lines.append(f"S{status.slot_id}: {short_status:<4}")

        lines.append("-" * 22)
        if state.parking_full:
            lines.append("PARKING FULL")
        elif state.invalid_count > 0:
            lines.append(f"CHECK SENSOR: {state.invalid_count}")
        else:
            lines.append(f"AVAILABLE: {state.free_count}")

        self.lcd_text.configure(state="normal")
        self.lcd_text.delete("1.0", tk.END)
        self.lcd_text.insert("1.0", "\n".join(lines))
        self.lcd_text.configure(state="disabled")

    def _update_indicators(self, state: ParkingSystemState) -> None:
        self.buzzer_canvas.delete("all")
        buzzer_fill = "#d92d20" if state.buzzer_on else "#d8dee8"
        buzzer_text = "ON" if state.buzzer_on else "OFF"
        self.buzzer_canvas.create_rectangle(10, 18, 84, 54, fill=buzzer_fill, outline="#1f2937", width=2)
        self.buzzer_canvas.create_arc(78, 14, 132, 58, start=-55, extent=110, style=tk.ARC, width=3, outline="#1f2937")
        self.buzzer_canvas.create_text(47, 36, text=buzzer_text, fill="#ffffff" if state.buzzer_on else "#1f2937", font=("Segoe UI", 12, "bold"))

        self.gate_canvas.delete("all")
        self.gate_canvas.create_line(12, 58, 138, 58, width=3, fill="#1f2937")
        self.gate_canvas.create_rectangle(20, 20, 34, 58, fill="#52616f", outline="#1f2937")
        if state.gate_open:
            self.gate_canvas.create_line(32, 24, 116, 8, width=8, fill="#16a34a")
            gate_text = "OPEN"
            color = "#16a34a"
        else:
            self.gate_canvas.create_line(34, 26, 128, 54, width=8, fill="#d92d20")
            gate_text = "CLOSED"
            color = "#d92d20"
        self.gate_canvas.create_text(80, 36, text=gate_text, fill=color, font=("Segoe UI", 11, "bold"))

    def _append_serial_output(self, state: ParkingSystemState) -> None:
        timestamp = time.strftime("%H:%M:%S")
        parts = []
        for status in state.statuses:
            if status.is_valid:
                parts.append(f"S{status.slot_id}={status.label}({status.distance_cm:.1f}cm)")
            else:
                parts.append(f"S{status.slot_id}=ERROR")

        buzzer = "ON" if state.buzzer_on else "OFF"
        gate = "OPEN" if state.gate_open else "CLOSED"
        line = (
            f"[{timestamp}] "
            + " | ".join(parts)
            + f" | Free={state.free_count} | Occupied={state.occupied_count}"
            + f" | Buzzer={buzzer} | Gate={gate}\n"
        )

        self.serial_text.configure(state="normal")
        self.serial_text.insert(tk.END, line)
        self.serial_text.see(tk.END)

        line_count = int(self.serial_text.index("end-1c").split(".")[0])
        if line_count > 250:
            self.serial_text.delete("1.0", "80.0")
        self.serial_text.configure(state="disabled")

    def _auto_tick(self) -> None:
        if self.auto_mode.get():
            random_slot = random.randrange(TOTAL_SLOTS)
            current = self.distance_vars[random_slot].get()

            if current < self._safe_threshold():
                new_distance = random.choice([28.0, 35.0, 50.0, 70.0])
                action = "vehicle left"
            else:
                new_distance = random.choice([5.0, 8.0, 11.0, 13.0])
                action = "vehicle parked"

            self.distance_vars[random_slot].set(new_distance)
            self.controller.sensors[random_slot].set_distance(new_distance)
            self.status_var.set(f"Auto traffic: {action} at slot {random_slot + 1}")
            self.refresh_system()

        self.after(1500, self._auto_tick)


def print_console_instructions() -> None:
    print("=" * 72)
    print("Smart Parking System using Ultrasonic Sensors - Python Simulation")
    print("=" * 72)
    print("Distance formula:")
    print("  Distance = (Echo Time x Speed of Sound) / 2")
    print("Slot logic:")
    print("  If distance < threshold, slot is OCCUPIED")
    print("  Else, slot is FREE")
    print("")
    print("Use the sliders to simulate vehicle distance from each sensor.")
    print("Set a small distance such as 5 cm to simulate an occupied slot.")
    print("Set a larger distance such as 50 cm to simulate a free slot.")
    print("=" * 72)


def main() -> None:
    print_console_instructions()
    app = SmartParkingApp()
    app.mainloop()


if __name__ == "__main__":
    main()
