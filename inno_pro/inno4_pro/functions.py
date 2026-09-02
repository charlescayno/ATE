from inno_pro.inno4_pro.definitions import *
from inno_pro.functions import *
from misc_functions.misc_functions import *
import math

params = Inno4Pro_Parameters
commands = Inno4Pro_I2C_Commands
defaults = Inno4Pro_I2C_Defaults

def process_cv_command(vout_V:float, auto_cv:bool = False):
    """ Process a CV command and output the 32 byte I2C data"""
    # Vout is split into 2 parts
    # Lower part is 7 bits. Higher part is 5 bits
    
    vout_V = set_in_range(vout_V,params.CV_MAX_V,params.CV_MIN_V)
    
    vout_count = int(round(int(vout_V*1000) / params.CV_RESOLUTION_MV))
    vout_lowbyte = limit_bits(vout_count, 7)
    vout_highbyte = limit_bits((vout_count >> 7), 5)

    # Create a CV register structure to hold the values
    reg = CV()
    reg.bits.vout_low_byte = vout_lowbyte
    reg.bits.vout_high_byte = vout_highbyte
    if auto_cv == True:
        reg.bits.auto_cv = commands.CV_AUTO_UV_OV_ENABLED
    else:
        reg.bits.auto_cv = commands.CV_AUTO_UV_OV_DISABLED
    # Add the parity
    reg.asbyte = add_parity_2bytes(reg.asbyte)
    return reg

def process_cc_command(iout_A:float, rsense_mohm:float = 6, offset_lsb:int=0):
    """ Process a CC command and output the 32 byte I2C data"""
    if rsense_mohm == 0:
        return
    imax_A = params.IS_MAX_MV/rsense_mohm
    iout_count = int(round(iout_A/imax_A*params.CC_MAX_COUNT))
    iout_count = set_in_range(iout_count,params.CC_MAX_COUNT,params.CC_MIN_COUNT)
    iout_count += offset_lsb

    iout_count = min_max_int(iout_count, params.CC_MIN_COUNT, params.CC_MAX_COUNT)

    # Iout is split into 2 parts
    # Lower part is 7 bits. Higher part is 1 bit 
        
    iout_lowbyte = limit_bits(iout_count, 7)
    iout_highbyte = limit_bits((iout_count >> 7), 1)
    
    # Create a CC register structure to hold the values
    reg = CC()
    reg.bits.iout_high_byte = iout_highbyte
    reg.bits.iout_low_byte = iout_lowbyte
    
    # Add the parity
    reg.asbyte = add_parity_2bytes(reg.asbyte)
    return reg

def process_uva_command(threshold_V:float, response, timer):
    """ Process a UVA command and output the 32 byte I2C data"""
    
    # Threshold is split into 2 parts
    # Lower part is 7 bits. Higher part is 1 bit
    threshold_V = set_in_range(threshold_V,params.UV_MAX_V,params.UV_MIN_V)
    thresh_count = int(round(int(threshold_V*1000) / params.UV_RESOLUTION_MV))
    thresh_lowbyte = limit_bits(thresh_count, 7)
    thresh_highbyte = limit_bits((thresh_count >> 7), 1)
    # Create an UVA register structure to hold the values
    reg = UVA()
    reg.bits.thresh_low_byte = thresh_lowbyte
    reg.bits.thresh_high_byte = thresh_highbyte
    reg.bits.response = response
    reg.bits.timer = timer
    
    # Add the parity
    reg.asbyte = add_parity_2bytes(reg.asbyte)
    return reg

def process_ova_command(threshold_V:float, response):
    """ Process an OVA command and output the 32 byte I2C data"""
    
    # Threshold is split into 2 parts
    # Lower part is 7 bits. Higher part is 1 bit
    threshold_V = set_in_range(threshold_V,params.OV_MAX_V,params.OV_MIN_V)
    thresh_count = int(round(int(threshold_V*1000) / params.OV_RESOLUTION_MV))
    thresh_lowbyte = limit_bits(thresh_count, 7)
    thresh_highbyte = limit_bits((thresh_count >> 7), 1)
    
    # Create an OVA register structure to hold the values
    reg = OVA()
    reg.bits.thresh_low_byte = thresh_lowbyte
    reg.bits.thresh_high_byte = thresh_highbyte
    reg.bits.response = response

    # Add the parity
    reg.asbyte = add_parity_2bytes(reg.asbyte)
    return reg

