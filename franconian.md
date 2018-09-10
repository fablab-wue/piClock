# Franconian Clock

![franconian.png](/franconian.Demo.jpg)

A real word clock with 24 LEDs controlled by a Raspberry Pi Zero W (RPi) in Python.

## The goal:
Reduce the additional components to an absolute minimum. No additional PCBs or parts (shift register, port expander, driver, resistors, …) are needed.

## The Result:
Just glue 24 strong LEDs behind/below acrylic plates with the words and wire them directly to the RPi pads. The soldering is reduced to cables between LEDs and RPi. The clock can be powered over a Micro-USB cable from a mobile phone power supply.

## The Features:
 * The transitions between time values are blended via PWM for all LEDs.
 * The current time is received via NTP over WiFi.
 * Two free pins for additional gadgets (I²C, GPIO).



# Details

## The words:
In the German language it is common to say „halb zwölf“ (translated: „half twelve“ or „half of twelve“ = 11:30h).

In a little area in the south of Germany – Franconia – you can hear people saying consequently „viertel zwölf“ („quarter twelve“ = 11:15h) and „dreiviertel zwölf“ („three-quarter twelve“ = 11:45h). In the other parts of Germany the Franconians often are not understood.

It is also common to say „fife to twelve“ (11:55h) and „fife past twelve“ (12:05h). This is equal in German and English.

In final consequence it is logical to say „zwei vor dreiviertel zwölf“ („two to tree-quarter twelve“ = 12:42h = 23:42h)

The clock is using this Franconian schema/wording to show the time with 24 elements/LEDs.

Most other so called “word clocks” are using illuminated characters and get a time in a resolution of 5 minutes. The Franconian clock uses 24 complete words and gets a time resolution of 1 minute!

#### To implement this wording you use 4 groups:

 * Numbers 1 to 7 for minutes
 * “to” and “past”
 * “quarter”, “half” and “three-quarter” (the “quarter” is shared)
 * Numbers 1 to 12 for hours


## Easy to Build

Reducing the electronic components to the RPi, the LEDs and the wires between them, you can concentrate on form and design.

## LEDs

Using high luminance LEDs with a max. of 3.1 volts. Any color you like.

The current to the LEDs is limited by the RPi to 8 mA per GPIO via software. Possible values are 2, 4, 8, 16 (higher than 8 is not recommended). The usual resistor in line of the LED is not needed!

## Powering

The RPi can be powered over a Micro-USB cable. Use a mobile phone power supply (for USB) or a nearby PC/server with USB.

The typical current at the 5 volts line is about 100 mA with peaks up to 300 mA when WiFi fires.

## Design

Following the rules of the wording you are free to sculpt, form and place the illuminated words with any material and technique.

## Upgrading

To use low voltage bulbs (5...24V), you can add 3 driver ICs like the ULN2803 directly to the RPi without a level shifter.

Pins for I²C are left free for additional IoT gadgets for e.g. temperature, humidity, luminosity, presence, notification... 


# Instructions

## RPi Pinout

Pins 7 to 40 should be used for the clock LEDs.

Pins 1 to 6 are free for optional I²C devices and other GPIO stuff.

### Default Pinout:

![Franconian.Pinout.png](/franconian.Pinout.png)

Four groups to set the time as text:

E.g.: "| drei | vor | drei.viertel | zwölf |" (23:42h)

#### Minute group in random order
| Pin | engl. | ger. |
| --- | --- | --- |
| M1 | one | eins |
| M2 | two | zwei |
| M3 | three | drei |
| M4 | four | vier |
| M5 | five | fünf |
| M6 | six | sechs |
| M7 | seven | sieben |

#### To/past group in random order
| Pin | engl. | ger. |
| --- | --- | --- |
| TO | to | vor |
| PAST | past | nach |

#### Quater group - Q3 followed directly by Q1; Q2 anywhere
| Pin | engl. | ger. |
| --- | --- | --- |
| Q1 | ...quarter | ...viertel |
| Q2 | half | halb |
| Q3 | three... | drei... |

#### Hour group in random order
| Pin | engl. | ger. |
| --- | --- | --- |
| H1 | one | eins |
| H2 | two | zwei |
| H3 | three | drei |
| H4 | four | vier |
| H5 | five | fünf |
| H6 | six | sechs |
| H7 | seven | sieben |
| H8 | eigth | acht |
| H9 | nine | neun |
| H10 | ten | zehn |
| H11 | eleven | elf |
| H12 | twelve | zwölf |


Note: The LED to GPIO mapping can be easily changed in source code

## RPi Software

See detail description on https://github.com/fablab-wue/piClock/blob/master/prepare.md

In short:

 * Setup network/WiFi
 * Disable SPI, 1-Wire, Serial
 * Install Python3, pigpio-lib
 * Download source from GitHub
 * Autostart at boot the ~/piClock/franconian.py

Linux experts will configure the RPi in no-time. Less experienced users (like me) needed more time for configuring than for wood-working and soldering.
