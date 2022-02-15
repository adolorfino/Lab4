"""!
    @file       user_interface.py
        This file is responsible for collecting collected from the RC
        circuit. It communicates with the MicroPython directly and sends data
        to the VCP to be read and plotted separately.

    @author: Chloe Chou
    @author: Aleya Dolorfino
    @author: Christian Roberts
    @date: February 15, 2022
"""

import pyb
import micropython
import utime
import task_share
from pyb import USB_VCP
vcp = USB_VCP()

micropython.alloc_emergency_exception_buf(100)

# Creates a queue to hold 1000 16-bit integers
my_queue = task_share.Queue('H', 1000)


def handler(tim):
     """!
        This method reads values off the circuit and store them in a queue
        to be read separately.
        
        @param tim A timer object from the MicroPython board.
        """
    x = ADC_C0.read()
    my_queue.put(x)
    

if __name__ == '__main__':

    while True:
        if vcp.any():
            # Creates pins as an input and output
            pinC1 = pyb.Pin(pyb.Pin.board.PC1, mode = pyb.Pin.OUT_PP)
            pinC0 = pyb.Pin(pyb.Pin.board.PC0, mode = pyb.Pin.IN)
            ADC_C0 = pyb.ADC(pinC0)
            
            # Creates the time and voltage arrays to store the information
            time = []
            voltage = []
            
            #Keep the output pin low to begin with
            pinC1.low()
            
            #Creates a timer object to track the data
            tim = pyb.Timer(1, freq = 1000)
            
            #Turn the pin on
            pinC1.high()
            
            # Wait 1000 ms
            tim.callback(handler)
            utime.sleep_ms(1000)
            tim.callback(None)
            
            # Append the queue data into the established arrays
            print("printing queue")
            for x in range (my_queue.num_in()):
                time.append(x)
                voltage.append(my_queue.get())
            
            # Turn the pin off after the data is collected
            pinC1.low()
            
            #Clear the queue
            my_queue.clear()
            
            # Print the data into the VCP
            state = 0
            while True:
                if state == 0:
                    if vcp.any() == True:
                        for n in range(0,len(time),1):
                            auteur = str(voltage[n])+', '+str(time[n])
                            vcp.write(auteur.encode())
                            vcp.write('\n')
                        

                        vcp.write('end\n'.encode())
                        state = 1
                        vcp.write('\n')
                elif state == 1:
                    if vcp.read() == b'g':
                        state = 0
                    else:
                        pass
        
