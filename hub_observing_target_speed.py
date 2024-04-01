""" hub_observing_target_speed.py

Sample script for receiving data through Bluetooth BLE advertising.
Use this file on your LEGO hub in combination with the file
pico_advertising_target_speed.py on your Raspberry Pi Pico.

Hub setup:
- Make sure your hub runs pybricks.
- Connect a motor to port A.
- Connect a motor to port B.

Usage:
- start script hub_observing_target_speed.py on your LEGO hub.
- start script pico_advertising_target_speed.py on your Pico.
- Turn speed potentiometer on the Pico to adjust the speed of motor A.
- Turn target potentiometer on the Pico to adjust the target angle for motor B.
"""

from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port

hub = TechnicHub(observe_channels=[1,2])
motor_a = Motor(Port.A)
motor_b = Motor(Port.B)

while True:
    # Read speed on channel 1
    speed = hub.ble.observe(1)
    if speed:
        motor_a.run(speed=speed)
    else:
        motor_a.stop()

    # Read target angle on channel 2
    target = hub.ble.observe(2)
    if target:
        motor_b.run_target(speed=200, target_angle=target)
