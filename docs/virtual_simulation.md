# Virtual Simulation Guide

## VS Code Python Simulation

1. Open this project folder in VS Code.
2. Open a terminal in the project root.
3. Run:

```bash
python simulation/smart_parking_simulation.py
```

4. Move each slot slider:
   - 5 cm to 14 cm means occupied.
   - 15 cm or more means free.
5. Use `All Free`, `All Occupied`, and `Random Test` buttons for quick verification.
6. Watch the LCD/OLED panel, red/green LED indicators, buzzer state, gate state, and serial monitor log.

## Console-Only Simulation

Run:

```bash
python simulation/console_demo.py
```

This prints predefined test scenarios without opening a GUI window.

## Wokwi or Tinkercad Simulation

1. Create a new ESP32 DevKit project.
2. Add four HC-SR04 ultrasonic sensors.
3. Add red and green LEDs for every slot.
4. Add a buzzer.
5. Add an I2C LCD if available.
6. Add a servo motor if pins are available.
7. Connect the modules using `circuit_diagram/pin_mapping.md`.
8. Paste `arduino_code/smart_parking_arduino.ino`.
9. Start the simulation.
10. Set all sensor distances high and verify all slots are free.
11. Reduce Sensor 1 distance and verify Slot 1 is occupied.
12. Reduce Sensor 2 and Sensor 3 distances and verify the available count decreases.
13. Set all sensors below threshold and verify `PARKING FULL`, buzzer ON, and gate CLOSED.
14. Free one slot and verify buzzer OFF and available count 1.
