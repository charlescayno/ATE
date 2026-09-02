from equipment.equipment import Equipment, visa_io
from equipment.definitions import ELECTRONIC_LOAD_MODULES_LIST, ELECTRONIC_LOAD_MODULES_PROG_LIST
from equipment.eload_specs import EloadModuleBaseClass, EloadStatus, ELoadTypes,Eload_Chroma_Prog_Group1

from misc_functions.misc_functions import *

from typing import TYPE_CHECKING


from pyvisa.resources.resource import Resource

class ElectronicLoadMainframe(Equipment):
    def __init__(self, device, device_id):
        super().__init__(device, device_id)

        # Inherited objects start
        self.device: Resource
        self.device_id: str
        # Inherited objects end

        # Details of the currently selected channel
        self.current_channel = 0

        # Channel ID is a list of the 4 items below it
        self.current_channel_id = []
        self.current_channel_model = ''
        self.current_channel_manufacturer = ''
        self.current_channel_serial = ''
        self.current_channel_fw_version = ''

        self.connected_channels = []

        self.eload_modules: list[ElectronicLoad] = []

    def get_eload_module_objects(self):
        """ Create ElectronicLoadModule objects for each eload module 

        """
        self.get_connected_channels()

        # Empty the modules container first before doing the check
        self.eload_modules.clear()

        # Create an ElectronicLoadModule object for each connected channel
        for channel in self.connected_channels:
            # Get the channel ID for the channel in iteration
            self.set_current_channel(channel_number=channel)
            self.get_channel_id()

            self.eload_modules.append(ElectronicLoadModule(
                mainframe_device=self.device,
                mainframe_id=self.device_id,
                channel_id=self.current_channel_id,
                channel=channel
            ))

        return self.eload_modules

    def get_connected_channels(self):
        """ Check

        """
        self.get_channel_id()

        # Empty the list of connected channels
        self.connected_channels.clear()

        # Empty the list of eload module objects
        self.eload_modules.clear()

        # If manufacturer field is empty, it means that there
        # is no module connected to the eload mainframe
        if self.current_channel_manufacturer == '':
            return self.connected_channels

        # To check the channels, a known connected channel is used as a reference
        known_connected_channel = self.get_current_channel_number()

        # To check if a channel is active, first set the known connected channel
        # Then change the channel to the one being tested
        # If the current channel changed after a query then the channel being tested is connected
        # If not, then it is empty

        # Test channels 1 to 8
        for channel_num in range(1, 9):

            # If tested channel is the known connected channel
            # No need to test
            if channel_num == known_connected_channel:
                self.connected_channels.append(channel_num)

            else:
                # Else, set the known connected channel first
                self.set_current_channel(known_connected_channel)

                # Then change the channel to the one being tested
                self.set_current_channel(channel_num)
                self.get_current_channel_number()

                # If the channel number changed to the one that was set
                # Then that channel is connected
                if self.current_channel == channel_num:
                    self.connected_channels.append(channel_num)

    @visa_io
    def get_channel_id(self):
        channel_id = self.write(f'CHAN:ID?')

        # Split the channel ID into a listo of its contents
        self.current_channel_id = self.split_device_id(channel_id)

        # Separate the channel into individual variables
        self.current_channel_manufacturer, self.current_channel_model, \
            self.current_channel_serial, self.current_channel_fw_version \
            = self.current_channel_id

    @visa_io
    def get_current_channel_number(self):
        self.current_channel = int(self.write('CHAN?'))
        return self.current_channel

    @visa_io
    def set_current_channel(self, channel_number):
        """ Set the channel of the Eload module that will receive the command

        """
        self.write(f'CHAN {channel_number}')


