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

### Why RPi?

#### Pros:

 * The RPi can use up to 26 GPIO pins directly without an additional port expander or shift register. Most smaller/cheaper controllers do not have enough pins to drive the 20 LEDs directly.
 * The RPi has a built in current limiter on the GPIO pins. Resistors in line to LEDs are not necessary.
 * The RPi Zero has onboard WiFi to get the correct time via NTP. No external RTC is needed.
 * The RPi Zero has sufficient power and pins to run additional IoT features.
 * Faster development (and code change). 

#### Cons:

 * Linux! Many steps to setup the controller. See chapter on GitHub Wiki...
 * Linux! Potential security leaks to your local network.
 * A little more expensive (about 20 Euro incl. MicroSD) than an ESP8266 (<7 Euro). 

### Why pigpio-lib?

#### Pros:

 * This lib can handle software PWM for ALL 26 GPIOs without glitches.
 * Faster than BCM-lib.
 * Development and debugging can be done on your PC, remote-controlling the RPi GPIOs over the network.
 * Implementation for several programming languages available. 

#### Cons:

 * pigpio-deamon eats 7...10 percent of CPU time continously, independent of how many GPIOs or PWMs are active.
 * The lib's documentation leaves room for improvement. 


## Prepare the Raspberry Pi Zero

See [detail description](/prepare.md)
