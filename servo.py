from machine import Pin, PWM


servo0 = PWM(Pin(3, Pin.OUT))
servo1 = PWM(Pin(4, Pin.OUT))

servo0.freq(50)
servo0.duty_u16(0)
servo1.freq(50)
servo1.duty_u16(0)

servo0_mult = -35.0
servo1_mult = -34.0
servo0_offset = 8100
servo1_offset = 7800


def set_angle(motor, angle):
    if angle >= 0 and angle <= 180:
        if motor == 0:
            servo0.duty_u16(int((servo0_mult*angle)+servo0_offset))
        elif motor == 1:
            servo1.duty_u16(int((servo1_mult*angle)+servo1_offset))

