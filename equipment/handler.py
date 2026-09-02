from equipment.ac_source import ACSource, AC_SOURCE_COUPLING
from equipment.power_meter import PowerMeter
from equipment.electronic_load import ElectronicLoad, ElectronicLoadMainframe, ElectronicLoadModule
from equipment.dc_source import DCSource
from equipment.oscilloscope import Oscilloscope
from equipment.oscilloscope_specs import *

import hid
import usb.core
import usb.util
import libusb_package
from sink_controllers.epr_sink_control import STM32SinkController
from sink_controllers.pi_epr_sink import PISinkController
import sink_controllers.pi_epr_sink as PI_EPR_SINK
import sink_controllers.epr_sink_control as STM32_EPR_SINK
from sink_controllers import pat_tool
from sink_controllers.pat_tool import SMBUS_STATE, PDSinkController, InnoProI2CControllerContainer
from time import sleep

import pyvisa
from pyvisa.resources.resource import Resource
from lecroydso import LeCroyDSO
from equipment.lecroyvisa import LeCroyVISA

from equipment.definitions import (AC_SOURCE_LIST, POWER_METER_LIST, ELECTRONIC_LOAD_MAINFRAME_LIST, 
                                        ELECTRONIC_LOAD_MODULES_LIST, ELECTRONIC_LOAD_LIST,
                                        DC_SOURCE_LIST, OSCILLOSCOPE_LIST)
from equipment.definitions import EquipmentType


from user_settings.save_load import (read_from_default_config, SaveFileKeys)

