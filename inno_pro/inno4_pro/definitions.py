import ctypes as ct
from ctypes import c_uint32

class Inno4Pro_Parameters():
    CV_MAX_V = 24
    CV_MIN_V = 3
    CV_RESOLUTION_MV = 10
    
    VOUT_DAC_OFFSET_V = 5
    
    IS_MAX_MV = 32
    CC_MIN_COUNT = 29
    CC_MAX_COUNT = 192 
    
    OV_MAX_V = 25
    OV_MIN_V = 3.3
    OV_RESOLUTION_MV = 100
    
    UV_MAX_V = 24
    UV_MIN_V = 2.7
    UV_RESOLUTION_MV = 100
    
    CDC_MAX_MV = 600
    CDC_MIN_MV = 0
    CDC_RESOLUTION_MV = 50
    
    VKP_MAX_V = 24
    VKP_MIN_V = 5.3
    VKP_RESOLUTION_MV = 100
    
    LS1_THRESH_RESOLUTION_MV = 10
    LS1_MIN_THRESH_MV = 0
    LS1_MAX_THRESH_MV = 2550
    
    LS2_STEP_RESOLUTION_MV = 10
    LS2_MAX_STEP_MV = 150
    LS2_MIN_STEP_MV = 0
    LS2_MIN_THRESH_COUNT = 0
    LS2_MAX_THRESH_COUNT = 15
    
    FAST_CC_OFFSET_MIN_COUNT = 0
    FAST_CC_OFFSET_MAX_COUNT = 31
    SLOW_CC_OFFSET_MIN_COUNT = 0
    SLOW_CC_OFFSET_MAX_COUNT = 31

    TIMING_RESOLUTION_NS = 85
    

class Inno4Pro_I2C_Defaults():
    INNOPRO_SLAVE_ADDR  =   0x18      # InnoSwitch4-Pro I2C 7-bit Slave Address
    OMF_CC_MODE =           0b100     # Default OMF Readback for CC mode
    OMF_CP_MODE =           0b010     # Default OMF Readback for CP mode
    OMF_CV_MODE =           0b001     # Default OMF Readback for CV mode
    OMF_UNDEFINED =         0b000     #

    OMF_TEXT = {
        OMF_CC_MODE: 'CC',
        OMF_CP_MODE: 'CP',
        OMF_CV_MODE: 'CV'
    }
class Inno4Pro_I2C_Registers():
    
    FWD_PEAK_REG =          0x02        # FWD Peak Register
    WATCHDOG_REG =         	0x26        # Watchdog Register 
    VBEN_REG =              0x04        # Bus Switch Enable Register
    CV_REG =                0x10        # Constant Voltage Register
    BLEEDER_REG =           0x86        # Bleeder Register
    VDIS_REG =              0x08        # Strong Discharge Register
    TURN_OFF_PSU_REG =      0x8A        # Latch Off Register
    FAST_VI_REG =         	0x8C        # Fast VI Register
    CVO_REG =               0x0E        # Constant Voltage Only Register
    OVA_REG =               0x92        # Over-Voltage Threshold Register 
    UVA_REG =               0x94		# Under-Voltage Threshold Register
    CC_REG =                0x98        # Constant Current Register 
    VKP_REG =               0x1A        # Constant Output Power Knee Voltage Register
    CCSC_REG =              0x20		# Output Short Circuit Fault Detection Response Register 
    ISSC_REG =              0xA2		# IS-Pin Short Fault Response  and Detection Frequency Register
    VBUSSC_REG =          	0xB6        # Series BUS Switch Short Circuit Fault Register
    INT_MASK_REG =          0x2C        # Interrupt Mask Register
    OTP_REG =               0xAE        # Over-Temperature Fault Register
    FAST_CC_REG =           0xB0		# Constant Voltage Load / Fast CC Register
    LOOPSPEED_1_REG =       0x32        # Loop Speed 1 Register
    LOOPSPEED_2_REG =       0x34        # Loop Speed 2 Register
    DCM_ONLY_REG =          0xBA		# Discontinuous Conduction Mode Only
    CDC_REG =               0x16        # Cable Drop Compensation Register
    READ_CMD_REG =          0x80        # Readback command Register
    
    # Special Registers
    LOOP_OPTION_REG =       0x7C        # Loop option register (different from loop speed 1 & 2)
    LOCK_UNLOCK_SREG =      0x5E
    
class Inno4Pro_I2C_Readback_Registers():
    
    READ0 =         0x00		#  Revision ID   
    READ1 =         0x02		#  Output Voltage Set-Point   
    READ2 =         0x04		#  Constant Current Set-Point 
    READ3 =         0x06		#  Over-Voltage Threshold    
    READ4 =         0x08		#  Under-Voltage Threshold 
    READ5 =         0x0A		#  Constant Current and Constant Power Set-Point
    READ6 =         0x0C		#  OVL,UVL,CCSC,ISSC,UVLTIMER,WDTIMER,CVOL,CVTIMER	
    READ7 =         0x0E		#  FWDPK, VBEN, BLEEDER, Turn-Off, FAST VI, CVO MODE, OTP FAULT, CDC
    READ8 =         0x10        #  Instantaneous Measured current
    READ9 =         0x12		#  Instantaneous Measured Voltage  
    READ10 =        0x14		#  INNTERRUPT, CONTROL_S, VDIS_REG, HIGH_FSW, WRITE_AUTO_CV, OTP, VOUT2PCT, VOUT10PCT, ISSC, CCSC, VOUT_UV, VOUT_OV 
    READ11 =        0x16	    #  MODE (OMF)
    READ12 =        0x18		#  Average Measured Output Current                		
    READ13 =        0x1A		#  Average Measured Output Voltage   
    READ14 =        0x1C	    #  Voltage DAC Telemetry Register (DAC100mV, DAC10mV)
    READ16 =        0x20	    #  CVO_AR, ISSC_AR, CCSC_AR, VOUT_OV_AR, VOUT_UV_AT, PSU_OFF, CVOL_LO, Turn-OFF CMD, ISSC_LO, VOUT_OV_LO, VOUT_UV_LO, BPS_OV_LO
    READ17 =        0x22	    #  CTRL_S_MASK, LO_FAULT_MASK, CVOL_MASK, ISSC_MASK, CCSC_MASK, VOUT_UV_MASK, VOUT_OV_MASK, MODE_CHANGE, VBUS_SC, CONTROL_S, LO_FAULT, CVOL, ISSC, CCSC, VOUT_UV, VOUT_OV
    READ18 =        0x24	    #  SLOW_CC_OFFSET, FAST_CC_ENABLE, FAST_CC_OFFSET  
    READ19 =        0x26	    #  Loop Speed 1  Telemetry Register 
    READ20 =        0x28	    #  Loop Speed 2  Telemetry Register  
         
    READ_VOLT_DAC = 	    READ14     # Read Voltage DAC  Telemetry Register  
    READ_OMF_FLAG =         READ11     # Operating Mode Flag  
    
    READ_OV =               READ3      # OV Threshold
    READ_UV =               READ4      # UV Threshold
    READ_CDC =              READ7      # FWDPK, VBEN, BLEEDER, DISCHARGE, FAST VI, CVO MODE, OTP FAULT, CDC
    READ_VKP =              READ5      # VKP Setpoint

    
    READ_CV =               READ1      # Readback CV setpoint
    READ_CC =               READ2      # Readback CC setpoint

    READ_VOUT =            	READ9      # Read Voltage value
    READ_IOUT =            	READ8      # Measured Output Current 

    READ_VOUT_AVE =         READ13     # Read Average Output Voltage 
    READ_IOUT_AVE =         READ12     # Read Average Output Current 
    
    READ_LOOP_SPEED_1 =     READ19	    #  Loop Speed 1  Telemetry Register 
    READ_LOOP_SPEED_2 =     READ20	    #  Loop Speed 2  Telemetry Register
    
