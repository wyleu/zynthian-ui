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
import logging
from colour import Color

gpio_modes = {
    GPIO.BOARD: 'Pins on Board',
    GPIO.BCM: 'Pins on BCM'
}
gpio_pinmodes = {
    GPIO.IN: 'In',
    GPIO.OUT: 'Out',
    GPIO.SPI: 'SPI',
    GPIO.I2C: 'I2C',
    GPIO.HARD_PWM: 'PWM',
    GPIO.SERIAL: 'Serial',
    GPIO.UNKNOWN: 'Unknown'
}

FREQ = 50

GPIO.setmode(GPIO.BOARD)
print(gpio_modes[GPIO.getmode()])

logging.info('GPIO: 0x%X %s' % (GPIO.getmode(),gpio_modes[GPIO.getmode()]))
# logging.error('Board Version: 0x%X %s' % (GPIO.getmode(),gpio_modes[GPIO.getmode()]))

ENCODERS = {
	'LS': 'Load Snapshot',
	'SELECT': 'Select',
	'BACK': 'Back',
	'CHANNEL': 'Channel'
}

ENCODER_LEDS = {
	'LS': {'r': 12, 'g': 10, 'b':7},
	'SELECT': {'r': 21, 'g': 18, 'b':15},
	'BACK': {'r': 16, 'g': 19, 'b': 22},
	'CHANNEL': {'r': 8, 'g': 11, 'b': 13},
}
EL_PIN = 1 #if the items turn into a list or tuple . . .

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
		pass

	def begin(self, config=None):
		self.pins = []
		for encoder in ENCODERS:
			for pin in ENCODER_LEDS[encoder].items():
				GPIO.setup(pin[EL_PIN], GPIO.OUT)
				try:
					self.pins.append(GPIO.PWM(pin[EL_PIN], FREQ))
				except:
					logging.error('Failed to setup pin as PWM')
				self.pins[-1].start(0.5)

	def end(self):
		for pin in self.pins:
			pin.stop()
		GPIO.cleanup()

	def set_lib_ledshow(self, led, colours):
		self.value = ''

	def get_pins_status(self, pin=None):
		"""
		Display pi status
		pin: Pin to Display if None all
		"""
		if pin:
			pass

if __name__ =='__main__':
	ledshow = LedShow()
	ledshow.begin()
	ledshow.run_test()
	ledshow.end()