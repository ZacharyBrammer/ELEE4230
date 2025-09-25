from machine import Pin, ADC
import utime


adc0 = ADC(Pin(26))
adc0_slope = 0.00005
adc0_offst = 0.00211


def get_voltage(adcval):
    return adc0_slope*adcval + adc0_offst


loops = 0
readings = []
while loops < 1000:
    utime.sleep(0.01)
    value = f"{get_voltage(adc0.read_u16()):.2f}"
    readings.append(value)
    print(value)
    loops += 1


with open(f'logpot.csv', 'w') as f:
        for row in readings:
            f.write(str(row) + '\n')
