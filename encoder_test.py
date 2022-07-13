from ast import literal_eval
from ntpath import join
from smbus import SMBus
import time
from matplotlib import pyplot as plt
import numpy as np
import time
import AMS_encoder


encodeAngle1 = 0
encodeAngle2 = 0
jointAngles1 = []
jointAngles2 = []
xList = []

# pi i2c address for encoder
enc1i2cAddress = 0x43
enc2i2cAddress = 0x40
# encoder magnitude i2c address
encDatAddress = 0xFE

#Angle data addresses
angDatFrontAddress = 0xFF
angDatBackAddress = 0xFE

#Sample time Graph variables
startTime = 0
prevTime = 0
curTime = 0
dt = 1
sampRateY = []

angleSampleRate = 0.002

i2cBus = SMBus(1)
encoder1 = AMS_encoder.EncoderAMS(i2cBus, enc1i2cAddress, angDatFrontAddress, angDatBackAddress)
encoder2 = AMS_encoder.EncoderAMS(i2cBus, enc2i2cAddress, angDatFrontAddress, angDatBackAddress)

if __name__ == '__main__':
    x = 0
    try:
        startTime = time.time()
        prevTime = startTime
        prevSample = x
        curTime = startTime
        while True:
            # curTime = time.clock_gettime_ns(time.CLOCK_REALTIME)
            curTime = time.time()
            curSample = x
            if (curTime - prevTime) >= dt:
                sampRateY.append(x - prevSample)
                prevSample = x
                prevTime = curTime

            xList.append(x)

            encodeAngle1 = encoder1.getAngle()
            encodeAngle2 = encoder2.getAngle()

            jointAngles1.append(encodeAngle1)
            jointAngles2.append(encodeAngle2)

            print("%.2f, %.2f, %.2f" % (curTime, encodeAngle1, encodeAngle2))
            x += 1
            if (time.time() - curTime) < angleSampleRate:
                try:
                    time.sleep(angleSampleRate - (time.time() - curTime))
                except:
                    continue

    except KeyboardInterrupt:
        if len(jointAngles1) < len(xList):
            jointAngles1.append(encodeAngle1)

        if len(jointAngles2) < len(xList):
            jointAngles2.append(encodeAngle2)

        endTime = time.time()

        sampleRate = x/(endTime - startTime)
        
        plt.plot(xList, jointAngles1)
        plt.plot(xList, jointAngles2)
        plt.show()

        sampRateX = range(0, len(sampRateY))

        plt.figure
        plt.clf

        plt.plot(sampRateX, sampRateY)
        plt.show()

        print("Sampling Rate for this run: " + str(sampleRate) + " samples per second")


