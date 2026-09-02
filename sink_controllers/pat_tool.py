# Standard Python Library Imports
import math
from time import sleep
from functools import wraps
from enum import Enum
from ctypes import c_uint16, c_ubyte
import hid

# For controlling the CP2112 interface
from dll import SLABHIDtoSMBUS as smbus
from dll.SLABHIDtoSMBUS import (HID_SMBUS_S0, HID_SMBUS_S1) 
from dll.hidsmbus_definitions import HID_SMBUS_DEFINITIONS as HID_SMBUS


# Define PD commands, CCG2 register structures and responses
from pd import pd_types
from pd.pd_types import PD_COMMAND, HPI_V1_REG as CY_PD_REG, HPI_RESPONSE as CY_PD_RESP
from pd import protocol
from pd.pd_types import *

from sink_controllers.exceptions import *
from sink_controllers.misc_functions import *
from sink_controllers.definitions import *

from PySide2.QtCore import (
    QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QTimer,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent, Signal, Slot, QThread)

# Needed for running PPS requests periodically
from threading import Timer

from misc_functions.misc_functions import timeit

FAST_I2C_WRITE = True

class Comms:
    UNLOCK = 0
    LOCK = 1

class PAT_TOOL_SETTINGS():
    PPS_REQUEST_INTERVAL_SEC = 3

class SMBUS_STATE:
    DISCONNECTED        = 0
    CONNECTED           = 1
    ERROR               = 2
    
class DEVICE_INFO:
    VID = HID_SMBUS.VID.value
    PID = HID_SMBUS.PID.value
    MFG = 'Silicon Laboratories'
    PROD = 'CP2112 HID USB-to-SMBus Bridge'
    SLAVE_ADDR = 0X10

class I2CWriteError(Exception):
    pass

class I2CReadBackError(Exception):
    pass

