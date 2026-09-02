import ctypes as ct
from ctypes import c_uint32, c_uint16

from enum import Enum


class PD_MULTIPLIER():
    APDO_MAX_VOLT_MULTIPLIER = 100
    APDO_MIN_VOLT_MULTIPLIER = 100
    PPS_MAX_CURRENT_MULTIPLIER = 50
    
    SPR_AVS_CURRENT_MULTIPLIER = 10

    EPR_AVS_RDO_CURRENT_MULTIPLIER = 20
    EPR_AVS_RDO_VOLTAGE_MULTIPLIER = 40

    PPS_RDO_CURRENT_MULTIPLIER = 20
    PPS_RDO_VOLTAGE_MULTIPLIER = 50

    EPR_AVS_POWER_MULTIPLIER = 1
    FPDO_SUPPLY_VOLT_MULTIPLIER = 50
    FPDO_SUPPLY_MAX_CURRENT_MULTIPLIER = 10
    POWER_DIVIDER = 100

# Define USB PD specs
class PD_SPECS():
        
    USBPD_MIN_REQ_CURRENT_A = 1.0
    USBPD_MAX_REQ_CURRENT_A = 5.0
    
    USBPD_MIN_SPR_PPS_VOLTAGE_V = 3.3
    USBPD_MAX_SPR_PPS_VOLTAGE_V = 21.0
    USBPD_MAX_SPR_FIXED_VOLTAGE_V = 20.0
    
    USBPD_STEP_SPR_VOLTAGE_MV = 20
    USBPD_STEP_SPR_CURRENT_MA = 50
    
    USBPD_MIN_SPR_AVS_LOW_VOLTAGE_V = 9
    USBPD_MAX_SPR_AVS_LOW_VOLTAGE_V = 15
    
    USBPD_MIN_SPR_AVS_HIGH_VOLTAGE_V = 15
    USBPD_MAX_SPR_AVS_HIGH_VOLTAGE_V = 20
    
    USBPD_MIN_EPR_AVS_VOLTAGE_V = 15
    USBPD_MAX_EPR_AVS_VOLTAGE_V = 48
    USBPD_MAX_EPR_FIXED_VOLTAGE_V = 48.0
    
    USBPD_STEP_EPR_VOLTAGE_MV = 100
    USBPD_STEP_EPR_CURRENT_MA = 50
    
    USBPD_SPR_MAX_OBJECT_POSITION = 7
    USBPD_EPR_MAX_OBJECT_POSITION = 13

# USB PD Table 6-7
class SUPPLY_TYPE():
    FIXED = 0
    VARIABLE = 1
    BATTERY = 2
    AUGMENTED = 3

class AUGMENTED_TYPE():
    SPR_PPS = 0
    EPR_AVS = 1
    SPR_AVS = 2
    
class USBPD_REQUEST_ID():
    GET_BOARD_INFO          = 1
    USB_PD_STATUS           = 2
    USBPD_RDO_REQUEST       = 3
    USBPD_EPR_TEST_CASE     = 4
    USBPD_HID_TEST_REQUEST_ID = 5
    USBPD_UVDM_XRAM_READ_ID = 6
    USBPD_DATA_ROLE_SWAP_ID = 7
    
class SOP_TYPE():
    PD_E_SOP_TYPE_SOP           = 0
    PD_E_SOP_TYPE_SOP1          = 1
    PD_E_SOP_TYPE_SOP2          = 2
    PD_E_SOP_TYPE_SOP1_DEBUG    = 3
    PD_E_SOP_TYPE_SOP2_DEBUG    = 4
    PD_E_HARD_RESET             = 5
    PD_E_CABLE_RESET            = 6
    PD_E_BIST_MODE              = 7
    PD_E_SOP_TYPE_ERROR         = 0xFF
    

TXRX_TIMEOUT_MS         = 100
    
class EPR_TEST_CASE():
    TC_EPR_IDLE                                         =   1
    TC_EPR_ENTRY                                        =   2
    TC_EPR_EXIT                                         =   3
    TC_EPR_KEEP_LIVE_TIMEOUT                            =   4
    TC_EPR_SEND_HARD_RESET                              =   5
    TC_EPR_SEND_SOFT_RESET                              =   6
    TC_EPR_SEND_EPR_MODE_COMMAND_BEFORE_EPR_ENTRY       =   7
    TC_EPR_SEND_EPR_MODE_COMMAND_AFTER_EPR_ENTRY        =   8
    TC_EPR_EXIT_WITH_EPR_REQUEST                        =   9
    TC_SPR_GET_SOURCE_CAP                               =   10
    TC_EPR_GET_SOURCE_CAP                               =   11
    TC_EPR_SEND_OTHER_THAN_KEEP_ALIVE                   =   12
    TC_VCONN_SWAP                                       =   13
    
