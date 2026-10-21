from equipment.equipment import Equipment
from equipment.dc_source_specs import *
from equipment.definitions import DC_SOURCE_LIST

from time import sleep

class DC_SOURCE_STATUS:
    OFF = 0
    ON = 1


def _resolve_dc_source_model(model: str):
    key = (model or '').strip()
    if key in DC_SOURCE_LIST:
        return DC_SOURCE_LIST[key]
    if model in DC_SOURCE_LIST:
        return DC_SOURCE_LIST[model]
    raise KeyError(f'Unknown DC source model {model!r}')


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
        try:
            status_ret = self.write(f'{self.command_output}:{self.command_state}?')
        except Exception:
            return
        if status_ret in ['1', 'ON']:
            self.output_status = DC_SOURCE_STATUS.ON
        elif status_ret in ['0', 'OFF']:
            self.output_status = DC_SOURCE_STATUS.OFF
        
    def turn_on(self):
        print(f"[DC_SOURCE] {self.description}: Output ON")
        self.write(f'{self.command_output_on}')
        self.output_status = DC_SOURCE_STATUS.ON
        self.update_status()

    def turn_off(self):
        print(f"[DC_SOURCE] {self.description}: Output OFF")
        self.write(f'{self.command_output_off}')
        self.output_status = DC_SOURCE_STATUS.OFF
        self.update_status()
    
    def set_voltage_with_coupling(self,voltage,coupling):
        # Added function just for convenience in programming when using either ac source or dc source during ATE
        self.voltage = voltage

    def set_current_limit(self, current_a: float):
        self.current = current_a
        
    def turn_sequence(self,state=DC_SOURCE_STATUS.OFF):
        try:
            if state == DC_SOURCE_STATUS.OFF:
                self.write(f'{self.command_sequence} OFF')
            else:
                self.write(f'{self.command_sequence} ON')
        except Exception:
            pass
            
    @property
    def voltage(self):
        self._voltage = float(self.write(f'{self.command_measure}:{self.command_volt}?'))
        return self._voltage

    @property
    def current(self):
        self._current = float(self.write(f'{self.command_measure}:{self.command_curr}?'))
        return self._current
    
    @voltage.setter
    def voltage(self, voltage):
        self._voltage = float(voltage)
        cmd = getattr(self.dc_source_object, 'set_volt', None) or self.command_volt
        print(f"[DC_SOURCE] {self.description}: Set Voltage to {self._voltage:.3f} V")
        self.write(f'{cmd} {self._voltage}')
    
    @current.setter
    def current(self, current):
        self._current = float(current)
        cmd = getattr(self.dc_source_object, 'set_curr', None) or self.command_curr
        print(f"[DC_SOURCE] {self.description}: Set Current limit to {self._current:.3f} A")
        self.write(f'{cmd} {self._current}')
        
    def unpack_dc_source_specs(self):
        dc_source_model = _resolve_dc_source_model(self.model)
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