def process_cdc_command(cdc_mV:float):
    """ Process a CDC command and output the 32 byte I2C data"""
    cdc_count = int(math.floor(cdc_mV/params.CDC_RESOLUTION_MV))
    #cdc_count = cdc_lsb

    # Create a CDC register structure to hold the values
    reg = CDC()
    reg.bits.cdc_low_byte = cdc_count
    return reg

def process_cvo_command(response, timer, cvo_en:bool = False):
    """ Process a CVO command and output the 32 byte I2C data"""
    # Create a CVO register structure to hold the values
    if cvo_en:        
        cvo_en = commands.CVO_CV_ONLY_MODE
    else:
        cvo_en = commands.CVO_CV_CC_MODE           
    reg = CVO()
    reg.bits.response = response
    reg.bits.timer = timer
    reg.bits.cvo_enable = cvo_en
    return reg

def process_vkp_command(vkp_V):
    """ Process a VKP command and output the 32 byte I2C data"""
    # Iout is split into 2 parts
    # Lower part is 7 bits. Higher part is 1 bit
    vkp_count = int(round(int(vkp_V*1000) / params.VKP_RESOLUTION_MV))
    vkp_lowbyte = limit_bits(vkp_count, 7)
    vkp_highbyte = limit_bits((vkp_count >> 7), 1)
    
    # Create a CC register structure to hold the values
    reg = VKP()
    reg.bits.vkp_high_byte = vkp_highbyte
    reg.bits.vkp_low_byte = vkp_lowbyte
    
    # Add the parity
    reg.asbyte = add_parity_2bytes(reg.asbyte)
    return reg

def process_vben_command(setting):
    """ Process a VBEN command and output the 32 byte I2C data"""
    # Create a VBEN register structure to hold the values
    reg = VBEN()
    reg.bits.vben_enable = setting
        
    # Add the parity
    reg.asbyte = add_odd_parity_1byte(reg.asbyte)
    return reg

def process_watchdog_command(setting):
    """ Process a WATCHDOG command and output the 32 byte I2C data"""
    # Create an WATCHDOG register structure to hold the values
    reg = WATCHDOG()
    reg.bits.timer = setting
    
    return reg
    
def process_bleeder_command(bleeder_en,weak_bleeder_en:bool = False):
    """ Process a BLEEDER command and output the 32 byte I2C data"""
    # Create a BLEEDER register structure to hold the values
    if weak_bleeder_en:
        weak_bleeder_en = commands.WEAK_BLEEDER_ON
    else:
        weak_bleeder_en = commands.WEAK_BLEEDER_OFF
    
    reg = BLEEDER()
    reg.bits.weak_bleeder_enable = weak_bleeder_en
    reg.bits.bleeder_enable = bleeder_en
    return reg

def process_fast_vi_command(setting:bool = False):  
    """ Process a FAST VI command and output the 32 byte I2C data"""
    # Create a FAST_VI register structure to hold the values
    if setting:
        fast_vi_en = commands.FASTVI_LIMIT_DIS
    else:
        fast_vi_en = commands.FASTVI_LIMIT_EN
    reg = FAST_VI()
    reg.bits.enable = fast_vi_en
    return reg

def process_ccsc_command(response):
    """ Process a CCSC command and output the 32 byte I2C data"""
    # Create a CCSC register structure to hold the values
    reg = CCSC()
    reg.bits.response = response
    return reg

def process_issc_command(threshold_bits, threshold_freq, response):
    """ Process a ISSC command and output the 32 byte I2C data"""
    # Create a ISSC register structure to hold the values
    reg = ISSC()
    reg.bits.thresh = threshold_bits
    reg.bits.freq = threshold_freq
    reg.bits.response = response
    return reg

