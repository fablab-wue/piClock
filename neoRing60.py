#!/usr/bin/python3
"""
Neo-Pixel-Clock for RPi Zero W
with x library
See https://learn.adafruit.com/neopixels-on-raspberry-pi?view=all
"""
__author__      = "Jochen Krapf"
__email__       = "jk@nerd2nerd.org"
__copyright__   = "Copyright 2018, JK"
__license__     = "GPL3"
__version__     = "0.0.1"

import pigpio
import time
from argparse import ArgumentParser
try:
    from neopixel import *
    NEOPIXEL = True
except:
    NEOPIXEL = False

#######
# definitions and configuration

#args.leds = 24
LED_MER = 0

LED_LUM_MAX = 255
LED_LUM_SCALE = 1.0

# LED strip configuration:
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)

REMOTE_RPI = 'raspberrypi.local'
GPIO_BUTTON = 21

#######
# init PIGPIO lib and deamon

#try:
#    PI = pigpio.pi()
#except:
#    PI = pigpio.pi(REMOTE_RPI)
#    if not PI.connected:
#        raise Exception('No connection to PIGPIO deamon on RPi')

#######
# global variables

last_button = -1
V = [0, 0, 0]

strip = None
args = None

#######

def hand_function(x):
    if not -1 < x < 1:
        return 0.0
    if x > 0:
        y = 1 - x
    else:
        y = 1 + x
    return y

# -----

def clear_leds():
    global args

    for i in range(args.leds):
        for j in range(3):
            V[j][i] = 0

# -----

def add_led_color(idx, value, rgb):
    global args, V

    if value <= 0:
        return

    idx += args.meridiem
    while idx >= args.leds:
        idx -= args.leds

    r, g, b = rgb
    V[0][idx] += r * value
    V[1][idx] += g * value
    V[2][idx] += b * value

# -----

def set_hand(idx, hand_pos, hand_width, rgb):
    global args

    for mirror in range(-args.leds, 2*args.leds, args.leds):
        x = (idx + mirror - hand_pos * args.leds) / hand_width
        value = hand_function(x)
        add_led_color(idx, value, rgb)

# =====

def init():
    global strip, args

    for j in range(3):
        V[j] = [0]*args.leds

    #PI.set_mode(GPIO_BUTTON, pigpio.INPUT)
    #PI.set_pull_up_down(GPIO_BUTTON, pigpio.PUD_UP)
    if NEOPIXEL:
        # Create NeoPixel object with appropriate configuration.
        strip = Adafruit_NeoPixel(args.leds, args.pin, LED_FREQ_HZ, LED_DMA, args.invert)
        # Intialize the library (must be called once before other functions).
        strip.begin()
        strip.setBrightness(255)

# =====

def loop():
    global strip, args

    global last_button

    clear_leds()

    for i in range(0, args.leds, args.leds//4):
        add_led_color(i, 0.05, (1, 1, 1))
    if args.leds >= 60:
        for i in range(0, args.leds, args.leds//12):
            add_led_color(i, 0.1, (1, 1, 1))

    # get act time
    t = time.time()
    t -= time.altzone

    # norm s, m, h to 0...1
    s = t / 60
    m = s / 60
    h = m / 12
    s = s - int(s)
    m = m - int(m)
    h = h - int(h)

    p = t / 3.14
    # linear ping-pong -1...1
    p = (p - int(p) - 0.5) * 4
    if p < -1: p = -2 - p
    if p > 1: p = 2 - p
    # pentulum
    if p > 0:
        p = 1 - p
        p *= p
        p = 1 - p
    else:
        p = 1 + p
        p *= p
        p = -1 + p
    # scale to circle
    p *= 0.1
    p += 0.5


    #print (h, m, s)

    for i in range(args.leds):
        set_hand(i, s, 1.5, (0, 0, 0.8))
        set_hand(i, m, 2.0, (0, 0.8, 0))
        set_hand(i, h, 2.5, (0.8, 0, 0))
        set_hand(i, p, 3.0, (0.4, 0.4, 0))

    if not NEOPIXEL:
        SYM = ' .▁▂▃▅▆▇█#???????'
        for j in range(3):
            print ('|', end='')
            for i in range(args.leds):
                print (SYM[int(V[j][i] * 10 +0.5)], end='')
        print ('|', end='')
        print (m)

    if NEOPIXEL:
        rgb = [0, 0, 0]
        for i in range(args.leds):
            for j in range(3):
                v = V[j][i]
                v *= LED_LUM_SCALE
                v *= v   # gamma correction
                v = int(v * LED_LUM_MAX + 0.5)
                if v > LED_LUM_MAX: v = LED_LUM_MAX
                rgb[j] = v
            color = Color(rgb[1], rgb[0], rgb[2])
            strip.setPixelColor(i, color)
        strip.show()

    return

    # check button
    button = PI.read(GPIO_BUTTON)
    if not button:
        #TODO
        pass

# =====

def main():
    global args

    parser = ArgumentParser(prog='piClock', conflict_handler='resolve')

    parser.add_argument("-l", "--leds", 
                        dest="leds", default=60, metavar='LEDS', type=int,
                        help="Number of LEDs")

    parser.add_argument("-m", "--meridiem", 
                        dest="meridiem", default=30, metavar='LED', type=int,
                        help="Index of meridiem LED")

    parser.add_argument("-p", "--pin", 
                        dest="pin", default=18, metavar='GPIO', type=int,
                        help="GPIO Number")

    parser.add_argument("-i", "--invert",
                        dest="invert", default=False, action="store_true", 
                        help="Invert GPIO pin")


    parser.add_argument("-w", "--noweb",
                        dest="useWeb", default=True, action="store_false", 
                        help="Don't start web server part")
    parser.add_argument("-W", "--useweb",
                        dest="useWeb", default=True, action="store_true", 
                        help="Start web server part")
                        
    parser.add_argument("-a", "--loglevel", 
                        dest="logLevel", default=0, type=int, metavar="LEVEL",
                        help="Set the maximum logging level - 0=no output, 1=error, 2=warning, 3=info, 4=debug, 5=ext.debug")

    parser.add_argument("-L", "--logfile", 
                        dest="logFile", default='Test', metavar="FILE",
                        help="Set FILE name for logging output")

    parser.add_argument("-q", "--quiet",
                        dest="verbose", default=True, action="store_false", 
                        help="don't print status messages to stdout")

    args = parser.parse_args()

    init()

    try:
        while True:
            loop()
            time.sleep(0.02)   # update with max 50 Hz

    except (KeyboardInterrupt, SystemExit):
        pass

    except:
        raise

#######

if __name__== "__main__":
    main()

