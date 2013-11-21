# -*- coding: utf-8 -*-
##Code for ball-tracking
##It should be easy to use. Though, launch robot from "testMotors" file!!!

import cv2
import numpy as np
import Robot
import MotorsThinkPad
from MotorsThinkPad import *
from Robot import *
from readmeh import *
import time
from time import sleep

def wholeCamera(motorLeft,motorRight,motorBack,Coilgun,color):
    #Initial values for different stuff
    maxSpeed = 65
    randomSpeed = 55
    maxY = 480
    LINE_SIZE = 7
    dribbler_point = (320.0, 470.0)
    ball_min_size = 5
    gate_min_size = 15
    borderline_min_size = 15
    BORDERLINE_MIN = np.array(minborder, "uint8")
    BORDERLINE_MAX = np.array(maxborder, "uint8")
    ORANGE_MIN = np.array(minball, "uint8")
    ORANGE_MAX = np.array(maxball, "uint8")
    BLUE_MIN = np.array(minb, "uint8")
    BLUE_MAX = np.array(maxb, "uint8")
    YELLOW_MIN = np.array(miny, "uint8")
    YELLOW_MAX = np.array(maxy, "uint8")
    borderEro = int(sedborder[2])
    borderDil = int(sedborder[3])
    ballEro = int(sedball[2])
    ballDil = int(sedball[3])
    yellowEro = int(sedy[2])
    yellowDil = int(sedy[3])
    blueEro = int(sedb[2])
    blueDil = int(sedb[3])
    yellow = 0
    blue = 0
    if color == "yellow":
        yellow = True
        blue = False
    elif color == "blue":
        yellow = False
        blue = True
    else:
        print "wrong gate color"

    #Capture webcam
    cap = cv2.VideoCapture(2)
    w = cap.get(3)
    h = cap.get(4)
    print "Width: " + str(w) + " Height: " + str(h)
    Coilgun.sendMotorCommand("c")
    #Basically main algorithm of what's going on
    while(1):
        #Grabs, decodes and returns the next video frame.
        ret, frame = cap.read()
        Coilgun.sendMotorCommand("p")
        if ret == True:
            ballInTrb = motorRight.andur()           
            if ballInTrb:
                if yellow:
                    gate_contour = searchForObject(yellowEro,yellowDil,YELLOW_MIN,YELLOW_MAX,gate_min_size,frame)
                    
                    if gate_contour != None:
                        (x,y), radius = cv2.minEnclosingCircle(gate_contour)
                        gateX = int(x)
                        gateY = int(y)
                        
                        doGateStuff(gateX,gateY,motorLeft,motorRight,motorBack,ballInTrb,Coilgun)
                        drawObjectOnFrame(gateX,gateY,radius,frame)
          
                    else:
                        robotMoveAroundDribblerLeft(motorLeft,motorRight,motorBack,27)
                        
                elif blue:
                    gate_contour = searchForObject(blueEro,blueDil,BLUE_MIN,BLUE_MAX,gate_min_size,frame)
                    
                    if gate_contour != None:
                        (x,y), radius = cv2.minEnclosingCircle(gate_contour)
                        gateX = int(x)
                        gateY = int(y)

                        doGateStuff(gateX,gateY,motorLeft,motorRight,motorBack,ballInTrb,Coilgun)
                        drawObjectOnFrame(gateX,gateY,radius,frame)
          
                    else:
                        robotMoveAroundDribblerRight(motorLeft,motorRight,motorBack,27)
            else:
                #dostuffforball
                ball_contour = searchForObject(ballEro,ballDil,ORANGE_MIN,ORANGE_MAX,ball_min_size,frame)
                
                if ball_contour != None:
                    (x,y), radius = cv2.minEnclosingCircle(ball_contour)
                    ballX = int(x)
                    ballY = int(y)
                    borderY = 170
                    if ballY > borderY:
                        speed = maxSpeed - (randomSpeed * ballY / maxY)
                        if speed < 10:
                                speed = 10
                    else:
                        speed = maxSpeed
                        
                    border = searchForBorderline(borderEro,borderDil,BORDERLINE_MIN,BORDERLINE_MAX,borderline_min_size,(x,y),frame,dribbler_point,LINE_SIZE)
                    
                    if not border:
                        doBallStuff(ballX,ballY,motorLeft,motorRight,motorBack,speed)
                        drawObjectOnFrame(ballX,ballY,radius,frame)
                    else:
                        robotTurnLeft(15,motorLeft,motorRight,motorBack)
    
                else:
                    robotTurnLeft(6,motorLeft,motorRight,motorBack)
