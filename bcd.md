# BCD Clock
BCD LED Clock based on Raspberri Pi Zero W and pigpio-lib

## Hardware Design
![bcd.FrontView.png](/bcd.FrontView.png)

#### LEDs
Solder all cathodes (short leg) of the LEDs together and connect them to GND.
Solder the anodes (long leg) of the LEDs to the corresponding pin on the RPi (see pinout). Resistors are not necessary

Note: The current to the LEDs is limited by the RPi to 4 mA per GPIO via software. Possible values are 2, 4, 8, 16 (higher than 4 is not recommended).

#### RPi Pin Header

Pins 11 to 38 should be used for the LEDs.

Pins 39 to 40 is reserved for an option button

Pins 1 to 10 are free for optional I²C devices, 1-Wire devices, serial adapter and other GPIO stuff.


## Pinout
![bcd.Pinout.png](/bcd.Pinout.png)

Note: The LED to GPIO mapping can be changed in source code
