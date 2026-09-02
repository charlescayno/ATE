
from numpy import source
import usb.core
import usb.util
import libusb_package

from time import sleep

from PySide2.QtCore import (QObject, QThread, Signal, Slot, QTimer)

from pd import protocol
from pd.pd_types import *


from sink_controllers.exceptions import *
from sink_controllers.misc_functions import *
from sink_controllers.definitions import *
from functools import wraps

import debugpy

class Comms:
    UNLOCK = 0
    LOCK = 1
    
class DEVICE_INFO:
    VID = 0x2D76
    PID = 0x0200
    MFG = 'SiliConch Systems'
    PROD = 'USB-C PD Sink EPR Board'
    REPORT_ID = 0

class STM32SinkController(QObject):
    """ Class for STM32 EPR Sink Controller device
    """
    
    # Signal for pps request thread
    comms_channel_lock_response = Signal(Comms)
    stop_pps_thread = Signal()

    def __init__(self):
        super().__init__()
        # Device identifier
        self._vid = DEVICE_INFO.VID
        self._pid = DEVICE_INFO.PID
        self.serial_number = ''

        # Bulk transfer interface endpoint addresses
        self._bulk_in_address = 0x81
        self._bulk_out_address = 0x01

        # USB device 
        self._usb_device = None
        self.CC1_status = 0
        self.CC2_status = 0

        # TX and RX buffers
        self._rx_buffer = []
        self._tx_buffer = []

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

        # EPR Capability
        # Will change depending on received source caps
        self.epr_capable = False

        # EPR Mode Flag
        # If enabled, EPR mode is entered
        # PDO must be appended on RDO to successfuly do a request
        self.epr_mode_enabled = False

        self.status = SINK_STATE.SINK_DISCONNECTED
        self.open_status = False
        
        # Try to find if USB device with same
        # identifiers specified is connected
        self.get_status()

        # PPS Thread related
        self.pps_request_thread = None
        self.comms_channel_lock = Comms.UNLOCK
        self.comms_lock_counter = 0
        self.ongoing_transmit = False

        # Description for UI display
        # TODO: For I2C multiplexed ports, use the port number as identifier
        # Add the I2C multiplexer channel number to the status update option
        self.port = 1
        self.update_device_description()


    ##################################################################################
    #                      USB CDC COMMUNICATION FUNCTIONS
    ##################################################################################
    def update_device_description(self):
        
        self.description = f"USB-C PD Sink EPR Board, SN: {self.serial_number}"
        self.details =  "STM32 based USB-PD Sink Controller\n" +\
                        "Connected through USB-CDC\t" +\
                        f"VID = {self._vid}\tPID = {self._pid}"
    
    def show_usb_device_details(self):
        """
        Show the details of the usb device
        including its interfaces and configurations
        """
        print(self._usb_device)

    @Slot(Comms)
    def comms_channel_lock_request(self, request):
        # TODO: Simplify logic
        match request:
            case Comms.UNLOCK: 
                # Request to remove lock
                self.comms_lock_counter = 0
                self.comms_channel_lock = Comms.UNLOCK
                self.comms_channel_lock_response.emit(Comms.UNLOCK)
            case Comms.LOCK: 
                # Request to lock channel to a thread if it is currently unlocked
                if self.comms_channel_lock == Comms.UNLOCK:
                    self.comms_channel_lock = Comms.LOCK
                    self.comms_channel_lock_response.emit(Comms.LOCK)

                # If it is currently locked, it means that another process is using
                # the communications channel.
                # If the comms channel has been locked for 10 consecutive requests,
                # the thread that has locked it has probably been destroyed
                # If then, remove the lock of the comms channel
                self.comms_lock_counter += 1
                if self.comms_lock_counter == 10:
                    self.comms_channel_lock = Comms.UNLOCK


    def usbcdc_transmit(self, priority=True):
        """ Sends the contents of the _tx_buffer to the USB device

        The response is stored into the _rx_buffer and also returned

        Returns:
        _rx_buffer      --      Response of the sink board for the transmitted message
        
        """
        self.ongoing_transmit = True
        send_buffer =[]        
        # for i in range (0,4):
        # Transmit the contents of the tx buffer to the USB device
        # bulk out addresss
        send_buffer.extend(self._tx_buffer)
        
        # Add trailing zeros to complete 65 bytes
        #send_buffer.extend([0]*(MAX_TX_BUFFER_SIZE-len(send_buffer)))
        try:
            return_byte = self._usb_device.write(
            self._bulk_out_address, 
            bytes(send_buffer), 
            500)
        except Exception as e:
            self.ongoing_transmit = False
            print(e)
            self.usbcdc_receive()
            return None
        
        if return_byte != (len(send_buffer)):
            print('Incorrect number of data bytes sent')
            self.usbcdc_receive()   
            return None 

        # Always get a response to flush the RX buffer contents
        # Succeeding messages cannot be received without flushing it by reading
        self.usbcdc_receive()
        return self._rx_buffer
           
    def usbcdc_receive(self):
        try: 
            self._rx_buffer = list(self._usb_device.read(
                self._bulk_in_address,
                MAX_RX_BUFFER_SIZE,
                500
            ))
        except Exception as e:
            self.ongoing_transmit = False
            print(e)
            return None
        else:
            # sleep(0.15)
            self.ongoing_transmit = False
            return self._rx_buffer

    ##################################################################################
    #                       USB PD SINK STATUS FUNCTIONS
    ##################################################################################
    def close(self):
        """Close the USB CDC device"""
        # Needs updating
        self.open_status = False
        if self._usb_device is not None:
            self._usb_device.reset()
    
    def get_status(self, serial_number = ''):
        """Return the status of the USBPD sink setup.

        Returns either of the following:
        PAT_TOOL_DISCONNECTED, 
        PAT_TOOL_CONNECTED, 
        USBPD_SOURCE_CONNECTED
        """

        self.epr_mode_enabled = False
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
    
    def ping_sink_controller_device(self,serial_number:str = '')->bool:
        """Use the GET_BOARD_INFO request to check if the device is connected"""

        # Check if the USB device was not found before
        if (self.status == SINK_STATE.SINK_DISCONNECTED) | (serial_number == ''):
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
                    self.open_status = True
                    self._tx_buffer = [USBPD_REQUEST_ID.GET_BOARD_INFO]
                    self.usbcdc_transmit()
                else:
                    self._tx_buffer = [USBPD_REQUEST_ID.GET_BOARD_INFO]
                    self.usbcdc_transmit()
                    # print(f'Checking status of {self._usb_device.get_serial_number_string()}')
            except Exception as e:
                self._usb_device = None
                # print(e)
                self.status = SINK_STATE.SINK_DISCONNECTED
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
        
        if self._usb_device is not None:
            del self._usb_device
         
        # Try to define the device if not previously found   
        if self.serial_number != '':
            self._usb_device = libusb_package.find(idVendor = self._vid, 
                                              idProduct = self._pid,
											  iSerialNumber=self.serial_number)
            try:
                self.open_status = True
                self._usb_device.set_configuration()
            except Exception as e:
                self._usb_device = None
                # print(e)
            else:
                print(f"Manufacturer: {self._usb_device.manufacturer}")
                print(f"Product: {self._usb_device.product}")
                print(f"Serial No: {self._usb_device.serial_number}")
        else:
            for device in libusb_package.find(find_all = True, idVendor = self._vid, idProduct = self._pid):
                sn = device.serial_number
                self._usb_device = device
                try:
                    self.open_status = True
                    self._usb_device.set_configuration()
                except Exception as e:
                    self._usb_device = None
                    # print(e)
                        
                else:
                    self.serial_number = sn
                    print(f"Manufacturer: {self._usb_device.manufacturer}")
                    print(f"Product: {self._usb_device.product}")
                    print(f"Serial No: {self._usb_device.serial_number}")
                    break
            
        # If device is still not found
        if self._usb_device is None:
            self.status = SINK_STATE.SINK_DISCONNECTED
            if print_status:
                print("EPR sink device not found")
        
        # If device is already found
        else:
            self.status = SINK_STATE.SINK_CONNECTED
            if print_status:
                print("EPR sink device found.")    

    def check_pd_supply_connection(self, print_status:bool=False):
        # Check USB PD Power Supply connection
        if self.status != SINK_STATE.SINK_DISCONNECTED:
            self.get_usbpd_status()

            if self.status == SINK_STATE.USBPD_SOURCE_CONNECTED:
                if print_status:
                    print("USB PD source detected")
            else:
                if print_status:
                    print("No USBPD source detected")
    
    def get_usbpd_status(self, 
        print_source_caps:bool = False,
        print_vbus:bool = False,
        update_source_caps = True
        )->None:
        """ Gets the USB PD status with structure defined below

        []

        Optional Parameter:
        print_source_caps:bool          --          set to true to print source caps
        """    
        # Request a USB PD Status update from the sink
        self._tx_buffer = [USBPD_REQUEST_ID.USB_PD_STATUS]
        transmit_status = self.usbcdc_transmit()
        
        
        # If transmit failed
        if transmit_status is None:
            self.pd_data_cleanup()
            self.source_cap_count = 0
            self.policy_state = 'Unknown'
            self.bus_voltage_V = 0
            self.sink_request_bytes = []
            self.bc_level = 0
            return
        
        # Get the values from the RX buffer
        self.policy_state = protocol.policy_states.get(self._rx_buffer[1],f'UnknownKey{self._rx_buffer[1]}')
        self.bc_level = self._rx_buffer[2]
        self.bus_voltage_V = (self._rx_buffer[3] + (self._rx_buffer[4]<<8)) * EPR_SINK_HARDWARE.VOUT_DIV * EPR_SINK_HARDWARE.ADC_RES
        self.sink_request_bytes = self._rx_buffer[5:9]
        
        # Get status if Type-C Cable is connected
        self.get_tc_connected_status()
        if self.status != SINK_STATE.USBPD_SOURCE_CONNECTED:
            self.pd_data_cleanup()
            return
            
        self.source_cap_count = self._rx_buffer[9]
        
        # Limit max number of PDOS
        if self.source_cap_count > PD_SPECS.USBPD_EPR_MAX_OBJECT_POSITION:
            self.source_cap_count = PD_SPECS.USBPD_EPR_MAX_OBJECT_POSITION
        
        # Check if EPR Mode Enabled
        if self.source_cap_count > PD_SPECS.USBPD_SPR_MAX_OBJECT_POSITION:
            self.epr_mode_enabled = True
            self.epr_capable = True
        else:
            self.epr_mode_enabled = False
        
        self.source_caps_bytes = self._rx_buffer[10:]
        self.source_caps_bytes = self.source_caps_bytes[0:(self.source_cap_count+1)*4]
        
        if print_source_caps:
            self.print_source_caps()

        if print_vbus:
            self.print_vbus()
        
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
        self.epr_capable = False
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
                                     
    def get_tc_connected_status(self):
        self.CC1_status = self._rx_buffer[2] & 0xFF
        self.CC2_status = self._rx_buffer[2] >> 4
        
        if self.CC1_status | self.CC2_status:
            self.status = SINK_STATE.USBPD_SOURCE_CONNECTED
        else:
            self.status = SINK_STATE.SINK_CONNECTED
        return self.status

    def print_source_caps(self):
        if self.source_cap_count == 0:
            print("No received caps")
        else:
            print("Source Capabilities")
            for pdo in self.received_source_caps:
                print(pdo)
    
    def print_vbus(self):
        print(f"Bus Voltage: {round(self.bus_voltage_V,3)}")
        
    def usb_pd_initialize(self):
        self.close()
        self.pd_sleep_ms(50)
        sleep(0.1)
        self.get_status(serial_number=self.serial_number)
        self.pd_sleep_ms(50)
        sleep(0.1)
        if self.status == SINK_STATE.USBPD_SOURCE_CONNECTED:
            self.send_dr_swap()
            sleep(0.1)
            return True
        else:
            return False

    ##################################################################################
    #                       SOURCE CAP PROCESSING FUNCTIONS
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
        

    ##################################################################################
    #                       FIXED PDO REQUEST FUNCTIONS
    ##################################################################################
    
    def pps_thread_cleanup(self):
        
        if self.pps_request_thread is not None:
            self.stop_pps_thread.emit()
            self.pps_worker.stop_thread()
            self.delete_pps_request_thread()
            print('PPS Thread stopped')
            # del self.pps_request_thread

    def usbpd_request(func):
        def wrapper(self, *args, **kwargs):
            # Ensure no PPS request thread is running before doing a request 
            self.pps_thread_cleanup()
            func(self, *args, **kwargs)
        return wrapper

    @usbpd_request
    def fpdo_request(self, iout_max_A:float, vbus_V:float=0,  object_position:int=0,no_usb_suspend:int=0,usb_comm_capable:int=0,cap_mismatch:int=0,give_back:int=0):
        """
        Request a fixed pdo.

        If the object position is not specified, the source caps received
        are checked to see if an applicable source cap can be used.

        Parameters:
            vbus: float
                --  output voltage in Volts
            iout_max: float
                --  ouput current limit in Amps
        
        Optional argument:
            object_position: int, optional

        Returns:
        0 - PDO request successful
        1 - Mismatched RDO from received PDOs
        2 - No VBUS equivalent found
        3 - Requested Iout is too high
        """
        # If request voltage is for EPR, check EPR mode and if it is not yet enabled,
        # Enable it first
        if vbus_V > PD_SPECS.USBPD_MAX_SPR_FIXED_VOLTAGE_V and not self.epr_mode_enabled:
            self.epr_entry()

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
        self._tx_buffer.append(USBPD_REQUEST_ID.USBPD_RDO_REQUEST)
        self._tx_buffer.extend(rdo_bytes)
             
        if self.epr_mode_enabled:
            tx_pdo_bytes = reversed(fs_pdo.bytes)
            self._tx_buffer.extend(tx_pdo_bytes)
        
        self.usbcdc_transmit()

        print(f"Requested FS PDO {object_position}: {vbus_V} V {iout_max_A} A")

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

    
    ##################################################################################
    #                       PPS REQUEST FUNCTIONS
    ##################################################################################

    @usbpd_request
    def pps_request(self, vout_V:float, iout_max_A:float = None, object_position:int = 0,no_usb_suspend:int=0,usb_comm_capable:int=0,cap_mismatch:int=0):
        """ Request a PPS with given vout and iout_max.

        If Iout is not specified, set to the maximum the PPS APDO can handle.
        Raise an error if no PPS PDO fits the request

        Parameters: 
        vbus_V:float            --      output voltage
        
        Optional Parameter:
        iout_max_A:float        --      maximum current
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
        
        pps_message = []
        self._tx_buffer = []
        
        pps_message.append(USBPD_REQUEST_ID.USBPD_RDO_REQUEST)
        pps_message.extend(rdo_bytes)
        
        if self.epr_mode_enabled:
            tx_pdo_bytes = reversed(pps_pdo.bytes)
            pps_message.extend(tx_pdo_bytes)
            
        self._tx_buffer = pps_message
        
        # The transmission is handled by a separate thread to let it run on the background
        # Set up the worker and thread
        self.pps_request_thread = QThread()
        self.pps_worker = PPSRequestWorker(
            self._usb_device, self._bulk_out_address,
            self._bulk_in_address, pps_message,self.ongoing_transmit)
        self.pps_worker.moveToThread(self.pps_request_thread)

        # Connect the necessary signals and slots
        self.pps_request_thread.started.connect(self.pps_worker.run)
        # self.pps_request_thread.finished.connect(self.pps_request_thread.deleteLater)
        # self.pps_request_thread.finished.connect(self.delete_pps_request_thread)
        
        # self.pps_worker.finish_sequence.connect(self.delete_pps_request_thread)
        # self.pps_worker.finished.connect(self.pps_request_thread.deleteLater)
        self.pps_worker.comms_channel_lock_request.connect(self.comms_channel_lock_request)
        
        # Main Thread Signals
        self.comms_channel_lock_response.connect(self.pps_worker.comms_channel_lock_response)
        self.stop_pps_thread.connect(self.pps_worker.stop_request_timer)
        self.pps_request_thread.start()

        # Connect the defined signals and slots


        # self.usbcdc_transmit()
        
        print(f"Requested PPS PDO {pps_pdo.object_position}: {vout_V} V {iout_max_A} A")     
        
    def delete_pps_request_thread(self):
        self.pps_request_thread.quit()
        sleep(0.1)
        self.pps_request_thread.deleteLater()
        sleep(0.1)
        self.pps_worker = None
        self.pps_request_thread = None
            
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
        self._tx_buffer.append(USBPD_REQUEST_ID.USBPD_RDO_REQUEST)
        self._tx_buffer.extend(rdo_bytes)
        
        if self.epr_mode_enabled:
            tx_pdo_bytes = reversed(spr_avs_pdo.bytes)
            self._tx_buffer.extend(tx_pdo_bytes)

        self.usbcdc_transmit()


        print(f"Requested SPR AVS PDO {spr_avs_pdo.object_position}: {vout_V} V {iout_set_A} A")
        

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
    
    
    @usbpd_request
    def epr_avs_request(self, vout_V:float, iout_max_A:float = None,object_position:int=0,no_usb_suspend:int=0,usb_comm_capable:int=0,cap_mismatch:int=0):
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
        
        if not self.epr_mode_enabled:
            self.epr_entry()
            
        if object_position == 0:
            try:
                epr_avs_pdo, iout_set_A = self.get_matching_epr_avs_source_cap(vout_V, iout_max_A)
            except NoAVSSourceCapFoundError or AVSSourceCapNotSufficientError:
                raise AVSRequestError

        else:
            try:
                source_cap_index = self.source_caps_object_position.index(object_position)
                epr_avs_pdo:SourceCap = self.received_source_caps[source_cap_index]
                epr_avs_pdo, iout_set_A = self.epr_avs_check_capability(epr_avs_pdo=epr_avs_pdo, vout_V=vout_V, iout_max_A=iout_max_A)
                if epr_avs_pdo is None:
                    raise AVSSourceCapNotSufficientError
            except NoAVSSourceCapFoundError or AVSSourceCapNotSufficientError:
                raise AVSRequestError
            
        # Once a valid AVS PDO is chosen, prepare the RDO
        rdo_bytes = self.source_cap_to_rdo(source_cap=epr_avs_pdo, vout_V=vout_V, iout_max_A=iout_set_A,\
            no_usb_suspend=no_usb_suspend,usb_comm_capable=usb_comm_capable,cap_mismatch=cap_mismatch)
        
        self._tx_buffer = []
        self._tx_buffer.append(USBPD_REQUEST_ID.USBPD_RDO_REQUEST)
        self._tx_buffer.extend(rdo_bytes)
        
        if self.epr_mode_enabled:
            tx_pdo_bytes = reversed(epr_avs_pdo.bytes)
            self._tx_buffer.extend(tx_pdo_bytes)


        self.usbcdc_transmit()


        print(f"Requested EPR AVS PDO {epr_avs_pdo.object_position}: {vout_V} V {iout_set_A} A")
        

    def get_matching_epr_avs_source_cap(self, vout_V:float, iout_max_A:float=0) -> SourceCap:
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
        epr_avs_pdo_count = len(self.epr_avs_list)

        # If AVS PDO list is empty, raise an error
        if epr_avs_pdo_count == 0:
            raise NoAVSSourceCapFoundError
        
        # If there is a single AVS PDO, 
        elif epr_avs_pdo_count == 1:
            epr_avs_pdo = self.epr_avs_list[0]
            
            # Check the PDO if it fits the requirement
            epr_avs_pdo, iout_set_A = self.epr_avs_check_capability(epr_avs_pdo, vout_V, iout_max_A)
            
            # If there is a returned PDO, return both the PDO and current
            if epr_avs_pdo is not None:
                return epr_avs_pdo, iout_set_A
            
            # Raise an error if the PDO does not fit the requirement
            else:
                raise AVSSourceCapNotSufficientError
        
        # If there are multiple AVS PDOs, 
        else:
            # Loop throught the AVS PDOs and use the first one that fits
            for epr_avs_pdo in self.epr_avs_list:

                # Check the PDO if it fits the requirement
                epr_avs_pdo, iout_set_A = self.epr_avs_check_capability(epr_avs_pdo, vout_V, iout_max_A)
            
            # If the checking loop finishes without returning, no PDO is found
            # Raise an error
            else:
                raise AVSSourceCapNotSufficientError


    def epr_avs_check_capability(self, epr_avs_pdo:SourceCap, 
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
        
        # Get the total power of the request
        request_power_W = vout_V * iout_max_A
        
        # If EPR AVS
        if epr_avs_pdo.object_position > PD_SPECS.USBPD_SPR_MAX_OBJECT_POSITION:
            # Check if the voltage and power of the request is within SourceCap limits
            if epr_avs_pdo.max_voltage_mV >= round(vout_V * 1000) \
                and epr_avs_pdo.pd_power_W >= request_power_W:
                
                # If output current is not defined in the inputs, use the maximum that 
                # the AVS source can supply
                if iout_max_A == 0:
                    iout_max_set_A = epr_avs_pdo.pd_power_W / vout_V
                else:
                    iout_max_set_A = iout_max_A
                
                # If the computed limit with power and voltage is more than the maximum
                # USB current, use just the USB limit
                if iout_max_set_A > epr_avs_pdo.max_current_mA/1000:
                    iout_max_set_A = epr_avs_pdo.max_current_mA/1000
                
                # Rename to avoid confusion
                iout_set_A = iout_max_set_A

                return epr_avs_pdo, iout_set_A
            else:
                return None, None            


    ##################################################################################
    #                       EPR MODE FUNCTIONS
    ##################################################################################
    @usbpd_request
    def epr_entry(self, retries:int = 1)->None:
        """ Request entry to EPR Mode
        """

        # Do not proceed if the USBPD did not advertise EPR capability
        if not self.epr_capable:
            return

        # Send the code for EPR test case
        self._tx_buffer = []
        self._tx_buffer.append(USBPD_REQUEST_ID.USBPD_EPR_TEST_CASE)
        # EPR entry should be bit 2, but in this hardware it is 1
        # self._tx_buffer.append(EPR_TEST_CASE.TC_EPR_ENTRY)
        self._tx_buffer.append(1)
        self._tx_buffer.append(0xF0)
        self.usbcdc_transmit()
        print('Enter EPR mode')
        sleep(1.5)
        self.get_usbpd_status()
        sleep(0.1)
        


    @usbpd_request
    def epr_exit(self)->None:
        """ Request EPR Mode Exit
        """
        # Send the code for EPR test case
        self._tx_buffer = []
        self._tx_buffer.append(USBPD_REQUEST_ID.USBPD_EPR_TEST_CASE)
        # EPR exit should be bit 3, but in this hardware it is 2
        # self._tx_buffer.append(EPR_TEST_CASE.TC_EPR_EXIT)
        self._tx_buffer.append(2)
        self.usbcdc_transmit()
        print('Exit EPR mode')
        sleep(1.5)
        self.get_usbpd_status()
        sleep(0.1)

    def request_epr_capable_pdo(self):
        
        epr_source_cap = self.epr_fs_list[0]
        self.fpdo_request(  object_position=epr_source_cap.object_position, 
                            iout_max_A=epr_source_cap.max_current_mA/1000)

    @usbpd_request
    def epr_get_source_caps(self)->None:
        """ Request an EPR source cap update

        """
        # Send the code for EPR test case and EPR source cap
        self._tx_buffer = []
        self._tx_buffer.append(USBPD_REQUEST_ID.USBPD_EPR_TEST_CASE)
        self._tx_buffer.append(EPR_TEST_CASE.TC_EPR_GET_SOURCE_CAP)
        self.usbcdc_transmit()
        # Call get_usbpd_status to update the source caps list

    def get_source_caps(self)->None:
        """ Request a source cap update

        If EPR mode is enabled, try to get EPR source caps
        """        
        if self.epr_capable:
            self.epr_get_source_caps()
        self.get_usbpd_status()
        
    def send_dr_swap(self)->None:
        """ Send a Data Role Swap Message"""
        self._tx_buffer = []
        self._tx_buffer.append(USBPD_REQUEST_ID.USBPD_DATA_ROLE_SWAP_ID)
        self.usbcdc_transmit()
        
    @usbpd_request
    def send_hard_reset(self)->None:
        """ Send Hard Reset Message"""
        self._tx_buffer = []
        self._tx_buffer.append(USBPD_REQUEST_ID.USBPD_HID_TEST_REQUEST_ID)
        self._tx_buffer.append(EPR_TEST_CASE.TC_EPR_SEND_HARD_RESET)
        self.usbcdc_transmit()
        
    def pd_sleep_ms(self, ms_sleep:int):
        QThread.msleep(ms_sleep)

class PPSRequestWorker(QObject):
    """Runs the PPS requests periodically in the background."""

    comms_channel_lock_request = Signal(Comms)
    finish_sequence = Signal()
    
    @Slot(Comms)
    def comms_channel_lock_response(self, response):
        match response:
            # Sink is still using the channel
            case Comms.UNLOCK:
                # print("Responded unlock")
                self.comms_lock = Comms.UNLOCK

            # Sink allowed this thread to use the comms channel
            case Comms.LOCK:
                # print("Responded lock")
                self.comms_lock = Comms.LOCK

    def __init__(self, _usb_device, _bulk_out_address, _bulk_in_address, tx_buffer,ongoing_transmit):
        super().__init__()
        print("Initialized new pps thread")
        self.comms_lock = Comms.UNLOCK
        self._usb_device= _usb_device 
        self._bulk_out_address = _bulk_out_address
        self._bulk_in_address = _bulk_in_address
        self._tx_buffer = tx_buffer
        self.ongoing_transmit = ongoing_transmit
        self.pps_request_timer:QTimer = None
       
        
    def stop_request_timer(self):
        self.pps_request_timer.stop()
        
    def run(self):
        print("New PPS Run")

    #    if self.parent.run_settings['debug']: 
        debugpy.debug_this_thread()


        # Setup a timer that will send the request
        self.pps_request_timer = QTimer()
        
        # self.pps_request_timer.moveToThread(self.thread)
        self.pps_request_timer.timeout.connect(self.pps_update_service)
        self.pps_request_timer.start(30)
        print("Started PPS Timer")

    def pps_update_service(self):
        # TODO: Need to modify usbcdc_transmit to have flow control to avoid collision
        # Use signals to do so
        # TODO: Error after turning off ac source after requesting PPS
        match self.comms_lock:
            case Comms.UNLOCK:
                # print("Channel is unlocked. Request main thread to lock")
                # Send a request to the main thread 
                # to let this thread control the comms channel
                self.comms_channel_lock_request.emit(Comms.LOCK)
                # print("Emitted signal to request lock.")
                # Change interval to 15ms to wait for response 
                self.pps_request_timer.setInterval(15)
                # print("Modified request interval (15)")

            # Communication from this thread is allowed       
            case Comms.LOCK:
                # print("Channel is ready.")             
                # Change the interval to 2s
                self.pps_request_timer.setInterval(8000)
                # Send the request
                # print("Request interval changed")
                self.usbcdc_transmit()
                # print(f"Transmitted {self._tx_buffer}")
                # Emit an unlock request to let the main thread have control
                # over the communication channel
                self.comms_channel_lock_request.emit(Comms.UNLOCK)
                # print("Requested main thread to release lock.")
        
    @Slot()
    def stop_thread(self):
        # Request unlock channel
        self.comms_channel_lock_request.emit(Comms.UNLOCK)
        sleep(0.1)        

        
    def usbcdc_transmit(self):
        """ Sends the contents of the _tx_buffer to the USB device

        The response is stored into the _rx_buffer and also returned

        Returns:
        _rx_buffer      --      Response of the sink board for the transmitted message
        
        """
        self.ongoing_transmit = True
        send_buffer =[]        
        # for i in range (0,4):
        # Transmit the contents of the tx buffer to the USB device
        # bulk out addresss
        send_buffer.extend(self._tx_buffer)
        
        # Add trailing zeros to complete 65 bytes
        # send_buffer.extend([0]*(MAX_TX_BUFFER_SIZE-len(send_buffer)))
        try:
            return_byte = self._usb_device.write(
            self._bulk_out_address, 
            bytes(self._tx_buffer), 
            TXRX_TIMEOUT_MS)
        except Exception as e:
            self.ongoing_transmit = False
            print(e)
            self.usbcdc_receive()
            return None
        
        if return_byte != (len(send_buffer)):
            print('Incorrect number of data bytes sent')
            self.usbcdc_receive()   
            return None 

        # Always get a response to flush the RX buffer contents
        # Succeeding messages cannot be received without flushing it by reading
        self.usbcdc_receive()
        return self._rx_buffer
           
    def usbcdc_receive(self):
        try:
            # self._rx_buffer = list(self._usb_device.read(
            #     USB_CDC_REQUEST.MAX_USB_FRAME_SIZE,
            #     0
            # ))
            
            self._rx_buffer = list(self._usb_device.read(
                self._bulk_in_address,
                MAX_TX_BUFFER_SIZE,
                TXRX_TIMEOUT_MS
            ))
        except Exception as e:
            self.ongoing_transmit = False
            print(e)
            return None
        else:
            # sleep(0.15)
            self.ongoing_transmit = False
            return self._rx_buffer