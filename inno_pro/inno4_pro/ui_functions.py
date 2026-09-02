from dll import SLABHIDtoSMBUS as smbus
from dll.SLABHIDtoSMBUS import (HID_SMBUS_S0, HID_SMBUS_S1) 
from dll.hidsmbus_definitions import HID_SMBUS_DEFINITIONS as HID_SMBUS

from inno_pro.inno4_pro.definitions import *
from inno_pro.inno4_pro.functions import *
from inno_pro.inno4_pro.ui_definitions import *
from inno_pro.inno4_pro.controller import *
from page_controls.definitions import *
from misc_functions.misc_functions import *
from inno_pro.functions import *
from inno_pro.definitions import *

from sink_controllers.pat_tool import PDSinkController, InnoProI2CControllerContainer
from sink_controllers.pi_epr_sink import PISinkController

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

params = Inno4Pro_Parameters
commands = Inno4Pro_I2C_Commands
defaults = Inno4Pro_I2C_Defaults

page_name = "i2c_controls"


def inno4_i2c_initialize(page_handler):
    status_list = []
    i2c_controller:InnoProI2CControllerContainer = page_handler.i2c_controller
    usbpd_sink:PISinkController|PDSinkController = page_handler.usbpd_sink
    try:
        if page_handler.message_type.currentText() == InnoPro_MessageType.I2C:
            status_list.append(i2c_controller.watchdog(commands.WATCHDOG_OFF))

            status_list.append(i2c_controller.uva(
                    params.UV_MIN_V,
                    commands.UVA_RESP_AR,
                    commands.UVA_TIMER_8MS))
            
            status_list.append(i2c_controller.ova(
                    params.OV_MAX_V,
                    commands.OVA_RESP_AR))
            
            status_list.append(i2c_controller.cvo(
                    commands.CVO_RESP_AR,
                    commands.CVO_TIMER_8MS,
                    commands.CVO_CV_CC_MODE))
        
            status_list.append(i2c_controller.fwd_peak(
                    pre_shift_ns=commands.FWD_PEAK_PRESHIFT_90NS,
                    window_pct=commands.FWD_PEAK_WINDOW_15_35_PCT,
                    fwd_peak_en=commands.FWD_PEAK_ENABLE))
        
        elif page_handler.message_type.currentText() in InnoProMessageUVDMList:
            
            usbpd_sink.usb_pd_initialize()
            # usbpd_sink.vdm_initialize()
            
            if page_handler.message_type.currentText() == InnoPro_MessageType.UVDM_PDC1:
                cmd_fnc = usbpd_sink.send_uvdm_i2c_write_message_pdc1
            elif page_handler.message_type.currentText() == InnoPro_MessageType.UVDM_PDC2:
                cmd_fnc = usbpd_sink.send_uvdm_i2c_write_message_pdc2
            else:
                raise TypeError("No valid UVDM type selected")
            
            status_list.append(cmd_fnc(Inno4Pro_I2C_Registers.WATCHDOG_REG,
                                                process_watchdog_command(commands.WATCHDOG_OFF).asbyte))
            
            status_list.append(cmd_fnc(Inno4Pro_I2C_Registers.UVA_REG,
                                                process_uva_command(
                                                    params.UV_MIN_V,
                                                    commands.UVA_RESP_AR,
                                                    commands.UVA_TIMER_8MS).asbyte))
            
            status_list.append(cmd_fnc(Inno4Pro_I2C_Registers.OVA_REG,
                                                process_ova_command(
                                                    params.OV_MAX_V,
                                                    commands.OVA_RESP_AR).asbyte))
            
            status_list.append(cmd_fnc(Inno4Pro_I2C_Registers.CVO_REG,
                                                process_cvo_command(
                                                    commands.CVO_RESP_AR,
                                                    commands.CVO_TIMER_8MS,
                                                    commands.CVO_CV_CC_MODE).asbyte))
            
            status_list.append(cmd_fnc(Inno4Pro_I2C_Registers.FWD_PEAK_REG,
                                                process_fwd_peak_command(
                                                    pre_shift_ns=commands.FWD_PEAK_PRESHIFT_90NS,
                                                    window_pct=commands.FWD_PEAK_WINDOW_15_35_PCT,
                                                    fwd_peak_en=commands.FWD_PEAK_ENABLE).asbyte))
    finally:
        test = HID_SMBUS_S0.COMPLETE
        if all(test == element for element in status_list) \
            and len(status_list)>0:
            status = HID_SMBUS_S0.COMPLETE
        else:
            status = -1

        return status

