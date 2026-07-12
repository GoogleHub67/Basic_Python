# ruff: noqa
# pylint: disable=import-error, no-name-in-module, wrong-import-order, undefined-variable
# pyright: reportMissingImports=false
# flake8: noqa

from machine import Pin, PWM
import time
import utime

trig = Pin(12, Pin.OUT)
echo = Pin(13, Pin.IN)
servo = PWM(Pin(10))
servo.freq(50)

def distance():
    trig.off()
    utime.sleep_us(2)
    trig.on()
    utime.sleep_us(10)
    trig.off()
    for i in range(40):
        if echo.value():
            break
    pulse_len = time.ticks_us()
    while echo.value():
        pass
    pulse_len = time.ticks_diff(time.ticks_us(), pulse_len)
    return (pulse_len * 0.034) / 2

while True:
    dist = distance()
    if dist < 30:
        servo.duty_u16(5000)  # Closed
        utime.sleep(0.5)
        servo.duty_u16(10000) # Open ~90°
        utime.sleep(3)
        servo.duty_u16(5000)  # Close
    utime.sleep(0.5)