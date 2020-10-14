from microbit import *
from airpy import *
import radio
radio.on()
radio.config(channel=1)
uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin1, rx=pin2)
Roll=0
Pitch=0
Throttle=0
Yaw=0
while True:
    display.clear()
    mottatt=radio.receive()
    if mottatt:
        verdier=mottatt.split(',')
        Pitch =int(verdier[0])
        Roll=int(verdier[1])
        Throttle=int(verdier[2])
        Yaw=int(verdier[3])
    display.set_pixel(map(Roll,-90,90,0,4),map(Pitch,-90,90,0,4),9)
    display.set_pixel(0,map(Throttle,0,100,4,0),9)
    display.set_pixel(2,0,9)
    display.set_pixel(4,4,9)
    flightcontrol(Throttle,Yaw,Pitch,Roll,0,1,0)