class ElectronicLoadModule(Equipment):
    """ An electronic load module needs to set the channel first before issuing commands
    to the load module.
    """

    def __init__(self, mainframe_device: Resource, mainframe_id, channel_id, channel):
        super().__init__(mainframe_device, mainframe_id)
        # Use the visa resource of the mainframe for communication
        self.device = mainframe_device
        self.mainframe_model = self.model
        # The channel needs to be sent whenever there are commands to be issued to this module
        self.channel = channel

        # List containing Manufacturer, Model, Serial and FW Version
        self.channel_id = channel_id
        self.manufacturer = channel_id[0]
        self.model = channel_id[1]
        self.serial = channel_id[2]
        self.fw_version = channel_id[3]

        # Measurement Parameters
        self._cv = 0
        self._cc = 0
        self._cr = 0
        self._cp = 0
        self._cv_current = 0
        
        self._led_voltage = 0
        self._led_current = 0
        self._von = 0
        self._voltage = 0
        self._current = 0
        self._power = 0

        self._active_level = '1'
        self.active_channel_status = EloadStatus.OFF
        self.active_channel_short = 0

        # TODO: Determine spec limits based on model
        # e.g. CR limits for CRL and CRL, etc.
        self.set_spec_limits()
        
        self.active_channel_voltage = self.crh_max_v
        self.active_channel_power = self.cch_max_power_w

        last = self.device.resource_name.rfind("::")
        addr = self.device.resource_name[:last]
        self.description = f'{self.manufacturer} {self.mainframe_model} {self.model} Ch{self.channel}  {addr}'
        self._cc = self.cc_static_l1
        self._cr = self.cr_l1
        self._cp = self.cp_l1
        self._cv = self.cv_l1

    def set_spec_limits(self):
        # Take the model number from the channel ID
        model = self.channel_id[1]

        eload_model = ELECTRONIC_LOAD_MODULES_LIST[model]

        # create an instance of the specified eload model to use its specs
        eload_object: EloadModuleBaseClass = eload_model()
        
        self.prog_func:Eload_Chroma_Prog_Group1 =  ELECTRONIC_LOAD_MODULES_PROG_LIST[eload_model]

        # LOADING MODES
        self.load_modes = eload_object.MODES
        
        self.mode_range_count = eload_object.MODE_RANGE_COUNT

        self.multi_channel = eload_object.MULTI_CHANNEL
        
        self.cr_slew_available = eload_object.CR_SLEW_AVAILABLE
        
        self.cp_slew_unit = eload_object.CP_SLEW_UNIT

        # SLEW RATE LIMITS
        self.h_slew_min = eload_object.H_SLEW_MIN
        self.h_slew_max = eload_object.H_SLEW_MAX
        self.l_slew_min = eload_object.L_SLEW_MIN
        self.l_slew_max = eload_object.L_SLEW_MAX

        # # CCX MODE LIMITS
        self.cch_max_a = eload_object.CCH_MAX_A
        self.ccl_max_a = eload_object.CCL_MAX_A
        self.cch_max_power_w = eload_object.CCH_MAX_POWER_W
        self.ccl_max_power_w = eload_object.CCL_MAX_POWER_W

        # CR
        self.crh_min_r = eload_object.CRH_MIN_R
        self.crh_max_r = eload_object.CRH_MAX_R

        self.crl_min_r = eload_object.CRL_MIN_R
        self.crl_max_r = eload_object.CRL_MAX_R

        self.crl_max_v = eload_object.CRL_MAX_V
        self.crh_max_v = eload_object.CRH_MAX_V
        
        self.crl_max_a = eload_object.CRL_MAX_A
        self.crh_max_a = eload_object.CRH_MAX_A
        
        self.ccd_t_min_s = eload_object.CCD_T_MIN_S
        self.ccd_t_max_s = eload_object.CCD_T_MAX_S

        self.cv_max_v = eload_object.CV_MAX_V
        
        if ELoadTypes.CP in self.load_modes:
            self.cph_min_w = eload_object.CPH_MIN_W
            self.cpl_min_w = eload_object.CPL_MIN_W
            self.cph_max_w = eload_object.CPH_MAX_W
            self.cpl_max_w = eload_object.CPL_MAX_W
            
            self.cph_slew_min = eload_object.CPH_SLEW_MIN
            self.cph_slew_max = eload_object.CPH_SLEW_MAX
            self.cpl_slew_min = eload_object.CPL_SLEW_MIN
            self.cpl_slew_max = eload_object.CPL_SLEW_MAX
        else:
            self.cph_min_w = 0
            self.cpl_min_w = 0
            self.cph_max_w = eload_object.CCH_MAX_POWER_W
            self.cpl_max_w = eload_object.CCL_MAX_POWER_W
            
            self.cph_slew_min = eload_object.H_SLEW_MIN
            self.cph_slew_max = eload_object.H_SLEW_MAX
            self.cpl_slew_min = eload_object.L_SLEW_MIN
            self.cpl_slew_max = eload_object.L_SLEW_MAX
        
        if self.mode_range_count  == 3:
            # SLEW RATE LIMITS
            self.m_slew_min = eload_object.M_SLEW_MIN
            self.m_slew_max = eload_object.M_SLEW_MAX
            
            # # CCX MODE LIMITS
            self.ccm_max_a = eload_object.CCM_MAX_A
            self.ccm_max_power_w = eload_object.CCM_MAX_POWER_W

            # CR
            self.crm_min_r = eload_object.CRM_MIN_R
            self.crm_max_r = eload_object.CRM_MAX_R

            self.crm_max_v = eload_object.CRM_MAX_V
            
            self.crm_max_a = eload_object.CRM_MAX_A
            
            if ELoadTypes.CP in self.load_modes:
                self.cpm_min_w = eload_object.CPM_MIN_W
                self.cpm_max_w = eload_object.CPM_MAX_W
                
                self.cpm_slew_min = eload_object.CPM_SLEW_MIN
                self.cpm_slew_max = eload_object.CPM_SLEW_MAX
            else:
                self.cpm_min_w = 0
                self.cpm_max_w = eload_object.CCM_MAX_POWER_W
                
                self.cpm_slew_min = eload_object.M_SLEW_MIN
                self.cpm_slew_max = eload_object.M_SLEW_MAX            

    def reset_values(self):
        # Set CRL to CRH min resistance
        # self.set_load(vout_V=self.crl_max_v*0.8, 
        #               iout_A= self.crl_max_v*0.8/self.crh_min_r,
        #               mode=ELoadTypes.CR)
                            # self.turn_off()
        self.turn_off()
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.write(f'{self.prog_func.mode} CRH') 
        self.write(f'{self.prog_func.resistance}:L{self._active_level} {self.crh_min_r}')
        
    def turn_on_all(self):
        for i in range(1, 9):
            self.channel[i].turn_on()

    def turn_off_all(self):
        for i in range(1, 9):
            self.channel[i].turn_off()

    def cleanup(self):
        self.turn_off_all()
        self.close()

    def set_active_level(self, level:int):
        self._active_level = f'{round(level):g}'
        
    def get_active_level(self):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.active_channel_mode = self.write(f'{self.prog_func.mode}?')
        if self.active_channel_mode in ['CCL','CCM','CCH',]:
            if abs(self._cc - self.cc_static_l2) <= self.cc_static_l2 *0.05:
                self._active_level = '2'
            else:
                self._active_level = '1'
        elif self.active_channel_mode in ['CRL','CRM','CRH']:
            if abs(self._cr - self.cr_l2) <= self.cr_l2*0.05:
                
                self._active_level = '2'
            else:
                self._active_level = '1'
        elif self.active_channel_mode in ['CPL','CPM','CPH']:
            if abs(self._cp - self.cp_l2) <= self.cp_l2*0.05:
                
                self._active_level = '2'
            else:
                self._active_level = '1'
        return self._active_level

    @visa_io
    def dynamic(self, low, high, ton, toff, rise, fall):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.write(f'{self.prog_func.current_dynamic}:L1 {low}')
        self.write(f'{self.prog_func.current_dynamic}:L2 {high}')
        self.write(f'{self.prog_func.current_dynamic}:{self.prog_func.rise} {rise}')
        self.write(f'{self.prog_func.current_dynamic}:{self.prog_func.fall} {fall}')
        self.write(f'{self.prog_func.current_dynamic}:T1 {ton}')
        self.write(f'{self.prog_func.current_dynamic}:T2 {toff}')

    @property
    @visa_io
    def voltage(self):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._voltage = float(self.write(f'{self.prog_func.fetch}:VOLT?'))
        return self._voltage

    @property
    @visa_io
    def current(self):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._current = float(self.write(f'{self.prog_func.fetch}:CURR?'))
        return self._current

    @property
    def cv(self):
        return self._cv

    @property
    def cc(self):
        return self._cc
    
    @property
    def cr(self):
        return self._cr

    @property
    def led_voltage(self):
        return self._led_voltage
    
    @property
    def cp(self):
        return self._cp

    @property
    def led_current(self):
        return self._led_current

    @property
    def cc_static_rise(self):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._cc_static_rise = float(self.write(f'{self.prog_func.current_static}:{self.prog_func.rise}?'))
        return self._cc_static_rise
    
    @property
    def cc_static_fall(self):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._cc_static_fall = float(self.write(f'{self.prog_func.current_static}:{self.prog_func.fall}?'))
        return self._cc_static_fall
    
    @property
    def cc_static_l1(self):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._cc_static_l1 = float(self.write(f'{self.prog_func.current_static}:L1?'))
        return self._cc_static_l1
    
    @property
    def cc_static_l2(self):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._cc_static_l2 = float(self.write(f'{self.prog_func.current_static}:L2?'))
        return self._cc_static_l2
    
    @property
    def cr_rise(self):
        if not self.cr_slew_available:
            return 0
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._cr_rise = float(self.write(f'{self.prog_func.resistance}:{self.prog_func.rise}?'))
        return self._cr_rise
    
    @property
    def cr_fall(self):
        if not self.cr_slew_available:
            return 0
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._cr_fall = float(self.write(f'{self.prog_func.resistance}:{self.prog_func.fall}?'))
        return self._cr_fall
    
    @property
    def cr_l1(self):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._cr_l1 = float(self.write(f'{self.prog_func.resistance}:L1?'))
        return self._cr_l1
    
    @property
    def cr_l2(self):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._cr_l2 = float(self.write(f'{self.prog_func.resistance}:L2?'))
        return self._cr_l2
    
    @property
    def cp_l1(self):
        if not (ELoadTypes.CP in self.load_modes):
            print('CP mode not supported by this module')
            self._cp_l1 = None
            return
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._cp_l1 = float(self.write(f'{self.prog_func.power}:L1?'))
        return self._cp_l1
    
    @property
    def cp_l2(self):
        if not (ELoadTypes.CP in self.load_modes):
            print('CP mode not supported by this module')
            self._cp_l2 = None
            return
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._cp_l2 = float(self.write(f'{self.prog_func.power}:L2?'))
        return self._cp_l2
    
    @property
    def cp_rise(self):
        if not (ELoadTypes.CP in self.load_modes):
            print('CP mode not supported by this module')
            self._cp_rise = None
            return
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._cp_rise = float(self.write(f'{self.prog_func.power}:{self.prog_func.rise}?'))
        return self._cp_rise
    
    @property
    def cp_fall(self):
        if not (ELoadTypes.CP in self.load_modes):
            print('CP mode not supported by this module')
            self._cp_fall = None
            return
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._cp_fall = float(self.write(f'{self.prog_func.power}:{self.prog_func.fall}?'))
        return self._cp_fall
    
    @property
    def cv_l1(self):
        if not (ELoadTypes.CV in self.load_modes):
            print('CV mode not supported by this module')
            self._cv_l1 = None
            return
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._cv_l1 = float(self.write(f'{self.prog_func.voltage}:L1?'))
        return self._cv_l1
    
    @property
    def cv_l2(self):
        if not (ELoadTypes.CV in self.load_modes):
            print('CV mode not supported by this module')
            self._cv_l2 = None
            return
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._cv_l2 = float(self.write(f'{self.prog_func.voltage}:L2?'))
        return self._cv_l2
    
    @property
    def cv_current(self):
        if not (ELoadTypes.CV in self.load_modes):
            print('CV mode not supported by this module')
            self._cv_current = None
            return
        self.write(f'{self.prog_func.channel} {self.channel}')
        self._cv_current = float(self.write(f'{self.prog_func.cv_current}?'))
        return self._cv_current
        
    @property
    def von(self):
        return self._von

    # @visa_io
    @von.setter
    def von(self, voltage):
        self._von = voltage
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.write(f'{self.prog_func.config}:{self.prog_func.voltage}:ON {self._von}')

    # @visa_io
    @cv.setter
    def cv(self, voltage):
        if not (ELoadTypes.CV in self.load_modes):
            print('CV mode not supported by this module')
            self._cv = 0
            return
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.active_channel_mode = self.write(f'{self.prog_func.mode}?')
        self.active_channel_status = self.write(f'{self.prog_func.load}?')
        
        self._cv = voltage
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.write(f'{self.prog_func.mode} CV')
        self.write(f'{self.prog_func.voltage}:L{self._active_level} {self._cv}')
        
        
    @cv_current.setter
    def cv_current(self,current=None):
        if not (ELoadTypes.CV in self.load_modes):
            print('CV mode not supported by this module')
            self._cv = 0
            return
        self.write(f'{self.prog_func.channel} {self.channel}')
        if current is not None:
            self._cv_current = current
            self.write(f'{self.prog_func.mode} CV')
            self.write(f'{self.prog_func.cv_current}: {current}')    

    # @visa_io
    @cc.setter
    def cc(self, current):
        
        # Check which range is suitable
        # Prefer CCL for better adjustment resolution
        # UPDATE 4/17/2023: Need to check OPP limit
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.active_channel_mode = self.write(f'{self.prog_func.mode}?')
        self.active_channel_status = self.write(f'{self.prog_func.load}?')
        initial_channel_status = self.active_channel_status
        
        if (current <= self.ccl_max_a) & (self.active_channel_power <= 0.9*self.ccl_max_power_w):
            if not (self.active_channel_mode =='CCL'):
                if (initial_channel_status == EloadStatus.ON):
                    self.turn_off()
                self.write(f'{self.prog_func.mode} CCL')
        elif (self.mode_range_count == 3):
            if  (current <= self.ccm_max_a) & (self.active_channel_power <= 0.9*self.ccm_max_power_w):
                if not (self.active_channel_mode =='CCM'):
                    if (initial_channel_status == EloadStatus.ON):
                        self.turn_off()
                    self.write(f'{self.prog_func.mode} CCM')
        else:
            if not (self.active_channel_mode =='CCH'):
                if (initial_channel_status == EloadStatus.ON):
                    self.turn_off()
                self.write(f'{self.prog_func.mode} CCH') 
        
        self._cc = current
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.write(f'{self.prog_func.current_static}:L{self._active_level} {self._cc}')
        # print(f'Test CC {current}')
        if initial_channel_status == EloadStatus.ON:
            self.turn_on()
    
    # @visa_io
    @cc_static_rise.setter
    def cc_static_rise(self,rise):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.active_channel_mode = self.write(f'{self.prog_func.mode}?')
        if self.active_channel_mode == 'CCL':
            rise = set_in_range(rise,self.l_slew_max,self.l_slew_min)
            self.write(f'{self.prog_func.current_static}:{self.prog_func.rise} {rise:g}')
        elif (self.mode_range_count ==  3) & (self.active_channel_mode == 'CCM'):
            rise = set_in_range(rise,self.m_slew_max,self.m_slew_min)
            self.write(f'{self.prog_func.current_static}:{self.prog_func.rise} {rise:g}')
        elif self.active_channel_mode == 'CCH':
            rise = set_in_range(rise,self.h_slew_max,self.h_slew_min)
            self.write(f'{self.prog_func.current_static}:{self.prog_func.rise} {rise:g}')
    
    # @visa_io
    @cc_static_fall.setter
    def cc_static_fall(self,fall):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.active_channel_mode = self.write(f'{self.prog_func.mode}?')
        if self.active_channel_mode == 'CCL':
            fall = set_in_range(fall,self.l_slew_max,self.l_slew_min)
            self.write(f'{self.prog_func.current_static}:{self.prog_func.fall} {fall:g}')
        elif (self.mode_range_count ==  3) & (self.active_channel_mode == 'CCM'):
            fall = set_in_range(fall,self.m_slew_max,self.m_slew_min)
            self.write(f'{self.prog_func.current_static}:{self.prog_func.fall} {fall:g}')
        elif self.active_channel_mode == 'CCH':
            fall = set_in_range(fall,self.h_slew_max,self.h_slew_min)
            self.write(f'{self.prog_func.current_static}:{self.prog_func.fall} {fall:g}')

    # @visa_io
    @cr_rise.setter
    def cr_rise(self,rise):
        if not self.cr_slew_available:
            return 0
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.active_channel_mode = self.write(f'{self.prog_func.mode}?')
        if self.active_channel_mode == 'CRL':
            rise = set_in_range(rise,self.h_slew_max,self.h_slew_min)
            self.write(f'{self.prog_func.resistance}:{self.prog_func.rise} {rise:g}')
        if (self.mode_range_count ==  3) & (self.active_channel_mode == 'CRM'):
            rise = set_in_range(rise,self.m_slew_max,self.m_slew_min)
            self.write(f'{self.prog_func.resistance}:{self.prog_func.rise} {rise:g}')
        elif self.active_channel_mode == 'CRH':
            rise = set_in_range(rise,self.l_slew_max,self.l_slew_min)
            self.write(f'{self.prog_func.resistance}:{self.prog_func.rise} {rise:g}')
    
    # @visa_io
    @cr_fall.setter
    def cr_fall(self,fall):
        if not self.cr_slew_available:
            return 0
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.active_channel_mode = self.write(f'{self.prog_func.mode}?')
        if self.active_channel_mode == 'CRL':
            fall = set_in_range(fall,self.h_slew_max,self.h_slew_min)
            self.write(f'{self.prog_func.resistance}:{self.prog_func.fall} {fall:g}')
        if (self.mode_range_count ==  3) & (self.active_channel_mode == 'CRM'):
            fall = set_in_range(fall,self.m_slew_max,self.m_slew_min)
            self.write(f'{self.prog_func.resistance}:{self.prog_func.fall} {fall:g}')
        elif self.active_channel_mode == 'CRH':
            fall = set_in_range(fall,self.l_slew_max,self.l_slew_min)
            self.write(f'{self.prog_func.resistance}:{self.prog_func.fall} {fall:g}')
    
    # @visa_io
    @cr.setter
    def cr(self, resistance): 
               
        # Check which range is suitable
        # Prefer CRL for better adjustment resolution
        # UPDATE 4/17/2023: Need to check OVP limit
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.active_channel_mode = self.write(f'{self.prog_func.mode}?')
        self.active_channel_status = self.write(f'{self.prog_func.load}?')
        
        if ((resistance <= self.crl_max_r) & (self.active_channel_voltage <= 0.9*self.crl_max_v)) | ((self.active_channel_voltage/resistance) > self.crl_max_a):
            if not (self.active_channel_mode =='CRL'):
                if (self.active_channel_status == EloadStatus.ON):
                    self.turn_off()
                self.write(f'{self.prog_func.mode} CRL')          
        elif (self.mode_range_count == 3):
            if ((resistance <= self.crm_max_r) & (self.active_channel_voltage <= 0.9*self.crm_max_v)) | ((self.active_channel_voltage/resistance) > self.crm_max_a):
                if not (self.active_channel_mode =='CRM'):
                    if (self.active_channel_status == EloadStatus.ON):
                        self.turn_off()
                    self.write(f'{self.prog_func.mode} CRM') 
        else:
            if not (self.active_channel_mode =='CRH'):
                if (self.active_channel_status == EloadStatus.ON):
                    self.turn_off()
                self.write(f'{self.prog_func.mode} CRH') 
        
        # print(f'{self.prog_func.load}: {self.active_channel_mode}, {resistance}R, {self.active_channel_voltage}V')
        self._cr = resistance
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.write(f'{self.prog_func.resistance}:L{self._active_level} {self._cr}')
        
        if self.active_channel_status == EloadStatus.ON:
            self.turn_on()

    # @visa_io
    @led_voltage.setter
    def led_voltage(self, voltage):
        self._led_voltage = voltage
        # not supported yet...
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.write(f'{self.prog_func.led_voltage} {self._led_voltage}')
        self.write(f'{self.prog_func.mode} LEDH')

    # @visa_io
    @led_current.setter
    def led_current(self, current):
        self._led_current = current
        # not supported yet...
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.write(f'{self.prog_func.led_current} {self._led_current}')
        self.write(f'{self.prog_func.mode} LEDH')
        
    # @visa_io
    @cp.setter
    def cp(self, power):
        if not (ELoadTypes.CP in self.load_modes):
            print('CP mode not supported by this module')
            self._cp = self._voltage*self._current
            return
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.active_channel_mode = self.write(f'{self.prog_func.mode}?')
        self.active_channel_status = self.write(f'{self.prog_func.load}?')
        initial_channel_status = self.active_channel_status
        
        if (power <= self.cpl_max_w) & (self.active_channel_power <= 0.9*self.cpl_max_w):
            if not (self.active_channel_mode =='CPL'):
                if (initial_channel_status == EloadStatus.ON):
                    self.turn_off()
                self.write(f'{self.prog_func.mode} CPL')        
        elif (self.mode_range_count == 3):
            if (power <= self.cpm_max_w) & (self.active_channel_power <= 0.9*self.cpm_max_w):
                if not (self.active_channel_mode =='CPM'):
                    if (initial_channel_status == EloadStatus.ON):
                        self.turn_off()
                    self.write(f'{self.prog_func.mode} CPM')        
        else:
            if not (self.active_channel_mode =='CPH'):
                if (initial_channel_status == EloadStatus.ON):
                    self.turn_off()
                self.write(f'{self.prog_func.mode} CPH') 
        
        self._cp = power
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.write(f'POWER:STAT:L{self._active_level} {self._cp}')
        # print(f'Test CC {current}')
        if initial_channel_status == EloadStatus.ON:
            self.turn_on()
    
    # @visa_io
    @cp_rise.setter
    def cp_rise(self,rise):
        if not (ELoadTypes.CP in self.load_modes):
            print('CP mode not supported by this module')
            return
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.active_channel_mode = self.write(f'{self.prog_func.mode}?')
        if self.active_channel_mode == 'CPL':
            rise = set_in_range(rise,self.cpl_slew_max,self.cpl_slew_min)
            self.write(f'{self.prog_func.power}:{self.prog_func.rise} {rise:g}')
        elif (self.mode_range_count == 3) & (self.active_channel_mode == 'CPM'):
            rise = set_in_range(rise,self.cpm_slew_max,self.cpm_slew_min)
            self.write(f'{self.prog_func.power}:{self.prog_func.rise} {rise:g}')
        elif self.active_channel_mode == 'CPH':
            rise = set_in_range(rise,self.cph_slew_max,self.cph_slew_min)
            self.write(f'{self.prog_func.power}:{self.prog_func.rise} {rise:g}')
    
    # @visa_io
    @cp_fall.setter
    def cp_fall(self,fall):
        if not (ELoadTypes.CP in self.load_modes):
            print('CP mode not supported by this module')
            return
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.active_channel_mode = self.write(f'{self.prog_func.mode}?')
        if self.active_channel_mode == 'CPL':
            fall = set_in_range(fall,self.cpl_slew_max,self.cpl_slew_min)
            self.write(f'{self.prog_func.power}:{self.prog_func.fall} {fall:g}')
        elif (self.mode_range_count == 3) & (self.active_channel_mode == 'CPM'):
            fall = set_in_range(fall,self.cpm_slew_max,self.cpm_slew_min)
            self.write(f'{self.prog_func.power}:{self.prog_func.fall} {fall:g}')
        elif self.active_channel_mode == 'CPH':
            fall = set_in_range(fall,self.cph_slew_max,self.cph_slew_min)
            self.write(f'{self.prog_func.power}:{self.prog_func.fall} {fall:g}')    
    
    # @cp.setter
    # def cp(self, power):
    #     self._cp = power
    #     self.write(f'{self.prog_func.channel} {self.channel}')
    #     self.write(f'POWER:STAT:L{self._active_level} {self._cp}')
    #     self.write(f'{self.prog_func.mode} CPL')

    def set_max_cr(self):
        self.cr = self.crh_max_r
        
    @visa_io
    def turn_on(self):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.write(f'{self.prog_func.load} ON')
        self.active_channel_status = self.write(f'{self.prog_func.load}?')
        if self.active_channel_status == EloadStatus.OFF:
            raise Exception("Eload did not turn on")
        return 0

    @visa_io
    def turn_off(self):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.write(f'{self.prog_func.load} OFF')
        self.active_channel_status = self.write(f'{self.prog_func.load}?')
        if self.active_channel_status == EloadStatus.ON:
            raise Exception("Eload did not turn off")
        return 0

    @visa_io
    def short_on(self):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.write(f'{self.prog_func.load}:{self.prog_func.short} ON')
        self.active_channel_status = self.write(f'{self.prog_func.load}?')
        self.active_channel_short = 1
        return self.active_channel_short

    @visa_io
    def short_off(self):
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.write(f'{self.prog_func.load}:{self.prog_func.short} OFF')
        self.active_channel_status = self.write(f'{self.prog_func.load}?')
        self.active_channel_short = 0
        return self.active_channel_short
        
    @visa_io
    def set_load(self, vout_V:float, iout_A:float, mode:str):
        ''' Set eload to defined load and automatically choose the eload type'''
        self.write(f'{self.prog_func.channel} {self.channel}')
        self.active_channel_voltage = vout_V
        if (not iout_A == 0) and (iout_A is not None):
            self.active_channel_power = vout_V*iout_A
            
        # print(f'\nPower: {self.active_channel_power}W\n'
        #       f'Voltage: {self.active_channel_voltage}V')
        match mode:
            case ELoadTypes.CC:
                # print(f'{self.prog_func.load}: CC, {iout_A}A')
                self.cc = iout_A
                return self._cc
            
            case ELoadTypes.CR:
                if iout_A == 0:
                    self.set_max_cr()
                else:
                    self.cr = round(vout_V/iout_A,6)
                return self._cr
            
            case ELoadTypes.CP:
                self.cp = vout_V*iout_A
                return self._cp
            
            case ELoadTypes.CV:
                self.cv = vout_V
                return self._cv
            case _:
                pass
            
    @visa_io        
    def set_cc_static_slew(self,rise:float=0.15,fall:float=0.15):
        ''' Set slew rate for cc static mode'''
        self.cc_static_rise = rise
        if self.cc_static_rise in [0,None]:
            return None
        
        self.cc_static_fall = fall
        if self.cc_static_fall in [0,None]:
            return None
        
        return 1
        
    @visa_io    
    def set_cr_slew(self,rise:float=0.15,fall:float=0.15):
        ''' Set slew rate for cr mode'''
        self.cr_rise = rise
        if self.cr_rise in [0,None]:
            return None
        
        self.cr_fall = fall
        if self.cr_fall in [0,None]:
            return None
        
        return 1
    
    @visa_io    
    def set_cp_slew(self,rise:float=0.15,fall:float=0.15):
        ''' Set slew rate for cp mode'''
        self.cp_rise = rise
        if self.cp_rise in [0,None]:
            return None
        
        self.cp_fall = fall
        if self.cp_fall in [0,None]:
            return None
        
        return 1
        
                
            

