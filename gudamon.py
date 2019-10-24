#!/usr/bin/python
# Copyright dhq (August 23 2016)
# License GPLV3

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import os
import sys
import tft_py as GLCD
from random import randint

import urllib2
import json
import cStringIO
import RPi.GPIO as GPIO

gudauptime=0
fail = 0
textid = 0

font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf', 26)	# use a truetype font
font2 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf', 16)#use a truetype font


textdata = [
	["du...", "PFEIFFE", font], 
	["u went full DevOps?", "never go full DevOps!", font2],
	["Ein Admin schlaeft", "nicht, er root!", font2],
	["sudo rm -f /", "Don't drink and root!", font2],
	["... und zu Weihnachten","ist er Knecht Rootrecht!",font2],
	["Und der Mann heisst","ROLAND!",font2],
	["EIGENTLICH","gehts!",font2],
	["Nicht dein", "Ernst?!", font],
	["Armageddon", "111elf!!!!", font],
	["Someone told you","to do it not?!",font2],
	["HAHA","",font],
	["Der Guder","wieder...",font2],
	["Die Baumann","heitert dich auf!",font2],
	["Hackaburg","2045",font2],
	["Guda, geh die","Kaffemaschine putzen",font2],
	["Suicide Squad-- ","",font2]
	]

def buttonhandler(channel):
	global fail, gudauptime
	fail=1
 
def main(argv):
	global fail, gudauptime, textid
	print("========= gudamon v0.0.0.0.0.0.0.1 ==========")
	print("******************************************")

	height = GLCD.TFT_HEIGHT
	width = GLCD.TFT_WIDTH

	disp = GLCD.TFT()		# Create TFT LCD display class.
	disp.initialize()		# Initialize display.
	disp.clear()			# Alternatively can clear to a black screen by calling:
	draw = disp.draw()		# Get a PIL Draw object to start drawing on the display buffer
	
	disp.setRotation(4)
	
	
	#GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(10, GPIO.FALLING, callback=buttonhandler)
	
	while True:
		if fail == 0:
			disp.clear(color=(0,0,0))
			gudauptime = gudauptime + 1
			draw.text((5, 20), 'GuDaUptime', font=font, fill=(255,255,255,255))
			draw.text((5, 50), str(gudauptime), font=font, fill=(255,255,255,255))
			draw.text((5, 80), 'seconds', font=font, fill=(255,255,255,255))
			disp.display()
			time.sleep(0.001)
		else:
			fail = 0
			disp.clear(color=(0,0,0))
			gudauptime = 0
			textid = randint(0,len(textdata)-1)
			#if textid%2 :
			#	draw.text((5, 20), 'du...', font=font, fill=(255,255,255,255))
			#draw.text((5, 50), 'PFEIFFE', font=font, fill=(255,255,255,255))
			#else:
			#	draw.text((5, 20), 'u went full DevOps?', font=font2, fill=(255,255,255,255))
			#	draw.text((5, 50), 'never go full DevOps!', font=font2, fill=(255,255,255,255))
			draw.text((5,20), textdata[textid][0], font=textdata[textid][2])
			draw.text((5,50), textdata[textid][1], font=textdata[textid][2])
			disp.display()
			time.sleep(5)			
		

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("")

