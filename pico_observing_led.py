""" pico_observer_led.py

Sample application to test reading advertismentdata from LEOG hub.
Run this script on your Rapsberry Pi Pico.
Use with script hub_advertiser_led.py on your LEGO hub.

Pico setup:
- connect LED to pin GP15. Don't forget to add a resistor to the circuit.
- Upload file ble_pybricks.py together with this file to your Pico.

LEGO Hub setup:
- Make shure your LEGO hub is running Pybricks.
- Attach motor to port A.
- Attach a technic beam to the motor to make it easy to turn manualy.

Usage:
- start script hub_advertiser_led.py on your LEGO hub.
- start script pico_observer_led.py on your Pico.
- Turn motor A on your LEGO hub to adjust the brightness of the led.
"""

import bluetooth
import machine
import ustruct
from micropython import const

from ble_pybricks import check_lego_manufacturer_id, get_list_of_values


_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)

#event handler function
def bt_irq(event, data):
    global receivedNumber, dataReceivedFlag, led_value
    values = []
    if _IRQ_SCAN_RESULT:
        # A single scan result.
        addr_type, addr, adv_type, rssi, adv_data = data
        address = bytes(addr)
        if check_lego_manufacturer_id(adv_data) and not dataReceivedFlag:
            values = get_list_of_values(adv_data)
            led_value = values[0]
            print(led_value)
            receivedNumber=ustruct.unpack('<i',bytes(adv_data))[0]
            dataReceivedFlag = True
    elif event == _IRQ_SCAN_DONE:
        print('scan finished.')

ble = bluetooth.BLE()
ble.active(True)
ble.irq(bt_irq)

led15 = machine.PWM(machine.Pin(15))
led15.freq(1000)

scanDuration_ms = 0   # 0 means indefenitely
interval_us = 100     # Interval 100ms is Pybricks condition
window_us = 100       # The same window as interval, means continuous scan
active = False        # Do not care for a reply for a scan from the transmitter

receivedNumber = 0
dataReceivedFlag = False
led_value = 0
ble.gap_scan(scanDuration_ms, interval_us, window_us, active)

f = 65535 / 360

while True:
    if dataReceivedFlag:
        # print(receivedNumber)
        dataReceivedFlag = False
    if led_value < 0:
        led_value = 0
    led15.duty_u16(int(f*led_value))