INNO4_PRO_SINGLE_BYTE_COMMAND_LIST = [
    Inno4Pro_I2C_Registers.FWD_PEAK_REG,
    Inno4Pro_I2C_Registers.WATCHDOG_REG, 
    Inno4Pro_I2C_Registers.VBEN_REG,
    Inno4Pro_I2C_Registers.BLEEDER_REG,
    Inno4Pro_I2C_Registers.VDIS_REG,
    Inno4Pro_I2C_Registers.TURN_OFF_PSU_REG,
    Inno4Pro_I2C_Registers.FAST_VI_REG,
    Inno4Pro_I2C_Registers.CVO_REG,
    Inno4Pro_I2C_Registers.CCSC_REG, 
    Inno4Pro_I2C_Registers.ISSC_REG,
    Inno4Pro_I2C_Registers.VBUSSC_REG,
    Inno4Pro_I2C_Registers.OTP_REG,
    Inno4Pro_I2C_Registers.DCM_ONLY_REG,
    Inno4Pro_I2C_Registers.CDC_REG,
]
  
INNO4_PRO_REG_LIST =[
    Inno4Pro_I2C_Registers.FWD_PEAK_REG,
    Inno4Pro_I2C_Registers.WATCHDOG_REG, 
    Inno4Pro_I2C_Registers.VBEN_REG,
    Inno4Pro_I2C_Registers.CV_REG,
    Inno4Pro_I2C_Registers.BLEEDER_REG,
    Inno4Pro_I2C_Registers.VDIS_REG,
    Inno4Pro_I2C_Registers.TURN_OFF_PSU_REG,
    Inno4Pro_I2C_Registers.FAST_VI_REG,
    Inno4Pro_I2C_Registers.CVO_REG,
    Inno4Pro_I2C_Registers.OVA_REG, 
    Inno4Pro_I2C_Registers.UVA_REG,
    Inno4Pro_I2C_Registers.CC_REG, 
    Inno4Pro_I2C_Registers.VKP_REG,
    Inno4Pro_I2C_Registers.CCSC_REG, 
    Inno4Pro_I2C_Registers.ISSC_REG,
    Inno4Pro_I2C_Registers.VBUSSC_REG,
    Inno4Pro_I2C_Registers.INT_MASK_REG,
    Inno4Pro_I2C_Registers.OTP_REG,
    Inno4Pro_I2C_Registers.FAST_CC_REG,
    Inno4Pro_I2C_Registers.LOOPSPEED_1_REG,
    Inno4Pro_I2C_Registers.LOOPSPEED_2_REG,
    Inno4Pro_I2C_Registers.DCM_ONLY_REG,
    Inno4Pro_I2C_Registers.CDC_REG,
    Inno4Pro_I2C_Registers.READ_CMD_REG,
    Inno4Pro_I2C_Registers.LOOP_OPTION_REG,
    ]  
    
INNO4_PRO_READBACK_REG_LIST =[
    Inno4Pro_I2C_Readback_Registers.READ0,
    Inno4Pro_I2C_Readback_Registers.READ1,
    Inno4Pro_I2C_Readback_Registers.READ2,
    Inno4Pro_I2C_Readback_Registers.READ3,
    Inno4Pro_I2C_Readback_Registers.READ4,
    Inno4Pro_I2C_Readback_Registers.READ5,
    Inno4Pro_I2C_Readback_Registers.READ6,
    Inno4Pro_I2C_Readback_Registers.READ7,
    Inno4Pro_I2C_Readback_Registers.READ8,
    Inno4Pro_I2C_Readback_Registers.READ9,
    Inno4Pro_I2C_Readback_Registers.READ10,
    Inno4Pro_I2C_Readback_Registers.READ11,
    Inno4Pro_I2C_Readback_Registers.READ12,
    Inno4Pro_I2C_Readback_Registers.READ13,
    Inno4Pro_I2C_Readback_Registers.READ14,
    Inno4Pro_I2C_Readback_Registers.READ16,
    Inno4Pro_I2C_Readback_Registers.READ17,
    Inno4Pro_I2C_Readback_Registers.READ18,
    Inno4Pro_I2C_Readback_Registers.READ19,
    Inno4Pro_I2C_Readback_Registers.READ20,
]


