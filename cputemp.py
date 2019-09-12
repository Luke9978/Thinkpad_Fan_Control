import time
import os
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
f = []
for (dirpath, dirnames, filenames) in os.walk(dir_path):
    f.extend(filenames)
    break
r = re.compile("tempData*.csv")

# temp[1-8]_input
InitTime = time.time_ns()
fanFeedback = "/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon2/fan1_input"
pwmInput = "/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon2/pwm1"


def readHWMONFile(name):
    with open(name, "r") as file:
        myInt = file.read()
        myInt = myInt.strip()
        return str(myInt)


def composeData(sensors):
    composed = []
    for sensor in sensors:
        currentTime = time.time_ns()
        currentReading = readHWMONFile(sensor)
        msPassed = str(round((currentTime - InitTime)/10e6, 1))
        line = msPassed + "," + currentReading
        composed.append(line)
    fanSpeed = readHWMONFile(fanFeedback)
    pwmLevel = readHWMONFile(pwmInput)
    composed.append(fanSpeed)
    composed.append(pwmLevel)
    return composed


def fileName():
    files = list(filter(r.match, f))
    return("tempData" + str(len(files)) + ".csv")


if __name__ == "__main__":
    sensors = []
    for i in range(1, 3):
        sensors.append("/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon2/temp" \
                      + str(i) + "_input")
    file = fileName()
    with open(file, "w") as dataFile:
        dataFile.write("time, temp1_input, temp2_input, Fan Level, PWM level\n")
        while True:
            lines = composeData(sensors)
            temp1 = lines[0].split(',')
            temp2 = lines[1].split(',')
            dataFile.write(temp1[0]+','+temp1[1]+','+temp2[1]+',')
            dataFile.write(lines[2]+','+lines[3]+'\n')
            print(lines)
            time.sleep(3)
