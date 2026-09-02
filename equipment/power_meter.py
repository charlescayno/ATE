from equipment.equipment import Equipment, visa_io
from equipment.power_meter_specs import *
from equipment.definitions import POWER_METER_LIST
from time import sleep, time

import pyvisa
import numpy as np

class IntegType:
    NORMAL = 0
    CONTINUOUS = 1

class PowerMeter(Equipment):
    def __init__(self, device, device_id):
        super().__init__(device, device_id)
        
        self.device_id = device_id
        self.device = device
        
        self.unpack_power_meter_specs()

        self._voltage = 0
        self._current = 0
        self._power = 0
        self._pf = 0
        self._thd = 0
        

        self._integration_mode = "NORMAL"
        self._integration_time = 0
        self._current_range = 0
        self._voltage_range = 0
        self._integration_status = None
        self._integration_done = False
        self._current_auto_range_status = False
        self._voltage_auto_range_status = False
        self._averaging_status = False
        
        last = self.device.resource_name.rfind("::")
        addr = self.device.resource_name[:last]
        self.description = f'{self.manufacturer} {self.model} {addr}'
        self.voltage_range_max = 0
        self.current_range_max = 0

        self.set_preset()
        self.query_averaging_state()
        self.stop_integration()
        self.reset_integration()
        self.auto_range_enable()
        


    def set_preset(self):
        self.power_meter_object.set_preset()# TODO: Fix for WT3XX 

    def update_basic_params(self):
        # Update later with better code
        # Updates all the parameters
        try:
            _ = self.voltage
            _ = self.current
            _ = self.power
            _ = self.pf
        except Exception as e:
            pass
        # _ = self.thd
    
    @visa_io
    def integrate(self, integration_time=60):
        self.power_meter_object.integrate(integration_time)

    def integration_settings(self, mode:str, timer_s:int, reset=True):
        """ Sets the integration parameters of the Power Meter. 
        Resets the integration 

        Keyword Arguments:
        mode        --      Either NORMAL or Continuous
        timer       --      Tuple of (hhhh, mm, ss)
        """
        try:
            self.set_integration_mode(mode)
            self.set_integration_timer(timer_s)
            self.stop_integration()
            self.reset_integration()
            self.get_integration_timer()
        except Exception as e:
            raise e    
    
    @visa_io   
    def set_integration_mode(self, integ_mode:str = 'NORMAL'):
        """ Sets the integration parameters of the Power Meter. 
        
        Keyword Arguments:
        mode        --      Either NORMAL or Continuous
        """
        
        self.power_meter_object.set_integration_mode(integ_mode)
        self._integration_mode = integ_mode
        

    @visa_io
    def set_integration_timer(self, timer_s:int):
        """ Sets the integration timer of the power meter.

        Keyword Argument:
        timer_s     --      value of the timer in seconds
        """

        self.power_meter_object.set_integration_timer(timer_s)
        self._integration_time = timer_s
    
    @visa_io
    def get_integration_timer(self):
        """ Returns the integration timer value in seconds"""
        
        time_s = self.power_meter_object.get_integration_timer()
        return time_s

    def start_integration(self):
        try:
            self.query_averaging_state()
            self.current_auto_range_query()
            self.voltage_auto_range_query()
            self.reset_integration()
            self.power_meter_object.start_integration()
        except Exception as e:
            raise e
    
    @visa_io
    def stop_integration(self):
        self.power_meter_object.stop_integration()

    @visa_io
    def reset_integration(self):
        self.power_meter_object.reset_integration()
    
    @visa_io
    def poll_integration_status(self):
        self.power_meter_object.poll_integration_status()
        self._integration_done = self.power_meter_object._integration_done
        self._integration_status = self.power_meter_object._integration_status

    @visa_io
    def get_integrated_power(self, reset = True):
        """Returns the power equivalent of the total integrated energy"""
        power = self.power_meter_object.get_integrated_power(reset)
        self.voltage_auto_range_enable(self._voltage_auto_range_status)
        self.current_auto_range_enable(self._current_auto_range_status)
        self.enable_averaging(self._averaging_status)
        return power

    @property
    @visa_io
    def voltage(self):
        self._voltage = self.power_meter_object.voltage
        return self._voltage
        
    @property
    @visa_io
    def current(self):
        self._current = self.power_meter_object.current
        return self._current


    @property
    @visa_io
    def power(self):
        self._power = self.power_meter_object.power
        return self._power

    @property
    @visa_io
    def pf(self):
        self._pf = self.power_meter_object.pf
        return self._pf

    @property
    @visa_io
    def thd(self):
        self._thd = self.power_meter_object.thd
        return self._thd
    
    @visa_io
    def get_current_range(self):
        self._current_range = self.power_meter_object.get_current_range()
        return self._current_range

    @visa_io
    def set_current_range(self, amps = None):
        self.power_meter_object.set_current_range(amps)
        self.get_current_range()
        
    @visa_io
    def set_current_range_max(self):
        self.power_meter_object.set_current_range_max()
        self.get_current_range()
        
    @visa_io
    def get_voltage_range(self):
        self._voltage_range = self.power_meter_object.get_voltage_range()
        return self._voltage_range

    @visa_io
    def set_voltage_range(self, volts = None):
        self.power_meter_object.set_voltage_range(volts)
        self.get_voltage_range()
    
    @visa_io
    def set_voltage_range_max(self):
        self.power_meter_object.set_current_range_max()
        self.get_voltage_range()

    @visa_io
    def auto_range_enable(self, en:bool=True):
        self.get_current_range()
        self.get_voltage_range()
        if en:
            self.set_current_range_max()
            self.set_voltage_range_max()
        else:
            self.set_current_range(self._current_range)
            self.set_current_range(self._current_range)
        self.power_meter_object.auto_range_enable(en)
        self.current_auto_range_query()
        self.voltage_auto_range_query()

    @visa_io
    def current_auto_range_enable(self, en:bool=True):
        self.get_current_range()
        if not en:
            self.set_current_range(self._current_range)
        self.power_meter_object.current_auto_range_enable(en)
        self.current_auto_range_query()
    
    @visa_io
    def current_auto_range_query(self):
        self._current_auto_range_status = self.power_meter_object.current_auto_range_query()
        return self._current_auto_range_status
    
    @visa_io
    def current_auto_range_toggle(self):
        self.power_meter_object.current_auto_range_toggle()
        self.current_auto_range_query()

    @visa_io
    def voltage_auto_range_enable(self, en:bool=True):
        self.get_voltage_range()
        if not en:
            self.set_voltage_range(self._voltage_range)
        self.power_meter_object.voltage_auto_range_enable(en)
        self.voltage_auto_range_query()

    @visa_io
    def voltage_auto_range_query(self):
        self._voltage_auto_range_status = self.power_meter_object.voltage_auto_range_query()
        return self._voltage_auto_range_status  

    @visa_io
    def voltage_auto_range_toggle(self):
        self.power_meter_object.voltage_auto_range_toggle()
        self.voltage_auto_range_query()

    @visa_io
    def auto_range_query(self):
        v_auto = self.power_meter_object.voltage_auto_range_query()
        i_auto = self.power_meter_object.current_auto_range_query()
        auto_range_status = v_auto and i_auto

        return auto_range_status
    
    @visa_io
    def auto_range_toggle(self):
        self.current_auto_range_query()
        self.voltage_auto_range_query()

        self.voltage_auto_range_enable(not self._voltage_auto_range_status)
        self.current_auto_range_enable(not self._current_auto_range_status)

    @visa_io
    def enable_averaging(self, en:bool=True):
        self.power_meter_object.enable_averaging(en)
        self.query_averaging_state()
    
    @visa_io
    def query_averaging_state(self):
        self._averaging_status = self.power_meter_object.query_averaging_state()
        return self._averaging_status

    @visa_io
    def averaging_toggle(self):
        self.power_meter_object.averaging_toggle()
        self.query_averaging_state()

    def get_harmonics(self):
        harmonic_content, percent_content = self.power_meter_object.get_harmonics()
        return harmonic_content, percent_content

    @visa_io
    def reset(self):
        self.power_meter_object.reset()
    
    def unpack_power_meter_specs(self):
        model = self.model

        power_meter_model = POWER_METER_LIST[model]

        # create an instance of the specified ac source model to use its specs
        self.power_meter_object: PowerMeterBaseClass = power_meter_model(self.device, self.device_id)

    def cleanup(self):
        self.close()
        
    
