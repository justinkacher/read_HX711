from hx711 import HX711
import RPi.GPIO as GPIO


num_measures=3                                     #number of measurements to be taken by scale (more will be more precise)
readval = 0
tare = 0

def initreset():
    hx711 = HX711(                                      #set pins and gain
                dout_pin=3,
                pd_sck_pin=2,
                channel='A',
                gain=128
            )
    hx711.reset()                                       #reset board


def average(list):                                  #takes average of each measure taken
    measureaverage = sum(list)/len(list)
    return int(measureaverage)


def twotodec(num):                                  #converts two's compliment output of HX711 to a decimal number we can interpret
      
    # to convert from 2's compliment to bianary:
    # invert bianary of 2's compliment
    # add 1 and convert back to decimal

    inverse = ''
    binnum = bin(num)
    if binnum[0] == '-':            #removes signed bit to make inversion smoother
        sign = binnum[0:3]          #bit 0 is a signed bit ... 1 and 2 are "0b"
        unsign = binnum[3:]
    else:
        sign = binnum[0:2]          #bit 0 is a signed bit ... 1 and 2 are "0b"
        unsign = binnum[2:]

    for x in unsign:                #returns inverse of unsign
        
        if x == '0':
            inverse += '1'
        else:
            inverse += '0'

    convertednum = int(inverse,2)      #converts to integer from base 2
    convertednum+=1                    #add 1 to inverted integer
    return convertednum


def readscale():                                    #takes raw measuremnts from scale
    #set up pins, set gain
    while True:
        try:
            hx711 = HX711(
                dout_pin=3,
                pd_sck_pin=2,
                channel='A',
                gain=128
            )

            hx711.reset()                                   # Before we start, reset the HX711 (not obligate)
            measures = hx711.get_raw_data(num_measures)     #taking measurement num_measures # of times
            return measures
            
        except: 
            pass
        finally:
            GPIO.cleanup()                                  # always do a GPIO cleanup in your scripts!



#tare scale:
def tarescale():
    while True:
        measures = readscale()          #generates list of raw measures in two's compliment
        tare = average(measures)        #averages the list of measures
        tare = twotodec(tare)           #converts to readable decimal (nearly sure this is in thousandths of a pound?)
        round(tare)
        if tare >=0:
            round(tare,2)
            return tare/450
            break
        else:
            pass

        

#take a raw measurement
def takemeasure(tare):
    while True:
        measures = readscale()          #generates list of raw measures in two's compliment
        readavg = average(measures)     #averages the list of measures
        readval = twotodec(readavg)     #converts to readable decimal (nearly sure this is in thousandths of a pound?)
        readval = readval-tare
        readval = readval/450
        
        if (0<=(readval)<=5000):  #load cell max of 5 kg, and less than 0 means misread
            round(readval,2)
            return round((readval-tare),2)
            break
        else:
            pass