class Inno4Pro_I2C_Commands():    
    # FWD_PEAK
    FWD_PEAK_ENABLE =       0b1         # Enable FWD Peak (bit 0)
    FWD_PEAK_DISABLE =      0b0         # Disable FWD Peak (bit 0)
    
    FWD_PEAK_WINDOW_15_35_PCT = 0b11    # Set FWD Peak Window to 15% tO 35% (bit 1:2)
    FWD_PEAK_WINDOW_20_40_PCT = 0b10    # Set FWD Peak Window to 20% tO 40% (bit 1:2)
    FWD_PEAK_WINDOW_25_45_PCT = 0b01    # Set FWD Peak Window to 25% tO 45% (bit 1:2)
    FWD_PEAK_WINDOW_30_50_PCT = 0b00    # Set FWD Peak Window to 30% tO 50% (bit 1:2)
    
    FWD_PEAK_PRESHIFT_90NS = 0b11       # Set FW Peak Pre-shift to 90 ns (bit 3:4)
    FWD_PEAK_PRESHIFT_60NS = 0b10       # Set FW Peak Pre-shift to 60 ns (bit 3:4)
    FWD_PEAK_PRESHIFT_30NS = 0b01       # Set FW Peak Pre-shift to 30 ns (bit 3:4)
    FWD_PEAK_PRESHIFT_0NS = 0b00       # Set FW Peak Pre-shift to 0 ns (bit 3:4)
    
    FWD_PEAK_PARITY =       False       # Parity not needed for FWD_PEAK
    
    # VBEN
    VBEN_ON =               0b11        # Enable VBEN/Disable VDIS_REG bit(0:1)
    VBEN_OFF_NO_RST =       0b01        # Disable VBEN/No Reset bit(0:1)
    VBEN_OFF_RST =          0b00        # Disable VBEN/Reset bit(0:1)
    
    VBEN_READBACK_ON =      0b1         # Readback for VBEN enabled
    VBEN_READBACK_OFF =     0b0         # Readback for VBEN disabled
    
    VBEN_PARITY =           True        # Parity needed for VBEN
    
    # BLEEDER
    BLEEDER_OFF =           0b00        # Bleeder Disabled (bit 0:1)
    BLEEDER_ON =            0b01        # Bleeder Enabled without Auto Disable (bit 0:1)
    BLEEDER_ON_AUTO_DIS =   0b11        # Bleeder Enabled with Auto Disable (bit 0:1)
    
    # BLEEDER_VOUT10PCT =     0b00        # Bleeder Auto Disable set to VOUT10PCT (bit 2:3)
    # BLEEDER_VOUT4PCT =      0b01        # Bleeder Auto Disable set to VOUT4PCT (bit 2:3)
    WEAK_BLEEDER_ON =       0b1101      # Weak Bleeder Enabled (bit 4:7)
    WEAK_BLEEDER_OFF =      0b0000      # Weak Bleeder Enabled (bit 4:7)  
    
    BLEEDER_PARITY =        False       # Parity not needed for BLEEDER
    
    # VDIS
    VDIS_ON_NO_RST =        0b0010		# Enable Discharge/No Reset (bit 0:3)
    VDIS_ON_RST =           0b0011		# Enable Discharge/Disable VBEN/Reset (bit 0:3)
    VDIS_OFF =              0b1100		# Disable Discharge (bit 0:3)
    
    VDIS_PARITY =           True        # Parity Needed for VDIS

    # TURN_OFF_PSU
    TURN_OFF_PSU_ENABLED =  0b1         # Enable Latch-Off (bit 0)
    TURN_OFF_PSU_DISABLED = 0b0         # Disable Latch-Off (bit 0)
    
    TURN_OFF_PSU_PARITY =   False       # Parity not needed for TURN_OFF_PSU
    
    # FAST VI
    FASTVI_LIMIT_EN =       0b0		    # Fast VI Command Enable (bit 0)
    FASTVI_LIMIT_DIS =      0b1		    # Fast VI Command Disable (bit 0)
    
    FAST_VI_PARITY =        False       # Parity not needed for FAST VI
    
    # CVO
    CVO_CV_ONLY_MODE =      0x1         # CV Only Mode/No CC Regulation (bit 0)
    CVO_CV_CC_MODE =        0x0         # Both CV and CC Regulation (bit 0)

    CVO_RESP_DO	=           0b11        # Constant Voltage Only Fault Set to Disable Output (bit 1:2)
    CVO_RESP_AR =           0b10    	# Constant Voltage Only Fault Set to Auto-Restart (bit 1:2)
    CVO_RESP_LO	=           0b01        # Constant Voltage Only Fault Set to Latch-Off (bit 1:2)
    CVO_RESP_NR	=           0b00        # Constant Voltage Only Fault Set to No Response (bit 1:2)

    CVO_TIMER_64MS =        0b11		# Constant Voltage Only Fault Timer Set to 64ms (bit 3:4)
    CVO_TIMER_32MS =        0b10        # Constant Voltage Only Fault Timer Set to 32ms (bit 3:4)
    CVO_TIMER_16MS =        0b01		# Constant Voltage Only Fault Timer Set to 16ms (bit 3:4)
    CVO_TIMER_8MS  =        0b00		# Constant Voltage Only Fault Timer Set to 8ms (bit 3:4)
    
    CVO_PARITY =            False       # Parity not needed for CVO
    
    # CV
    CV_REG_DEFAULT =        500         # Default CV value (5V)
    CV_REG_DEFAULT_LSB =    0b1110100   # LSB of Default Voltage (5V) (bit 0:6) 
    CV_REG_DEFAULT_MSB =    0b00011     # MSB of Default Voltage (5V) (bit 8:12)  
    
    CV_AUTO_UV_OV_ENABLED = 0b1         # Enable auto set of UVA, OVA in CVO mode (bit 13)
    CV_AUTO_UV_OV_DISABLED= 0b0         # Disable auto set of UVA, OVA in CVO mode (bit 13)
    
    CV_PARITY =             True        # Parity Needed for CV
    
    # OVA
    OVA_RESP_DO =           0b11		# Overvoltage Fault Response Set to Disable Output (bit 9:10)
    OVA_RESP_AR =           0b10		# Overvoltage Fault Response Set to Auto-Restart (bit 9:10)
    OVA_RESP_LO	=           0b01        # Overvoltage to Latch Off (bit 9:10)
    OVA_RESP_NR	=           0b00        # Overvoltage to NO Response (bit 9:10)
    
    OVA_PARITY =            True        # Parity Needed for OVA
    
    # UVA
    UVA_RESP_DO =           0b11		# Undervoltage Fault Response Set to Disable Output (bit 9:10)
    UVA_RESP_AR =           0b10		# Undervoltage Fault Response Set to Auto-Restart (bit 9:10)
    UVA_RESP_LO	=           0b01        # Under-Voltage to Latch Off (bit 9:10)
    UVA_RESP_NR	=           0b00        # Under-Voltage to NO Response (bit 9:10)
    
    UVA_TIMER_64MS =        0b11	    # Undervoltage Fault Timer Set to 64ms (bit 11:12)
    UVA_TIMER_32MS =        0b10		# Undervoltage Fault Timer Set to 32ms (bit 11:12)
    UVA_TIMER_16MS =        0b01		# Undervoltage Fault Timer Set to 16ms (bit 11:12)
    UVA_TIMER_8MS =         0b00		# Undervoltage Fault Timer Set to 8ms (bit 11:12)   
    
    UVA_PARITY =            True        # Parity Needed for UVA
    
    # CDC
    CDC_VAL_0mV =            0b00       # CDC Value 0 mV (bit 0:3)
    CDC_VAL_50mV =           0x01       # CDC Value 50 mV (bit 0:3)
    CDC_VAL_100mV =          0x02       # CDC Value 100 mV (bit 0:3)
    CDC_VAL_150mV =          0x03       # CDC Value 150 mV (bit 0:3)
    CDC_VAL_200mV =          0x04       # CDC Value 200 mV (bit 0:3)
    CDC_VAL_250mV =          0x05       # CDC Value 250 mV (bit 0:3)
    CDC_VAL_300mV =          0x06       # CDC Value 300 mV (bit 0:3)
    CDC_VAL_350mV =          0x07       # CDC Value 350 mV (bit 0:3)
    CDC_VAL_400mV =          0x08       # CDC Value 400 mV (bit 0:3)
    CDC_VAL_450mV =          0x09       # CDC Value 450 mV (bit 0:3)
    CDC_VAL_500mV =          0x0A       # CDC Value 500 mV (bit 0:3)
    CDC_VAL_550mV =          0x0B       # CDC Value 550 mV (bit 0:3)
    CDC_VAL_600mV =          0x0C       # CDC Value 600 mV (bit 0:3)
    
    CDC_PARITY =             False      # Parity not needed for CDC
    
    # CC
    CC_MAX_LSB =             192        # Max CC LSB Request
    CC_MIN_LSB =             29         # Min CC LSB Request
    
    CC_PARITY =              True       # Parity needed for CC
    
    # CCSC
    CCSC_RESP_DO =           0b11       # Output Short Circuit Fault Set to Disable Output (bit 0:1)
    CCSC_RESP_AR =           0b10		# Output Short Circuit Fault Set to Auto Restart (bit 0:1)
    CCSC_RESP_LO =           0b01		# Output Short Circuit Fault Set to Latch Off (bit 0:1)
    CCSC_RESP_NR =           0b00		# Output Short Circuit Fault Set to No Response (bit 0:1)
    
    CCSC_PARITY =            False      # Parity not needed for CCSC
    
    # ISSC
    
    ISSC_RESP_48_NR_60KHZ =  0x30	    # IS-Pin Short Set to No Response and 60Khz Frequency -Default 
    ISSC_RESP_48_AR_60KHZ =  0x32		# IS-Pin Short Set to Auto Restart and 60Khz Frequency -Default 

    ISSC_RESP_DO =           0b11		# ISSC Fault Response Set to Disable Output (bit 0:1)
    ISSC_RESP_AR =           0b10		# ISSC Fault Response Set to Auto Restart (bit 0:1)
    ISSC_RESP_LO =           0b01		# ISSC Fault Response Set to Latch Off (bit 0:1)
    ISSC_RESP_NR =           0b00		# ISSC Fault Response Set to No Response (bit 0:1)

    ISSC_FREQ_120KHZ =       0b11		# ISSC Frequency Detection Threshold Set to 120 Khz (bit 2:3)
    ISSC_FREQ_90KHZ =        0b10		# ISSC Frequency Detection Threshold Set to 90 Khz (bit 2:3)
    ISSC_FREQ_30KHZ =        0b01		# ISSC Frequency Detection Threshold Set to 30 Khz (bit 2:3)
    ISSC_FREQ_60KHZ =        0b00		# ISSC Frequency Detection Threshold Set to 60 Khz (bit 2:3)

    ISSC_CC_LIMIT_112 =      0b111		# ISSC Current Limit Set to 112 (bit 4:6) 
    ISSC_CC_LIMIT_96 =       0b110		# ISSC Current Limit Set to 96 (bit 4:6)
    ISSC_CC_LIMIT_80 =       0b101		# ISSC Current Limit Set to 80 (bit 4:6)
    ISSC_CC_LIMIT_64 =       0b100		# ISSC Current Limit Set to 64 (bit 4:6)
    ISSC_CC_LIMIT_48 =       0b011		# ISSC Current Limit Set to 48 (bit 4:6)
    ISSC_CC_LIMIT_32 =       0b010		# ISSC Current Limit Set to 32 (bit 4:6)
    ISSC_CC_LIMIT_16 =       0b001		# ISSC Current Limit Set to 16 (bit 4:6)
    ISSC_CC_LIMIT_00 =       0b000      # ISSC Current Limit Set to 0 (bit 4:6)
    
    ISSC_PARITY =            False      # Parity not needed for ISSC
    
    # WATCHDOG
    WATCHDOG_OFF =           0b00		# Watchdog Timer Set to 0 sec (bit 0:1)
    WATCHDOG_500MS =         0b01		# Watchdog Timer Set to 0.5 sec (bit 0:1)
    WATCHDOG_1000MS =        0b10		# Watchdog Timer Set to 1 sec (bit 0:1)
    WATCHDOG_2000MS =        0b11		# Watchdog Timer Set to 2 sec (bit 0:1)
    
    WATCHDOG_PARITY =        False      # Parity not needed for WATCHDOG
    
    # OTP
    OTP_60DEGC =             0b1        # Set OTP limit to 60 C (bit 0)
    OTP_40DEGC =             0b0        # Set OTP limit to 40 C(bit 0)
    
    OTP_PARITY =             False      # Parity not needed for OTP
    
    # VBUSSC
    VBUSSC_RESP_DO =      0b11		# Series BUS Switch Short Fault Response to Disable Output (bit 0:1)
    VBUSSC_RESP_AR =      0b10		# Series BUS Switch Short Fault Response to Disable Output (bit 0:1)
    VBUSSC_RESP_LO =      0b01		# Series BUS Switch Short Fault Response to Disable Output (bit 0:1)
    VBUSSC_RESP_NR =      0b00		# Series BUS Switch Short Fault Response to Disable Output (bit 0:1)
    
    VBUSSC_SAMPLE_4 =      0b11		# Series BUS Switch Short Isense Samples  4 (bit 2:3)
    VBUSSC_SAMPLE_3 =      0b10		# Series BUS Switch Short Isense Samples  3 (bit 2:3)
    VBUSSC_SAMPLE_2 =      0b01		# Series BUS Switch Short Isense Samples  2 (bit 2:3)
    VBUSSC_SAMPLE_1 =      0b00		# Series BUS Switch Short Isense Samples  1 (bit 2:3)

    VBUSSC_IS_VAL_72 =       0b11		# Series BUS Switch Short Isense Threshold  72 (bit 4:5)
    VBUSSC_IS_VAL_64 =       0b10		# Series BUS Switch Short Isense Threshold  64 (bit 4:5)
    VBUSSC_IS_VAL_32 =       0b01		# Series BUS Switch Short Isense Threshold  32 (bit 4:5)
    VBUSSC_IS_VAL_48 =       0b00		# Series BUS Switch Short Isense Threshold  48 (bit 4:5)
    
    VBUSSC_PARITY =          False      # Parity nit needed for VBUSSC
    
    # DCM_ONLY
    DCM_ONLY_THRESHOLD_50MV =0b00       #Set DCM Only Threshold to 50 mV (bit 0:1)
    DCM_ONLY_THRESHOLD_25MV =0b01       #Set DCM Only Threshold to 25 mV (bit 0:1)
    DCM_ONLY_THRESHOLD_100MV=0b10       #Set DCM Only Threshold to 100 mV (bit 0:1)
    DCM_ONLY_THRESHOLD_75MV =0b11       #Set DCM Only Threshold to 75 mV (bit 0:1)
    
    DCM_ONLY_DISABLE =       0b0        # Discontinuous Conduction Mode Only  DISABLED (bit 2)
    DCM_ONLY_ENABLE =        0b1        # Discontinuous Conduction Mode Only  ENABLED (bit 2) 
    
    DCM_ONLY_PARITY =        False      # Parity not needed for DCM Only

    # FAST_CC
    
    FAST_CC_ENABLED =        0b1        # Fast CC Enabled (bit 5)
    FAST_CC_DISABLED =       0b0        # Fast CC Disabled (bit 5)
    
    SLOW_CC_ENABLED =        0b0        # Slow CC Enabled (bit 6)
    SLOW_CC_DISABLED =       0b1        # Slow CC Disabled (bit 6)
    
    CVLOAD_DEFAULT_MSB =     0x00		# MSB of Constant Voltage Load Default Settings
    CVLOAD_DEFAULT_LSB =     0x1F		# LSB of Constant Voltage Load Default Settings
    
    CVLOAD_RECOMMENDED =     0x0A		# MSB ofConstant Voltage Load Recommended Settings
    CVLOAD_RECOMMENDED =     0x20		# LSB ofConstant Voltage Load Recommended Settings
    
    FAST_CC_PARITY =         False      # Parity not needed for FAST_CC
    
    # LOOP SPEED 1 & 2

    LOOPSPEED_1_LSB_DEFAULT =      	0x0A    # LSB For Default Loop Speed 1 Settings
    LOOPSPEED_1_MSB_DEFAULT =      	0x14    # MSB For Default Loop Speed 1 Settings

    VST_LOOPSPEED_2_LSB =      	  	0x40    # LSB For Default Loop Speed 2 Settings at CV mode
    VST_LOOPSPEED_2_MSB =      	  	0x2F    # MSB For Default Loop Speed 2 Settings at CV mode

    CLT_LOOPSPEED_2_LSB =      	  	0x32    # LSB For Default Loop Speed 1 Settings at CC mode and Vout > 11 V and CC request < 1 A
    CLT_LOOPSPEED_2_MSB =      	  	0x1F    # MSB For Default Loop Speed 1 Settings at CC mode and Vout > 11 V and CC request < 1 A
    
    CLT_LOOPSPEED_2_LSB_LOW_VOLT = 	0x84    # LSB For Default Loop Speed 1 Settings at CC mode and Vout < 8 V
    CLT_LOOPSPEED_2_MSB_LOW_VOLT = 	0x18    # MSB For Default Loop Speed 1 Settings at CC mode and Vout < 8 V
    
    LOOPSPEED_2_LSB_DEFAULT	=  		0x84    # LSB For Default Loop Speed 2 Settings at CC mode
    LOOPSPEED_2_MSB_DEFAULT	=  		0x18    # MSB For Default Loop Speed 2 Settings at CC mode

    LOOPSPEED_PARITY =       False
    
    # LOCK/UNLOCK SREG
    
    UNLOCK_SREG_1_MSB =      0x20
    UNLOCK_SREG_1_LSB =      0x16
    UNLOCK_SREG_2_MSB =      0x12
    UNLOCK_SREG_2_LSB =      0x34
    
    LOCK_SREG_1_MSB =        0x20
    LOCK_SREG_1_LSB =        0x16
    LOCK_SREG_2_MSB =        0xAB
    LOCK_SREG_2_LSB =        0xCD
    
    # LOOP OPTION
    LOOP_OPTION_DEF_LSB =    0x96           # LSB of Default Loop Option
    LOOP_OPTION_DEF_MSB =    0x07           # MSB of Default Loop Option
    
    LOOP_OPTION1_LSB =       0xAA           # LSB of Loop Option 1
    LOOP_OPTION1_MSB =       0x07           # MSB of Loop Option 1
    
    LOOP_OPTION2_LSB =       0xB2           # LSB of Loop Option 2
    LOOP_OPTION2_MSB =       0x07           # MSB of Loop Option 2
         

