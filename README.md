# piClock
A collection of LED Clocks based on Raspberri Pi Zero W. The library/deamon "pigpio" is used to handle up to 26 PWM channels for smooth blending the transitions.

## BCD Clock

A classic BCD (binary coded decimal) clock with 18 or 20 LEDs (12h or 24h). Additional LEDs for am/pm and colon can be configured in software.

![bcd.png](/bcd.Demo.jpg)

See [detail description](/bcd.md)

## Franconian Clock

A special word clock with 24 LEDs. It uses whole words per LED and a franconian style quater coding.

![franconian.png](/franconian.Demo.jpg)

See [detail description](/franconian.md)

## Pro and Cons for using a Raspberry Pi instead of Arduino/ESP

#### Pros:
* The RPi can use 26 GPIO pins directly with PWM without aa additional port expander or shift register. Most smaller/cheeper controller has too less pins to drive the LEDs directly.
* The RPi has a build in current limiter at GPIO pins. Resistors in line to LEDs are not necessary.
* The RPi Zero has an onboard WiFi to get the correct time via NTP. No external RTC needed.
* The RPi Zero has additional power and pins to run additional IoT features.
* Faster development (and code change).

#### Cons:
* Linux! Many steps to do for setup the controller. See next chanpter...
* Linux! Potential security leak in your local network.
* Little more expensive (about 20 Euro) than a ESP8266 (about 7 Euro).

## Prepare the Raspberry Pi Zero

See [detail description](/prepare.md)
