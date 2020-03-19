#!/usr/bin/python3
# -*- coding: utf-8 -*-
#********************************************************************
# ZYNTHIAN PROJECT: LedShow Python Wrapper
#
# A Python wrapper for ledshow library
#
# Copyright (C) 2020 Chris Lyon <wyleus@gmail.com>
#
#********************************************************************
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# For a full copy of the GNU General Public License see the LICENSE.txt file.
#
#********************************************************************
import time
import RPi.GPIO as GPIO
from colour import Color

gpio_modes = {
    GPIO.BOARD: 'Pins on Board',
    GPIO.BCM: 'Pins on BCM'
}

GPIO.setmode(GPIO.BOARD)
print(gpio_modes[GPIO.getmode()])

gpio_pinmodes = {
    GPIO.IN: 'In',
    GPIO.OUT: 'Out',
    GPIO.SPI: 'SPI',
    GPIO.I2C: 'I2C',
    GPIO.HARD_PWM: 'PWM',
    GPIO.SERIAL: 'Serial',
    GPIO.UNKNOWN: 'Unknown'
}


R_PIN = 33
G_PIN = 36
B_PIN = 32

FREQ = 50



lib_ledshow = None

def lib_ledshow_init():
	global lib_ledshow
	try:
		lib_ledshow = LedShow()
	except Exception as e:
		lib_ledshow=None
		print("Can't init ledshow library: %s" % str(e))
	return lib_ledshow


class LedShow(object):
	def __init__(self):
		self.b = GPIO.PWM(B_PIN, FREQ)  # channel=32 frequency=50Hz
		self.r = GPIO.PWM(R_PIN, FREQ)
		self.g = GPIO.PWM(B_PIN, FREQ)

		self.b.start(0)
		self.r.start(0)
		self.g.start(0)

	def cleanup_lib_ledshow(self):
		self.b.stop()
		self.r.stop()
		self.g.stop()
		GPIO.cleanup()

	def set_lib_ledshow(self, led, colours):
		self.value = ''