# COMMAND REGISTERS FOR INNO4-PRO

class CV_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("vout_low_byte",               c_uint32, 7),  
        ("lowbyte_parity",              c_uint32, 1),
        ("vout_high_byte",              c_uint32, 5),
        ("auto_cv",                     c_uint32, 1),   
        ("reserved",                    c_uint32, 1),  
        ("highbyte_parity",             c_uint32, 1)]   
class CV(ct.Union):
    _fields_ = [("bits", CV_bits),
                ("asbyte", c_uint32)]
    
class CC_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("iout_low_byte",               c_uint32, 7),  
        ("lowbyte_parity",              c_uint32, 1),
        ("iout_high_byte",              c_uint32, 1),
        ("reserved",                    c_uint32, 6), 
        ("highbyte_parity",             c_uint32, 1)]   
    
class CC(ct.Union):
    _fields_ = [("bits", CC_bits),
                ("asbyte", c_uint32)]
    
class VKP_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("vkp_low_byte",                c_uint32, 7),  
        ("lowbyte_parity",              c_uint32, 1),
        ("vkp_high_byte",               c_uint32, 1),
        ("reserved",                    c_uint32, 6), 
        ("highbyte_parity",             c_uint32, 1)]   
    
class VKP(ct.Union):
    _fields_ = [("bits", VKP_bits),
                ("asbyte", c_uint32)]


