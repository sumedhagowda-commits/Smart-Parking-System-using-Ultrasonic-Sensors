# Testing Strategy

| Test Case | Input | Expected Output | Pass Criteria |
|---|---|---|---|
| All slots free | S1-S4 = 50 cm | Available = 4, buzzer OFF, gate OPEN | LCD and serial monitor show 4 free slots |
| One slot occupied | S1 = 7 cm, others 50 cm | Available = 3 | Slot 1 red LED ON, others green |
| Multiple slots occupied | S1 = 7 cm, S2 = 9 cm, others 50 cm | Available = 2 | Correct occupied/free count |
| All slots occupied | S1-S4 below 15 cm | Parking full | Buzzer ON and gate CLOSED |
| One vehicle leaves | Change one occupied slot to 50 cm | Available count increases by 1 | Buzzer turns OFF if no longer full |
| Noisy sensor reading | Enable noise in Python GUI | Slot still follows threshold logic | Status remains reasonable near stable distances |
| Invalid echo | Enable invalid echo | Slot shows ERROR | Invalid count increments |
| LCD update | Change any slot distance | LCD updates status and count | Display matches slot states |
| LED indication | Move slider below and above threshold | Red/green LED changes | Red means occupied, green means free |
| System reset | Press All Free | All slots free | Available = 4 |

Run automated tests:

```bash
python -m unittest discover -s test_cases
```

