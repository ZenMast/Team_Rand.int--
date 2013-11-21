
import cv2
import numpy as np
import tkMessageBox
from Tkinter import *
from threading import Thread
from time import time, sleep
import pickle


# create video capture
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)
cap.set(cv2.cv.CV_CAP_PROP_FPS, 30)
width, height = cap.get(3), cap.get(4)




#default settings for balls
pkl_file = open('config.pkl', 'rb')
data = pickle.load(pkl_file)
pkl_file.close()

COLORSETTINGS = data['colorsettings']
SETTINGS = data['settings']


#How to read dis: [0] = minvalues, [1] = maxvalues, [2] = erode, [3] = dilate, [4] = size
current_color_options = COLORSETTINGS.keys()[0]
current_random_options = SETTINGS.keys()[0]

#variables to initialize with
kernel = None
kernel2 = None
min_hue_slider = None
max_hue_slider = None
min_sat_slider = None
max_sat_slider = None
min_val_slider = None
max_val_slider = None
dilation_slider = None
erode_slider = None
size_slider = None

confwindow = None

changes_made = 0


fpsbox = None
fps = None


running = 1


#commands for sliders
def change_min_hue(n):
    global changes_made, COLORSETTINGS, current_color_options
    COLORSETTINGS[current_color_options.get()][0][0] = n
    changes_made = 1
    
    
def change_min_sat(n):
    global changes_made, COLORSETTINGS, current_color_options
    COLORSETTINGS[current_color_options.get()][0][1] = n
    changes_made = 1
    
def change_min_val(n):
    global changes_made, COLORSETTINGS, current_color_options
    COLORSETTINGS[current_color_options.get()][0][2] = n
    changes_made = 1

def change_max_hue(n):
    global changes_made, COLORSETTINGS, current_color_options
    COLORSETTINGS[current_color_options.get()][1][0] = n
    changes_made = 1

def change_max_sat(n):
    global changes_made, COLORSETTINGS, current_color_options
    COLORSETTINGS[current_color_options.get()][1][1] = n
    changes_made = 1

def change_max_val(n):
    global changes_made, COLORSETTINGS, current_color_options
    COLORSETTINGS[current_color_options.get()][1][2] = n
    changes_made = 1
    
def change_dilation(n):
    global changes_made, COLORSETTINGS, current_color_options
    COLORSETTINGS[current_color_options.get()][3] = n 
    changes_made = 1
    
def change_erosion(n):
    global changes_made, COLORSETTINGS, current_color_options
    COLORSETTINGS[current_color_options.get()][2] = n
    changes_made = 1
    
def change_size(n):
    global changes_made, COLORSETTINGS, current_color_options
    COLORSETTINGS[current_color_options.get()][4] = n
    changes_made = 1
    
#reset slider positions on changing color tabs
def slider_callback(n, i, m):
    global current_color_options, min_hue_slider, min_sat_slider, min_val_slider, max_hue_slider, max_sat_slider, max_val_slider, dilation_slider, erode_slider
    min_hue_slider.set(COLORSETTINGS[current_color_options.get()][0][0])
    min_sat_slider.set(COLORSETTINGS[current_color_options.get()][0][1])
    min_val_slider.set(COLORSETTINGS[current_color_options.get()][0][2])
    max_hue_slider.set(COLORSETTINGS[current_color_options.get()][1][0])
    max_sat_slider.set(COLORSETTINGS[current_color_options.get()][1][1])
    max_val_slider.set(COLORSETTINGS[current_color_options.get()][1][2])
    dilation_slider.set(COLORSETTINGS[current_color_options.get()][3])
    erode_slider.set(COLORSETTINGS[current_color_options.get()][2])
    size_slider.set(COLORSETTINGS[current_color_options.get()][4])