class OVA_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("thresh_low_byte",             c_uint32, 7),
        ("lowbyte_parity",              c_uint32, 1),
        ("thresh_high_byte",            c_uint32, 1),
        ("response",                    c_uint32, 2),
        ("reserved",                    c_uint32, 4),   
        ("highbyte_parity",             c_uint32, 1)]  
class OVA(ct.Union):
    _fields_ = [("bits", OVA_bits),
                ("asbyte", c_uint32)]

class UVA_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("thresh_low_byte",             c_uint32, 7),
        ("lowbyte_parity",              c_uint32, 1),
        ("thresh_high_byte",            c_uint32, 1),
        ("response",                    c_uint32, 2),
        ("timer",                       c_uint32, 2),
        ("reserved",                    c_uint32, 2),   
        ("highbyte_parity",             c_uint32, 1)]
class UVA(ct.Union):
    _fields_ = [("bits", UVA_bits),
                ("asbyte", c_uint32)]
    
class CDC_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("cdc_low_byte",                c_uint32, 4),
        ("reserved",                    c_uint32, 12)]
class CDC(ct.Union):
    _fields_ = [("bits", CDC_bits),
                ("asbyte", c_uint32)]
    
class VBEN_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("vben_enable",                 c_uint32, 2),
        ("reserved2",                   c_uint32, 5),
        ("lowbyte_parity",              c_uint32, 1),
        ("reserved",                    c_uint32, 7),
        ("highbyte_parity",             c_uint32, 1)]
