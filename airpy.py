import math
import radio
from microbit import *


def mapping(value, fromLow, fromHigh, toLow, toHigh):
    a = (toLow - toHigh) / (fromLow - fromHigh)
    b = toHigh - a * fromHigh
    exact = a * value + b
    rest = exact - math.floor(exact)
    if rest > 0.5:
        return math.ceil(exact)
    else:
        return math.floor(exact)


def flightcontrol(Throttle=0, Yaw=0, Pitch=0, Roll=0, Aux=0, flightMode=1, Buzzer=0):
    """
        Dette er en funksjon for å styre en drone med en KK 2.1.5. flight controller. \n
        Verdiene Throttle, Yaw, Pitch Roll, Aux,flightmode og Buzzer sendes til KK 2.1.5 kortet.\n
        Throttle=gass, øker hastigheten oppover   (0 til 100) \n
        Pitch=Beveger dronen fremover/bakover (-90 til 90) \n
        Roll=Beveger dronen mot høyre/vesntre (-90 til 90) \n
        Yaw=Rotajosn av dronen rundt sin egen akse (-90 til 90) \n
        Aux skal settes lik 0. \n
        FlightMode skal settes lik 1 \n
        Buzzer skal settes lik 0
    """
    buf = bytearray(16)
    scaling = 3.5
    offset = 512  # Header "Fade" (Spektsat code)
    buf[0] = 0  # Header "System" (Spektsat code)
    buf[1] = 0x01
    # 0x01 22MS 1024 DSM2
    # 0x12 11MS 2048 DSM2
    # 0xa2 22MS 2048 DSMS
    # 0xb2 11MS 2048 DSMX
    # Calibrate mode, perform a calibration of the acc using stick command
    if flightMode == 3:
        Throttle = 100
        Yaw = -90
        Pitch = -90
        Roll = 0
        Aux = 0
        flightMode = 1
    # Upscale Aux (Aux = true or false)
    Aux11 = 0
    if Aux == 0:
        Aux11 = 0
    if Aux == 1:
        Aux11 = 180 * (scaling + 1.5)
    # Upscale Buzzer (Buzzer = 0 or 1)
    Buzzer11 = 0
    if Buzzer == 0:
        Buzzer11 = 0
    if Buzzer == 1:
        Buzzer11 = 180 * scaling
    # Acro mode (no self level)
    if flightMode == 0:
        flightMode = 0
    # Stabilise / self level mode
    if flightMode == 1:
        flightMode = 180
    # Vision mode similar to angle mode in terms of stabilisation in flight controller
    if flightMode == 2:
        flightMode = 180
    if Throttle > 99:
        Throttle = 99
    if Throttle < 0:
        Throttle = 0
    if Yaw > 90:
        Yaw = 90
    if Yaw < -90:
        Yaw = -90
    if Pitch > 90:
        Pitch = 90
    if Pitch < -90:
        Pitch = -90
    if Roll > 90:
        Roll = 90
    if Roll < -90:
        Roll = -90
    pitch11 = int(Pitch * scaling + offset)
    roll11 = int(Roll * scaling + offset + 9.5)
    yaw11 = int(Yaw * (scaling + 1.5) + offset)
    throttle10 = int(2*Throttle/3+20)
    flightMode11 = int(flightMode * (scaling + 1.5))
    buf[2] = (0 << 2) | ((roll11 >> 8) & 3)
    buf[3] = roll11 & 255
    buf[4] = (1 << 2) | ((pitch11 >> 8) & 3)
    buf[5] = pitch11 & 255
    buf[6] = (2 << 2) | ((throttle10 >> 8) & 3)
    buf[7] = throttle10 & 255
    buf[8] = (3 << 2) | ((yaw11 >> 8) & 3)
    buf[9] = yaw11 & 255
    buf[10] = (4 << 2) | ((Aux11 >> 8) & 3)
    buf[11] = Aux11 & 255
    buf[12] = (5 << 2) | ((flightMode11 >> 8) & 3)
    buf[13] = flightMode11 & 255
    buf[14] = (6 << 2) | ((Buzzer11 >> 8) & 3)
    buf[15] = Buzzer11 & 255
    uart.write(buf)