def process_vbussc_command(threshold_bits, num_samples, response):
    """ Process a VBUSSC command and output the 32 byte I2C data"""
    # Create a VBUSSC register structure to hold the values
    reg = VBUSSC()
    reg.bits.thresh = threshold_bits
    reg.bits.num_samples = num_samples
    reg.bits.response = response
    return reg

def process_vdis_command(setting):
    """ Process a VDIS command and output the 32 byte I2C data"""
    # Create a VDIS register structure to hold the values
    reg = VDIS()
    reg.bits.discharge_setting = setting

    # Add the parity
    reg.asbyte = add_odd_parity_1byte(reg.asbyte)
    return reg

def process_turn_off_psu_command(latch_off_en:bool = False):
    """ Process a TURN-OFF command and output the 32 byte I2C data"""
     # Create a VDIS register structure to hold the values
    if latch_off_en:
        latch_off_en = commands.TURN_OFF_PSU_ENABLED
    else:
        latch_off_en = commands.TURN_OFF_PSU_DISABLED
    
    reg = TURN_OFF_PSU()
    reg.bits.latch_off_enable = latch_off_en
    return reg

def process_dcm_only_command(threshold,enable:bool = False):
    """ Process a DCM ONLY command and output the 32 byte I2C data"""
    # Create a DCM-Only register structure to hold the values
    if enable:
        enable = commands.DCM_ONLY_ENABLE
    else:
        enable = commands.DCM_ONLY_DISABLE
    reg = DCM_ONLY()
    reg.bits.thresh = threshold
    reg.bits.enable = enable
    return reg

# def process_sr_zvs_command(delay_time_count,on_time_count,fwd_valley_switch_en:bool = False,sr_zvs_en:bool = False):
#     # Create a SR ZVS register structure to hold the values
#     if sr_zvs_en:
#         sr_zvs_en = commands.SR_ZVS_ENABLED
#     else:
#         sr_zvs_en = commands.SR_ZVS_DISABLED
        
#     if fwd_valley_switch_en:
#         fwd_valley_en = commands.SR_ZVS_VALLEY_SW_ON
#     else:
#         fwd_valley_en = commands.SR_ZVS_VALLEY_SW_OFF
#     reg = SR_ZVS()
#     reg.bits.fwd_valley_switch_enable = fwd_valley_en
#     reg.bits.sr_zvs_enable = sr_zvs_en
#     reg.bits.delay = int(delay_time_count)
#     reg.bits.on_time = int(on_time_count)
#     return reg

def process_int_mask_command(omf:bool = False,vbussc:bool = False,control_s:bool = False,latch_off:bool = False,cvol:bool = False,issc:bool = False,ccsc:bool = False,uv:bool = False,ov:bool = False):
    """ Process a INT MASK command and output the 32 byte I2C data"""
    # Create an INT MASK register structure to hold the values
    omf_bit=0
    vbussc_bit=0
    control_s_bit=0
    latch_off_bit=0
    cvol_bit=0
    issc_bit=0
    ccsc_bit=0
    uv_bit=0
    ov_bit=0
    
    if omf:
        omf_bit = 1
    if vbussc:
        vbussc_bit = 1
    if control_s:
        control_s_bit = 1
    if latch_off:
        latch_off_bit = 1
    if cvol:
        cvol_bit = 1
    if issc:
        issc_bit = 1
    if ccsc:
        ccsc_bit = 1
    if uv:
        uv_bit = 1      
    if ov:
        ov_bit = 1
    
    reg = INT_MASK()
    reg.bits.omf = omf_bit
    reg.bits.vbussc = vbussc_bit
    reg.bits.control_s = control_s_bit
    reg.bits.latch_off = latch_off_bit
    reg.bits.cvol = cvol_bit
    reg.bits.issc = issc_bit
    reg.bits.ccsc = ccsc_bit
    reg.bits.uv = uv_bit
    reg.bits.ov = ov_bit
    return reg

