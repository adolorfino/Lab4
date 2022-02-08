"""!
    @file       user_interface.py
        This file is responsible for the user interface of the motor commands. It
        communicates with the computer directly and takes motor's output data and
        plots it in a graph when the enter key on the keyboard is pressed.

    @author: Chloe Chou
    @author: Aleya Dolorfino
    @author: Christian Roberts
    @date: February 8, 2022
"""
from matplotlib import pyplot 
import serial

ser_port = serial.Serial("COM3", 115200, timeout = 10)

x_axis = []
y_axis = []

S0_INIT = 0
S1_WAIT_FOR_CHAR = 1
S2_APPEND = 2
S3_PLOT = 3

state = S0_INIT
while True:
    if state == S0_INIT:
        print ('\033[2JWelcome to ME 405 Lab 4\r\n')
        state = S1_WAIT_FOR_CHAR
        
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