def inno4_i2c_set_nr(page_handler):
    status_list = []
    i2c_controller:InnoProI2CControllerContainer = page_handler.i2c_controller
    usbpd_sink:PISinkController|PDSinkController = page_handler.usbpd_sink
    try:
        if page_handler.message_type.currentText() == InnoPro_MessageType.I2C:
            status_list.append(i2c_controller.watchdog(commands.WATCHDOG_OFF))
            status_list.append(i2c_controller.uva(
                    params.UV_MIN_V,commands.UVA_RESP_NR,
                    commands.UVA_TIMER_8MS))
            status_list.append(i2c_controller.ova(
                    params.OV_MAX_V,commands.OVA_RESP_NR))
            status_list.append(i2c_controller.cvo(
                    commands.CVO_RESP_NR,
                    commands.CVO_TIMER_8MS,
                    commands.CVO_CV_CC_MODE))
            status_list.append(i2c_controller.ccsc(
                    response=commands.CCSC_RESP_NR))
            status_list.append(i2c_controller.issc(
                    threshold_bits=commands.ISSC_CC_LIMIT_48,
                    threshold_freq=commands.ISSC_FREQ_60KHZ,
                    response=commands.ISSC_RESP_NR))
            status_list.append(i2c_controller.vbussc(
                    threshold_bits=commands.VBUSSC_IS_VAL_48,
                    num_samples=commands.VBUSSC_SAMPLE_2,
                    response=commands.VBUSSC_RESP_NR))
        
        elif page_handler.message_type.currentText() in InnoProMessageUVDMList:
            
            usbpd_sink.usb_pd_initialize()
            # usbpd_sink.vdm_initialize()
            
            if page_handler.message_type.currentText() == InnoPro_MessageType.UVDM_PDC1:
                cmd_fnc = usbpd_sink.send_uvdm_i2c_write_message_pdc1
            elif page_handler.message_type.currentText() == InnoPro_MessageType.UVDM_PDC2:
                cmd_fnc = usbpd_sink.send_uvdm_i2c_write_message_pdc2
            else:
                raise TypeError("No valid UVDM type selected")
            
            status_list.append(cmd_fnc(Inno4Pro_I2C_Registers.WATCHDOG_REG,
                                                process_watchdog_command(commands.WATCHDOG_OFF).asbyte))
            
            status_list.append(cmd_fnc(Inno4Pro_I2C_Registers.UVA_REG,
                                                process_uva_command(
                                                    params.UV_MIN_V,commands.UVA_RESP_NR,
                                                    commands.UVA_TIMER_8MS).asbyte))
            
            status_list.append(cmd_fnc(Inno4Pro_I2C_Registers.OVA_REG,
                                                process_ova_command(
                                                    params.OV_MAX_V,
                                                    commands.OVA_RESP_NR).asbyte))
            
            status_list.append(cmd_fnc(Inno4Pro_I2C_Registers.CVO_REG,
                                                process_cvo_command(
                                                    commands.CVO_RESP_NR,
                                                    commands.CVO_TIMER_8MS,
                                                    commands.CVO_CV_CC_MODE).asbyte))
            
            status_list.append(cmd_fnc(Inno4Pro_I2C_Registers.ISSC_REG,
                                                process_issc_command(
                                                    threshold_bits=commands.ISSC_CC_LIMIT_48,
                                                    threshold_freq=commands.ISSC_FREQ_60KHZ,
                                                    response=commands.ISSC_RESP_NR).asbyte))
            
            status_list.append(cmd_fnc(Inno4Pro_I2C_Registers.VBUSSC_REG,
                                                process_vbussc_command(
                                                    threshold_bits=commands.VBUSSC_IS_VAL_48,
                                                    num_samples=commands.VBUSSC_SAMPLE_2,
                                                    response=commands.VBUSSC_RESP_NR).asbyte))
            
        
    finally:
        test = HID_SMBUS_S0.COMPLETE
        if all(test == element for element in status_list) \
            and len(status_list)>0:
            status = HID_SMBUS_S0.COMPLETE
        else:
            status = -1
        return status
         