# def process_line_sense_command(line_sense_enable:bool = False):
#     if line_sense_enable:
#         line_sense_en = commands.LINE_SENSE_ENABLED
#     else:
#         line_sense_en = commands.LINE_SENSE_DISABLED
#     reg = LINE_SENSE()
#     reg.bits.line_sense_enable = line_sense_en
#     return reg
def process_fwd_peak_command(pre_shift_ns,window_pct,fwd_peak_en):
    # Create FWD Peak register structure to hold the values
    if fwd_peak_en:
        fwd_peak_en = commands.FWD_PEAK_ENABLE
    else:
        fwd_peak_en = commands.FWD_PEAK_DISABLE
        
    reg = FWD_PEAK()
    reg.bits.pre_shift = pre_shift_ns
    reg.bits.window = window_pct
    reg.bits.enable = fwd_peak_en
    return reg

def process_loop_speed1_command(cv_small_step_thresh_mv,cv_large_step_thresh_mv):
    """ Process a LOOP SPEED 1 command and output the 32 byte I2C data"""
    # Create a Loop Speed 1 register structure to hold the values
    
    cv_small_step_thresh_count = int(math.floor(cv_small_step_thresh_mv/params.LS1_THRESH_RESOLUTION_MV))
    cv_large_step_thresh_count = int(math.floor(cv_large_step_thresh_mv/params.LS1_THRESH_RESOLUTION_MV))
    
    reg = LOOPSPEED_1()
    reg.bits.cv_small_step_thresh = cv_small_step_thresh_count
    reg.bits.cv_large_step_thresh = cv_large_step_thresh_count   
    return reg 

def process_loop_speed2_command(small_step_size_mv,large_step_size_mv,cc_large_step_thresh_lsb,cc_small_step_thresh_lsb):
    """ Process a LOOP SPEED 2 command and output the 32 byte I2C data"""
    # Create a Loop Speed 2 register structure to hold the values
    small_step_size_count = int(math.floor(small_step_size_mv/params.LS2_STEP_RESOLUTION_MV))
    large_step_size_count = int(math.floor(large_step_size_mv/params.LS2_STEP_RESOLUTION_MV))
        
    reg = LOOPSPEED_2()
    reg.bits.small_step_size = small_step_size_count
    reg.bits.large_step_size = large_step_size_count    
    reg.bits.cc_large_step_thresh = int(cc_large_step_thresh_lsb)
    reg.bits.cc_small_step_thresh = int(cc_small_step_thresh_lsb)
    return reg

def process_fast_cc_command(fast_cc_offset,slow_cc_offset,fast_cc_enable:bool = False, calibration_disable:bool = True):
    """ Process a FAST CC command and output the 32 byte I2C data"""
    # Create a Fast CC register structure to hold the values
    if calibration_disable:
        calibration_disable = commands.SLOW_CC_DISABLED
    else:
        calibration_disable = commands.SLOW_CC_ENABLED
        
    if fast_cc_enable:
        fast_cc_enable = commands.FAST_CC_ENABLED
    else:
        fast_cc_enable = commands.FAST_CC_DISABLED
        
    reg = FAST_CC()
    reg.bits.fast_cc_offset = int(fast_cc_offset)
    reg.bits.slow_cc_offset = int(slow_cc_offset)    
    reg.bits.calibration_disable = calibration_disable
    reg.bits.fast_cc_enable = fast_cc_enable
    return reg

# For Special Registers

# def process_sr_disable_command(sr_on_protection_en,sr_zvs_on_protection_en,protection_threshold_mV,bit5_en,bit4_en,unwanted_pulse_protection_en,unwanted_pulse_protection_count):
#     if sr_on_protection_en:
#         sr_on_protection_en = commands.SR_ON_PROTECTON_ENABLED
#     else:
#         sr_on_protection_en = commands.SR_ON_PROTECTON_DISABLED
        
