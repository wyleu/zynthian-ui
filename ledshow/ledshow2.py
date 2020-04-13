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

gpio_constants = {
	'BCM': 11,
	'BOARD': 10,
	'BOTH': 33,
	'FALLING': 32,
	'HARD_PWM': 43,
	'HIGH': 1,
	'I2C': 42,
	'IN': 1,
	'LOW': 0,
	'OUT': 0,
	'PUD_DOWN': 21,
	'PUD_OFF': 20,
	'PUD_UP': 22,
	# 'PWM':"""<class 'RPi.GPIO.PWM'>""",
	'RISING': 31,
	'RPI_INFO': {
		'P1_REVISION': 3,
		'REVISION': 'a02082',
		'TYPE': 'Pi 3 Model B',
		'MANUFACTURER': 'Sony',
		'PROCESSOR': 'BCM2837',
		'RAM': '1G'
		},
	'RPI_REVISION': 3,
	'SERIAL': 40,
	'SPI': 41,
	'UNKNOWN': -1,
	'VERSION': '0.7.0'
}


gpio_functions = (
	'add_event_callback',
	'add_event_detect',
	'cleanup',
	'event_detected',
	'getmode',
	'gpio_function',
	'input',
	'output',
	'remove_event_detect',
	'setmode',
	'setup',
	'setwarnings',
	'wait_for_edge',
)

FREQ = 50
PHYSICAL_TEST=True

# logging.basicConfig(level=logging.DEBUG)
# logging.critical('CRITICAL')
# logging.error('ERROR')
# logging.warning('WARNING')
# logging.info('INFO')
# logging.debug('DEBUG')


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


class Board(object):

	def dir_constants(self):
		return {item: getattr(GPIO,item)
				for item in dir(GPIO)
				if item[0:2] != '__'
				and item.isupper()
				and item != 'PWM'
				}

	def dir_functions(self):
		return [item
				for item in dir(GPIO)
				if item[0:2] != '__'
				and item.islower()
				]


	def setmode(self, mode):
		GPIO.setmode(mode)


	def getmodes(self):
		return gpio_modes.keys()

	def getmode(self):
		return GPIO.getmode()

	def cleanup(self):
		return GPIO.cleanup()

	def setwarnings(self, warning):
		GPIO.setwarnings(warning)





class LED(object):
	def __init__(self, pin, colour):
		self.pin = pin
		self.colour = colour


class Encoder(object):
	def __init__(self, name):
		self.leds = None

	def add_led(self, led):
		try:
			self.leds.append(led)
		except AttributeError:
			self.leds = [led,]


class Display(object):
	def __init__(self, name):
		self.encoders = None
	def add_encoder(self, encoder):
		try:
			self.encoders.append(encoder)
		except AttributeError:
			self.encoders = [encoder,]





class LedShow(object):
	def __init__(self):
		self.encoders = ENCODERS

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
				time.sleep(0.3)
		self.step_set(0)
		self.step_set(100)
		self.step_set(0)

	def step_set(self, value):
		logging.info('Clearing down LEDs')
		for pin in self.pins:
			dc = 100
			pin.ChangeDutyCycle(value)
			time.sleep(1)


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