class USB_PD_PACKET_TYPE():
    UCPD_CONFIG_PACKET_TYPE                 = 0x02
    UCPD_WRITE_PACKET_TYPE                  = 0x03
    UCPD_READ_PACKET_TYPE                   = 0x04
    UCPD_READ_CURRENT_STATUS_PACKET_TYPE    = 0x05
    UCPD_RDO_PACKET_TYPE                    = 0x06
    UCPD_CONTROL_MESSAGE_TYPE               = 0x07    

class UVDM_VID():
    VID_LOW_SCS   = 0x2D
    VID_HIGH_SCS  = 0x76

    VID_HIGH_PI   = 0x28
    VID_LOW_PI    = 0x31

    PI_VID_OTP_SRN_RD = 0xA2
    PI_VID_OTP_SRN_WR = 0xA4

    PI_VID_I2C_RD = 0xB1
    PI_VID_I2C_WR = 0xB2

    PI_VID_OTP_RD = 0xB3
    PI_VID_OTP_WR = 0xB4

    PI_VID_XRAM_RD = 0xB5
    PI_VID_XRAM_WR = 0xB6
    
class UCPD_VDM_TYPE():
    UCPD_UNSTRUCTURED   = 0
    UCPD_STRUCTURED     = 1

class UCPD_RESPONSE_STATUS():
    UCPD_NAK            = 0
    UCPD_ACK            = 1
    
class UCPD_REQUEST_RESPONSE():
    UCPD_REQUEST        = 0
    UCPD_RESPONSE       = 1
    
class UCPD_MESSAGE_TYPE():
    UCPD_MTP            = 0
    UCPD_XRAM           = 1
    UCPD_SFR            = 2
    UCPD_INNO           = 3
    UCPD_MCU            = 4
    UCPD_FW_UPDATE      = 5
    
class UCPD_WRITE_READ():
    UCPD_READ           = 0
    UCPD_WRITE          = 1
    
    
INNO_PRO_PD_VDM_WRITE = 0x40

PD_SPR_REQ = 0x02
PD_EPR_REQ = 0x09    

USBPD_VENDOR_ID  = 0x2831
    
    
# Enumeration of the commands supported in PD_CTRL register
###############################################################################################
#  PD Commands                                                                                #
###############################################################################################

class PD_DATA_MESSAGE(Enum):
    RESERVED            = 0
    SOURCE_CAPABILITIES = 1
    REQUEST             = 2
    BIST                = 3
    SINK_CAPABILITIES   = 4
    BATTERY_STATUS      = 5
    ALERT               = 6
    GET_COUNTRY_INFO    = 7
    ENTER_USB           = 8
    EPR_REQUEST         = 9
    EPR_MODE            = 10
    SOURCE_INFO         = 11
    REVISION            = 12
    VENDOR_DEFINED      = 15

class PD_CONTROL_MESSAGE(Enum):
    RESERVED                = 0
    GOODCRC                 = 1
    GOTOMIN                 = 2
    ACCEPT                  = 3
    REJECT                  = 4
    PING                    = 5
    PS_RDY                  = 6
    GET_SOURCE_CAP          = 7
    GET_SINK_CAP            = 8
    DR_SWAP                 = 9
    PR_SWAP                 = 10
    VCONN_SWAP              = 11
    WAIT                    = 12
    SOFT_RESET              = 13
    DATA_RESET              = 14
    DATA_RESET_COMPLETE     = 15
    NOT_SUPPORTED           = 16
    GET_SOURCE_CAP_EXTENDED = 17
    GET_STATUS              = 18
    FR_SWAP                 = 19
    GET_PPS_STATUS          = 20
    GET_COUNTRY_CODES       = 21
    GET_SINK_CAP_EXTENDED   = 22
    GET_SOURCE_INFO         = 23
    GET_REVISION            = 24