#reset current values for sliders back to default
def reset_values():
    global current_color_options, min_hue_slider, min_sat_slider, min_val_slider, max_hue_slider, max_sat_slider, max_val_slider, COLORSETTINGS
    COLORSETTINGS[current_color_options.get()][0][0] = 0
    COLORSETTINGS[current_color_options.get()][0][1] = 0
    COLORSETTINGS[current_color_options.get()][0][2] = 0
    COLORSETTINGS[current_color_options.get()][1][0] = 180
    COLORSETTINGS[current_color_options.get()][1][1] = 255
    COLORSETTINGS[current_color_options.get()][1][2] = 255
    min_hue_slider.set(COLORSETTINGS[current_color_options.get()][0][0])
    min_sat_slider.set(COLORSETTINGS[current_color_options.get()][0][1])
    min_val_slider.set(COLORSETTINGS[current_color_options.get()][0][2])
    max_hue_slider.set(COLORSETTINGS[current_color_options.get()][1][0])
    max_sat_slider.set(COLORSETTINGS[current_color_options.get()][1][1])
    max_val_slider.set(COLORSETTINGS[current_color_options.get()][1][2])
    changes_to_none()

def save_values():
    global COLORSETTINGS, SETTINGS, changes_made
    try:   
        output = open('config.pkl', 'wb')
        pickle.dump({'colorsettings': COLORSETTINGS, 'settings': SETTINGS}, output)
        output.close()
        changes_made = 0
    except Exception:
        pass
    

#what to do when x is pressed
def ask_quit():
    global changes_made, running
    if changes_made:
        if tkMessageBox.askokcancel("Quit", "Changes not saved, confirm exit."):
            running = 0
            confwindow.destroy()
            
    else:
        running = 0
        confwindow.destroy()

#self explanatory        
def changes_to_none():
    global changes_made
    sleep(0.5)
    changes_made = 0      
    


#Tkinter frame
class mywidgets:
    
    
    def __init__(self,root):
        frame = Frame(root)
        self.make_optionmenus(frame)
        self.make_sliders(frame)
        self.make_entry_box(frame)
        self.make_reset_button(frame)
        self.make_save_button(frame)
        frame.pack()
        return
    
    
    def make_optionmenus(self, frame):
        global COLORSETTINGS, current_color_options, SETTINGS, current_random_options 
        current_color_options = StringVar()
        current_color_options.set(COLORSETTINGS.keys()[0])
        options = apply(OptionMenu, (frame, current_color_options) + tuple(COLORSETTINGS.keys()))
        options.pack(side = LEFT)
        current_color_options.trace('w', slider_callback)
        #current_random_options = StringVar()
        #current_random_options.set(SETTINGS.keys()[0])
        #randoms = apply(OptionMenu, (frame, current_random_options) + tuple(SETTINGS.keys()))
        #randoms.pack(side = RIGHT)
        
        
        
    def make_reset_button(self, frame):
        resetbutton = Button(frame, text = 'Reset', command = reset_values)
        resetbutton.pack(side = TOP)
    
    def make_save_button(self, frame):
        savebutton = Button(frame, text = 'Save', command = save_values)
        savebutton.pack(side = TOP)
        
        
    def make_sliders(self, frame):        
        global min_hue_slider, min_sat_slider, min_val_slider, max_hue_slider, max_sat_slider, max_val_slider, changes_made, dilation_slider, erode_slider, size_slider
        dilation_slider = Scale(frame, from_=1, to=10, orient=HORIZONTAL, length=111, command = change_dilation, label = 'Dilation')
        dilation_slider.pack(side = RIGHT)
        dilation_slider.set(COLORSETTINGS[current_color_options.get()][3])
        erode_slider = Scale(frame, from_=1, to=10, orient=HORIZONTAL, length=111, command = change_erosion, label = 'Erode')
        erode_slider.pack(side=RIGHT)
        erode_slider.set(COLORSETTINGS[current_color_options.get()][2])
        min_hue_slider = Scale(frame, from_=0, to=180, orient=HORIZONTAL, length=500, command = change_min_hue, label = 'Minimum hue')
        min_hue_slider.pack()
        min_hue_slider.set(COLORSETTINGS[current_color_options.get()][0][0])
        max_hue_slider = Scale(frame, from_=0, to=180, orient=HORIZONTAL, length=500, command = change_max_hue, label = 'Maximum hue')
        max_hue_slider.pack()
        max_hue_slider.set(COLORSETTINGS[current_color_options.get()][1][0])
        min_sat_slider = Scale(frame, from_=0, to=255, orient=HORIZONTAL, length=500, command = change_min_sat, label = 'Minimum saturation')
        min_sat_slider.pack()
        min_sat_slider.set(COLORSETTINGS[current_color_options.get()][0][1])
        max_sat_slider = Scale(frame, from_=0, to=255, orient=HORIZONTAL, length=500, command = change_max_sat, label = 'Maximum saturation')
        max_sat_slider.pack()
        max_sat_slider.set(COLORSETTINGS[current_color_options.get()][1][1])
        min_val_slider = Scale(frame, from_=0, to=255, orient=HORIZONTAL, length=500, command = change_min_val, label = 'Minimum value')
        min_val_slider.pack()
        min_val_slider.set(COLORSETTINGS[current_color_options.get()][0][2])
        max_val_slider = Scale(frame, from_=0, to=255, orient=HORIZONTAL, length=500, command = change_max_val, label = 'Maximum value')
        max_val_slider.pack()
        max_val_slider.set(COLORSETTINGS[current_color_options.get()][1][2])
        size_slider = Scale(frame, from_=0, to=1000, orient=HORIZONTAL, length=500, command = change_size, label = 'Minimum Size')
        size_slider.pack()
        size_slider.set(COLORSETTINGS[current_color_options.get()][4])
        
        
    def make_entry_box(self, frame):
        global fpsbox, fps
        fps = StringVar()
        fpsbox = Entry(frame, state = 'readonly', textvariable=fps, width = 3)
        fpsbox.pack(side = LEFT)