# General write Register
def inno4_send_command_write(page_handler,reg:INNO4_WRITE_REG_UI):
    status = -1
    i2c_controller:Inno4ProI2CController = page_handler.i2c_controller
    usbpd_sink:PISinkController|PDSinkController = page_handler.usbpd_sink
    reg_address, data_lsb, data_msb = reg.validate()
    try:
        if (reg_address is not None) and (data_lsb is not None) and (data_msb is not None):
            u16_val = join_8bits(data_msb,data_lsb)
            if page_handler.message_type.currentText() == InnoPro_MessageType.I2C:
                fnc_write = i2c_controller.process_write_2bytes
            elif page_handler.message_type.currentText() == InnoPro_MessageType.UVDM_PDC1:
                fnc_write = usbpd_sink.send_uvdm_i2c_write_message_pdc1
            elif page_handler.message_type.currentText() == InnoPro_MessageType.UVDM_PDC2:
                fnc_write = usbpd_sink.send_uvdm_i2c_write_message_pdc2
            else:
                pass
            if reg_address == Inno4Pro_I2C_Registers.LOOP_OPTION_REG:
                status_list = []
                status_list.append(fnc_write(0x5E,join_8bits(commands.UNLOCK_SREG_1_MSB,commands.UNLOCK_SREG_1_LSB)))
                status_list.append(fnc_write(0x5E,join_8bits(commands.UNLOCK_SREG_2_MSB,commands.UNLOCK_SREG_2_LSB)))
                status_list.append(fnc_write(reg_address,u16_val))
                status_list.append(fnc_write(0x5E,join_8bits(commands.LOCK_SREG_1_MSB,commands.LOCK_SREG_1_LSB)))
                status_list.append(fnc_write(0x5E,join_8bits(commands.LOCK_SREG_2_MSB,commands.LOCK_SREG_2_LSB)))
                test = HID_SMBUS_S0.COMPLETE
                if all(test == element for element in status_list) \
                    and len(status_list)>0:
                    status = HID_SMBUS_S0.COMPLETE
                else:
                    status = -1
            else:
                status = fnc_write(reg_address,u16_val)
        elif (reg_address is not None) and (data_lsb is not None):
            if page_handler.message_type.currentText() == InnoPro_MessageType.I2C:
                fnc_write = i2c_controller.process_write_1byte
            elif page_handler.message_type.currentText() == InnoPro_MessageType.UVDM_PDC1:
                fnc_write = usbpd_sink.send_uvdm_i2c_write_message_pdc1
            elif page_handler.message_type.currentText() == InnoPro_MessageType.UVDM_PDC2:
                fnc_write = usbpd_sink.send_uvdm_i2c_write_message_pdc2
            else:
                pass
            status = fnc_write(reg_address,data_lsb)
    finally:
        return status, reg.send
    
# Readback Registers 
    
def inno4_send_command_read(page_handler,read_reg:INNO4_READ_REG_UI):
    status = -1
    i2c_controller:Inno4ProI2CController = page_handler.i2c_controller
    usbpd_sink:PDSinkController = page_handler.usbpd_sink
    read_reg.validate()
    reg_address = read_reg.reg_address_byte
    rb_u16 = None
    try:
        if reg_address is not None:
            if page_handler.message_type.currentText() == InnoPro_MessageType.I2C:
                rb_u16 = i2c_controller.read_u16(reg_address)
            elif page_handler.message_type.currentText() == InnoPro_MessageType.UVDM_PDC1:
                status, rb_u16 = usbpd_sink.send_uvdm_i2c_read_message_pdc1(reg_address)
            elif page_handler.message_type.currentText() == InnoPro_MessageType.UVDM_PDC2:
                status, rb_u16 = usbpd_sink.send_uvdm_i2c_read_message_pdc2(reg_address)
            else:
                pass
            if rb_u16 is not None:
                status = HID_SMBUS_S0.COMPLETE
                read_reg.update_i2c_data(rb_u16)
    finally:
        return status, read_reg.send

