from machine import Pin, ADC
import time


adc0 = ADC(Pin(26))

readings = []
delays = [0.001, 0.0045, 0.005, 0.0056, 0.01, 0.02, 0.1]

# 10x :  0.001
# 2.2x:  0.0045
# 2x  :  0.005
# 1.8x:  0.0056
# 1x  :  0.01
# 0.5x:  0.02
# 0.1x:  0.1


for delay in delays:
    start_time = time.ticks_us()
    while time.ticks_us() - start_time < 100000:
        adcval = adc0.read_u16()
        (adcval*(1/20008))-(42.143/20008)
        readings.append(f'{time.ticks_us()-start_time},{adcval}')
        time.sleep(0.001)

    with open(f'{delay}.csv', 'w') as f:
        for row in readings:
            f.write(str(row) + '\n')

