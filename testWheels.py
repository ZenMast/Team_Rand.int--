import MotorsThinkPad
from MotorsThinkPad import *
import CameraNew06
from CameraNew06 import *
import time
from time import sleep

motorLeft = MotorsThinkPad(1,MotorsThinkPad.ports[0])
motorRight = MotorsThinkPad(2,MotorsThinkPad.ports[1])
motorBack = MotorsThinkPad(3,MotorsThinkPad.ports[2])
Coilgun = MotorsThinkPad(4,MotorsThinkPad.ports[3])

print "start"

def testWheels(motorLeft,motorRight,motorBack):
    while(1):
        
        motorBack.motorMoveBd(0)
        motorRight.motorMoveFd(15)
        motorLeft.motorMoveBd(15)

def testAndur(motorRight):
    while(1):
        motorRight.andur()


def testCoilgun(Coilgun):
    while(1):
        Coilgun.coilgun()
        print "shot"
        sleep(1)

#testAndur(motorRight)    
##wholeCamera(motorLeft,motorRight,motorBack,Coilgun,"blue")
##wholeCamera(motorLeft,motorRight,motorBack,Coilgun,"yellow")
testWheels(motorLeft,motorRight,motorBack)
##Coilgun.coilgun()
##testCoilgun(Coilgun)

def robotMoveInDirAndRot(desDirect,speed,rotSpeed,motor1,motor2,motor3):
    speed1 = aContribRot(desDirect,speed,rotSpeed)
    speed2 = bContribRot(desDirect,speed,rotSpeed)
    speed3 = cContribRot(desDirect,speed,rotSpeed)
    motor1.motorMoveFd(speed1)
    motor2.motorMoveFd(speed2)
    motor3.motorMoveFd(speed3)
