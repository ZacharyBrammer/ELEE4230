from machine import Pin, ADC
from kalman import KalmanFilter
import utime


kf = KalmanFilter(error_est_x=100, error_est_y=0.001, error_mea_x=1)

mux_pin = Pin(14, Pin.OUT)
mux_slope = 0.1598
mux_offst = -0.2077

adc0 = ADC(Pin(26))
adc0_slope = 0.00005
adc0_offst = 0.00211


def get_voltage(adcval):
    return adc0_slope*adcval+adc0_offst


def get_ldr_state(voltage):
    if voltage > 2.4:
        return "Flashlight"
    elif voltage > 1.3:
        return "Normal"
    else:
        return "Blocked/Dark"


mux_pin.value(0)
initial_kalman = adc0.read_u16()
kf.last_x = initial_kalman

while True:
    pot_samples = []
    ldr_samples = []
    for sample in range(10):
        mux_pin.value(0)
        #pot_samples.append(get_voltage(kf.get_filtered_value(adc0.read_u16())))
        pot_samples.append(get_voltage(adc0.read_u16()))
        mux_pin.value(1)
        ldr_samples.append(get_voltage(adc0.read_u16()))
    
    pot_voltage = sum(pot_samples)/len(pot_samples)
    ldr_offst = (mux_slope*pot_voltage)+mux_offst
    ldr_voltage = (sum(ldr_samples)/len(ldr_samples))#+ldr_offst
    print(f"Potentiometer: {pot_voltage:.2f} V\nLDR: {get_ldr_state(ldr_voltage)} ({ldr_voltage:.2f} V)\n")
    utime.sleep(0.1)

