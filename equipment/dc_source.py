from equipment.equipment import Equipment
from equipment.dc_source_specs import *
from equipment.definitions import DC_SOURCE_LIST

from time import sleep

class DC_SOURCE_STATUS:
    OFF = 0
    ON = 1


class DCSource(Equipment):
    def __init__(self, device, device_id):
        super().__init__(device, device_id)
        
        self.device_id = device_id
        self.device = device
        
        self.unpack_dc_source_specs()
        
        self._voltage:float = 0
        self._current:float = 0
        self.output_status = DC_SOURCE_STATUS.OFF

        self.generate_description()
        self.update_status()
        # Turn off sequence mode
        self.turn_sequence()
    
    def generate_description(self):
        self.description = f"{self.manufacturer} {self.model} {self.serial}"

    def update_status(self):
        status_ret = self.write(f'{self.command_output}:{self.command_state}?')
        if status_ret in ['1', 'ON']:
            self.output_status = DC_SOURCE_STATUS.ON
        elif status_ret in ['0', 'OFF']:
            self.output_status = DC_SOURCE_STATUS.OFF
        
    def turn_on(self):            
        self.write(f'{self.command_output_on}')

    def turn_off(self):
        self.write(f'{self.command_output_off}')
    
    def set_voltage_with_coupling(self,voltage,coupling):
        # Added function just for convenience in programming when using either ac source or dc source during ATE
        self.voltage = voltage
        
    def turn_sequence(self,state=DC_SOURCE_STATUS.OFF):
        if state == DC_SOURCE_STATUS.OFF:
            self.write(f'{self.command_sequence} OFF')
        else:
            self.write(f'{self.command_sequence} ON')
            
    @property
    def voltage(self):
        self._voltage = self.write(f'{self.command_measure}:{self.command_volt}?')
        return self._voltage

    @property
    def current(self):
        self._current = self.write(f'{self.command_measure}:{self.command_curr}?')
        return self._current
    
    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.write(f'{self.command_volt} {self._voltage}')
    
    @voltage.setter
    def current(self, current):
        self._current = current
        self.write(f'{self.command_curr} {self._current}')
        
    def unpack_dc_source_specs(self):
        # Take the model number
        model = self.model

        dc_source_model = DC_SOURCE_LIST[model]

        # create an instance of the specified ac source model to use its specs
        self.dc_source_object: DCSourceBaseClass = dc_source_model()
        
        self.command_output_on = self.dc_source_object.output_on
        self.command_output_off = self.dc_source_object.output_off
        self.command_measure = self.dc_source_object.measure
        self.command_volt = self.dc_source_object.volt
        self.command_curr = self.dc_source_object.curr
        self.command_output = self.dc_source_object.output
        self.command_state = self.dc_source_object.state
        self.command_sequence = self.dc_source_object.sequence

    def cleanup(self):
        self.turn_off()
        self.close()
