from equipment.equipment import Equipment, visa_io
from time import sleep, time
from PySide2.QtCore import QTimer
import re

def parse_float_response(val, default=0.0):
    """Safely parse float response from power meter SCPI strings."""
    if val is None:
        return default
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).strip()
    try:
        return float(val_str)
    except ValueError:
        matches = re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?', val_str)
        if matches:
            try:
                return float(matches[-1])
            except ValueError:
                pass
        return default

class PowerMeterBaseClass(Equipment):
    MEASUREMENT_MODE_RMS = 'RMS'
    MEASUREMENT_MODE_MEAN = 'VMEan'
    MEASUREMENT_MODE_DC = 'DC'
    
    def __init__(self, device, device_id):
        super().__init__(device, device_id)
        self._voltage = 0
        self._current = 0
        self._power = 0
        self._pf = 0
        self._thd = 0
        

        self._integration_mode = "NORMAL"
        self._integration_time = 0
        self._integration_status = None
        self._integration_done = False
        self._current_auto_range_status = False
        self._current_range = 0
        self._voltage_range = 0
        self._voltage_auto_range_status = False
        self._averaging_status = False
        
        last = self.device.resource_name.rfind("::")
        addr = self.device.resource_name[:last]
        self.description = f'{self.manufacturer} {self.model} {addr}'

    def integrate(self, integration_time=60):
        self.write('INTEGRATE:RESET')
        self.write('INTEGRATE:MODE NORMAL')
        self.write(f'INTEGRATE:TIMER 0, {integration_time // 60}, {integration_time%60} ')
        self.write('INTEGRATE:START')
    
    def set_integration_mode(self, mode:str):
        ''' Sets the integration parameters of the Power Meter. 
        
        Keyword Arguments:
        mode        --      Either NORMAL or Continuous
        '''
        
        self.write(f'INTEGRATE:MODE {mode}')
        self._integration_mode = mode 


    def set_integration_timer(self, timer_s:int):
        """ Sets the integration timer of the power meter.

        Keyword Argument:
        timer_s     --      value of the timer in seconds
        """
        time_h = int(timer_s // 3600 )
        time_m = int((timer_s - 3600*time_h) // 60)
        time_s = int((timer_s - 3600*time_h - 60*time_m) )
        self.write(f'INTEGRATE:TIMER {time_h}, {time_m}, {time_s}')
        self._integration_time = timer_s
    
    def get_integration_timer(self):
        """ Returns the integration timer value in seconds"""
        try:
            status = self.write(f'INTEGRATE:TIMER?')
            if status is None:
                return self._integration_time
            status = str(status).strip()
            parts = status.split()
            time_str = parts[-1] if parts else status
            if ',' in time_str:
                components = [int(float(c.strip())) for c in time_str.split(',')]
                if len(components) == 3:
                    time_s = components[0]*3600 + components[1]*60 + components[2]
                elif len(components) == 2:
                    time_s = components[0]*60 + components[1]
                else:
                    time_s = components[0]
            else:
                time_s = int(float(time_str))
            self._integration_time = time_s
            return time_s
        except Exception:
            return self._integration_time
 
    def start_integration(self):
        self.write('INTEGRATE:START')
    
    def stop_integration(self):
        self.write('INTEGRATION:STOP')

    def reset_integration(self):
        self.write('INTEGRATE:RESET')
    
    def check_integration_status(self):
        self._integration_done = False
        self._integration_status = self.write("INTEGRATE:STATE?")
            
        if self._integration_status in ["TIM", "RES"]:
            self._integration_done = True
        
    def poll_integration_status(self):
        self.check_integration_status()
        while not self._integration_done:
            sleep(0.5)
            self.check_integration_status()
    
    def get_integrated_power(self, reset = True):
        """Returns the power equivalent of the total integrated energy"""
        try:
            val = self.write('NUMERIC:VAL? 15')
            energy = parse_float_response(val, 0.0)
            if self._integration_time and self._integration_time > 0:
                power = energy * 3600 / self._integration_time
            else:
                power = energy
        except Exception:
            try:
                self.write('NUMERIC:ITEM3 P, 1')
                val = self.write('NUM:NORM:VAL? 3')
                power = parse_float_response(val, 0.0)
            except Exception:
                power = 0.0
        
        # Reset integration if reset flag is true
        if reset:
            try:
                self.reset_integration()
            except Exception:
                pass
        
        return power

    def set_measurement_mode(self,mode=MEASUREMENT_MODE_RMS):
        self.write(f'INPUT:MODE {mode}')
    
    @property
    def voltage(self):
        self.write('NUMERIC:ITEM1 U, 1')
        self._voltage = parse_float_response(self.write('NUM:NORM:VAL? 1'), 0.0)
        return self._voltage
        
    @property
    def current(self):
        self.write('NUMERIC:ITEM2 I, 1')
        self._current = parse_float_response(self.write('NUM:NORM:VAL? 2'), 0.0)
        return self._current
    
    @property
    def power(self):
        if self.get_integration_timer() == 0:
            self.write('NUMERIC:ITEM3 P, 1')
            self._power = parse_float_response(self.write('NUM:NORM:VAL? 3'), 0.0)
        else:
            # Reset the integration before beginning to avoid issues
            self.reset_integration()
            self.set_integration_mode('NORMAL')
            self._integration_done = False

            # Start the integration and wait for it to finish
            self.start_integration()
            self.poll_integration_status()

            # Process the resulting energy
            power = self.get_integrated_power()
            self.reset_integration()
            
            self._power = power      
        return self._power

    @property
    def pf(self):
        self.write('NUMERIC:ITEM4 lambda, 1')
        self._pf = parse_float_response(self.write('NUM:NORM:VAL? 4'), 0.0)
        return self._pf

    @property
    def thd(self):
        self.write('INPUT:FILTER:FREQUENCY ON')
        self.write('NUMERIC:ITEM5 ITHD, 1')
        sleep(2)
        self._thd = parse_float_response(self.write('NUM:NORM:VAL? 5'), 0.0)
        self.write('INPUT:FILTER:FREQUENCY OFF')
        return self._thd
    
    def get_current_range(self):
        try:
            self._current_range = parse_float_response(self.write('INPUT:CURRENT:RANGE?'), 0.0)
        except Exception as e:
            self._current_range = 0
        return self._current_range

    def set_current_range(self, amps = None):
        if amps is None:
            self.set_current_range_max()
        else:
            self.write(f'INPUT:CURRENT:RANGE {amps}A')
    
    def set_current_range_max(self):
        self.write(f'INPUT:CURRENT:RANGE MAX')
        
    def get_voltage_range(self):
        try:
            self._voltage_range = parse_float_response(self.write('INPUT:VOLTAGE:RANGE?'), 0.0)
        except Exception as e:
            self._voltage_range = 0
        return self._voltage_range
    
    def set_voltage_range(self, volts = None):
        if volts is None:
            self.set_voltage_range_max()
        else:
            self.write(f'INPUT:VOLTAGE:RANGE {volts}V')
    
    def set_voltage_range_max(self):
        self.write(f'INPUT:VOLTAGE:RANGE MAX')
            
    def auto_range_enable(self, en:bool=True):
        if en:
            en_str = 'ON'
        else:
            en_str = 'OFF'
        self.voltage_auto_range_enable(en_str)
        self.current_auto_range_enable(en_str)

    def current_auto_range_enable(self, en:bool=True):
        if en:
            en_str = 'ON'
        else:
            en_str = 'OFF'
        self.write(f'INPUT:CURRENT:AUTO {en_str}')
    
    def current_auto_range_query(self):
        status = self.write('INPUT:CURRENT:AUTO?')

        if status == '1':
            self._current_auto_range_status = True
        else:
            self._current_auto_range_status = False
        return self._current_auto_range_status
    
    def current_auto_range_toggle(self):
        auto_range = self.current_auto_range_query()
        if auto_range:
            self.current_auto_range_enable(False)
        else:
            self.current_auto_range_enable(True)
    
    def voltage_auto_range_enable(self, en:bool=True):
        if en:
            en_str = 'ON'
        else:
            en_str = 'OFF'
        self.write(f'INPUT:VOLTAGE:AUTO {en_str}')

    def voltage_auto_range_query(self):
        status = self.write('INPUT:VOLTAGE:AUTO?')
        if status == '1':
            self._voltage_auto_range_status = True
        else:
            self._voltage_auto_range_status = False
        return self._voltage_auto_range_status

    def voltage_auto_range_toggle(self):
        auto_range = self.voltage_auto_range_query()
        if auto_range:
            self.voltage_auto_range_enable(False)
        else:
            self.voltage_auto_range_enable(True)

    def enable_averaging(self, en:bool=True):
        if en:
            self.write('MEASURE:AVERAGING:STATE ON')
        else:
            self.write('MEASURE:AVERAGING:STATE OFF')
    
    def averaging_toggle(self):
        averaging_enabled = self.query_averaging_state()

        # Inverse the current averaging state
        self.enable_averaging(not averaging_enabled)

    def query_averaging_state(self):
        state = self.write('MEASURE:AVERAGING:STATE?')[-1]
        
        if state == '1':
            self.averaging_status = True
        elif state == '0':
            self.averaging_status = False
        else:
            raise ValueError
        return self.averaging_status

    def get_harmonics(self):
        '''
            returns: list of float harmonic content (mA)
        '''
        self.write('INPUT:FILTER:FREQUENCY ON')
        self.write('HARMONICS:DISPLAY ON')
        self.write('NUMERIC:LIST:CLEAR ALL')
        self.write('NUMERIC:LIST:ITEM2 I,1')
        sleep(2)
        a = self.write("NUMeric:LIST:VALue? 2").split(',NAN,')[1].split(',')
        sleep(2)
        harmonic_content = []
        for i in a:
            harmonic_content.append(float(i)*1000)

        percent_content = []
        for i in range(len(harmonic_content)):
            percent_content.append(float(f"{(harmonic_content[i]*100/harmonic_content[0]):2f}"))

        pin = float(f"{self.power:.6f}")
        self.write("HARMONICS:DISPLAY OFF")
        self.write("INPUT:FILTER:FREQUENCY OFF")
        return harmonic_content, percent_content  

    def reset(self):
        self.write('*RST')
        
class PowerMeterWT310(PowerMeterBaseClass):
    MEASUREMENT_MODE_RMS = 'RMS'
    MEASUREMENT_MODE_MEAN = 'VMEan'
    MEASUREMENT_MODE_DC = 'DC'
    
    def __init__(self, device, device_id):
        super().__init__(device, device_id)
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

        self.set_preset()
        self.query_averaging_state()
        self.stop_integration()
        self.reset_integration()
        self.auto_range_enable()
        
    def set_preset(self):
        """
        Preset Pattern 4:
        ITEM<x>     Function    Description
        1           U           Voltage V
        2           I           Current I
        3           P           Active Power P
        4           S           Apparent Power VA
        5           Q           Reactive Power VAR
        6           LAMBda      Power Factor
        7           PHI         Phase Differnce
        8           FU          Voltage Frequency fU
        9           FI          Current Frequency FI
        10          UPPeak      Maximum Voltage U+Pk
        11          UMPeak      Minimum Voltage U-Pk
        12          IPPeak      Maximum Current I+Pk
        13          IMPeak      Minimum Current I-Pk
        14          TIME        Integration Time
        15          WH          Watt Hour
        16          WHP         Positive Watt Hour WP+
        17          WHM         Negative Watt Hour
        18          AH          Ampere Hour
        19          AHP         Ampere Hour Positive
        20          AHM         Ampere Hour Negative
        """
        # Select preset 4 to enable all types of measurement
        self.write('NUMERIC:PRESET 4')
           
    def integrate(self, integration_time=60):
        self.write('INTEGRATE:RESET')
        self.write('INTEGRATE:MODE NORMAL')
        self.write(f'INTEGRATE:TIMER 0, {integration_time // 60}, {integration_time%60} ')
        self.write('INTEGRATE:START')
    
    
    def set_integration_mode(self, mode:str):
        ''' Sets the integration parameters of the Power Meter. 
        
        Keyword Arguments:
        mode        --      Either NORMAL or Continuous
        '''
        
        self.write(f'INTEGRATE:MODE {mode}')
        self._integration_mode = mode 
        return True # Return for error handling

    
    def set_integration_timer(self, timer_s:int):
        """ Sets the integration timer of the power meter.

        Keyword Argument:
        timer_s     --      value of the timer in seconds
        """
        time_h = int(timer_s // 3600 )
        time_m = int((timer_s - 3600*time_h) // 60)
        time_s = int((timer_s - 3600*time_h - 60*time_m) )
        self.write(f'INTEGRATE:TIMER {time_h}, {time_m}, {time_s}')
        self._integration_time = timer_s

        return True # Return for error handling
    
    
    def get_integration_timer(self):
        """ Returns the integration timer value in seconds"""
        try:
            status = self.write(f'INTEGRATE:TIMER?')
            if status is None:
                return self._integration_time
            status = str(status).strip()
            parts = status.split()
            time_str = parts[-1] if parts else status
            if ',' in time_str:
                components = [int(float(c.strip())) for c in time_str.split(',')]
                if len(components) == 3:
                    time_s = components[0]*3600 + components[1]*60 + components[2]
                elif len(components) == 2:
                    time_s = components[0]*60 + components[1]
                else:
                    time_s = components[0]
            else:
                time_s = int(float(time_str))
            self._integration_time = time_s
            return time_s
        except Exception:
            return self._integration_time
 
    def start_integration(self):
        self.write('INTEGRATE:START')
    
    def stop_integration(self):
        self.write('INTEGRATION:STOP')

    def reset_integration(self):
        self.write('INTEGRATE:RESET')
    
    def check_integration_status(self):
        self._integration_done = False
        self._integration_status = self.write("INTEGRATE:STATE?")
            
        if self._integration_status in ["TIM", "RES"]:
            self._integration_done = True

    def poll_integration_status(self):
        self.check_integration_status()
        while not self._integration_done:
            sleep(0.5)
            self.check_integration_status()
            
    def get_integrated_power(self, reset = True):
        """Returns the power equivalent of the total integrated energy"""
        try:
            val = self.write('NUMERIC:VAL? 15')
            energy = parse_float_response(val, 0.0)
            if self._integration_time and self._integration_time > 0:
                power = energy * 3600 / self._integration_time
            else:
                power = energy
        except Exception:
            try:
                self.write('NUMERIC:ITEM3 P, 1')
                val = self.write('NUM:NORM:VAL? 3')
                power = parse_float_response(val, 0.0)
            except Exception:
                power = 0.0
        
        # Reset integration if reset flag is true
        if reset:
            try:
                self.reset_integration()
            except Exception:
                pass
        
        return power
    
    def set_measurement_mode(self,mode=MEASUREMENT_MODE_RMS):
        self.write(f'INPUT:MODE {mode}')

    @property
    
    def voltage(self):
        self.write('NUMERIC:ITEM1 U, 1')
        self._voltage = parse_float_response(self.write('NUM:NORM:VAL? 1'), 0.0)
        return self._voltage
        
    @property
    
    def current(self):
        self.write('NUMERIC:ITEM2 I, 1')
        self._current = parse_float_response(self.write('NUM:NORM:VAL? 2'), 0.0)
        return self._current
    
    @property
    
    def power(self):
        if self.get_integration_timer() == 0:
            self.write('NUMERIC:ITEM3 P, 1')
            self._power = parse_float_response(self.write('NUM:NORM:VAL? 3'), 0.0)
        else:
            # Reset the integration before beginning to avoid issues
            self.reset_integration()
            self.set_integration_mode('NORMAL')
            self._integration_done = False

            # Start the integration and wait for it to finish
            self.start_integration()
            self.poll_integration_status()

            # Process the resulting energy
            power = self.get_integrated_power()
            self.reset_integration()
            
            self._power = power      
        return self._power

    @property
    
    def pf(self):
        self.write('NUMERIC:ITEM4 lambda, 1')
        self._pf = parse_float_response(self.write('NUM:NORM:VAL? 4'), 0.0)
        return self._pf

    @property
    
    def thd(self):
        self.write('INPUT:FILTER:FREQUENCY ON')
        self.write('NUMERIC:ITEM5 ITHD, 1')
        sleep(2)
        self._thd = parse_float_response(self.write('NUM:NORM:VAL? 5'), 0.0)
        self.write('INPUT:FILTER:FREQUENCY OFF')
        return self._thd

    def get_current_range(self):
        try:
            self._current_range = parse_float_response(self.write('INPUT:CURRENT:RANGE?'), 0.0)
        except Exception as e:
            self._current_range = 0
        return self._current_range

    def set_current_range(self, amps = None):
        if amps is None:
            self.set_current_range_max()
        else:
            self.write(f'INPUT:CURRENT:RANGE {amps}A')
    
    def set_current_range_max(self):
        self.write(f'INPUT:CURRENT:RANGE MAX')
            
    def get_voltage_range(self):
        try:
            self._voltage_range = parse_float_response(self.write('INPUT:VOLTAGE:RANGE?'), 0.0)
        except Exception as e:
            self._voltage_range = 0
        return self._voltage_range
    
    def set_voltage_range(self, volts = None):
        if volts is None:
            self.set_voltage_range_max()
        else:
            self.write(f'INPUT:VOLTAGE:RANGE {volts}V')
    
    def set_voltage_range_max(self):
        self.write(f'INPUT:VOLTAGE:RANGE MAX')

    def auto_range_enable(self, en:bool=True):
        if en:
            en_str = 'ON'
        else:
            en_str = 'OFF'
        self.voltage_auto_range_enable(en_str)
        self.current_auto_range_enable(en_str)

    def current_auto_range_enable(self, en:bool=True):
        if en:
            en_str = 'ON'
        else:
            en_str = 'OFF'
        self.write(f'INPUT:CURRENT:AUTO {en_str}')
    
    def current_auto_range_query(self):
        status = self.write('INPUT:CURRENT:AUTO?')
        
        if status[-1] == '1':
            self._current_auto_range_status = True
        else:
            self._current_auto_range_status = False
        return self._current_auto_range_status
    
    def current_auto_range_toggle(self):
        auto_range = self.current_auto_range_query()
        if auto_range:
            self.current_auto_range_enable(False)
        else:
            self.current_auto_range_enable(True)
    
    def voltage_auto_range_enable(self, en:bool=True):
        if en:
            en_str = 'ON'
        else:
            en_str = 'OFF'
        self.write(f'INPUT:VOLTAGE:AUTO {en_str}')

    def voltage_auto_range_query(self):
        status = self.write('INPUT:VOLTAGE:AUTO?')
        
        if status[-1] == '1':
            self._voltage_auto_range_status = True
        else:
            self._voltage_auto_range_status = False
        return self._voltage_auto_range_status

    def voltage_auto_range_toggle(self):
        auto_range = self.voltage_auto_range_query()
        if auto_range:
            self.voltage_auto_range_enable(False)
        else:
            self.voltage_auto_range_enable(True)

    def enable_averaging(self, en:bool=True):
        if en:
            self.write('MEASURE:AVERAGING:STATE ON')
        else:
            self.write('MEASURE:AVERAGING:STATE OFF')
    
    def averaging_toggle(self):
        averaging_enabled = self.query_averaging_state()

        # Inverse the current averaging state
        self.enable_averaging(not averaging_enabled)

    def query_averaging_state(self):
        state = self.write('MEASURE:AVERAGING:STATE?')[-1]
        
        if state == '1':
            self.averaging_status = True
        elif state == '0':
            self.averaging_status = False
        else:
            raise ValueError
        return self.averaging_status
    
    def get_harmonics(self):
        '''
            returns: list of float harmonic content (mA)
        '''
        self.write('INPUT:FILTER:FREQUENCY ON')
        self.write('HARMONICS:DISPLAY ON')
        self.write('NUMERIC:LIST:CLEAR ALL')
        self.write('NUMERIC:LIST:ITEM2 I,1')
        sleep(2)
        a = self.write("NUMeric:LIST:VALue? 2").split(',NAN,')[1].split(',')
        sleep(2)
        harmonic_content = []
        for i in a:
            harmonic_content.append(float(i)*1000)

        percent_content = []
        for i in range(len(harmonic_content)):
            percent_content.append(float(f"{(harmonic_content[i]*100/harmonic_content[0]):2f}"))

        pin = float(f"{self.power:.6f}")
        self.write("HARMONICS:DISPLAY OFF")
        self.write("INPUT:FILTER:FREQUENCY OFF")
        return harmonic_content, percent_content  

    def reset(self):
        self.write('*RST')    

class PowerMeterWT500(PowerMeterBaseClass):
    MEASUREMENT_MODE_RMS = 'RMS'
    MEASUREMENT_MODE_MEAN = 'VMEan'
    MEASUREMENT_MODE_DC = 'DC'
    
    def __init__(self, device, device_id):
        super().__init__(device, device_id)
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

        self.set_preset()
        self.query_averaging_state()
        self.stop_integration()
        self.reset_integration()
        self.auto_range_enable()
        
    def set_preset(self):
        """
        Preset Pattern 4:
        ITEM<x>     Function    Description
        1 URMS 1
        2 UMN 1
        3 UDC 1
        4 URMN 1
        5 UAC 1
        6 IRMS 1
        7 IMN 1
        8 IDC 1
        9 IRMN 1
        10 IAC 1
        11 P 1
        12 S 1
        13 Q 1
        14 LAMBda 1
        15 PHI 1
        16 FU 1
        17 FI 1
        18 UPPeak 1
        19 UMPeak 1
        20 IPPeak 1
        21 IMPeak 1
        22 CFU 1
        23 CFI 1
        24 TIME 1
        25 WH 1
        26 WHP 1
        27 WHM 1
        28 AH 1
        29 AHP 1
        30 AHM 1
        31 WS 1
        32 WQ 1
        33 to 64 URMS to WQ 2
        65 to 96 URMS to WQ 3
        97 to 128 URMS to WQ SIGMA
        129 to 255 NONE
        """
        # Select preset 4 to enable all types of measurement
        self.write('NUMERIC:PRESET 4')
           
    def integrate(self, integration_time=60):
        self.write('INTEGRATE:RESET')
        self.write('INTEGRATE:MODE NORMAL')
        self.write(f'INTEGRATE:TIMER 0, {integration_time // 60}, {integration_time%60} ')
        self.write('INTEGRATE:START')
    
    
    def set_integration_mode(self, mode:str):
        ''' Sets the integration parameters of the Power Meter. 
        
        Keyword Arguments:
        mode        --      Either NORMAL or Continuous
        '''
        
        self.write(f'INTEGRATE:MODE {mode}')
        self._integration_mode = mode 
        return True # Return for error handling

    
    def set_integration_timer(self, timer_s:int):
        """ Sets the integration timer of the power meter.

        Keyword Argument:
        timer_s     --      value of the timer in seconds
        """
        time_h = int(timer_s // 3600 )
        time_m = int((timer_s - 3600*time_h) // 60)
        time_s = int((timer_s - 3600*time_h - 60*time_m) )
        self.write(f'INTEGRATE:TIMER {time_h}, {time_m}, {time_s}')
        self._integration_time = timer_s

        return True # Return for error handling
    
    
    def get_integration_timer(self):
        """ Returns the integration timer value in seconds"""
        try:
            status = self.write(f'INTEGRATE:TIMER?')
            if status is None:
                return self._integration_time
            status = str(status).strip()
            parts = status.split()
            time_str = parts[-1] if parts else status
            if ',' in time_str:
                components = [int(float(c.strip())) for c in time_str.split(',')]
                if len(components) == 3:
                    time_s = components[0]*3600 + components[1]*60 + components[2]
                elif len(components) == 2:
                    time_s = components[0]*60 + components[1]
                else:
                    time_s = components[0]
            else:
                time_s = int(float(time_str))
            self._integration_time = time_s
            return time_s
        except Exception:
            return self._integration_time
 
    def start_integration(self):
        self.write('INTEGRATE:START')
    
    def stop_integration(self):
        self.write('INTEGRATION:STOP')

    def reset_integration(self):
        self.write('INTEGRATE:RESET')
    
    def check_integration_status(self):
        self._integration_done = False
        self._integration_status = self.write("INTEGRATE:STATE?")
            
        if self._integration_status in ["TIM", "RES"]:
            self._integration_done = True

    def poll_integration_status(self):
        self.check_integration_status()
        while not self._integration_done:
            sleep(0.5)
            self.check_integration_status()
            
    def get_integrated_power(self, reset = True):
        """Returns the power equivalent of the total integrated energy"""
        try:
            val = self.write('NUMERIC:VAL? 25')
            energy = parse_float_response(val, 0.0)
            if self._integration_time and self._integration_time > 0:
                power = energy * 3600 / self._integration_time
            else:
                power = energy
        except Exception:
            try:
                self.write('NUMERIC:ITEM3 P, 1')
                val = self.write('NUM:NORM:VAL? 3')
                power = parse_float_response(val, 0.0)
            except Exception:
                power = 0.0
        
        # Reset integration if reset flag is true
        if reset:
            try:
                self.reset_integration()
            except Exception:
                pass
        
        return power
    
    def set_measurement_mode(self,mode=MEASUREMENT_MODE_RMS):
        self.write(f'INPUT:MODE {mode}')

    @property
    
    def voltage(self):
        self.write('NUMERIC:ITEM1 URMS, 1')
        self._voltage = parse_float_response(self.write('NUM:NORM:VAL? 1'), 0.0)
        return self._voltage
        
    @property
    
    def current(self):
        self.write('NUMERIC:ITEM2 IRMS, 1')
        self._current = parse_float_response(self.write('NUM:NORM:VAL? 2'), 0.0)
        return self._current
    
    @property
    
    def power(self):
        if self.get_integration_timer() == 0:
            self.write('NUMERIC:ITEM3 P, 1')
            self._power = parse_float_response(self.write('NUM:NORM:VAL? 3'), 0.0)
        else:
            # Reset the integration before beginning to avoid issues
            self.reset_integration()
            self.set_integration_mode('NORMAL')
            self._integration_done = False

            # Start the integration and wait for it to finish
            self.start_integration()
            self.poll_integration_status()

            # Process the resulting energy
            power = self.get_integrated_power()
            self.reset_integration()
            
            self._power = power      
        return self._power

    @property
    
    def pf(self):
        self.write('NUMERIC:ITEM4 lambda, 1')
        self._pf = parse_float_response(self.write('NUM:NORM:VAL? 4'), 0.0)
        return self._pf

    @property
    
    def thd(self):
        self.write('INPUT:FILTER:FREQUENCY ON')
        self.write('NUMERIC:ITEM5 ITHD, 1')
        sleep(2)
        self._thd = parse_float_response(self.write('NUM:NORM:VAL? 5'), 0.0)
        self.write('INPUT:FILTER:FREQUENCY OFF')
        return self._thd

    def get_current_range(self):
        try:
            self._current_range = parse_float_response(self.write('INPUT:CURRENT:RANGE?'), 0.0)
        except Exception as e:
            self._current_range = 0
        return self._current_range

    def set_current_range(self, amps = None):
        if amps is None:
            self.set_current_range_max()
        else:
            self.write(f'INPUT:CURRENT:RANGE {amps}A')
    
    def set_current_range_max(self):
        self.write(f'INPUT:CURRENT:RANGE MAX')
            
    def get_voltage_range(self):
        try:
            self._voltage_range = parse_float_response(self.write('INPUT:VOLTAGE:RANGE?'), 0.0)
        except Exception as e:
            self._voltage_range = 0
        return self._voltage_range
    
    def set_voltage_range(self, volts = None):
        if volts is None:
            self.set_voltage_range_max()
        else:
            self.write(f'INPUT:VOLTAGE:RANGE {volts}V')
    
    def set_voltage_range_max(self):
        self.write(f'INPUT:VOLTAGE:RANGE MAX')

    def auto_range_enable(self, en:bool=True):
        if en:
            en_str = 'ON'
        else:
            en_str = 'OFF'
        self.voltage_auto_range_enable(en_str)
        self.current_auto_range_enable(en_str)

    def current_auto_range_enable(self, en:bool=True):
        if en:
            en_str = 'ON'
        else:
            en_str = 'OFF'
        self.write(f'INPUT:CURRENT:AUTO {en_str}')
        sleep(2)
    
    def current_auto_range_query(self):
        status = self.write('INPUT:CURRENT:AUTO?')
        
        if status[-1] == '1':
            self._current_auto_range_status = True
        else:
            self._current_auto_range_status = False
        return self._current_auto_range_status
    
    def current_auto_range_toggle(self):
        auto_range = self.current_auto_range_query()
        if auto_range:
            self.current_auto_range_enable(False)
        else:
            self.current_auto_range_enable(True)
    
    def voltage_auto_range_enable(self, en:bool=True):
        if en:
            en_str = 'ON'
        else:
            en_str = 'OFF'
        self.write(f'INPUT:VOLTAGE:AUTO {en_str}')
        sleep(2)

    def voltage_auto_range_query(self):
        status = self.write('INPUT:VOLTAGE:AUTO?')
        
        if status[-1] == '1':
            self._voltage_auto_range_status = True
        else:
            self._voltage_auto_range_status = False
        return self._voltage_auto_range_status

    def voltage_auto_range_toggle(self):
        auto_range = self.voltage_auto_range_query()
        if auto_range:
            self.voltage_auto_range_enable(False)
        else:
            self.voltage_auto_range_enable(True)

    def enable_averaging(self, en:bool=True):
        if en:
            self.write('MEASURE:AVERAGING:STATE ON')
        else:
            self.write('MEASURE:AVERAGING:STATE OFF')
    
    def averaging_toggle(self):
        averaging_enabled = self.query_averaging_state()

        # Inverse the current averaging state
        self.enable_averaging(not averaging_enabled)

    def query_averaging_state(self):
        state = self.write('MEASURE:AVERAGING:STATE?')[-1]
        
        if state == '1':
            self.averaging_status = True
        elif state == '0':
            self.averaging_status = False
        else:
            raise ValueError
        return self.averaging_status
    
    def get_harmonics(self):
        '''
            returns: list of float harmonic content (mA)
        '''
        self.write('INPUT:FILTER:FREQUENCY ON')
        self.write('HARMONICS:DISPLAY ON')
        self.write('NUMERIC:LIST:CLEAR ALL')
        self.write('NUMERIC:LIST:ITEM2 I,1')
        sleep(2)
        a = self.write("NUMeric:LIST:VALue? 2").split(',NAN,')[1].split(',')
        sleep(2)
        harmonic_content = []
        for i in a:
            harmonic_content.append(float(i)*1000)

        percent_content = []
        for i in range(len(harmonic_content)):
            percent_content.append(float(f"{(harmonic_content[i]*100/harmonic_content[0]):2f}"))

        pin = float(f"{self.power:.6f}")
        self.write("HARMONICS:DISPLAY OFF")
        self.write("INPUT:FILTER:FREQUENCY OFF")
        return harmonic_content, percent_content  

    def reset(self):
        self.write('*RST')  

class PowerMeterWT210(PowerMeterBaseClass):
    MEASUREMENT_MODE_RMS = '0'
    MEASUREMENT_MODE_MEAN = '1'
    MEASUREMENT_MODE_DC = '2'
    
    def __init__(self, device, device_id):
        super().__init__(device, device_id)
        
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
        
        self.write("MEASURE:HARMONICS:ITEM:PRESET CLEAR")
        self.write("HARMONICS:STATE OFF")
        sleep(2)
        self.write("MEASURE:ITEM:PRESET CLEAR")
        
        self.query_averaging_state()
        self.stop_integration()
        self.reset_integration()
        self.auto_range_enable()
    
    def set_preset(self):
        pass
    
    def integrate(self, integration_time=60):
        self.write('INTEGRATE:RESET')
        self.write('INTEGRATE:MODE NORMAL')
        self.write(f'INTEGRATE:TIMER 0, {integration_time // 60}, {integration_time%60} ')
        self.write('INTEGRATE:START')
    
    def set_integration_mode(self, mode:str):
        ''' Sets the integration parameters of the Power Meter. 
        
        Keyword Arguments:
        mode        --      Either NORMAL or Continuous
        '''
        
        self.write(f'INTEGRATE:MODE {mode}')
        self._integration_mode = mode 


    def set_integration_timer(self, timer_s:int):
        """ Sets the integration timer of the power meter.

        Keyword Argument:
        timer_s     --      value of the timer in seconds
        """
        time_h = int(timer_s // 3600 )
        time_m = int((timer_s - 3600*time_h) // 60)
        time_s = int((timer_s - 3600*time_h - 60*time_m) )
        self.write(f'INTEGRATE:TIMER {time_h}, {time_m}, {time_s}')
        self._integration_time = timer_s
    
    def get_integration_timer(self):
        """ Returns the integration timer value in seconds"""
        try:
            status = self.write(f'INTEGRATE:TIME?')
            if status is None:
                return self._integration_time
            status = str(status).strip()
            parts = status.split()
            time_str = parts[-1] if parts else status
            if ',' in time_str:
                components = [int(float(c.strip())) for c in time_str.split(',')]
                if len(components) == 3:
                    time_s = components[0]*3600 + components[1]*60 + components[2]
                elif len(components) == 2:
                    time_s = components[0]*60 + components[1]
                else:
                    time_s = components[0]
            else:
                time_s = int(float(time_str))
            self._integration_time = time_s
            return time_s
        except Exception:
            return self._integration_time
 
    def start_integration(self):
        self._integration_done = False
        self.write('INTEGRATE:START')
        self._integration_status = "START"
    
    def stop_integration(self):
        self.write('INTEGRATION:STOP')
        self._integration_status = "STOP"

    def reset_integration(self):
        self.write('INTEGRATE:RESET')
        self._integration_status = "RES"
    
    def check_integration_status(self):
        try:
            self._integration_done = False
            self.write('MEASURE:ITEM:TIME ON')
            time = self.write('MEASURE:VALUE?')
            self.write('MEASURE:ITEM:TIME OFF')
            if time:
                parts = str(time).strip().split(',')
                if len(parts) == 3:
                    time_s = int(float(parts[0]))*3600 + int(float(parts[1]))*60 + int(float(parts[2]))
                    if time_s >= self._integration_time:         
                        self._integration_status = "TIM"
                        self._integration_done = True
        except Exception:
            pass
    
    def poll_integration_status(self):
        self.check_integration_status()
        while not self._integration_done:
            sleep(0.5)
            self.check_integration_status()

    def get_integrated_power(self, reset = True):
        """Returns the power equivalent of the total integrated energy"""
        try:
            self.write("MEASURE:ITEM:WH:ELEMENT1 ON")
            val = self.write("MEASURE:VALUE?")
            self.write("MEASURE:ITEM:WH:ELEMENT1 OFF")
            energy = parse_float_response(val, 0.0)
            if self._integration_time and self._integration_time > 0:
                power = energy * 3600 / self._integration_time
            else:
                power = energy
        except Exception:
            try:
                self.write("MEASURE:ITEM:W:ELEMENT1 ON")
                val = self.write("MEASURE:VALUE?")
                self.write("MEASURE:ITEM:W:ELEMENT1 OFF")
                power = parse_float_response(val, 0.0)
            except Exception:
                power = 0.0
        
        # Reset integration if reset flag is true
        if reset:
            try:
                self.reset_integration()
            except Exception:
                pass
        return power
    
    def set_measurement_mode(self,mode=MEASUREMENT_MODE_RMS):
        self.write(f'MN {mode}')

    @property
    
    def voltage(self):
        self.write('MEASURE:ITEM:V:ELEMENT1 ON')
        self._voltage = parse_float_response(self.write('MEASURE:VALUE?'), 0.0)
        self.write('MEASURE:ITEM:V:ELEMENT1 OFF')
        return self._voltage
        
    @property
    
    def current(self):
        self.write('MEASURE:ITEM:A:ELEMENT1 ON')
        self._current = parse_float_response(self.write('MEASURE:VALUE?'), 0.0)
        self.write('MEASURE:ITEM:A:ELEMENT1 OFF')
        return self._current
    
    @property
    
    def power(self):
        if self.get_integration_timer() == 0:
            self.write('MEASURE:ITEM:W:ELEMENT1 ON')
            self._power = parse_float_response(self.write('MEASURE:VALUE?'), 0.0)
            self.write('MEASURE:ITEM:W:ELEMENT1 OFF')
        else:
            # Reset the integration before beginning to avoid issues
            self.reset_integration()
            self.set_integration_mode('NORMAL')
            self._integration_done = False

            # Start the integration and wait for it to finish
            self.start_integration()
            self.poll_integration_status()

            # Process the resulting energy
            power = self.get_integrated_power()
            self.reset_integration()
            
            self._power = power      
        return self._power

    @property
    
    def pf(self):
        self.write('MEASURE:ITEM:PF:ELEMENT1 ON')
        self._pf = parse_float_response(self.write('MEASURE:VALUE?'), 0.0)
        self.write('MEASURE:ITEM:PF:ELEMENT1 OFF')
        return self._pf

    @property
    
    def thd(self):
        self.write('CONFIGURE:FILTER ON')
        self.write('HARMONICS:STATE ON')
        self.write('MEASURE:HARMONICS:ITEM:PRESET CLEAR')
        self.write('MEASURE:HARMONICS:ITEM:ATHD ON')
        sleep(2)
        self._thd = parse_float_response(self.write('MEASURE:HARMONICS:VALUE?'), 0.0)
        self.write('MEASURE:HARMONICS:ITEM:ATHD OFF')
        self.write('HARMONICS:STATE OFF')
        self.write('CONFIGURE:FILTER OFF')
        return self._thd
        
    def get_current_range(self):
        try:
            self._current_range = parse_float_response(self.write('CONFIGURE:CURRENT:RANGE?'), 0.0)
        except Exception as e:
            self._current_range = 0
        return self._current_range

    def set_current_range(self, amps = None):
        if amps is None:
            self.set_current_range_max()
        else:
            self.write(f'CONFIGURE:CURRENT:RANGE {amps}A')
    
    def set_current_range_max(self):
        self.write(f'CONFIGURE:CURRENT:RANGE MAX')
            
    def get_voltage_range(self):
        try:
            self._voltage_range = parse_float_response(self.write('CONFIGURE:VOLTAGE:RANGE?'), 0.0)
        except Exception as e:
            self._voltage_range = 0
        return self._voltage_range
    
    def set_voltage_range(self, volts = None):
        if volts is None:
            self.set_voltage_range_max()
        else:
            self.write(f'CONFIGURE:VOLTAGE:RANGE {volts}V')
    
    def set_voltage_range_max(self):
        self.write(f'CONFIGURE:VOLTAGE:RANGE MAX')

    def auto_range_enable(self, en:bool=True):
        if en:
            en_str = 'ON'
        else:
            en_str = 'OFF'
        self.voltage_auto_range_enable(en_str)
        self.current_auto_range_enable(en_str)

    def current_auto_range_enable(self, en:bool=True):
        if en:
            en_str = 'ON'
        else:
            en_str = 'OFF'
        self.write(f'CONFIGURE:CURRENT:AUTO {en_str}')
    
    def current_auto_range_query(self):
        status = self.write('CONFIGURE:CURRENT:AUTO?')

        if status[-1] == '1':
            self._current_auto_range_status = True
        else:
            self._current_auto_range_status = False
        return self._current_auto_range_status
    
    def current_auto_range_toggle(self):
        auto_range = self.current_auto_range_query()
        if auto_range:
            self.current_auto_range_enable(False)
        else:
            self.current_auto_range_enable(True)
    
    def voltage_auto_range_enable(self, en:bool=True):
        if en:
            en_str = 'ON'
        else:
            en_str = 'OFF'
        self.write(f'CONFIGURE:VOLTAGE:AUTO {en_str}')

    def voltage_auto_range_query(self):
        status = self.write('CONFIGURE:VOLTAGE:AUTO?')

        if status[-1] == '1':
            self._voltage_auto_range_status = True
        else:
            self._voltage_auto_range_status = False
        return self._voltage_auto_range_status

    def voltage_auto_range_toggle(self):
        auto_range = self.voltage_auto_range_query()
        if auto_range:
            self.voltage_auto_range_enable(False)
        else:
            self.voltage_auto_range_enable(True)

    def enable_averaging(self, en:bool=True):
        if en:
            self.write('CONF:AVERAGING:STATE ON')
        else:
            self.write('CONF:AVERAGING:STATE OFF')
    
    def averaging_toggle(self):
        averaging_enabled = self.query_averaging_state()
        # Inverse the current averaging state
        self.enable_averaging(not averaging_enabled)

    def query_averaging_state(self):
        state = self.write('CONF:AVERAGING:STATE?')[-1]
        
        if state == '1':
            self.averaging_status = True
        elif state == '0':
            self.averaging_status = False
        else:
            raise ValueError
        return self.averaging_status

    def get_harmonics(self):
        '''
            returns: list of float harmonic content (mA)
        '''
        self.write('CONFIGURE:FILTER ON')
        self.write('HARMONICS:STATE ON')
        self.write('MEASURE:HARMONICS:ITEM:PRESET APATTERN')
        sleep(2)
        a = self.write("MEASURE:HARMONICS:VALUE?").split(',NAN,')[1].split(',')
        sleep(2)
        harmonic_content = []
        for i in a:
            harmonic_content.append(float(i)*1000)

        percent_content = []
        for i in range(len(harmonic_content)):
            percent_content.append(float(f"{(harmonic_content[i]*100/harmonic_content[0]):2f}"))
        #(percent_content)

        pin = float(f"{self.power:.6f}")
        self.write("HARMONICS:STATE OFF")
        self.write("CONFIGURE:FILTER OFF")
        return harmonic_content, percent_content  

    def reset(self):
        self.write('*RST')
        
class PowerMeterChroma(PowerMeterBaseClass):
    def __init__(self, device, device_id):
        super().__init__(device, device_id)
    