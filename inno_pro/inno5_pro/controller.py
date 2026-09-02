from functools import wraps
from inno_pro.inno5_pro.definitions import *
from inno_pro.inno5_pro.functions import *
from inno_pro.functions import *
from sink_controllers.pat_tool import CP2112, readback_retry
from misc_functions.misc_functions import timeit
from time import sleep

class Inno5ProI2CController(CP2112):
    """ Class for the SMBUS interface to directly send I2C commands to DUT.
        Used specifically for InnoSwitch Pro family devices
    """
    commands = Inno5Pro_I2C_Commands()
    defaults = Inno5Pro_I2C_Defaults()
    params = Inno5Pro_Parameters()
    
    def __init__(self, rsense_mohm=6, *args, **kwargs):
        super().__init__()
        
        self.registers = Inno5Pro_I2C_Registers()
        self.commands = Inno5Pro_I2C_Commands()
        self.defaults = Inno5Pro_I2C_Defaults()
        self.params = Inno5Pro_Parameters()
        self.readback_commands = Inno5Pro_I2C_Readback_Registers()
        self.readback_commands_list = INNO5_PRO_READBACK_REG_LIST
        self.registers_list = INNO5_PRO_REG_LIST
        # Zero is added at the end for write address (CP2112 requirement)
        self.slave_address = self.defaults.INNOPRO_SLAVE_ADDR << 1
        self.smbus = None
        self.rsense_mohm = rsense_mohm
        self.imax_A = self.params.IS_MAX_MV/self.rsense_mohm

        self.description = f"TST-058 PAT Tool, SN: {self.serial_number}"# : Port {self.port}"
        self.details =  (   f"CP2112 + CYPD2122 based \n"
                            f"I2C Interface and  USB-PD Sink Controller\n"
                            f"VID = {self._vid}\tPID = {self._pid}")
    
    def close(self):
        super().close()
    def open(self,serial_num:str=''):
        super().open(serial_num=serial_num)
    def reset(self):
        super().reset()
    
    def update_rsense(self, rsense_mohm):
        self.rsense_mohm = rsense_mohm
        self.imax_A = self.params.IS_MAX_MV/self.rsense_mohm

    def process_write_2bytes(self, reg_addr, u16_val)->None:
        """Write a 2 byte value from a uint16 to a register."""
        # Get the bytes of the u16 input 
        h_byte, l_byte = u16_bytes(u16_val)
        
        # print(f'low_byte:{hex(l_byte)}\n'
        #       f'high_byte:{hex(h_byte)}\n')

        write_buffer = [0,0,0]
        write_buffer[0] = reg_addr
        write_buffer[1] = l_byte
        write_buffer[2] = h_byte

        # print(write_buffer)
        return self.write(write_buffer)

    def process_write_1byte(self, reg_addr, u8_val)->None:
        """Write a 1 byte value from a uint16 to a register."""
        # Get the bytes of the u16 input 
        u8_val = u8_val & 0xFF  # Ensure 8 bits
        

        write_buffer = [0,0]
        write_buffer[0] = reg_addr
        write_buffer[1] = u8_val

        # print(write_buffer)
        return self.write(write_buffer)
        
    def write_2bytes_from_input(self,reg_addr,u8_lsb,u8_msb)->None:
        """Write a 2 byte value directly to a register."""
        write_buffer = [0,0,0]
        write_buffer[0] = reg_addr
        write_buffer[1] = u8_lsb
        write_buffer[2] = u8_msb

        # print(write_buffer)
        return self.write(write_buffer)

    def vben(self, setting):
        """Configure the VBEN register"""
        reg:VBEN = process_vben_command(setting)
        return reg, True
    
    def bleeder(self, bleeder_en, 
                bleeder_thresh=Inno5Pro_I2C_Commands.BLEEDER_VOUT10PCT,
                weak_bleeder_en=Inno5Pro_I2C_Commands.WEAK_BLEEDER_OFF,
                weak_bleeder_thresh=0):
        """Configure the Bleeder (BLEEDER) register"""

        # Create a BLEEDER register structure to hold the values
        reg:BLEEDER = process_bleeder_command(bleeder_en=bleeder_en,bleeder_thresh=bleeder_thresh,weak_bleeder_en=weak_bleeder_en,weak_bleeder_thresh=weak_bleeder_thresh)
        return reg, True
    
    def cv(self, vout_V:float, autocv:bool=False):
        """Configure the Constant Voltage (CV) register"""
        # Vout is split into 2 parts
        # Lower part is 7 bits. Higher part is 5 bits
        reg:CV = process_cv_command(vout_V=vout_V,auto_cv=autocv)
        return reg, True
        
    def cc(self,iout_A, offset=0):
        """Configure the Constant Current (CC) register"""
        
        reg:CC = process_cc_command(iout_A=iout_A,
                                    rsense_mohm=self.rsense_mohm,
                                    offset_lsb=int(offset))
        return reg, True
    
    def vkp(self,vkp_V):
        """Configure the Constant Power Knee Voltage (VKP) register"""

        reg:VKP = process_vkp_command(vkp_V=vkp_V)
        
        return reg, True
            
    def cdc(self, cdc_mV):
        """Configure the Cable Drop Compensation (CDC) register"""
        
        reg:CDC = process_cdc_command(cdc_mV = cdc_mV)

        return reg, True

    def ova(self, threshold_V, response):
        """Configure the Absolute Over Voltage (OVA) register"""
        
        reg:OVA = process_ova_command(threshold_V=threshold_V, response=response)

        return reg, True
    
    def uva(self, 
            threshold_V, 
            response, 
            timer,
            timer_en:bool = True):
        """Configure the Absolute Under Voltage (UVA) register"""
        
        reg:UVA = process_uva_command(threshold_V= threshold_V, response = response, timer = timer, timer_en=timer_en)

        return reg, True
    
    def cvo(self, 
            response, 
            timer,
            cvo_en:bool = False):
        """Configure the Constant Voltage Only (CVO) register"""
        
	    # Create an CVO register structure to hold the values
        reg:CVO = process_cvo_command(response=response, timer=timer, cvo_en=cvo_en)
        
        return reg, True
    
    def ccsc(self,response):
        """Configure the Constant Current Short Circuit (CCSC) register"""
        
        # Create a CCSC register structure to hold the values
        reg:CCSC = process_ccsc_command(response=response)
        
        return reg, True
        
    def issc(self, 
            threshold_bits, 
            threshold_freq,
            response):
        """Configure the IS pin Short Circuit (ISSC) register"""
        
	    # Create an ISSC register structure to hold the values
        reg:ISSC = process_issc_command(threshold_bits=threshold_bits, threshold_freq=threshold_freq, response=response)
        
        return reg, True
        
    def vbussc(self,
               threshold_bits,
               num_samples,
               response):
        """Configure the Bus Switch Short Circuit (VBUSSC) register"""
        
        # Create a VBUSSC register structure to hold the values
        reg:VBUSSC = process_vbussc_command(threshold_bits=threshold_bits, num_samples=num_samples, response=response)
        
        return reg, True
    
    def watchdog(self, setting):
        """Configure the Watchdog (WATCHDOG) register"""
        
        # Create a WATCHDOG register structure to hold the values
        reg:WATCHDOG = process_watchdog_command(setting=setting)

        return reg, True
        
    def fast_vi(self,setting:bool = False):
        """Configure the Fast VI (FAST_VI) register"""   
        
        # Create a FAST_VI register structure to hold the values
        reg:FAST_VI = process_fast_vi_command(setting=setting)

        return reg, True  
        
    def vdis(self,setting):
        """Configure the VDIS register"""  
        
        # Create a VDIS register structure to hold the values
        reg:VDIS = process_vdis_command(setting=setting)
        
        return reg, True
    
    def turn_off_psu(self,latch_off_en:bool = False):
        """"Configure the LATCH_OFF register"""    
        
        # Create a LATCH_OFF register structure to hold the values
        reg:TURN_OFF_PSU = process_turn_off_psu_command(latch_off_en=latch_off_en)
        
        return reg, True
    
    def dcm_only(self,
            threshold=0b00,
            enable:bool = False):
        """Configure the DCM Only (DCM_ONLY) register"""
        
	    # Create a DCM-Only register structure to hold the values
        reg = process_dcm_only_command(threshold=threshold,enable=enable)

        return reg, True
        
    def sr_zvs(self, 
            delay_time_count,
            on_time_count,
            fwd_valley_switch_en:bool = False,
            sr_zvs_en:bool = False):
        
        """Configure the SR ZVS (SR_ZVS) register"""
        # Create a SR ZVS register structure to hold the values
        reg = process_sr_zvs_command(delay_time_count=delay_time_count,on_time_count=on_time_count,fwd_valley_switch_en=fwd_valley_switch_en,sr_zvs_en=sr_zvs_en)
        
        return reg, True
        
    def int_mask(self,
            omf:bool=False,
            vbussc:bool=False,
            control_s:bool=False,
            latch_off:bool=False,
            cvol:bool=False,
            issc:bool=False,
            ccsc:bool=False,
            uv:bool=False,
            ov:bool=False):
        """Configure the Interrupt Mask (INT_MASK) register"""
        
        # Create an INT MASK register structure to hold the values
        reg:INT_MASK = process_int_mask_command(omf=omf,vbussc=vbussc,control_s=control_s,latch_off=latch_off,cvol=cvol,issc=issc,ccsc=ccsc,uv=uv,ov=ov)

        return reg, True
        
    def line_sense(self,line_sense_enable:bool = False):
        """Configure the Line Sense (LINE_SENSE) register"""
        # Create an INT MASK register structure to hold the values
        reg:LINE_SENSE = process_line_sense_command(line_sense_enable)

        return reg, True
     
    def fwd_peak(self,pre_shift_ns, window_pct, fwd_peak_en:bool = True):
        """Configure the FWD Peak (FWD_PEAK) register"""
        # Create an INT MASK register structure to hold the values
        reg:FWD_PEAK = process_fwd_peak_command(pre_shift_ns=pre_shift_ns, window_pct=window_pct, fwd_peak_en=fwd_peak_en)

        return reg, True
    
    def loopspeed_1(self,
            cv_small_step_thresh_mv = 200,
            cv_large_step_thresh_mv = 100):
        """Configure the Loop Speed 1 (LOOPSPEED_1) register"""       
        # Create a LOOPSPEED 1 register structure to hold the values
        reg:LOOPSPEED_1 = process_loop_speed1_command(cv_small_step_thresh_mv=cv_small_step_thresh_mv,cv_large_step_thresh_mv=cv_large_step_thresh_mv) 
        
        return reg, True
    
    def loopspeed_2(self,
            small_step_size_mv = 10,
            large_step_size_mv = 80,
            cc_small_step_thresh_lsb = 8,
            cc_large_step_thresh_lsb = 4):
        """Configure the Loop Speed 2 (LOOPSPEED_2) register"""
        
        reg:LOOPSPEED_2 = process_loop_speed2_command(small_step_size_mv=small_step_size_mv,large_step_size_mv=large_step_size_mv,
                                    cc_large_step_thresh_lsb=cc_large_step_thresh_lsb,cc_small_step_thresh_lsb=cc_small_step_thresh_lsb)
        
        return reg, True
        
    def fast_cc(self,
            fast_cc_offset = 0,
            slow_cc_offset = 0,
            fast_cc_enable:bool = False,
            calibration_disable:bool = True):
        """Configure the Fast CC (FAST_CC) register"""
                
        reg:FAST_CC = process_fast_cc_command(fast_cc_offset=fast_cc_offset,slow_cc_offset=slow_cc_offset,fast_cc_enable=fast_cc_enable,calibration_disable=calibration_disable)
        
        return reg, True
        
    def loop_option(self,option_bytes_lsb,option_bytes_msb):
        reg = u32()
        reg.byte2 = option_bytes_lsb
        reg.byte1 = option_bytes_msb
        return reg, True

    def sr_disable(self,
            sr_on_protection_en:bool = False,
            sr_zvs_on_protection_en:bool = False,
            protection_threshold_mV:int = commands.SR_PROTECTION_THRESHOLD_300MV,
            bit5_en:bool = False,
            bit4_en:bool = False,
            unwanted_pulse_protection_en:bool = False,
            unwanted_pulse_protection_count:int = 0):
        """Configure the SR DISABLE (SR_DISABLE) register"""
                
        reg:SR_DISABLE = process_sr_disable_command(sr_on_protection_en=sr_on_protection_en,sr_zvs_on_protection_en=sr_zvs_on_protection_en,protection_threshold_mV=protection_threshold_mV,
            bit5_en=bit5_en,bit4_en=bit4_en,unwanted_pulse_protection_en=unwanted_pulse_protection_en,unwanted_pulse_protection_count=unwanted_pulse_protection_count)
        
        return reg, True
        
        
    # READBACK
    def send_read_command(self, register):
        """Generate a read request using the read command and requested register."""
        if register in INNO5_PRO_READBACK_REG_LIST:
            wb = [self.registers.READ_CMD_REG,
                register,
                register]
            return wb, True
        else:
            return None, False
    
    def get_read_value(self):
        rb = self.read(num_bytes=2)
        return list_to_uint16(rb)

    def read_u16(self, address):
        # Send a read command
        self.send_read_command(address)
        # Get the uint16 value of the readbback
        return self.get_read_value()
    
    def read_cv(self,rb_u16):
        """Return the CV setpoint register value."""
        cv = process_read1_command(rb_u16)
        return cv

    def read_cv_v(self,rb_u16):
        """Return the CV setpoint in Volts"""
        cv = self.read_cv(rb_u16)
        vout_setpoint = cv * self.params.CV_RESOLUTION_MV/1000
        return vout_setpoint
    
    def read_vout_average_v(self, rb_u16):
        vout_10mV = process_read13_command(rb_u16)
        vout_average = vout_10mV * self.params.CV_RESOLUTION_MV/1000
        return round(vout_average,3)
    
    def read_vout_v(self,rb_u16):
        vout_inst_bits = process_read9_command(rb_u16)
        vout_inst_v = vout_inst_bits * self.params.CV_RESOLUTION_MV/1000
        return round(vout_inst_v,3)
        
    def read_vout_dac_v(self,rb_u16):      
        vout_dac = process_read14_command(rb_u16)
        return vout_dac
    
    def read_ov_v(self,rb_u16):        
        ov = process_read3_command(rb_u16)
        ov_V = ov * self.params.OV_RESOLUTION_MV/1000
        return ov_V
        
    def read_uv_v(self,rb_u16):        
        uv = process_read4_command(rb_u16)
        uv_V = uv * self.params.UV_RESOLUTION_MV/1000
        return uv_V
    
    def read_cdc_mv(self,rb_u16):
        # Place the readback value to a READ7 structure
        read = READ7(rb_u16)
        cdc_bits = read.bits.cdc
        cdc_mv = ( cdc_bits * self.params.CDC_RESOLUTION_MV )
        return cdc_mv
	    
    def read_omf(self,rb_u16):
        cv_flag, cp_flag, cc_flag = process_read11_command(rb_u16)
        
        if cc_flag:
            return self.defaults.OMF_CC_MODE
        elif cp_flag:
            return self.defaults.OMF_CP_MODE
        elif cv_flag:
            return self.defaults.OMF_CV_MODE
        else:
            return 0

    def read_omf_txt(self,rb_u16):
        cv_flag, cp_flag, cc_flag = process_read11_command(rb_u16)
        
        flag_sum = cv_flag + cp_flag + cc_flag 
        flag_txt = f"{cv_flag}{cp_flag}{cc_flag}"

        omf_text = ""
        if flag_sum == 1:
            if cc_flag:
                omf_text = self.defaults.OMF_TEXT[self.defaults.OMF_CC_MODE] 
            elif cp_flag:
                omf_text = self.defaults.OMF_TEXT[self.defaults.OMF_CP_MODE]
            elif cv_flag:
                omf_text = self.defaults.OMF_TEXT[self.defaults.OMF_CV_MODE]
        
        omf_text = omf_text + flag_txt

        return omf_text
        

    def read_iout_average(self,rb_u16):
        iout_average = process_read12_command(rb_u16)
        return iout_average
    

    def read_iout_average_a(self,rb_u16):
        inno = self.params
        is_max_mv = inno.IS_MAX_MV
        is_max_count = inno.CC_MAX_COUNT

        iout_u8 = self.read_iout_average(rb_u16)
        iout_ave = inno.IS_MAX_MV * (iout_u8 / inno.CC_MAX_COUNT) / self.rsense_mohm
        return iout_ave
    
        

    def read_cc(self,rb_u16):    
        cc = process_read2_command(rb_u16)
        return cc
        

    def read_cc_a(self,rb_u16):
        cc = self.read_cc(rb_u16)
        cc_a = self.imax_A * (cc / 192)
        return cc_a
        

    def read_vkp(self,rb_u16):
        vkp = process_read5_command(rb_u16)      
        return vkp
          
  
    def read_vkp_v(self,rb_u16):
        vkp = self.read_vkp(rb_u16)
        vkp_V = vkp*self.params.VKP_RESOLUTION_MV / 1000
        return round(vkp_V, 3)
    
    # @readback_retry
    # # Line Sense Functions
    # def read_line_sense_us(self)->tuple[int, int]:
    #     self.trigger_line_sense()
    #     self.poll_line_sense()
    #     return self.get_line_sense_report_us()
    
    # @readback_retry
    # # Line Sense Functions
    # def read_line_sense_count(self)->tuple[int, int]:
    #     """Do the line sense read sequence and return a tuple
    #     containing the t_on and t_off count"""
    #     self.trigger_line_sense()
    #     self.poll_line_sense()
    #     return self.get_line_sense_report()
    
    # # @readback_retry
    # def trigger_line_sense(self):
    #     """Trigger the line sense to start the sample accumulation"""
    #     return self.process_write_1byte(reg_addr=self.registers.LINE_SENSE_REG,
    #                              u8_val=1)
        

    def read_loop_speed_1_byte(self):
        """Read Loop Speed 1 Byte Value"""
        ls1 = self.read_u16(self.readback_commands.READ19)
        
        return f"{ls1:04X}"


    def read_loop_speed_2_byte(self):
        """Read Loop Speed 2 Byte Value"""
        ls2 = self.read_u16(self.readback_commands.READ20)
        
        return f"{ls2:04X}"

    def poll_line_sense(self, rb_u16):
        """Poll the line sense to see if the report is ready"""
        reg = READ10(rb_u16)
        report_ready = reg.bits.reg_line_sense
        sleep(0.001)
        return report_ready

    def get_line_sense_report(self,rb_u16_ton, rb_u16_toff)->tuple[int, int]:
        """Return a tuple containing the t_on and t_off count"""
        reg1 = READ21(rb_u16_ton)

        reg2 = READ22(rb_u16_toff)

        t_on_count = reg1.bits.ton_report
        t_off_count = reg2.bits.toff_report
        
        return (t_on_count, t_off_count)
    
    def get_line_sense_report_us(self,rb_u16_ton, rb_u16_toff)->tuple[float, float]:
        """Return a tuple containing the t_on and t_off in units of µs"""

        t_on_count, t_off_count = self.get_line_sense_report(rb_u16_ton, rb_u16_toff)

        t_on_us = round(t_on_count * self.params.TIMING_RESOLUTION_NS / 1000 / 16 , 3)
        t_off_us = round(t_off_count * self.params.TIMING_RESOLUTION_NS / 1000 / 16, 3)

        return (t_on_us, t_off_us)