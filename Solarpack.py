# import pymeasure
# print(pymeasure.__version__)

# from pymeasure.instruments.keithley import keithley2450
# from pymeasure.adapters import visa
#
# kAdapter = visa('USB0::0x05E6::0x2450::04366211::INSTR')
#
# sourcemeter = keithley2450('USB0::0x05E6::0x2450::04366211::INSTR')
# sourcemeter.id

import pyvisa
import time
import pandas as pd
from statistics import mean

rm = pyvisa.ResourceManager()

#print(rm.list_resources())     # returns a tuple of connected devices # 'USB0::0x05E6::0x2450::04366211::INSTR'

keithley = rm.open_resource('USB0::0x05E6::0x2450::04366211::INSTR')

print(keithley.query("*IDN?"))      # query's the Identity of the device connected
# alternative to query is write/read
# keithley.write("*IDN?")
# print(keithley.read())

# keithley.write("*rst; status:preset; *cls")     # send initialization, reset, and clear status register message
#
# keithley.query('opc?')      # operation complete waits untial previuos comand have finished before moving forward

# manual page 34
# keithley.write('*LANG SCPI')        # To change to the SCPI command set from a remote interface
# # then reboot?

# var1 = 5
# print(f'test {var1} and {1+2}')       # test 5 and 3


# battery connection:
# Sense Hi and Force Hi connect to positive terminal
# Sense Lo and Force Lo connect to negative terminal



# battery capacity testing on keithley 2450 https://www.mouser.com/pdfdocs/RechargeableBattery_2450_AN1.PDF
# 1. set to four-wire configuration
# 2. set to source voltage, measure load current
# 3. use high impedance output off state; opens output relay when output is turned off to prevent drainage when not testing
# 4. set output voltage. Charging: VSource > VBattery (current is positive); Discharging: VS < VB (current is negative)
# 5. turn voltage soucre readback function to measure battery voltage
# 6. set current limit to charge or discharge the battery

sourceVoltage = 2.7          # Charging: VSource > VBattery; Discharging: VS < VB # 18650 is 3.7v; max charging is 4.2v and min discharge final is 2.75
voltageRange = 20            # 20mV, 200mV, 2V, 20V, 200V
sourceLimit = 1              # Current Limit = Charge or Discharge rate # units A => 460e-3 A =.46 A = 460mA
currentRange = 1             # Max 1.05A

keithley.write('*RST')      # first line is to reset the instrument

keithley.write('OUTP:SMOD HIMP')                    # turn on high-impedance output mode

keithley.write('SENS:CURR:RSEN ON')                 # set to 4-wire sense mode  # OFF = 2-Wire mode

keithley.write('SENS:FUNC "CURR"')                  # set measure, sense, to current

keithley.write(f'SENS:CURR:RANG {currentRange}')    # set current range # can also be 'SENS:CURR:RANG:AUTO ON'

#keithley.write('SENS:CURR:UNIT OHM')                # set measure units to Ohm, can also be Watt or Amp

keithley.write('SOUR:FUNC VOLT')                    # set source to voltage

keithley.write(f'SOUR:VOLT {sourceVoltage}')        # set output voltage => discharge or charge test

keithley.write('SOUR:VOLT:READ:BACK ON')            # turn on source read back

keithley.write(f'SOUR:VOLT:RANG {voltageRange}')    # set source range

keithley.write(f'SOUR:VOLT:ILIM {sourceLimit}')     # set source (current) limit

keithley.write('OUTP ON')                           # turn on output, source

iteration = 1       # iteration must start at 1 for Keithly write
voltLimit = 2.75      # voltage which to stop the test
currentL = []
voltageL = []
measTimeL = []

rollingList = []

# 7. read load current, source voltage, and time stamp
# 8. stop tset when battery reaches desired voltage

while iteration >=0:    # infinite while loop; breaks when voltLimit is reached
    #print(iteration)

    keithley.write('READ? "defbuffer1"')        # a ? is used for a query command otherwise is a set command
    current = keithley.read()                   # a query command asks the instrument to return specifed information # a read is required before next set or query
    # print(current)
    currentL.append(float(current))
    keithley.write(f'TRAC:DATA? {iteration}, {iteration},"defbuffer1", SOUR')
    volt = keithley.read()
    # print(volt)
    voltageL.append(float(volt))
    keithley.write(f'TRAC:DATA? {iteration}, {iteration}, "defbuffer1", REL')
    timeSec = keithley.read()
    # print(float(timeSec))
    measTimeL.append(float(timeSec))


    # takes the rolling average voltage
    # this average is used to determine when to break from the tests
    # onlyy breaks after the first 15 measurements have been collected
    rollingList.append(float(volt))
    if len(rollingList) > 15:
        rollingList.pop(0)              #removes the very first item in list when there are 10 measurements

        if mean(rollingList) <= voltLimit:  # <= voltLimit for Discharging # >= voltLimit for Charging
            print('break')
            break                           # breaks out of while loop when the specified condition is met

    iteration += 1
    time.sleep(1)      # sleep is in seconds


keithley.write('OUTP OFF')


# initialize dataframe to store all the lists in a single grouping
measurementDF = pd.DataFrame()
measurementDF['Time (sec.)'] = pd.Series(measTimeL)
measurementDF['Voltage (V)'] = pd.Series(voltageL)
measurementDF['Current (A)'] = pd.Series(currentL)
# exports the data frame to excel
measurementDF.to_excel('C:/Users/nwoodwa/Desktop/SolarPack/'+'Test2.xlsx')
# export the data to csv
# measurementDF.to_csv('C:/Users/nwoodwa/Desktop/SolarPack/'+'Test2.csv')
# export the data to json
# measurementDF.to_json('C:/Users/nwoodwa/Desktop/SolarPack/'+'Test2.json')


#keithley.query('opc?')      # operation complete waits untial previuos comand have finished before moving forward







