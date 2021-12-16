from tkinter import *
import tkinter as tk
from tkinter.constants import *
from RaspberryPi_Read import *
from hx711 import HX711
import RPi.GPIO as GPIO
from RaspberryPi_Read import *

#init variables
num_measures=3                                     #number of measurements to be taken by scale (more will be more precise)
tare = 0
measureval = 0

initreset()

#tare scale
def fcntare():
    global tare
    tare = tarescale()
    print("tare complete")
    return tare

#shell fcn to pass tare value
def fmeasure():
    fcnmeasure(tare)
#take measurement
def fcnmeasure(tare):
    print(tare)
    measureval = takemeasure(tare)
    print('measure complete')
    print(measureval)
    measurevallbl.configure(
        text = measureval
    )
    print("lbl update succesful")


#start tkinter window
window = tk.Tk()
print('starting GUI generation')

##################################################
Lframe = Frame(window)
Lframe.pack(side = LEFT)


##################################################
rightoutputframe = Frame(window)
rightoutputframe.pack(  
    side = RIGHT,
    padx = 20
)

topRframe = Frame(rightoutputframe)
topRframe.pack(side = TOP)

midRframe = Frame(rightoutputframe)
midRframe.pack()

botRframe = Frame(rightoutputframe)
botRframe.pack(
    side = BOTTOM,
    pady = 10
    )
##################################################


#TARE BUTTON
print("generating tare btn")
tarebutton = tk.Button(
    Lframe,
    text="Tare",
    height = 10,
    width = 20,
    font = ("Courier",10),
    command = fcntare
)
tarebutton.pack(side = TOP)
print("Done")

#TAKE MEASURE BUTTON
print("generating measure btn")
measurebutton = tk.Button(
    Lframe,
    text="Take Measurement",
    height = 10,
    width = 20,
    font = ("Courier",10),
    command = fmeasure
)
measurebutton.pack(side = BOTTOM)
print("Done")

#SAVE VALUE LABEL
print("generating save lbl")
checkvallbl = tk.LabelFrame(
    topRframe,
    text = "Save this value?",
    height = 20,
    width=20,
    font = ("Courier",10)
)
checkvallbl.pack()
print("Done")

#VALUE OF MEASURE LABEL
print("generating val lbl")
measurevallbl = tk.Label(
    checkvallbl,
    text = measureval,
    font = ("Courier",40)
)
measurevallbl.pack()
print("Done")

#YES BUTTON
print("generating 'yes' button")
yesbtn = tk.Button(
    botRframe,
    text = "YES",
    height=3,
    width=10,
    font = ("Courier",10)
)
yesbtn.pack(side = LEFT)
print("Done")

#NO BUTTON
print("generating 'no' button")
nobtn = tk.Button(
    botRframe,
    text = "NO",
    height=3,
    width=10,
    font = ("Courier",10)
)
nobtn.pack(side = RIGHT)
print("Done")

print('GUI generation succesful')

window.mainloop()