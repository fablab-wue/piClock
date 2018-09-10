# BCD Clock

![bcd.png](/bcd.Demo.jpg)

A classic BCD (binary coded decimal) clock with 18 or 20 LEDs (12h or 24h) controlled by a Raspberry Pi Zero W (RPi) in Python.

## The goal:
Reduce the electronic components to an absolute minimum. No additional PCBs or parts (shift register, port expander, driver, resistors, …) are needed.

## Result:
Just glue 18 or 20 standard LEDs into a front panel and wire them directly to the RPi pads. The soldering is reduced to cables between LEDs and RPi. The clock can be powered over a Micro-USB-cable from a mobile phone power supply.

## Features:
 * The transitions between time values are blended via PWM for all LEDs.
 * The PWM is also used to let those LEDs that are off glow a bit for better reading at night.
 * 12 and 24 hour format.
 * Additional LEDs for am/pm and colon can be configured in software.
 * The current time is received via NTP over WiFi.
 * 6 free pins for additional gadgets (I²C, 1-Wire, serial, GPIO, …).

# Details

## Easy to Build

Reducing the electronic components to one RPi, the LEDs, and the wires between them allows you to concentrate on the form and design.

## LEDs

Using standard LEDs with a max. of 3.1 volts. Any color and shape you like.

The current to the LEDs is limited by the RPi to 4 mA per GPIO via software. Possible values are 2, 4, 8, 16 (higher than 4 is not recommended). The usual resistor in line of the LED is not needed!

## Powering

The RPi can be powered over a Micro-USB cable. Use a mobile phone power supply (for USB) or a nearby PC/server with USB.

The typical current on the 5 volts line is about 100 mA with peaks up to 300 mA when WiFi fires.

## Adaption

The clock is implemented in the Python file ~/piClock/bcd.py. It can be adapted to use a different pin to LED mapping, and 2 additional pins can be defined to extend the displayable hours to 24.

## Upgrading

To use low voltage bulbs (5...24V), you can add 3 driver ICs like the ULN2008 or ULN2803 directly to the RPi without a level shifter.

To use a pure binary display (6 LEDs for minutes/seconds) the python program can be easily adapted.

Pins for I²C, 1-Wire, serial and button are left free for additional IoT gadgets for e.g. temperature, humidity, luminosity, presence, notifications...


# Instructions 

## Housing

In this example I used LASER-cut plywood with a veneer layer and bend cuts.

Feel free to use any kind of material and technique for your housing.

## Layout

The BCD coding uses 4 LEDs for the second digit and 3 LEDs for the first digit. In the 12-hour configuration the hours are also displayed with 4 LEDs.

The layout can be horizontal (like this example) or vertical. The second digit LEDs can be aligned in a row or between the first digit LEDs. Feel free to experiment/design.

![bcd.FrontView.png](/bcd.FrontView.png)

## LEDs

Solder all cathodes (short leg, minus) of the LEDs together and connect them to GND. Solder the anodes (long leg, plus) of the LEDs to the corresponding pin on the RPi (see pinout). Resistors are not necessary.

## RPi Pinout

Pins 11 to 38 should be used for the clock LEDs.

Pins 39 to 40 is reserved for an option button.

Pins 1 to 10 are free for optional I²C devices, 1-Wire devices, serial adapter and other GPIO stuff.

#### Default Pinout:

![bcd.Pinout.png](/bcd.Pinout.png)

Note: The LED to GPIO mapping can be easily changed in source code

## RPi Software

See detail description on https://github.com/fablab-wue/piClock/blob/master/prepare.md

#### In short:

 * Setup network/WiFi
 * Disable SPI
 * Install Python3, pigpio-lib
 * Download source from GitHub
 * Autostart at boot the ~/piClock/bcd.py

Linux experts will configure the RPi in no-time. Less experienced users (like me) needed more time for configuring than for wood-working and soldering.

