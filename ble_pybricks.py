""" ble_pybricks.py

Use this file to read datavalues from advertisement data sent
from a LEGO hub which runs on Pybricks.

Author: Kees Smit
Version: 1.00
Date: 23-03-2024
"""
import ustruct

# Public methods

def check_lego_manufacturer_id(adv_data) -> bool:
    """ Check for LEGO manufacturer ID in advertisement data."""
    try:
        if adv_data[2] == 151 and adv_data[3] == 3:
            return True
        else:
            return False
    except IndexError:
        return False

def get_list_of_values(adv_data):
    """Retrieve all data values from advertisement data."""
    values = []
    len_adv_data = int(adv_data[0] + 1)
    index = 5
    while index < len_adv_data:
        data_type, data_size = _get_data_type_and_size(adv_data[index])
        if data_type == 0:
            # Only one data object, read next item for type and size
            index += 1
        elif data_type == 1:
            # Data type boolean with value True
            values.append(True)
            index += 1
        elif data_type == 2:
            # Data type boolean with value False
            values.append(False)
            index += 1
        else:
            # Data type int, float, str or bytes
            start = index + 1
            end = start + data_size
            values.append(_get_value(data_type, data_size, adv_data[start:end]))
            index += data_size + 1
    return values

# Private methods

def _get_data_type_and_size(value):
    """Get data and size of datavalue."""
    packed_value = ustruct.pack('<B', value)
    type = packed_value[0] >> 5
    size = packed_value[0] & 0x1F
    return type, size

def _get_value(data_type, data_size, data):
    """Unpack datavalue from advertisement data."""
    value = None
    if data_type == 3:
        # int
        if data_size == 1:
            value = ustruct.unpack('<b', data)[0]
        elif data_size == 2:
            value = ustruct.unpack('<h', data)[0]
        elif data_size == 4:
            value = ustruct.unpack('<i', data)[0]
    elif data_type == 4:
        # float (length is always 4)
        value = ustruct.unpack('f', data)
    elif data_type == 5:
        # str
        value = ustruct.unpack(str(data_size)+'s', data)[0].decode()
    elif data_type == 6:
        # bytes
        value = ustruct.unpack(str(data_size)+'s', data)
    return value
