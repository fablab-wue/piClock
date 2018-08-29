# Franconian Clock
Franconian LED Clock based on Raspberri Pi Zero W and pigpio-lib

## Hardware Design

Four groups to set the time as text:

E.g.: "| drei | vor | drei.viertel | zwölf |" (23:42h)

24 LEDs are needed.

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
| Q1 | ...quater | ...viertel |
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



#### LEDs
Solder all cathodes (short leg) of the LEDs together and connect them to GND.
Solder the anodes (long leg) of the LEDs to the corresponding pin on the RPi (see pinout). Resistors are not necessary

Note: The current to the LEDs is limited by the RPi to 8 mA per GPIO via software. Possible values are 2, 4, 8, 16
Note: A maximum of 5 LEDs is powered at the same time.

#### RPi Pin Header

Pins 4 to 40 should be used for the LEDs.

Pins 3 and 5 are free for optional I²C devices or other GPIO stuff.


## Pinout
![Franconian.Pinout.png](/franconian.Pinout.png)

Note: The LED to GPIO mapping can be changed in source code
