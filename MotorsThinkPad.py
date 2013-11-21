# -*- coding: utf-8 -*-
import time
import serial
from serial import *

class MotorsThinkPad:
    
    #those are needed for connection
    deviceName = 0
    motId = 0
    motorBck = 0
    motorLft = 0
    motorRght = 0
    coil = 0

    ports = [motorLft,motorRght,motorBck,coil] # device names

    #this stuff is initialized when motor object is created
    def __init__(self,devId,devName):
        self.deviceName = devName
        self.connectMotor(devId,self.deviceName)

    def disconnectMotor(self):
        self.deviceName.close()
        
    def connectMotor(self,devId,devName):
        for devNum in range(256): #it goes through all the ACMn, just in case
            motorId = 999
            try:
                self.deviceName = serial.Serial(port="/dev/ttyACM" + str(devNum), baudrate=115200, bytesize=EIGHTBITS,
                                        parity=PARITY_NONE, stopbits=STOPBITS_ONE, timeout=0.3,
                                        xonxoff=False, rtscts=False, writeTimeout=None, dsrdtr=False,
                                        interCharTimeout=None)

                isOpen = self.deviceName.isOpen()
                
                while(isOpen != True):
                    self.deviceName = serial.Serial(port="/dev/ttyACM" + str(devNum), baudrate=115200, bytesize=EIGHTBITS,
                                        parity=PARITY_NONE, stopbits=STOPBITS_ONE, timeout=0.3,
                                        xonxoff=False, rtscts=False, writeTimeout=None, dsrdtr=False,
                                        interCharTimeout=None)

                    isOpen = self.deviceName.isOpen()

                while(True):
                    try:
                        self.sendMotorCommand("?") #ask for motor id so we know left, right etc
                        id_string = self.deviceName.readline()
                        if id_string == '' or id_string == "?\n":
                            break
                        motorId = int(float(id_string.split(":")[1].split(">")[0]))
                    except:
                        continue
                    break
                
                if motorId == devId and devId == 4:
                    print "Coilgun connected"
                    break
                elif motorId == devId:#if succeeded, make it right, left or etc.
                    self.motId = motorId
                    print "Motor nr." + str(devId) + " connected."
                    break
                else:
                    pass
                
            except:
                pass

    #send random command, just implements motor "write" method
    def sendMotorCommand(self,command):
        self.deviceName.write(command + "\n")

    #apply on motor object to move, speed passed as argument
    def motorMoveFd(self,speed):
        self.sendMotorCommand("sd" + str(speed))

    def motorMoveBd(self,speed):
        self.sendMotorCommand("sd-" + str(speed))

    def andur(self):
        self.deviceName.write("gb\n")
        value=self.deviceName.readline()
        if "1" in value:
            self.deviceName.write("gb\n")
            value=self.deviceName.readline()
            if "1" in value:
                #print "Andur sees ball"
                return True
        else:
            #print "Andur doesnt see ball"
            return False

    def coilgun(self):
        self.deviceName.write("k10000\n")
