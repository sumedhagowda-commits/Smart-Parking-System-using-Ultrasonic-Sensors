# Smart Parking System using Ultrasonic Sensors

Embedded smart parking system using ultrasonic sensors for real-time parking slot detection, availability counting, visual indication, and parking-full alerts.

## Overview

This project detects whether parking slots are free or occupied using ultrasonic distance measurement. It includes a complete Python simulation for VS Code and Arduino code for real hardware implementation.

## Problem Statement

Traditional parking management is inefficient because drivers often search manually for available slots. This wastes time, increases congestion, and requires more manpower. A smart parking system gives real-time slot visibility and improves parking flow.

## Objectives

- Detect slot occupancy using ultrasonic sensor distance.
- Count available and occupied slots.
- Show status on LCD/OLED style display.
- Indicate each slot using red and green LEDs.
- Activate buzzer when parking is full.
- Provide a virtual simulation for students without hardware.
- Keep the project GitHub-ready and interview-ready.

## Features

- 4 parking slot simulation
- HC-SR04 style distance and echo-time calculation
- Configurable threshold
- Red LED for occupied slots
- Green LED for free slots
- LCD/OLED display simulation
- Serial monitor style log
- Buzzer alert when parking is full
- Optional gate open/closed behavior
- Noise and invalid echo testing
- Automated traffic mode
- Arduino hardware code
- Unit tests

## Tech Stack and Options

| Option | Components | Difficulty | Hardware Required |
|---|---|---|---|
| A - Easy | Arduino UNO, 2 ultrasonic sensors, LEDs, serial monitor | Beginner | Optional if using Python simulation |
| B - Recommended | ESP32, 4 ultrasonic sensors, LCD/OLED, LEDs, buzzer | Intermediate | Optional |
| C - Advanced | ESP32, many sensors, servo gate, Wi-Fi dashboard, RFID | Advanced | Yes for full demo |

Recommended student path: use Option B in Python simulation, then implement a smaller Arduino hardware version if components are available.

## Embedded Systems Concepts

- Microcontroller: reads sensors and controls outputs.
- GPIO: connects trigger, echo, LEDs, buzzer, and servo pins.
- Ultrasonic sensor: measures object distance using sound waves.
- Timer: measures echo pulse duration.
- Threshold logic: decides occupied or free.
- Display: shows available slots and parking-full status.
- Serial communication: prints debugging output.
- State tracking: stores each slot state before updating outputs.

## System Architecture

```text
Parking Slot
    -> Ultrasonic Sensor
    -> Distance Measurement
    -> Controller Logic
    -> Occupied / Free Decision
    -> Available Slot Counter
    -> LCD / LED / Buzzer / Gate Output
```

## Folder Structure

```text
Smart-Parking-System-Embedded-System/
|-- src/
|-- arduino_code/
|-- simulation/
|-- circuit_diagram/
|-- data/
|-- test_cases/
|-- outputs/
|-- screenshots/
|-- reports/
|-- docs/
|-- README.md
|-- requirements.txt
`-- .gitignore
```

## How To Run In VS Code

1. Open this folder in VS Code.
2. Make sure Python 3 is installed.
3. Open the VS Code terminal in the project root.
4. Run the GUI simulation:

```bash
python simulation/smart_parking_simulation.py
```

5. For a terminal-only demo, run:

```bash
python simulation/console_demo.py
```

6. Run automated tests:

```bash
python -m unittest discover -s test_cases
```

No external Python packages are required.

## Distance Calculation

```text
Distance = (Echo Time x Speed of Sound) / 2
```

The division by two is required because the ultrasonic wave travels from the sensor to the object and then returns to the sensor.

## Parking Slot Logic

```text
IF distance < threshold:
    slot = OCCUPIED
ELSE:
    slot = FREE
```

Example threshold: 15 cm.

| Distance | Status |
|---|---|
| 5 cm | Occupied |
| 10 cm | Occupied |
| 15 cm | Free |
| 30 cm | Free |

## Sample Output

```text
Slot 1: OCCUPIED distance=7.0 cm
Slot 2: FREE     distance=50.0 cm
Slot 3: OCCUPIED distance=10.0 cm
Slot 4: FREE     distance=50.0 cm
Available slots: 2
Buzzer: OFF
Gate: OPEN
```

When all slots are occupied:

```text
PARKING FULL
Buzzer: ON
Gate: CLOSED
```

## Circuit Diagram

See `circuit_diagram/pin_mapping.md` for full wiring instructions.

Basic HC-SR04 connection:

| HC-SR04 Pin | Microcontroller |
|---|---|
| VCC | 5V |
| GND | GND |
| TRIG | Digital output pin |
| ECHO | Digital input pin |

For ESP32, connect ECHO through a voltage divider because many HC-SR04 modules output 5V logic.

## Virtual Simulation

The main virtual simulation is the Python Tkinter app in `simulation/smart_parking_simulation.py`.

Optional online simulation can be created in Wokwi or Tinkercad:

1. Add ESP32 DevKit.
2. Add 4 ultrasonic sensors.
3. Add red and green LEDs.
4. Add buzzer.
5. Add LCD/OLED.
6. Paste `arduino_code/smart_parking_arduino.ino`.
7. Change sensor distances and verify slot status.

## Test Cases

See `docs/testing_strategy.md` and `test_cases/test_parking_logic.py`.


## GitHub Upload Strategy

```bash
git init
git add .
git commit -m "Initial project setup"
git branch -M main
git remote add origin <repository-url>
git push -u origin main
```

Suggested future commits:

- `Add ultrasonic distance measurement`
- `Implement parking slot detection`
- `Add multiple slot monitoring`
- `Add LED parking indicators`
- `Implement LCD available slot display`
- `Add parking full alert`
- `Complete virtual simulation and testing`
- `Add project documentation`

## Day-Wise Proof Building

| Day | Work | Commit Message | Screenshot |
|---|---|---|---|
| 1 | Project setup and circuit planning | Initial project setup | Folder structure |
| 2 | Single ultrasonic sensor logic | Add ultrasonic distance measurement | Single sensor output |
| 3 | Slot detection | Implement parking slot detection | Occupied/free proof |
| 4 | Multiple sensor integration | Add multiple slot monitoring | 4 slot status |
| 5 | LED indicators | Add LED parking indicators | Red/green LEDs |
| 6 | Display output | Implement LCD available slot display | LCD panel |
| 7 | Full alert | Add parking full alert | Buzzer ON |
| 8 | Simulation and testing | Complete virtual simulation and testing | Test run |
| 9 | Documentation | Add project documentation | README preview |

## Industry Relevance

Smart parking systems are used in shopping malls, airports, hospitals, office buildings, railway stations, universities, residential societies, commercial parking facilities, and smart cities. They reduce search time, improve space utilization, reduce congestion, automate monitoring, and improve customer experience.

## Limitations

- Sensor readings depend on mounting position.
- Ultrasonic sensors can be noisy in some environments.
- Arduino UNO has limited GPIO pins for a full system with LCD, servo, LEDs, and many sensors.

## Future Improvements

- ESP32 Wi-Fi dashboard
- Cloud database logging
- Mobile app
- RFID access control
- Payment integration
- Camera verification
- Larger multi-floor parking support

## Learning Outcomes

- Ultrasonic sensor interfacing
- Distance measurement
- GPIO control
- Threshold-based decision making
- Display and actuator control
- Simulation-based embedded project development
- Testing and documentation for GitHub

## Author

Student Embedded Systems Project
