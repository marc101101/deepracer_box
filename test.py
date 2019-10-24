import time
import os

time_count = 0

def time_formater(count):
    miliseconds = str((float(count) / 1000)).split('.')[1].zfill(3) 
    seconds = "%02d" % ((count /1000) % 60)
    minutes = "%02d" %  ((count /1000) / 60)

    print(str(minutes) + ":" + str(seconds) + ":" + miliseconds)

while True:
    time_formater(time_count)

    time_count += 1

    time.sleep(0.001)

