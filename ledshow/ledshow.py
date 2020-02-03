#!/usr/bin/python3
# -*- coding: utf-8 -*-
#********************************************************************
# ZYNTHIAN PROJECT: LedShow Python Wrapper
#
# A Python wrapper for ldshow library
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

from ctypes import *
from os.path import dirname, realpath


lib_ledshow = None

def lib_ledshow_init():
	global lib_ledshow
	try:
		lib_ledshow=cdll.LoadLibrary(dirname(realpath(__file__))+"/build/libledshow.so")
		lib_ledshow.initLedshow()
		lib_ledshow.getPeak.restype = c_float
		lib_ledshow.getPeakRaw.restype = c_float
		lib_ledshow.getHold.restype = c_float


	except Exception as e:
		lib_ledshow=None
		print("Can't init ledshow library: %s" % str(e))
	return lib_ledshow

def get_lib_ledshow():
	return lib_ledshow