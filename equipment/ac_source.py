from equipment.equipment import Equipment
from equipment.ac_source_specs import *
from equipment.definitions import AC_SOURCE_LIST

from time import sleep

class AC_SOURCE_STATUS:
    OFF = 0
    ON = 1

class AC_SOURCE_COUPLING:
    AC = 'AC'
    DC = 'DC'

class ACSource(Equipment):
    def __init__(self, device, device_id):
        super().__init__(device, device_id)
        
        self.device_id = device_id
        self.device = device
        
        self.unpack_ac_source_specs()
        
        self._voltage:float = 0
        self._offset:float = 0
        self._frequency:float = 0
        self._coupling:str = AC_SOURCE_COUPLING.AC
        self.output_status = AC_SOURCE_STATUS.OFF

        self.generate_description()
    
    def generate_description(self):
        self.description = f"{self.manufacturer} {self.model} {self.serial}"

    def update_status(self):
        status_ret = self.write(f'{self.command_output}:{self.command_state}?')
        if status_ret in ['1', 'ON']:
            self.output_status = AC_SOURCE_STATUS.ON
        elif status_ret in ['0', 'OFF']:
            self.output_status = AC_SOURCE_STATUS.OFF
        
    def turn_on(self):
        # if self._coupling == AC_SOURCE_COUPLING.AC:
            # self._offset = 0
            # self.write(f'{self.command_volt_dc} {self._offset}')
        # self.write(f'{self.command_volt_ac} {self._voltage}')
        # self.write(f'{self.command_coupling} {self._coupling}')
        # self.write(f'{self.command_volt_dc} {self._offset}')
            
        self.write(f'{self.command_output} ON')

    def turn_off(self):
        self.write(f'{self.command_output} OFF')

    def set_freq(self, voltage):
        if voltage >= 180 and voltage <= 265: ac_freq = 50
        else: ac_freq = 60
        return ac_freq

    @property
    def voltage(self):
        return self._voltage
    
    @property
    def offset(self):
        return self._offset

    @property
    def frequency(self):
        return self._frequency
    
    @property
    def coupling(self):
        return self._coupling
    
    @property
    def ac_slew_rate(self):
        return self._ac_slew_rate
    
    @property
    def dc_slew_rate(self):
        return self._dc_slew_rate
    
    @property
    def freq_slew_rate(self):
        return self._freq_slew_rate
    
    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.write(f'{self.command_volt_ac} {self._voltage}')
    
    @offset.setter
    def offset(self, offset):
        self._offset = offset
        self.write(f'{self.command_volt_dc} {self._offset}')

    @frequency.setter
    def frequency(self, frequency):
        self._frequency = frequency # manual setting
        self.write(f'{self.command_freq} {self._frequency}')

    @coupling.setter
    def coupling(self, type):
        self._coupling = type.upper()
        self.write(f'{self.command_coupling} {self._coupling}')
    
    @ac_slew_rate.setter
    def ac_slew_rate(self, slew):
        self._ac_slew_rate = slew
        self.write(f'{self.command_volt_ac_slew_rate} {self._ac_slew_rate}')
        
    @dc_slew_rate.setter
    def dc_slew_rate(self, slew):
        self._dc_slew_rate = slew
        self.write(f'{self.command_volt_dc_slew_rate} {self._dc_slew_rate}')
        
    @freq_slew_rate.setter
    def freq_slew_rate(self, slew):
        self._freq_slew_rate = slew
        self.write(f'{self.command_freq_slew_rate} {self._freq_slew_rate}')
        
    def set_voltage_with_coupling(self,voltage,coupling):
        if type(self.ac_source_object) is ACSourceIT7800:
            if coupling == AC_SOURCE_COUPLING.DC:
                if not self.coupling == AC_SOURCE_COUPLING.DC:
                    # Remove AC component first before setting DC voltage
                    self.voltage = 0
                self.coupling = coupling
                self.offset = voltage
                
            else:
                if not self.coupling == AC_SOURCE_COUPLING.AC:
                    # Remove DC componnent first before setting AC voltage
                    self.offset = 0
                self.coupling = coupling
                self.voltage = voltage
        else:
            if coupling == AC_SOURCE_COUPLING.DC:
                # Remove AC component first before setting DC voltage
                self.voltage = 0
                self.offset = voltage
                
            else:
                # Remove DC componnent first before setting AC voltage
                self.offset = 0
                self.voltage = voltage
                
            self.coupling = coupling

    # def ac_cycling(self, pulse_count, vin, start_soak, off_time, on_time, end_soak):
    
    #     freq = self.set_freq(vin)
    #     self.write(f"TRIG:TRAN:SOUR BUS")
        
    #     a = f"LIST:DWELL {start_soak}, "
    #     for i in range(pulse_count):
    #         a = a + f"{off_time}, {on_time}, "
    #     a = a + f"{off_time}, {end_soak}"
    #     # print(a)
    #     self.write(f"{a}")

    #     self.write(f"VOLT:MODE LIST")
        
    #     b = f"LIST:VOLT {vin}, "
    #     for i in range(pulse_count):
    #         b = b + f"0, {vin}, "
    #     b = b + f"0, {vin}"
    #     # print(b)
    #     self.write(b)

    #     self.write(f"VOLT:SLEW:MODE LIST")

    #     c = f"LIST:VOLT:SLEW 9.9e+037, "
    #     for i in range(pulse_count):
    #         c = c + f"9.9e+037, 9.9e+037, "
    #     c = c + f"9.9e+037, 9.9e+037"
    #     # print(c)
    #     self.write(c)

    #     self.write(f"FREQ:MODE LIST")
    #     d = f"LIST:FREQ {freq}, "
    #     for i in range(pulse_count):
    #         d = d + f"{freq}, {freq}, "
    #     d = d + f"{freq}, {freq}"
    #     # print(d)
    #     self.write(d)

    #     self.write(f"FREQ:SLEW:MODE LIST")

    #     e = f"LIST:FREQ:SLEW 9.9e+037, "
    #     for i in range(pulse_count):
    #         e = e + f"9.9e+037, 9.9e+037, "
    #     e = e + f"9.9e+037, 9.9e+037"
    #     # print(e)
    #     self.write(e)

    #     self.write(f"VOLT:OFFS:MODE FIX")
    #     self.write(f"VOLT:OFFS:SLEW:MODE FIX")
    #     self.write(f"PHAS:MODE LIST")

    #     f = f"LIST:PHAS 270, "
    #     for i in range(pulse_count):
    #         f = f + f"270, 270, "
    #     f = f + f"270, 270"
    #     # print(f)
    #     self.write(f)

    #     self.write(f"CURR:PEAK:MODE LIST")

    #     g = f"LIST:CURR 40.4, "
    #     for i in range(pulse_count):
    #         g = g + f"40.4, 40.4, "
    #     g = g + f"40.4, 40.4"
    #     # print(g)
    #     self.write(g)

    #     self.write(f"FUNC:MODE FIX")

    #     h = f"LIST:TTLT ON, "
    #     for i in range(pulse_count):
    #         h = h + f"OFF, OFF, "
    #     h = h + f"OFF, OFF"
    #     # print(h)
    #     self.write(h)

    #     self.write(f"LIST:STEP AUTO")
    #     self.write(f"OUTP:TTLT:STAT ON")
    #     self.write(f"OUTP:TTLT:SOUR LIST")
    #     self.write(f"TRIG:SYNC:SOUR PHASE")
    #     self.write(f"TRIG:SYNC:PHAS 0.0")
    #     self.write(f"TRIG:TRAN:DEL 0")
    #     self.write(f"Sens:Swe:Offs:Poin 0")
    #     self.write(f"TRIG:ACQ:SOUR TTLT")
    #     self.write(f"INIT:IMM:SEQ3")
    #     self.write(f"LIST:COUN 1")
    #     self.write(f"INIT:IMM:SEQ1")
    #     self.write(f"TRIG:TRAN:SOUR BUS")
    #     self.write(f"TRIG:IMM")

    #     delay = start_soak + end_soak + (pulse_count*(off_time + on_time)) + off_time
    #     sleep(delay)

    def unpack_ac_source_specs(self):
        # Take the model number
        model = self.model

        ac_source_model = AC_SOURCE_LIST[model]

        # create an instance of the specified ac source model to use its specs
        self.ac_source_object: ACSourceBaseClass = ac_source_model()
        
        self.command_volt_ac = self.ac_source_object.volt_ac
        self.command_volt_dc = self.ac_source_object.volt_dc
        self.command_freq = self.ac_source_object.freq
        self.command_coupling = self.ac_source_object.coupling
        self.command_output = self.ac_source_object.output
        self.command_state = self.ac_source_object.state
        self.command_shape = self.ac_source_object.shape
        self.command_volt_ac_slew_rate = self.ac_source_object.volt_ac_slew_rate
        self.command_volt_dc_slew_rate = self.ac_source_object.volt_dc_slew_rate
        self.command_freq_slew_rate = self.ac_source_object.freq_slew_rate
        
    
    def cleanup(self):
        self.turn_off()
        self.close()
