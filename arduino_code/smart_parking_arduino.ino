/*
  Smart Parking System using Ultrasonic Sensors
  Board: ESP32 DevKit recommended for the full feature build

  Features:
    - 4 HC-SR04 ultrasonic sensors
    - Red LED for occupied slot
    - Green LED for free slot
    - Buzzer when all slots are occupied
    - Optional I2C 16x2 LCD display
    - Optional servo barrier gate

  Required library for LCD:
    LiquidCrystal_I2C by Frank de Brabander or compatible

  Optional library for servo:
    ESP32Servo
*/

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define USE_SERVO_GATE 0

#if USE_SERVO_GATE
#include <ESP32Servo.h>
#endif

const byte TOTAL_SLOTS = 4;
const float OCCUPIED_THRESHOLD_CM = 15.0;
const unsigned long ECHO_TIMEOUT_US = 30000UL;

const byte I2C_SDA_PIN = 21;
const byte I2C_SCL_PIN = 22;

const byte trigPins[TOTAL_SLOTS] = {5, 18, 19, 23};
const byte echoPins[TOTAL_SLOTS] = {13, 12, 14, 35};
const byte greenLedPins[TOTAL_SLOTS] = {26, 25, 33, 32};
const byte redLedPins[TOTAL_SLOTS] = {4, 16, 17, 2};

const byte BUZZER_PIN = 15;
const byte SERVO_PIN = 27;

LiquidCrystal_I2C lcd(0x27, 16, 2);

#if USE_SERVO_GATE
Servo gateServo;
#endif

bool slotOccupied[TOTAL_SLOTS] = {false, false, false, false};
float slotDistanceCm[TOTAL_SLOTS] = {0, 0, 0, 0};

float readDistanceCm(byte trigPin, byte echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  unsigned long echoTimeUs = pulseIn(echoPin, HIGH, ECHO_TIMEOUT_US);

  if (echoTimeUs == 0) {
    return -1.0;
  }

  return (echoTimeUs * 0.0343) / 2.0;
}

void updateSlot(byte index) {
  float distanceCm = readDistanceCm(trigPins[index], echoPins[index]);
  slotDistanceCm[index] = distanceCm;

  if (distanceCm < 0) {
    slotOccupied[index] = false;
    digitalWrite(greenLedPins[index], LOW);
    digitalWrite(redLedPins[index], LOW);
    return;
  }

  slotOccupied[index] = distanceCm < OCCUPIED_THRESHOLD_CM;

  if (slotOccupied[index]) {
    digitalWrite(greenLedPins[index], LOW);
    digitalWrite(redLedPins[index], HIGH);
  } else {
    digitalWrite(greenLedPins[index], HIGH);
    digitalWrite(redLedPins[index], LOW);
  }
}

byte countOccupiedSlots() {
  byte count = 0;
  for (byte i = 0; i < TOTAL_SLOTS; i++) {
    if (slotOccupied[i]) {
      count++;
    }
  }
  return count;
}

void updateDisplay(byte freeSlots, bool parkingFull) {
  lcd.clear();

  if (parkingFull) {
    lcd.setCursor(0, 0);
    lcd.print(" PARKING FULL ");
    lcd.setCursor(0, 1);
    lcd.print(" Gate: CLOSED ");
    return;
  }

  lcd.setCursor(0, 0);
  lcd.print("Available: ");
  lcd.print(freeSlots);

  lcd.setCursor(0, 1);
  for (byte i = 0; i < TOTAL_SLOTS; i++) {
    lcd.print("S");
    lcd.print(i + 1);
    lcd.print(slotOccupied[i] ? ":O " : ":F ");
  }
}

void updateAlertAndGate(bool parkingFull) {
  if (parkingFull) {
    digitalWrite(BUZZER_PIN, HIGH);
#if USE_SERVO_GATE
    gateServo.write(0);
#endif
  } else {
    digitalWrite(BUZZER_PIN, LOW);
#if USE_SERVO_GATE
    gateServo.write(90);
#endif
  }
}

void printSerialOutput(byte freeSlots, byte occupiedSlots, bool parkingFull) {
  Serial.println("----------------------------------------");

  for (byte i = 0; i < TOTAL_SLOTS; i++) {
    Serial.print("Slot ");
    Serial.print(i + 1);
    Serial.print(": ");

    if (slotDistanceCm[i] < 0) {
      Serial.print("INVALID ECHO");
    } else {
      Serial.print(slotOccupied[i] ? "OCCUPIED" : "FREE");
      Serial.print(" | Distance: ");
      Serial.print(slotDistanceCm[i], 1);
      Serial.print(" cm");
    }
    Serial.println();
  }

  Serial.print("Available Slots: ");
  Serial.println(freeSlots);
  Serial.print("Occupied Slots : ");
  Serial.println(occupiedSlots);
  Serial.print("Buzzer         : ");
  Serial.println(parkingFull ? "ON" : "OFF");
  Serial.print("Gate           : ");
  Serial.println(parkingFull ? "CLOSED" : "OPEN");
}

void setup() {
  Serial.begin(9600);
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);

  for (byte i = 0; i < TOTAL_SLOTS; i++) {
    pinMode(trigPins[i], OUTPUT);
    pinMode(echoPins[i], INPUT);
    pinMode(greenLedPins[i], OUTPUT);
    pinMode(redLedPins[i], OUTPUT);
  }

  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);

  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Smart Parking");
  lcd.setCursor(0, 1);
  lcd.print("System Ready");

#if USE_SERVO_GATE
  gateServo.attach(SERVO_PIN);
  gateServo.write(90);
#endif

  delay(1500);
}

void loop() {
  for (byte i = 0; i < TOTAL_SLOTS; i++) {
    updateSlot(i);
    delay(60);
  }

  byte occupiedSlots = countOccupiedSlots();
  byte freeSlots = TOTAL_SLOTS - occupiedSlots;
  bool parkingFull = freeSlots == 0;

  updateAlertAndGate(parkingFull);
  updateDisplay(freeSlots, parkingFull);
  printSerialOutput(freeSlots, occupiedSlots, parkingFull);

  delay(1000);
}