#how to kick off Tkinter
def main():
    global confwindow, fps, changes_made
    confwindow = Tk()
    k = mywidgets(confwindow)
    confwindow.title('Configuration')
    confwindow.protocol("WM_DELETE_WINDOW", ask_quit)
    confwindow.mainloop()
    
#kicking off Tkinter  
thread = Thread(target = main, args = [])
thread.start()

#setting changes_made to 0 
thread2 = Thread(target = changes_to_none, args = [])
thread2.start()


#just got the video and this is crazy
start_time = time()
while running:  
    if type(current_color_options) is str:
        kernel = np.ones((int(COLORSETTINGS[current_color_options][2]), int(COLORSETTINGS[current_color_options][2])), 'uint8')
        kernel2 = np.ones((int(COLORSETTINGS[current_color_options][3]), int(COLORSETTINGS[current_color_options][3])), 'uint8')
    else:
        kernel = np.ones((int(COLORSETTINGS[current_color_options.get()][2]), int(COLORSETTINGS[current_color_options.get()][2])), 'uint8')
        kernel2 = np.ones((int(COLORSETTINGS[current_color_options.get()][3]), int(COLORSETTINGS[current_color_options.get()][3])), 'uint8')
    #but here's my frame
    _,frame = cap.read()
    #so erode me maybe
    erode = cv2.erode(frame, kernel)
    #convert picture to hsv and filter the colors, dilate the image
    hsv = cv2.cvtColor(erode, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv, np.array(COLORSETTINGS[current_color_options.get()][0], np.uint8), np.array(COLORSETTINGS[current_color_options.get()][1], np.uint8))
    dilate = cv2.dilate(thresh, kernel2)
    #for display purposes
    display_dilation = cv2.dilate(thresh, kernel2)
    #find the contours of the objects in hsv range
    cont = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = cont[0]
    
    #find the middle point of the object with the biggest contour
    suurused = []
    for contour in contours:
        suurused.append(len(contour))
        if len(contour) > int(COLORSETTINGS[current_color_options.get()][4]): 
            cordX = 0
            cordY = 0
            for i in contour:
                cordX += i[0][0]
                cordY += i[0][1]
            cordX = cordX / len(contour)
            cordY = cordY / len(contour)
            
            
    #display the windows        
    cv2.imshow('Original', erode)
    cv2.imshow('Editing', display_dilation)
    now = time()
    seconds_from_last = now - start_time
    fps.set(str(int(sorted(suurused)[-1] if suurused else 0)))
    start_time = now
    
    #kill on escape
    if cv2.waitKey(5)== 27:
        break

#lights out before leaving
cv2.destroyAllWindows()
cap.release()