from page_controls.i2c_controls import i2c_access, send_btn_update

@i2c_access
@send_btn_update
def inno4_run_cmd_fnc(page_handler, cmd_fnc, *args,**kwargs):
    return cmd_fnc(page_handler,*args,**kwargs)

def inno4_queue_cmd_fnc(page_handler, reg:INNO4_WRITE_REG_UI, *args,**kwargs):
    fnc_name = reg.reg_label
    extra_params = [InnoProFamily.Inno4Pro]
    command = None
    value, ui_params = reg.extract_command_parameters()
    try:
        if value is not None:
            extra_params = [InnoProFamily.Inno4Pro,ui_params]
            command = I2CCommandObject(fnc_name, value, extra_params)
    except Exception as e:
        print(e)  

    if command is not None:
        page_handler.i2c_command_list.append(command)
        page_handler.update_i2c_command_list_table()
        
# Execute any queued command Register
def inno4_run_queue_command_write(page_handler,fnc_name,value:str,extra_params:list):
    try:
        reg_index = page_handler.cmd_reg_name_list.index(fnc_name)
        reg = page_handler.cmd_reg_list[reg_index]
        ui_params = extra_params[1]
        reg.set_parameters_from_list(ui_params)
        inno_pro_family = extra_params[0]
        if not (inno_pro_family == InnoProFamily.Inno4Pro):
            return    
        else:
            reg.send.click()
    except Exception as e:
        print(e)
    
def inno4_queue_readback_fnc(page_handler, reg, *args, **kwargs):
    fnc_name = None
    value = None
    extra_params = [InnoProFamily.Inno4Pro]
    if (type(reg) == INNO4_READ_REG_UI):
        reg_address = reg.validate()
        if reg_address is not None:
            fnc_name = reg.reg_label
            value = reg_address
            command = I2CCommandObject(fnc_name,value,extra_params)
        else:
            command = None
    else:
        fnc_name = reg.reg_label
        value = None
        command = I2CCommandObject(fnc_name,value,extra_params)
    if command is not None:
        page_handler.i2c_command_list.append(command)
        page_handler.update_i2c_command_list_table()

# Run queued readback register
def inno4_run_queue_command_read(page_handler,fnc_name,value,extra_params:list):
    try:
        reg_index = page_handler.cmd_readback_reg_name_list.index(fnc_name)
        reg = page_handler.cmd_readback_reg_list[reg_index]
        if reg.reg_label == INNO4_READ_REG_UI.reg_label:
            reg.set_parameters_from_data(value)
        if not(extra_params[0] == InnoProFamily.Inno4Pro):
            return    
        else:
            reg.send.click()
    except Exception as e:
        print(e)

def inno4_create_reg_ui(page_handler,frame,grid,reg_ui:INNO4_WRITE_REG_UI):
    reg = reg_ui(frame,grid)
    cmd_fnc = inno4_send_command_write
    reg.send.clicked.connect(lambda: inno4_run_cmd_fnc(page_handler,cmd_fnc,reg))
    reg.queue.clicked.connect(lambda: inno4_queue_cmd_fnc(page_handler,reg))
    return reg

def inno4_create_readback_reg_ui(page_handler,frame,grid,reg_ui:INNO4_READ_REG_UI):
    reg = reg_ui(frame,grid)
    cmd_fnc =  inno4_send_command_read
    reg.send.clicked.connect(lambda: inno4_run_cmd_fnc(page_handler,cmd_fnc,reg))
    reg.queue.clicked.connect(lambda: inno4_queue_readback_fnc(page_handler,reg))
    return reg