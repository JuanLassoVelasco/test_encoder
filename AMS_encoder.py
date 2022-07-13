from ast import literal_eval
from ntpath import join
from smbus import SMBus

ENCODER_MAX = 16383
ENCODER_MIN = 0

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
        frontDat = self.i2cBus.read_byte_data(self.i2cAddress, self.frontDatAddress)
        backDat = self.i2cBus.read_byte_data(self.i2cAddress, self.backDatAddress)
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
