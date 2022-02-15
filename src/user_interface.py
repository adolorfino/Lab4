"""!
    @file       user_interface.py
        This file communicates with the computer directly and is responsible
        for interfacing with the user. When the enter key on the keyboard is
        pressed, it plots the data collected from the RC circuit in a graph.

    @author: Chloe Chou
    @author: Aleya Dolorfino
    @author: Christian Roberts
    @date: February 15, 2022
"""
from matplotlib import pyplot 
import serial

#Sets up connection from computer on COM3
ser_port = serial.Serial("COM3", 115200, timeout = 10)

#Establishes data sets for x and y axes to be filled with data
x_axis = []
y_axis = []

#Establishes different states: init state, waiting for character, append, and plot.
S0_INIT = 0
S1_WAIT_FOR_CHAR = 1
S2_APPEND = 2
S3_PLOT = 3

#Begins at State 0 
state = S0_INIT
while True:
    
    #State 0 prints welcome message
    if state == S0_INIT:
        print ('\033[2JWelcome to ME 405 Lab 4\r\n')
        state = S1_WAIT_FOR_CHAR
    
    #State 1 prints message for users
    elif state == S1_WAIT_FOR_CHAR:
        char_in = input("Press ENTER to run the step response:")
        ser_port.write(b'g')
        if True:
            try:
                state = S2_APPEND
            except ValueError:
                print('value')
                pass
            except IndexError:
                print('index')
                pass
            
    #State 2 appends data from circuit into the x and y axes arrays
    elif state == S2_APPEND:
        if ser_port.in_waiting>0:
                if ser_port.in_waiting != 0:

                    line = ser_port.readline()
                    row = line.split (b',')
                    if line == b'end' or line == b'end\n':
                        state = S3_PLOT
                    try:
                        x = float(row[0])*(3.3/4095)
                        y = float(row[1])
                            
                        x_axis.append(y)
                        y_axis.append(x)
                    except:
                        pass
        else:
            pass
    # State 3 plots all data into a graph
    elif state == S3_PLOT:
        
        fig = pyplot.figure()
        ax = fig.add_axes([0.18, 0.1, .75, 0.8])
        ax.plot(x_axis,y_axis, linestyle = 'solid', color = 'green', linewidth = 1)
        ax.set_title('ME 405 Lab')
        ax.set_xlabel('Time [milliseconds]')
        ax.set_ylabel('ADC Reading [Volts]')
        pyplot.show()
        state = S1_WAIT_FOR_CHAR
        x_axis = []
        y_axis = []