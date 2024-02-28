import time

from board import SCL, SDA
import busio

from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

defaultPositions = [90, 150, 20 ,90, 90, 150]

class ArmController:
    def __init__(self):
        self.initServos()
        self.isInit = True
        self.servoPos = defaultPositions.copy()
        if self.setPositions(defaultPositions):
            print("initilization completed\n")
            return
        self.servoPos = None
        self.isInit = False
        return None

    def getPositions(self):
        if self.isInit:
            return self.servoPos.copy()
        else:
            return None
    
    def getPosition(self, servoPos):
        if self.isInit:
            return self.servos[servoPos].angle
        else:
            return None
    
    def setPositions(self, servoPos : list):
        if not self.isInit:
            return
        if len(servoPos) != 6:
            return False
        for i in range(6):
            self.setPosition(i,servoPos[i])
        
        return True
    
    def setPosition(self, servoPos : int, angle : int):
        if not self.isInit:
            return

        for i in range(self.servoPos[servoPos], angle, 10):
            self.servos[servoPos].angle = i
            time.sleep(0.03)
        self.servos[servoPos].angle = angle
        self.servoPos[servoPos] = angle
    
    def initServos(self):
        i2c = busio.I2C(SCL, SDA)
        self.pca = PCA9685(i2c)
        self.pca.frequency = 50
        self.servos = []
        self.servos.append(servo.Servo(self.pca.channels[0], min_pulse=500, max_pulse=2600))
        self.servos.append(servo.Servo(self.pca.channels[1], min_pulse=500, max_pulse=2600))
        self.servos.append(servo.Servo(self.pca.channels[2], min_pulse=500, max_pulse=2600))
        self.servos.append(servo.Servo(self.pca.channels[3], min_pulse=500, max_pulse=2600))
        self.servos.append(servo.Servo(self.pca.channels[8], min_pulse=500, max_pulse=2600))
        self.servos.append(servo.Servo(self.pca.channels[9], min_pulse=500, max_pulse=2600))

    def initialize(self):
        self.initServos()
        self.isInit = True
        return self.setPositions(defaultPositions)

    def deinit(self):
        self.pca.deinit()
        self.isInit = False

