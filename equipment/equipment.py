
import pyvisa
from pyvisa.resources.resource import Resource
from pyvisa.errors import VisaIOError

from functools import wraps

from abc import ABC, abstractmethod

from time import sleep

from math import isnan
    
EQUIPMENT_TIMEOUT = 500

def visa_io(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        for i in range(2):
            try:
                response = func(*args, **kwargs)
                if response is None:
                    # return None
                    continue
                if not isnan(response):
                    return response
            # Continue retrying if an error happens
            except (TypeError, ValueError, VisaIOError, Exception) as e:
                print(f'Retry #{i} Waived Exception: {e}')
                if i == 1:
                    return None
            sleep(0.1)
        return None
    return wrapped

# depends on the equipment base class
class Equipment(ABC):
    def __init__(self, device, device_id):

        # Get the individual fields on the device ID
        manufacturer, model_num, serial_num, fw_version = self.split_device_id(device_id)

        # Equipment Details
        self.device_id = device_id
        self.manufacturer:str = manufacturer
        self.model:str = model_num
        self.serial:str = serial_num
        self.fw_version = fw_version

        # VISA Resource
        self.device:Resource = device
        self.device.timeout = EQUIPMENT_TIMEOUT

    def get_id(self):
        return self.write("*IDN?")
    
    def split_device_id(self, device_id):
        """ Returns a list of the individual parameters of the device ID
        
        manufacturer, model, serial, fw_version
        """
        return device_id.split(',',4)[:4]

    def __repr__(self):
        """ Return the Manufacturer, Model, Serial and firmware
        """
        return self.device_id


    def close(self):
        """ Close the VISA resource to disable further communication
        """
        self.device.close()

    
    def write(self, command):
        """ Send a write command and get a reply if needed
        
        """
        response = None
        reply_available = False # CDO
        try:
            if "BDMM" in command: # CDO
                reply_available = True
                command = command.split(':')[1]

            if "?" in command:
                response = self.device.query(command).strip()
            else:
                self.device.write(command)

            if reply_available: # CDO
                self.device.read()
                reply_available = False

        except Exception as e:
            print(f"Error when writing {command} to {self.device_id}")
            raise e

        return response
    




if __name__ == '__main__':
    pass
