import serial
import time
from drawnow import *
import csv

with open('dispCSV.txt', mode='w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['displacementX', 'displacement Y', 'displacement Z'])

arduinoDataPacket = serial.Serial('com5', 115200)
plt.ion()
count = 0

accX = []
accY = []
accZ = []

uX = 0
uY = 0
uZ = 0

finalSX = 0
finalSY = 0
finalSZ = 0

t = 0.01
velCountX = 0
velCountY = 0
X = []
velocity = []
time.sleep(1)


# plt.ion()
def findVelocityX(u):
    u = u + t * (accX[-1] + accX[-2]) / 2
    return u


def findVelocityY(u):
    u = u + t * (accY[-1] + accY[-2]) / 2
    return u


def findVelocityZ(u):
    u = u + t * (accZ[-1] + accZ[-2]) / 2
    return u


def findDisplacementX(u):
    s = u * t + 0.5 * ((accX[-1] + accX[-2]) / 2) * t * t
    return s


def findDisplacementZ(u):
    s = u * t + 0.5 * ((accZ[-1] + accZ[-2]) / 2) * t * t
    return s


def findDisplacementY(u):
    s = u * t + 0.5 * ((accY[-1] + accY[-2]) / 2) * t * t
    return s


def draw():
    plt.xlim(-7, 7)
    plt.ylim(-5, 5)
    plt.plot(X, 0)


while 1 == 1:
    if arduinoDataPacket.inWaiting() > 0:
        rawDataPacket = arduinoDataPacket.readline().decode('ascii')
        strDataPacket = rawDataPacket.replace("\r\n", "")
        lst = strDataPacket.split(',')

        try:

            ax = float(lst[0])
            ay = float(lst[1])
            az = float(lst[2])

            #if az < 0:
             #   az = az * 0.8
            if -0.01 < az < 0.01:
              az = 0

            accX.append(ax)
            accY.append(ay)
            accZ.append(az)

            count = count + 1

            if count > 10:
                accX.pop(0)
                accY.pop(0)
                accZ.pop(0)

            if count > 1:
                tempX = uX
                tempY = uY
                tempZ = uZ
                uX = findVelocityX(uX)
                uY = findVelocityY(uY)
                uZ = findVelocityZ(uZ)

            if round(uX, 2) == round(tempX, 2):
                velCountX = velCountX + 1
            else:
                velCountX = 0

            if round(uY, 2) == round(tempY, 2):
                velCountY = velCountY + 1
            else:
                velCountY = 0

            if round(uZ, 2) == round(tempZ, 2):
                velCountZ = velCountZ + 1
            else:
                velCountZ = 0

            if velCountX > 5:
                uX = 0
                velCountX = 0

            if velCountY > 5:
                uY = 0
                velCountY = 0

            if velCountZ > 5:
                uZ = 0
                velCountZ = 0

            finalSX = finalSX + findDisplacementX(uX)
            finalSY = finalSY + findDisplacementY(uY)
            finalSZ = finalSZ + findDisplacementZ(uZ)

            with open('dispCSV.txt', mode='a', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow([str(round(finalSX, 2)), str(round(finalSY, 2)), str(round(finalSZ, 2))])

            print(round(finalSX, 2), end="")
            print(",", end="")
            print(round(finalSY, 2), end="")
            print(",", end="")
            print(round(finalSZ, 2))


        # drawnow(draw)
        except Exception as e:
            print(strDataPacket)

            pass
