from microbit import *
import radio
import math
from airpy import *
radio.on()
radio.config(channel=1,power=7)
Throttle=0
Yaw=0
Arm=0
display.set_pixel(0,4,9)
while True:

    Roll=mapping(accelerometer.get_x(),-1024,1024,-90,90)
    if Roll>90: Roll=90
    if Roll<-90: Roll=-90
    Pitch=mapping(accelerometer.get_y(),-1024,1024,-90,90)
    if Pitch>90: Pitch=90
    if Pitch<-90: Pitch=-90
    if button_a.was_pressed():
        Throttle=Throttle-5
    if button_b.was_pressed():
        Throttle=Throttle+5
    if Throttle>95: Throttle=95
    if Throttle<0: Throttle=0
    gesture = accelerometer.current_gesture()
    if gesture == "shake":
        Throttle=0
        Arm=0
    if button_a.is_pressed() and button_b.is_pressed():
        Throttle=0
        Arm=1
        sendTekst = str(Pitch)+","+str(Roll)+","+str(Throttle)+","+str(Yaw)+","+str(Arm)
        radio.send(sendTekst)
        sleep(1000)
        Yaw=0
    display.clear()
    display.set_pixel(2, 0, 9)
    display.set_pixel(4, 4, 9)
    display.set_pixel(0, mapping(Throttle, 0, 100, 4, 0), 9)
    display.set_pixel(mapping(Roll, -90, 90, 0, 4), mapping(Pitch, -90, 90, 0, 4), 9)
    sendTekst = str(Pitch)+","+str(Roll)+","+str(Throttle)+","+str(Yaw)+","+str(Arm)
    radio.send(sendTekst)
