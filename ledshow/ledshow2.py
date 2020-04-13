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
PHYSICAL_TEST=True

logging.basicConfig(level=logging.DEBUG)
logging.critical('CRITICAL')
logging.error('ERROR')
logging.warning('WARNING')
logging.info('INFO')
logging.debug('DEBUG')


ENCODERS = {
	'LS': 'Load Snapshot',
	'SELECT': 'Select',
	'BACK': 'Back',
	'CHANNEL': 'Channel'
}

ENCODER_LEDS = {
	'LS': {'red': 12, 'green': 10, 'blue':7},
	'SELECT': {'red': 21, 'green': 18, 'blue':15},
	'BACK': {'red': 16, 'green': 19, 'blue': 22},
	'CHANNEL': {'red': 8, 'green': 11, 'blue': 13},
}
EL_COLOUR = 0
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
		GPIO.setmode(GPIO.BOARD)
		logging.info('GPIO: 0x%X %s' % (GPIO.getmode(), gpio_modes[GPIO.getmode()]))
		self.pins = []
		for encoder in ENCODERS:
			for pin in ENCODER_LEDS[encoder].items():
				GPIO.setup(pin[EL_PIN], GPIO.OUT)
				try:
					self.pins.append(GPIO.PWM(pin[EL_PIN], FREQ))
				except:
					logging.error('Failed to setup pin as PWM')

				self.pins[-1].start(100)  # start the new instance at one
				logging.info('{0} should be {1} on pin {2}'.format(encoder, *pin))
				time.sleep(4)
		self.dump()
		self.clear()

	def dump(self):
		logging.info('Dumping PWM')
		for pin in self.pins:
			logging.info(dir(pin))



	def clear(self):
		logging.info('Clearing down LEDs')
		for pin in self.pins:
			dc = 1
			pin.ChangeDutyCycle(dc)
			time.sleep(0.3)

	def end(self):
		logging.info('Running PWM End...')
		for pin in self.pins:
			pin.stop()
		GPIO.cleanup()

	def run_test(self):
		""" Do something demonstrative """
		logging.info('Running LEDs tests')
		try:
			while 1:
				for pin in self.pins:
					for dc in range(0, 101, 5):
						pin.ChangeDutyCycle(dc)
						time.sleep(0.1)
					for dc in range(100, -1, -5):
						pin.ChangeDutyCycle(dc)
						time.sleep(0.1)
		except KeyboardInterrupt:
			pass

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
	# ledshow.run_test()
	ledshow.end()