def i2c_write_handling(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 5 retries maximum
        for i in range(0, 10):
            S0_status, S1_status, *_ = func(*args, **kwargs)
            if not FAST_I2C_WRITE:
                sleep(0.05)
            # Proceed if transfer is complete
            if S0_status == HID_SMBUS_S0.COMPLETE:
                return S0_status
            
            elif S0_status == HID_SMBUS_S0.ERROR:
                if S1_status == HID_SMBUS_S1.ERROR_TIMEOUT_NACK:
                    raise I2CWriteError("I2C Device NACK, Timeout")
                else:
                    # Retry if there is an error
                    print(f"Retry #{i}")
                    continue
            elif S0_status == HID_SMBUS_S0.BUSY:
                    raise I2CWriteError("SMBUS Busy")
            
        raise I2CWriteError("Exceeded write retry attempts")

    return wrapper

def readback_retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 15 retries maximum
        for i in range(0, 15):
            try:
                return func(*args, **kwargs)
            except I2CWriteError as e:
                print(f"Readback retry {i+1}")
            sleep(0.01)
        raise I2CReadBackError("Exceeded readback attempts")
    return wrapper

class CP2112(smbus.HidSmbusDevice):
    """ USB HID to SMBUS Device Class

        CP2112 is an interface for USB to connect to SMBUS (I2C) devices
        It is used in this program to connect to multiple PD sink controller devices (CCG2)
        This class uses SLABHIDtoSMBUS.dll from Silicon Labs through the wrapper taken from
        Silicon Labs USBXpressHostSdk
        # https://www.silabs.com/documents/public/software/USBXpressHostSDK-Win.zip

        And can be found in the below directory after installing
        # C:/SiliconLabs/USBXpressHostSDK/CP2112/Release/x64
    """
    def __init__(self, *args, **kwargs):
        super().__init__()

        # CP2112 VID and PID defined in datasheet
        self._vid = DEVICE_INFO.VID
        self._pid = DEVICE_INFO.PID
        self.serial_number = ''

        # Placeholder for PD sink controller objects to be controlled by the SMBUS interface
        self.pd_sink_controllers = []
        
        self.connection_status = SMBUS_STATE.DISCONNECTED

        self.slave_address = DEVICE_INFO.SLAVE_ADDR
        self.open_status = False
        # Open the
        # self.set_smbus_config()



    ###############################################################################################
    #  Functions using dll wrapper configured for PAT tool use                                    #
    ###############################################################################################

    def open(self,serial_num:str=''):
        self.num_devices = smbus.GetNumDevices()

        if self.num_devices == 0:
            # print("No PAT tool detected.")
            self.connection_status = SMBUS_STATE.DISCONNECTED
        
        # elif self.num_devices > 1:
        #     print("More than 1 PAT tool is detected. Please remove the unused device")
        #     self.connection_status = SMBUS_STATE.ERROR
        else:
            if not self.open_status:
                if serial_num == '':
                    for index in range(self.num_devices):
                        try:
                            self.Open(index=index)
                            string = self.GetString(HID_SMBUS.SERIAL_STR.value)
                            self.serial_number = string
                            self.set_smbus_config()
                            self.connection_status = SMBUS_STATE.CONNECTED
                            # print("PAT tool opened successfully")
                            self.open_status = self.IsOpened()
                            break
                        except Exception as e:
                            if self.open_status:
                                self.close()
                                self.open_status = self.IsOpened()
                            # print(e)
                            # print(f"PAT tool is detected but cannot be" 
                                # f" accessed by this program.")
                            self.connection_status = SMBUS_STATE.ERROR
                else:
                    device_list = hid.enumerate(vendor_id=DEVICE_INFO.VID,product_id=DEVICE_INFO.PID)
                    hid_index = self.num_devices - len(device_list)
                    for hid_device in hid.enumerate(vendor_id=DEVICE_INFO.VID,product_id=DEVICE_INFO.PID):
                        if serial_num == hid_device['serial_number']:
                            break
                        else:
                            hid_index += 1
                    if hid_index < self.num_devices:
                        try:
                            self.Open(index = hid_index)
                            string = self.GetString(HID_SMBUS.SERIAL_STR.value)
                            self.serial_number = string
                            self.set_smbus_config()
                            self.connection_status = SMBUS_STATE.CONNECTED
                            # print("PAT tool opened successfully")
                            self.open_status = self.IsOpened()
                        except Exception as e:
                            if self.open_status:
                                self.close()
                                self.open_status = self.IsOpened()
                            # print(e)
                            # print(f"PAT tool is detected but cannot be" 
                                # f" accessed by this program.")
                            self.connection_status = SMBUS_STATE.ERROR
                    else:
                        # print(f"PAT Tool with SN {serial_num} not detected.")
                        self.connection_status = SMBUS_STATE.DISCONNECTED
        self.open_status = self.IsOpened()
                                       
    def close(self):
        if self.IsOpened():
            self.set_smbus_config()
            self.Close()
            # print("PAT Tool Closed")
        self.open_status = self.IsOpened()

    def reset(self):
        if self.IsOpened():
            self.Reset()
        self.open_status = self.IsOpened()
        self.open(serial_num=self.serial_number)
        self.open_status = self.IsOpened()
        self.set_smbus_config()
                    
    def set_smbus_config(self):
        address = 0x2
        autoReadRespond = 0
        writeTimeout = 1000
        readTimeout = 1000
        sclLowTimeout = 0
        transferRetries = 2
        bitRate = 400000

        if self.open_status:
            self.SetSmbusConfig(bitRate, address, autoReadRespond, writeTimeout,
                readTimeout,sclLowTimeout, transferRetries)
    
    # CCG2 device address is 0x08 with 7bit addressing
    def write(self, write_buffer, device_addr=None):
        if self.open_status:
            if device_addr is None:
                device_addr = self.slave_address
            self.WriteRequest(device_addr, write_buffer, len(write_buffer))
            return self.hid_get_transfer_status()

    def read(self, num_bytes, device_addr=None):
        if device_addr is None:
            device_addr = self.slave_address
        self.hid_read_request(device_addr,num_bytes)
        self.hid_get_transfer_status()
        self.hid_force_read_response(num_bytes)

        ret_bytes = self.hid_get_read_response()[:num_bytes]
        # CP2112 does not give readback if byte is 0
        # Fill the missing with bytes containing 0
        while len(ret_bytes) < num_bytes: 
            ret_bytes.append(0)
        
        return ret_bytes
    @readback_retry
    def address_read(self, slave_address, register_address, num_bytes_to_read):
        """Reads the value of a register

        Keyword arguments:
        @   register_address    --  register address to be read
        @   num_bytes_to_read   --  number of bytes to read
        """

        self.hid_address_read_request(slave_address,register_address,num_bytes_to_read)
        self.hid_get_transfer_status()
        self.hid_force_read_response(num_bytes_to_read)
        read_buffer =  self.hid_get_read_response()[:num_bytes_to_read]
        while len(read_buffer) < num_bytes_to_read: 
            read_buffer.append(0)
        return read_buffer

    def hid_read_request(self, slave_address:int, num_bytes:int):
        """ Initiate a read transfer from the specified slave device address.

        Keyword arguments:
        @   slave_address    --  register address to be read
        @   num_bytes        --  number of bytes to read
        """
        if self.open_status:
            self.ReadRequest(address=slave_address, count=num_bytes)

    def hid_address_read_request(self, slave_address, register_address, num_bytes_to_read):
        
        # Make sure that the device is Opened
        if self.open_status:# == HID_SMBUS.SUCCESS:
            
            # Issue an address read request
            offset = (register_address).to_bytes(length=1, byteorder='big')
            status = self.AddressReadRequest(address=slave_address,
                                            count=num_bytes_to_read,
                                            offset_size=1,
                                            offset=offset)

    def hid_get_transfer_status(self):
        if self.open_status:
            self.TransferStatusRequest()
            return self.GetTransferStatusResponse()
        else:
            return None
        
    def hid_force_read_response(self, num_bytes_to_read):
        if self.open_status:
            self.ForceReadResponse(count=num_bytes_to_read)
        
    def hid_get_read_response(self):
        if self.open_status:
            read_buffer = self.GetReadResponse()
            read_buffer_list = list(bytes(read_buffer))
            return read_buffer_list     

from inno_pro.definitions import *
from inno_pro.functions import *

class InnoProI2CControllerContainer(CP2112):
    """ Class for the SMBUS interface to directly send I2C commands to DUT.
        Used specifically for InnoSwitch Pro family devices
    """
    def __init__(self, rsense_mohm=6, *args, **kwargs):
        super().__init__()
        self.rsense_mohm = rsense_mohm
        self.update_controller(InnoProFamily.Inno5Pro)
        self.smbus = None
        self.open()
        self.update_device_description()

    def update_device_description(self):
        
        self.description = f"TST-058 PAT Tool, SN: {self.serial_number}"# : Port {self.port}"
        self.details =  (   f"CP2112 + CYPD2122 based \n"
                            f"I2C Interface and  USB-PD Sink Controller\n"
                            f"VID = {self._vid}\tPID = {self._pid}")
    
    def update_controller(self,innopro_family=InnoProFamily.Inno5Pro):
        self.innoswitch_family = innopro_family
        match self.innoswitch_family:
            case InnoProFamily.Inno5Pro:
                self.controller = Inno5ProI2CController()
            case InnoProFamily.Inno4Pro:
                self.controller = Inno4ProI2CController()
        self.slave_address = self.controller.slave_address
        self.rsense_mohm = self.controller.rsense_mohm
        self.imax_A = self.controller.imax_A
        self.registers = self.controller.registers
        self.commands = self.controller.commands
        self.defaults = self.controller.defaults
        self.params = self.controller.params
        self.readback_commands = self.controller.readback_commands
        self.readback_commands_list = self.controller.readback_commands_list
        self.registers_list = self.controller.registers_list
                
    def update_rsense(self, rsense_mohm):
        self.rsense_mohm = rsense_mohm
        self.controller.update_rsense(rsense_mohm)
        self.imax_A = self.controller.imax_A
        
    def process_send_i2c_write(self, reg_addr, i2c_data, data_byte_count:int = 2):
        """Write either a 2 byte or 1 byte value to a register."""
        if data_byte_count == 2:
            return self.process_write_2bytes(reg_addr = reg_addr, u16_val = i2c_data)
        elif data_byte_count == 1:
            return self.process_write_1byte(reg_addr = reg_addr, u8_val = i2c_data)
        else:
            I2CWriteError('Incorrect number of data bytes')
            return HID_SMBUS_S0.ERROR
            
    @i2c_write_handling
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
    
    @i2c_write_handling
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

    def vben(self, *args, **kwargs):
        """Configure the VBEN register"""
        reg, valid = self.controller.vben(*args, **kwargs)
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.VBEN_REG,
            i2c_data=reg.asbyte,data_byte_count=1)
        else:
            return None
    
    def bleeder(self, *args, **kwargs):
        """Configure the Bleeder (BLEEDER) register"""
        reg, valid = self.controller.bleeder(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.BLEEDER_REG,
            i2c_data=reg.asbyte,data_byte_count=1)
        else:
            return None
    
    def cv(self, *args, **kwargs):
        """Configure the Constant Voltage (CV) register"""
        reg, valid = self.controller.cv(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.CV_REG,
            i2c_data=reg.asbyte,data_byte_count=2)
        else:
            return None
        
        
    def cc(self, *args, **kwargs):
        """Configure the Constant Current (CC) register"""
        reg, valid = self.controller.cc(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.CC_REG,
            i2c_data=reg.asbyte,data_byte_count=2)
        else:
            return None
    
    def vkp(self, *args, **kwargs):
        """Configure the Constant Power Knee Voltage (VKP) register"""
        reg, valid = self.controller.vkp(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.VKP_REG,
            i2c_data=reg.asbyte,data_byte_count=2)
        else:
            return None
        
    def cdc(self, *args, **kwargs):
        """Configure the Cable Drop Compensation (CDC) register"""
        reg, valid = self.controller.cdc(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.CDC_REG,
            i2c_data=reg.asbyte,data_byte_count=1)
        else:
            return None

    def ova(self, *args, **kwargs):
        """Configure the Absolute Over Voltage (OVA) register"""
        reg, valid = self.controller.ova(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.OVA_REG,
            i2c_data=reg.asbyte,data_byte_count=2)
        else:
            return None
    
    def uva(self, *args, **kwargs):
        """Configure the Absolute Under Voltage (UVA) register"""
        reg, valid = self.controller.uva(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.UVA_REG,
            i2c_data=reg.asbyte,data_byte_count=2)
        else:
            return None
    
    def cvo(self, *args, **kwargs):
        """Configure the Constant Voltage Only (CVO) register"""
        reg, valid = self.controller.cvo(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.CVO_REG,
            i2c_data=reg.asbyte,data_byte_count=1)
        else:
            return None
    
    def ccsc(self, *args, **kwargs):
        """Configure the Constant Current Short Circuit (CCSC) register"""
        reg, valid = self.controller.ccsc(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.CCSC_REG,
            i2c_data=reg.asbyte,data_byte_count=1)
        else:
            return None
        
    def issc(self, *args, **kwargs):
        """Configure the IS pin Short Circuit (ISSC) register"""
        reg, valid = self.controller.issc(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.ISSC_REG,
            i2c_data=reg.asbyte,data_byte_count=1)
        else:
            return None
        
    def vbussc(self, *args, **kwargs):
        """Configure the Bus Switch Short Circuit (VBUSSC) register"""
        reg, valid = self.controller.vbussc(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.VBUSSC_REG,
            i2c_data=reg.asbyte,data_byte_count=1)
        else:
            return None
       
    def watchdog(self, *args, **kwargs):
        """Configure the Watchdog (WATCHDOG) register"""
        reg, valid = self.controller.watchdog(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.WATCHDOG_REG,
            i2c_data=reg.asbyte,data_byte_count=1)
        else:
            return None
        
    def fast_vi(self, *args, **kwargs):
        """Configure the Fast VI (FAST_VI) register"""   
        reg, valid = self.controller.fast_vi(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.FAST_VI_REG,
            i2c_data=reg.asbyte,data_byte_count=1)
        else:
            return None
        
    def vdis(self, *args, **kwargs):
        """Configure the VDIS register"""  
        reg, valid = self.controller.vdis(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.VDIS_REG,
            i2c_data=reg.asbyte,data_byte_count=1)
        else:
            return None
    
    def turn_off_psu(self, *args, **kwargs):
        """"Configure the LATCH_OFF register"""    
        reg, valid = self.controller.turn_off_psu(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.TURN_OFF_PSU_REG,
            i2c_data=reg.asbyte,data_byte_count=1)
        else:
            return None
    
    def dcm_only(self, *args, **kwargs):
        """Configure the DCM Only (DCM_ONLY) register"""
        reg, valid = self.controller.dcm_only(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.DCM_ONLY_REG,
            i2c_data=reg.asbyte,data_byte_count=1)
        else:
            return None
        
    def sr_zvs(self, *args, **kwargs):
        """Configure the SR ZVS (SR_ZVS) register"""
        reg, valid = self.controller.sr_zvs(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.SR_ZVS_REG,
            i2c_data=reg.asbyte,data_byte_count=2)
        else:
            return None
    def int_mask(self, *args, **kwargs):
        """Configure the Interrupt Mask (INT_MASK) register"""
        reg, valid = self.controller.int_mask(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.INT_MASK_REG,
            i2c_data=reg.asbyte,data_byte_count=2)
        else:
            return None
        
    def line_sense(self, *args, **kwargs):
        """Configure the Line Sense (LINE_SENSE) register"""
        reg, valid = self.controller.line_sense(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.LINE_SENSE_REG,
            i2c_data=reg.asbyte,data_byte_count=1)
        else:
            return None
     
    def fwd_peak(self, *args, **kwargs):
        """Configure the FWD Peak (FWD_PEAK) register"""
        reg, valid = self.controller.fwd_peak(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.FWD_PEAK_REG,
            i2c_data=reg.asbyte,data_byte_count=1)
        else:
            return None
    
    def loopspeed_1(self, *args, **kwargs):
        """Configure the Loop Speed 1 (LOOPSPEED_1) register"""       
        reg, valid = self.controller.loopspeed_1(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.LOOPSPEED_1_REG,
            i2c_data=reg.asbyte,data_byte_count=2)
        else:
            return None
    
    def loopspeed_2(self, *args, **kwargs):
        """Configure the Loop Speed 2 (LOOPSPEED_2) register"""
        reg, valid = self.controller.loopspeed_2(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.LOOPSPEED_2_REG,
            i2c_data=reg.asbyte,data_byte_count=2)
        else:
            return None
        
    def fast_cc(self, *args, **kwargs):
        """Configure the Fast CC (FAST_CC) register"""
        reg, valid = self.controller.fast_cc(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.FAST_CC_REG,
            i2c_data=reg.asbyte,data_byte_count=2)
        else:
            return None
        
    @i2c_write_handling    
    def loop_option(self, *args, **kwargs):
        reg, valid = self.controller.loop_option(*args, **kwargs)
        
        if valid:
            self.write([self.registers.LOCK_UNLOCK_SREG, 0x16, 0x20])
            self.write([self.registers.LOCK_UNLOCK_SREG, 0x34, 0x12])
            self.process_send_i2c_write(
            reg_addr=self.registers.LOOP_OPTION_REG,
            i2c_data=reg.asbyte,data_byte_count=2)
            self.write([self.registers.LOCK_UNLOCK_SREG, 0x16, 0x20])
            return self.write([self.registers.LOCK_UNLOCK_SREG, 0xCD, 0xAB])
            
        else:
            return None

    def sr_disable(self, *args, **kwargs):
        """Configure the SR DISABLE (SR_DISABLE) register"""
        reg, valid = self.controller.sr_disable(*args, **kwargs)
        
        if valid:
            return self.process_send_i2c_write(
            reg_addr=self.registers.SR_DISABLE_REG,
            i2c_data=reg.asbyte,data_byte_count=2)
        else:
            return None
        
    # READBACK
    def send_read_command(self, *args, **kwargs):
        """Generate a read request using the read command and requested register."""
        wb, valid = self.controller.send_read_command(*args, **kwargs)
        if valid:
            return self.write(wb)
        else:
            return None
    
    def get_read_value(self):
        rb = self.read(num_bytes=2)
        return list_to_uint16(rb)
    
    def read_u16(self, address):
        # Send a read command with the register READ5
        self.send_read_command(address)
        # Get the uint16 value of the readbback
        return self.get_read_value()
    
    @readback_retry
    def read_cv(self):
        """Return the CV setpoint register value."""
        if not hasattr(self.readback_commands,'READ_CV'):
            return None 
        rb_u16 = self.read_u16(self.readback_commands.READ_CV)
        return self.controller.read_cv(rb_u16)

    @readback_retry
    def read_cv_v(self):
        """Return the CV setpoint in Volts"""
        if not hasattr(self.readback_commands,'READ_CV'):
            return None
        rb_u16 = self.read_u16(self.readback_commands.READ_CV)
        return self.controller.read_cv_v(rb_u16)
    
    @readback_retry
    def read_vout_average_v(self):
        """Return the average output voltage in Volts."""
        if not hasattr(self.readback_commands,'READ_VOUT_AVE'):
            return None
        # Get a U16 value by doing a readback from the address
        rb_u16 = self.read_u16(self.readback_commands.READ_VOUT_AVE)
        return self.controller.read_vout_average_v(rb_u16)
    
    @readback_retry
    def read_vout_v(self):
        """Return the instantaneous output voltage in Volts."""
        if not hasattr(self.readback_commands,'READ_VOUT'):
            return None
        # Get a U16 value by doing a readback from the address
        rb_u16 = self.read_u16(self.readback_commands.READ_VOUT)
        return self.controller.read_vout_v(rb_u16)
        
    @readback_retry
    def read_vout_dac_v(self):
        """Return the Voltage DAC redback in Volts."""
        if not hasattr(self.readback_commands,'READ_VOLT_DAC'):
            return None
        # Get a U16 value by doing a readback from the address
        rb_u16 = self.read_u16(self.readback_commands.READ_VOLT_DAC)
        return self.controller.read_vout_dac_v(rb_u16)
    
    @readback_retry
    def read_ov_v(self):
        """Return the OV threshold in Volts."""
        if not hasattr(self.readback_commands,'READ_OV'):
            return None
        # Get a U16 value by doing a readback from the address
        rb_u16 = self.read_u16(self.readback_commands.READ_OV)
        return self.controller.read_ov_v(rb_u16)
        
    @readback_retry
    def read_uv_v(self):
        """Return the uV threshold in Volts."""
        if not hasattr(self.readback_commands,'READ_UV'):
            return None
        # Get a U16 value by doing a readback from the address
        rb_u16 = self.read_u16(self.readback_commands.READ_UV)
        return self.controller.read_uv_v(rb_u16)
    
    @readback_retry
    def read_cdc_mv(self):
        """Returns the CDC in mV from the readback"""
        if not hasattr(self.readback_commands,'READ_CDC'):
            return None
        # Get a U16 value by doing a readback from the address
        rb_u16 = self.read_u16(self.readback_commands.READ_CDC)
        return self.controller.read_cdc_mv(rb_u16)
	    
    @readback_retry
    def read_omf(self):
        """Returns the OMF readback"""
        if not hasattr(self.readback_commands,'READ_OMF_FLAG'):
            return None
        # Get a U16 value by doing a readback from the address
        rb_u16 = self.read_u16(self.readback_commands.READ_OMF_FLAG)
        # Get a U16 value by doing a readback from the address
        return self.controller.read_omf(rb_u16)

    @readback_retry
    def read_omf_txt(self):
        """Returns the OMF readback in text"""
        if not hasattr(self.readback_commands,'READ_OMF_FLAG'):
            return None
        # Get a U16 value by doing a readback from the address
        rb_u16 = self.read_u16(self.readback_commands.READ_OMF_FLAG)
        # Get a U16 value by doing a readback from the address
        return self.controller.read_omf_txt(rb_u16)
        
    @readback_retry
    def read_iout_average(self):
        """Return the 8-bit average measured current"""
        if not hasattr(self.readback_commands,'READ_IOUT_AVE'):
            return None
        # Get a U16 value by doing a readback from the address
        rb_u16 = self.read_u16(self.readback_commands.READ_IOUT_AVE)
        return self.controller.read_iout_average(rb_u16)
    
    @readback_retry
    def read_iout_average_a(self):
        """Return the average measured current in Amps."""
        if not hasattr(self.readback_commands,'READ_IOUT_AVE'):
            return None
        # Get a U16 value by doing a readback from the address
        rb_u16 = self.read_u16(self.readback_commands.READ_IOUT_AVE)
        return self.controller.read_iout_average_a(rb_u16)
    
    @readback_retry
    def read_cc(self):
        """Return the 8-bit CC setpoint value."""
        if not hasattr(self.readback_commands,'READ_CC'):
            return None
        # Get a U16 value by doing a readback from the address
        rb_u16 = self.read_u16(self.readback_commands.READ_CC)
        return self.controller.read_cc(rb_u16)
        
    @readback_retry
    def read_cc_a(self):
        """Return the CC setpoint value in amps"""
        if not hasattr(self.readback_commands,'READ_CC'):
            return None
        # Get a U16 value by doing a readback from the address
        rb_u16 = self.read_u16(self.readback_commands.READ_CC)
        return self.controller.read_cc_a(rb_u16)
        
    @readback_retry
    def read_vkp(self):
        """Return the VKP setpoint value"""
        if not hasattr(self.readback_commands,'READ_VKP'):
            return None
        # Get a U16 value by doing a readback from the address
        rb_u16 = self.read_u16(self.readback_commands.READ_VKP)
        return self.controller.read_vkp(rb_u16)
          
    @readback_retry  
    def read_vkp_v(self):
        """Return the constant power threshold in V
        To be multiplied by Iout full scale to get power"""
        if not hasattr(self.readback_commands,'READ_VKP'):
            return None
        # Get a U16 value by doing a readback from the address
        rb_u16 = self.read_u16(self.readback_commands.READ_VKP)
        return self.controller.read_vkp_v(rb_u16)
    
    @readback_retry
    # Line Sense Functions
    def read_line_sense_us(self)->tuple[int, int]:
        """Do the line sense read sequence and return a tuple
        containing the t_on and t_off count"""
        if not hasattr(self.registers,'LINE_SENSE_REG'):
            return None
        self.trigger_line_sense()
        self.poll_line_sense()
        return self.get_line_sense_report_us()
    
    @readback_retry
    # Line Sense Functions
    def read_line_sense_count(self)->tuple[int, int]:
        """Do the line sense read sequence and return a tuple
        containing the t_on and t_off count"""
        if not hasattr(self.registers,'LINE_SENSE_REG'):
            return None
        self.trigger_line_sense()
        self.poll_line_sense()
        return self.get_line_sense_report()
    
    def trigger_line_sense(self):
        """Trigger the line sense to start the sample accumulation"""
        if not hasattr(self.registers,'LINE_SENSE_REG'):
            return None
        return self.process_send_i2c_write(reg_addr=self.registers.LINE_SENSE_REG,
                                 i2c_data=1,data_byte_count=1)
    
    @readback_retry
    def read_loop_speed_1_byte(self):
        """Read Loop Speed 1 Byte Value"""
        if not hasattr(self.readback_commands,'READ_LOOP_SPEED_1'):
            return None
        ls1 = self.read_u16(self.readback_commands.READ_LOOP_SPEED_1)
        return f"{ls1:04X}"
    
    @readback_retry
    def read_loop_speed_2_byte(self):
        """Read Loop Speed 2 Byte Value"""
        if not hasattr(self.readback_commands,'READ_LOOP_SPEED_2'):
            return None
        ls2 = self.read_u16(self.readback_commands.READ_LOOP_SPEED_2)
        return f"{ls2:04X}"
    
    def poll_line_sense(self):
        """Poll the line sense to see if the report is ready"""
        if not hasattr(self.readback_commands,'READ_LS_READY'):
            raise Exception("Line sense feature not supported")
        report_ready = False
        count = 0
        while report_ready == False:
            # Get a U16 value by doing a readback from the address
            rb_u16 = self.read_u16(self.readback_commands.READ_LS_READY)
            report_ready = self.controller.poll_line_sense(rb_u16)
            sleep(0.001)

            count += 1
            if count == 20:
                raise Exception("Line sense report is not ready.")

    def get_line_sense_report(self)->tuple[int, int]:
        """Return a tuple containing the t_on and t_off count"""
        # Get a U16 value by doing a readback from the address
        if not hasattr(self.readback_commands,'READ_LINE_SENSE_TON'):
            return None, None
        if not hasattr(self.readback_commands,'READ_LINE_SENSE_TOFF'):
            return None, None
        rb1_u16_ton = self.read_u16(self.readback_commands.READ_LINE_SENSE_TON)

        rb1_u16_toff = self.read_u16(self.readback_commands.READ_LINE_SENSE_TOFF)
        
        return self.controller.get_line_sense_report(rb1_u16_ton,rb1_u16_toff)
    
    def get_line_sense_report_us(self)->tuple[float, float]:
        """Return a tuple containing the t_on and t_off in units of µs"""
        if not hasattr(self.readback_commands,'READ_LINE_SENSE_TON'):
            return None, None
        if not hasattr(self.readback_commands,'READ_LINE_SENSE_TOFF'):
            return None, None
        rb1_u16_ton = self.read_u16(self.readback_commands.READ_LINE_SENSE_TON)

        rb1_u16_toff = self.read_u16(self.readback_commands.READ_LINE_SENSE_TOFF)

        return self.controller.get_line_sense_report_us(rb1_u16_ton,rb1_u16_toff)
    
