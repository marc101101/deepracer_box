#!/usr/bin/python
# Copyright dhq (August 23 2016)
# License GPLV3

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import requests

import time
import os
import sys
import tft_py as GLCD
from random import randrange

import urllib2
import json
import cStringIO
import RPi.GPIO as GPIO

status=1
counter_time = 0
textid = 0
team = "-- no team --"

font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf', 16) #use a truetype font
font2 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf', 36) #use a truetype font



def getCurrentTeam():
	resp = requests.get('https://swapi.co/api/people/' + str(randrange(10)))
	if resp.status_code != 200:
		# This means something went wrong.
		# Maybe retry mechanism?
	#	raise ApiError('GET /tasks/ {}'.format(resp.status_code))
		return "connection error"
	else:
		return resp.json()["name"]


def setCurrentTeamTime(time, team):
	payload = {
				"team": team,
				"time": time
			}

	#resp = requests.post('https://todolist.example.com/tasks/', json=payload)


def buttonhandler(channel):
	global status, team

	start_time = time.time()

	while GPIO.input(channel) == 0:  # Wait for the button up
		pass

	buttonTime = time.time() - start_time
	print("BUTTONTIME: " + str(buttonTime))

	if .1 <= buttonTime < 2:  # Ignore noise
		print("BRIEF")
		if status == 1:
			status = 2
		else:
			if status == 2:
				status = 3
			else:
				if status == 3:
					status = 1

	elif buttonTime >= 4:
		print("REALLY LONG")
		team = "-- no team --"
		team = getCurrentTeam()
		status = 1


def get_current_time(count):
	milliseconds = str((float(count) / 1000)).split('.')[1].zfill(3)
	seconds = "%02d" % ((count / 1000) % 60)
	minutes = "%02d" % ((count / 1000) / 60)
	return str(minutes) + ":" + str(seconds) + ":" + milliseconds


def draw_method(disp, draw, team, counter_time):
	disp.clear(color=(0,0,0))						
	draw.text((10,20), team, font=font)
	draw.text((10,50), get_current_time(counter_time), font=font2)
	draw.text((10, 100), "mode: " + str(status), font=font)
	disp.display()


def main(argv):
	global status, counter_time, textid, team

	print("========= deepracker-box v0.0.0.0.0.0.0.1 ==========")
	print("******************************************")

	# status - modues:
	# 1 = receive current_team and set counter_time = 0  => set status 2
	# 2 = start counter_time => set status 3
	# 3 = stop counter_time and send team update to server => set status 1

	########################
	##### INIT DISPLAY  ####
	########################

	height = GLCD.TFT_HEIGHT
	width = GLCD.TFT_WIDTH

	disp = GLCD.TFT()		# Create TFT LCD display class.
	disp.initialize()		# Initialize display.
	disp.clear()			# Alternatively can clear to a black screen by calling:
	draw = disp.draw()		# Get a PIL Draw object to start drawing on the display buffer
	
	disp.setRotation(4)	
	
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(10, GPIO.FALLING, callback=buttonhandler)


	########################
	##### STATE MACHINE ####
	########################

	team = getCurrentTeam()

	while True:
		if status == 1:
			counter_time = 0
			draw_method(disp, draw, team, counter_time)

		if status == 2:
			counter_time += 1
			draw_method(disp, draw, team, counter_time)
			time.sleep(0.001)

		if status == 3:
			draw_method(disp, draw, team, counter_time)


if __name__ == '__main__':
	try:
		main(sys.argv[1:])
	except KeyboardInterrupt:
		print("")
