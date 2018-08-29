#!/usr/bin/python3
"""
Franconian-Clock for RPi Zero W
with pigpio library
Switch off SPI, Serial and 1-Wire in paspi-config
"""
__author__      = "Jochen Krapf"
__email__       = "jk@nerd2nerd.org"
__copyright__   = "Copyright 2018, JK"
__license__     = "GPL3"
__version__     = "0.0.1"

import pigpio
import time
#from argparse import ArgumentParser

#######
# definitions and configuration

#REMOTE_RPI = 'raspberrypi.local'
REMOTE_RPI = 'RPiToGo.local'
GPIOS = {
    # minutes
    'M1': 21,
    'M2': 20,
    'M3': 16,
    'M4': 12,
    'M5': 7,
    'M6': 8,
    'M7': 25,
    # to/past
    'TO': 24,
    'PAST': 23,
    # quaters 'three' 'quater' 'half'
    'Q3': 14,
    'Q1': 15,
    'Q2': 18,
    # hours
    'H1': 29,
    'H2': 19,
    'H3': 13,
    'H4': 6,
    'H5': 5,
    'H6': 11,
    'H7': 9,
    'H8': 10,
    'H9': 22,
    'H10': 27,
    'H11': 17,
    'H12': 4,
}

NUMBERS = ['', 'eins', 'zwei', 'drei', 'vier', 'fünf', 'sechs', 'sieben', 'acht', 'neun', 'zehn', 'elf', 'zwölf']

LUM0 = 0
LUM1 = 16

LED_CURRENT = 8   # mA    values: 2, 4, 8, 16
# Note: maximum 5 LEDs are on at same time

#######
# init PIGPIO lib and deamon

try:
    PI = pigpio.pi(REMOTE_RPI)
except:
    PI = pigpio.pi()
if not PI.connected:
    raise Exception('No connection to PIGPIO deamon on RPi')

#######
# global variables

LUM_ACT = {}
LUM_PRED = {}
last_min = -1

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

# =====

def loop():
    global last_min
    t = ''

    # get act time
    tm = time.localtime()
    m = tm.tm_min
    h = tm.tm_hour

    if False:
        m = int(time.time())
        h = (m // 60) % 24
        m = m % 60

    # set LED PWM values
    if m != last_min:   # only on change
        last_min = m
        val = {}

        if m != 0:
            mm = m % 15
            if mm != 0:
                if mm > 7:
                    mm = 15 - mm
                    val['TO'] = 1
                    t += NUMBERS[mm] + ' vor '
                else:
                    val['PAST'] = 1
                    t += NUMBERS[mm] + ' nach '
                val['M'+str(mm)] = 1

            q = (m + 7) // 15
            if 1 <= q <= 3:
                val['Q'+str(q)] = 1
                if q == 2:
                    t += 'halb '
                if q == 3:
                    t += 'drei'
                if q == 1 or q == 3:
                    t += 'viertel '

        # hours
        if m > 7:
            h += 1
        h12 = h % 12
        if h12 == 0: h12 = 12
        val['H'+str(h12)] = 1
        t += NUMBERS[h12]

        print (h, m, '|', t, list(val.keys()))

        # set predicted lum values
        for key in LUM_PRED:
            if key in val:
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

