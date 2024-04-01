""" pico_advertising_target_speed.py

Sample application to test sending advertisment data to LEGO hub.
Run this script on your Rapsberry Pi Pico.
Use with script hub_observing_target_speed.py on your LEGO hub.

Pico setup:
- connect potentiometer for adjusting speed on pin GP26/ADC0.
- conned potentiometer for adjusting target on pin GP27/ADC1.

LEGO Hub setup:
- Make shure your LEGO hub is running Pybricks.
- Attach motor to port A.
- Attach motor to port B.

Usage:
- start script hub_observing_target_speed.py on your LEGO hub.
- start script pico_advertising_target_speed.py on your Pico.
- Turn speed potentiometer to adjust the speed of motor A on your hub.
- Turn target potentiometer to adjust the target angle for motor B.

For explanation of constructing the advertisment data see:
https://github.com/pybricks/technical-info/blob/master/pybricks-ble-broadcast-observe.md
"""

import bluetooth
import machine
import time
import ustruct


ble = bluetooth.BLE()
ble.active(True)

# Potentiometers for adjusting speed and target
pm_speed = machine.ADC(26)
pm_target = machine.ADC(27)

# We use a factor for each potentiometer to scale its range to
# the range of the LEGO motor. For speed we want adjust the
# motor between zero and maximum speed (900), for the target
# angle we want to use the range 0 to 180 degrees.
factor_speed = 900 / 65535
factor_target = 180 / 65535

while True:
    
    # BLE advertising channel 1: speed
    speed = int(factor_speed * pm_speed.read_u16())
    payload_speed = b'\x08\xFF\x97\x03\x01\x00\x62' + ustruct.pack('<h', speed)
    ble.gap_advertise(100, adv_data=payload_speed, resp_data=None, connectable=False)
    time.sleep_ms(10)

    # BLE advertising channel 2: target
    target = int(factor_target * pm_target.read_u16())
    payload_target = b'\x08\xFF\x97\x03\x02\x00\x62' + ustruct.pack('<h', target)
    ble.gap_advertise(100, adv_data=payload_target, resp_data=None, connectable=False)
    time.sleep_ms(10)
