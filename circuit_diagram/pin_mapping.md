# Circuit Diagram and Pin Mapping

Use this file as the text version of the circuit diagram. You can recreate the same circuit in Wokwi, Tinkercad Circuits, Proteus, or on a breadboard.

## ESP32 Full Feature Pin Mapping

| Module | VCC | GND | Signal Pins |
|---|---|---|---|
| HC-SR04 Sensor 1 | 5V | GND | TRIG GPIO5, ECHO GPIO13 |
| HC-SR04 Sensor 2 | 5V | GND | TRIG GPIO18, ECHO GPIO12 |
| HC-SR04 Sensor 3 | 5V | GND | TRIG GPIO19, ECHO GPIO14 |
| HC-SR04 Sensor 4 | 5V | GND | TRIG GPIO23, ECHO GPIO35 |
| Slot 1 Green LED | GPIO26 through 220 ohm resistor | GND | Free indication |
| Slot 2 Green LED | GPIO25 through 220 ohm resistor | GND | Free indication |
| Slot 3 Green LED | GPIO33 through 220 ohm resistor | GND | Free indication |
| Slot 4 Green LED | GPIO32 through 220 ohm resistor | GND | Free indication |
| Slot 1 Red LED | GPIO4 through 220 ohm resistor | GND | Occupied indication |
| Slot 2 Red LED | GPIO16 through 220 ohm resistor | GND | Occupied indication |
| Slot 3 Red LED | GPIO17 through 220 ohm resistor | GND | Occupied indication |
| Slot 4 Red LED | GPIO2 through 220 ohm resistor | GND | Occupied indication |
| Buzzer | GPIO15 | GND | Parking full alert |
| Servo Gate Optional | 5V external recommended | Common GND | Signal GPIO27 |
| I2C LCD | 5V or 3.3V module-dependent | GND | SDA GPIO21, SCL GPIO22 |

## Arduino UNO Note

Arduino UNO can run a reduced build, but it does not have enough clean GPIO pins for 4 sensors, 8 LEDs, buzzer, LCD, and servo at the same time without compromises. For UNO, choose one of these clean options:

1. Use the Python simulation as the complete virtual proof.
2. Use fewer slots, for example 2 sensors with LEDs and LCD.
3. Use ESP32 for the complete hardware build because it has more GPIO pins.
4. Use an I2C GPIO expander such as PCF8574 for LEDs.

## Safe Wiring Notes

- Always connect all module grounds together.
- Use 220 ohm or 330 ohm resistors in series with LEDs.
- Do not power a servo directly from the Arduino 5V pin if the servo draws high current.
- For ESP32, reduce each HC-SR04 ECHO signal from 5V to 3.3V using a voltage divider.
- Mount each ultrasonic sensor above or in front of a parking slot so a parked vehicle produces a shorter measured distance.