class PD_COMMAND(Enum):
    SET_TYPE_C_DEFAULT_RP           = 0
    SET_TYPE_C_1_5A_RP              = 1
    SET_TYPE_C_3A_RP                = 2
    SEND_DR_SWAP                    = 5
    SEND_PR_SWAP                    = 6
    TURN_ON_VCONN                   = 7
    TURN_OFF_VCONN                  = 8
    SEND_VCONN_SWAP                 = 9
    GET_SRC_CAP                     = 10
    GET_SNK_CAP                     = 11
    SEND_GOTOMIN                    = 12
    SEND_HARD_RESET                 = 13
    SEND_SOFT_RESET_SOP             = 14
    SEND_CABLE_RESET                = 0xF
    SEND_EC_INIT_COMPLETE           = 0x10
    DISABLE_PORT                    = 17
    SEND_SOFT_RESET_SOP_PRIME       = 18
    SEND_SOFT_RESET_SOP_D_PRIME     = 19
    CHANGE_PORT_PARAMS              = 20
    ABORT_PD_CMD                    = 21
    GET_EXTD_SRC_CAP                = 22
    GET_STATUS                      = 23
    SEND_NOT_SUPPORTED              = 24
    GET_PPS_STATUS                  = 25
    RSVD1                           = 26
    RSVD2                           = 27
    SEND_OV_NOTIFICATION            = 28
    SEND_OC_NOTIFICATION            = 29
    SEND_OT_NOTIFICATION            = 30
    SEND_CCG_ALIVE                  = 0x1F
    READ_SRC_PDO                    = 0x20
    READ_SNK_PDO                    = 33
    READ_EXTD_SRC_CAP               = 36
    WR_EXTD_SRC_CAP                 = 37
    

###############################################################################################
#  CYPD2122 - CCG2 HPI v1 Register                                                            #
###############################################################################################
# Import as CY_PD_REG
class HPI_V1_REG(Enum):
    DEVICE_MODE_ADDR                = 0
    BOOT_MODE_REASON                = 1
    SILICON_ID                      = 2
    INTR_REG_ADDR                   = 6
    JUMP_TO_BOOT_REG_ADDR           = 7
    RESET_ADDR                      = 8
    ENTER_FLASH_MODE_ADDR           = 10
    VALIDATE_FW_ADDR                = 11
    FLASH_READ_WRITE_ADDR           = 12
    GET_VERSION                     = 0x10
    U_VDM_CTRL_ADDR                 = 0x20
    READ_PD_PROFILE                 = 34
    EFFECTIVE_SOURCE_PDO_MASK       = 36
    EFFECTIVE_SINK_PDO_MASK         = 37
    SELECT_SOURCE_PDO               = 38
    SELECT_SINK_PDO                 = 39
    PD_CONTROL                      = 40
    PD_STATUS                       = 44
    TYPE_C_STATUS                   = 48
    CURRENT_PDO                     = 52
    CURRENT_RDO                     = 56
    CURRENT_CABLE_VDO               = 60
    HPD_MODE                        = 68
    DP_MUX_SELECT                   = 69
    EVENT_MASK                      = 72
    SRC_PDO                         = 84
    SRC_PDO_CNT                     = 112
    MEASURE_VBUS                    = 113
    RESPONSE_ADDR                   = 126
    BOOTDATA_MEMORY_ADDR            = 0x80
    FWDATA_MEMORY_ADDR              = 192

###############################################################################################
#  CYPD2122 - CCG2 HPI Response                                                               #
###############################################################################################
# Import as CY_PD_RESP