class VBEN(ct.Union):
    _fields_ = [("bits", VBEN_bits),
                ("asbyte", c_uint32)]
    
class BLEEDER_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("bleeder_enable",              c_uint32, 2),
        ("reserved2",                   c_uint32, 2),
        ("weak_bleeder_enable",         c_uint32, 4),
        ("reserved",                    c_uint32, 8)]
class BLEEDER(ct.Union):
    _fields_ = [("bits", BLEEDER_bits),
                ("asbyte", c_uint32)]
    
class VDIS_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("discharge_setting",           c_uint32, 4),
        ("reserved2",                   c_uint32, 3),
        ("lowbyte_parity",              c_uint32, 1),
        ("reserved",                    c_uint32, 7),
        ("highbyte_parity",             c_uint32, 1)]
class VDIS(ct.Union):
    _fields_ = [("bits", VDIS_bits),
                ("asbyte", c_uint32)]

class TURN_OFF_PSU_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("latch_off_enable",            c_uint32, 1),
        ("reserved",                    c_uint32, 15)]
class TURN_OFF_PSU(ct.Union):
    _fields_ = [("bits", TURN_OFF_PSU_bits),
                ("asbyte", c_uint32)]
    
class FWD_PEAK_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("enable",                      c_uint32, 1),
        ("window",                      c_uint32, 2),
        ("pre_shift",                   c_uint32, 2),
        ("reserved",                    c_uint32, 11)]
class FWD_PEAK(ct.Union):
    _fields_ = [("bits", FWD_PEAK_bits),
                ("asbyte", c_uint32)]
    
class WATCHDOG_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("timer",                       c_uint32, 2),
        ("reserved",                    c_uint32, 14)]
class WATCHDOG(ct.Union):
    _fields_ = [("bits", WATCHDOG_bits),
                ("asbyte", c_uint32)]
    
class FAST_VI_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("enable",                      c_uint32, 1),
        ("reserved",                    c_uint32, 15)]
class FAST_VI(ct.Union):
    _fields_ = [("bits", FAST_VI_bits),
                ("asbyte", c_uint32)]
    
class CVO_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("cvo_enable",                  c_uint32, 1),
        ("response",                    c_uint32, 2),
        ("timer",                       c_uint32, 2),
        ("reserved",                    c_uint32, 11)]
class CVO(ct.Union):
    _fields_ = [("bits", CVO_bits),
                ("asbyte", c_uint32)]
    
class CCSC_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("response",                    c_uint32, 2),
        ("reserved",                    c_uint32, 14)]
class CCSC(ct.Union):
    _fields_ = [("bits", CCSC_bits),
                ("asbyte", c_uint32)]
    
class ISSC_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("response",                    c_uint32, 2),
        ("freq",                        c_uint32, 2),
        ("thresh",                      c_uint32, 3),
        ("reserved",                    c_uint32, 9)]
class ISSC(ct.Union):
    _fields_ = [("bits", ISSC_bits),
                ("asbyte", c_uint32)]    
    
class VBUSSC_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("response",                    c_uint32, 2),
        ("num_samples",                 c_uint32, 2),
        ("thresh",                      c_uint32, 2),
        ("reserved",                    c_uint32, 10)]
class VBUSSC(ct.Union):
    _fields_ = [("bits", VBUSSC_bits),
                ("asbyte", c_uint32)]       

