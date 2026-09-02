# Standard Library imports
from time import sleep
from math import ceil
import os

# Third party imports
import numpy as np
import json

# Local Imports
from misc_functions.misc_functions import timeit
from user_settings.save_load import *
from pd.pd_types import SUPPLY_TYPE, AUGMENTED_TYPE

# Flags for controlling threaded tests
test_control_flags = {'StopTest': False,
                      'SkipTest': False}

class TestStopped(Exception):
    pass

class TestFailed(Exception):
    pass

class TestSkipped(Exception):
    pass

class TestStatus:
    IN_QUEUE = "In Queue"
    IN_PROGRESS = "In Progress"
    COMPLETE = "Complete"

    STOPPED = "Stopped"
    SKIPPED = "Skipped"
    FAILED = "FAILED"

class MessageType:
    INFO = 'info'
    WARNING = 'warning'
    ABORT = 'abort'

class LineRange():
    """ Defines the ranges of a line including the voltage and frequency
    """
    def __init__(self, name='', vin_freq=[], custom=False, *args, **kwargs):
        self.name = name
        self.vin_freq:list = vin_freq
        self.custom = custom

    def add_vin_freq(self, vin:float, freq:float):
        """ Add a VIN and Frequency pair to the range list
        """
        self.vin_freq.append([vin, freq])


    def delete_vin_freq(self, index):
        """ Remove a VIN and Frequency pair from the range list
        """
        self.vin_freq.pop(index)

    def get_dict(self)->dict:
        """Return a dictionary containing the details of the LineRange object."""
        d = {'name':self.name, 
             'vin_freq':self.vin_freq, 
             'custom':self.custom}
        return d
    
    def init_from_dict(self, dict):
        """Initialize the object from a dictionary input."""
        self.name = dict['name']
        self.vin_freq = dict['vin_freq']
        self.custom = dict['custom']


class LineSettings:
    """
    Contains all the different configurations of line
    """
    # Settings available by default
    UNIVERSAL = LineRange(
        name="Universal",
        vin_freq=[ [90, 60], [115, 60], [230, 50], [265, 50] ],
        custom = False)
    UNIVERSAL_EXT = LineRange(
        name="Universal Extended",
        vin_freq=[ [90, 60], [115, 60], [132, 60], [180, 50], [230, 50], [265, 50] ],
        custom = False)
    LOW_LINE = LineRange(
        name="Low Line",
        vin_freq=[ [90, 60], [100,60], [110,60], [115, 60], [120, 60], [132, 60] ],
        custom = False)
    HIGH_LINE = LineRange(
        name="High Line",
        vin_freq=[ [180, 50], [200, 50], [220, 50], [240, 50], [265, 50] ],
        custom = False)
    LL_HL = LineRange(
        name="90, 230",
        vin_freq=[ [90, 60], [230,50]],
        custom = False)
    CUSTOM = LineRange(
        name = "Custom",
        vin_freq=[],
        custom = True
    )
    
    def __init__(self):
        # TODO: In the future, place these settings in text files
        # then load it during initialization so that the 
        # information is stored
        self.line_range_list:list[LineRange] = []
        self.set_ranges()
        self.default_list_names = list(x.name for x in self.line_range_list)

    def read_user_settings(self):
        """Read the custom line settings that are stored in the documents folder"""
        # Check if the file already exists
        if not os.path.exists(line_settings_filepath):
            # If it doesn't exist, write the defaults
            self.write_user_settings()
        
        # If the settings file already exists
        else:
            # Open the file as json to read its contents
            with open(line_settings_filepath, "r") as line_settings_file:
                line_settings_list = json.load(line_settings_file)
            
            # Go through each setting
            # Add it to the current settings only if isn't already defined
            # self.line_range_list.clear()
            for line_range_dict in line_settings_list:
                self.add_dict_to_range_list(line_range_dict)
    
    def add_dict_to_range_list(self, line_range_dict:dict):
        """Add the line range to the list only if it isn't already defined."""

        match_found = False
        # Loop through the values in the line range list
        # and check if the tested object already exists
        for count, range in enumerate(self.line_range_list):
            # Ignore if stored is equal to the tested value
            if range.name == line_range_dict['name'] and \
                    range.vin_freq == line_range_dict['vin_freq']:
                match_found = True
                break
            # Overwrite the vin_freq if the name already exists
            if range.name == line_range_dict['name']:
                if line_range_dict['custom'] and \
                    line_range_dict['name'] not in self.default_list_names:
                    self.line_range_list[count].vin_freq = line_range_dict['vin_freq']
                match_found = True
                break
        
        if not match_found:
            new_line_range = LineRange(
                name=line_range_dict['name'],
                vin_freq=line_range_dict['vin_freq'],
                custom=line_range_dict['custom'])
            self.line_range_list.append(new_line_range)
            

    def write_user_settings(self):
        """Write the user settings from memory to the json file"""
        obj_list = []
        for line_range in self.line_range_list:
            d = line_range.get_dict()
            obj_list.append(d)
        
        with open(line_settings_filepath, 'w') as settings_file:
            json.dump(obj_list, settings_file, indent=2)
            
    def set_ranges(self):       
        self.add_line_range(self.UNIVERSAL)
        self.add_line_range(self.UNIVERSAL_EXT)
        self.add_line_range(self.LOW_LINE)
        self.add_line_range(self.HIGH_LINE)
        self.add_line_range(self.LL_HL)
        self.add_line_range(self.CUSTOM)
    
    def add_line_range(self, line_range:LineRange):
        # Adds a LineRange object to the list of LineRange objects
        self.line_range_list.append(line_range)

    def add_vin_freq(self, line_range, vin, freq):
        """Add a vin freq to the line range given"""
        # Get the index of the line range in the list
        for i, item in enumerate(self.line_range_list):
            if item.name == line_range.name:
                index = i
                line_range_item:LineRange = item
        
        line_range_item.add_vin_freq(vin, freq)
    
    def delete_vin_freq(self, line_range, index):
        """Remove the line range entry specified"""
        # Get the index of the line range in the list
        for i, item in enumerate(self.line_range_list):
            if item.name == line_range.name:
                index = i
                line_range_item:LineRange = item
        
        line_range_item.delete_vin_freq(index)

