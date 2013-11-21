import MotorsThinkPad
from MotorsThinkPad import *
import CameraNew06
from CameraNew06 import *

motorLeft = MotorsThinkPad(1,MotorsThinkPad.ports[0])
motorRight = MotorsThinkPad(2,MotorsThinkPad.ports[1])
motorBack = MotorsThinkPad(3,MotorsThinkPad.ports[2])
Coilgun = MotorsThinkPad(4,MotorsThinkPad.ports[3])

print "start"

wholeCamera(motorLeft,motorRight,motorBack,Coilgun,"blue")



 