# TODO: Later implement for non-module eload
class ElectronicLoad(Equipment):
    def __init__(self, device, device_id):
        super().__init__(device, device_id)

        self.write('CHAN:ID')

    def get_active_channels(self):
        pass

    def turn_on_all(self):
        for i in range(1, 9):
            self.channel[i].turn_on()

    def turn_off_all(self):
        for i in range(1, 9):
            self.channel[i].turn_off()

    def cleanup(self):
        self.turn_off_all()
        self.close()

    class Channel:
        def __init__(self, load, channel):
            self.load = load
            self.channel = channel
            self._cv = 0
            self._cc = 0
            self._cr = 0
            self._led_voltage = 0
            self._led_current = 0
            self._von = 0
            self._voltage = 0
            self._current = 0
            self.prog_func = Eload_Chroma_Prog_Group1

        def dynamic(self, low, high, ton, toff, rise, fall):
            self.load.write(f'{self.prog_func.channel} {self.channel}')
            self.load.write(f'{self.prog_func.current_dynamic}:L1 {low}')
            self.load.write(f'{self.prog_func.current_dynamic}:L2 {high}')
            self.load.write(f'{self.prog_func.current_dynamic}:{self.prog_func.rise} {rise}')
            self.load.write(f'{self.prog_func.current_dynamic}:{self.prog_func.fall} {fall}')
            self.load.write(f'{self.prog_func.current_dynamic}:T1 {ton}')
            self.load.write(f'{self.prog_func.current_dynamic}:T2 {toff}')

        @property
        def voltage(self):
            self.load.write(f'{self.prog_func.channel} {self.channel}')
            self._voltage = float(self.load.write(f'{self.prog_func.fetch}:VOLT?'))
            return self._voltage

        @property
        def current(self):
            self.load.write(f'{self.prog_func.channel} {self.channel}')
            self._current = float(self.load.write(f'{self.prog_func.fetch}:CURR?'))
            return self._current

        @property
        def cv(self):
            return self._cv

        @property
        def cc(self):
            return self._cc

        @property
        def cr(self):
            return self._cr

        @property
        def led_voltage(self):
            return self._led_voltage

        @property
        def led_current(self):
            return self._led_current

        @property
        def von(self):
            return self._von

        @von.setter
        def von(self, voltage):
            self._von = voltage
            self.load.write(f'{self.prog_func.channel} {self.channel}')
            self.load.write(f'CONF:{self.prog_func.voltage}:ON {self._von}')

        @cv.setter
        def cv(self, voltage):
            self._cv = voltage
            self.load.write(f'{self.prog_func.channel} {self.channel}')
            self.load.write(f'{self.por}:L1 {self._cv}')
            self.load.write(f'{self.prog_func.mode} CV')

        @cc.setter
        def cc(self, current):
            self._cc = current
            self.load.write(f'{self.prog_func.channel} {self.channel}')
            self.load.write(f'{self.prog_func.current_static}:L1 {self._cc}')
            self.load.write(f'{self.prog_func.mode} CCH')

        @cr.setter
        def cr(self, resistance):
            self._cr = resistance
            self.load.write(f'{self.prog_func.channel} {self.channel}')
            self.load.write(f'{self.prog_func.resistance}:L1 {self._cr}')
            self.load.write(f'{self.prog_func.mode} CRH')

        @led_voltage.setter
        def led_voltage(self, voltage):
            self._led_voltage = voltage
            # not supported yet...
            self.load.write(f'{self.prog_func.channel} {self.channel}')
            self.load.write(f'LED:VO {self._led_voltage}')
            self.load.write(f'{self.prog_func.mode} LEDH')

        @led_current.setter
        def led_current(self, current):
            self._led_current = current
            # not supported yet...
            self.load.write(f'{self.prog_func.channel} {self.channel}')
            self.load.write(f'LED:IO {self._led_current}')
            self.load.write(f'{self.prog_func.mode} LEDH')

        def turn_on(self):
            self.load.write(f'{self.prog_func.channel} {self.channel}')
            self.load.write(f'{self.prog_func.load} ON')

        def turn_off(self):
            self.load.write(f'{self.prog_func.channel} {self.channel}')
            self.load.write(f'{self.prog_func.load} OFF')

        def short_on(self):
            self.load.write(f'{self.prog_func.channel} {self.channel}')
            self.load.write(f'{self.prog_func.load}:SHOR ON')

        def short_off(self):
            self.load.write(f'{self.prog_func.channel} {self.channel}')
            self.load.write(f'{self.prog_func.load}:SHOR OFF')
