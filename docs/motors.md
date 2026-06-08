# Motor IDs

| Motor Name | ID |
|------------|----|
| Left Hip Yaw | 11 |
| Left Hip Roll | 12 |
| Left Hip Pitch | 13 |
| Left Knee | 14 |
| Left Ankle Pitch | 15 |
| Left Ankle Roll | 16 |
| Right Hip Yaw | 21 |
| Right Hip Roll | 22 |
| Right Hip Pitch | 23 |
| Right Knee | 24 |
| Right Ankle Pitch | 25 |
| Right Ankle Roll | 26 |
| Left Shoulder Pitch | 31 |
| Left Shoulder Roll | 32 |
| Left Elbow | 33 |
| Right Shoulder Pitch | 41 |
| Right Shoulder Roll | 42 |
| Right Elbow | 43 |
| Head | 51 |

# Motor Setup

First, factory reset all motors to clear any previous configurations if they have been used before. 
TODO: Add img of the factory reset in wizard ?

Then, some specific settings need to be applied through the Dynamixel Wizard software. While scanning for motors, be sure to scan for 57600 bps and Protocol 2.0, which are the default settings after a factory reset.

Apply the following settings to each motor:
    Return Delay Time: 0
    Baud Rate: 3 (1Mbps)
    Shutdown: 52 (Removing "Bit 0 Input voltage error")
    PWM Slope: 255 (no slope)