#     if sr_zvs_on_protection_en:
#         sr_zvs_on_protection_en = commands.SR_ZVS_ON_PROTECTON_ENABLED
#     else:
#         sr_zvs_on_protection_en = commands.SR_ZVS_ON_PROTECTON_DISABLED
        
#     if bit5_en:
#         bit5_en = commands.SR_DISABLE_BIT5_ENABLE
#     else:
#         bit5_en = commands.SR_DISABLE_BIT5_DISABLE
    
#     if bit4_en:
#         bit4_en = commands.SR_DISABLE_BIT4_ENABLE
#     else:
#         bit4_en = commands.SR_DISABLE_BIT4_DISABLE
        
#     if unwanted_pulse_protection_en:
#         unwanted_pulse_protection_en = commands.SR_UNWANTED_PULSE_PROTECTION_ENABLED
#     else:
#         unwanted_pulse_protection_en = commands.SR_UNWANTED_PULSE_PROTECTION_DISABLED
    
#     reg = SR_DISABLE()
#     reg.bits.sr_on_protection = sr_on_protection_en
#     reg.bits.sr_zvs_on_protection = sr_zvs_on_protection_en  
#     reg.bits.threshold_mV = int(protection_threshold_mV)
#     reg.bits.bit_5 = bit5_en
#     reg.bits.bit_4 = bit4_en   
#     reg.bits.unwanted_pulse_protection = unwanted_pulse_protection_en
#     reg.bits.unwanted_pulse_count = int(unwanted_pulse_protection_count)
#     return reg

# For Readback Registers

def process_read1_command(rb_u16):
    # Place the readback value to a READ1 structure
    reg = READ1(rb_u16)

    # Take the individual bytes and join to get the needed value
    ub = reg.bits.high_byte
    lb = reg.bits.low_byte
    cv = join_7bits(ub,lb)
    return cv

def process_read2_command(rb_u16):
    # Place the readback value to a READ2 structure
    reg = READ2(rb_u16)

    # Take the individual bytes
    cc_lowbyte = reg.bits.low_byte
    cc_highbyte = reg.bits.high_byte
    
    cc = join_7bits(cc_highbyte, cc_lowbyte)
    return cc

def process_read3_command(rb_u16):
    # Place the readback value to a READ3 structure
    reg = READ3(rb_u16)

    # Take the individual bytes
    ov_lowbyte = reg.bits.low_byte
    ov_highbyte = reg.bits.high_byte
    
    ov = join_7bits(ov_highbyte, ov_lowbyte)
    return ov

def process_read4_command(rb_u16):
    # Place the readback value to a READ4 structure
    reg = READ4(rb_u16)

    # Take the individual bytes
    uv_lowbyte = reg.bits.low_byte
    uv_highbyte = reg.bits.high_byte
    
    uv = join_7bits(uv_highbyte, uv_lowbyte)
    return uv

def process_read5_command(rb_u16):
    # Place the readback value to a READ5 structure
    reg = READ5(rb_u16)
    vkp = reg.bits.vkp_setpoint
    
    return vkp

def process_read6_command(rb_u16):
    # Place the readback value to a READ6 structure
    reg = READ6(rb_u16)
    cvo_timer = reg.bits.cvo_timer
    cvo_response = reg.bits.cvo_response
    wd_timer = reg.bits.wd_timer
    uva_timer = reg.bits.uva_timer
    issc_response = reg.bits.issc_response
    ccsc_response = reg.bits.ccsc_response
    uva_response = reg.bits.uva_response
    ova_response = reg.bits.ova_response
    
    return cvo_timer, cvo_response, wd_timer, uva_timer, issc_response, ccsc_response, uva_response, ova_response

def process_read7_command(rb_u16):
    # Place the readback value to a READ7 structure
    reg = READ7(rb_u16)
    cdc = reg.bits.cdc
    otp_hysteresis = reg.bits.otp_hysteresis
    cvo = reg.bits.cvo
    fstvic = reg.bits.fstvic
    psu_off = reg.bits.psu_off
    bleeder = reg.bits.bleeder
    vben = reg.bits.vben

    return cdc, otp_hysteresis, cvo, fstvic, psu_off, bleeder, vben

