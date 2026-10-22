from equipment.equipment import Equipment
from equipment.dc_source_specs import *
from equipment.definitions import DC_SOURCE_LIST

from time import sleep

class DC_SOURCE_STATUS:
    OFF = 0
    ON = 1


HMP_MANUAL_CHANNEL_COUNT = 3

_MAGNA_MODEL_PREFIXES = ('SL', 'TSD', 'TS', 'XR')


def is_magna_hvdc(dc) -> bool:
    """True for Magna-Power primary HV DC supplies (SL, TSD, etc.)."""
    if dc is None:
        return False
    man = (getattr(dc, 'manufacturer', '') or '').upper()
    if 'MAGNA' in man:
        return True
    m = (getattr(dc, 'model', '') or '').strip().upper()
    return any(m.startswith(p) for p in _MAGNA_MODEL_PREFIXES)


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

    def is_hmp_series(self) -> bool:
        return (getattr(self, 'model', '') or '').strip().upper().startswith('HMP')

    def select_channel(self, channel: int):
        if not self.is_hmp_series():
            return
        ch = int(channel)
        if ch < 1 or ch > HMP_MANUAL_CHANNEL_COUNT:
            raise ValueError(f'HMP channel must be 1..{HMP_MANUAL_CHANNEL_COUNT}')
        nsel = getattr(self.dc_source_object, 'inst_nsel', 'INSTrument:NSEL')
        self.write(f'{nsel} {ch}')

    def channel_set_voltage(self, channel: int, voltage: float):
        self.select_channel(channel)
        self.voltage = voltage

    def channel_set_current_limit(self, channel: int, current_a: float):
        self.select_channel(channel)
        self.set_current_limit(current_a)

    def channel_turn_on(self, channel: int):
        self.select_channel(channel)
        self.turn_on()

    def channel_turn_off(self, channel: int):
        self.select_channel(channel)
        self.turn_off()

    def channel_update_status(self, channel: int) -> int:
        self.select_channel(channel)
        self.update_status()
        return self.output_status

    def cleanup(self):
        self.turn_off()
        self.close()
