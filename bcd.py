#!/usr/bin/python3
"""
BCD-Clock for RPi Zero W
with pigpio library
"""
__author__      = "Jochen Krapf"
__email__       = "jk@nerd2nerd.org"
__copyright__   = "Copyright 2018, JK"
__license__     = "GPL3"
__version__     = "0.0.1"

import pigpio
import time
from argparse import ArgumentParser

#######
# definitions and configuration

REMOTE_RPI = 'raspberrypi.local'
GPIOS = {
    # seconds
    'S1.1': 24,
    'S1.2': 25,
    'S1.4': 8,
    'S1.8': 7,
    'S10.1': 12,
    'S10.2': 16,
    'S10.4': 20,
    # minutes
    'M1.1': 9,
    'M1.2': 11,
    'M1.4': 5,
    'M1.8': 6,
    'M10.1': 13,
    'M10.2': 19,
    'M10.4': 26,
    # hours
    'H1.1': 17,
    'H1.2': 27,
    'H1.4': 22,
    'H1.8': 10,
    #'H10.1': 18,
    #'H10.2': 23,
    # colon
    #'C': 23,
    # am/pm
    #'PM': 18,
}
GPIO_BUTTON = 21

LUM0 = 1
LUM1 = 5

LED_CURRENT = 2   # mA    values: 2, 4, 8, 16

#######
# init PIGPIO lib and deamon

try:
    PI = pigpio.pi()
except:
    PI = pigpio.pi(REMOTE_RPI)
    if not PI.connected:
        raise Exception('No connection to PIGPIO deamon on RPi')

#######
# global variables

LUM_ACT = {}
LUM_PRED = {}
last_sec = -1
last_button = -1

#######

def set_led_lum(key, act):
    PI.set_PWM_dutycycle(GPIOS[key], act*act)   # set PWM with gamma correction
    LUM_ACT[key] = act

# =====

def init():
    PI.set_pad_strength(0, LED_CURRENT)   # limit LED current to n mA

    for key, pin in GPIOS.items():
        PI.set_mode(pin, pigpio.OUTPUT)
        PI.set_PWM_frequency(pin, 200)   # 200 Hz
        PI.set_PWM_range(pin, LUM1*LUM1)   # 0...10²
        set_led_lum(key, 0)
        #LUM_ACT[key] = 0
        LUM_PRED[key] = 0

    PI.set_mode(GPIO_BUTTON, pigpio.INPUT)
    PI.set_pull_up_down(GPIO_BUTTON, pigpio.PUD_UP)
    #PI.set_glitch_filter(PIN_BUTTON, 10000)
    #PI.set_noise_filter(PIN_BUTTON, 10000, 100000)

# =====

def loop():
    global last_sec, last_button

    # get act time
    tm = time.localtime()
    s = tm.tm_sec
    m = tm.tm_min
    h = tm.tm_hour

    # check button
    button = PI.read(GPIO_BUTTON)
    if not button:
        #TODO
        pass

    # set LED PWM values
    if s != last_sec:   # only on change
        last_sec = s
        val = {}

        #DEBUG print (h, m, s)

        # seconds with 3+4 LEDs
        s1 = s % 10
        val['S1.1'] = s1 & 1
        val['S1.2'] = s1 & 2
        val['S1.4'] = s1 & 4
        val['S1.8'] = s1 & 8
        s10 = s // 10
        val['S10.1'] = s10 & 1
        val['S10.2'] = s10 & 2
        val['S10.4'] = s10 & 4

        # minutes with 3+4 LEDs
        m1 = m % 10
        val['M1.1'] = m1 & 1
        val['M1.2'] = m1 & 2
        val['M1.4'] = m1 & 4
        val['M1.8'] = m1 & 8
        m10 = tm.tm_min // 10
        val['M10.1'] = m10 & 1
        val['M10.2'] = m10 & 2
        val['M10.4'] = m10 & 4

        # hours
        if 'H10.1' in GPIOS:   # 24h format with 2+4 LEDs
            h1 = h % 10
        else:   # 12h format with 4 LEDs
            h1 = h % 12
            if h1 == 0: h1 = 12
        val['H1.1'] = h1 & 1
        val['H1.2'] = h1 & 2
        val['H1.4'] = h1 & 4
        val['H1.8'] = h1 & 8
        if 'H10.1' in GPIOS:
            h10 = h // 10
            val['H10.1'] = h10 & 1
            val['H10.2'] = h10 & 2

        if 'PM' in GPIOS:
            val['PM'] = h >= 12

        if 'C' in GPIOS:
            val['C'] = 1 - (s & 1)

        # set predicted lum values
        for key, is_on in val.items():
            if is_on:
                LUM_PRED[key] = LUM1
            else:
                LUM_PRED[key] = LUM0

    # follow LED PWM to predicted lum values
    for key, pred in LUM_PRED.items():
        act = LUM_ACT[key]
        if pred != act:
            # follow linear
            if pred > act:
                act += 1
            else:
                act -= 1
            set_led_lum(key, act)

# =====

def main():
    init()

    try:
        while True:
            loop()
            time.sleep(0.05)   # update with 20 Hz

    except (KeyboardInterrupt, SystemExit):
        pass

    except:
        raise

#######

if __name__== "__main__":
    main()

