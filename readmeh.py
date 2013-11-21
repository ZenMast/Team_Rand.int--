##cameraNew02 lisasin
##import pickle  so we can read pkl fils.
## cPickle is faster than pickle 1000x
## cameraNew02 includes the variables and the list values given below now
## so in theory configurator.py works with our code.
import cPickle as pickle
pkl_file= open("config.pkl", "rb") 
colorvalues=pickle.load(pkl_file)
print colorvalues["colorsettings"]
## miinimumv22rtused min hue, mi sat,min value listis
minb = [int(i) for i in colorvalues["colorsettings"]["bluegate"][0]]
miny = [int(i) for i in colorvalues["colorsettings"]["yellowgate"][0]]
minball = [int(i) for i in colorvalues["colorsettings"]["ball"][0]]
minborder = [int(i) for i in colorvalues["colorsettings"]["borderline"][0]]
## maksimumv22rtused max hue, max sat, max value listis
maxb = [int(i) for i in colorvalues["colorsettings"]["bluegate"][1]]
maxy = [int(i) for i in colorvalues["colorsettings"]["yellowgate"][1]]
maxball = [int(i) for i in colorvalues["colorsettings"]["ball"][1]]
maxborder = [int(i) for i in colorvalues["colorsettings"]["borderline"][1]]
## minimum size, erode ja dilate v22rtused listis
sedb=colorvalues["colorsettings"]["bluegate"]
sedy=colorvalues["colorsettings"]["yellowgate"]
sedball=colorvalues["colorsettings"]["ball"]
sedborder=colorvalues["colorsettings"]["borderline"]



## andur ja dribbler peaks stabiilne olema 100protsenti et saaks korralikult koodi parandada


## how to be certain that it always aims perfectly?
##  we know that the gate always has a certain size ratio like 1:3? height:length
## knowing that we can ask the robot to check the contour values(need to check hw to do that)
## if the size fits its ok to shoot we can also have a minimum size requirement




## borders- the white lines being dominant also in the middle means its much
##harder to code
#### but the official stage has black lines around the outer perimeter
##of the white lines thus
##making it much easier to code the robot to avoid certain borders

## either make the videocode better or make the robot smarter and tell it to follow the blacklines til he finds a primary color




    

