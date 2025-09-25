from machine import Pin, ADC
import math
import utime


adc1 = ADC(Pin(27))
adc1_slope = 0.00005
adc1_offst = 0.00211


def get_voltage(adcval):
    return adc1_slope*adcval+adc1_offst


while True:
    thm_samples = []
    for sample in range(100):
        thm_samples.append(get_voltage(adc1.read_u16()))
    thm_voltage = sum(thm_samples)/len(thm_samples)
    thm_resistance = thm_voltage/0.00007
    thm_temp = (-27.87*math.log(thm_resistance))+218.77
    print(f'{thm_temp}°C')
    utime.sleep(0.1)