class PDSinkController(CP2112):
    """ Class for CCG2 Sink Controller device

        The CCG2 sink device is a slave to the SMBUS interface
        We don't know how to change the I2C address of the CCG2 device
        so an I2C multiplexer (TCA9548) is used to address 
        multiple CCG2 units

        TCA9548 Multiplexer has 8 channels that can be selected

        Keyword Arguments:
        
    """
    def __init__(self, *args, **kwargs):
        super().__init__()
        
        # If is_multiport = False, the multiplexer will not be used
    

        # I2C address is 0x08 by default for CCG2 devices
        self.i2c_address=0x10
        
        # PAT tool can be assigned by using add_PDController from the PAT tool object
        
        # Received Source Caps
        self.received_source_caps = []
        # List of available source cap object positions
        self.source_caps_object_position = []
        # List of PPS PDOs
        self.pps_list = []
        # List of EPR and SPR AVS PDOs
        self.epr_avs_list = []
        self.spr_avs_list = []
        # List of EPR capable fixed supply source caps
        self.epr_fs_list = []
        # List of all fixed output supply source caps
        self.fs_list = []
        
        # Previous Source Cap Bytes fro comparison
        self.old_source_caps_bytes = []
        
        # Transmit and Receive bytes
        self._tx_buffer = []
        self._rx_buffer = []
        
        # EPR Capability
        # Will change depending on received source caps
        self.epr_capable = False

        # EPR Mode Flag
        # If enabled, EPR mode is entered
        # PDO must be appended on RDO to successfuly do a request
        self.epr_mode_enabled = False
        # Flag for checking if PPS request thread is running
        self.pps_request_thread_running = False
        
        self.description = f"TST-058 PAT Tool, SN: {self.serial_number}"# : Port {self.port}"
        self.details =  (   f"CP2112 + CYPD2122 based \n"
                            f"I2C Interface and  USB-PD Sink Controller\n"
                            f"VID = {self._vid}\tPID = {self._pid}")
        
        self.status = SINK_STATE.SINK_DISCONNECTED
        
        # USB device 
        self.CC1_status = 0
        self.CC2_status = 0
        self.dfp_state = False
        
        self.get_status(serial_number=self.serial_number)
        
    def usbi2c_transmit(self):
        """ Sends the contents of the _tx_buffer to the I2C device with given address

        Returns:
        None
        
        """
        status = -1
        self.ongoing_transmit = True
        try:
            status =  self.write(write_buffer=self._tx_buffer,device_addr=self.i2c_address)
        except Exception as e:            
            print(e)
        self.ongoing_transmit = False
        return status
        
    
    def usbi2c_receive(self,register_address:int=None,num_bytes:int= None):
        """ Reads the contents of the register of the I2C device with given address

        The response is stored into the _rx_buffer and also returned

        Returns:
        _rx_buffer
        
        """
        self.ongoing_transmit = True
        if register_address is None:
            print('No register addess specified')
            return None
        if num_bytes is None:
            num_bytes = 4
        try:
            self._rx_buffer = self.address_read(slave_address=self.i2c_address,
                                                register_address=register_address,
                                                num_bytes_to_read=num_bytes)
        except Exception as e:
            self.ongoing_transmit = False
            # print(e)
            return None
        
        self.ongoing_transmit = False
        return self._rx_buffer 

    def close(self):
        self.pps_thread_cleanup()
        super().close()
    
    def open(self,serial_num:str=''):
        self.pps_thread_cleanup()
        super().open(serial_num=serial_num)
    
    def get_status(self, serial_number = ''):
        """Return the status of the USBPD sink setup.

        Returns either of the following:
        PAT_TOOL_DISCONNECTED, 
        PAT_TOOL_CONNECTED, 
        USBPD_SOURCE_CONNECTED
        """

        # If a different nonzero serial number is input:
        if (serial_number != self.serial_number) & (serial_number != ''):
            if self.open_status:
                self.close()
            self.serial_number = serial_number
            
        self.ping_sink_controller_device(self.serial_number)
        
        if self.status != SINK_STATE.SINK_DISCONNECTED:
            self.check_pd_supply_connection()
        else:
            self.pd_data_cleanup()
        self.update_device_description()

        return self.status
    
    def update_device_description(self):
        
        self.description = f"TST-058 PAT Tool, SN: {self.serial_number}"# : Port {self.port}"
        self.details =  (   f"CP2112 + CYPD2122 based \n"
                            f"I2C Interface and  USB-PD Sink Controller\n"
                            f"VID = {self._vid}\tPID = {self._pid}")

    def ping_sink_controller_device(self,serial_number:str = '')->bool:
        """Use the GET_BOARD_INFO request to check if the device is connected"""

        # Check if the USB device was not found before
        if (self.status == SINK_STATE.SINK_DISCONNECTED) | (serial_number == ''):
            self.dfp_state = False
            self.find_sink_controller_device()
            # If the device still can't be found, return False
            if self.status == SINK_STATE.SINK_CONNECTED:
                return True
            # If the device was found then return true
            else:
                return False
        
        # If the device was found before, don't use the same routine
        # to avoid crashing due to USBError. Instead, use GET_BOARD_INFO
        # to ping the board
        else:
            try:
                if (self.open_status == False):
                    # print("Opening the device")
                    self.open(self.serial_number)
                    if self.connection_status == SMBUS_STATE.ERROR:
                        raise ConnectionError("PAT tool is detected but cannot be accessed by this program.")
                    elif self.connection_status == SMBUS_STATE.DISCONNECTED:
                        raise ConnectionError(f"PAT Tool with SN {self.serial_number} not detected.")
                    self.GetString()
                    self.open_status = True
                else:
                    self.GetString()
            except Exception as e:
                # print(e)
                self.status = SINK_STATE.SINK_DISCONNECTED
                self.dfp_state = False
                self.open_status = False
                return False
            else:
                return True

    def find_sink_controller_device(self, print_status=False):
        """
        Find the sink controller device using its PID and VID.
        Sets the device_found flag if the usb device is found.

        This method should not be used multiple times to avoid USBError.
        """
        self.open_status = False 
        # Try to define the device if not previously found   
        if self.serial_number != '':
            try:
                # print("Opening the device")
                self.open(self.serial_number)
                if self.connection_status == SMBUS_STATE.ERROR:
                    raise ConnectionError("PAT tool is detected but cannot be accessed by this program.")
                elif self.connection_status == SMBUS_STATE.DISCONNECTED:
                    raise ConnectionError(f"PAT Tool with SN {self.serial_number} not detected.")
                self.open_status = self.IsOpened()
            except Exception as e:
                self.open_status = False
            else:
                print(f"Manufacturer: {self.GetString(HID_SMBUS.MANUFACTURER_STR.value)}")
                print(f"Product: {self.GetString(HID_SMBUS.PRODUCT_STR.value)}")
                print(f"Serial No: {self.GetString(HID_SMBUS.SERIAL_STR.value)}")
        else:
            for d in hid.enumerate(vendor_id=self._vid,product_id=self._pid):
                sn = d['serial_number']
                try:
                    # print("Opening the device")
                    self.open(sn)
                    if self.connection_status == SMBUS_STATE.ERROR:
                        raise ConnectionError("PAT tool is detected but cannot be accessed by this program.")
                    elif self.connection_status == SMBUS_STATE.DISCONNECTED:
                        raise ConnectionError(f"PAT Tool with SN {sn} not detected.")
                    self.open_status = self.IsOpened()
                except Exception as e:
                    self.open_status = False
                else:
                    self.serial_number = sn
                    print(f"Manufacturer: {self.GetString(HID_SMBUS.MANUFACTURER_STR.value)}")
                    print(f"Product: {self.GetString(HID_SMBUS.PRODUCT_STR.value)}")
                    print(f"Serial No: {self.GetString(HID_SMBUS.SERIAL_STR.value)}")
                    break
            
        # If device is still not found
        if self.open_status == False:
            self.status = SINK_STATE.SINK_DISCONNECTED
            if print_status:
                print("SPR sink device not found.")
        
        # If device is already found
        else:
            self.status = SINK_STATE.SINK_CONNECTED
            if print_status:
                print("SPR sink device found.")    

    def check_pd_supply_connection(self, print_status:bool=False):
        # Check USB PD Power Supply connection
        if self.status != SINK_STATE.SINK_DISCONNECTED:
            self.get_usbpd_status()

            if self.status == SINK_STATE.USBPD_SOURCE_CONNECTED:
                if print_status:
                    print("USB PD source detected")
                    try:
                        self.get_dfp_state()
                    except Exception as e:
                        self.status != SINK_STATE.SINK_CONNECTED
            else:
                if print_status:
                    print("No USBPD source detected")
    
    def get_usbpd_status(self
        )->None:
        """ Gets the USB PD status with structure defined below

        []

        Optional Parameter:
        print_source_caps:bool          --          set to true to print source caps
        """
        try:
            return_status = self.get_tc_connected_status()
            if (self.status != SINK_STATE.USBPD_SOURCE_CONNECTED) or (return_status is None):
                self.dfp_state = False
                self.pd_data_cleanup()
                return
            self.get_source_caps()
        except Exception as e:
            # print(e)
            self.status = SINK_STATE.SINK_CONNECTED
            self.dfp_state = False
            self.pd_data_cleanup()
        else:
            self.status = SINK_STATE.USBPD_SOURCE_CONNECTED
            

    def get_source_caps(self):
        """ Get the source capability of the power supply
        
        """
        self.source_caps_bytes = []

        # Get PDO Count
        self.source_cap_count = self.usbi2c_receive(register_address=CY_PD_REG.SRC_PDO_CNT.value,
                                                    num_bytes=1)[0]

        # Read PDOs
        self.source_caps_bytes = []
        for index in range(0, self.source_cap_count):
            source_caps_byte = self.usbi2c_receive(register_address=CY_PD_REG.SRC_PDO.value + 4*index,
                                                    num_bytes=4)
            # If only 3 bytes are received, assume 4th byte is 0x00
            if len(source_caps_byte) == 3:
                source_caps_byte.append(0)
            self.source_caps_bytes.extend(source_caps_byte)
        
        # If no changes from previous source cap
        if self.source_caps_bytes == self.old_source_caps_bytes:
            return
        
        # Else continue update source caps
        
        # Reset the list of received source caps
        self.received_source_caps = []
        self.source_caps_object_position = []
        self.pps_list = []
        self.epr_avs_list = []
        self.spr_avs_list = []
        self.epr_fs_list = []
        self.fs_list = []
            
        self.old_source_caps_bytes = self.source_caps_bytes   
            
        # Process SourceCapabilities bytes
        for obj_pos in range(1, self.source_cap_count+1):

            # Prepare PDO structure buffer
            buffer_PDO = PDO()
            
            # Take 4 bytes for each PDO
            source_cap_bytes = self.source_caps_bytes[obj_pos*4-4:obj_pos*4]
            
            # Combine the 4 bytes into a 32bit variable 
            source_cap_32bit = list_to_uint32(source_cap_bytes)

            # Place the 32bit value from buffer to a PDO structure
            buffer_PDO.asbyte = source_cap_32bit

            if buffer_PDO.asbyte == 0:
                continue

            # Process data depending on PDO type
            match buffer_PDO.bits.supply_type:

                case SUPPLY_TYPE.FIXED:
                    self.process_fixed_pdo_source_cap(obj_pos, buffer_PDO)

                case SUPPLY_TYPE.AUGMENTED:

                    # Process data depending on APDO type
                    match buffer_PDO.bits.apdo_type:
                        case AUGMENTED_TYPE.SPR_PPS:
                            self.process_spr_pps_source_cap(obj_pos, buffer_PDO)

                        case AUGMENTED_TYPE.EPR_AVS:
                            self.process_epr_avs_source_cap(obj_pos, buffer_PDO)
                        
                        case AUGMENTED_TYPE.SPR_AVS:
                            self.process_spr_avs_source_cap(obj_pos, buffer_PDO)
        self.source_cap_count = len(self.received_source_caps)
    
    def pd_data_cleanup(self):
            # Reset the list of received source caps
            self.source_cap_count = 0 
            self.received_source_caps = []
            self.source_caps_object_position = []
            self.pps_list = []
            self.epr_avs_list = []
            self.spr_avs_list = []
            self.epr_fs_list = []
            self.fs_list = []
            self.source_caps_bytes = []
            self.old_source_caps_bytes = []
                                     
    ##################################################################################
    #                       SOURCE CAP PROCESSING FUNCTIONS                          #
    ##################################################################################
    
    def process_fixed_pdo_source_cap(self, obj_pos:int, buffer_PDO:PDO)->None:
        # Prepare FPDOSupply structure buffer
        buffer_FPDOSupply = FPDOSupply()

        # Copy the byte values into the FPDO Structure buffer
        buffer_FPDOSupply.asbyte = buffer_PDO.asbyte

        # Create a Source Cap object for temporary use
        buffer_source_cap = SourceCap()
                    
        # Set the types
        buffer_source_cap.supply_type = SUPPLY_TYPE.FIXED
        buffer_source_cap.epr_mode_capable = buffer_FPDOSupply.bits.epr_mode_capable

        # Set object position
        buffer_source_cap.object_position = obj_pos
                    
        # Set peak current setting
        buffer_source_cap.peak_current = buffer_FPDOSupply.bits.peak_current

        # Supports
        buffer_source_cap.unchunked_ext_msg_support = buffer_FPDOSupply.bits.unchunked_ext_msg_support
        buffer_source_cap.data_role_swap = buffer_FPDOSupply.bits.data_role_swap
        buffer_source_cap.usb_comm_capable = buffer_FPDOSupply.bits.usb_comm_capable
        buffer_source_cap.externally_powered = buffer_FPDOSupply.bits.externally_powered
        buffer_source_cap.usb_suspend_support = buffer_FPDOSupply.bits.usb_suspend_support
        buffer_source_cap.dual_role_power = buffer_FPDOSupply.bits.dual_role_power

        # Set voltage and current
        buffer_source_cap.voltage_mV = buffer_FPDOSupply.bits.voltage_50mV * PD_MULTIPLIER.FPDO_SUPPLY_VOLT_MULTIPLIER
        buffer_source_cap.min_voltage_mV = buffer_source_cap.voltage_mV
        buffer_source_cap.max_voltage_mV = buffer_source_cap.voltage_mV
        buffer_source_cap.max_current_mA = buffer_FPDOSupply.bits.max_current_10mA * PD_MULTIPLIER.FPDO_SUPPLY_MAX_CURRENT_MULTIPLIER
        buffer_source_cap.max_current_high_range_mA = buffer_source_cap.max_current_mA
        buffer_source_cap.max_current_low_range_mA = buffer_source_cap.max_current_mA

        # Power Settings - PD Power - 1 W increments
        buffer_source_cap.pd_power_W = buffer_source_cap.voltage_mV/1000 * buffer_source_cap.max_current_mA/1000
        
        # Text for printing
        if buffer_source_cap.epr_mode_capable:
            buffer_source_cap.pdo_type_text = "EPR FS "
        else:
            buffer_source_cap.pdo_type_text = "SPR FS "

        buffer_source_cap.text = f"PDO {buffer_source_cap.object_position}: {buffer_source_cap.pdo_type_text} {buffer_source_cap.voltage_mV}mV, {buffer_source_cap.max_current_mA} mA"

        # Save the 32bit value
        buffer_source_cap.bytes = uint32_to_list(buffer_FPDOSupply.asbyte)
                    
        # Store the received source cap to the port SinkController object
        self.received_source_caps.append(buffer_source_cap)
        self.source_caps_object_position.append(buffer_source_cap.object_position)

        # If source cap is EPR mode capable, set the SinkController Object's epr capable flag
        # Then add the source cap to the list of EPR capable fixed supplies
        if buffer_source_cap.epr_mode_capable:
            self.epr_capable = True
            self.epr_fs_list.append(buffer_source_cap)
        
        # Add the source cap to the list of fixed source caps
        self.fs_list.append(buffer_source_cap)

    def process_spr_pps_source_cap(self, obj_pos:int, buffer_PDO:PDO)->None:
        # Prepare PPS Object buffer
        buffer_PPS = SPR_PPS_APDO()

        # Copy the byte values into the PPS structure buffer
        buffer_PPS.asbyte = buffer_PDO.asbyte

        # Create a SourceCap object for temporary use
        buffer_source_cap = SourceCap()

        # Set the types
        buffer_source_cap.supply_type = SUPPLY_TYPE.AUGMENTED
        buffer_source_cap.augmented_type = AUGMENTED_TYPE.SPR_PPS
                            
        # Set the object position
        buffer_source_cap.object_position = obj_pos

        # Power limited bit
        buffer_source_cap.pps_power_limited = buffer_PPS.bits.pps_power_limited
                            
        # Voltage and current settings
        buffer_source_cap.max_voltage_mV = buffer_PPS.bits.max_voltage_100mV * PD_MULTIPLIER.APDO_MAX_VOLT_MULTIPLIER
        buffer_source_cap.min_voltage_mV = buffer_PPS.bits.min_voltage_100mV * PD_MULTIPLIER.APDO_MIN_VOLT_MULTIPLIER
        buffer_source_cap.voltage_mV = buffer_source_cap.max_voltage_mV
        buffer_source_cap.max_current_mA = buffer_PPS.bits.max_current_50mA * PD_MULTIPLIER.PPS_MAX_CURRENT_MULTIPLIER
        buffer_source_cap.max_current_high_range_mA = buffer_source_cap.max_current_mA
        buffer_source_cap.max_current_low_range_mA = buffer_source_cap.max_current_mA
        
        # Power Settings - PD Power - 1 W increments
        buffer_source_cap.pd_power_W = buffer_source_cap.voltage_mV/1000 * buffer_source_cap.max_current_mA/1000
        
        # Text for printing
        buffer_source_cap.pdo_type_text = "SPR PPS"
        buffer_source_cap.text = f"PDO {buffer_source_cap.object_position}: {buffer_source_cap.pdo_type_text} {buffer_source_cap.min_voltage_mV}mV to {buffer_source_cap.max_voltage_mV}mV, {buffer_source_cap.max_current_mA} mA"

        # Save the 32bit value
        buffer_source_cap.bytes  = uint32_to_list(buffer_PPS.asbyte)

        # Store the received source cap to the port SinkController object
        self.received_source_caps.append(buffer_source_cap)
        self.pps_list.append(buffer_source_cap)
        self.source_caps_object_position.append(buffer_source_cap.object_position)
    
    def process_epr_avs_source_cap(self, obj_pos:int, buffer_PDO:PDO)->None:
        
        # Prepare EPR AVS object buffer
        buffer_EPR_AVS = EPR_AVS_APDO()

        # Copy the byte values into the PPS structure buffer
        buffer_EPR_AVS.asbyte = buffer_PDO.asbyte

        # Create a SourceCap object for temporary use
        buffer_source_cap = SourceCap()

        # Set the types
        buffer_source_cap.supply_type = SUPPLY_TYPE.AUGMENTED
        buffer_source_cap.augmented_type = AUGMENTED_TYPE.EPR_AVS

        # Set the object position
        buffer_source_cap.object_position = obj_pos

        # # Set peak current setting
        # buffer_source_cap.peak_current = buffer_AVS.bits.peak_current

        # Voltage settings - 100mV increments
        buffer_source_cap.max_voltage_mV = buffer_EPR_AVS.bits.max_voltage_100mV * PD_MULTIPLIER.APDO_MAX_VOLT_MULTIPLIER
        buffer_source_cap.min_voltage_mV = buffer_EPR_AVS.bits.min_voltage_100mV * PD_MULTIPLIER.APDO_MIN_VOLT_MULTIPLIER
        buffer_source_cap.voltage_mV = buffer_source_cap.max_voltage_mV
        buffer_source_cap.max_current_high_range_mA = buffer_source_cap.max_current_mA
        buffer_source_cap.max_current_low_range_mA = buffer_source_cap.max_current_mA
        
        # Power Settings - PD Power - 1 W increments
        buffer_source_cap.pd_power_W = buffer_EPR_AVS.bits.pdp_1W * PD_MULTIPLIER.EPR_AVS_POWER_MULTIPLIER
        buffer_source_cap.max_current_mA = PD_SPECS.USBPD_MAX_REQ_CURRENT_A*1000
        buffer_source_cap.pdo_type_text = "EPR AVS"
        buffer_source_cap.text = f"PDO {buffer_source_cap.object_position}: {buffer_source_cap.pdo_type_text} {buffer_source_cap.min_voltage_mV}mV to {buffer_source_cap.max_voltage_mV}mV, {buffer_source_cap.pd_power_W} W"
        
        # Save the 32bit value
        buffer_source_cap.bytes = uint32_to_list(buffer_EPR_AVS.asbyte)

        # Store the received source cap to the port SinkController object
        self.received_source_caps.append(buffer_source_cap)
        self.epr_avs_list.append(buffer_source_cap)
        self.source_caps_object_position.append(buffer_source_cap.object_position)
        
    def process_spr_avs_source_cap(self, obj_pos:int, buffer_PDO:PDO)->None:
        
        # Prepare SPR AVS object buffer
        buffer_SPR_AVS = SPR_AVS_APDO()

        # Copy the byte values into the PPS structure buffer
        buffer_SPR_AVS.asbyte = buffer_PDO.asbyte

        # Create a SourceCap object for temporary use
        buffer_source_cap = SourceCap()

        # Set the types
        buffer_source_cap.supply_type = SUPPLY_TYPE.AUGMENTED
        buffer_source_cap.augmented_type = AUGMENTED_TYPE.SPR_AVS

        # Set the object position
        buffer_source_cap.object_position = obj_pos

        # # Set peak current setting
        # buffer_source_cap.peak_current = buffer_AVS.bits.peak_current

        # Voltage settings - 100mV increments
        buffer_source_cap.max_current_high_range_mA = buffer_SPR_AVS.bits.max_current_high_range_10mA * PD_MULTIPLIER.SPR_AVS_CURRENT_MULTIPLIER
        buffer_source_cap.max_current_low_range_mA = buffer_SPR_AVS.bits.max_current_low_range_10mA * PD_MULTIPLIER.SPR_AVS_CURRENT_MULTIPLIER
        
        
        buffer_source_cap.pdo_type_text = "SPR AVS"
        buffer_source_cap.min_voltage_mV = PD_SPECS.USBPD_MIN_SPR_AVS_LOW_VOLTAGE_V*1000
        if buffer_source_cap.max_current_high_range_mA == 0:
            buffer_source_cap.max_current_mA = buffer_source_cap.max_current_low_range_mA
            buffer_source_cap.max_voltage_mV = PD_SPECS.USBPD_MAX_SPR_AVS_LOW_VOLTAGE_V
            buffer_source_cap.text = f"PDO {buffer_source_cap.object_position}: {buffer_source_cap.pdo_type_text} {buffer_source_cap.min_voltage_mV}mV to {buffer_source_cap.max_voltage_mV}mV, {buffer_source_cap.max_current_low_range_mA} mA"
        elif buffer_source_cap.max_current_high_range_mA == buffer_source_cap.max_current_low_range_mA:
            buffer_source_cap.max_current_mA = buffer_source_cap.max_current_low_range_mA
            buffer_source_cap.max_voltage_mV = PD_SPECS.USBPD_MAX_SPR_AVS_HIGH_VOLTAGE_V*1000
            buffer_source_cap.text = f"PDO {buffer_source_cap.object_position}: {buffer_source_cap.pdo_type_text} {buffer_source_cap.min_voltage_mV}mV to {buffer_source_cap.max_voltage_mV}mV, {buffer_source_cap.max_current_low_range_mA} mA"
        else:
            buffer_source_cap.max_current_mA = buffer_source_cap.max_current_high_range_mA
            buffer_source_cap.max_voltage_mV = PD_SPECS.USBPD_MAX_SPR_AVS_HIGH_VOLTAGE_V*1000
            buffer_source_cap.text = f"PDO {buffer_source_cap.object_position}: {buffer_source_cap.pdo_type_text} {buffer_source_cap.min_voltage_mV}mV to {PD_SPECS.USBPD_MAX_SPR_AVS_LOW_VOLTAGE_V*1000}mV, {buffer_source_cap.max_current_low_range_mA} mA\n"
            buffer_source_cap.text += f"PDO {buffer_source_cap.object_position}: {buffer_source_cap.pdo_type_text} {PD_SPECS.USBPD_MAX_SPR_AVS_LOW_VOLTAGE_V*1000}mV to {buffer_source_cap.max_voltage_mV}mV, {buffer_source_cap.max_current_high_range_mA} mA"
        
        # Power Settings - PD Power - 1 W increments
        buffer_source_cap.voltage_mV = buffer_source_cap.max_voltage_mV
        buffer_source_cap.pd_power_W = buffer_source_cap.voltage_mV/1000 * buffer_source_cap.max_current_mA/1000
        
        # Save the 32bit value
        buffer_source_cap.bytes = uint32_to_list(buffer_SPR_AVS.asbyte)

        # Store the received source cap to the port SinkController object
        self.received_source_caps.append(buffer_source_cap)
        self.spr_avs_list.append(buffer_source_cap)
        self.source_caps_object_position.append(buffer_source_cap.object_position)
    
        
    def pps_thread_cleanup(self):
        if self.pps_request_thread_running == True:
            self.pps_periodic_request_thread.stop()
            self.pps_request_thread_running = False
            # del self.pps_request_thread

    def usbpd_request(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self:PDSinkController = args[0]
            try:
                # Ensure no PPS request thread is running before doing a request 
                self.pps_thread_cleanup()
                func(*args, **kwargs)
            except Exception as e:
                print(e)
        return wrapper
    
    @usbpd_request
    def fpdo_request(self, iout_max_A:float, vbus_V:float=0,  object_position:int=0,no_usb_suspend:int=0,usb_comm_capable:int=0,cap_mismatch:int=0,give_back:int=0):
        
        # Search for corresponding PDO if object_position is not provided
        if object_position == 0:
            try:
                fs_pdo = self.get_matching_fixed_source_cap(vbus_V, iout_max_A)

            except NoMatchingFixedPDOFoundError:
                raise FixedPDORequestError

            except NotEnoughFPDOMaxCurrentError:
                raise FixedPDORequestError
            
            object_position = fs_pdo.object_position
            
        else:
            source_cap_index = self.source_caps_object_position.index(object_position)
            fs_pdo:SourceCap = self.received_source_caps[source_cap_index]
        rdo_bytes = self.source_cap_to_rdo(source_cap=fs_pdo, iout_max_A=iout_max_A,\
            no_usb_suspend=no_usb_suspend,usb_comm_capable=usb_comm_capable,cap_mismatch=cap_mismatch,give_back=give_back)
        self._tx_buffer = []
        self._tx_buffer.append(CY_PD_REG.CURRENT_RDO.value)
        self._tx_buffer.extend(rdo_bytes)

        print(f"Requested FS PDO {object_position}: {vbus_V} V {iout_max_A} A")
        return self.usbi2c_transmit()
    
    def get_matching_fixed_source_cap(self, vbus_V:float, iout_max_A:float)->SourceCap:
        """
        Tries to get a matching source cap from the list of received source caps
        Raises an error if no matching source cap is found

        Keyword Arguments
        vbus:float              --      bus voltage
        iout_max:float          --      max output current

        Returns
        source_cap:SourceCap    --      matching source cap
        """
        # Loop through all received source caps
        for source_cap in self.received_source_caps:
            if round(vbus_V * 1000) == source_cap.voltage_mV:
                # If matching both voltage and current
                if round(iout_max_A * 1000) <= source_cap.max_current_mA:
                    return source_cap
                # If matching voltage but not enough current
                else:
                    raise NotEnoughFPDOMaxCurrentError
        else:
            raise NoMatchingFixedPDOFoundError


    def source_cap_to_rdo(self,
                        source_cap:SourceCap = None, 
                        vout_V:float = None,
                        iout_max_A:float = None,
                        no_usb_suspend:int = 0,
                        usb_comm_capable:int = 0,
                        cap_mismatch:int = 0,
                        give_back:int = 0
                        ) -> list:
        """ Generate the RDO bytes needed for the request given Vout and Iout

        Parameters:
        source_cap: SourceCap   --      SourceCap object to be processed into RDO
        vout_V:float            --      output voltage set point in Volts
        iout_max_A:float        --      output current limit in Amps
        

        Returns:
        rdo_bytes               --      list of RDO bytes in reverse order
        """                                
        buffer_pdo = source_cap        

        # Look for matching type then convert the PDO to a request data object
        match buffer_pdo.supply_type:
            case SUPPLY_TYPE.FIXED:
                # Prepare buffer RDO object structure
                buffer_fvrdo = FVRDO()
                buffer_fvrdo.asbyte = 0
                
                # EPR Capability
                if self.epr_capable:
                    buffer_fvrdo.bits.epr_mode_capable = 1
                else:
                    buffer_fvrdo.bits.epr_mode_capable = 0
                    
                # buffer_fvrdo.bits.epr_mode_capable = buffer_pdo.epr_mode_capable

                # Output Current
                # buffer_fvrdo.bits.iout_max_10mA = milliamp_to_10mA(buffer_pdo.max_current_mA) & 0x3FF
                buffer_fvrdo.bits.iout_max_10mA = round(iout_max_A / 0.01) & 0x3FF
                buffer_fvrdo.bits.iout_operating_10mA = round(iout_max_A / 0.01) & 0x3FF

                # Position                
                buffer_fvrdo.bits.object_position = buffer_pdo.object_position

                # Supports
                buffer_fvrdo.bits.unchunked_ext_msg_support = buffer_pdo.unchunked_ext_msg_support
                buffer_fvrdo.bits.no_usb_suspend = no_usb_suspend
                buffer_fvrdo.bits.usb_comm_cap = usb_comm_capable
                buffer_fvrdo.bits.cap_mismatch = cap_mismatch
                buffer_fvrdo.bits.give_back = give_back
                
                # Return a reversed list
                rdo_bytes = uint32_to_list_reversed(buffer_fvrdo.asbyte)
                return rdo_bytes

            case SUPPLY_TYPE.AUGMENTED:
                match buffer_pdo.augmented_type:

                    # Programmable Power Supply Mode
                    case AUGMENTED_TYPE.SPR_PPS:
                        # Prepare buffer RDO object structure
                        buffer_ppsrdo = PPSRDO()
                        buffer_ppsrdo.asbyte = 0

                        # EPR Capability
                        if self.epr_capable:
                            buffer_ppsrdo.bits.epr_mode_capable = 1
                        else:
                            buffer_ppsrdo.bits.epr_mode_capable = 0
                            
                        # buffer_ppsrdo.bits.epr_mode_capable = 1

                        # Output Voltage and Current
                        buffer_ppsrdo.bits.operating_current_50mA = \
                                int(iout_max_A * PD_MULTIPLIER.PPS_RDO_CURRENT_MULTIPLIER)
                        buffer_ppsrdo.bits.operating_voltage_20mV = \
                                int(vout_V * PD_MULTIPLIER.PPS_RDO_VOLTAGE_MULTIPLIER)
                        
                        # Object Position
                        buffer_ppsrdo.bits.object_position = buffer_pdo.object_position

                        # Supports
                        buffer_ppsrdo.bits.unchunked_ext_msg_support = buffer_pdo.unchunked_ext_msg_support
                        buffer_ppsrdo.bits.no_usb_suspend = no_usb_suspend
                        buffer_ppsrdo.bits.usb_comm_capable = usb_comm_capable
                        buffer_ppsrdo.bits.capability_mismatch = cap_mismatch
                        
                        rdo_bytes = uint32_to_list_reversed(buffer_ppsrdo.asbyte)
                        return rdo_bytes


                    # EPR Adjustable Voltage Supply
                    case AUGMENTED_TYPE.EPR_AVS:
                        # Prepare buffer RDO object structure
                        buffer_avsrdo = AVSRDO()
                        buffer_avsrdo.asbyte = 0

                        # EPR Capability
                        if self.epr_capable:
                            buffer_avsrdo.bits.epr_mode_capable = 1
                        else:
                            buffer_avsrdo.bits.epr_mode_capable = 0
                            
                        # buffer_avsrdo.bits.epr_mode_capable = buffer_pdo.epr_mode_capable
                        
                        # Output Voltage and Current
                        buffer_avsrdo.bits.operating_current_50mA = \
                                int(iout_max_A * PD_MULTIPLIER.EPR_AVS_RDO_CURRENT_MULTIPLIER) 
                        buffer_avsrdo.bits.output_voltage_25mV = \
                                int(vout_V * PD_MULTIPLIER.EPR_AVS_RDO_VOLTAGE_MULTIPLIER)

                        # Object position
                        buffer_avsrdo.bits.object_position = buffer_pdo.object_position

                        # Supports
                        buffer_avsrdo.bits.unchunked_ext_msg_support = buffer_pdo.unchunked_ext_msg_support
                        buffer_avsrdo.bits.no_usb_suspend = no_usb_suspend
                        buffer_avsrdo.bits.usb_comm_capable = usb_comm_capable
                        buffer_avsrdo.bits.capability_mismatch = cap_mismatch

                        rdo_bytes = uint32_to_list_reversed(buffer_avsrdo.asbyte)
                        return rdo_bytes

                    # EPR Adjustable Voltage Supply
                    case AUGMENTED_TYPE.SPR_AVS:
                        # Prepare buffer RDO object structure
                        buffer_avsrdo = AVSRDO()
                        buffer_avsrdo.asbyte = 0

                        # EPR Capability
                        if self.epr_capable:
                            buffer_avsrdo.bits.epr_mode_capable = 1
                        else:
                            buffer_avsrdo.bits.epr_mode_capable = 0
                            
                        # buffer_avsrdo.bits.epr_mode_capable = buffer_pdo.epr_mode_capable
                        
                        # Output Voltage and Current
                        buffer_avsrdo.bits.operating_current_50mA = \
                                int(iout_max_A * PD_MULTIPLIER.EPR_AVS_RDO_CURRENT_MULTIPLIER) 
                        buffer_avsrdo.bits.output_voltage_25mV = \
                                int(vout_V * PD_MULTIPLIER.EPR_AVS_RDO_VOLTAGE_MULTIPLIER)

                        # Object position
                        buffer_avsrdo.bits.object_position = buffer_pdo.object_position

                        # Supports
                        buffer_avsrdo.bits.unchunked_ext_msg_support = buffer_pdo.unchunked_ext_msg_support
                        buffer_avsrdo.bits.no_usb_suspend = no_usb_suspend
                        buffer_avsrdo.bits.usb_comm_capable = usb_comm_capable
                        buffer_avsrdo.bits.capability_mismatch = cap_mismatch

                        rdo_bytes = uint32_to_list_reversed(buffer_avsrdo.asbyte)
                        return rdo_bytes

    @usbpd_request
    def pps_request(self, vout_V:float, iout_max_A:float = None, object_position:int = 0,no_usb_suspend:int=0,usb_comm_capable:int=0,cap_mismatch:int=0):
        """Send a PPS request

        Keyword arguments:
        vout -- output voltage request in 20mV increments
        iout -- current limit request in 50mA increments
        object_position -- PDO object position
                
        """
        if object_position == 0:
            try:
                pps_pdo, iout_set_A = self.get_matching_pps_source_cap(vout_V=vout_V, iout_max_A=iout_max_A)
            except NoPPSSourceCapFoundError or PPSSourceCapNotSufficientError:
                raise PPSRequestError

        else:
            try:
                source_cap_index = self.source_caps_object_position.index(object_position)
                pps_pdo:SourceCap = self.received_source_caps[source_cap_index]
                pps_pdo, iout_set_A = self.pps_check_capability(pps_pdo=pps_pdo, vout_V=vout_V, iout_max_A=iout_max_A)
                if pps_pdo is None:
                    raise PPSSourceCapNotSufficientError
            except NoPPSSourceCapFoundError or PPSSourceCapNotSufficientError:
                raise PPSRequestError
        rdo_bytes = self.source_cap_to_rdo(source_cap=pps_pdo, vout_V=vout_V, iout_max_A=iout_set_A,\
            no_usb_suspend=no_usb_suspend,usb_comm_capable=usb_comm_capable,cap_mismatch=cap_mismatch)

        # Prepare write buffer
        write_buffer = []

        write_buffer.append(CY_PD_REG.CURRENT_RDO.value)
        write_buffer.extend(rdo_bytes)

        # Store the write buffer in the object so it can be accessed
        # by the periodic request function
        self.pps_write_buffer = write_buffer

        # Write the buffer once in the I2C
        # Let the timed thread do the rest
       
        if self.pps_write() == False:
            print(f"Failed to Request PPS PDO {pps_pdo.object_position}: {vout_V} V {iout_max_A} A")
            return
        # Create a RepeatedTimer object which will run the pps_periodic_write
        # function with interval defined by the PAT_TOOL_SETTINGS
        self.pps_periodic_request_thread = RepeatedTimer(
            interval=PAT_TOOL_SETTINGS.PPS_REQUEST_INTERVAL_SEC,
            function=self.pps_write
        )
        self.pps_request_thread_running = True
        
        print(f"Requested PPS PDO {pps_pdo.object_position}: {vout_V} V {iout_max_A} A")
        
    
    def get_matching_pps_source_cap(self, vout_V:float, iout_max_A:float=0) -> SourceCap:
        """Return a PDO that is appropriate for the request along with the output current set point 
        If output current is not defined, get the maximum current considering the PDO data
        
        Parameters:
        vbus_V:float        -       Requested voltage
        
        Optional Parameters:
        iout_max_A:float    -       Output current set point

        Returns
        pps_pdo:SourceCap   -       Applicable source cap object
        
        Check for AVS Limits
        There are 3 possible configurations for AVS
        1.  15V - 28V
        2.  15V - 36V
        3.  15V - 48V
        """
        pps_pdo_count = len(self.pps_list)

        # If PPS PDO list is empty, raise an error
        if pps_pdo_count == 0:
            raise NoPPSSourceCapFoundError
        
        # If there is a single PPS PDO, 
        elif pps_pdo_count == 1:
            pps_pdo = self.pps_list[0]

            # Check the PDO if it fits the requirement
            pps_pdo, iout_set_A = self.pps_check_capability(pps_pdo, vout_V, iout_max_A)
            
            # If there is a returned PDO, return both the PDO and current
            if pps_pdo is not None:
                return pps_pdo, iout_set_A
            
            # Raise an error if the PDO does not fit the requirement
            else:
                raise PPSSourceCapNotSufficientError
        
        # If there are multiple PPS PDOs, select the first one that fits
        # Raise an error if no pps pdo fits
        else:
            for pps_pdo in self.pps_list:
                # Check the PDO if it fits the requirement
                pps_pdo, iout_set_A = self.pps_check_capability(pps_pdo, vout_V, iout_max_A)
                
                # If there is a returned PDO, return both the PDO and current
                if pps_pdo is not None:
                    return pps_pdo, iout_set_A

            # If the checking loop finishes without returning, no PDO is found
            # Raise an error
            else:
                raise PPSSourceCapNotSufficientError


    def pps_check_capability(self, pps_pdo:SourceCap, vout_V:float, iout_max_A:float):
        """ Check the PPS SourceCap if it fits the given Vout and Iout values

        Parameters:
        pps_pdo:SourceCap       --      PPS Source cap to be checked
        vout_V:float            --      Required Voltage

        Returns:
        pps_pdo                 --      Same PPS SourceCap if it fits
                                --      None if not applicable
        
        iout_max_A              --      If not specified, use the PDO maximum
                                --      If not found, return None
        """
        if pps_pdo.max_voltage_mV >= round(vout_V * 1000) \
            and pps_pdo.max_current_mA >= round(iout_max_A * 1000):
                
            if iout_max_A == 0:
                iout_max_set_A = pps_pdo.max_current_mA/1000
            else:
                iout_max_set_A = iout_max_A

            iout_set_A = iout_max_set_A

            return pps_pdo, iout_set_A

        else:
            return None, None

    def pps_write(self):
        """Periodically request the PPS RDO defined in the pps_write_buffer
        
        This function is to be called with a RepeatedTimer object
        """
        # Send an SMBUS write request to the PD controller
        # with the write_buffer as the message
        self.ongoing_transmit = True
        try:
            self.write(write_buffer=self.pps_write_buffer,
                       device_addr=self.i2c_address)
            self.ongoing_transmit = False
            return True
        except Exception as e:
            self.ongoing_transmit = False
            print(e)
            self.pps_thread_cleanup()
            return False
        
            
    
    ##################################################################################
    #                       AVS REQUEST FUNCTIONS
    ##################################################################################
    
    @usbpd_request
    def spr_avs_request(self, vout_V:float, iout_max_A:float = None,object_position:int=0,no_usb_suspend:int=0,usb_comm_capable:int=0,cap_mismatch:int=0):
        """ Request an AVS with given vout and iout_max.

        If Iout is not specified, set to the maximum the PDP can handle.
        Raise an error if no AVS PDO fits the request

        Parameters: 
        vbus_V:float            --      output voltage
        
        Optional Parameter:
        iout_max_A:float        --      maximum current
        
        """
        
        # Check if there is a matching AVS object
        # Return the avs object along with the current limit
        # Iout is set to maximum if iout_max_A is not specified 
        # If there is none, raise an error
            
        if object_position == 0:
            try:
                spr_avs_pdo, iout_set_A = self.get_matching_spr_avs_source_cap(vout_V, iout_max_A)
            except NoAVSSourceCapFoundError or AVSSourceCapNotSufficientError:
                raise AVSRequestError

        else:
            try:
                source_cap_index = self.source_caps_object_position.index(object_position)
                spr_avs_pdo:SourceCap = self.received_source_caps[source_cap_index]
                spr_avs_pdo, iout_set_A = self.spr_avs_check_capability(spr_avs_pdo=spr_avs_pdo, vout_V=vout_V, iout_max_A=iout_max_A)
                if spr_avs_pdo is None:
                    raise AVSSourceCapNotSufficientError
            except NoAVSSourceCapFoundError or AVSSourceCapNotSufficientError:
                raise AVSRequestError
            
        # Once a valid AVS PDO is chosen, prepare the RDO
        rdo_bytes = self.source_cap_to_rdo(source_cap=spr_avs_pdo, vout_V=vout_V, iout_max_A=iout_set_A,\
            no_usb_suspend=no_usb_suspend,usb_comm_capable=usb_comm_capable,cap_mismatch=cap_mismatch)
        
        self._tx_buffer = []
        self._tx_buffer.append(CY_PD_REG.CURRENT_RDO.value)
        self._tx_buffer.extend(rdo_bytes)

        print(f"Requested SPR AVS PDO {spr_avs_pdo.object_position}: {vout_V} V {iout_set_A} A")
        return self.usbi2c_transmit()
        

    def get_matching_spr_avs_source_cap(self, vout_V:float, iout_max_A:float=0) -> SourceCap:
        """Return a PDO that is appropriate for the request along with the output current set point 
        If output current is not defined, get the maximum current considering the PDP
        Raise an error if a source cap is not found
        
        Parameters:
        vbus_V:float        -       Requested voltage
        
        Optional Parameters:
        iout_max_A:float    -       Output current set point

        Returns
        avs_pdo:SourceCap   -       Applicable source cap object
        iout_set_A:float    -       iout_max_A if defined
                                    computed from PDP and Vout if not defined
        
        Check for AVS Limits
        There are 3 possible configurations for AVS
        1.  15V - 28V
        2.  15V - 36V
        3.  15V - 48V
        """
        spr_avs_pdo_count = len(self.spr_avs_list)

        # If AVS PDO list is empty, raise an error
        if spr_avs_pdo_count == 0:
            raise NoAVSSourceCapFoundError
        
        # If there is a single AVS PDO, 
        elif spr_avs_pdo_count == 1:
            spr_avs_pdo = self.spr_avs_list[0]
            
            # Check the PDO if it fits the requirement
            spr_avs_pdo, iout_set_A = self.spr_avs_check_capability(spr_avs_pdo, vout_V, iout_max_A)
            
            # If there is a returned PDO, return both the PDO and current
            if spr_avs_pdo is not None:
                return spr_avs_pdo, iout_set_A
            
            # Raise an error if the PDO does not fit the requirement
            else:
                raise AVSSourceCapNotSufficientError
        
        # If there are multiple AVS PDOs, 
        else:
            # Loop throught the AVS PDOs and use the first one that fits
            for spr_avs_pdo in self.spr_avs_list:

                # Check the PDO if it fits the requirement
                spr_avs_pdo, iout_set_A = self.spr_avs_check_capability(spr_avs_pdo, vout_V, iout_max_A)
            
            # If the checking loop finishes without returning, no PDO is found
            # Raise an error
            else:
                raise AVSSourceCapNotSufficientError


    def spr_avs_check_capability(self, spr_avs_pdo:SourceCap, 
                             vout_V:float, 
                             iout_max_A:float
                             ):
        """ Check the AVS SourceCap if it fits the given Vout and Iout values

        Parameters:
        avs_pdo:SourceCap       --      AVS Source cap to be checked
        vout_V:float            --      Required Voltage
        iout_max_A:float        --      Required AVS current

        Returns:
        avs_pdo                 --      Same AVS SourceCap if it fits
                                --      None if not applicable
        
        iout_max_A              --      If not specified, use the PDO maximum
                                --      If not found, return None
        """
        
        # Check if the voltage and power of the request is within SourceCap limits
        if spr_avs_pdo.max_voltage_mV >= round(vout_V * 1000):
            if round(iout_max_A * 1000) <= spr_avs_pdo.max_current_mA:
                # If output current is not defined in the inputs, use the maximum that 
                # the AVS source can supply
                if iout_max_A == 0:
                    iout_max_set_A = spr_avs_pdo.pd_power_W / vout_V
                else:
                    iout_max_set_A = iout_max_A
                
                # If the computed limit with power and voltage is more than the maximum
                # USB current, use just the USB limit
                if iout_max_set_A > spr_avs_pdo.max_current_mA/1000:
                    iout_max_set_A = spr_avs_pdo.max_current_mA/1000
                
                # Rename to avoid confusion
                iout_set_A = iout_max_set_A

                return spr_avs_pdo, iout_set_A
            else:
                return None, None            
    
    #EPR AVS request unsupported
    def epr_avs_request(self, vout_V:float, iout_max_A:float = None,object_position:int=0,no_usb_suspend:int=0,usb_comm_capable:int=0,cap_mismatch:int=0):
        print('TST-058 is unable to support EPR requests')
        return
    # Convert the bytes received to a single value and apply Little Endian 
    def list_to_uint32(self, data_list):
        dl = data_list
        return (dl[3]<<24)+(dl[2]<<16)+(dl[1]<<8)+(dl[0])
    
    def epr_entry(self):
        print('TST-058 is unable to support EPR requests')
        return
    
    def epr_exit(self):
        print('TST-058 is unable to support EPR requests')
        return
    
    def epr_get_source_caps(self):
        print('TST-058 is unable to support EPR requests')
        return
    
    ##################################################################################
    #                      USB PD Communication Functions                            #
    ##################################################################################
    
    
    def get_tc_connected_status(self):
        self._rx_buffer = self.usbi2c_receive(register_address=CY_PD_REG.TYPE_C_STATUS.value,
                                                num_bytes=1)
        if self._rx_buffer is None:
            return None
        if (self._rx_buffer[0] & 0x01):
            if (self._rx_buffer[0] & 0x02):
                self.CC2_status = 1
                self.CC1_status = 0
            else:
                self.CC2_status = 0
                self.CC1_status = 1
        else:
            self.CC2_status = 0
            self.CC1_status = 0
            
        if self.CC1_status | self.CC2_status:
            self.status = SINK_STATE.USBPD_SOURCE_CONNECTED
        else:
            self.status = SINK_STATE.SINK_CONNECTED
        return self.status
    
    def get_pd_reg_status(self):
        """Check the CY PD Reg PD Status"""
        self._rx_buffer = self.usbi2c_receive(HPI_V1_REG.PD_STATUS.value,4)
        if self._rx_buffer is None:
            return None
        result = (  (self._rx_buffer[3] << 24  ) |
                    (self._rx_buffer[2] << 16  ) |
                    (self._rx_buffer[1] << 8  ) |
                    (self._rx_buffer[0])  )
        return result
    
    def usb_pd_initialize(self):
        self.close()
        self.pd_sleep_ms(50)
        sleep(0.1)
        self.get_status()
        self.pd_sleep_ms(50)
        sleep(0.1)
        # if self.status == SINK_STATE.USBPD_SOURCE_CONNECTED:
        #     # self.set_dfp_state()
        #     # self.pd_sleep_ms(20)
        #     # # voltage = self.received_source_caps[0].voltage_mV/1000
        #     # current = self.received_source_caps[0].max_current_mA/1000
        #     # self.fpdo_request(iout_max_A=current,vbus_V=voltage,object_position=1)
        #     return True
        # else:
        #     return False
        return self.vdm_initialize()
        
    def vdm_initialize(self):
        try:
            if self.status != SINK_STATE.SINK_DISCONNECTED:
                self.send_set_event_mask()
                self.pd_sleep_ms(20)
            if self.status == SINK_STATE.USBPD_SOURCE_CONNECTED:
                self.set_dfp_state()
                self.pd_sleep_ms(20)
                voltage = self.received_source_caps[0].voltage_mV/1000
                current = self.received_source_caps[0].max_current_mA/1000
                self.fpdo_request(iout_max_A=current,vbus_V=voltage,object_position=1)
                return True
            else:
                return False
        except Exception as e:
            return False

    def send_dr_swap(self)->None:
        """ Send a Data Role Swap Message"""
        status_list = []
        self._tx_buffer = []
        self._tx_buffer.append(CY_PD_REG.PD_CONTROL.value)
        self._tx_buffer.append(PD_COMMAND.SEND_DR_SWAP.value)
        status_list.append(self.usbi2c_transmit())
        self.pd_sleep_ms(10)
        
        status_list.append(self.send_clear_interrupt())
        self.pd_sleep_ms(10)
        status_list.append(self.send_reset_interrupt())
        self.pd_sleep_ms(10)
        status_list.append(self.send_reset_interrupt())
        
        test = HID_SMBUS_S0.COMPLETE
        if all(test == element[0] for element in status_list) \
            and len(status_list)>0:
            status = HID_SMBUS_S0.COMPLETE
        else:
            status = HID_SMBUS_S0.ERROR
            
        try:
            self.get_dfp_state()
        except Exception as e:
            status =  HID_SMBUS_S0.ERROR
        
        return status

    def get_dfp_state(self)->None:
        return_bytes = self.get_pd_reg_status()
        if return_bytes is None:
            self.dfp_state = False
            raise I2CReadBackError('Unsuccessful I2C Readback')
        if ((return_bytes & 0x40) >> 6):
            self.dfp_state = True
        else:
            self.dfp_state = False
    
    def set_dfp_state(self)->None:
        """ Set Sink to Downward Facing Port"""
        try:
            self.get_dfp_state()
            if not self.dfp_state:
                return self.send_dr_swap()
            else:
                return None
        except Exception as e:
            return HID_SMBUS_S0.ERROR
        
    @usbpd_request
    def send_hard_reset(self)->None:
        """ Send Hard Reset Message"""
        self._tx_buffer = []
        self._tx_buffer.append(CY_PD_REG.PD_CONTROL.value)
        self._tx_buffer.append(PD_COMMAND.SEND_HARD_RESET.value)
        status = self.usbi2c_transmit()
        self.dfp_state = False
        return status
        
    def send_uvdm_i2c_write_message_pdc2(self, reg_address:c_ubyte,i2c_data:c_uint16)->None:
        """ Create UVDM PDC2 I2C Write Message and Send"""
        message_buffer = []
        
        reg_address_w_parity = add_odd_parity_1byte(reg_address)
        
        # message_buffer.append(reg_address_w_parity)
        message_buffer.append(UCPD_MESSAGE_TYPE.UCPD_INNO<<5 | USB_PD_PACKET_TYPE.UCPD_CONFIG_PACKET_TYPE)
       
        message_buffer.append(INNO_PRO_PD_VDM_WRITE)
        message_buffer.append(UVDM_VID.VID_LOW_PI)
        message_buffer.append(UVDM_VID.VID_HIGH_PI)

        # message_buffer.append(UVDM_VID.PI_VID_I2C_WR)
        message_buffer.append(reg_address_w_parity)
        
        message_buffer.append(0x00)
        message_buffer.append(0x00)
        message_buffer.append(0x00)

        data_msb, data_lsb = u16_bytes(i2c_data)
        message_buffer.append(data_lsb)
        message_buffer.append(data_msb)

        message_buffer.append(0x00)
        message_buffer.append(0x00)
        return self.send_uvdm_write(message_buffer,len(message_buffer))
        
    def send_uvdm_i2c_read_message_pdc2(self, reg_address:c_ubyte):
        """ Create UVDM PDC2 I2C Read Message Packet and Send"""        
        message_buffer = []
        
        message_buffer.append(UCPD_MESSAGE_TYPE.UCPD_INNO<<5 | USB_PD_PACKET_TYPE.UCPD_CONFIG_PACKET_TYPE)
        # message_buffer.append(reg_address)
        
        message_buffer.append(0x00)
        message_buffer.append(UVDM_VID.VID_LOW_PI)
        message_buffer.append(UVDM_VID.VID_HIGH_PI)


        # message_buffer.append(UVDM_VID.PI_VID_I2C_RD)
        message_buffer.append(reg_address)
        
        message_buffer.append(0x00)
        message_buffer.append(0x00)
        message_buffer.append(0x00)

        status = self.send_uvdm_read(message_buffer,len(message_buffer))
        if status != HID_SMBUS_S0.COMPLETE:
            return status, None
        
        data_lsb = self._rx_buffer[12]
        data_msb = self._rx_buffer[13]
        u16_val = join_8bits(data_msb,data_lsb)
        
        return status, u16_val
    
    def send_uvdm_i2c_write_message_pdc1(self, reg_address:c_ubyte,i2c_data:c_uint16)->None:
        """ Create UVDM PDC1 I2C Write Message and Send"""
        message_buffer = []
        
        reg_address_w_parity = add_odd_parity_1byte(reg_address)
        
        message_buffer.append(reg_address_w_parity)
        # message_buffer.append(UCPD_MESSAGE_TYPE.UCPD_INNO<<5 | USB_PD_PACKET_TYPE.UCPD_CONFIG_PACKET_TYPE)
        
        message_buffer.append(INNO_PRO_PD_VDM_WRITE)
        
        # PI VID low and high byte in PDC1 is reversed
        message_buffer.append(UVDM_VID.VID_HIGH_PI)
        message_buffer.append(UVDM_VID.VID_LOW_PI)

        message_buffer.append(UVDM_VID.PI_VID_I2C_WR)
        # message_buffer.append(reg_address_w_parity)
        
        message_buffer.append(0x00)
        message_buffer.append(0x00)
        message_buffer.append(0x00)

        data_msb, data_lsb = u16_bytes(i2c_data)
        message_buffer.append(data_lsb)
        message_buffer.append(data_msb)

        message_buffer.append(0x00)
        message_buffer.append(0x00)
        return self.send_uvdm_write(message_buffer,len(message_buffer))
    
    def send_uvdm_i2c_read_message_pdc1(self, reg_address:c_ubyte):
        """ Create UVDM PDC1 I2C Read Message Packet and Send"""        
        message_buffer = []
        
        # message_buffer.append(UCPD_MESSAGE_TYPE.UCPD_INNO<<5 | USB_PD_PACKET_TYPE.UCPD_CONFIG_PACKET_TYPE)
        message_buffer.append(reg_address)
        
        message_buffer.append(0x00)
        
        # PI VID low and high byte in PDC1 is reversed
        message_buffer.append(UVDM_VID.VID_HIGH_PI)
        message_buffer.append(UVDM_VID.VID_LOW_PI)


        message_buffer.append(UVDM_VID.PI_VID_I2C_RD)
        # message_buffer.append(reg_address)
        
        message_buffer.append(0x00)
        message_buffer.append(0x00)
        message_buffer.append(0x00)

        status = self.send_uvdm_read(message_buffer,len(message_buffer))
        if status != HID_SMBUS_S0.COMPLETE:
            return status, None
        
        data_lsb = self._rx_buffer[12]
        data_msb = self._rx_buffer[13]
        u16_val = join_8bits(data_msb,data_lsb)
        
        return status, u16_val
    
    def send_uvdm_otp_read_message(self, reg_address:c_uint16):
        """ Create UVDM I2C Read Message Packet and Send"""        
        message_buffer = []
        
        message_buffer.append(reg_address & 0xFF)
        message_buffer.append((reg_address>> 8) & 0xFF)
        message_buffer.append(UVDM_VID.VID_LOW_PI)
        message_buffer.append(UVDM_VID.VID_HIGH_PI)


        message_buffer.append(UVDM_VID.PI_VID_OTP_RD)
        message_buffer.append(0x00)
        message_buffer.append(0x00)
        message_buffer.append(0x00)

        status = self.send_uvdm_read(message_buffer,len(message_buffer))
        if status != HID_SMBUS_S0.COMPLETE:
            return status, None
        
        data = self._rx_buffer[12]
        
        return status, data
        
    def send_uvdm_write(self,message_buffer:list,buffer_size:int):
        """ Send UVDM Write Message"""
        status_list =[]
        self._tx_buffer = []
        try:           
            self._tx_buffer.append(HPI_V1_REG.FWDATA_MEMORY_ADDR.value)
            self._tx_buffer.extend(message_buffer)
            self.usbi2c_transmit()
            
            self.pd_sleep_ms(20)
            
            self._tx_buffer = []
            self._tx_buffer.append(HPI_V1_REG.U_VDM_CTRL_ADDR.value)
            self._tx_buffer.append(0x00)
            self._tx_buffer.append(buffer_size & 0xFF)    
            status_list.append(self.usbi2c_transmit())
            
            status_list.append(self.send_clear_interrupt())

            self.pd_sleep_ms(10)

            status_list.append(self.send_reset_interrupt())

            self.pd_sleep_ms(10)

            status_list.append(self.send_reset_interrupt())

            self.pd_sleep_ms(10)

            status_list.append(self.send_reset_interrupt())
        finally:
            test = HID_SMBUS_S0.COMPLETE
            if all(test == element[0] for element in status_list) \
                and len(status_list)>0:
                status = HID_SMBUS_S0.COMPLETE
            else:
                status = -1
        return status
        
    def send_uvdm_read(self,message_buffer:list,buffer_size:int):
        """ Send UVDM Write Message"""
        status_list =[]
        self._tx_buffer = []
        return_buffer = None
        try:         
            self._tx_buffer.append(HPI_V1_REG.FWDATA_MEMORY_ADDR.value)
            self._tx_buffer.extend(message_buffer)
            status_list.append(self.usbi2c_transmit())
            
            self.pd_sleep_ms(20)
            
            self._tx_buffer = []
            self._tx_buffer.append(HPI_V1_REG.U_VDM_CTRL_ADDR.value)
            self._tx_buffer.append(0x00)
            self._tx_buffer.append(buffer_size & 0xFF)
            status_list.append(self.usbi2c_transmit())
            
            self.pd_sleep_ms(20)
            
            for i in range(2):
                return_buffer = self.usbi2c_receive(register_address=0x80,num_bytes=20)
                status_list.append(self.send_clear_interrupt())
                self.pd_sleep_ms(20)
                status_list.append(self.send_reset_interrupt())
                
            self.pd_sleep_ms(10)

            status_list.append(self.send_reset_interrupt())

            self.pd_sleep_ms(10)

            status_list.append(self.send_reset_interrupt())
                      
        finally:
            test = HID_SMBUS_S0.COMPLETE
            if all(test == element[0] for element in status_list) \
                and (len(status_list)>0) and (return_buffer is not None):
                status = HID_SMBUS_S0.COMPLETE
            else:
                status = -1
        return status
        
    def send_clear_interrupt(self):
        self._tx_buffer = []
        self._tx_buffer.append(0x06)
        self._tx_buffer.append(0x01)
        return self.usbi2c_transmit()
        
    def send_reset_interrupt(self):
        self._tx_buffer = []
        self._tx_buffer.append(0x06)
        self._tx_buffer.append(0xFF)
        return self.usbi2c_transmit()
    
    def send_pd_device_reset(self):
        # Reset Device
        try:
            self._tx_buffer = []
            status_list = []
            self._tx_buffer.append(HPI_V1_REG.RESET_ADDR.value)
            self._tx_buffer.append(0x52)
            self._tx_buffer.append(0x01)
            status_list.append(self.usbi2c_transmit())
            
            self.pd_sleep_ms(100)
            status_list.append(self.send_clear_interrupt())
            self.pd_sleep_ms(2000)
            status_list.append(self.send_set_event_mask())
        finally:
            test = HID_SMBUS_S0.COMPLETE
            if all(test == element[0] for element in status_list) \
                and len(status_list)>0:
                status = HID_SMBUS_S0.COMPLETE
            else:
                status = -1
        return status 
            
    def send_set_event_mask(self):
        # Set Event Mask
        try:
            self._tx_buffer = []
            status_list = []
            self._tx_buffer.append(HPI_V1_REG.EVENT_MASK.value)
            self._tx_buffer.append(0xFF)
            self._tx_buffer.append(0xFF)
            self._tx_buffer.append(0xFF)
            self._tx_buffer.append(0xFF)
        
            status_list.append(self.usbi2c_transmit())
            self.pd_sleep_ms(100)
            status_list.append(self.send_clear_interrupt())
        finally:
            test = HID_SMBUS_S0.COMPLETE
            if all(test == element[0] for element in status_list) \
                and len(status_list)>0:
                status = HID_SMBUS_S0.COMPLETE
            else:
                status = -1
        return status      
        
    def pd_sleep_ms(self, ms_sleep:int):
        QThread.msleep(ms_sleep)

import time
from threading import Event, Thread

class RepeatedTimer:

    """Repeat `function` every `interval` seconds."""

    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start = time.time()
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.start()

    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)

    @property
    def _time(self):
        return self.interval - ((time.time() - self.start) % self.interval)

    def stop(self):
        self.event.set()
        self.thread.join()

