#!/usr/bin/python3
"""
Neo-Pixel-Clock for RPi Zero W
With library from https://github.com/jgarff/rpi_ws281x
For usage see https://learn.adafruit.com/neopixels-on-raspberry-pi?view=all
"""
__author__      = "Jochen Krapf"
__email__       = "jk@nerd2nerd.org"
__copyright__   = "Copyright 2018, JK"
__license__     = "GPL3"
__version__     = "0.0.1"

import pigpio
import time
import math
from argparse import ArgumentParser
try:
    from neopixel import *
    NEOPIXEL = True
except:
    NEOPIXEL = False

#######
# definitions and configuration

LED_MER = 30

LED_LUM_MAX = 255
LED_LUM_SCALE = 1.0

# LED strip configuration:
LED_COUNT       = 60+49      # Number of LED pixels.
LED_PIN         = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ     = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA         = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS  = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT      = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL     = 0
#LED_STRIP       = ws.WS2812_STRIP
#LED_STRIP       = ws.SK6812_STRIP
LED_STRIP       = ws.SK6812W_STRIP

#REMOTE_RPI = 'raspberrypi.local'
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
V = []

strip = None
args = None

#######

def hand_function(x, hand_width_n, hand_width_p):
    if not -hand_width_n < x < hand_width_p:
        return 0.0
    if x > 0:
        y = 1 - x / hand_width_p
    else:
        y = 1 + x / hand_width_n
    return y

# -----

def clear_leds():
    global args, V

    for i in range(args.leds):
        V[i] = [0, 0, 0]

# -----

def add_led_color(idx, value, rgb):
    global args, V

    if value <= 0:
        return

    idx += args.meridiem
    while idx >= args.leds:
        idx -= args.leds

    r, g, b = rgb
    V[idx][0] += r * value
    V[idx][1] += g * value
    V[idx][2] += b * value

# -----

def set_hand(idx, hand_pos, hand_width_n, hand_width_p, rgb):
    global args

    for mirror in range(-args.leds, 2*args.leds, args.leds):
        x = (idx + mirror - hand_pos * args.leds)
        value = hand_function(x, hand_width_n, hand_width_p)
        add_led_color(idx, value, rgb)

# =====

def init():
    global strip, args, V

    V = [0]*args.leds
    for i in range(args.leds):
        V[i] = [0, 0, 0]


    #PI.set_mode(GPIO_BUTTON, pigpio.INPUT)
    #PI.set_pull_up_down(GPIO_BUTTON, pigpio.PUD_UP)

    if NEOPIXEL:
        # Create NeoPixel object with appropriate configuration.
        strip = Adafruit_NeoPixel(args.leds, args.pin, LED_FREQ_HZ, LED_DMA, args.invert, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
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
    t -= time.altzone   # time zone + dst

    # norm s, m, h to 0...1
    s = t / 60
    m = s / 60
    h = m / 12
    s = s - int(s)
    m = m - int(m)
    h = h - int(h)

    if False:
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
    else:
        p = t * 2
        p = math.sin(p)
    # scale to circle
    p *= 0.1   # size = +/-10%
    p += 0.5   # position = 50% = bottom


    #print (h, m, s)

    for i in range(args.leds):
        set_hand(i, s, 1.5, 0.5, (0, 0, 0.8))
        set_hand(i, m, 3.0, 0.5, (0, 0.8, 0))
        set_hand(i, h, 4.5, 0.5, (0.8, 0, 0))
        if args.pentulum:
            set_hand(i, p, 3.0, 3.0, (0.4, 0.4, 0))

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
            rgb = V[i]
            w = min(rgb)
            for c in range(3):
                rgb[c] -= w
            rgb.append(w)

            for c in range(4):
                v = rgb[c]
                v *= LED_LUM_SCALE
                v *= v   # gamma correction
                v = int(v * LED_LUM_MAX + 0.5)
                if v > LED_LUM_MAX: v = LED_LUM_MAX
                rgb[c] = v
            strip.setPixelColorRGB(i, rgb[0], rgb[1], rgb[2], rgb[3])
        strip.show()

    return

    # check button
    #button = PI.read(GPIO_BUTTON)
    #if not button:
    #    #TODO
    #    pass

# =====

def main():
    global args

    parser = ArgumentParser(prog='piClock', conflict_handler='resolve')

    parser.add_argument("-l", "--leds", 
        dest="leds", default=LED_COUNT, metavar='LEDS', type=int,
        help="Number of LEDs")

    parser.add_argument("-m", "--meridiem", 
        dest="meridiem", default=LED_MER, metavar='LED', type=int,
        help="Index of meridiem LED")

    parser.add_argument("-p", "--pin", 
        dest="pin", default=LED_PIN, metavar='GPIO', type=int,
        help="GPIO Number")

    parser.add_argument("-i", "--invert",
        dest="invert", default=LED_INVERT, action="store_true", 
        help="Invert GPIO pin")

    parser.add_argument("-u", "--nopentulum",
        dest="pentulum", default=True, action="store_false", 
        help="No Pentulum")
    parser.add_argument("-U", "--pentulum",
        dest="pentulum", default=True, action="store_true", 
        help="Use Pentulum")

    '''
    parser.add_argument("-a", "--loglevel", 
                        dest="logLevel", default=0, type=int, metavar="LEVEL",
                        help="Set the maximum logging level - 0=no output, 1=error, 2=warning, 3=info, 4=debug, 5=ext.debug")

    parser.add_argument("-L", "--logfile", 
                        dest="logFile", default='Test', metavar="FILE",
                        help="Set FILE name for logging output")

    parser.add_argument("-q", "--quiet",
                        dest="verbose", default=True, action="store_false", 
                        help="don't print status messages to stdout")
    '''
    args = parser.parse_args()

    init()

    try:
        while True:
            loop()
            time.sleep(0.001)   # update with max ??? Hz

    except (KeyboardInterrupt, SystemExit):
        pass

    except:
        raise

#######

if __name__== "__main__":
    main()

