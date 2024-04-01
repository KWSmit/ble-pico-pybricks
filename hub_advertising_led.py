""" hub_advertising_led.py

Sample script for advertising data through Bluetooth BLE advertising.
Use this file on your LEGO hub in combination with the file
pico_observing_led.py on your Raspberry Pi Pico.

Hub setup:
- Make sure your hub runs pybricks.
- Connect a motor to port A.
- Put this file together with the file ble_pybricks.py on your hub.

Usage:
- start script hub_advertising_led.py on your LEGO hub.
- start script pico_observing_led.py on your Pico.
- Turn the motor manually to adjust the brightness of the led on your Pico.
"""

from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

hub = TechnicHub(broadcast_channel=0)
motor_a = Motor(Port.A)

while True:
    data = motor_a.angle()
    hub.ble.broadcast(data)
    wait(10)
