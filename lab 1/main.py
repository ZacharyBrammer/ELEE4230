from machine import Pin, I2C, ADC
from secrets import secrets
import potentiometer
import servo
import bmp280
import random
import network
import urequests
import time
import math


sda = Pin(14)
scl = Pin(15)
i2c = I2C(1, scl=scl, sda=sda, freq=100000)

adc0 = ADC(Pin(26))
magnet = False

#bmp = bmp280.BMP280(i2c, addr=0x77)

last_send = 0
send_cool = 15.1

ssid = secrets['ssid']
password = secrets['password']
ts_key = secrets['ts_key']
ts_id = secrets['ts_id']
ts_url = 'https://api.thingspeak.com/update'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)


def connect_to_wifi():
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 2:
            break
        max_wait -= 1
        print('Connecting...')
        time.sleep(1)

    if wlan.status() == 3:
        print(f'Connection successful with IP {wlan.ifconfig()[0]}.')
    else:
        print('Connection failed.')


def thingspeak_write(data, field):
    global last_send
    if time.time() - last_send > send_cool:
        last_send = time.time()
        url = f'{ts_url}?api_key={ts_key}&{field}={data}'
        response = urequests.get(url)
        response.close()


def i2c_scan():
    devices = i2c.scan()
    if devices:
        for device_address in devices:
            print(f'{device_address:02x}')
    else:
        print("No")


def bmp_data(temperature=True, pressure=True, altitude=True):
    if temperature:
        print(bmp.temperature)
    if pressure:
        print(bmp.pressure)
    #if altitude:
    #    print(bmp.altitude)
    print('')


def adc2volt(adcval):
    return (adcval*(1/20008))-(42.143/20008)


def hall_magnet():
    global magnet
    hall_voltage = adc2volt(adc0.read_u16())
    if hall_voltage > 3:
        magnet = True
        pole = 'A'
    elif hall_voltage < 2.7 and hall_voltage > 0.6:
        magnet = False
        pole = 'N/A'
    elif hall_voltage < 0.3:
        magnet = True
        pole = 'B'
    else:
        magnet = False
        pole = 'N/A'
    return f'{magnet}, Pole {pole} ({hall_voltage}V)'


# Modes
# 0: Default
# 1: Error
# 2: Resolution
# 3: "Fuel Gauge"
# 4: Noise vs. Interference
# 5: Sensitivity
# 6: Saturation
# 7: Default No Wi-Fi

mode = 4

#i2c_scan()
#connect_to_wifi()
while True:
    if mode == 0:
        thingspeak_write(adc2volt(adc0.read_u16()), 'field1')
        servo.set_angle(0, potentiometer.get_servo_angle())
        servo.set_angle(1, 180-potentiometer.get_servo_angle())
    elif mode == 1:
        meas_val = potentiometer.get_servo_angle()
        servo.set_angle(0, meas_val)
        true_val = potentiometer.get_servo_angle() + random.randint(-5, 5)
        error = ((meas_val-true_val)/true_val)*100
        servo.set_angle(1, error+90)
    elif mode == 2:
        high_res = potentiometer.get_servo_angle()
        servo.set_angle(0, high_res)
        low_res = round(high_res/30)*30
        servo.set_angle(1, low_res)
    elif mode == 3:
        normal = potentiometer.get_servo_angle()
        servo.set_angle(0, normal)
        fuel = normal
        if normal >= 90:
            fuel = normal
        elif normal >= 45:
            fuel = (2*normal)-90
        elif normal < 45:
            fuel = 0
        servo.set_angle(1, fuel)
    elif mode == 4:
        noisy = potentiometer.get_servo_angle() + random.randint(-5, 5)
        servo.set_angle(0, noisy)
        intfs = potentiometer.get_servo_angle() + ((math.sin(time.ticks_us()/100000))*10)
        servo.set_angle(1, intfs)
    elif mode == 5:
        normal = potentiometer.get_servo_angle()
        servo.set_angle(0, normal)
        if potentiometer.get_servo_angle()*2 <= 180:
            sensitive = potentiometer.get_servo_angle()*2
        else:
            sensitive = 180
        servo.set_angle(1, sensitive)
    elif mode == 6:
        normal = potentiometer.get_servo_angle()
        servo.set_angle(0, normal)
        saturation = normal
        if potentiometer.get_servo_angle() <= 90:
            sautration = potentiometer.get_servo_angle()
        else:
            saturation = 90
        servo.set_angle(1, saturation)
    elif mode == 7:
        servo.set_angle(0, potentiometer.get_servo_angle())
        servo.set_angle(1, 180-potentiometer.get_servo_angle())
        
