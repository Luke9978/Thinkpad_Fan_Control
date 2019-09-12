import time
import os
import re

# Yoked code from StackOverflow
dir_path = os.path.dirname(os.path.realpath(__file__))
f = []
for (dirpath, dirnames, filenames) in os.walk(dir_path):
    f.extend(filenames)
    break

# Filter out data files in the dir
r = re.compile("tempData*.csv")
# Capture inital starting time
InitTime = time.time_ns()

fanRPM_location = "/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon2/fan1_input"
pwmOutput_location = "/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon2/pwm1"


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
        msPassed = str(round((currentTime - InitTime) / 10e6, 1))
        line = msPassed + "," + currentReading
        composed.append(line)
    fanRPM = readHWMONFile(fanRPM_location)
    pwmOutput = readHWMONFile(pwmOutput_location)
    composed.append(fanRPM)
    composed.append(pwmOutput)
    return composed


def fileName():
    files = list(filter(r.match, f))
    return("tempData" + str(len(files)) + ".csv")


if __name__ == "__main__":
    sensors = []
    # Only two sensors have Data on my t460p
    for i in range(1, 3):
        sensors.append("/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon2/temp"
                       + str(i) + "_input")
    file = fileName()
    with open(file, "w") as dataFile:
        dataFile.write(
            "time, temp1_input, temp2_input, Fan Level, PWM level\n")
        while True:
            lines = composeData(sensors)
            temp1 = lines[0].split(',')
            temp2 = lines[1].split(',')
            dataFile.write(temp1[0] + ',' + temp1[1] + ',' + temp2[1] + ',')
            dataFile.write(lines[2] + ',' + lines[3] + '\n')
            print(lines)
            time.sleep(3)
