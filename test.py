import time
import os

time_count = 0

while True:
    milliseconds = str((float(time_count) / 1000)).split('.')[1].zfill(3)[:2]
    seconds = "%02d" % ((time_count / 1000) % 60)
    minutes = "%02d" % ((time_count / 1000) / 60)

    print(str(minutes) + ":" + str(seconds) + ":" + milliseconds)

    time_count += 1

    time.sleep(0.001)

