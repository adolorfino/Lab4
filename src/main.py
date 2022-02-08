import pyb
import micropython
import utime
import task_share
from pyb import USB_VCP
vcp = USB_VCP()

micropython.alloc_emergency_exception_buf(100)
my_queue = task_share.Queue('H', 1000)

def handler(tim):
    x = ADC_C0.read()
    my_queue.put(x)
    

if __name__ == '__main__':
    while True:
        if vcp.any():
            pinC1 = pyb.Pin(pyb.Pin.board.PC1, mode = pyb.Pin.OUT_PP)
            pinC0 = pyb.Pin(pyb.Pin.board.PC0, mode = pyb.Pin.IN)
            ADC_C0 = pyb.ADC(pinC0)
            time = []
            voltage = []
            pinC1.low()
            
            tim = pyb.Timer(1, freq = 1000)
            pinC1.high()
            
            tim.callback(handler)
            utime.sleep_ms(1000)
            tim.callback(None)
            
            print("printing queue")
            for x in range (my_queue.num_in()):
                time.append(x)
                voltage.append(my_queue.get())
            pinC1.low()
            
            my_queue.clear()
            
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
        
