# Interview Preparation

1. Explain your project.
   - My project is a Smart Parking System using ultrasonic sensors. Each parking slot has one sensor that measures distance. If the measured distance is below the configured threshold, the system marks that slot as occupied. The controller counts free slots, shows the result on a display, turns on red or green LEDs, and activates a buzzer when the parking area is full.

2. Why did you use ultrasonic sensors?
   - Ultrasonic sensors are low-cost, easy to interface, and suitable for distance measurement. They work by sending a sound pulse and measuring the echo return time, which is enough to detect whether a car is present in a slot.

3. What is the distance formula?
   - Distance equals echo time multiplied by speed of sound divided by two. Division by two is required because the sound travels from the sensor to the object and then back to the sensor.

4. What does the threshold value mean?
   - The threshold is the distance limit used to decide if a slot is occupied. In this project I used 15 cm for simulation. If distance is below 15 cm, the slot is occupied; otherwise it is free.

5. Which embedded concepts are used?
   - The project uses GPIO, sensor interfacing, timing, threshold logic, serial communication, display output, actuator control, and state tracking.

6. How do you handle multiple sensors?
   - The controller reads each sensor one by one, stores each slot status, counts occupied and free slots, then updates LEDs, display, buzzer, and optional gate.

7. How does the buzzer work?
   - The buzzer turns on only when all valid slots are occupied. If at least one slot is free, the buzzer remains off.

8. What problems did you consider during testing?
   - I tested free slots, occupied slots, parking full, one vehicle leaving, noisy readings, invalid echo readings, LCD updates, and LED behavior.

9. How would you improve this project?
   - I would use ESP32 Wi-Fi to send live slot data to a web dashboard, add cloud logging, add RFID entry authentication, and build a mobile app for real-time availability.

10. Why is this project industry-relevant?
    - Similar systems are used in malls, airports, hospitals, offices, universities, and smart cities to reduce parking search time, improve space utilization, and automate monitoring.

