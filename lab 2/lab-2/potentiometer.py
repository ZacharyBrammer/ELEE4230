from machine import Pin, ADC
import utime


adc0 = ADC(Pin(26))
adc0_slope = 0.00005
adc0_offst = 0.00211

pot_slope = -80.65
pot_offst = 264.44


def get_voltage(adcval):
    return adc0_slope*adcval + adc0_offst


def get_angle():
    voltage = get_voltage(adc0.read_u16())
    angle = pot_slope*voltage + pot_offst
    return angle


while True:
    print(f"{get_voltage(adc0.read_u16()):.2f}V")
    utime.sleep(0.1)