class INT_MASK_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("ov",                          c_uint32, 1),
        ("uv",                          c_uint32, 1),
        ("ccsc",                        c_uint32, 1),
        ("issc",                        c_uint32, 1),
        ("cvol",                        c_uint32, 1),
        ("latch_off",                   c_uint32, 1),
        ("control_s",                   c_uint32, 1),
        ("vbussc",                      c_uint32, 1),
        ("omf",                         c_uint32, 1),
        ("reserved",                    c_uint32, 7)]
class INT_MASK(ct.Union):
    _fields_ = [("bits", INT_MASK_bits),
                ("asbyte", c_uint32)]    
    
class OTP_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("hysteresis",                  c_uint32, 1),
        ("reserved",                    c_uint32, 15)]
class OTP(ct.Union):
    _fields_ = [("bits", OTP_bits),
                ("asbyte", c_uint32)]   
    
class FAST_CC_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("fast_cc_offset",              c_uint32, 5),
        ("fast_cc_enable",              c_uint32, 1),
        ("calibration_disable",         c_uint32, 1),
        ("reserved0",                   c_uint32, 1),
        ("slow_cc_offset",              c_uint32, 5),
        ("reserved1",                   c_uint32, 3)]
class FAST_CC(ct.Union):
    _fields_ = [("bits", FAST_CC_bits),
                ("asbyte", c_uint32)]

class LOOPSPEED_1_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("cv_small_step_thresh",        c_uint32, 8),
        ("cv_large_step_thresh",        c_uint32, 8)]
class LOOPSPEED_1(ct.Union):
    _fields_ = [("bits", LOOPSPEED_1_bits),
                ("asbyte", c_uint32)]    
  
class LOOPSPEED_2_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("cc_small_step_thresh",        c_uint32, 4),
        ("cc_large_step_thresh",        c_uint32, 4),
        ("large_step_size",             c_uint32, 4),
        ("small_step_size",             c_uint32, 4)]
class LOOPSPEED_2(ct.Union):
    _fields_ = [("bits", LOOPSPEED_2_bits),
                ("asbyte", c_uint32)]
    
class DCM_ONLY_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("thresh",                      c_uint32, 2),
        ("enable",                      c_uint32, 1),
        ("reserved",                    c_uint32, 13)]
class DCM_ONLY(ct.Union):
    _fields_ = [("bits", DCM_ONLY_bits),
                ("asbyte", c_uint32)]  

class READBACK_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("high_readback_register",      c_uint32, 7),
        ("lowbyte_parity",              c_uint32, 1),
        ("low_readback_register",       c_uint32, 7),
        ("highbyte_parity",             c_uint32, 1)]
class READBACK(ct.Union):
    _fields_ = [("bits", READBACK_bits),
                ("asbyte", c_uint32)]
    
# READBACK REGISTERS FOR INNO4_PRO

