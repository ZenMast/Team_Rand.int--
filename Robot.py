import MotorsThinkPad
from MotorsThinkPad import *
import math
import time
from time import sleep

#move and rotate at the same time
def robotMoveInDirAndRot(desDirect,speed,rotSpeed,motor1,motor2,motor3):
    speed1 = aContribRot(desDirect,speed,rotSpeed)
    speed2 = bContribRot(desDirect,speed,rotSpeed)
    speed3 = cContribRot(desDirect,speed,rotSpeed)
    motor1.motorMoveFd(speed1)
    motor2.motorMoveFd(speed2)
    motor3.motorMoveFd(speed3)

#same shit as upper but with rotation parameter
def aContribRot(desDirect,speed,rotSpeed):
    angle = 150
    Fa = round(speed * (math.cos(math.radians(angle - desDirect))) + rotSpeed,2)
    return Fa

def bContribRot(desDirect,speed,rotSpeed):
    angle = 30
    Fb = round(speed * (math.cos(math.radians(angle - desDirect))) + rotSpeed,2)
    return Fb

def cContribRot(desDirect,speed,rotSpeed):
    angle = 270
    Fc = round(speed * (math.cos(math.radians(angle - desDirect))) + rotSpeed,2)
    return Fc

#turns on te spot with given speed
def robotTurnLeft(speed,motorLeft,motorRight,motorBack):
    motorLeft.motorMoveFd(speed)
    motorRight.motorMoveFd(speed)
    motorBack.motorMoveFd(speed)

def robotTurnRight(speed,motorLeft,motorRight,motorBack):
    motorLeft.motorMoveBd(speed)
    motorRight.motorMoveBd(speed)
    motorBack.motorMoveBd(speed)

def robotMoveAroundDribblerLeft(motorLeft,motorRight,motorBack,speed):
    motorLeft.motorMoveBd(round(speed / 3))
    motorRight.motorMoveBd(round(speed / 3))
    motorBack.motorMoveBd(round(speed))

def robotMoveAroundDribblerRight(motorLeft,motorRight,motorBack,speed):
    motorLeft.motorMoveFd(round(speed / 3))
    motorRight.motorMoveFd(round(speed / 3))
    motorBack.motorMoveFd(round(speed))

def robotMoveInCircleRight(speed1,speed2,speed3,motorLeft,motorRight,motorBack):
    motorLeft.motorMoveFd(speed1)
    motorRight.motorMoveFd(speed2)
    motorBack.motorMoveFd(speed3)
    
def robotMoveInCircleLeft(speed1,speed2,speed3,motorLeft,motorRight,motorBack):
    motorLeft.motorMoveFd(speed1)
    motorRight.motorMoveFd(speed2)
    motorBack.motorMoveBd(speed3)


    
##makes robot move in desired direction (desired direction givein in
##degrees, Fa, Fb and Fc are motor contributions. In other words
##it calculates how much effort on scale of 100% must motors use to move
##in desired direction (0 degrees means forward)
def robotMoveInDir(desDirect,speed,motor1,motor2,motor3):
    speed1 = aContrib(desDirect,speed)
    speed2 = bContrib(desDirect,speed)
    speed3 = cContrib(desDirect,speed)
    motor1.motorMoveFd(speed1)
    motor2.motorMoveFd(speed2)
    motor3.motorMoveFd(speed3)
    
def aContrib(desDirect,speed):
    angle = 150
    Fa = speed * round(math.cos(math.radians(angle - desDirect)),2)
    return Fa

def bContrib(desDirect,speed):
    angle = 30
    Fb = speed * round(math.cos(math.radians(angle - desDirect)),2)
    return Fb

def cContrib(desDirect,speed):
    angle = 270
    Fc = speed * round(math.cos(math.radians(angle - desDirect)),2)
    return Fc
