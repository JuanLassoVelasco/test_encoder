from ast import literal_eval
from ntpath import join
from smbus import SMBus
import time
from matplotlib import pyplot as plt
import numpy as np
import time

ENCODER_MAX = 16383
ENCODER_MIN = 0

jointAngles = []
xList = []

# pi i2c address for encoder
i2cAddress = 0x43
# encoder magnitude i2c address
encDatAddress = 0xFE

#Angle data addresses
angDatFrontAddress = 0xFF
angDatBackAddress = 0xFE

class EncoderAMS:
    def __init__(self, i2cBus, i2cAddress, FDatAddress, BDatAddress):
        self.i2cBus = i2cBus
        self.i2cAddress = i2cAddress
        self.frontDatAddress = FDatAddress
        self.backDatAddress = BDatAddress

    def encI2CtoAngle(self, encRaw):
        angle = ((encRaw*360)/ENCODER_MAX)
        return angle

    def getAngle(self):
        frontDat = self.i2cBus.read_byte_data(i2cAddress, angDatFrontAddress)
        backDat = self.i2cBus.read_byte_data(i2cAddress, angDatBackAddress)
        frontDatStrTemp = str(bin(frontDat))
        frontDatStr = frontDatStrTemp[2:len(frontDatStrTemp)]
        backDatStrTemp = str(bin(backDat))
        backDatStr = backDatStrTemp[2:len(backDatStrTemp)]
        frontLen = len(frontDatStr)
        backLen = len(backDatStr)
        if frontLen < 6:
            for i in range(0,6-frontLen):
                frontDatStr = '0' + frontDatStr

        if backLen < 8:
            for i in range(0,8-backLen):
                backDatStr = '0' + backDatStr

        fullDat = float(literal_eval(bin(int("0b" + backDatStr + frontDatStr, 2))))

        jointAngle = self.encI2CtoAngle(fullDat)

        return jointAngle



i2cBus = SMBus(1)
encoder = EncoderAMS(i2cBus, i2cAddress, angDatFrontAddress, angDatBackAddress)

if __name__ == '__main__':
    x = 0
    try:
        startTime = time.time()
        while True:
            xList.append(x)

            encodeAngle = encoder.getAngle()

            jointAngles.append(encodeAngle)
            # curTime = time.clock_gettime_ns(time.CLOCK_REALTIME)
            curTime = time.time()
            print(str(encodeAngle) + " " + str(x))
            x += 1
    except KeyboardInterrupt:
        if len(jointAngles) < len(xList):
            jointAngles.append(encodeAngle)

        endTime = time.time()

        sampleRate = x/(endTime - startTime)
        
        plt.plot(xList, jointAngles)
        plt.show()
        print("Sampling Rate for this run: " + str(sampleRate) + " samples per second")