# READ0 - Unknown
class READ0_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("reserved",                c_uint32, 16)]
class READ0(ct.Union):
    _fields_ = [("bits", READ0_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16

# READ1 - Output Voltage Set-Point
class READ1_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("low_byte",                c_uint32, 7),
        ("lowbyte_parity",          c_uint32, 1),
        ("high_byte",               c_uint32, 5),
        ("reserved",                c_uint32, 2),
        ("highbyte_parity",         c_uint32, 1)]
class READ1(ct.Union):
    _fields_ = [("bits", READ1_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16

# READ2 - Output Current Set-Point
class READ2_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("low_byte",                c_uint32, 7),
        ("lowbyte_parity",          c_uint32, 1),
        ("high_byte",               c_uint32, 1),
        ("reserved",                c_uint32, 6),
        ("highbyte_parity",         c_uint32, 1)]
class READ2(ct.Union):
    _fields_ = [("bits", READ2_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16

# READ3 - Overvoltage Threshold
class READ3_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("low_byte",                c_uint32, 7),
        ("lowbyte_parity",          c_uint32, 1),
        ("high_byte",               c_uint32, 5),
        ("reserved",                c_uint32, 2),
        ("highbyte_parity",         c_uint32, 1)] 
class READ3(ct.Union):
    _fields_ = [("bits", READ3_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16

# READ4 - Undervoltage Threshold
class READ4_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("low_byte",                c_uint32, 7),
        ("lowbyte_parity",          c_uint32, 1),
        ("high_byte",               c_uint32, 5),
        ("reserved",                c_uint32, 2),
        ("highbyte_parity",         c_uint32, 1)] 
class READ4(ct.Union):
    _fields_ = [("bits", READ4_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16

# READ5 - CC and VKP setpoint
class READ5_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("vkp_setpoint",            c_uint32, 8),
        ("cc_setpoint",             c_uint32, 8)]
class READ5(ct.Union):
    """VKP Setpoint"""
    _fields_ = [("bits", READ5_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16
    
# READ6 - Fault Settings
class READ6_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("cvo_timer",               c_uint32, 2),
        ("cvo_response",            c_uint32, 2),
        ("wd_timer",                c_uint32, 2),
        ("uva_timer",               c_uint32, 2),
        ("issc_response",           c_uint32, 2),
        ("ccsc_response",           c_uint32, 2),
        ("uva_response",            c_uint32, 2),
        ("ova_response",            c_uint32, 2)]
class READ6(ct.Union):
    """Fault Settings"""
    _fields_ = [("bits", READ6_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16
    
# READ7 - 
class READ7_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("cdc",                     c_uint32, 4),
        ("reserved0",               c_uint32, 5),
        ("otp_hysteresis",          c_uint32, 1),
        ("cvo",                     c_uint32, 1),
        ("fstvic",                  c_uint32, 1),
        ("psu_off",                 c_uint32, 1),
        ("bleeder",                 c_uint32, 1),
        ("vben",                    c_uint32, 1),
        ("reserved1",               c_uint32, 1)]
class READ7(ct.Union):
    _fields_ = [("bits", READ7_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16
    
# READ8 - Measured Output Current
class READ8_bits(ct.LittleEndianStructure):
    """Instantaneous Measured Output Current"""
    _fields_ = [
        ("low_byte",                c_uint32, 7),
        ("lowbyte_parity",          c_uint32, 1),
        ("high_byte",               c_uint32, 1),
        ("reserved",                c_uint32, 6),
        ("highbyte_parity",         c_uint32, 1)] 
class READ8(ct.Union):
    _fields_ = [("bits", READ8_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16
    
# READ9 - Measured Output Voltage
class READ9_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("output_voltage",          c_uint32, 12),
        ("reserved0",               c_uint32, 4)]
class READ9(ct.Union):
    """Instantaneous Measured Output Voltage"""
    _fields_ = [("bits", READ9_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16
    
# READ10 - 0x14
class READ10_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("reg_vout_ov",             c_uint32, 1),   # Output OV Fault Comparator
        ("reg_vout_uv",             c_uint32, 1),   # Output UV Fault comparator
        ("reg_ccsc",                c_uint32, 1),   # Output short-circuit detected
        ("reg_issc",                c_uint32, 1),   # IS-pin short circuit detected
        ("reg_vout10pct",           c_uint32, 1),   # VOUTADC > 1.1*Vout
        ("reg_voutwk",              c_uint32, 1),   # Weak bleeder enabled?
        ("reserved1",               c_uint32, 3),
        ("reg_otp",                 c_uint32, 1),   # OTP Fault?    
        ("reg_cv_en",               c_uint32, 1),   # AutoCV Enabled?
        ("reserved0",               c_uint32, 1),
        ("reg_high_fsw",            c_uint32, 1),   # Switching Frequency High?
        ("reg_vdis",                c_uint32, 1),   # Output Discharge
        ("reg_control_s",           c_uint32, 1),   # System Ready Signal
        ("reg_interrupt_en",        c_uint32, 1)]  # Interrupt Enable
class READ10(ct.Union):
    _fields_ = [("bits", READ10_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16
    
# READ11 - 0x16 - Operating Mode Flag
class READ11_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("cv_mode",                 c_uint32, 1),   
        ("cp_mode",                 c_uint32, 1),   
        ("cc_mode",                 c_uint32, 1),
        ("reserved0",               c_uint32, 13)]
class READ11(ct.Union):
    """Operating Mode Flag"""
    _fields_ = [("bits", READ11_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16

# READ12 - 0x18 - Average Output Current
class READ12_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("average_iout",            c_uint32, 8),
        ("reserved0",               c_uint32, 8)]
class READ12(ct.Union):
    """16 sample Average Output Current"""
    _fields_ = [("bits", READ12_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16

# READ13 - 0x1A - Average Output Voltage
class READ13_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("average_vout",            c_uint32, 12),
        ("reserved0",               c_uint32, 4)]   
class READ13(ct.Union):
    """16 sample Average Output Voltage"""
    _fields_ = [("bits", READ13_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16

# READ14 - 0x1C - Voltage DAC
class READ14_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("dac_10mV",                 c_uint32, 8),
        ("dac_100mV",                c_uint32, 8)]   
class READ14(ct.Union):
    """DAC Voltage"""
    _fields_ = [("bits", READ14_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16
    
# READ16 - 0x20 - 
class READ16_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("reg_lo_bps_ov",           c_uint32, 1),
        ("reg_lo_vout_uv",          c_uint32, 1),
        ("reg_lo_vout_ov",          c_uint32, 1),
        ("reserved2",               c_uint32, 1),
        ("reg_lo_issc",             c_uint32, 1),
        ("reg_psuoff",              c_uint32, 1),
        ("reg_lo_cvo",              c_uint32, 1),
        ("reg_lo_fault",            c_uint32, 1),
        ("reserved1",               c_uint32, 1),
        ("reg_ar_vout_uv",          c_uint32, 1),
        ("reg_ar_vout_ov",          c_uint32, 1),
        ("reg_ar_ccsc",             c_uint32, 1),
        ("reg_ar_issc",             c_uint32, 1),
        ("reserved0",               c_uint32, 2),
        ("reg_ar_cvo",              c_uint32, 1)]
class READ16(ct.Union):
    """Auto Restart and Latch off Fault bits"""
    _fields_ = [("bits", READ16_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16
        
# READ17 - 0x22 - 
class READ17_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("ov_int_status",           c_uint32, 1),
        ("uv_int_status",           c_uint32, 1),
        ("ccsc_int_status",         c_uint32, 1),
        ("issc_int_status",         c_uint32, 1),
        ("cvo_ar_int_status",       c_uint32, 1),
        ("lo_fault_int_status",     c_uint32, 1),
        ("control_s_int_status",    c_uint32, 1),
        ("vbussc_int_status",       c_uint32, 1),
        ("omf_int_status",          c_uint32, 1),
        ("ov_int_mask",             c_uint32, 1),
        ("uv_int_mask",             c_uint32, 1),
        ("ccsc_int_mask",           c_uint32, 1),
        ("issc_int_mask",           c_uint32, 1),
        ("cvo_ar_int_mask",         c_uint32, 1),
        ("lo_fault_int_mask",       c_uint32, 1),
        ("control_s_int_mask",      c_uint32, 1)]
class READ17(ct.Union):
    """Interrupt mask and status bits"""
    _fields_ = [("bits", READ17_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16

# READ18 - 0x24 - 
class READ18_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("fast_cc_offset",              c_uint32, 5),
        ("fast_cc_enable",              c_uint32, 1),
        ("reserved",                    c_uint32, 2),
        ("slow_cc_offset",              c_uint32, 5),
        ("reserved1",                   c_uint32, 3)]
        
class READ18(ct.Union):
    """Fast CC Readback"""
    _fields_ = [("bits", READ18_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16
        
# READ19 - 0x26 - 
class READ19_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("cv_small_step_thresh",        c_uint32, 8),
        ("cv_large_step_thresh",        c_uint32, 8)]
        
class READ19(ct.Union):
    """Loop Speed 1 Readback"""
    _fields_ = [("bits", READ19_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16
        
# READ20 - 0x28 - 
class READ20_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("cc_small_step_thresh",        c_uint32, 4),
        ("cc_large_step_thresh",        c_uint32, 4),
        ("large_step_size",             c_uint32, 4),
        ("small_step_size",             c_uint32, 4)]
        
class READ20(ct.Union):
    """Loop Speed 2 Readback"""
    _fields_ = [("bits", READ20_bits),
                ("asbyte", c_uint32)]
    def __init__(self, u16=0):
        self.asbyte=u16