##            cv2.imshow('Frame', frame)

            #Hold random key for 1sec + press 'q' to end program
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    cap.release()
    cv2.destroyAllWindows()
    motorLeft.disconnectMotor()
    motorRight.disconnectMotor()
    motorBack.disconnectMotor()
    Coilgun.disconnectMotor()

def searchForBorderline(objEro,objDil,color_min,color_max,object_min_size,ballCoord,frame,dribbler_point,LINE_SIZE):
    dil_thresh_frame = threshFrame(objEro,objDil,color_min,color_max,frame)
    return get_line_between_ball(dil_thresh_frame,ballCoord,dribbler_point,LINE_SIZE)

def get_line_between_ball(image, ball,dribbler_point,LINE_SIZE):
        ballx = int(ball[0])
        bally = int(ball[1])
        div = (bally - dribbler_point[1])
        if div == 0:
            div = 1
        

        m = (ballx - dribbler_point[0]) / div
        points = []
        to = int(dribbler_point[1])
        for i in range(bally, to):
            x = int(m * (i - dribbler_point[1]) + dribbler_point[0])
            points.append(image[i][x])
        if (points):
            counter = 0
            temp_counter = 0
            previous_i = points[0]
            for i in points:
                if (i and previous_i):
                    temp_counter += 1
                if (temp_counter > counter):
                    counter = temp_counter
                previous_i = i

            return True if counter > LINE_SIZE else False
        else:
            return False

def searchForObject(objEro,objDil,color_min,color_max,object_min_size,frame):
    dil_thresh_frame = threshFrame(objEro,objDil,color_min,color_max,frame)
    largest_contour = getContoursOfObject(dil_thresh_frame,object_min_size)
    return largest_contour

def drawObjectOnFrame(x,y,radius,frame):
    center = (int(x),int(y))
    radius = int(radius)
    cv2.circle(frame, center, radius, (0,255,0), 2)

def doBallStuff(x,y,motorLeft,motorRight,motorBack,speed):
    if x < 270:
        robotMoveInDirAndRot(0,speed,10,motorLeft,motorRight,motorBack)
    elif x > 370:
        robotMoveInDirAndRot(0,speed,-10,motorLeft,motorRight,motorBack)
    else:
        robotMoveInDir(0,speed,motorLeft,motorRight,motorBack)
                                 
def doGateStuff(x,y,motorLeft,motorRight,motorBack,ballInTrb,Coilgun):
    if x < 240:
        robotMoveAroundDribblerRight(motorLeft,motorRight,motorBack,20)
    elif x > 390:
        robotMoveAroundDribblerLeft(motorLeft,motorRight,motorBack,20)
    elif x >= 240 and x <= 390:
        Coilgun.coilgun()        

def getContoursOfObject(dil_thresh_frame,object_min_size):
    #Search for contour (ball or whatever)
    contours, hierarchy = cv2.findContours \
                          (dil_thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #search for nearest object
    max_area = 0
    largest_contour = None

    for contour in contours:              
        if len(contour) > object_min_size:
            area = cv2.contourArea(contour)
            if area > max_area:
              max_area = area
              largest_contour = contour
              
    return largest_contour

def threshFrame(erosion,dilation,color_min,color_max,mainframe):

    erosion = np.ones((erosion,erosion), "uint8")
    dilation = np.ones((dilation,dilation), "uint8")
    
    ero_frame = cv2.erode(mainframe, erosion)

    #Convert "usual" picture to HSV
    ero_hsv_frame = cv2.cvtColor(ero_frame, cv2.COLOR_BGR2HSV)

    #Initialize color sort
    searchcolor = cv2.inRange(ero_hsv_frame, color_min, color_max)

    ero_hsv_frame = searchcolor

    dil_thresh_frame = cv2.dilate(ero_hsv_frame, dilation)
    return dil_thresh_frame
