# Smart Parking System using Ultrasonic Sensors - Project Report

## Abstract

This project implements a smart parking system that detects parking slot availability using ultrasonic sensors. The system measures distance for each slot, classifies slots as free or occupied, counts available slots, displays parking status, and triggers an alert when parking is full. A Python simulation is included so the project can be tested without physical hardware.

## Introduction

Finding a free parking slot manually wastes time and increases congestion. A smart parking system automates slot monitoring and gives real-time information to drivers or parking operators.

## Problem Statement

Traditional parking areas often do not show accurate slot availability. Drivers must search manually, which causes delays, fuel waste, and poor user experience.

## Objectives

- Detect whether each parking slot is occupied or free.
- Count available slots in real time.
- Display status using LCD/OLED or simulated display.
- Use red and green LEDs for slot guidance.
- Activate buzzer when parking is full.
- Provide hardware and virtual simulation implementation.

## Existing System

Manual parking management depends on guards, signs, or driver observation. It is slower and less accurate than automated slot-level monitoring.

## Proposed System

Each slot uses an ultrasonic sensor. The controller reads distance, applies threshold logic, updates indicators, and reports the available count.

## Hardware Requirements

- Arduino UNO or ESP32
- HC-SR04 ultrasonic sensors
- Red and green LEDs
- Buzzer
- 16x2 I2C LCD or OLED
- Optional servo motor
- Breadboard, resistors, jumper wires, power supply

## Software Requirements

- VS Code
- Python 3
- Arduino IDE
- Optional Wokwi or Tinkercad Circuits

## System Architecture

```text
Parking Slot
    -> Ultrasonic Sensor
    -> Distance Measurement
    -> Microcontroller / Python Controller
    -> Occupied or Free Decision
    -> Available Slot Count
    -> LCD, LEDs, Buzzer, Gate, Serial Monitor
```

## Working Principle

The ultrasonic sensor sends a trigger pulse and waits for the reflected echo. Echo time is converted to distance. A short distance means a vehicle is present; a long distance means the slot is free.

## Distance Calculation

```text
Distance = (Echo Time x Speed of Sound) / 2
```

Division by two is needed because the sound pulse travels to the object and returns back to the sensor.

## Algorithm

1. Start system.
2. Read distance from each ultrasonic sensor.
3. Validate sensor readings.
4. Compare distance with threshold.
5. Mark slot occupied if distance is below threshold.
6. Count free and occupied slots.
7. Update LCD/OLED display.
8. Turn green LED on for free slot.
9. Turn red LED on for occupied slot.
10. Turn buzzer on if all slots are occupied.
11. Open optional gate if at least one slot is free.

## Simulation

The Python simulation provides sliders for four parking slots. Each slider represents the measured distance from a virtual HC-SR04 sensor. It also includes LCD output, LEDs, buzzer, gate, serial monitor, noise mode, invalid echo mode, and automated traffic mode.

## Testing

Testing covers all slots free, single slot occupied, multiple slots occupied, parking full, invalid sensor echo, noisy readings, LED indication, LCD update, buzzer alert, gate behavior, and reset behavior.

## Results

The project successfully detects free and occupied parking slots, calculates available slot count, displays slot status, and activates parking full alerts.

## Applications

Shopping malls, airports, hospitals, office buildings, railway stations, universities, residential societies, and smart city parking facilities.

## Advantages

- Reduces parking search time.
- Improves space utilization.
- Reduces manual monitoring.
- Gives real-time parking visibility.
- Beginner-friendly and expandable.

## Limitations

- Ultrasonic sensors can be affected by placement angle and environmental noise.
- Large parking systems need better wiring, networking, and sensor calibration.
- Arduino UNO has limited GPIO pins for a full feature build.

## Future Scope

- ESP32 Wi-Fi dashboard
- Cloud data logging
- RFID-based entry
- Mobile app
- Camera-based verification
- Payment integration

## Conclusion

The Smart Parking System demonstrates practical embedded systems concepts through sensor interfacing, GPIO control, timing, display output, and automation logic. The included Python simulation makes the project testable even without hardware.