class EquipmentHandler():
    """
    Handles all of the equipment 

    Notes
    -----
    Electronic Load Modules are handled individually without needing to reference the channel number.
    Electronic Load Mainframe can also be accessed as a whole.
    
    """
    def __init__(self, parent):
        """
        
        Multiple instances are initialized to allow for future expansions

        The equipment settings are set up later
        """
        self.parent = parent

        self.initialize_pyvisa()
        try:
            # List of all equipment
            self.initialize_equipment_lists()
        except:
            raise Exception


        # Check which equipment are accessible
        self.update_accessible_equipment()

        # The equipment are assigned roles which are universal to the program
        # For example: 
        # self.power_meters[0] can be assigned as -> self.power_meter_source
        # so that it is easier to access the equipment
        self.define_equipment_roles()
        self.initialize_equipment_role_assigment()
        
    def initialize_pyvisa(self):
        """ Try to access the pyvisa resource manager
        
        """
        try:
            self.rm = pyvisa.ResourceManager()
        except Exception as e:
            # Prepare try except block 
            raise e

    def initialize_equipment_lists(self):
        """ Initialize containers for the individual equipment types
        """
        self.ac_sources:list[ACSource] = []
        
        self.dc_sources:list[DCSource] = []

        self.e_loads:list[ElectronicLoad] = []
        self.e_load_mainframes:list[ElectronicLoadMainframe] = []

        self.power_meters:list[PowerMeter] = []

        self.oscilloscopes:list[Oscilloscope] = []

        # List of equipment that can be accessed by PyVisa
        self.gpib_resource:list[Resource] = []   

        # TODO: Setup the SinkController list for multiplexed sink controllers
        # For now, use only 1 USB CDC connected sink controller
        self.sink_controllers:list[PISinkController|STM32SinkController|PDSinkController] = []
        
        #self.sink_controllers.append(STM32SinkController())
        

        #self.usbpd_sink = self.sink_controllers[0]
        self.i2c_controllers:list[InnoProI2CControllerContainer] = []
        # To be opened by the thread that will use the resource
        # self.i2c_controller.close()
    ################################################################################
    #                    EQUIPMENT ACCESSIBILITY CHECKS                            #
    ################################################################################

    def update_accessible_equipment(self):
        """ Update the accessible equipment from the different interfaces
        
        """
        
        self.update_accessible_visa_equipment()
        # self.check_scope_availability(get_default=True)
        self.update_accessible_sink_controllers()
   

    def clear_accessible_visa_equipment(self):
        """ Clear all the entries on the lists of GPIB Equipment
        """
        self.ac_sources.clear()
        self.dc_sources.clear()
        self.e_loads.clear()
        self.e_load_mainframes.clear()
        self.power_meters.clear()
        self.gpib_resource.clear()


    def update_accessible_visa_equipment(self):
        """ Update the list of available GPIB resources that VISA can access
        """
        self.clear_accessible_visa_equipment()
        
        # List the equipment accessible by the Visa Resource Manager
        resource_list = self.rm.list_resources()


        # Loop through all the equipment
        for resource_txt in resource_list:
            last = resource_txt.rfind("::")
            addr = resource_txt[:last]

            # Look only for GPIB connected equipment
            # TODO: Expand to other interfaces
            if "GPIB" in resource_txt:
                
                # Check if equipment can be accessed
                try:
                    device = self.rm.open_resource(addr)
                    device_id  = device.query("*IDN?")
                
                except pyvisa.VisaIOError as e:
                    # print(e)
                    if e.error_code == pyvisa.errors.VI_ERROR_CONN_LOST:
                        try:
                            self.rm.close()
                            self.rm = pyvisa.ResourceManager()
                        except Exception as e:
                            pass
                            # print(e)
                    # retry after resetting resource manager
                    try:
                        device = self.rm.open_resource(addr)
                        device_id  = device.query("*IDN?")
                           
                    # Ignore the exception if the equipment cannot be accessed
                    except pyvisa.VisaIOError as e:
                        print(f'Cannot open resource: {resource_txt}')
                    else:
                        print(resource_txt)
                        print(f'Accessible Resource: {device_id}')
                
                        # Use that information along with the visa resource to create a new Equipment object
                        self.gpib_resource.append(device)
                        self.new_gpib_equipment(device, device_id, addr)
            
                # If equipment is accessible 
                else:
                    print(resource_txt)
                    print(f'Accessible Resource: {device_id}')
                
                    # Use that information along with the visa resource to create a new Equipment object
                    self.gpib_resource.append(device)
                    self.new_gpib_equipment(device, device_id, addr)
            
            # elif "TCPIP" in resource_txt:
            #     last = addr.rfind("::")
            #     addr = resource_txt[:last]
            #     left = addr.find('::')
            #     address = addr[left+2:]
            #     try:
            #         device = self.rm.open_resource(f'TCPIP::{address}', timeout=2100)
            #         device_id  = device.query("*IDN?")
            #     except:
            #         pass

    def check_scope_availability(self, address:str='', get_default: bool = False)->bool:
        # At startup, the default value is loaded
        if get_default:
            address = read_from_default_config(
                key=SaveFileKeys.OSCILLOSCOPE_ADDRESS,
                default_value='')
        
        # Check if equipment can be accessed
        try:
            device = self.rm.open_resource(f'TCPIP::{address}', timeout=2100)
            device_id  = device.query("*IDN?")
        
        # Ignore the exception if the equipment cannot be accessed
        except pyvisa.VisaIOError as e:
            print(f'Cannot open oscilloscope at: {address}')
            return False
        # If equipment is accessible 
        else:
            print(f'Accessible Resource: {device_id}')

            # Check if response has header
            # Trim that header if it does
            if "*IDN" in device_id:
                device_id = device_id[5:]

            # Use that information along with the visa resource to create a new Equipment object
            self.oscilloscopes.clear()

            manufacturer = device_id[:device_id.find(',')].upper()
            if manufacturer == 'ROHDE&SCHWARZ':
                self.oscilloscopes.append(RohdeSchwarzOscilloscope(device, device_id))
            
            # LeCroy uses pyvisa internally but it has to be defined through the 
            # LeCroyVISA to work properly
            elif manufacturer == 'LECROY':
                transport = LeCroyVISA(f'TCPIP0::{address}::inst0::INSTR')
                dso = LeCroyDSO(transport)
                self.oscilloscopes.append(LeCroyOscilloscope(dso, device_id))
                
            if len(self.oscilloscopes):
                self.oscilloscope = self.oscilloscopes[0]
                return True
            else:
                self.oscilloscope = None
                return False


    def new_gpib_equipment(self, device:Resource, device_id:str, addr:str)->None:
        """ Create an equipment object from the device id and visa resource
        
        """
        # Split the device ID string into its contents
        manufacturer, model, serial, fw_version = device_id.split(",", 4)[:4]

        # Check the device model to see what kind of equipment it is
        equipment_type = self.get_equipment_type(model)
        
        match equipment_type:
            case EquipmentType.AC_SOURCE:
                self.ac_sources.append(ACSource(device, device_id))
            
            case EquipmentType.DC_SOURCE:
                self.dc_sources.append(DCSource(device, device_id))
            
            case EquipmentType.POWER_METER:
                self.power_meters.append(PowerMeter(device, device_id))

            case EquipmentType.ELECTRONIC_LOAD_MAINFRAME:
                # Get individual modules from the mainframe
                new_load_mainframe = ElectronicLoadMainframe(device, device_id)
                self.e_load_mainframes.append(new_load_mainframe)
                
                # Get individual modules from the mainframe
                eload_modules = new_load_mainframe.get_eload_module_objects()
                
                for module in eload_modules:
                    self.e_loads.append(module)


            case EquipmentType.ELECTRONIC_LOAD:
                self.e_loads.append(ElectronicLoad(device, device_id))
            
            # Typically oscilloscope is connected through lan but just in case
            case EquipmentType.OSCILLOSCOPE:
                self.oscilloscopes.append(Oscilloscope(device, device_id))

    def get_equipment_type(self, equipment_model:str)->EquipmentType:
        """ Check the equipment type by comparing the equipment model
        to a list of predefined equipment model numbers
        
        """
        # Check if equipment is AC Source
        if equipment_model in AC_SOURCE_LIST:
            return EquipmentType.AC_SOURCE

        # Check if equipment is DC Source
        elif equipment_model in DC_SOURCE_LIST:
            return EquipmentType.DC_SOURCE

        # Check if equipment is Power Meter
        elif equipment_model in POWER_METER_LIST:
            return EquipmentType.POWER_METER
        
        # Check if equipment is Electronic Load Mainframe
        elif equipment_model in ELECTRONIC_LOAD_MAINFRAME_LIST:
            return EquipmentType.ELECTRONIC_LOAD_MAINFRAME

        # Check if equipment is standalone Electronic load
        elif equipment_model in ELECTRONIC_LOAD_LIST:
            return EquipmentType.ELECTRONIC_LOAD

        # Check if equipment is Oscilloscope
        elif equipment_model in OSCILLOSCOPE_LIST:
            return EquipmentType.OSCILLOSCOPE
    
    def update_accessible_sink_controllers(self):
        """ Check the interfaces either USB to I2C or direct CDC if a known SinkController is connected
        
        Currently only a single CDC device is being checked
        TODO: update for multiplexed SinkController modules using I2C
        """
        
        self.usbpd_sink = None
        self.i2c_controller = None
        
        # self.usbpd_sink.find_sink_controller_device()
        # if self.usbpd_sink.sink_controller_device_found:
        for sink_controller in self.sink_controllers:
            try:
                sink_controller.close()
            except:
                pass
            
        # For PI EPR sinks
        self.sink_controllers:list[PISinkController|STM32SinkController|PDSinkController] = []
        self.i2c_controllers:list[InnoProI2CControllerContainer] = []
        sink_index = 0
        for hid_device in hid.enumerate(vendor_id=PI_EPR_SINK.DEVICE_INFO.VID,product_id=PI_EPR_SINK.DEVICE_INFO.PID):
            sn = hid_device['serial_number']
            self.sink_controllers.append(PISinkController())
            self.sink_controllers[sink_index].get_status(serial_number=sn)
            sink_index +=1
            
        for device in libusb_package.find(find_all = True, idVendor = STM32_EPR_SINK.DEVICE_INFO.VID, idProduct = STM32_EPR_SINK.DEVICE_INFO.PID):
            sn = device.serial_number
            device.reset()
            self.sink_controllers.append(STM32SinkController())
            self.sink_controllers[sink_index].get_status(serial_number=sn)
            self.sink_controllers[sink_index]._usb_device.reset()
            device.reset()
            sink_index +=1
            
        i2c_controller_index = 0
        
        for hid_device in hid.enumerate(vendor_id=pat_tool.DEVICE_INFO.VID,product_id=pat_tool.DEVICE_INFO.PID):
            self.sink_controllers.append(PDSinkController())
            self.sink_controllers[sink_index].close()
            self.i2c_controllers.append(InnoProI2CControllerContainer())
            self.i2c_controllers[i2c_controller_index]
            sink_index +=1
            i2c_controller_index +=1 

        if len(self.sink_controllers) > 0:
            self.usbpd_sink = self.sink_controllers[0]
        else:
            self.usbpd_sink = None
            
        if len(self.i2c_controllers) > 0:
            self.i2c_controller = self.i2c_controllers[0]
        else:
            self.i2c_controller = None
        
        for i2c_controller in self.i2c_controllers:
            i2c_controller.close()
        return self.sink_controllers, self.i2c_controllers
            

    ################################################################################
    #                       Equipment Role Assignment                              #
    ################################################################################
    def define_equipment_roles(self):
        """The identifiers for each roles are defined but not assigned yet."""

        # Power Meter Roles
        self.reset_power_meter_roles()
        # List of assigned roles
        self.power_meter_roles = [
            self.power_meter_source,
            self.power_meter_load_1,
            self.power_meter_load_2,
            self.power_meter_load_3,
            self.power_meter_load_4,
            self.power_meter_load_5,
            self.power_meter_load_6,
        ]

        # Electronic Load Roles
        self.reset_electronic_load_roles()
        # List of assigned roles
        self.electronic_load_roles = [
            self.electronic_load_1,
            self.electronic_load_2,
            self.electronic_load_3,
            self.electronic_load_4,
            self.electronic_load_5,
            self.electronic_load_6,
        ]

        # Sink Controller Roles
        self.reset_sink_controller_roles()
        # List of assigned roles
        self.sink_controller_roles = [
            self.sink_controller_1,
            self.sink_controller_2,
            self.sink_controller_3,
            self.sink_controller_4,
        ]
        
        self.reset_i2c_controller_roles()
        # List of assigned roles
        self.i2c_controller_roles = [
            self.i2c_controller_1,
            self.i2c_controller_2,
            self.i2c_controller_3,
            self.i2c_controller_4,
        ]

        # No need for list of roles for equipment that we don't expect to have multiples of
        self.ac_source:ACSource = None
        self.dc_source:DCSource = None
        self.oscilloscope:OscilloscopeBaseClass = None

    def reset_power_meter_roles(self):
        self.power_meter_source:PowerMeter = None
        self.power_meter_load_1:PowerMeter = None
        self.power_meter_load_2:PowerMeter = None
        self.power_meter_load_3:PowerMeter = None
        self.power_meter_load_4:PowerMeter = None
        self.power_meter_load_5:PowerMeter = None
        self.power_meter_load_6:PowerMeter = None

    def reset_electronic_load_roles(self):
        self.electronic_load_1:ElectronicLoadModule = None
        self.electronic_load_2:ElectronicLoadModule = None
        self.electronic_load_3:ElectronicLoadModule = None
        self.electronic_load_4:ElectronicLoadModule = None
        self.electronic_load_5:ElectronicLoadModule = None
        self.electronic_load_6:ElectronicLoadModule = None

    def reset_sink_controller_roles(self):
        self.sink_controller_1:PISinkController = None
        self.sink_controller_2:PISinkController = None
        self.sink_controller_3:PISinkController = None
        self.sink_controller_4:PISinkController = None
        
    def reset_i2c_controller_roles(self):
        self.i2c_controller_1:InnoProI2CControllerContainer = None
        self.i2c_controller_2:InnoProI2CControllerContainer = None
        self.i2c_controller_3:InnoProI2CControllerContainer = None
        self.i2c_controller_4:InnoProI2CControllerContainer = None

    def get_ac_source(self):
        
        id_list = []
        for ac_source in self.ac_sources:
            id_list.append(ac_source.description)

    def initialize_equipment_role_assigment(self):
        """ Assign a role to each equipment

        Each equipment connected will have a specific role

        For example:
        There are multiple power meters connected but one of them can be for source
        and the others are for different load

        Assigning roles to them will make it easier and more uniform for testing

            self.power_meter_source = self.power_meters[0]
            self.power_meter_load1 = self.power_meters[1]
        
        This role assignment can be changed either through an interface or a configuration file        
        
        The function will first look for a saved configuration file but if no file is found,
        it will default to setting the roles according to the sequence that it is read
        """

        # TODO: Look for a configuration file in AppData
        # for now, assume no configuration file is found 
        configuration_file_found = False

        if not configuration_file_found:
            # If no configuration file is 
            self.auto_set_equipment_roles()

    def auto_set_equipment_roles(self):

        self.auto_set_power_meter_roles()
        self.auto_set_electronic_load_roles()
        self.auto_set_sink_controller_roles()
        self.auto_set_i2c_controller_roles()
        
        self.auto_set_ac_source_roles()
        self.auto_set_dc_source_roles()

    def auto_set_power_meter_roles(self)->None:
        """ Set the roles of the power meters according to the order of the GPIB addresses
            This initial order is determined when the list of available equipment is defined
        
            Loop through all available power meters and set each roles depending on the order that it is defined
            

            Example
            -----------
            If we have 3 power meters connected with GPIB addresses 1, 2 and 4
                power_meter_source <- power meter @ GPIB::1 
                power_meter_load_1 <- power meter @ GPIB::2 
                power_meter_load_2 <- power meter @ GPIB::4 
                power_meter_load_3 <- None
                power_meter_load_4 <- None
                power_meter_load_5 <- None
                power_meter_load_6 <- None
            
            This automatic assignment is based on the list self.power_meter_roles
        """

        
        # Reset the roles first so that there will be no leftover assignment
        self.reset_power_meter_roles()

        # Loop through the available power meters and set the roles
        # according to the order in self.power_meter_roles
        self.power_meter_roles = [None] * 6
        for i, power_meter in enumerate(self.power_meters):
            self.power_meter_roles[i] = (power_meter)

        self.power_meter_source = self.power_meter_roles[0]
        self.power_meter_load_1 = self.power_meter_roles[1]
        self.power_meter_load_2 = self.power_meter_roles[2]
        self.power_meter_load_3 = self.power_meter_roles[3]
        self.power_meter_load_4 = self.power_meter_roles[4]
        self.power_meter_load_5 = self.power_meter_roles[5]

    def auto_set_electronic_load_roles(self):
        """ Set the roles of the power meters according to the order of the GPIB addresses and channel numbers
            This initial order is determined when the list of available equipment is defined
        
            Loop through all available power meters and set each roles depending on the order that it is defined
            
            Example
            -----------
            If we have 2 Electronic load mainframes (GPIB::1 and ::2)
                with 2 modules each at channels 3 and 5:
                
                electronic_load_1 <- Eload module @ GPIB::1 > Channel 3
                electronic_load_2 <- Eload module @ GPIB::1 > Channel 5
                electronic_load_3 <- Eload module @ GPIB::2 > Channel 3
                electronic_load_4 <- Eload module @ GPIB::2 > Channel 5
                electronic_load_5 <- None
                electronic_load_6 <- None
            
            This automatic assignment is based on the list self.electronic_load_roles
        """
        # Reset the roles first so that there will be no leftover assignment
        self.reset_electronic_load_roles()

        # Loop through the available electronic loads and set the roles
        # according to the order in self.electronic_load_roles
        self.electronic_load_roles = [None] * 6
        for i, e_load in enumerate(self.e_loads):
            self.electronic_load_roles[i] = e_load
        
        self.electronic_load_1 = self.electronic_load_roles[0]
        self.electronic_load_2 = self.electronic_load_roles[1]
        self.electronic_load_3 = self.electronic_load_roles[2]
        self.electronic_load_4 = self.electronic_load_roles[3]
        self.electronic_load_5 = self.electronic_load_roles[4]
        self.electronic_load_6 = self.electronic_load_roles[5]



    def auto_set_sink_controller_roles(self):
        """
        """
        # TODO: For multiplexed sink controllers
        # For now, just set it as self.sink_controller_1
        
        # Check first how many sink controllers are available
        # NOTE: for now check one only
        self.reset_sink_controller_roles()
        
        self.sink_controller_roles = [None] * 4
        for i, sink_controller in enumerate(self.sink_controllers):
            self.sink_controller_roles[i] = (sink_controller)
        
        self.sink_controller_1 = self.sink_controller_roles[0]
        self.sink_controller_2 = self.sink_controller_roles[1]
        self.sink_controller_3 = self.sink_controller_roles[2]
        self.sink_controller_4 = self.sink_controller_roles[3]
            
        # if self.usbpd_sink.usb_pd_sink_connection_ok:
        #     self.sink_controller_1 = self.usbpd_sink
        # else:
        #     self.sink_controller_1 = None

        # # TODO: Update for multiplexed sink controllers
        # self.sink_controller_2 = None
        # self.sink_controller_3 = None
        # self.sink_controller_4 = None


    def auto_set_i2c_controller_roles(self):
        """
        """
        # TODO: For multiplexed sink controllers
        # For now, just set it as self.sink_controller_1
        
        # Check first how many sink controllers are available
        # NOTE: for now check one only
        self.reset_i2c_controller_roles()
        
        self.i2c_controller_roles = [None] * 4
        for i, i2c_controller in enumerate(self.i2c_controllers):
            self.i2c_controller_roles[i] = (i2c_controller)
        
        self.i2c_controller_1 = self.i2c_controller_roles[0]
        self.i2c_controller_2 = self.i2c_controller_roles[1]
        self.i2c_controller_3 = self.i2c_controller_roles[2]
        self.i2c_controller_4 = self.i2c_controller_roles[3]

    
    def auto_set_ac_source_roles(self):
        """ Placeholder if there are tests with multiple AC sources
        """
        # For now, set it as the first AC source in the list
        self.ac_source = None
        
        if len(self.ac_sources) > 0:
            self.ac_source = self.ac_sources[0]


    def auto_set_dc_source_roles(self):
        """ Placeholder if there are tests with multiple DC sources
        """
        # For now, set it as the first DC source in the list

        self.dc_source = None
        
        if len(self.dc_sources) > 0:   
            self.dc_source = self.dc_sources[0]
            
    def input_supply_eload_discharge_sequence(self,iout_A,coupling=AC_SOURCE_COUPLING.AC):
        self.electronic_load_1.cc = iout_A
        self.electronic_load_1.turn_on()
        if (self.dc_source is not None) and (coupling == AC_SOURCE_COUPLING.DC):
            self.dc_source.turn_off()
        else:
            self.ac_source.turn_off()
            self.ac_source.coupling = 'AC'
            self.ac_source.offset = 0
            self.ac_source.ac_slew_rate = 9.9e37
            self.ac_source.dc_slew_rate = 9.9e37
            self.ac_source.freq_slew_rate = 9.9e37
        sleep(3)
        self.electronic_load_1.turn_off()
        sleep(0.5)
        self.electronic_load_1.reset_values()
        self.power_meter_load_1.set_current_range_max()
        self.power_meter_load_1.current_auto_range_enable()
            
        
if __name__ == '__main__':
    pass