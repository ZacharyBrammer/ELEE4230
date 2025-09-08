from machine import Pin, ADC


adc0 = ADC(Pin(26))


def adc2volt(adcval):
    return (adcval*(1/20008))-(42.143/20008)


def get_angle():
    voltage = adc2volt(adc0.read_u16())
    angle = (-80.65*voltage)+314.11
    return angle


def get_servo_angle():
    voltage = adc2volt(adc0.read_u16())
    angle = (-80.65*voltage)+314.11
    return angle-90
        