def process_read8_command(rb_u16):
    # Place the readback value to a READ8 structure
    reg = READ8(rb_u16)
    
     # Take the individual bytes
    cc_i_lowbyte = reg.bits.low_byte
    cc_i_highbyte = reg.bits.high_byte
    
    cc_i = join_7bits(cc_i_highbyte, cc_i_lowbyte)
    return cc_i

def process_read9_command(rb_u16):
    # Place the readback value to a READ9 structure
    reg = READ9(rb_u16)

    # Take the individual bytes and join to get the needed value
    cv_i = reg.bits.output_voltage
    return cv_i

def process_read10_command(rb_u16):
    # Place the readback value to a READ10 structure
    reg = READ10(rb_u16)
    reg_vout_ov = reg.bits.reg_vout_ov
    reg_vout_uv = reg.bits.reg_vout_uv
    reg_ccsc = reg.bits.reg_ccsc
    reg_issc = reg.bits.reg_issc
    reg_vout10pct = reg.bits.reg_vout10pct
    reg_voutwk = reg.bits.reg_voutwk
    reg_otp = reg.bits.reg_otp
    reg_cv_en = reg.bits.reg_cv_en
    reg_high_fsw = reg.bits.reg_high_fsw
    reg_vdis = reg.bits.reg_vdis
    reg_control_s = reg.bits.reg_control_s
    reg_interrupt_en = reg.bits.reg_interrupt_en
    
    return reg_vout_ov, reg_vout_uv, reg_ccsc, reg_issc, reg_vout10pct, reg_voutwk, reg_otp, reg_cv_en, reg_high_fsw, reg_vdis, reg_control_s, reg_interrupt_en

def process_read11_command(rb_u16):
    # Place the readback value to a READ11 structure
    reg = READ11(rb_u16)

    # Take the individual bytes and join to get the needed value
    cv_mode = reg.bits.cv_mode
    cp_mode = reg.bits.cp_mode
    cc_mode = reg.bits.cc_mode
    return cv_mode, cp_mode, cc_mode

def process_read12_command(rb_u16):
    # Place the readback value to a READ12 structure
    reg = READ12(rb_u16)

    # Take the individual bytes and join to get the needed value
    iout_average = reg.bits.average_iout
    
    return iout_average

def process_read13_command(rb_u16):
    # Place the readback value to a READ13 structure
    reg = READ13(rb_u16)

    # Take the individual bytes and join to get the needed value
    vout_10mV = reg.bits.average_vout
    
    return vout_10mV

def process_read14_command(rb_u16):
    # Place the readback value to a READ14 structure
    reg = READ14(rb_u16)
    # Take the individual bytes and join to get the needed value
    dac_10mV = reg.bits.dac_10mV
    dac_100mV = reg.bits.dac_100mV
    vout_dac = params.VOUT_DAC_OFFSET_V + (dac_100mV*0.1) - (dac_10mV*0.01)
    
    return vout_dac

# def process_read15_command(rb_u16): 
#     # Place the readback value to a READ15 structure
#     reg = READ15(rb_u16)
#     # Take the individual bytes
#     reg_watchdog = reg.bits.reg_watchdog
#     reg_do_vout_uv = reg.bits.reg_do_vout_uv
#     reg_do_vout_ov = reg.bits.reg_do_vout_ov
#     reg_do_ccsc = reg.bits.reg_do_ccsc
#     reg_do_issc = reg.bits.reg_do_issc
#     reg_do_cvo = reg.bits.reg_do_cvo

#     return reg_watchdog, reg_do_vout_uv, reg_do_vout_ov, reg_do_ccsc, reg_do_issc, reg_do_cvo