class LoadRange:
    """ Contains the load percentage range
    """
    def __init__(self, name:str = '', load_range_pct:list = [], 
                 custom:bool = False, *args, **kwargs):
        self.name:str = name
        self.load_range_pct:list = load_range_pct
        self.custom:bool = custom
    
    def add_load_pct(self, load_pct):
        """ Add a load step with given percentage
        Update the order of the list
        """
        self.load_range_pct.append(load_pct)

    def delete_load_pct(self, index):
        """ Remove the load step with given index
        Update the order of the list
        """
        self.load_range_pct.pop(index)
        
    def check_load_direction(self,direction):
        """ Update the order of the list based
        on direction
        """
        if direction == 'Upward':
            return list(reversed(self.load_range_pct))
        else:
            return self.load_range_pct
################################################################################
    def get_dict(self)->dict:
        """Return a dictionary containing the details of the LoadRange object."""
        d = {'name':self.name, 
             'load_range_pct':self.load_range_pct, 
             'custom':self.custom}
        return d
    
class LoadSettings:
    """ Container class for the different load settings
    """
    LOAD_10_PCT_STEP = LoadRange(
        name="10% Step", 
        load_range_pct=[ 100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0],
        custom = False)
    
    LOAD_50_PCT_STEP = LoadRange(
        name="50% Step",
        load_range_pct=[ 100, 50, 0,],
        custom = False)
    
    LOAD_25_PCT_STEP = LoadRange(
        name="25% Step",
        load_range_pct=[ 100, 75, 50, 25, 0])
    
    LOAD_100_50_PCT = LoadRange(
        name="100%, 50%",
        load_range_pct=[ 100, 50],
        custom = False)
    
    LOAD_FL_NL_FL_10_PCT_STEP = LoadRange(
        name="FL - NL - FL",
        load_range_pct=[ 100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        custom = False)
    
    LOAD_EFF = LoadRange(
        name="Efficiency Test",
        load_range_pct=[ 100, 75, 50, 25, 10],
        custom = False)

    LOAD_SINGLE_VALUE_100_PCT = LoadRange(
        name="Full Load",
        load_range_pct=[100],
        custom = False)

    LOAD_SINGLE_VALUE_50_PCT = LoadRange(
        name="Half Load",
        load_range_pct=[50],
        custom = False)
    
    LOAD_LIGHT_LOAD_W = LoadRange(
        name="Light Load Power",
        load_range_pct=[0.15,0.25,0.5,1,2,5,10,15,20],
        custom = False)
    
    LOAD_CUSTOM = LoadRange(
        name="Custom",
        load_range_pct=[],
        custom = True)
    
    def __init__(self):
        # Create a list containing the load ranges
        self.load_range_list:list[LoadRange] = []
        self.set_ranges()
        self.default_list_names = list(x.name for x in self.load_range_list)
        
    def set_ranges(self):
        # Add the predetermined load lists
        self.add_load_range(self.LOAD_10_PCT_STEP)
        self.add_load_range(self.LOAD_50_PCT_STEP)
        self.add_load_range(self.LOAD_25_PCT_STEP)
        self.add_load_range(self.LOAD_EFF)
        self.add_load_range(self.LOAD_FL_NL_FL_10_PCT_STEP)
        self.add_load_range(self.LOAD_100_50_PCT)
        self.add_load_range(self.LOAD_SINGLE_VALUE_50_PCT)
        self.add_load_range(self.LOAD_SINGLE_VALUE_100_PCT)
        self.add_load_range(self.LOAD_LIGHT_LOAD_W)
        self.add_load_range(self.LOAD_CUSTOM)

    def add_load_range(self, load_range:LoadRange):
        self.load_range_list.append(load_range)

    def read_user_settings(self):
        """Read the custom load settings that are stored in the documents folder"""
        # Check if the file already exists
        if not os.path.exists(load_settings_filepath):
            # If it doesn't exist, write the defaults
            self.write_user_settings()
        
        # If the settings file already exists
        else:
            # Open the file as json to read its contents
            with open(load_settings_filepath, "r") as load_settings_file:
                load_settings_list = json.load(load_settings_file)
            
            # Go through each setting
            # Add it to the current settings only if isn't already defined
            # self.line_range_list.clear()
            for load_range_dict in load_settings_list:
                self.add_dict_to_range_list(load_range_dict)
    
    def add_dict_to_range_list(self, load_range_dict:dict):
        """Add the load range to the list only if it isn't already defined."""

        match_found = False
        # Loop through the values in the load range list
        # and check if the tested object already exists
        for count, range in enumerate(self.load_range_list):
            # Ignore if stored is equal to the tested value
            if range.name == load_range_dict['name'] and \
                    range.load_range_pct == load_range_dict['load_range_pct']:
                match_found = True
                break
            # Overwrite the vin_freq if the name already exists
            if range.name == load_range_dict['name']:
                if load_range_dict['custom'] and \
                    load_range_dict['name'] not in self.default_list_names:
                    self.load_range_list[count].load_range_pct\
                        = load_range_dict['load_range_pct']
                match_found = True
                break
        
        if not match_found:
            new_load_range = LoadRange(
                name=load_range_dict['name'],
                load_range_pct=load_range_dict['load_range_pct'],
                custom=load_range_dict['custom'])
            self.load_range_list.append(new_load_range)
            

    def write_user_settings(self):
        """Write the user settings from memory to the json file"""
        obj_list = []
        for load_range in self.load_range_list:
            d = load_range.get_dict()
            obj_list.append(d)
        
        with open(load_settings_filepath, 'w') as settings_file:
            json.dump(obj_list, settings_file, indent=2)


class SoakTime:
    def __init__(self,
                name:str = '',
                initial:float=0, 
                line:float=0, 
                load:float=0,
                integration:float=0,
                custom:bool = False):

        self.name = name
        self.initial_soak = initial
        self.soak_per_line = line
        self.soak_per_load = load
        self.integration_time = integration
        self.custom = custom
    
    def do_initial_soak(self):
        global test_control_flags

        soak = ceil(self.initial_soak)

        for i in range(soak*2):
            sleep(0.5)
            if test_control_flags['StopTest'] == True:
                raise TestStopped
            if test_control_flags['SkipTest'] == True:
                raise TestSkipped
        # sleep(self.initial_soak)

    def do_soak_per_line(self):
        global test_control_flags

        soak = ceil(self.soak_per_line)

        for i in range(soak*2):
            sleep(0.5)
            if test_control_flags['StopTest'] == True:
                raise TestStopped
            if test_control_flags['SkipTest'] == True:
                raise TestSkipped
        # sleep(self.soak_per_line)
    
    def do_soak_per_load(self):
        global test_control_flags

        soak = ceil(self.soak_per_load)

        for i in range(soak*2):
            sleep(0.5)
            if test_control_flags['StopTest'] == True:
                raise TestStopped
            if test_control_flags['SkipTest'] == True:
                raise TestSkipped

    def do_integration_soak(self):
        global test_control_flags

        soak = ceil(self.integration_time)

        for i in range(soak*2):
            sleep(0.5)
            if test_control_flags['StopTest'] == True:
                raise TestStopped
            if test_control_flags['SkipTest'] == True:
                raise TestSkipped
            
    ################################################################################
    def get_dict(self)->dict:
        """Return a dictionary containing the details of the LoadRange object."""
        d = {'name':self.name, 
             'initial_soak':self.initial_soak, 
             'soak_per_line':self.soak_per_line, 
             'soak_per_load':self.soak_per_load, 
             'integration_time':self.integration_time, 
             'custom':self.custom}
        return d

class SoaktimeSettings:
    """ Container class for the different soaktime settings
    """
    SOAK_LOAD_REG = SoakTime(
        name="Load Regulation", 
        initial=600,
        line=600,
        load=60,
        integration=0,
        custom = False)
    
    SOAK_LINE_REG = SoakTime(
        name="Line Regulation", 
        initial=600,
        line=60,
        load=60,
        integration=0,
        custom = False)
    
    SOAK_EFF = SoakTime(
        name="Efficiency", 
        initial=1800,
        line=1800,
        load=60,
        integration=0,
        custom = False)
    
    SOAK_NO_LOAD = SoakTime(
        name="No Load", 
        initial=900,
        line=900,
        load=0,
        integration=300,
        custom = False)
    
    SOAK_INPUT_HARMONICS = SoakTime(
        name="Input Harmonics", 
        initial=600,
        line=600,
        load=0,
        integration=0,
        custom = False)
    
    SOAK_CVCC = SoakTime(
        name="CVCC", 
        initial=10,
        line=10,
        load=2,
        integration=0,
        custom = False)

    SOAK_TEST = SoakTime(
        name="TEST", 
        initial=2,
        line=1,
        load=2,
        integration=1,
        custom = False)
    
    SOAK_CUSTOM = SoakTime(
        name="Custom", 
        initial=0,
        line=0,
        load=0,
        integration=0,
        custom = True)
    

    def __init__(self):

        # Create a list containing the soaktime settings
        self.soaktime_list:list[SoakTime] = []

        # Add the predetermined soaktime settings
        self.add_soaktime(self.SOAK_LOAD_REG)
        self.add_soaktime(self.SOAK_LINE_REG)
        self.add_soaktime(self.SOAK_EFF)
        self.add_soaktime(self.SOAK_NO_LOAD)
        self.add_soaktime(self.SOAK_CVCC)
        self.add_soaktime(self.SOAK_INPUT_HARMONICS)
        self.add_soaktime(self.SOAK_TEST)
        self.add_soaktime(self.SOAK_CUSTOM)
        
        self.default_list_names = list(x.name for x in self.soaktime_list)


    def add_soaktime(self, soaktime:SoakTime):
        self.soaktime_list.append(soaktime)
    
    def read_user_settings(self):
        """Read the custom soak time settings that are stored in the documents folder"""
        # Check if the file already exists
        if not os.path.exists(soak_settings_filepath):
            # If it doesn't exist, write the defaults
            self.write_user_settings()
        
        # If the settings file already exists
        else:
            # Open the file as json to read its contents
            with open(soak_settings_filepath, "r") as soaktime_settings_file:
                soak_settings_list = json.load(soaktime_settings_file)
            
            # Go through each setting
            # Add it to the current settings only if isn't already defined
            # self.line_range_list.clear()
            for soak_settings_dict in soak_settings_list:
                self.add_dict_to_soaktime_list(soak_settings_dict)
    
    def add_dict_to_soaktime_list(self, soak_settings_dict:dict):
        """Add the load range to the list only if it isn't already defined."""

        match_found = False
        # Loop through the values in the load range list
        # and check if the tested object already exists
        for count, range in enumerate(self.soaktime_list):
            # Ignore if stored is equal to the tested value
            if range.name == soak_settings_dict['name'] and \
                    range.initial_soak == soak_settings_dict['initial_soak'] and \
                    range.soak_per_line == soak_settings_dict['soak_per_line'] and \
                    range.soak_per_load == soak_settings_dict['soak_per_load'] and \
                    range.integration_time == soak_settings_dict['integration_time']:
                match_found = True
                break
            # Overwrite the soaktime settings if the name already exists
            if range.name == soak_settings_dict['name']:
                if soak_settings_dict['custom'] and \
                    soak_settings_dict['name'] not in self.default_list_names:
                    self.soaktime_list[count].initial_soak = soak_settings_dict['initial_soak']
                    self.soaktime_list[count].soak_per_line = soak_settings_dict['soak_per_line']
                    self.soaktime_list[count].soak_per_load = soak_settings_dict['soak_per_load']
                    self.soaktime_list[count].integration_time = soak_settings_dict['integration_time']
                match_found = True
                break
        
        if not match_found:
            new_soaktime_setting = SoakTime(
                name=soak_settings_dict['name'],
                initial=soak_settings_dict['initial_soak'],
                line=soak_settings_dict['soak_per_line'],
                load=soak_settings_dict['soak_per_load'],
                integration=soak_settings_dict['integration_time'],
                custom=soak_settings_dict['custom'])
            self.soaktime_list.append(new_soaktime_setting)
            
    def write_user_settings(self):
        """Write the user settings from memory to the json file"""
        obj_list = []
        for soaktime_setting in self.soaktime_list:
            d = soaktime_setting.get_dict()
            obj_list.append(d)
        
        with open(soak_settings_filepath, 'w') as settings_file:
            json.dump(obj_list, settings_file, indent=2)

class CVCCSettings:
    """Container class for the different CVCC test parameters"""
    def __init__(
        self, 
        multiple_setpoints:bool = False,
        nom_vout_V:float = 0,
        max_current_A:float = 0,
        min_current_A:float = 0,
        step_size_A:float = 0):
        """Define the class using the UI fields"""
        self.multiple_setpoints = multiple_setpoints
        self.nom_vout_V = nom_vout_V
        self.max_current_A = max_current_A
        self.min_current_A = min_current_A
        self.step_size_A = step_size_A

        self.iout_setpoints = []

        self.process_inputs()

    def process_inputs(self):
        """Return the list of current set points from the input."""
        # If multiple_setpoints is true, create a list from the range
        if self.multiple_setpoints:
            iout_setpoints = np.round(np.arange(
                self.min_current_A, self.max_current_A, self.step_size_A),6)\
                .tolist()
            iout_setpoints.append(self.max_current_A)
        # If multiple_setpoints is false, return the max current in a list
        else:
            iout_setpoints = [self.max_current_A] 

        self.iout_setpoints = iout_setpoints        



from equipment.power_meter import PowerMeter
from equipment.ac_source import ACSource
from equipment.electronic_load import ElectronicLoadModule

class TestData():

    def __init__(self):
        self.vin_V = 0
        self.iin_mA = 0
        self.ac_freq_Hz = 0
        self.pin_W = 0
        self.PF = 0
        self.thd_pct = 0
        self.vout_V = 0
        self.iout_A = 0
        self.pout_W = 0
        self.vreg_pct = 0
        self.vreg_limit_pct = 5
        self.eff_pct = 0
        
        self.vreg_passfail = ''
        self.vin_set_V = None

        # Test settings
        self.measure_ripple = False
        self.output_ripple_mV = None
        self.vout_nom_V = None
        self.ac_freq_Hz = None
        self.use_eload_data = False

        # Equipment
        self.source_power_meter:PowerMeter = None
        self.load_power_meter:PowerMeter = None
        self.electronic_load:ElectronicLoadModule = None
    
    
    def gather_data(self, 
                    integrate: bool = True, 
                    measure_thd: bool = True, 
                    coupling:str = 'AC',
                    force_use_eload_data = False,
                    usb_pd: bool = False):
        
        # Source measurement
        self.vin_V = self.source_power_meter.voltage
        self.iin_mA = self.source_power_meter.current
        self.PF = self.source_power_meter.pf
        
        # Determine whether load power meter is present and active
        has_load_pm = (self.load_power_meter is not None) and (not self.use_eload_data) and (not force_use_eload_data)
        
        source_timer = self.source_power_meter.get_integration_timer() if self.source_power_meter else 0
        load_timer = self.load_power_meter.get_integration_timer() if has_load_pm else None
        
        if source_timer == 0 or (has_load_pm and load_timer == 0):
            integrate = False

        if not integrate:
            self.pin_W = self.source_power_meter.power

        # Load measurement
        if self.use_eload_data or force_use_eload_data or (self.load_power_meter is None):
            if self.electronic_load is not None:
                self.vout_V = self.electronic_load.voltage
                self.iout_A = self.electronic_load.current
                if self.vout_V is not None and self.iout_A is not None:
                    self.pout_W = self.vout_V * self.iout_A
                else:
                    self.pout_W = 0
            else:
                self.vout_V = 0
                self.iout_A = 0
                self.pout_W = 0
        else:
            self.vout_V = self.load_power_meter.voltage
            self.iout_A = self.load_power_meter.current
        
        # Integrate the power for both source and load if applicable
        if integrate and has_load_pm:
            self.synchronous_integration()
        else:
            if integrate:
                self.source_power_meter.start_integration()
                self.source_power_meter.poll_integration_status()
                self.pin_W = self.source_power_meter.get_integrated_power()
            
            if has_load_pm:
                if not integrate:
                    self.pout_W = self.load_power_meter.power
                
        # Fallback for Pin if None
        if self.pin_W is None:
            self.pin_W = self.source_power_meter.power if self.source_power_meter else 0
            
        # Fallback for Pout if None
        if self.pout_W is None:
            if has_load_pm:
                self.pout_W = self.load_power_meter.power
            elif self.vout_V is not None and self.iout_A is not None:
                self.pout_W = self.vout_V * self.iout_A
            else:
                self.pout_W = 0

        # THD is placed AFTER power measurement so it doesn't flush the power meter buffer
        if measure_thd and not (coupling == 'DC'):
            self.thd_pct = self.source_power_meter.thd
        else:
            self.thd_pct = None

        # Measurement handling
        if self.vin_V is None:
            self.vin_V = 0
            
        if self.iin_mA is None:
            self.iin_mA = 0
        else:
            self.iin_mA = self.iin_mA * 1000
        
        if self.pin_W is None:
            self.pin_W = 0
            
        if self.pout_W is None:
            self.pout_W = 0
        
        if self.pin_W == 0:
            self.eff_pct = 0
        else:
            self.eff_pct = self.pout_W / self.pin_W * 100
        
        if self.PF is None:
            self.PF = 0
        
        if self.thd_pct is None:
            self.thd_pct = 0
        
        if self.vout_V is None:
            self.vout_V = 0
            self.vreg_pct = 1000
        else:
            self.vreg_pct = (self.vout_V - self.vout_nom_V) / self.vout_nom_V * 100
        
        if self.iout_A is None:
            self.iout_A = 0
            
        if usb_pd and (round(self.vout_nom_V, 2) == 5.00):
            if (self.vout_V > 5.5) or (self.vout_V < 4.75):
                self.vreg_passfail = 'FAIL'
            else:
                self.vreg_passfail = 'PASS'
        else:
            if abs(self.vreg_pct) > self.vreg_limit_pct:
                self.vreg_passfail = 'FAIL'
            else:
                self.vreg_passfail = 'PASS'
            
    
    def gather_data_source(self, 
                           integrate:bool = True, 
                           measure_thd:bool = True, 
                           coupling:str = 'AC'):
        # Source measurement
        self.vin_V = self.source_power_meter.voltage
        self.iin_mA = self.source_power_meter.current
        self.PF = self.source_power_meter.pf

        source_timer = self.source_power_meter.get_integration_timer() if self.source_power_meter else 0
        if source_timer == 0:
            integrate = False

        if not integrate:
            self.pin_W = self.source_power_meter.power

        # Integrate the power for the source
        if integrate:
            self.source_power_meter.start_integration()
            self.source_power_meter.poll_integration_status()
            self.pin_W = self.source_power_meter.get_integrated_power()
            
        if self.pin_W is None:
            self.pin_W = self.source_power_meter.power if self.source_power_meter else 0
            
        # THD is placed AFTER integration so it doesn't flush the power meter buffer
        if measure_thd and not (coupling == 'DC'):
            self.thd_pct = self.source_power_meter.thd
        else:
            self.thd_pct = None  
        
        if self.vin_V is None:
            self.vin_V = 0
            
        if self.iin_mA is None:
            self.iin_mA = 0
        else:
            self.iin_mA = self.iin_mA * 1000
        
        if self.pin_W is None:
            self.pin_W = 0
        
        if self.PF is None:
            self.PF = 0
        
        if self.thd_pct is None:
            self.thd_pct = 0
    
    def gather_data_load(self, 
                         integrate:bool = True, 
                         force_use_eload_data:bool = False,
                         usb_pd:bool = False):
        
        # Load measurement
        if self.use_eload_data or force_use_eload_data or (self.load_power_meter is None):
            if self.electronic_load is not None:
                self.vout_V = self.electronic_load.voltage
                self.iout_A = self.electronic_load.current
                if self.vout_V is not None and self.iout_A is not None:
                    self.pout_W = self.vout_V * self.iout_A
                else:
                    self.pout_W = 0
            else:
                self.vout_V = 0
                self.iout_A = 0
                self.pout_W = 0
        else:
            self.vout_V = self.load_power_meter.voltage
            self.iout_A = self.load_power_meter.current
            
            # Integrate the power for the load
            load_timer = self.load_power_meter.get_integration_timer() if self.load_power_meter else 0
            if load_timer == 0:
                integrate = False
                
            if integrate and not force_use_eload_data:
                self.load_power_meter.start_integration()
                self.load_power_meter.poll_integration_status()
                self.pout_W = self.load_power_meter.get_integrated_power()
            else:
                self.pout_W = self.load_power_meter.power

        if self.vout_V is None:
            self.vout_V = 0
            self.vreg_pct = 1000
        else:
            self.vreg_pct = (self.vout_V - self.vout_nom_V) / self.vout_nom_V * 100

        if usb_pd and (round(self.vout_nom_V, 2) == 5.00):
            if (self.vout_V > 5.5) or (self.vout_V < 4.75):
                self.vreg_passfail = 'FAIL'
            else:
                self.vreg_passfail = 'PASS'
        else:
            if abs(self.vreg_pct) > self.vreg_limit_pct:
                self.vreg_passfail = 'FAIL'
            else:
                self.vreg_passfail = 'PASS'
        
        if self.iout_A is None:
            self.iout_A = 0
        
        if self.pout_W is None:
            self.pout_W = 0

    def gather_data_load_minimal(self):
        # if self.use_eload_data == True:
        self.vout_V = self.load_power_meter.voltage
        self.iout_A = self.load_power_meter.current
        self.pout_W = self.vout_V*self.iout_A
            
    def synchronous_integration(self):
        """Gather data from source and load at the same time"""
        self.source_power_meter.start_integration()
        self.load_power_meter.start_integration()

        self.source_power_meter.poll_integration_status()
        self.load_power_meter.poll_integration_status()

        self.pin_W = self.source_power_meter.get_integrated_power()
        self.pout_W = self.load_power_meter.get_integrated_power()

    def get_eload_meas(self):
        self.vout_V = self.electronic_load.voltage
        self.iout_A = self.electronic_load.current

    def copy_settings(self, td, include_load:bool = False):
        """Copy the settings including test parameters and equipment from another TestData object
        
        td: TestData            another TestData Object
        include_load: bool      enable to also copy load equipment"""
        self.vout_nom_V = td.vout_nom_V
        self.use_eload_data = td.use_eload_data
        self.source_power_meter = td.source_power_meter
        if include_load:
            self.load_power_meter = self.power_meter_load
            self.electronic_load =  self.electronic_load_1


class USBPDOptions():    
    def __init__(
        self, 
        usbpd_test: bool = False,
        tracking_pdo_request: bool = False,
        pdo_type: SUPPLY_TYPE = SUPPLY_TYPE.FIXED,
        augmented_type: AUGMENTED_TYPE = None
        ):
        
        """
        
        Keyword arguments:
        usbpd_test              --      flag whether test is for usbpd psu
        tracking_pdo_request    --      Max current of pdo request tracks test condition
        """
        self.usbpd_test = usbpd_test
        self.tracking_pdo_request = tracking_pdo_request
        self.pdo_type = pdo_type
        self.augmented_type = augmented_type

class GeneralOptions():
    def __init__(
        self,
        measure_ripple: bool = False,
        use_eload_data: bool = False,
        eload_type: str = 'CC',
        load_direction:str = 'Downward',
        coupling:str = 'AC'):
        """General power supply test options"""
        self.measure_ripple = measure_ripple
        self.use_eload_data = use_eload_data
        self.eload_type = eload_type
        self.load_direction = load_direction
        self.coupling = coupling
        
class LineRamp():
    def __init__(self, name='', vin_slew=[], freq = 60, coupling = 'AC', custom=False, *args, **kwargs):
        self.name = name
        self.vin_slew:list = vin_slew
        self.freq = freq
        self.coupling = coupling
        self.custom = custom

    def add_vin_slew(self, vin:float, slew:float):
        """ Add a VIN and Frequency pair to the range list
        """
        self.vin_slew.append([vin, slew])


    def delete_vin_slew(self, index):
        """ Remove a VIN and Frequency pair from the range list
        """
        self.vin_slew.pop(index)

    def get_dict(self)->dict:
        """Return a dictionary containing the details of the LineRange object."""
        d = {'name':        self.name, 
            'vin_slew':    self.vin_slew,
            'freq':       self.freq,
            'coupling':   self.coupling,
            'custom':      self.custom
             }
        return d
    
    def init_from_dict(self, dict):
        """Initialize the object from a dictionary input."""
        self.name = dict['name']
        self.vin_slew = dict['vin_slew']
        self.freq = dict['freq']
        self.coupling = dict['coupling']
        self.custom = dict['custom']

class LineRampSettings():
    
    RAMP_BROWN_IN = LineRamp(
        name="Brown-in", 
        vin_slew = [ [60, 0.1], [130, 1e30] ],
        freq = 60,
        coupling = 'AC',
        custom = False)
    
    RAMP_BROWN_OUT = LineRamp(
        name="Brown-out", 
        vin_slew = [ [130, 0.1], [60, 1e30] ],
        freq = 60,
        coupling = 'AC',
        custom = False)
    
    RAMP_OVERVOLTAGE_UP= LineRamp(
        name="Overvoltage Ramp up", 
        vin_slew = [ [265, 0.1], [300, 1e30] ],
        freq = 50,
        coupling = 'AC',
        custom = False)
    
    RAMP_OVERVOLTAGE_DOWN = LineRamp(
        name="Overvoltage Ramp down", 
        vin_slew = [ [300, 0.1], [265, 1e30] ],
        freq = 50,
        coupling = 'AC',
        custom = False)
    
    RAMP_BROWN_IN_BROWN_OUT = LineRamp(
        name="Brown-in - Brown-out", 
        vin_slew = [ [60, 0.1], [130, 0.1], [60,1e30] ],
        freq = 60,
        coupling = 'AC',
        custom = False)
    
    RAMP_OVERVOLTAGE_FULL = LineRamp(
        name="Overvoltage Ramp up - down", 
        vin_slew = [ [265, 0.1], [300,0.1],[265, 1e30] ],
        freq = 60,
        coupling = 'AC',
        custom = False)
    
    RAMP_BROWN_IN_OV_BROWN_OUT = LineRamp(
        name="Brown-in - OV - Brown-out", 
        vin_slew = [ [60, 0.1], [130, 1e30], [265, 0.1], [300,0.1], [265, 1e30], [130, 0.1], [60, 1e30] ],
        freq = 50,
        coupling = 'AC',
        custom = False)
    
    RAMP_CUSTOM = LineRamp(
        name="Custom", 
        initial=[],
        freq = 60,
        coupling = 'AC',
        custom = True)
    
    def __init__(self):
        # Create a list containing the soaktime settings
        self.line_ramp_list:list[LineRamp] = []
        self.set_ranges()
        self.default_list_names = list(x.name for x in self.line_ramp_list)

    def set_ranges(self):
        # Add the predetermined soaktime settings
        self.add_line_ramp_setting(self.RAMP_BROWN_IN)
        self.add_line_ramp_setting(self.RAMP_BROWN_OUT)
        self.add_line_ramp_setting(self.RAMP_OVERVOLTAGE_UP)
        self.add_line_ramp_setting(self.RAMP_OVERVOLTAGE_DOWN)
        self.add_line_ramp_setting(self.RAMP_BROWN_IN_BROWN_OUT)
        self.add_line_ramp_setting(self.RAMP_OVERVOLTAGE_FULL)
        self.add_line_ramp_setting(self.RAMP_BROWN_IN_OV_BROWN_OUT)
        self.add_line_ramp_setting(self.RAMP_CUSTOM)

    def add_line_ramp_setting(self, line_ramp:LineRamp):
        self.line_ramp_list.append(line_ramp)
        
    def read_user_settings(self):
        """Read the custom line settings that are stored in the documents folder"""
        # Check if the file already exists
        if not os.path.exists(line_ramp_settings_filepath):
            # If it doesn't exist, write the defaults
            self.write_user_settings()
        
        # If the settings file already exists
        else:
            # Open the file as json to read its contents
            with open(line_ramp_settings_filepath, "r") as line_ramp_settings_file:
                line_ramp_settings_list = json.load(line_ramp_settings_file)
            
            # Go through each setting
            # Add it to the current settings only if isn't already defined
            # self.line_range_list.clear()
            for line_ramp_dict in line_ramp_settings_list:
                self.add_dict_to_ramp_list(line_ramp_dict)
    
    def add_dict_to_ramp_list(self, line_ramp_dict:dict):
        """Add the line range to the list only if it isn't already defined."""

        match_found = False
        # Loop through the values in the line range list
        # and check if the tested object already exists
        for count, range in enumerate(self.line_ramp_list):
            # Ignore if stored is equal to the tested value
            if range.name == line_ramp_dict['name'] and \
                range.vin_slew == line_ramp_dict['vin_slew'] and \
                range.freq == line_ramp_dict['freq'] and \
                range.coupling == line_ramp_dict['coupling']:
                    
                match_found = True
                break
            
            # Overwrite the vin_freq if the name already exists
            if range.name == line_ramp_dict['name']:
                if line_ramp_dict['custom'] and \
                    line_ramp_dict['name'] not in self.default_list_names:
                        
                    self.line_ramp_list[count].vin_slew = line_ramp_dict['vin_slew']
                    self.line_ramp_list[count].freq = line_ramp_dict['freq']
                    self.line_ramp_list[count].coupling = line_ramp_dict['coupling']
                    
                match_found = True
                break
        
        if not match_found:
            new_line_ramp = LineRamp(
                name=line_ramp_dict['name'],
                vin_slew=line_ramp_dict['vin_slew'],
                freq=line_ramp_dict['freq'],
                coupling=line_ramp_dict['coupling'],
                custom=line_ramp_dict['custom'])
            self.line_ramp_list.append(new_line_ramp)
            

    def write_user_settings(self):
        """Write the user settings from memory to the json file"""
        obj_list = []
        for line_ramp in self.line_ramp_list:
            d = line_ramp.get_dict()
            obj_list.append(d)
        
        with open(line_ramp_settings_filepath, 'w') as settings_file:
            json.dump(obj_list, settings_file, indent=2)

    def add_vin_slew(self, line_ramp, vin, slew):
        """Add a vin slew to the line ramp setting given"""
        # Get the index of the line range in the list
        for i, item in enumerate(self.line_ramp_list):
            if item.name == line_ramp.name:
                index = i
                line_ramp_item:LineRamp = item
        
        line_ramp_item.add_vin_slew(vin, slew)
    
    def delete_vin_slew(self, line_ramp, index):
        """Remove the line ramp entry specified"""
        # Get the index of the line range in the list
        for i, item in enumerate(self.line_ramp_list):
            if item.name == line_ramp.name:
                index = i
                line_ramp_item:LineRamp = item
        
        line_ramp_item.delete_vin_slew(index)
        
class I2CTestParameters():
    """Generic UI parameters from the UI.
    The assignment of these parameters vary per test."""

    def __init__(self, params=[0]*10, cbx_params=[0]*4):
        self.param = [0]*10
        self.cbx_param = [0]*4
        for index, parameter in enumerate(params):
            self.param[index] = parameter

        for index, parameter in enumerate(cbx_params):
            self.cbx_param[index] = parameter

class TestConditions():
    """Container of all the test conditions that a TestObject will need
    """
    def __init__(
        self,
        nominal_output_voltage_V: float,
        nominal_load_current_A: float,
        max_load_current_A: float,
        line_range: LineRange = LineRange(),
        load_range: LoadRange = LoadRange(),
        soak_time: SoakTime = SoakTime(),
        general_options: GeneralOptions = GeneralOptions(),
        usbpd_options: USBPDOptions = USBPDOptions(),
        cvcc_settings: CVCCSettings = CVCCSettings(),
        line_ramp_settings: LineRamp = LineRamp(),
        i2c_test_parameters: I2CTestParameters = I2CTestParameters(),
        name: str = "",
        **kwargs):
        """Expand this later with different test types
        Default options will be used if Options Object is specified
        """
        self.name = name
        self.nominal_output_voltage_V = nominal_output_voltage_V
        self.nominal_load_current_A = nominal_load_current_A
        self.max_load_current_A = max_load_current_A
        self.line_range = line_range
        self.load_range = load_range
        self.soak_time = soak_time
        self.general_options = general_options
        self.usbpd_options = usbpd_options
        self.cvcc_settings = cvcc_settings
        self.line_ramp_settings = line_ramp_settings
        self.i2c_test_parameters = i2c_test_parameters
    
# TODO: Change implementation
# One way is to define these defaults inside the tests such that this class
# will just need to pull the test conditions from the classes that are defined

from psu_tests.test_type import *

class TestConditionSettings():
    """ Container class for the different test condition settings
    """

    def __init__(self):

        # Create a list containing the test condition settings
        self.test_condition_list:list[TestConditions] = []
        
        for test_type in TestTypes:
            # Add the predetermined test condition settings
            self.add_test_condition(test_type.tc_default)

    def add_test_condition(self, test_condition:TestConditions):
        self.test_condition_list.append(test_condition)