class HPI_RESPONSE(Enum):
    NO_RESPONSE                     = 0
    SUCCESS                         = 2
    FLASH_DATA_AVAILABLE            = 3
    INVALID_COMMAND                 = 5
    COLLISION_DETECTED              = 6
    FLASH_UPDATE_FAILED             = 7
    INVALID_FW                      = 8
    INVALID_ARGUMENTS               = 9
    NOT_SUPPORTED                   = 10
    TRANSACTION_FAILED              = 12
    PD_COMMAND_FAILED               = 13
    UNDEFINED                       = 14
    RESET_COMPLETE                  = 0x80
    MESSAGE_QUEUE_OVERFLOW          = 129
    OVER_CURRENT_DETECTED           = 130
    OVER_VOLTAGE_DETECTED           = 131
    TYPC_C_CONNECTED                = 132
    TYPE_C_DISCONNECTED             = 133
    PD_CONTRACT_ESTABLISHED         = 134
    DR_SWAP                         = 135
    PR_SWAP                         = 136
    VCON_SWAP                       = 137
    PS_RDY                          = 138
    GOTOMIN                         = 139
    ACCEPT_MESSAGE                  = 140
    REJECT_MESSAGE                  = 141
    WAIT_MESSAGE                    = 142
    HARD_RESET                      = 143
    VDM_RECEIVED                    = 144
    SRC_CAP_RCVD                    = 145
    SINK_CAP_RCVD                   = 146
    DP_ALTERNATE_MODE               = 147
    DP_DEVICE_CONNECTED             = 148
    DP_DEVICE_NOT_CONNECTED         = 149
    DP_SID_NOT_FOUND                = 150
    MULTIPLE_SVID_DISCOVERED        = 151
    DP_FUNCTION_NOT_SUPPORTED       = 152
    DP_PORT_CONFIG_NOT_SUPPORTED    = 153
    HARD_RESET_SENT                 = 154
    SOFT_RESET_SENT                 = 155
    CABLE_RESET_SENT                = 156
    SOURCE_DISABLED_STATE_ENTERED   = 157
    SENDER_RESPONSE_TIMER_TIMEOUT   = 158
    NO_VDM_RESPONSE_RECEIVED        = 159
    UNEXPECTED_VOLTAGE_ON_VBUS      = 160
    TYPE_C_ERROR_RECOVERY           = 161
    EMCA_DETECTED                   = 166
    CABLE_DISC_FAILED               = 167
    RP_CHANGE_DETECTED              = 170
    SYS_EVT_VSEL                    = 178


# Class for PI EPR Sink UVDM Packet

class PI_UVDM_Packet_bits(ct.LittleEndianStructure):
    _fields_ = [("pi_uvdm_length",          c_uint16,    5),
                ("pi_uvdm_msg_type",        c_uint16,    3),
                ("pi_rsvd",                 c_uint16,    4),
                ("pi_request_response_bit", c_uint16,    1),
                ("pi_response_status",      c_uint16,    1),
                ("pi_uvdm_read_write",      c_uint16,    1),
                ("pi_uvdm_unstructured",    c_uint16,    1),
                ("pi_uvdm_vid",             c_uint16,    16)]