def process_read16_command(rb_u16):
    # Place the readback value to a READ16 structure
    reg = READ16(rb_u16)
    # Take the individual bytes
    reg_lo_bps_ov = reg.bits.reg_lo_bps_ov
    reg_lo_vout_uv = reg.bits.reg_lo_vout_uv
    reg_lo_vout_ov = reg.bits.reg_lo_vout_ov
    reg_lo_issc = reg.bits.reg_lo_issc
    reg_psuoff = reg.bits.reg_psuoff
    reg_lo_cvo = reg.bits.reg_lo_cvo
    reg_lo_fault = reg.bits.reg_lo_fault
    reg_ar_vout_uv = reg.bits.reg_ar_vout_uv
    reg_ar_vout_ov = reg.bits.reg_ar_vout_ov
    reg_ar_ccsc = reg.bits.reg_ar_ccsc
    reg_ar_issc = reg.bits.reg_ar_issc
    reg_ar_cvo = reg.bits.reg_ar_cvo
    
    return reg_lo_bps_ov, reg_lo_vout_uv, reg_lo_vout_ov, reg_lo_issc, reg_psuoff, reg_lo_cvo, reg_lo_fault, reg_ar_vout_uv, reg_ar_vout_ov, reg_ar_ccsc, reg_ar_issc, reg_ar_cvo

def process_read17_command(rb_u16):
    # Place the readback value to a READ17 structure
    reg = READ17(rb_u16)
    # Take the individual bytes
    control_s_int_mask = reg.bits.control_s_int_mask
    lo_fault_int_mask = reg.bits.lo_fault_int_mask
    cvo_ar_int_mask = reg.bits.cvo_ar_int_mask
    issc_int_mask = reg.bits.issc_int_mask
    ccsc_int_mask = reg.bits.ccsc_int_mask
    uv_int_mask = reg.bits.uv_int_mask
    ov_int_mask = reg.bits.ov_int_mask
    omf_int_status = reg.bits.omf_int_status
    vbussc_int_status = reg.bits.vbussc_int_status
    control_s_int_status = reg.bits.control_s_int_status
    cvo_ar_int_status = reg.bits.cvo_ar_int_status
    issc_int_status = reg.bits.issc_int_status
    ccsc_int_status = reg.bits.ccsc_int_status
    lo_fault_int_status = reg.bits.lo_fault_int_status
    uv_int_status = reg.bits.uv_int_status
    ov_int_status = reg.bits.ov_int_status
    
    
    return control_s_int_mask, lo_fault_int_mask, cvo_ar_int_mask, issc_int_mask, ccsc_int_mask, uv_int_mask, ov_int_mask, omf_int_status, vbussc_int_status, control_s_int_status, cvo_ar_int_status, issc_int_status, ccsc_int_status, lo_fault_int_status, uv_int_status, ov_int_status

def process_read18_command(rb_u16): 
    # Place the readback value to a READ18 structure
    reg = READ18(rb_u16)
    # Take the individual bytes and join to get the needed value
    fast_cc_offset = reg.bits.fast_cc_offset
    fast_cc_enable = reg.bits.fast_cc_enable
    slow_cc_offset = reg.bits.slow_cc_offset

    return fast_cc_offset, fast_cc_enable, slow_cc_offset

def process_read19_command(rb_u16):
    # Place the readback value to a READ19 structure
    reg = READ19(rb_u16)
    # Take the individual bytes and join to get the needed value
    cv_small_step_thresh = reg.bits.cv_small_step_thresh
    cv_large_step_thresh = reg.bits.cv_large_step_thresh

    return cv_small_step_thresh, cv_large_step_thresh

def process_read20_command(rb_u16):
    # Place the readback value to a READ20 structure
    reg = READ20(rb_u16)
    # Take the individual bytes and join to get the needed value
    cc_small_step_thresh = reg.bits.cc_small_step_thresh
    cc_large_step_thresh = reg.bits.cc_large_step_thresh
    small_step_size = reg.bits.small_step_size
    large_step_size = reg.bits.large_step_size

    return cc_small_step_thresh, cc_large_step_thresh, small_step_size, large_step_size