class PI_UVDM_Packet(ct.Union):
    _fields_ = [("bits", PI_UVDM_Packet_bits),
                ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0
        
class PI_UVDM_Mem_Packet_bits(ct.LittleEndianStructure):
    _fields_ = [("pi_mem_addr", c_uint16,    16),
                ("pi_mem_rsvd", c_uint16,    16)]
class PI_UVDM_Mem_Packet(ct.Union):
    _fields_ = [("bits", PI_UVDM_Mem_Packet_bits),
                ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0
# Source Cap Class

class SourceCap():
    def __init__(self, *args, **kwargs):
        # Type
        self.supply_type:SUPPLY_TYPE = None
        self.augmented_type:AUGMENTED_TYPE = None
        self.epr_mode_capable:bool = None
        self.pdo_type_text:str = ""
        
        # Supports
        self.unchunked_ext_msg_support = 0
        self.data_role_swap = 0
        self.usb_comm_capable = 0
        self.externally_powered = 0
        self.usb_suspend_support = 0
        self.dual_role_power = 0
        self.usb_comm_capable = 0

        # Position
        self.object_position:int = None

        # FPDO Specific
        self.voltage_mV:int = None

        # PPS APDO Specific
        self.pps_power_limited:bool = None

        # Shared FPDO, PPS APDO, PPS AVS
        self.max_current_mA:int = None

        # Shared APDO
        self.min_voltage_mV:int = None
        self.max_voltage_mV:int = None
        
        # PPS AVS Specific
        self.max_current_high_range_mA:int = None
        self.max_current_low_range_mA:int = None
        
        # EPR AVS Specific
        self.pd_power_W:int = None

        # Peak current setting
        self.peak_current:int = None

        # 32 bit object
        self.bytes = None

        # Text for debugging
        self.text:str = ""
    
    def __str__(self):
        return self.text
################################################################################
####################           POWER DATA OBJECTS           ####################
################################################################################

# General purpose Power Data Object
class PDO_bits(ct.LittleEndianStructure):
    _fields_ = [("reserved",    c_uint32,    28),
                ("apdo_type",   c_uint32,    2),
                ("supply_type", c_uint32,    2)]
class PDO(ct.Union):
    _fields_ = [("bits", PDO_bits),
                ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0


# Fixed Power Data Object for Supplies
class FPDOSupply_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("max_current_10mA",            c_uint32, 10),  # Max current in 10mA units
        ("voltage_50mV",                c_uint32, 10),  # Voltage in 50mV units
        ("peak_current",                c_uint32, 2),   # Peak I (divergent from Ioc ratings)
        ("reserved",                    c_uint32, 1),   # Reserved
        ("epr_mode_capable",            c_uint32, 1),   # 
        ("unchunked_ext_msg_support",   c_uint32, 1),   # 
        ("data_role_swap",              c_uint32, 1),   # Data role swap supported
        ("usb_comm_capable",            c_uint32, 1),   # USB communications capable
        ("externally_powered",          c_uint32, 1),   # Externally powered
        ("usb_suspend_support",         c_uint32, 1),   # USB Suspend Supported
        ("dual_role_power",             c_uint32, 1),   # Dual-Role power  - supports PR swap
        ("supply_type",                 c_uint32, 2)]   # 0b00 for fixed supply
class FPDOSupply(ct.Union):
    _fields_ = [("bits", FPDOSupply_bits),
                ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0


# Fixed Power Data Object for Sinks
class FPDOSink_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("operational_current_10mA",c_uint32, 10),  # Operational current in 10mA units
        ("voltage_50mV",            c_uint32, 10),  # Voltage in 50mV units
        ("reserved",                c_uint32, 5),   # Reserved
        ("data_role_swap",          c_uint32, 1),   # Data role swap supported
        ("usb_comm_capable",        c_uint32, 1),   # USB communications capable
        ("externally_powered",      c_uint32, 1),   # Externally powered
        ("higher_capability",       c_uint32, 1),   # Needs more than vSafe5V
        ("dual_role_power",         c_uint32, 1),   # Dual-Role power - supports PR swap
        ("supply_type",             c_uint32, 2)]   # 0b00 for Fixed supply
class FPDOSink(ct.Union):
    _fields_ = [("bits", FPDOSink_bits),
                ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0

# Augmented Power Data Object
class APDO_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("apdo_defined",            c_uint32, 28), # APDO-Defined Bits 
        ("apdo_type",               c_uint32, 2),  # Augmented Type
        ("supply_type",             c_uint32, 2)]
class APDO(ct.Union):
    _fields_ = [("bits", APDO_bits),
                ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0


# Variable Power Data Object
class VPDO_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("max_current",            c_uint32, 10),  # APDO-Defined Bits 
        ("min_voltage",            c_uint32, 10),  # APDO-Defined Bits 
        ("max_voltage",            c_uint32, 10),   # Augmented Type
        ("supply_type",         c_uint32, 2)]   # (Augmented PDO)
class VPDO(ct.Union):
    _fields_ = [("bits", VPDO_bits),
                ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0


# Programmable Power Supply Data Object
class SPR_PPS_APDO_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("max_current_50mA",    c_uint32, 7),   # Max current in 50mA units
        ("reserved0",           c_uint32, 1),   # Reserved
        ("min_voltage_100mV",   c_uint32, 8),   # Min voltage in 100mV unit
        ("reserved1",           c_uint32, 1),   # Reserved
        ("max_voltage_100mV",   c_uint32, 8),   # Max voltage in 100mV units
        ("reserved2",           c_uint32, 2),   # Reserved
        ("pps_power_limited",   c_uint32, 1),   # 
        ("apdo_type",           c_uint32, 2),   # 0b00 for SPR PPS
        ("supply_type",         c_uint32, 2)]   # 0b11 for APDO
class SPR_PPS_APDO(ct.Union):
    _fields_ = [("bits", SPR_PPS_APDO_bits),
                ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0


# EPR Adjustable Voltage Supply Data Object
# USB PD 3.1 Table 6.20
class EPR_AVS_APDO_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("pdp_1W",              c_uint32, 8),   # pdp in 1W increments
        ("min_voltage_100mV",   c_uint32, 8),   # Min voltage in 100mV increments
        ("reserved1",           c_uint32, 1),   # Reserved
        ("max_voltage_100mV",   c_uint32, 9),   # Max voltage in 100mV increments
        ("peak_current",        c_uint32, 2),  # Peak current mode - Refer to USB PD 3.1 Table 6-15
        ("apdo_type",           c_uint32, 2),   # 0b01 for EPR AVS
        ("supply_type",         c_uint32, 2),]  # 0b11 for APDO
class EPR_AVS_APDO(ct.Union):
    _fields_ = [("bits", EPR_AVS_APDO_bits),
                ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0

# SPR Adjustable Voltage Supply Data Object
# USB PD 3.1 Table 6.20
class SPR_AVS_APDO_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("max_current_high_range_10mA", c_uint32, 10),   # Max current in 10 mA increments for 20 V - 15 V range
        ("max_current_low_range_10mA",  c_uint32, 10),   # Max current in 10 mA increments for 15 V - 9 V range
        ("reserved1",                   c_uint32, 6),   # Reserved
        ("peak_current",                 c_uint32, 2),   # Peak current mode - Refer to USB PD 3.1 Table 6-15
        ("apdo_type",                   c_uint32, 2),   # 0b10 for SPR AVS
        ("supply_type",                 c_uint32, 2)]   # 0b11 for APDO
class SPR_AVS_APDO(ct.Union):
    _fields_ = [("bits", SPR_AVS_APDO_bits),
                ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0

################################################################################
####################         EPR RELATED DATA OBJECTS       ####################
################################################################################

# EPR Mode Data Object
"""
    Bit values for the ACTION field are defined in @EPRMODE_ACTION
    Bit values for DATA field when EPR Entry failed are defined in @EPRMODE_DATA_FAILED

    Below are the different values required for the DATA field for other values of ACTION field
    
    ACTION field                DATA field value
    Enter                       Set to the EPR Sink Operational PDP
    Enter ACKNOWLEDGED          Set to 0
    Enter SUCCEEDED             Set to 0
    Enter FAILED                Refer to @EPRMODE_DATA_FAILED
    Exit                        Set to 0

"""
class EPRMDO_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("reserved",            c_uint32, 16),  # Max power in 1W increments
        ("data",                c_uint32, 8),   # Min voltage in 100mV increments
        ("action",              c_uint32, 1)]   # Reserved
class EPRMDO(ct.Union):
    _fields_ = [("bits", EPR_AVS_APDO_bits),
                ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0


class EPRMODE_ACTION(Enum):         # Sent By
    RESERVED0           =   0       
    ENTER               =   1       # Sink Only
    ENTER_ACKNOWLEDGED  =   2       # Source Only
    ENTER_SUCCEEDED     =   3       # Source Only
    ENTER_FAILED        =   4       # Source Only
    EXIT                =   5       # Sink or Source

class EPRMODE_DATA_FAILED(Enum):
    UNKNOWN_CAUSE                   =   0
    CABLE_NOT_EPR_CAPABLE           =   1
    SOURCE_FAILED_VCONN             =   2
    EPR_MODE_CAP_BIT_NOT_SET_RDO    =   3
    SOURCE_UNABLE_TO_ENTER_EPR      =   4
    EPR_MODE_CAP_BIT_NOT_SET_PDO    =   5



################################################################################
####################         REQUEST DATA OBJECTS           ####################
################################################################################

# Fixed and Variable RDO
# USB PD 3.1 Table 6-21
class FVRDO_bits(ct.LittleEndianStructure):
    _fields_ = [
            ("iout_max_10mA",               c_uint32, 10),  # Min/Max current in 10mA units
            ("iout_operating_10mA",         c_uint32, 10),  # Operating current in 10mA units
            ("reserved0",                   c_uint32, 2),   # Reserved - set to zero
            ("epr_mode_capable",            c_uint32, 1),   # Reserved - set to zero
            ("unchunked_ext_msg_support",   c_uint32, 1),   # Reserved - set to zero
            ("no_usb_suspend",              c_uint32, 1),   # Set when the sink wants to continue
            #                                                 the contract during USB suspend
            #                                                 (i.e. charging battery)
            ("usb_comm_cap",                c_uint32, 1),   # USB communications capable
            ("cap_mismatch",                c_uint32, 1),   # Set if the sink cannot satisfy its
            #                                                 power requirements from caps offered
            ("give_back",                   c_uint32, 1),   # Whether the sink will respond to
            #                                                 the GotoMin message
            ("object_position",             c_uint32, 4)]   # Index of source cap being requested
class FVRDO(ct.Union):
    _fields_ = [
        ("bits", FVRDO_bits),
        ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0


# PPS RDO description
# USB PD 3.1 Table 6-25
class PPSRDO_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("operating_current_50mA",      c_uint32, 7),   # Operating current in 50mA units
        ("reserved0",                   c_uint32, 2),   # Reserved
        ("operating_voltage_20mV",      c_uint32, 12),  # Requested voltage in 20mV units
        ("reserved1",                   c_uint32, 1),   # Reserved
        ("epr_mode_capable",            c_uint32, 1),   # Reserved
        ("unchunked_ext_msg_support",   c_uint32, 1),   # Reserved
        ("no_usb_suspend",              c_uint32, 1),   # Set when the sink wants to continue
        #                                                 the contract during USB suspend
        #                                                 (i.e. charging battery)
        ("usb_comm_capable",            c_uint32, 1),   # USB communications capable
        ("capability_mismatch",         c_uint32, 1),   # Set if the sink cannot satisfy its
        #                                                 power requirements from caps offered
        ("reserved2",                   c_uint32, 1),   # Reserved
        ("object_position",             c_uint32, 4)]   # Index of source cap being requested
class PPSRDO(ct.Union):
    _fields_ = [("bits", PPSRDO_bits),
        ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0

# AVS RDO description
# USB PD 3.1 Table 6-26
class AVSRDO_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("operating_current_50mA",      c_uint32, 7),   # Operating current in 50mA units
        ("reserved0",                   c_uint32, 2),   # Reserved
        ("output_voltage_25mV",         c_uint32, 12),  # Requested voltage in 25mV units, 
                                                        # least significant bits set to 0
                                                        # Making effective vout step size 100mV
        ("reserved1",                   c_uint32, 1),   # Reserved
        ("epr_mode_capable",            c_uint32, 1),   # Reserved
        ("unchunked_ext_msg_support",   c_uint32, 1),   # Reserved
        ("no_usb_suspend",              c_uint32, 1),   # Set when the sink wants to continue
        #                                                 the contract during USB suspend
        #                                                 (i.e. charging battery)
        ("usb_comm_capable",            c_uint32, 1),   # USB communications capable
        ("capability_mismatch",         c_uint32, 1),   # Set if the sink cannot satisfy its
        #                                                 power requirements from caps offered
        ("reserved2",                   c_uint32, 1),   # Reserved
        ("object_position",             c_uint32, 4)]   # Index of source cap being requested
class AVSRDO(ct.Union):
    _fields_ = [("bits", AVSRDO_bits),
        ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0


# UVDM object
class UVDM_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("vendor_defined",      c_uint32, 15),  # Defined by the vendor
        ("vdm_type",            c_uint32, 1),   # Unstructured or structured msg header
        ("vendor_id",           c_uint32, 16)]  # Unique 16-bit unsigned integer
        #                                         assigned by the USB-IF
class UVDM(ct.Union):
    _fields_ = [
        ("bits", UVDM_bits),
        ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0
        
class PI_UVDM_PACKET_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("pi_uvdm_length",              c_uint32, 5),  
        ("pi_uvdm_msg_type",            c_uint32, 3),   
        ("pi_rsvd",                     c_uint32, 4), 
        ("pi_request_response_bit",     c_uint32, 1),  
        ("pi_response_status",          c_uint32, 1),   
        ("pi_uvdm_read_write",          c_uint32, 1), 
        ("pi_uvdm_unstructured",        c_uint32, 1),  
        ("pi_uvdm_vid",                 c_uint32, 16)]  
class PI_UVDM_PACKET(ct.Union):
    _fields_ = [
        ("bits", PI_UVDM_PACKET_bits),
        ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0
        
class PI_UVDM_MEM_PACKET_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("pi_mem_addr",                 c_uint32, 16),  
        ("pi_mem_rsvd",                 c_uint32, 16)]  
class PI_UVDM_MEM_PACKET(ct.Union):
    _fields_ = [
        ("bits", PI_UVDM_MEM_PACKET_bits),
        ("asbyte", c_uint32)]
    def __init__(self):
        self.asbyte = 0