from inno_pro.inno4_pro.definitions import *
from inno_pro.inno4_pro.functions import *
from inno_pro.inno4_pro.controller import *
from page_controls.definitions import *
from misc_functions.misc_functions import *
from inno_pro.functions import *
from inno_pro.definitions import *

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

params = Inno4Pro_Parameters
commands = Inno4Pro_I2C_Commands
defaults = Inno4Pro_I2C_Defaults

page_name = "i2c_controls"

class INNO4_I2C_RESPONSE():
    AR = 'Auto-Restart'
    LO = 'Latch-Off'
    DO = 'Disable Output'
    NR = 'No Response'
    
class INNO4_I2C_TIMER():
    TIMER_8MS   = '8 ms Timer'
    TIMER_16MS  = '16 ms Timer'
    TIMER_32MS  = '32 ms Timer'
    TIMER_64MS  = '64 ms Timer'
    

class INNO4_I2C_CDC_VALUES():
    CDC_0MV = '0 mV'
    CDC_50MV = '50 mV'
    CDC_100MV = '100 mV'
    CDC_150MV = '150 mV'
    CDC_200MV = '200 mV'
    CDC_250MV = '250 mV'
    CDC_300MV = '300 mV'
    CDC_350MV = '350 mV'
    CDC_400MV = '400 mV'
    CDC_450MV = '450 mV'
    CDC_500MV = '500 mV'
    CDC_550MV = '550 mV'
    CDC_600MV = '600 mV'
    
class INNO4_I2C_VBEN_OPTIONS():
    VBEN_ENABLE = 'Enabled'
    VBEN_DISABLE_RESET = 'Dis/Rst'
    VBEN_DISABLE_NO_RESET = 'Dis/No Rst'
    
class INNO4_I2C_BLEEDER_OPTIONS():
    BLEEDER_OFF = 'Bleeder OFF'
    BLEEDER_ON = 'Bleeder ON'
    BLEEDER_ON_AUTO_DIS = 'Bleeder ON, Auto-Disable'
    AUTO_DIS_THRESH_4PCT = 'VOUT4PCT Threshold'
    AUTO_DIS_THRESH_10PCT = 'VOUT10PCT Threshold'

class INNO4_I2C_WATCHDOG_OPTIONS():
    WATCHDOG_OFF = 'Timer OFF'
    WATCHDOG_500MS = '0.5s Timer'
    WATCHDOG_1000MS = '1s Timer'
    WATCHDOG_2000MS = '2s Timer'

class INNO4_I2C_ISSC_OPTIONS():
    THRESHOLD_BIT_00 = f'0 ({round(0/params.CC_MAX_COUNT*params.IS_MAX_MV,1):g} mV) Threshold'
    THRESHOLD_BIT_16 = f'16 ({round(16/params.CC_MAX_COUNT*params.IS_MAX_MV,1):g} mV) Threshold'
    THRESHOLD_BIT_32 = f'32 ({round(32/params.CC_MAX_COUNT*params.IS_MAX_MV,1):g} mV) Threshold'
    THRESHOLD_BIT_48 = f'48 ({round(48/params.CC_MAX_COUNT*params.IS_MAX_MV,1):g} mV) Threshold'
    THRESHOLD_BIT_64 = f'64 ({round(64/params.CC_MAX_COUNT*params.IS_MAX_MV,1):g} mV) Threshold'
    THRESHOLD_BIT_80 = f'80 ({round(80/params.CC_MAX_COUNT*params.IS_MAX_MV,1):g} mV) Threshold'
    THRESHOLD_BIT_96 = f'96 ({round(96/params.CC_MAX_COUNT*params.IS_MAX_MV,1):g} mV) Threshold'
    THRESHOLD_BIT_112 = f'112 ({round(112/params.CC_MAX_COUNT*params.IS_MAX_MV,1):g} mV) Threshold'
    
    THRESHOLD_FREQ_30KHZ ='30 KHz Threshold'
    THRESHOLD_FREQ_60KHZ ='60 KHz Threshold'
    THRESHOLD_FREQ_90KHZ ='90 KHz Threshold'
    THRESHOLD_FREQ_120KHZ ='120 KHz Threshold'
    
class INNO4_I2C_VBUSSC_OPTIONS():
    THRESHOLD_BIT_32 = f'32 ({round(32/params.CC_MAX_COUNT*params.IS_MAX_MV,1):g} mV) Threshold'
    THRESHOLD_BIT_48 = f'48 ({round(48/params.CC_MAX_COUNT*params.IS_MAX_MV,1):g} mV) Threshold'
    THRESHOLD_BIT_64 = f'64 ({round(64/params.CC_MAX_COUNT*params.IS_MAX_MV,1):g} mV) Threshold'
    THRESHOLD_BIT_72 = f'72 ({round(72/params.CC_MAX_COUNT*params.IS_MAX_MV,1):g} mV) Threshold'
    
    NUM_SAMPLES_1 ='1 sample'
    NUM_SAMPLES_2 ='2 samples'
    NUM_SAMPLES_3 ='3 samples'
    NUM_SAMPLES_4 ='4 samples'
    
class INNO4_I2C_VDIS_OPTIONS():
    VDIS_DISABLE = 'VDIS disable'
    VDIS_ENABLE_RESET = 'VDIS en/ VBEN dis/ Reset'
    VDIS_ENABLED_NO_RESET = 'VDIS en/ VBEN dis/ No Reset'

class INNO4_I2C_DCM_ONLY_OPTIONS():
    THRESHOLD_25MV = '25 mV Threshold'
    THRESHOLD_50MV = '50 mV Threshold'
    THRESHOLD_75MV = '75 mV Threshold'
    THRESHOLD_100MV = '100 mV Threshold'

class INNO4_I2C_FWD_PEAK_OPTIONS():
    PRE_SHIFT_0_NS = '0 ns Pre-Shift'
    PRE_SHIFT_30_NS = '30 ns Pre-Shift'
    PRE_SHIFT_60_NS = '60 ns Pre-Shift'
    PRE_SHIFT_90_NS = '90 ns Pre-Shift'
    
    WINDOW_30_50_PCT = '30%-50% Window'
    WINDOW_25_45_PCT = '25%-45% Window'
    WINDOW_20_40_PCT = '20%-40% Window'
    WINDOW_15_35_PCT = '15%-35% Window'

# Special Register entries

class INNO4_I2C_LOOP_OPTIONS():
    DEFAULT = 'Default Loop'
    OPTION1 = 'Loop Option 1'
    OPTION2 = 'Loop Option 2'

    
ResponseList = [
    INNO4_I2C_RESPONSE.AR,
    INNO4_I2C_RESPONSE.LO,
    INNO4_I2C_RESPONSE.DO,
    INNO4_I2C_RESPONSE.NR,
]

TimerList = [
    INNO4_I2C_TIMER.TIMER_8MS,
    INNO4_I2C_TIMER.TIMER_16MS,
    INNO4_I2C_TIMER.TIMER_32MS,
    INNO4_I2C_TIMER.TIMER_64MS,
]

CDCList = [
    INNO4_I2C_CDC_VALUES.CDC_0MV,
    INNO4_I2C_CDC_VALUES.CDC_50MV,
    INNO4_I2C_CDC_VALUES.CDC_100MV,
    INNO4_I2C_CDC_VALUES.CDC_150MV,
    INNO4_I2C_CDC_VALUES.CDC_200MV,
    INNO4_I2C_CDC_VALUES.CDC_250MV,
    INNO4_I2C_CDC_VALUES.CDC_300MV,
    INNO4_I2C_CDC_VALUES.CDC_350MV,
    INNO4_I2C_CDC_VALUES.CDC_400MV,
    INNO4_I2C_CDC_VALUES.CDC_450MV,
    INNO4_I2C_CDC_VALUES.CDC_500MV,
    INNO4_I2C_CDC_VALUES.CDC_550MV,
    INNO4_I2C_CDC_VALUES.CDC_600MV,
]

VBENList = [
    INNO4_I2C_VBEN_OPTIONS.VBEN_ENABLE,
    INNO4_I2C_VBEN_OPTIONS.VBEN_DISABLE_RESET,
    INNO4_I2C_VBEN_OPTIONS.VBEN_DISABLE_NO_RESET,
]

WatchdogList = [
    INNO4_I2C_WATCHDOG_OPTIONS.WATCHDOG_OFF,
    INNO4_I2C_WATCHDOG_OPTIONS.WATCHDOG_500MS,
    INNO4_I2C_WATCHDOG_OPTIONS.WATCHDOG_1000MS,
    INNO4_I2C_WATCHDOG_OPTIONS.WATCHDOG_2000MS,
    
]

BleederList = [
    INNO4_I2C_BLEEDER_OPTIONS.BLEEDER_OFF,
    INNO4_I2C_BLEEDER_OPTIONS.BLEEDER_ON,
    INNO4_I2C_BLEEDER_OPTIONS.BLEEDER_ON_AUTO_DIS,
]

AutoDisableList = [
    INNO4_I2C_BLEEDER_OPTIONS.AUTO_DIS_THRESH_10PCT,
    INNO4_I2C_BLEEDER_OPTIONS.AUTO_DIS_THRESH_4PCT,
]


ISSCThreshholdList = [
    INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_00,
    INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_16,
    INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_32,
    INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_48,
    INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_64,
    INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_80,
    INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_96,
    INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_112,
]

ISSCFreqList = [
    INNO4_I2C_ISSC_OPTIONS.THRESHOLD_FREQ_30KHZ,
    INNO4_I2C_ISSC_OPTIONS.THRESHOLD_FREQ_60KHZ,
    INNO4_I2C_ISSC_OPTIONS.THRESHOLD_FREQ_90KHZ,
    INNO4_I2C_ISSC_OPTIONS.THRESHOLD_FREQ_120KHZ,
]

VBUSSCResponseList = [
    INNO4_I2C_RESPONSE.AR,
    INNO4_I2C_RESPONSE.LO,
    INNO4_I2C_RESPONSE.NR,
]

VBUSSCThresholdList = [
    INNO4_I2C_VBUSSC_OPTIONS.THRESHOLD_BIT_32,
    INNO4_I2C_VBUSSC_OPTIONS.THRESHOLD_BIT_48,
    INNO4_I2C_VBUSSC_OPTIONS.THRESHOLD_BIT_64,
    INNO4_I2C_VBUSSC_OPTIONS.THRESHOLD_BIT_72,
]

VBUSSCNumSampleList = [
    INNO4_I2C_VBUSSC_OPTIONS.NUM_SAMPLES_1,
    INNO4_I2C_VBUSSC_OPTIONS.NUM_SAMPLES_2,
    INNO4_I2C_VBUSSC_OPTIONS.NUM_SAMPLES_3,
    INNO4_I2C_VBUSSC_OPTIONS.NUM_SAMPLES_4,
]

VDISLIst = [
    INNO4_I2C_VDIS_OPTIONS.VDIS_DISABLE,
    INNO4_I2C_VDIS_OPTIONS.VDIS_ENABLE_RESET,
    INNO4_I2C_VDIS_OPTIONS.VDIS_ENABLED_NO_RESET,
]

DCMOnlyList = [
    INNO4_I2C_DCM_ONLY_OPTIONS.THRESHOLD_25MV,
    INNO4_I2C_DCM_ONLY_OPTIONS.THRESHOLD_50MV,
    INNO4_I2C_DCM_ONLY_OPTIONS.THRESHOLD_75MV,
    INNO4_I2C_DCM_ONLY_OPTIONS.THRESHOLD_100MV,
]

FWDPeakPreShiftList = [
    INNO4_I2C_FWD_PEAK_OPTIONS.PRE_SHIFT_0_NS,
    INNO4_I2C_FWD_PEAK_OPTIONS.PRE_SHIFT_30_NS,
    INNO4_I2C_FWD_PEAK_OPTIONS.PRE_SHIFT_60_NS,
    INNO4_I2C_FWD_PEAK_OPTIONS.PRE_SHIFT_90_NS,
]

FWDPeakWindowList = [
    INNO4_I2C_FWD_PEAK_OPTIONS.WINDOW_30_50_PCT,
    INNO4_I2C_FWD_PEAK_OPTIONS.WINDOW_25_45_PCT,
    INNO4_I2C_FWD_PEAK_OPTIONS.WINDOW_20_40_PCT,
    INNO4_I2C_FWD_PEAK_OPTIONS.WINDOW_15_35_PCT,
]

# Special Register entry list

LoopOptionList = [
    INNO4_I2C_LOOP_OPTIONS.DEFAULT,
    INNO4_I2C_LOOP_OPTIONS.OPTION1,
    INNO4_I2C_LOOP_OPTIONS.OPTION2,
]

class INNO4_CV_Reg_UI():
    """Creates an I2C control UI frame for CV command register"""
    reg_label = 'CV'
    reg_address = Inno4Pro_I2C_Registers.CV_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = CV()
        reg_name = 'cv_reg'
        self.reg_label = 'CV'
        self.reg_address = Inno4Pro_I2C_Registers.CV_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=3,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.cv_value = UIObject(name = f'lineedit_{page_name}_{reg_name}_setpoint_V',object_type=UILineEditObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.cv_value:UILineEditObject = self.cv_value.add_lineedit_to_grid_frame(placeholder="Voltage (V)",max_value=params.CV_MAX_V,min_value=params.CV_MIN_V,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.auto_cv =  UIObject(name = f'chkbox_{page_name}_{reg_name}_auto_cv_enable',object_type=UICheckboxObject,
                            row_index=3,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.auto_cv:UICheckboxObject = self.auto_cv.add_checkbox_to_grid_frame(name="Auto-set Enable", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=3,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        self.text_change_flag = True
        self.validate()
        self.cv_value.textChanged.connect(self.validate)
        self.auto_cv.stateChanged.connect(self.validate)
    
    def validate(self):
        if self.text_change_flag == False:
            return None,None,None
        if self.cv_value.text() == '':
            return None,None,None
        cv_V = rounded_float(self.cv_value.text())
        if cv_V < params.CV_MIN_V:
            return None,None,None
        
        if not (cv_V == set_in_range(cv_V,params.CV_MAX_V,params.CV_MIN_V)):
            cv_V = set_in_range(cv_V,params.CV_MAX_V,params.CV_MIN_V)
            self.text_change_flag = False
            self.cv_value.setText(f'{cv_V:g}')
            self.text_change_flag = True        
            
        auto_cv= self.auto_cv.isChecked()
        reg = self.update_i2c_data(cv_V,auto_cv)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
        
    def update_i2c_data(self,cv_V,auto_cv):
        reg:CV = process_cv_command(vout_V= cv_V,auto_cv= auto_cv)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        cv_text = self.cv_value.text()
        auto_cv_en = self.auto_cv.isChecked()
        ui_params = [cv_text,auto_cv_en]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.cv_value.setText(ui_params[0])
        self.auto_cv.setChecked(ui_params[1])
        self.text_change_flag = True
        
class INNO4_CC_Reg_UI():
    """Creates an I2C control UI frame for CC command register"""
    reg_label = 'CC'
    reg_address = Inno4Pro_I2C_Registers.CC_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = CC()
        reg_name = 'cc_reg'
        self.reg_label = 'CC'
        self.reg_address = Inno4Pro_I2C_Registers.CC_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=3,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)

        self.cc_value = UIObject(name = f'lineedit_{page_name}_{reg_name}_setpoint_A',object_type=UILineEditObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.cc_value:UILineEditObject = self.cc_value.add_lineedit_to_grid_frame(placeholder="CC Setpoint (A)",max_value=100,min_value=0,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.rsense_value = UIObject(name = f'lineedit_{page_name}_{reg_name}_rsense_mohm',object_type=UILineEditObject,
                            row_index=3,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.rsense_value:UILineEditObject = self.rsense_value.add_lineedit_to_grid_frame(placeholder="Rsense (mΩ)",max_value=100,min_value=0,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=3,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.text_change_flag = True
        self.validate()
        self.cc_value.textChanged.connect(self.validate)
        self.rsense_value.textChanged.connect(self.validate)
    
    def validate(self):
        if self.text_change_flag == False:
            return None,None,None
        if self.cc_value.text() == '':
            return None,None,None
        if self.rsense_value.text() == '':
            return None,None,None
        rsense_mohm = rounded_float(self.rsense_value.text())
        cc_A = rounded_float(self.cc_value.text())
        
        if (rsense_mohm == 0) or (cc_A == 0):
            return None,None,None
        imax = round(params.IS_MAX_MV/rsense_mohm,6)
        cc_bits = round(cc_A / imax * params.CC_MAX_COUNT)
        if cc_bits < params.CC_MIN_COUNT:
            return None,None,None
        
        if not (cc_bits == set_in_range(cc_bits,params.CC_MAX_COUNT,params.CC_MIN_COUNT)):
            cc_bits = set_in_range(cc_bits,params.CC_MAX_COUNT,params.CC_MIN_COUNT)
            cc_A = round(cc_bits*(params.IS_MAX_MV/rsense_mohm)/params.CC_MAX_COUNT,6)
            self.text_change_flag = False
            self.cc_value.setText(f'{cc_A:g}')
            self.text_change_flag = True
            
        reg = self.update_i2c_data(cc_A, rsense_mohm)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
    
    def update_i2c_data(self,cc_A,rsense_mohm):
        reg:CC = process_cc_command(iout_A= cc_A,rsense_mohm= rsense_mohm)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg

    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        cc_text = self.cc_value.text()
        rsense_text = self.rsense_value.text()
        ui_params = [cc_text,rsense_text]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.cc_value.setText(ui_params[0])
        self.rsense_value.setText(ui_params[1])
        self.text_change_flag = True
        
class INNO4_UVA_Reg_UI():
    """Creates an I2C control UI frame for UVA command register"""
    reg_label = 'UVA'
    reg_address = Inno4Pro_I2C_Registers.UVA_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = UVA()
        reg_name = 'uva_reg'
        self.reg_label = 'UVA'
        self.reg_address = Inno4Pro_I2C_Registers.UVA_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=3,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.uva_thresh = UIObject(name = f'lineedit_{page_name}_{reg_name}_thresh_V',object_type=UILineEditObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.uva_thresh:UILineEditObject = self.uva_thresh.add_lineedit_to_grid_frame(placeholder="Voltage Threshold (V)",max_value=params.UV_MAX_V,min_value=params.UV_MIN_V,\
                                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.uva_response =  UIObject(name = f'cbx_{page_name}_{reg_name}_response',object_type=UIComboBoxObject,
                            row_index=3,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.uva_response = self.uva_response.add_combobox_to_grid_frame(options_list=ResponseList,\
                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.uva_timer =  UIObject(name = f'cbx_{page_name}_{reg_name}_timer',object_type=UIComboBoxObject,
                            row_index=4,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.uva_timer = self.uva_timer.add_combobox_to_grid_frame(options_list=TimerList,\
                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=2,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=4,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.text_change_flag = True
        self.validate()
        self.uva_thresh.textChanged.connect(self.validate)
        self.uva_response.currentIndexChanged.connect(self.validate)
        self.uva_timer.currentIndexChanged.connect(self.validate)
        
    def validate(self):
        if self.text_change_flag == False:
            return None,None,None
        if self.uva_thresh.text() == '':
            return None,None,None
        uv_V = rounded_float(self.uva_thresh.text())
        if uv_V < params.UV_MIN_V:
            return None,None,None
        if not (uv_V == set_in_range(uv_V,params.UV_MAX_V,params.UV_MIN_V)):
            uv_V = set_in_range(uv_V,params.UV_MAX_V,params.UV_MIN_V)
            self.text_change_flag = False
            self.uva_thresh.setText(f'{uv_V:g}')
            self.text_change_flag = True        
        
        match self.uva_response.currentText():
            case INNO4_I2C_RESPONSE.AR:
                response = commands.UVA_RESP_AR
            case INNO4_I2C_RESPONSE.LO:
                response = commands.UVA_RESP_LO
            case INNO4_I2C_RESPONSE.DO:
                response = commands.UVA_RESP_DO
            case INNO4_I2C_RESPONSE.NR:
                response = commands.UVA_RESP_NR
                
        match self.uva_timer.currentText():
            case INNO4_I2C_TIMER.TIMER_8MS:
                timer = commands.UVA_TIMER_8MS
            case INNO4_I2C_TIMER.TIMER_16MS:
                timer = commands.UVA_TIMER_16MS
            case INNO4_I2C_TIMER.TIMER_32MS:
                timer = commands.UVA_TIMER_32MS
            case INNO4_I2C_TIMER.TIMER_64MS:
                timer = commands.UVA_TIMER_64MS   
        
        reg = self.update_i2c_data(uv_V, response, timer)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
        
    def update_i2c_data(self,uv_V,response,timer):                 
        reg:UVA = process_uva_command(threshold_V= uv_V,response=response,timer=timer)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        uva_text = self.uva_thresh.text()
        uva_response_index = self.uva_response.currentIndex()
        uva_timer_index = self.uva_timer.currentIndex()
        ui_params = [uva_text,uva_response_index,uva_timer_index,]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.uva_thresh.setText(ui_params[0])
        self.uva_response.setCurrentIndex(ui_params[1])
        self.uva_timer.setCurrentIndex(ui_params[2])
        self.text_change_flag = True
        
class INNO4_OVA_Reg_UI():
    """Creates an I2C control UI frame for OVA command register"""
    reg_label = 'OVA'
    reg_address = Inno4Pro_I2C_Registers.OVA_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = OVA()
        reg_name = 'ova_reg'
        self.reg_label = 'OVA'
        self.reg_address = Inno4Pro_I2C_Registers.OVA_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=3,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.ova_thresh = UIObject(name = f'lineedit_{page_name}_{reg_name}_thresh_V',object_type=UILineEditObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.ova_thresh:UILineEditObject = self.ova_thresh.add_lineedit_to_grid_frame(placeholder="Voltage Threshold (V)",max_value=params.OV_MAX_V,min_value=params.OV_MIN_V,\
                                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.ova_response =  UIObject(name = f'cbx_{page_name}_{reg_name}_response',object_type=UIComboBoxObject,
                            row_index=3,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.ova_response = self.ova_response.add_combobox_to_grid_frame(options_list=ResponseList,\
                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=3,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
        self.text_change_flag = True
        self.validate()
        self.ova_thresh.textChanged.connect(self.validate)
        self.ova_response.currentIndexChanged.connect(self.validate)
    
    def validate(self):
        if self.text_change_flag == False:
            return None,None,None
        if self.ova_thresh.text() == '':
            return None,None,None
        ov_V = rounded_float(self.ova_thresh.text())
        if ov_V < params.OV_MIN_V:
            return None,None,None
        
        if not (ov_V == set_in_range(ov_V,params.OV_MAX_V,params.OV_MIN_V)):
            ov_V = set_in_range(ov_V,params.OV_MAX_V,params.OV_MIN_V)
            self.text_change_flag = False
            self.ova_thresh.setText(f'{ov_V:g}')
            self.text_change_flag = True      
            
        match self.ova_response.currentText():
            case INNO4_I2C_RESPONSE.AR:
                response = commands.OVA_RESP_AR
            case INNO4_I2C_RESPONSE.LO:
                response = commands.OVA_RESP_LO
            case INNO4_I2C_RESPONSE.DO:
                response = commands.OVA_RESP_DO
            case INNO4_I2C_RESPONSE.NR:
                response = commands.OVA_RESP_NR
          
        reg = self.update_i2c_data(ov_V, response)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
        
    def update_i2c_data(self,ov_V,response):             
        reg:OVA = process_ova_command(threshold_V= ov_V,response=response)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        ova_text = self.ova_thresh.text()
        ova_response_index = self.ova_response.currentIndex()
        ui_params = [ova_text,ova_response_index]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.ova_thresh.setText(ui_params[0])
        self.ova_response.setCurrentIndex(ui_params[1])
        self.text_change_flag = True

class INNO4_CDC_Reg_UI():
    """Creates an I2C control UI frame for CDC command register"""
    reg_label = 'CDC'
    reg_address = Inno4Pro_I2C_Registers.CDC_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = CDC()
        reg_name = 'cdc_reg'
        self.reg_label = 'CDC'
        self.reg_address = Inno4Pro_I2C_Registers.CDC_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=3,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)

        self.cdc_value = UIObject(name = f'cbx_{page_name}_{reg_name}_setpoint_mV',object_type=UIComboBoxObject,
                            row_index=3,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.cdc_value:UILineEditObject = self.cdc_value.add_combobox_to_grid_frame(options_list=CDCList,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=3,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
    
        self.validate()
        self.cdc_value.currentIndexChanged.connect(self.validate)
    
    def validate(self):
        match self.cdc_value.currentText():
            case INNO4_I2C_CDC_VALUES.CDC_0MV:
                cdc_mV = 0
            case INNO4_I2C_CDC_VALUES.CDC_50MV:
                cdc_mV = 50
            case INNO4_I2C_CDC_VALUES.CDC_100MV:
                cdc_mV = 100
            case INNO4_I2C_CDC_VALUES.CDC_150MV:
                cdc_mV = 150
            case INNO4_I2C_CDC_VALUES.CDC_200MV:
                cdc_mV = 200
            case INNO4_I2C_CDC_VALUES.CDC_250MV:
                cdc_mV = 250
            case INNO4_I2C_CDC_VALUES.CDC_300MV:
                cdc_mV = 300
            case INNO4_I2C_CDC_VALUES.CDC_350MV:
                cdc_mV = 350
            case INNO4_I2C_CDC_VALUES.CDC_400MV:
                cdc_mV = 400
            case INNO4_I2C_CDC_VALUES.CDC_450MV:
                cdc_mV = 450
            case INNO4_I2C_CDC_VALUES.CDC_500MV:
                cdc_mV = 500
            case INNO4_I2C_CDC_VALUES.CDC_550MV:
                cdc_mV = 550
            case INNO4_I2C_CDC_VALUES.CDC_600MV:
                cdc_mV = 600
                
        reg = self.update_i2c_data(cdc_mV)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
    
    def update_i2c_data(self,cdc_mV):                
        reg:CDC = process_cdc_command(cdc_mV = cdc_mV)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg

    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        cdc_index = self.cdc_value.currentIndex()
        ui_params = [cdc_index]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.cdc_value.setCurrentIndex(ui_params[0])
        self.text_change_flag = True
    
class INNO4_CVO_Reg_UI():
    """Creates an I2C control UI frame for CVO command register"""
    reg_label = 'CVO'
    reg_address = Inno4Pro_I2C_Registers.CVO_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = CVO()
        reg_name = 'cvo_reg'
        self.reg_label = 'CVO'
        self.reg_address = Inno4Pro_I2C_Registers.CVO_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=3,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.cvo_response =  UIObject(name = f'cbx_{page_name}_{reg_name}_response',object_type=UIComboBoxObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.cvo_response = self.cvo_response.add_combobox_to_grid_frame(options_list=ResponseList,\
                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.cvo_timer =  UIObject(name = f'cbx_{page_name}_{reg_name}_timer',object_type=UIComboBoxObject,
                            row_index=3,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.cvo_timer = self.cvo_timer.add_combobox_to_grid_frame(options_list=TimerList,\
                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.cvo_enable =  UIObject(name = f'chkbox_{page_name}_{reg_name}_enable',object_type=UICheckboxObject,
                            row_index=4,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        
        self.cvo_enable:UICheckboxObject = self.cvo_enable.add_checkbox_to_grid_frame(name="CVO Mode", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=2,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=4,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.validate()
        self.cvo_response.currentIndexChanged.connect(self.validate)
        self.cvo_timer.currentIndexChanged.connect(self.validate)
        self.cvo_enable.stateChanged.connect(self.validate)
      
    def validate(self):
        match self.cvo_response.currentText():
            case INNO4_I2C_RESPONSE.AR:
                response = commands.CVO_RESP_AR
            case INNO4_I2C_RESPONSE.LO:
                response = commands.CVO_RESP_LO
            case INNO4_I2C_RESPONSE.DO:
                response = commands.CVO_RESP_DO
            case INNO4_I2C_RESPONSE.NR:
                response = commands.CVO_RESP_NR
                
        match self.cvo_timer.currentText():
            case INNO4_I2C_TIMER.TIMER_8MS:
                timer = commands.CVO_TIMER_8MS
            case INNO4_I2C_TIMER.TIMER_16MS:
                timer = commands.CVO_TIMER_16MS
            case INNO4_I2C_TIMER.TIMER_32MS:
                timer = commands.CVO_TIMER_32MS
            case INNO4_I2C_TIMER.TIMER_64MS:
                timer = commands.CVO_TIMER_64MS     
                
        cvo_en = self.cvo_enable.isChecked()
        reg = self.update_i2c_data(response, timer, cvo_en)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
    
    def update_i2c_data(self,response, timer, cvo_en):  
        reg:CVO = process_cvo_command(response=response,timer=timer,cvo_en=cvo_en)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        cvo_response_index = self.cvo_response.currentIndex()
        cvo_timer_index = self.cvo_timer.currentIndex()
        cvo_en = self.cvo_enable.isChecked()
        ui_params = [cvo_response_index,cvo_timer_index,cvo_en]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.cvo_response.setCurrentIndex(ui_params[0])
        self.cvo_timer.setCurrentIndex(ui_params[1])
        self.cvo_enable.setChecked(ui_params[2])
        self.text_change_flag = True
    
class INNO4_VKP_Reg_UI():
    """Creates an I2C control UI frame for CC command register"""
    reg_label = 'VKP'
    reg_address = Inno4Pro_I2C_Registers.VKP_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = VKP()
        reg_name = 'vkp_reg'
        self.reg_label = 'VKP'
        self.reg_address = Inno4Pro_I2C_Registers.VKP_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=3,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)

        self.vkp_value = UIObject(name = f'lineedit_{page_name}_{reg_name}_setpoint_V',object_type=UILineEditObject,
                            row_index=3,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.vkp_value:UILineEditObject = self.vkp_value.add_lineedit_to_grid_frame(placeholder="VKP Setpoint (V)",max_value=params.VKP_MAX_V,min_value=params.VKP_MIN_V,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=3,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.text_change_flag = True
        self.validate()
        self.vkp_value.textChanged.connect(self.validate)
    
    def validate(self):
        if self.text_change_flag == False:
            return None, None, None
        if self.vkp_value.text() == '':
            return None, None, None

        vkp_V = rounded_float(self.vkp_value.text())

        if vkp_V < params.VKP_MIN_V:
            return None, None, None
        
        if not (vkp_V == set_in_range(vkp_V,params.VKP_MAX_V,params.VKP_MIN_V)):
            vkp_V = set_in_range(vkp_V,params.VKP_MAX_V,params.VKP_MIN_V)
            self.text_change_flag = False
            self.vkp_value.setText(f'{vkp_V:g}')
            self.text_change_flag = True
        reg = self.update_i2c_data(vkp_V)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
    
    def update_i2c_data(self, vkp_V):
        reg:VKP = process_vkp_command(vkp_V= vkp_V)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        vkp_text = self.vkp_value.text()
        ui_params = [vkp_text]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.vkp_value.setText(ui_params[0])
        self.text_change_flag = True

class INNO4_VBEN_Reg_UI():
    """Creates an I2C control UI frame for VBEN command register"""
    reg_label = 'VBEN'
    reg_address = Inno4Pro_I2C_Registers.VBEN_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = VBEN()
        reg_name = 'vben_reg'
        self.reg_label = 'VBEN'
        self.reg_address = Inno4Pro_I2C_Registers.VBEN_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.vben_option = UIObject(name = f'cbx_{page_name}_{reg_name}_option',object_type=UIComboBoxObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=90, min_height=30)
        self.vben_option:UILineEditObject = self.vben_option.add_combobox_to_grid_frame(options_list=VBENList,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=4,col_index=1,row_span=1,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=5,col_index=1,row_span=1,col_span=1,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
    
        self.validate()
        self.vben_option.currentIndexChanged.connect(self.validate)
    
    def validate(self):
        match self.vben_option.currentText():
            case INNO4_I2C_VBEN_OPTIONS.VBEN_ENABLE:
                vben = commands.VBEN_ON
            case INNO4_I2C_VBEN_OPTIONS.VBEN_DISABLE_RESET:
                vben = commands.VBEN_OFF_RST
            case INNO4_I2C_VBEN_OPTIONS.VBEN_DISABLE_NO_RESET:
                vben = commands.VBEN_OFF_NO_RST
        reg = self.update_i2c_data(vben)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
    
    def update_i2c_data(self,vben):
        reg:VBEN = process_vben_command(vben)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        vben_index = self.vben_option.currentIndex()
        ui_params = [vben_index]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.vben_option.setCurrentIndex(ui_params[0])
        self.text_change_flag = True

class INNO4_WATCHDOG_Reg_UI():
    """Creates an I2C control UI frame for WATCHDOG command register"""
    reg_label = 'Watchdog'
    reg_address = Inno4Pro_I2C_Registers.WATCHDOG_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = WATCHDOG()
        reg_name = 'watchdog_reg'
        self.reg_label = 'Watchdog'
        self.reg_address = Inno4Pro_I2C_Registers.WATCHDOG_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.watchdog_option = UIObject(name = f'cbx_{page_name}_{reg_name}_option',object_type=UIComboBoxObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=90, min_height=30)
        self.watchdog_option:UILineEditObject = self.watchdog_option.add_combobox_to_grid_frame(options_list=WatchdogList,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=4,col_index=1,row_span=1,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=5,col_index=1,row_span=1,col_span=1,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.validate()
        self.watchdog_option.currentIndexChanged.connect(self.validate)
    
    def validate(self):
        match self.watchdog_option.currentText():
            case INNO4_I2C_WATCHDOG_OPTIONS.WATCHDOG_OFF:
                watchdog = commands.WATCHDOG_OFF
            case INNO4_I2C_WATCHDOG_OPTIONS.WATCHDOG_500MS:
                watchdog = commands.WATCHDOG_500MS
            case INNO4_I2C_WATCHDOG_OPTIONS.WATCHDOG_1000MS:
                watchdog = commands.WATCHDOG_1000MS
            case INNO4_I2C_WATCHDOG_OPTIONS.WATCHDOG_2000MS:
                watchdog = commands.WATCHDOG_2000MS
        reg = self.update_i2c_data(watchdog)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
    
    def update_i2c_data(self,watchdog):
        reg:WATCHDOG = process_watchdog_command(watchdog)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        watchdog_index = self.watchdog_option.currentIndex()
        ui_params = [watchdog_index]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.watchdog_option.setCurrentIndex(ui_params[0])
        self.text_change_flag = True
    
class INNO4_BLEEDER_Reg_UI():
    """Creates an I2C control UI frame for CVO command register"""
    reg_label = 'Bleeder'
    reg_address = Inno4Pro_I2C_Registers.BLEEDER_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = BLEEDER()
        reg_name = 'bleeder_reg'
        self.reg_label = 'Bleeder'
        self.reg_address = Inno4Pro_I2C_Registers.BLEEDER_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=3,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.bleeder_en =  UIObject(name = f'cbx_{page_name}_{reg_name}_bleeder',object_type=UIComboBoxObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.bleeder_en = self.bleeder_en.add_combobox_to_grid_frame(options_list=BleederList,\
                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.weak_bleeder_en =  UIObject(name = f'chkbox_{page_name}_{reg_name}_weak_bleeder',object_type=UICheckboxObject,
                            row_index=3,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.weak_bleeder_en:UICheckboxObject = self.weak_bleeder_en.add_checkbox_to_grid_frame(name="Weak Bleeder Enable", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=3,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.validate()
        self.bleeder_en.currentIndexChanged.connect(self.validate)
        self.weak_bleeder_en.stateChanged.connect(self.validate)
      
    def validate(self):
        match self.bleeder_en.currentText():
            case INNO4_I2C_BLEEDER_OPTIONS.BLEEDER_OFF:
                bleeder_en = commands.BLEEDER_OFF
            case INNO4_I2C_BLEEDER_OPTIONS.BLEEDER_ON:
                bleeder_en = commands.BLEEDER_ON
            case INNO4_I2C_BLEEDER_OPTIONS.BLEEDER_ON_AUTO_DIS:
                bleeder_en = commands.BLEEDER_ON_AUTO_DIS
                
        weak_bleeder_en =  self.weak_bleeder_en.isChecked()            
        reg = self.update_i2c_data(bleeder_en, weak_bleeder_en)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
    
    def update_i2c_data(self,bleeder_en, weak_bleeder_en):  
        reg:BLEEDER = process_bleeder_command(bleeder_en=bleeder_en,weak_bleeder_en=weak_bleeder_en)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg

    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        bleeder_en_index = self.bleeder_en.currentIndex()
        weak_bleeder_en = self.weak_bleeder_en.isChecked()
        ui_params = [bleeder_en_index,weak_bleeder_en]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.bleeder_en.setCurrentIndex(ui_params[0])
        self.weak_bleeder_en.setChecked(ui_params[1])
        self.text_change_flag = True
    
class INNO4_FAST_VI_Reg_UI():
    """Creates an I2C control UI frame for Fast VI command register"""
    reg_label = 'Fast VI'
    reg_address = Inno4Pro_I2C_Registers.FAST_VI_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = FAST_VI()
        reg_name = 'fast_vi_reg'
        self.reg_label = 'Fast VI'
        self.reg_address = Inno4Pro_I2C_Registers.FAST_VI_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=2,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)

        self.fast_vi_en =  UIObject(name = f'chkbox_{page_name}_{reg_name}_enable',object_type=UICheckboxObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.fast_vi_en:UICheckboxObject = self.fast_vi_en.add_checkbox_to_grid_frame(name="10 ms Limit Disable", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=3,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.validate()
        self.fast_vi_en.clicked.connect(self.validate)
    
    def validate(self):
        fast_vi_en = self.fast_vi_en.isChecked()        
        reg = self.update_i2c_data(fast_vi_en)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
    
    def update_i2c_data(self, fast_vi_en):
        reg:FAST_VI = process_fast_vi_command(setting=fast_vi_en)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        fast_vi_en = self.fast_vi_en.isChecked()
        ui_params = [fast_vi_en]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.fast_vi_en.setChecked(ui_params[0])
        self.text_change_flag = True

class INNO4_CCSC_Reg_UI():
    """Creates an I2C control UI frame for CCSC command register"""
    reg_label = 'CCSC'
    reg_address = Inno4Pro_I2C_Registers.CCSC_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = CCSC()
        reg_name = 'ccsc_reg'
        self.reg_label = 'CCSC'
        self.reg_address = Inno4Pro_I2C_Registers.CCSC_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=2,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.ccsc_response =  UIObject(name = f'cbx_{page_name}_{reg_name}_response',object_type=UIComboBoxObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.ccsc_response = self.ccsc_response.add_combobox_to_grid_frame(options_list=ResponseList,\
                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=3,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.validate()
        self.ccsc_response.currentIndexChanged.connect(self.validate)
      
    def validate(self):
        match self.ccsc_response.currentText():
            case INNO4_I2C_RESPONSE.AR:
                response = commands.CCSC_RESP_AR
            case INNO4_I2C_RESPONSE.LO:
                response = commands.CCSC_RESP_LO
            case INNO4_I2C_RESPONSE.DO:
                response = commands.CCSC_RESP_DO
            case INNO4_I2C_RESPONSE.NR:
                response = commands.CCSC_RESP_NR
                
        reg = self.update_i2c_data(response)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
    
    def update_i2c_data(self,response):  
        reg:CCSC = process_ccsc_command(response)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        ccsc_response_index = self.ccsc_response.currentIndex()
        ui_params = [ccsc_response_index]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.ccsc_response.setCurrentIndex(ui_params[0])
        self.text_change_flag = True

class INNO4_ISSC_Reg_UI():
    """Creates an I2C control UI frame for ISSC command register"""
    reg_label = 'ISSC'
    reg_address = Inno4Pro_I2C_Registers.ISSC_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = ISSC()
        reg_name = 'issc_reg'
        self.reg_label = 'ISSC'
        self.reg_address = Inno4Pro_I2C_Registers.ISSC_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=3,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.thresh_bits =  UIObject(name = f'cbx_{page_name}_{reg_name}_threshold_bits',object_type=UIComboBoxObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.thresh_bits = self.thresh_bits.add_combobox_to_grid_frame(options_list=ISSCThreshholdList,\
                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.thresh_freq =  UIObject(name = f'cbx_{page_name}_{reg_name}_threshold_freq',object_type=UIComboBoxObject,
                            row_index=3,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.thresh_freq = self.thresh_freq.add_combobox_to_grid_frame(options_list=ISSCFreqList,\
                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.issc_response =  UIObject(name = f'cbx_{page_name}_{reg_name}_response',object_type=UIComboBoxObject,
                            row_index=4,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.issc_response = self.issc_response.add_combobox_to_grid_frame(options_list=ResponseList,\
                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=2,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=4,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.validate()
        self.thresh_bits.currentIndexChanged.connect(self.validate)
        self.thresh_freq.currentIndexChanged.connect(self.validate)
        self.issc_response.currentIndexChanged.connect(self.validate)
      
    def validate(self):
        match self.issc_response.currentText():
            case INNO4_I2C_RESPONSE.AR:
                response = commands.ISSC_RESP_AR
            case INNO4_I2C_RESPONSE.LO:
                response = commands.ISSC_RESP_LO
            case INNO4_I2C_RESPONSE.DO:
                response = commands.ISSC_RESP_DO
            case INNO4_I2C_RESPONSE.NR:
                response = commands.ISSC_RESP_NR
                
        match self.thresh_freq.currentText():
            case INNO4_I2C_ISSC_OPTIONS.THRESHOLD_FREQ_30KHZ:
                threshold_freq = commands.ISSC_FREQ_30KHZ
            case INNO4_I2C_ISSC_OPTIONS.THRESHOLD_FREQ_60KHZ:
                threshold_freq = commands.ISSC_FREQ_60KHZ
            case INNO4_I2C_ISSC_OPTIONS.THRESHOLD_FREQ_90KHZ:
                threshold_freq = commands.ISSC_FREQ_90KHZ
            case INNO4_I2C_ISSC_OPTIONS.THRESHOLD_FREQ_120KHZ:
                threshold_freq = commands.ISSC_FREQ_120KHZ
                
        match self.thresh_bits.currentText():
            case INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_00:
                threshold_bits = commands.ISSC_CC_LIMIT_00
            case INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_16:
                threshold_bits = commands.ISSC_CC_LIMIT_16
            case INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_32:
                threshold_bits = commands.ISSC_CC_LIMIT_32
            case INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_48:
                threshold_bits = commands.ISSC_CC_LIMIT_48
            case INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_64:
                threshold_bits = commands.ISSC_CC_LIMIT_64
            case INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_80:
                threshold_bits = commands.ISSC_CC_LIMIT_80
            case INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_96:
                threshold_bits = commands.ISSC_CC_LIMIT_96
            case INNO4_I2C_ISSC_OPTIONS.THRESHOLD_BIT_112:
                threshold_bits = commands.ISSC_CC_LIMIT_112
        
        reg = self.update_i2c_data(threshold_bits=threshold_bits,threshold_freq=threshold_freq,response=response)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
    
    def update_i2c_data(self,threshold_bits, threshold_freq, response):  
        reg:ISSC = process_issc_command(threshold_bits=threshold_bits, threshold_freq=threshold_freq, response=response)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        issc_response_index = self.issc_response.currentIndex()
        thresh_freq_index = self.thresh_freq.currentIndex()
        thresh_bits_index = self.thresh_bits.currentIndex()
        ui_params = [issc_response_index,thresh_freq_index,thresh_bits_index]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.issc_response.setCurrentIndex(ui_params[0])
        self.thresh_freq.setCurrentIndex(ui_params[1])
        self.thresh_bits.setCurrentIndex(ui_params[2])
        self.text_change_flag = True

class INNO4_VBUSSC_Reg_UI():
    """Creates an I2C control UI frame for VBUSSC command register"""
    reg_label = 'VBUSSC'
    reg_address = Inno4Pro_I2C_Registers.VBUSSC_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = VBUSSC()
        reg_name = 'vbussc_reg'
        self.reg_label = 'VBUSSC'
        self.reg_address = Inno4Pro_I2C_Registers.VBUSSC_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=3,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.thresh_bits =  UIObject(name = f'cbx_{page_name}_{reg_name}_threshold_bits',object_type=UIComboBoxObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.thresh_bits = self.thresh_bits.add_combobox_to_grid_frame(options_list=VBUSSCThresholdList,\
                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.num_samples =  UIObject(name = f'cbx_{page_name}_{reg_name}_num_samples',object_type=UIComboBoxObject,
                            row_index=3,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.num_samples = self.num_samples.add_combobox_to_grid_frame(options_list=VBUSSCNumSampleList,\
                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.vbussc_response =  UIObject(name = f'cbx_{page_name}_{reg_name}_response',object_type=UIComboBoxObject,
                            row_index=4,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.vbussc_response = self.vbussc_response.add_combobox_to_grid_frame(options_list=VBUSSCResponseList,\
                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=2,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=4,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.validate()
        self.thresh_bits.currentIndexChanged.connect(self.validate)
        self.num_samples.currentIndexChanged.connect(self.validate)
        self.vbussc_response.currentIndexChanged.connect(self.validate)
      
    def validate(self):
        match self.vbussc_response.currentText():
            case INNO4_I2C_RESPONSE.AR:
                response = commands.VBUSSC_RESP_AR
            case INNO4_I2C_RESPONSE.LO:
                response = commands.VBUSSC_RESP_LO
            case INNO4_I2C_RESPONSE.NR:
                response = commands.VBUSSC_RESP_NR
                
        match self.num_samples.currentText():
            case INNO4_I2C_VBUSSC_OPTIONS.NUM_SAMPLES_1:
                num_samples = commands.VBUSSC_SAMPLE_1
            case INNO4_I2C_VBUSSC_OPTIONS.NUM_SAMPLES_2:
                num_samples = commands.VBUSSC_SAMPLE_2
            case INNO4_I2C_VBUSSC_OPTIONS.NUM_SAMPLES_3:
                num_samples = commands.VBUSSC_SAMPLE_3
            case INNO4_I2C_VBUSSC_OPTIONS.NUM_SAMPLES_4:
                num_samples = commands.VBUSSC_SAMPLE_4
                
        match self.thresh_bits.currentText():
            case INNO4_I2C_VBUSSC_OPTIONS.THRESHOLD_BIT_32:
                threshold_bits = commands.VBUSSC_IS_VAL_32
            case INNO4_I2C_VBUSSC_OPTIONS.THRESHOLD_BIT_48:
                threshold_bits = commands.VBUSSC_IS_VAL_48
            case INNO4_I2C_VBUSSC_OPTIONS.THRESHOLD_BIT_64:
                threshold_bits = commands.VBUSSC_IS_VAL_64
            case INNO4_I2C_VBUSSC_OPTIONS.THRESHOLD_BIT_72:
                threshold_bits = commands.VBUSSC_IS_VAL_72
        
        reg = self.update_i2c_data(threshold_bits=threshold_bits,num_samples=num_samples,response=response)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
    
    def update_i2c_data(self,threshold_bits, num_samples, response):  
        reg:ISSC = process_vbussc_command(threshold_bits=threshold_bits, num_samples=num_samples, response=response)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        vbussc_response_index = self.vbussc_response.currentIndex()
        num_samples_index = self.num_samples.currentIndex()
        thresh_bits_index = self.thresh_bits.currentIndex()
        ui_params = [vbussc_response_index,num_samples_index,thresh_bits_index]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.vbussc_response.setCurrentIndex(ui_params[0])
        self.num_samples.setCurrentIndex(ui_params[1])
        self.thresh_bits.setCurrentIndex(ui_params[2])
        self.text_change_flag = True
    
class INNO4_VDIS_Reg_UI():
    """Creates an I2C control UI frame for VDIS command register"""
    reg_label = 'VDIS'
    reg_address = Inno4Pro_I2C_Registers.VDIS_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = VDIS()
        reg_name = 'vdis_reg'
        self.reg_label = 'VDIS'
        self.reg_address = Inno4Pro_I2C_Registers.VDIS_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=2,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)

        self.vdis_setting = UIObject(name = f'cbx_{page_name}_{reg_name}_setting',object_type=UIComboBoxObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.vdis_setting:UIComboBoxObject = self.vdis_setting.add_combobox_to_grid_frame(options_list=VDISLIst,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=3,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
    
        self.validate()
        self.vdis_setting.currentIndexChanged.connect(self.validate)
    
    def validate(self):
        match self.vdis_setting.currentText():
            case INNO4_I2C_VDIS_OPTIONS.VDIS_DISABLE:
                setting = commands.VDIS_OFF
            case INNO4_I2C_VDIS_OPTIONS.VDIS_ENABLE_RESET:
                setting = commands.VDIS_ON_RST
            case INNO4_I2C_VDIS_OPTIONS.VDIS_ENABLED_NO_RESET:
                setting = commands.VDIS_ON_NO_RST
                
        reg = self.update_i2c_data(setting)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
    
    def update_i2c_data(self,setting):                
        reg:VDIS = process_vdis_command(setting = setting)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        vdis_setting_index = self.vdis_setting.currentIndex()
        ui_params = [vdis_setting_index]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.vdis_setting.setCurrentIndex(ui_params[0])
        self.text_change_flag = True

class INNO4_TURN_OFF_PSU_Reg_UI():
    """Creates an I2C control UI frame for PSU Turn-Off command register"""
    reg_label = 'PSU Turn-Off'
    reg_address = Inno4Pro_I2C_Registers.TURN_OFF_PSU_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = TURN_OFF_PSU()
        reg_name = 'psu_turn_off_reg'
        self.reg_label = 'PSU Turn-Off'
        self.reg_address = Inno4Pro_I2C_Registers.TURN_OFF_PSU_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=2,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)

        self.latch_off_en =  UIObject(name = f'chkbox_{page_name}_{reg_name}_enable',object_type=UICheckboxObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.latch_off_en:UICheckboxObject = self.latch_off_en.add_checkbox_to_grid_frame(name="Latch-Off Enable", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=3,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.validate()
        self.latch_off_en.clicked.connect(self.validate)
    
    def validate(self):
        latch_off_en = self.latch_off_en.isChecked()
        reg = self.update_i2c_data(latch_off_en)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
    
    def update_i2c_data(self, latch_off_en):
        reg:TURN_OFF_PSU = process_turn_off_psu_command(latch_off_en=latch_off_en)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        latch_off_en = self.latch_off_en.isChecked()
        ui_params = [latch_off_en]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.latch_off_en.setChecked(ui_params[0])
        self.text_change_flag = True
    
class INNO4_DCM_ONLY_Reg_UI():
    """Creates an I2C control UI frame for DCM Only command register"""
    reg_label = 'DCM Only'
    reg_address = Inno4Pro_I2C_Registers.DCM_ONLY_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = DCM_ONLY()
        reg_name = 'dcm_only_reg'
        self.reg_label = 'DCM Only'
        self.reg_address = Inno4Pro_I2C_Registers.DCM_ONLY_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=3,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.thresh_mV =  UIObject(name = f'cbx_{page_name}_{reg_name}_threshold_mV',object_type=UIComboBoxObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.thresh_mV:UIComboBoxObject = self.thresh_mV.add_combobox_to_grid_frame(options_list=DCMOnlyList,\
                                frame=self.frame,grid_layout=self.gridLayout)

        self.dcm_only_en =  UIObject(name = f'chkbox_{page_name}_{reg_name}_enable',object_type=UICheckboxObject,
                            row_index=3,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.dcm_only_en:UICheckboxObject = self.dcm_only_en.add_checkbox_to_grid_frame(name="DCM Only Enable", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=3,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.validate()
        self.thresh_mV.currentIndexChanged.connect(self.validate)
        self.dcm_only_en.clicked.connect(self.validate)
    
    def validate(self):
        match self.thresh_mV.currentText():
            case INNO4_I2C_DCM_ONLY_OPTIONS.THRESHOLD_25MV:
                threshold_mV = commands.DCM_ONLY_THRESHOLD_25MV
            case INNO4_I2C_DCM_ONLY_OPTIONS.THRESHOLD_50MV:
                threshold_mV = commands.DCM_ONLY_THRESHOLD_50MV
            case INNO4_I2C_DCM_ONLY_OPTIONS.THRESHOLD_75MV:
                threshold_mV = commands.DCM_ONLY_THRESHOLD_75MV
            case INNO4_I2C_DCM_ONLY_OPTIONS.THRESHOLD_100MV:
                threshold_mV = commands.DCM_ONLY_THRESHOLD_100MV
        
        dcm_only_en = self.dcm_only_en.isChecked()
        reg = self.update_i2c_data(threshold_mV,dcm_only_en)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
    
    def update_i2c_data(self, threshold_mV,dcm_only_en):
        reg:TURN_OFF_PSU = process_dcm_only_command(threshold=threshold_mV,enable=dcm_only_en)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        thresh_mV_index = self.thresh_mV.currentIndex()
        dcm_only_en = self.dcm_only_en.isChecked()
        ui_params = [thresh_mV_index,dcm_only_en]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.thresh_mV.setCurrentIndex(ui_params[0])
        self.dcm_only_en.setChecked(ui_params[1])
        self.text_change_flag = True

class INNO4_INT_MASK_Reg_UI():
    """Creates an I2C control UI frame for Interrupt Mask command register"""
    reg_label = 'Interrupt Mask'
    reg_address = Inno4Pro_I2C_Registers.INT_MASK_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = INT_MASK()
        reg_name = 'int_mask_reg'
        self.reg_label = 'Interrupt Mask'
        self.reg_address = Inno4Pro_I2C_Registers.INT_MASK_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=6,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)

        self.omf =  UIObject(name = f'chkbox_{page_name}_{reg_name}_omf',object_type=UICheckboxObject,
                            row_index=2,col_index=1,row_span=1,col_span=2,min_width=0, min_height=30)
        self.omf:UICheckboxObject = self.omf.add_checkbox_to_grid_frame(name="OMF", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.vbussc =  UIObject(name = f'chkbox_{page_name}_{reg_name}_vbussc',object_type=UICheckboxObject,
                            row_index=3,col_index=1,row_span=1,col_span=2,min_width=50, min_height=30)
        self.vbussc:UICheckboxObject = self.vbussc.add_checkbox_to_grid_frame(name="VBUSSC", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.control_s =  UIObject(name = f'chkbox_{page_name}_{reg_name}_control_s',object_type=UICheckboxObject,
                            row_index=4,col_index=1,row_span=1,col_span=2,min_width=50, min_height=30)
        self.control_s:UICheckboxObject = self.control_s.add_checkbox_to_grid_frame(name="CTRL S", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.latch_off =  UIObject(name = f'chkbox_{page_name}_{reg_name}_latch_off',object_type=UICheckboxObject,
                            row_index=5,col_index=1,row_span=1,col_span=2,min_width=50, min_height=30)
        self.latch_off:UICheckboxObject = self.latch_off.add_checkbox_to_grid_frame(name="Latch-OFF", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cvol =  UIObject(name = f'chkbox_{page_name}_{reg_name}_cvol',object_type=UICheckboxObject,
                            row_index=2,col_index=3,row_span=1,col_span=2,min_width=50, min_height=30)
        self.cvol:UICheckboxObject = self.cvol.add_checkbox_to_grid_frame(name="CVO", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.issc =  UIObject(name = f'chkbox_{page_name}_{reg_name}_issc',object_type=UICheckboxObject,
                            row_index=3,col_index=3,row_span=1,col_span=2,min_width=50, min_height=30)
        self.issc:UICheckboxObject = self.issc.add_checkbox_to_grid_frame(name="ISSC", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.ccsc =  UIObject(name = f'chkbox_{page_name}_{reg_name}_ccsc',object_type=UICheckboxObject,
                            row_index=4,col_index=3,row_span=1,col_span=2,min_width=50, min_height=30)
        self.ccsc:UICheckboxObject = self.ccsc.add_checkbox_to_grid_frame(name="CCSC", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.uv =  UIObject(name = f'chkbox_{page_name}_{reg_name}_uv',object_type=UICheckboxObject,
                            row_index=5,col_index=3,row_span=1,col_span=2,min_width=50, min_height=30)
        self.uv:UICheckboxObject = self.uv.add_checkbox_to_grid_frame(name="UVA", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.ov =  UIObject(name = f'chkbox_{page_name}_{reg_name}_ov',object_type=UICheckboxObject,
                            row_index=2,col_index=5,row_span=1,col_span=2,min_width=50, min_height=30)
        self.ov:UICheckboxObject = self.ov.add_checkbox_to_grid_frame(name="OVA", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=7,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=7,row_span=3,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=5,col_index=7,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.validate()
        self.omf.clicked.connect(self.validate)
        self.vbussc.clicked.connect(self.validate)
        self.control_s.clicked.connect(self.validate)
        self.latch_off.clicked.connect(self.validate)
        self.cvol.clicked.connect(self.validate)
        self.issc.clicked.connect(self.validate)
        self.ccsc.clicked.connect(self.validate)
        self.uv.clicked.connect(self.validate)
        self.ov.clicked.connect(self.validate)
    
    def validate(self):
        omf = self.omf.isChecked()
        vbussc =self.vbussc.isChecked()
        control_s =self.control_s.isChecked()
        latch_off =self.latch_off.isChecked()
        cvol =self.cvol.isChecked()
        issc =self.issc.isChecked()
        ccsc =self.ccsc.isChecked()
        uv =self.uv.isChecked()
        ov =self.ov.isChecked()
            
        reg = self.update_i2c_data(omf=omf,vbussc=vbussc,control_s=control_s,latch_off=latch_off,cvol=cvol,issc=issc,ccsc=ccsc,uv=uv,ov=ov)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
    
    def update_i2c_data(self, omf,vbussc,control_s,latch_off,cvol,issc,ccsc,uv,ov):
        reg:INT_MASK = process_int_mask_command(omf=omf,vbussc=vbussc,control_s=control_s,latch_off=latch_off,cvol=cvol,issc=issc,ccsc=ccsc,uv=uv,ov=ov)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg   
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        omf = self.omf.isChecked()
        vbussc = self.vbussc.isChecked()
        control_s = self.control_s.isChecked()
        latch_off = self.latch_off.isChecked()
        cvol = self.cvol.isChecked()
        issc = self.issc.isChecked()
        ccsc = self.ccsc.isChecked()
        uv = self.uv.isChecked()
        ov =self.ov.isChecked()
        ui_params = [omf,vbussc,control_s,latch_off,cvol,issc,ccsc,uv,ov]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.omf.setChecked(ui_params[0])
        self.vbussc.setChecked(ui_params[1])
        self.control_s.setChecked(ui_params[2])
        self.latch_off.setChecked(ui_params[3])
        self.cvol.setChecked(ui_params[4])
        self.issc.setChecked(ui_params[5])
        self.ccsc.setChecked(ui_params[6])
        self.uv.setChecked(ui_params[7])
        self.ov.setChecked(ui_params[8])
        self.text_change_flag = True

class INNO4_FWD_PEAK_Reg_UI():
    """Creates an I2C control UI frame for FWD Peak command register"""
    reg_label = 'FWD Peak'
    reg_address = Inno4Pro_I2C_Registers.FWD_PEAK_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = FWD_PEAK()
        reg_name = 'fwd_pk_reg'
        self.reg_label = 'FWD Peak'
        self.reg_address = Inno4Pro_I2C_Registers.FWD_PEAK_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=3,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.pre_shift_ns =  UIObject(name = f'cbx_{page_name}_{reg_name}_pre_shift_ns',object_type=UIComboBoxObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.pre_shift_ns:UIComboBoxObject = self.pre_shift_ns.add_combobox_to_grid_frame(options_list=FWDPeakPreShiftList,\
                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.window_pct =  UIObject(name = f'cbx_{page_name}_{reg_name}_window_pct',object_type=UIComboBoxObject,
                            row_index=3,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.window_pct:UIComboBoxObject = self.window_pct.add_combobox_to_grid_frame(options_list=FWDPeakWindowList,\
                                frame=self.frame,grid_layout=self.gridLayout)
        
        self.fwd_peak_en =  UIObject(name = f'chkbox_{page_name}_{reg_name}_fwd_peak_enable',object_type=UICheckboxObject,
                            row_index=4,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.fwd_peak_en:UICheckboxObject = self.fwd_peak_en.add_checkbox_to_grid_frame(name="FWD Peak Enable", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=2,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=4,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        self.text_change_flag = True
        self.validate()
        self.pre_shift_ns.currentIndexChanged.connect(self.validate)
        self.window_pct.currentIndexChanged.connect(self.validate)
        self.fwd_peak_en.stateChanged.connect(self.validate)

    
    def validate(self):
        match self.pre_shift_ns.currentText():
            case INNO4_I2C_FWD_PEAK_OPTIONS.PRE_SHIFT_0_NS:
                pre_shift_ns = commands.FWD_PEAK_PRESHIFT_0NS
            case INNO4_I2C_FWD_PEAK_OPTIONS.PRE_SHIFT_30_NS:
                pre_shift_ns = commands.FWD_PEAK_PRESHIFT_30NS
            case INNO4_I2C_FWD_PEAK_OPTIONS.PRE_SHIFT_60_NS:
                pre_shift_ns = commands.FWD_PEAK_PRESHIFT_60NS
            case INNO4_I2C_FWD_PEAK_OPTIONS.PRE_SHIFT_90_NS:
                pre_shift_ns = commands.FWD_PEAK_PRESHIFT_90NS
                
        match self.window_pct.currentText():
            case INNO4_I2C_FWD_PEAK_OPTIONS.WINDOW_30_50_PCT:
                window_pct = commands.FWD_PEAK_WINDOW_30_50_PCT
            case INNO4_I2C_FWD_PEAK_OPTIONS.WINDOW_25_45_PCT:
                window_pct = commands.FWD_PEAK_WINDOW_25_45_PCT
            case INNO4_I2C_FWD_PEAK_OPTIONS.WINDOW_20_40_PCT:
                window_pct = commands.FWD_PEAK_WINDOW_20_40_PCT
            case INNO4_I2C_FWD_PEAK_OPTIONS.WINDOW_15_35_PCT:
                window_pct = commands.FWD_PEAK_WINDOW_15_35_PCT
            
        fwd_peak_en= self.fwd_peak_en.isChecked()
        reg = self.update_i2c_data(pre_shift_ns,window_pct,fwd_peak_en)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
        
    def update_i2c_data(self,pre_shift_ns,window_pct,fwd_peak_en):
        reg:FWD_PEAK = process_fwd_peak_command(pre_shift_ns=pre_shift_ns,window_pct=window_pct,fwd_peak_en=fwd_peak_en)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg     
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        pre_shift_ns_index = self.pre_shift_ns.currentIndex()
        window_pct_index = self.window_pct.currentIndex()
        fwd_peak_en = self.fwd_peak_en.isChecked()
        ui_params = [pre_shift_ns_index,window_pct_index,fwd_peak_en]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.pre_shift_ns.setCurrentIndex(ui_params[0])
        self.window_pct.setCurrentIndex(ui_params[1])
        self.fwd_peak_en.setChecked(ui_params[2])
        self.text_change_flag = True 

class INNO4_LOOP_SPEED_1_Reg_UI():
    """Creates an I2C control UI frame for SR ZVS command register"""
    reg_label = 'Loop Speed 1'
    reg_address = Inno4Pro_I2C_Registers.LOOPSPEED_1_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = LOOPSPEED_1()
        reg_name = 'loop_speed1_reg'
        self.reg_label = 'Loop Speed 1'
        self.reg_address = Inno4Pro_I2C_Registers.LOOPSPEED_1_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=3,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.cv_small_step_thresh_mv = UIObject(name = f'lineedit_{page_name}_{reg_name}_cv_small_step_thresh_mv',object_type=UILineEditObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.cv_small_step_thresh_mv:UILineEditObject = self.cv_small_step_thresh_mv.add_lineedit_to_grid_frame(placeholder="CV Small Step Threshold (mV)",max_value=params.LS1_MAX_THRESH_MV,min_value=params.LS1_MIN_THRESH_MV,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cv_large_step_thresh_mv = UIObject(name = f'lineedit_{page_name}_{reg_name}_cv_large_step_thresh_mv',object_type=UILineEditObject,
                            row_index=3,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.cv_large_step_thresh_mv:UILineEditObject = self.cv_large_step_thresh_mv.add_lineedit_to_grid_frame(placeholder="CV Large Step Threshold (mV)",max_value=params.LS1_MAX_THRESH_MV,min_value=params.LS1_MIN_THRESH_MV,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=3,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        self.text_change_flag = True
        self.validate()
        self.cv_small_step_thresh_mv.textChanged.connect(self.validate)
        self.cv_large_step_thresh_mv.textChanged.connect(self.validate)
    
    def validate(self):
        if self.text_change_flag == False:
            return None,None,None
        
        if not self.cv_small_step_thresh_mv.text() == '':
            cv_small_step_thresh_mv = rounded_float(self.cv_small_step_thresh_mv.text())
            if cv_small_step_thresh_mv >= params.LS1_MIN_THRESH_MV:        
                if not (cv_small_step_thresh_mv == set_in_range(cv_small_step_thresh_mv,params.LS1_MAX_THRESH_MV,params.LS1_MIN_THRESH_MV)):
                    cv_small_step_thresh_mv = set_in_range(cv_small_step_thresh_mv,params.LS1_MAX_THRESH_MV,params.LS1_MIN_THRESH_MV)
                    self.text_change_flag = False
                    self.cv_small_step_thresh_mv.setText(f'{cv_small_step_thresh_mv:g}')
                    self.text_change_flag = True
        
        if not self.cv_large_step_thresh_mv.text() == '':
            cv_large_step_thresh_mv = rounded_float(self.cv_large_step_thresh_mv.text())
            if cv_large_step_thresh_mv >= params.LS1_MIN_THRESH_MV:
                if not (cv_large_step_thresh_mv == set_in_range(cv_large_step_thresh_mv,params.LS1_MAX_THRESH_MV,params.LS1_MIN_THRESH_MV)):
                    cv_large_step_thresh_mv = set_in_range(cv_large_step_thresh_mv,params.LS1_MAX_THRESH_MV,params.LS1_MIN_THRESH_MV)
                    self.text_change_flag = False
                    self.cv_large_step_thresh_mv.setText(f'{cv_large_step_thresh_mv:g}')
                    self.text_change_flag = True        

        if (self.cv_small_step_thresh_mv.text() == ''):
            return None, None, None
        if (self.cv_large_step_thresh_mv.text() == ''):
            return None, None, None
        if (cv_small_step_thresh_mv < params.LS1_MIN_THRESH_MV):
            return None, None, None
        if (cv_large_step_thresh_mv < params.LS1_MIN_THRESH_MV):
            return None, None, None
        
        reg = self.update_i2c_data(cv_small_step_thresh_mv=cv_small_step_thresh_mv,cv_large_step_thresh_mv=cv_large_step_thresh_mv)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
        
            
    def update_i2c_data(self,cv_small_step_thresh_mv,cv_large_step_thresh_mv):
        reg:LOOPSPEED_1 = process_loop_speed1_command(cv_small_step_thresh_mv=cv_small_step_thresh_mv,cv_large_step_thresh_mv=cv_large_step_thresh_mv)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg     
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        cv_small_step_thresh_mv_text = self.cv_small_step_thresh_mv.text()
        cv_large_step_thresh_mv_text = self.cv_large_step_thresh_mv.text()
        ui_params = [cv_small_step_thresh_mv_text,cv_large_step_thresh_mv_text]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.cv_small_step_thresh_mv.setText(ui_params[0])
        self.cv_large_step_thresh_mv.setText(ui_params[1])
        self.text_change_flag = True

class INNO4_LOOP_SPEED_2_Reg_UI():
    """Creates an I2C control UI frame for SR ZVS command register"""
    reg_label = 'Loop Speed 2'
    reg_address = Inno4Pro_I2C_Registers.LOOPSPEED_2_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = LOOPSPEED_2()
        reg_name = 'loop_speed2_reg'
        self.reg_label = 'Loop Speed 2'
        self.reg_address = Inno4Pro_I2C_Registers.LOOPSPEED_2_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=3,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.small_step_size_mv = UIObject(name = f'lineedit_{page_name}_{reg_name}_small_step_size_mv',object_type=UILineEditObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.small_step_size_mv:UILineEditObject = self.small_step_size_mv.add_lineedit_to_grid_frame(placeholder="Small Step Size (mV)",max_value=params.LS2_MAX_STEP_MV,min_value=params.LS2_MIN_STEP_MV,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.large_step_size_mv = UIObject(name = f'lineedit_{page_name}_{reg_name}_large_step_size_mv',object_type=UILineEditObject,
                            row_index=3,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.large_step_size_mv:UILineEditObject = self.large_step_size_mv.add_lineedit_to_grid_frame(placeholder="Large Step Size (mV)",max_value=params.LS2_MAX_STEP_MV,min_value=params.LS2_MIN_STEP_MV,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cc_small_step_thresh_lsb = UIObject(name = f'lineedit_{page_name}_{reg_name}_cc_small_step_thresh_lsb',object_type=UILineEditObject,
                            row_index=4,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.cc_small_step_thresh_lsb:UILineEditObject = self.cc_small_step_thresh_lsb.add_lineedit_to_grid_frame(placeholder="CC Small Step Threshold (LSB)",max_value=params.LS2_MAX_THRESH_COUNT,min_value=params.LS2_MIN_THRESH_COUNT,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        validator = QIntValidator(params.LS2_MIN_THRESH_COUNT, params.LS2_MAX_THRESH_COUNT)
        self.cc_small_step_thresh_lsb.setValidator(validator)
        
        self.cc_large_step_thresh_lsb = UIObject(name = f'lineedit_{page_name}_{reg_name}_cc_large_step_thresh_lsb',object_type=UILineEditObject,
                            row_index=5,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.cc_large_step_thresh_lsb:UILineEditObject = self.cc_large_step_thresh_lsb.add_lineedit_to_grid_frame(placeholder="CC Large Step Threshold (LSB)",max_value=params.LS2_MAX_THRESH_COUNT,min_value=params.LS2_MIN_THRESH_COUNT,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cc_large_step_thresh_lsb.setValidator(validator)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=3,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=5,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        self.text_change_flag = True
        self.validate()
        self.small_step_size_mv.textChanged.connect(self.validate)
        self.large_step_size_mv.textChanged.connect(self.validate)
        self.cc_small_step_thresh_lsb.textChanged.connect(self.validate)
        self.cc_large_step_thresh_lsb.textChanged.connect(self.validate)
        
    def validate(self):
        if self.text_change_flag == False:
            return None,None,None
        
        if not self.small_step_size_mv.text() == '':
            small_step_size_mv = rounded_float(self.small_step_size_mv.text())
            if small_step_size_mv >= params.LS2_MIN_STEP_MV:
                if not (small_step_size_mv == set_in_range(small_step_size_mv,params.LS2_MAX_STEP_MV,params.LS2_MIN_STEP_MV)):
                    small_step_size_mv = set_in_range(small_step_size_mv,params.LS2_MAX_STEP_MV,params.LS2_MIN_STEP_MV)
                    self.text_change_flag = False
                    self.small_step_size_mv.setText(f'{small_step_size_mv:g}')
                    self.text_change_flag = True
            
        if not self.large_step_size_mv.text() == '':
            large_step_size_mv = rounded_float(self.large_step_size_mv.text())
            if large_step_size_mv >= params.LS2_MIN_STEP_MV:
                if not (large_step_size_mv == set_in_range(large_step_size_mv,params.LS2_MAX_STEP_MV,params.LS2_MIN_STEP_MV)):
                    large_step_size_mv = set_in_range(large_step_size_mv,params.LS2_MAX_STEP_MV,params.LS2_MIN_STEP_MV)
                    self.text_change_flag = False
                    self.large_step_size_mv.setText(f'{large_step_size_mv:g}')
                    self.text_change_flag = True      
            
        if not self.cc_small_step_thresh_lsb.text() == '':
            cc_small_step_thresh_lsb = rounded_float(self.cc_small_step_thresh_lsb.text())
            if cc_small_step_thresh_lsb >= params.LS2_MIN_THRESH_COUNT:
                if not (cc_small_step_thresh_lsb == set_in_range(cc_small_step_thresh_lsb,params.LS2_MAX_THRESH_COUNT,params.LS2_MIN_THRESH_COUNT)):
                    cc_small_step_thresh_lsb = set_in_range(cc_small_step_thresh_lsb,params.LS2_MAX_THRESH_COUNT,params.LS2_MIN_THRESH_COUNT)
                    self.text_change_flag = False
                    self.cc_small_step_thresh_lsb.setText(f'{cc_small_step_thresh_lsb:g}')
                    self.text_change_flag = True
        
        if not self.cc_large_step_thresh_lsb.text() == '':
            cc_large_step_thresh_lsb = rounded_float(self.cc_large_step_thresh_lsb.text())         
            if cc_large_step_thresh_lsb >= params.LS2_MIN_THRESH_COUNT:
                if not (cc_large_step_thresh_lsb == set_in_range(cc_large_step_thresh_lsb,params.LS2_MAX_THRESH_COUNT,params.LS2_MIN_THRESH_COUNT)):
                    cc_large_step_thresh_lsb = set_in_range(cc_large_step_thresh_lsb,params.LS2_MAX_THRESH_COUNT,params.LS2_MIN_THRESH_COUNT)
                    self.text_change_flag = False
                    self.cc_large_step_thresh_lsb.setText(f'{cc_large_step_thresh_lsb:g}')
                    self.text_change_flag = True       
            
        if self.small_step_size_mv.text() == '':
            return None,None,None       
        
        if self.large_step_size_mv.text() == '':
            return None,None,None
        
        if self.cc_small_step_thresh_lsb.text() == '':
            return None,None,None
        
        if self.cc_large_step_thresh_lsb.text() == '':
            return None,None,None
        
        if small_step_size_mv < params.LS2_MIN_STEP_MV:
            return None,None,None
        
        if large_step_size_mv < params.LS2_MIN_STEP_MV:
            return None,None,None
           
        if cc_small_step_thresh_lsb < params.LS2_MIN_THRESH_COUNT:
            return None,None,None  
        
        if cc_large_step_thresh_lsb < params.LS2_MIN_THRESH_COUNT:
            return None,None,None   
        
        reg = self.update_i2c_data(small_step_size_mv=small_step_size_mv,large_step_size_mv=large_step_size_mv,cc_small_step_thresh_lsb=cc_small_step_thresh_lsb,cc_large_step_thresh_lsb=cc_large_step_thresh_lsb)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
        
    def update_i2c_data(self,small_step_size_mv,large_step_size_mv,cc_small_step_thresh_lsb,cc_large_step_thresh_lsb):
        reg:LOOPSPEED_2 = process_loop_speed2_command(small_step_size_mv=small_step_size_mv,large_step_size_mv=large_step_size_mv,
                                                      cc_small_step_thresh_lsb=cc_small_step_thresh_lsb,cc_large_step_thresh_lsb=cc_large_step_thresh_lsb)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg  
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        small_step_size_mv_text = self.small_step_size_mv.text()
        large_step_size_mv_text = self.large_step_size_mv.text()
        cc_small_step_thresh_lsb_text = self.cc_small_step_thresh_lsb.text()
        cc_large_step_thresh_lsb_text = self.cc_large_step_thresh_lsb.text()
        ui_params = [small_step_size_mv_text,large_step_size_mv_text,cc_small_step_thresh_lsb_text,cc_large_step_thresh_lsb_text]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.small_step_size_mv.setText(ui_params[0])
        self.large_step_size_mv.setText(ui_params[1])
        self.cc_small_step_thresh_lsb.setText(ui_params[2])
        self.cc_large_step_thresh_lsb.setText(ui_params[3])
        self.text_change_flag = True
    
class INNO4_FAST_CC_Reg_UI():
    """Creates an I2C control UI frame for Fast CC command register"""
    reg_label = 'Fast CC'
    reg_address = Inno4Pro_I2C_Registers.FAST_CC_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = FAST_CC()
        reg_name = 'fast_cc_reg'
        self.reg_label = 'Fast CC'
        self.reg_address = Inno4Pro_I2C_Registers.FAST_CC_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=3,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.fast_cc_offset = UIObject(name = f'lineedit_{page_name}_{reg_name}_fast_cc_offset',object_type=UILineEditObject,
                            row_index=2,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.fast_cc_offset:UILineEditObject = self.fast_cc_offset.add_lineedit_to_grid_frame(placeholder="Fast CC Offset",max_value=params.FAST_CC_OFFSET_MAX_COUNT,min_value=params.FAST_CC_OFFSET_MIN_COUNT,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        fast_cc_validator = QIntValidator(params.FAST_CC_OFFSET_MIN_COUNT, params.FAST_CC_OFFSET_MAX_COUNT)
        self.fast_cc_offset.setValidator(fast_cc_validator)
        
        self.slow_cc_offset = UIObject(name = f'lineedit_{page_name}_{reg_name}_slow_cc_offset',object_type=UILineEditObject,
                            row_index=3,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.slow_cc_offset:UILineEditObject = self.slow_cc_offset.add_lineedit_to_grid_frame(placeholder="Slow CC Offset",max_value=params.SLOW_CC_OFFSET_MAX_COUNT,min_value=params.SLOW_CC_OFFSET_MIN_COUNT,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        slow_cc_validator = QIntValidator(params.SLOW_CC_OFFSET_MIN_COUNT, params.SLOW_CC_OFFSET_MAX_COUNT)
        self.slow_cc_offset.setValidator(slow_cc_validator)
        
        self.calibration_disable =  UIObject(name = f'chkbox_{page_name}_{reg_name}_calibration_disable',object_type=UICheckboxObject,
                            row_index=4,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.calibration_disable:UICheckboxObject = self.calibration_disable.add_checkbox_to_grid_frame(name="Calibration Disable", init_state=True, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.fast_cc_enable =  UIObject(name = f'chkbox_{page_name}_{reg_name}_fast_cc_enable',object_type=UICheckboxObject,
                            row_index=5,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        self.fast_cc_enable:UICheckboxObject = self.fast_cc_enable.add_checkbox_to_grid_frame(name="Fast CC Enable", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=4,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=4,row_span=3,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=5,col_index=4,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        self.text_change_flag = True
        self.validate()
        self.fast_cc_offset.textChanged.connect(self.validate)
        self.slow_cc_offset.textChanged.connect(self.validate)
        self.calibration_disable.stateChanged.connect(self.validate)
        self.fast_cc_enable.stateChanged.connect(self.validate)
    
    def validate(self):
        if self.text_change_flag == False:
            return None,None,None
        
        if not self.fast_cc_offset.text() == '':
            fast_cc_offset = rounded_float(self.fast_cc_offset.text())
            if fast_cc_offset >= params.FAST_CC_OFFSET_MIN_COUNT:
                if not (fast_cc_offset == set_in_range(fast_cc_offset,params.FAST_CC_OFFSET_MAX_COUNT,params.FAST_CC_OFFSET_MIN_COUNT)):
                    fast_cc_offset = set_in_range(fast_cc_offset,params.FAST_CC_OFFSET_MAX_COUNT,params.FAST_CC_OFFSET_MIN_COUNT)
                    self.text_change_flag = False
                    self.fast_cc_offset.setText(f'{fast_cc_offset:g}')
                    self.text_change_flag = True
                            
        if not self.slow_cc_offset.text() == '':     
            slow_cc_offset = rounded_float(self.slow_cc_offset.text())
            if slow_cc_offset >= params.SLOW_CC_OFFSET_MIN_COUNT:      
                if not (slow_cc_offset == set_in_range(slow_cc_offset,params.SLOW_CC_OFFSET_MAX_COUNT,params.SLOW_CC_OFFSET_MIN_COUNT)):
                    slow_cc_offset = set_in_range(slow_cc_offset,params.SLOW_CC_OFFSET_MAX_COUNT,params.SLOW_CC_OFFSET_MIN_COUNT)
                    self.text_change_flag = False
                    self.slow_cc_offset.setText(f'{slow_cc_offset:g}')
                    self.text_change_flag = True   
                    
        if self.fast_cc_offset.text() == '':
            return None,None,None
        if self.slow_cc_offset.text() == '':
            return None,None,None
        if (fast_cc_offset < params.FAST_CC_OFFSET_MIN_COUNT):
            return None,None,None
        if (slow_cc_offset < params.SLOW_CC_OFFSET_MIN_COUNT):
            return None,None,None
                    
        calibration_disable = self.calibration_disable.isChecked()
        fast_cc_enable = self.fast_cc_enable.isChecked()  
        reg = self.update_i2c_data(fast_cc_offset=fast_cc_offset,slow_cc_offset=slow_cc_offset,calibration_disable=calibration_disable,fast_cc_enable=fast_cc_enable)
        i2c_data = u16()
        i2c_data.asbyte = reg.asbyte
        data_lsb = i2c_data.bits.byte2
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            data_msb = i2c_data.bits.byte1
            return self.reg_address, data_lsb, data_msb
        else:
            return self.reg_address, data_lsb, None
        
    def update_i2c_data(self,fast_cc_offset,slow_cc_offset,calibration_disable,fast_cc_enable):
        reg:FAST_CC = process_fast_cc_command(fast_cc_offset=fast_cc_offset,slow_cc_offset=slow_cc_offset,calibration_disable=calibration_disable,fast_cc_enable=fast_cc_enable)
        if reg is None:
            return None
        if self.reg_address not in INNO4_PRO_SINGLE_BYTE_COMMAND_LIST:
            self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        else:
            self.i2c_data.setText(f'0x{reg.asbyte:02X}')
        return reg     
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        fast_cc_offset_text = self.fast_cc_offset.text()
        slow_cc_offset_text = self.slow_cc_offset.text()
        calibration_disable = self.calibration_disable.isChecked()
        fast_cc_enable = self.fast_cc_enable.isChecked()
        ui_params = [fast_cc_offset_text,slow_cc_offset_text,calibration_disable,fast_cc_enable]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.fast_cc_offset.setText(ui_params[0])
        self.slow_cc_offset.setText(ui_params[1])
        self.calibration_disable.setChecked(ui_params[2])
        self.fast_cc_enable.setChecked(ui_params[3])
        self.text_change_flag = True   

# Special Registers

class INNO4_LOOP_OPTION_Reg_UI():
    """Creates an I2C control UI frame for Loop option command register"""
    reg_label = 'Loop Option'
    reg_address = Inno4Pro_I2C_Registers.LOOP_OPTION_REG
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = None
        reg_name = 'loop_option_reg'
        self.reg_label = 'Loop Option'
        self.reg_address = Inno4Pro_I2C_Registers.LOOP_OPTION_REG
        label = f'{self.reg_label}, 0x{self.reg_address:02X}'
        
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.loop_option = UIObject(name = f'cbx_{page_name}_{reg_name}_option',object_type=UIComboBoxObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=90, min_height=30)
        self.loop_option:UIComboBoxObject = self.loop_option.add_combobox_to_grid_frame(options_list=LoopOptionList,\
                                        frame=self.frame,grid_layout=self.gridLayout)

        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x8080',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=4,col_index=1,row_span=1,col_span=1,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=5,col_index=1,row_span=1,col_span=1,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
    
        self.validate()
        self.loop_option.currentIndexChanged.connect(self.validate)
    
    def validate(self):
        match self.loop_option.currentText():
            case INNO4_I2C_LOOP_OPTIONS.DEFAULT:
                loop_option_lsb = commands.LOOP_OPTION_DEF_LSB
                loop_option_msb = commands.LOOP_OPTION_DEF_MSB
            case INNO4_I2C_LOOP_OPTIONS.OPTION1:
                loop_option_lsb = commands.LOOP_OPTION1_LSB
                loop_option_msb = commands.LOOP_OPTION1_MSB
            case INNO4_I2C_LOOP_OPTIONS.OPTION2:
                loop_option_lsb = commands.LOOP_OPTION2_LSB
                loop_option_msb = commands.LOOP_OPTION2_MSB
        self.update_i2c_data(loop_option_lsb,loop_option_msb)
        data_lsb = loop_option_lsb
        data_msb = loop_option_msb
        return self.reg_address, data_lsb, data_msb
    
    def update_i2c_data(self,loop_option_lsb,loop_option_msb):
        self.i2c_data.setText(f'0x{loop_option_msb:02X}{loop_option_lsb:02X}')
        return 
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        loop_option_index = self.loop_option.currentIndex()
        ui_params = [loop_option_index]
        value = self.i2c_data.text()
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.loop_option.setCurrentIndex(ui_params[0])
        self.text_change_flag = True
        
# General write command

class INNO4_WRITE_REG_UI():
    """Creates an I2C control UI frame for a general write command to a register"""
    reg_label = 'Write Reg'
    reg_address = None
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = None
        reg_name = 'write_command_reg'
        self.reg_label = 'Write Reg'
        self.reg_address = None
        label = f'Write to Register: 0x00'
        
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=4,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)
            
        self.reg_address_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_address_label',object_type=UILabelObject, 
                                          row_index=2,col_index=1,row_span=1,col_span=2,min_width=80,min_height=30)
        self.reg_address_label:UILabelObject = self.reg_address_label.add_label_to_grid_frame(name='Address:',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_address = UIObject(name = f'cbx_{page_name}_{reg_name}_option',object_type=UILineEditObject,
                            row_index=2,col_index=3,row_span=1,col_span=2,min_width=20, min_height=30)
        self.reg_address:UILineEditObject = self.reg_address.add_lineedit_to_grid_frame(placeholder= '0x12',max_value=999,min_value=0,\
                                        frame=self.frame,grid_layout=self.gridLayout)
                
        self.data_msb_label = UIObject(name=f'label_{page_name}_{reg_name}_data_lsb_label',object_type=UILabelObject, 
                                          row_index=3,col_index=1,row_span=1,col_span=2,min_width=80,min_height=30)
        self.data_msb_label:UILabelObject = self.data_msb_label.add_label_to_grid_frame(name='Data MSB:',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.data_msb = UIObject(name = f'cbx_{page_name}_{reg_name}_option',object_type=UILineEditObject,
                            row_index=3,col_index=3,row_span=1,col_span=2,min_width=20, min_height=30)
        self.data_msb:UILineEditObject = self.data_msb.add_lineedit_to_grid_frame(placeholder= '0x12',max_value=9,min_value=0,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.data_lsb_label = UIObject(name=f'label_{page_name}_{reg_name}_data_lsb_label',object_type=UILabelObject, 
                                          row_index=4,col_index=1,row_span=1,col_span=2,min_width=80,min_height=30)
        self.data_lsb_label:UILabelObject = self.data_lsb_label.add_label_to_grid_frame(name='Data LSB:',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.data_lsb = UIObject(name = f'cbx_{page_name}_{reg_name}_option',object_type=UILineEditObject,
                            row_index=4,col_index=3,row_span=1,col_span=2,min_width=20, min_height=30)
        self.data_lsb:UILineEditObject = self.data_lsb.add_lineedit_to_grid_frame(placeholder= '0x12',max_value=999,min_value=0,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.one_byte_en =  UIObject(name = f'chkbox_{page_name}_{reg_name}_one_byte_en',object_type=UICheckboxObject,
                            row_index=5,col_index=1,row_span=1,col_span=3,min_width=150, min_height=30)
        
        self.one_byte_en:UICheckboxObject = self.one_byte_en.add_checkbox_to_grid_frame(name="One Byte", init_state=False, tristate=False,\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=1,col_index=5,row_span=1,col_span=2,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='0x0000',\
                                        frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=2,col_index=5,row_span=3,col_span=2,min_width=80, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=5,col_index=5,row_span=1,col_span=2,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                        frame=self.frame,grid_layout=self.gridLayout)
        self.text_change_flag = True
        
        validator = QRegExpValidator(QRegExp("^0x[0-9A-F]{1,2}"))
        self.reg_address.setValidator(validator)
        self.data_msb.setValidator(validator)
        self.data_lsb.setValidator(validator)

        self.validate()
        
        self.reg_address.textChanged.connect(self.validate)
        self.data_msb.textChanged.connect(self.validate)
        self.data_lsb.textChanged.connect(self.validate)
        self.one_byte_en.stateChanged.connect(self.validate)    
    
    def validate(self):
        self.one_byte = self.one_byte_en.isChecked()
        if self.one_byte:
            self.data_msb.setEnabled(False)
        else:
            self.data_msb.setEnabled(True)
                       
        if self.text_change_flag == False:
            return None, None, None
         
        if (len(self.data_msb.text()) < 3):
            self.data_msb.setText('0x')
        if (len(self.data_lsb.text()) < 3):
            self.data_lsb.setText('0x')
        if (len(self.reg_address.text()) < 3):
            self.reg_address.setText('0x')
            
        if(len(self.data_lsb.text()) < 3)| ((not self.one_byte) & (len(self.data_msb.text()) < 3)) | (len(self.reg_address.text()) < 3):
            self.update_i2c_data(None,None,None)
            return None, None, None         
        
        try:
            reg_address = int(self.reg_address.text(),16)
            reg_address = add_odd_parity_1byte(reg_address)
        except:
            reg_address = None
            self.update_i2c_data(reg_address,None,None)
            return None, None, None
        
        if (self.data_lsb.text() == '') or ((not self.one_byte) & (self.data_msb.text() == '')):
            self.update_i2c_data(reg_address,None,None)
            return reg_address, None, None
            
        try:
            data_lsb = int(self.data_lsb.text(),16)
            if (not self.one_byte):
                data_msb = int(self.data_msb.text(),16)
                self.update_i2c_data(reg_address,data_lsb,data_msb)
                return reg_address, data_lsb, data_msb
            else:
                self.update_i2c_data(reg_address,data_lsb,None)
                return reg_address, data_lsb, None
        except:
            self.update_i2c_data(reg_address,None,None)
            return reg_address, None, None
            
    
    def update_i2c_data(self,reg_address,data_lsb,data_msb):
        if reg_address is None:
            label = 'Write to Register: 0x00'
        else:
            label = f'Write to Register: 0x{reg_address:02X}'
        self.name.setText(label)
        if self.one_byte:
            if (data_lsb is None):
                self.i2c_data.setText('0x00')
            else:
                self.i2c_data.setText(f'0x{data_lsb:02X}')
        else:
            if (data_lsb is None) & (data_msb is None):
                self.i2c_data.setText('0x0000')
            else:
                self.i2c_data.setText(f'0x{data_msb:02X}{data_lsb:02X}')
        return 
    
    def extract_command_parameters(self):
        param = self.validate()
        if (param[0] is None) & (param[1] is None) & (param[2] is None):
            return None, None
        reg_address_text = self.reg_address.text()
        data_msb_text = self.data_msb.text()
        data_lsb_text = self.data_lsb.text()
        data_lsb = int(data_lsb_text,16)
        one_byte = self.one_byte_en.isChecked()
        if not self.one_byte:
            ui_params = [reg_address_text,data_msb_text,data_lsb_text,one_byte]
            value = f'{reg_address_text}, {data_msb_text}{data_lsb:02X}'
        else:
            ui_params = [reg_address_text,'0x',data_lsb_text,one_byte]
            value = f'{reg_address_text}, 0x{data_lsb:02X}'
        return value, ui_params
    
    def set_parameters_from_list(self,ui_params:list):
        self.text_change_flag = False
        self.reg_address.setText(ui_params[0])
        self.data_msb.setText(ui_params[1])
        self.data_lsb.setText(ui_params[2])
        self.one_byte_en.setChecked(ui_params[3])
        self.text_change_flag = True
    
# General read command

class INNO4_READ_REG_UI():
    """Creates an I2C control UI frame for a general read command to a register"""
    reg_label = 'Read Reg'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = None
        reg_name = 'read_command_reg'
        self.reg_label = 'Read Reg'
        label = f'Readback Register: 0x00'
        self.reg_address_byte = None
        
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=2,row_span=1,col_span=1,min_width=80, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)

        self.reg_address_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_address_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.reg_address_label:UILabelObject = self.reg_address_label.add_label_to_grid_frame(name='Register Address:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_address = UIObject(name = f'cbx_{page_name}_{reg_name}_option',object_type=UILineEditObject,
                            row_index=3,col_index=2,row_span=1,col_span=1,min_width=150, min_height=30)
        self.reg_address:UILineEditObject = self.reg_address.add_lineedit_to_grid_frame(placeholder= 'Register Address:',max_value=999,min_value=0,\
                                        frame=self.frame,grid_layout=self.gridLayout)
        self.text_change_flag = True
        validator = QRegExpValidator(QRegExp("^0x[0-9A-F]{1,2}"))
        self.reg_address.setValidator(validator)
        
        self.validate()
        self.reg_address.textChanged.connect(self.validate)
    
    def validate(self):
        if self.text_change_flag == False:
            return None
        if (len(self.reg_address.text()) < 3):
            self.reg_address_byte = None
            self.reg_address.setText('0x')
            return None
        try:
            self.reg_address_byte = int(self.reg_address.text(),16)            
            return self.update_register_address()
        except:
            self.reg_address.setText('0x')
            self.reg_address_byte = None
            return None
    
    def update_register_address(self):
        if self.reg_address_byte is None:
            self.reg_address.setText('0x')
            return None
        label = f'Readback Register: 0x{self.reg_address_byte:02X}'
        reg_address_text = f'0x{self.reg_address_byte:02X}'
        self.name.setText(label)
        return reg_address_text
    
    def update_i2c_data(self,rb_u16):
        reg = READ0()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        return reg
    
    def set_parameters_from_data(self,reg_address):
        self.text_change_flag = False
        self.reg_address.setText(f'{reg_address}')
        self.text_change_flag = True

class INNO4_READ0_REG_UI():
    """Creates an I2C control UI frame for Read0 register"""
    reg_label = 'READ0'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ0()
        reg_name = 'read0_reg'
        self.reg_label = 'READ0'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ0:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ0
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
    def validate(self):
        pass
    
    def update_i2c_data(self,rb_u16):
        reg = READ0()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        return reg        
    
class INNO4_READ1_REG_UI():
    """Creates an I2C control UI frame for Read1 register"""
    reg_label = 'READ1'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ1()
        reg_name = 'read1_reg'
        self.reg_label = 'READ1'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ1:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ1
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cv_label = UIObject(name=f'label_{page_name}_{reg_name}_cv_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.cv_label:UILabelObject = self.cv_label.add_label_to_grid_frame(name='CV:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cv_data =  UIObject(name=f'label_{page_name}_{reg_name}_cv_data',object_type=UILabelObject,
                            row_index=3,col_index=2,row_span=1,col_span=1,min_width=80,min_height=30)
        self.cv_data:UILabelObject = self.cv_data.add_label_to_grid_frame(name='0 V',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ1()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        cv = process_read1_command(rb_u16)
        cv_V = cv * params.CV_RESOLUTION_MV/1000
        self.cv_data.setText(f'{cv_V:g} V')
        return reg        
        
class INNO4_READ2_REG_UI():
    """Creates an I2C control UI frame for Read2 register"""
    reg_label = 'READ2'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ2()
        reg_name = 'read2_reg'
        self.reg_label = 'READ2'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ2:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ2
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cc_label = UIObject(name=f'label_{page_name}_{reg_name}_cc_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.cc_label:UILabelObject = self.cc_label.add_label_to_grid_frame(name='CC:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cc_data =  UIObject(name=f'label_{page_name}_{reg_name}_cc_data',object_type=UILabelObject,
                            row_index=3,col_index=2,row_span=1,col_span=1,min_width=80,min_height=30)
        self.cc_data:UILabelObject = self.cc_data.add_label_to_grid_frame(name='0',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ2()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        cc = process_read2_command(rb_u16)
        self.cc_data.setText(f'{cc:g}')
        return reg  
    
class INNO4_READ3_REG_UI():
    """Creates an I2C control UI frame for Read3 register"""
    reg_label = 'READ3'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ3()
        reg_name = 'read3_reg'
        self.reg_label = 'READ3'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ3:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ3
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.ov_label = UIObject(name=f'label_{page_name}_{reg_name}_ov_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.ov_label:UILabelObject = self.ov_label.add_label_to_grid_frame(name='OV:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.ov_data =  UIObject(name=f'label_{page_name}_{reg_name}_ov_data',object_type=UILabelObject,
                            row_index=3,col_index=2,row_span=1,col_span=1,min_width=80,min_height=30)
        self.ov_data:UILabelObject = self.ov_data.add_label_to_grid_frame(name='0',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ3()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        ov = process_read3_command(rb_u16)
        ov_V = ov*params.CV_RESOLUTION_MV/1000
        self.ov_data.setText(f'{ov_V:g} V')
        return reg       
            
class INNO4_READ4_REG_UI():
    """Creates an I2C control UI frame for Read4 register"""
    reg_label = 'READ4'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ4()
        reg_name = 'read4_reg'
        self.reg_label = 'READ4'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ4:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ4
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.uv_label = UIObject(name=f'label_{page_name}_{reg_name}_uv_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.uv_label:UILabelObject = self.uv_label.add_label_to_grid_frame(name='UV:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.uv_data =  UIObject(name=f'label_{page_name}_{reg_name}_uv_data',object_type=UILabelObject,
                            row_index=3,col_index=2,row_span=1,col_span=1,min_width=80,min_height=30)
        self.uv_data:UILabelObject = self.uv_data.add_label_to_grid_frame(name='0',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ4()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        uv = process_read4_command(rb_u16)
        uv_V = uv*params.CV_RESOLUTION_MV/1000
        self.uv_data.setText(f'{uv_V:g} V')
        return reg  
    
class INNO4_READ5_REG_UI():
    """Creates an I2C control UI frame for Read5 register"""
    reg_label = 'READ5'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ5()
        reg_name = 'read5_reg'
        self.reg_label = 'READ5'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ5:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ5
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.vkp_label = UIObject(name=f'label_{page_name}_{reg_name}_vkp_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.vkp_label:UILabelObject = self.vkp_label.add_label_to_grid_frame(name='VKP:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.vkp_data =  UIObject(name=f'label_{page_name}_{reg_name}_vkp_data',object_type=UILabelObject,
                            row_index=3,col_index=2,row_span=1,col_span=1,min_width=80,min_height=30)
        self.vkp_data:UILabelObject = self.vkp_data.add_label_to_grid_frame(name='0',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ5()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        vkp = process_read5_command(rb_u16)
        vkp_V = vkp*params.VKP_RESOLUTION_MV / 1000
        self.vkp_data.setText(f'{vkp_V:g} V')
        return reg  
    
class INNO4_READ6_REG_UI():
    """Creates an I2C control UI frame for Read6 register"""
    reg_label = 'READ6'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ6()
        reg_name = 'read6_reg'
        self.reg_label = 'READ6'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ6:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ6
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=2,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=3,row_span=1,col_span=2,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=3,row_span=1,col_span=2,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=2,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cvo_timer_label = UIObject(name=f'label_{page_name}_{reg_name}_cvo_timer_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.cvo_timer_label:UILabelObject = self.cvo_timer_label.add_label_to_grid_frame(name='CVO Timer:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cvo_timer_data = UIObject(name=f'label_{page_name}_{reg_name}_cvo_timer_data',object_type=UILabelObject,
                        row_index=3,col_index=2,row_span=1,col_span=1,min_width=30,min_height=30)
        self.cvo_timer_data:UILabelObject = self.cvo_timer_data.add_label_to_grid_frame(name='',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cvo_response_label = UIObject(name=f'label_{page_name}_{reg_name}_cvo_response_label',object_type=UILabelObject,
                        row_index=4,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.cvo_response_label:UILabelObject = self.cvo_response_label.add_label_to_grid_frame(name='CVO Resp:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cvo_response_data = UIObject(name=f'label_{page_name}_{reg_name}_cvo_response_data',object_type=UILabelObject,
                        row_index=4,col_index=2,row_span=1,col_span=1,min_width=30,min_height=30)
        self.cvo_response_data:UILabelObject = self.cvo_response_data.add_label_to_grid_frame(name='',frame=self.frame,grid_layout=self.gridLayout)
        
        self.watchdog_timer_label = UIObject(name=f'label_{page_name}_{reg_name}_watchdog_timer_label',object_type=UILabelObject,
                        row_index=5,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.watchdog_timer_label:UILabelObject = self.watchdog_timer_label.add_label_to_grid_frame(name='Watchdog:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.watchdog_timer_data = UIObject(name=f'label_{page_name}_{reg_name}_watchdog_timer_data',object_type=UILabelObject,
                        row_index=5,col_index=2,row_span=1,col_span=1,min_width=30,min_height=30)
        self.watchdog_timer_data:UILabelObject = self.watchdog_timer_data.add_label_to_grid_frame(name='',frame=self.frame,grid_layout=self.gridLayout)
        
        self.uva_timer_label = UIObject(name=f'label_{page_name}_{reg_name}_uva_timer_label',object_type=UILabelObject,
                        row_index=6,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.uva_timer_label:UILabelObject = self.uva_timer_label.add_label_to_grid_frame(name='UVA Timer:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.uva_timer_data = UIObject(name=f'label_{page_name}_{reg_name}_uva_timer_data',object_type=UILabelObject,
                        row_index=6,col_index=2,row_span=1,col_span=1,min_width=30,min_height=30)
        self.uva_timer_data:UILabelObject = self.uva_timer_data.add_label_to_grid_frame(name='',frame=self.frame,grid_layout=self.gridLayout)
        
        self.issc_response_label = UIObject(name=f'label_{page_name}_{reg_name}_issc_response_label',object_type=UILabelObject,
                        row_index=3,col_index=3,row_span=1,col_span=1,min_width=30,min_height=30)
        self.issc_response_label:UILabelObject = self.issc_response_label.add_label_to_grid_frame(name='ISSC Resp:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.issc_response_data = UIObject(name=f'label_{page_name}_{reg_name}_issc_response_data',object_type=UILabelObject,
                        row_index=3,col_index=4,row_span=1,col_span=1,min_width=30,min_height=30)
        self.issc_response_data:UILabelObject = self.issc_response_data.add_label_to_grid_frame(name='',frame=self.frame,grid_layout=self.gridLayout)
        
        self.ccsc_response_label = UIObject(name=f'label_{page_name}_{reg_name}_ccsc_response_label',object_type=UILabelObject,
                        row_index=4,col_index=3,row_span=1,col_span=1,min_width=30,min_height=30)
        self.ccsc_response_label:UILabelObject = self.ccsc_response_label.add_label_to_grid_frame(name='CCSC Resp:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.ccsc_response_data = UIObject(name=f'label_{page_name}_{reg_name}_ccsc_response_data',object_type=UILabelObject,
                        row_index=4,col_index=4,row_span=1,col_span=1,min_width=30,min_height=30)
        self.ccsc_response_data:UILabelObject = self.ccsc_response_data.add_label_to_grid_frame(name='',frame=self.frame,grid_layout=self.gridLayout)
        
        self.uva_response_label = UIObject(name=f'label_{page_name}_{reg_name}_uva_response_label',object_type=UILabelObject,
                        row_index=5,col_index=3,row_span=1,col_span=1,min_width=30,min_height=30)
        self.uva_response_label:UILabelObject = self.uva_response_label.add_label_to_grid_frame(name='UVA Resp:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.uva_response_data = UIObject(name=f'label_{page_name}_{reg_name}_uva_response_data',object_type=UILabelObject,
                        row_index=5,col_index=4,row_span=1,col_span=1,min_width=30,min_height=30)
        self.uva_response_data:UILabelObject = self.uva_response_data.add_label_to_grid_frame(name='',frame=self.frame,grid_layout=self.gridLayout)
        
        self.ova_response_label = UIObject(name=f'label_{page_name}_{reg_name}_ova_response_label',object_type=UILabelObject,
                        row_index=6,col_index=3,row_span=1,col_span=1,min_width=30,min_height=30)
        self.ova_response_label:UILabelObject = self.ova_response_label.add_label_to_grid_frame(name='OVA Resp:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.ova_response_data = UIObject(name=f'label_{page_name}_{reg_name}_ova_response_data',object_type=UILabelObject,
                        row_index=6,col_index=4,row_span=1,col_span=1,min_width=30,min_height=30)
        self.ova_response_data:UILabelObject = self.ova_response_data.add_label_to_grid_frame(name='',frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ6()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        cvo_timer, cvo_response, wd_timer, uva_timer, issc_response, ccsc_response, uva_response, ova_response = process_read6_command(rb_u16)
        match cvo_timer:
            case commands.CVO_TIMER_8MS:
                cvo_timer_text = '8 ms'
            case commands.CVO_TIMER_16MS:
                cvo_timer_text = '16 ms'
            case commands.CVO_TIMER_32MS:
                cvo_timer_text = '32 ms'
            case commands.CVO_TIMER_64MS:
                cvo_timer_text = '64 ms'
            case _:
                cvo_timer_text = 'Invalid'
                
        match cvo_response:
            case commands.CVO_RESP_AR:
                cvo_response_text = 'AR'
            case commands.CVO_RESP_DO:
                cvo_response_text = 'DO'
            case commands.CVO_RESP_LO:
                cvo_response_text = 'LO'
            case commands.CVO_RESP_NR:
                cvo_response_text = 'NR'
            case _:
                cvo_response_text = 'Invalid'
        
        match wd_timer:
            case commands.WATCHDOG_OFF:
                wd_timer_text = 'OFF'
            case commands.WATCHDOG_500MS:
                wd_timer_text = '0.5 s'
            case commands.WATCHDOG_1000MS:
                wd_timer_text = '1 s'
            case commands.WATCHDOG_2000MS:
                wd_timer_text = '2s'
            case _:
                wd_timer_text = 'Invalid'
                
        match uva_timer:
            case commands.UVA_TIMER_8MS:
                uva_timer_text = '8 ms'
            case commands.UVA_TIMER_16MS:
                uva_timer_text = '16 ms'
            case commands.UVA_TIMER_32MS:
                uva_timer_text = '32 ms'
            case commands.UVA_TIMER_64MS:
                uva_timer_text = '64 ms'
            case _:
                uva_timer_text = 'Invalid'
        
        match uva_timer:
            case commands.UVA_TIMER_8MS:
                uva_timer_text = '8 ms'
            case commands.UVA_TIMER_16MS:
                uva_timer_text = '16 ms'
            case commands.UVA_TIMER_32MS:
                uva_timer_text = '32 ms'
            case commands.UVA_TIMER_64MS:
                uva_timer_text = '64 ms'
            case _:
                uva_timer_text = 'Invalid'
                
        match issc_response:
            case commands.ISSC_RESP_AR:
                issc_response_text = 'AR'
            case commands.ISSC_RESP_DO:
                issc_response_text = 'DO'
            case commands.ISSC_RESP_LO:
                issc_response_text = 'LO'
            case commands.ISSC_RESP_NR:
                issc_response_text = 'NR'
            case _:
                issc_response_text = 'Invalid'
                
        match ccsc_response:
            case commands.CCSC_RESP_AR:
                ccsc_response_text = 'AR'
            case commands.CCSC_RESP_DO:
                ccsc_response_text = 'DO'
            case commands.CCSC_RESP_LO:
                ccsc_response_text = 'LO'
            case commands.CCSC_RESP_NR:
                ccsc_response_text = 'NR'
            case _:
                ccsc_response_text = 'Invalid'
                
        match uva_response:
            case commands.UVA_RESP_AR:
                uva_response_text = 'AR'
            case commands.UVA_RESP_DO:
                uva_response_text = 'DO'
            case commands.UVA_RESP_LO:
                uva_response_text = 'LO'
            case commands.UVA_RESP_NR:
                uva_response_text = 'NR'
            case _:
                uva_response_text = 'Invalid'
                
        match ova_response:
            case commands.OVA_RESP_AR:
                ova_response_text = 'AR'
            case commands.OVA_RESP_DO:
                ova_response_text = 'DO'
            case commands.OVA_RESP_LO:
                ova_response_text = 'LO'
            case commands.OVA_RESP_NR:
                ova_response_text = 'NR'
            case _:
                ova_response_text = 'Invalid'

        self.cvo_timer_data.setText(f'{cvo_timer_text}')
        self.cvo_response_data.setText(f'{cvo_response_text}')
        self.watchdog_timer_data.setText(f'{wd_timer_text}')
        self.uva_timer_data.setText(f'{uva_timer_text}')
        self.issc_response_data.setText(f'{issc_response_text}')
        self.ccsc_response_data.setText(f'{ccsc_response_text}')
        self.uva_response_data.setText(f'{uva_response_text}')
        self.ova_response_data.setText(f'{ova_response_text}')
        
        return reg  

class INNO4_READ7_REG_UI():
    """Creates an I2C control UI frame for Read7 register"""
    reg_label = 'READ7'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ7()
        reg_name = 'read7_reg'
        self.reg_label = 'READ7'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ7:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ7
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=2,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=3,row_span=1,col_span=2,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=3,row_span=1,col_span=2,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=2,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)       
        
        self.cdc_label = UIObject(name=f'label_{page_name}_{reg_name}_cdc_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.cdc_label:UILabelObject = self.cdc_label.add_label_to_grid_frame(name='CDC:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cdc_data = UIObject(name=f'label_{page_name}_{reg_name}_cdc_data',object_type=UILabelObject,
                        row_index=3,col_index=2,row_span=1,col_span=1,min_width=30,min_height=30)
        self.cdc_data:UILabelObject = self.cdc_data.add_label_to_grid_frame(name='',frame=self.frame,grid_layout=self.gridLayout)
        
        self.otp_hysteresis_label = UIObject(name=f'label_{page_name}_{reg_name}_otp_hysteresis_label',object_type=UILabelObject,
                        row_index=4,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.otp_hysteresis_label:UILabelObject = self.otp_hysteresis_label.add_label_to_grid_frame(name='OTP:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.otp_hysteresis_data = UIObject(name=f'label_{page_name}_{reg_name}_otp_hysteresis_data',object_type=UILabelObject,
                        row_index=4,col_index=2,row_span=1,col_span=1,min_width=30,min_height=30)
        self.otp_hysteresis_data:UILabelObject = self.otp_hysteresis_data.add_label_to_grid_frame(name='',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cvo_label = UIObject(name=f'label_{page_name}_{reg_name}_cvo_label',object_type=UILabelObject,
                        row_index=5,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.cvo_label:UILabelObject = self.cvo_label.add_label_to_grid_frame(name='CVO:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cvo_data = UIObject(name=f'label_{page_name}_{reg_name}_cvo_data',object_type=UILabelObject,
                        row_index=5,col_index=2,row_span=1,col_span=1,min_width=30,min_height=30)
        self.cvo_data:UILabelObject = self.cvo_data.add_label_to_grid_frame(name='',frame=self.frame,grid_layout=self.gridLayout)
        
        self.fstvic_label = UIObject(name=f'label_{page_name}_{reg_name}_fstvic_label',object_type=UILabelObject,
                        row_index=6,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.fstvic_label:UILabelObject = self.fstvic_label.add_label_to_grid_frame(name='Fast VI:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.fstvic_data = UIObject(name=f'label_{page_name}_{reg_name}_fstvic_data',object_type=UILabelObject,
                        row_index=6,col_index=2,row_span=1,col_span=1,min_width=30,min_height=30)
        self.fstvic_data:UILabelObject = self.fstvic_data.add_label_to_grid_frame(name='',frame=self.frame,grid_layout=self.gridLayout)
        
        self.psu_off_label = UIObject(name=f'label_{page_name}_{reg_name}_psu_off_label',object_type=UILabelObject,
                        row_index=3,col_index=3,row_span=1,col_span=1,min_width=30,min_height=30)
        self.psu_off_label:UILabelObject = self.psu_off_label.add_label_to_grid_frame(name='Turn-Off:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.psu_off_data = UIObject(name=f'label_{page_name}_{reg_name}_psu_off_data',object_type=UILabelObject,
                        row_index=3,col_index=4,row_span=1,col_span=1,min_width=30,min_height=30)
        self.psu_off_data:UILabelObject = self.psu_off_data.add_label_to_grid_frame(name='',frame=self.frame,grid_layout=self.gridLayout)
        
        self.bleeder_label = UIObject(name=f'label_{page_name}_{reg_name}_bleeder_label',object_type=UILabelObject,
                        row_index=4,col_index=3,row_span=1,col_span=1,min_width=30,min_height=30)
        self.bleeder_label:UILabelObject = self.bleeder_label.add_label_to_grid_frame(name='Bleeder:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.bleeder_data = UIObject(name=f'label_{page_name}_{reg_name}_bleeder_data',object_type=UILabelObject,
                        row_index=4,col_index=4,row_span=1,col_span=1,min_width=30,min_height=30)
        self.bleeder_data:UILabelObject = self.bleeder_data.add_label_to_grid_frame(name='',frame=self.frame,grid_layout=self.gridLayout)
        
        self.vben_label = UIObject(name=f'label_{page_name}_{reg_name}_vben_label',object_type=UILabelObject,
                        row_index=5,col_index=3,row_span=1,col_span=1,min_width=30,min_height=30)
        self.vben_label:UILabelObject = self.vben_label.add_label_to_grid_frame(name='VBEN:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.vben_data = UIObject(name=f'label_{page_name}_{reg_name}_vben_data',object_type=UILabelObject,
                        row_index=5,col_index=4,row_span=1,col_span=1,min_width=30,min_height=30)
        self.vben_data:UILabelObject = self.vben_data.add_label_to_grid_frame(name='',frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass    
         
    def update_i2c_data(self,rb_u16):
        reg = READ7()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        cdc, otp_hysteresis, cvo, fstvic, psu_off, bleeder, vben = process_read7_command(rb_u16)
        cdc_mV = cdc*params.CDC_RESOLUTION_MV
        
        match otp_hysteresis:
            case commands.OTP_40DEGC:
                otp_hysteresis_text = '40 C'
            case commands.OTP_60DEGC:
                otp_hysteresis_text = '60 C'
            case _:
                otp_hysteresis_text = 'Invalid'
                
        match cvo:
            case commands.CVO_CV_ONLY_MODE:
                cvo_text = 'Enabled'
            case commands.CVO_CV_CC_MODE:
                cvo_text = 'Disabled'
            case _:
                cvo_text = 'Invalid'
        
        match fstvic:
            case commands.FASTVI_LIMIT_EN:
                fstvic_text = 'Disabled'
            case commands.FASTVI_LIMIT_DIS:
                fstvic_text = 'Enabled'
            case _:
                fstvic_text = 'Invalid'
                
        match psu_off:
            case commands.TURN_OFF_PSU_ENABLED:
                psu_off_text = 'Enabled'
            case commands.TURN_OFF_PSU_DISABLED:
                psu_off_text = 'Disabled'
            case _:
                psu_off_text = 'Invalid'
        
        match bleeder:
            case commands.BLEEDER_ON:
                bleeder_text = 'Enabled'
            case commands.BLEEDER_OFF:
                bleeder_text = 'Disabled'
            case _:
                bleeder_text = 'Invalid'
                
        match vben:
            case commands.VBEN_READBACK_ON:
                vben_text = 'Enabled'
            case commands.VBEN_READBACK_OFF:
                vben_text = 'Disabled'
            case _:
                vben_text = 'Invalid'

        self.cdc_data.setText(f'{cdc_mV:g} mV')
        self.otp_hysteresis_data.setText(f'{otp_hysteresis_text}')
        self.cvo_data.setText(f'{cvo_text}')
        self.fstvic_data.setText(f'{fstvic_text}')
        self.psu_off_data.setText(f'{psu_off_text}')
        self.bleeder_data.setText(f'{bleeder_text}')
        self.vben_data.setText(f'{vben_text}')
        
        return reg
    
class INNO4_READ8_REG_UI():
    """Creates an I2C control UI frame for Read8 register"""
    reg_label = 'READ8'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ8()
        reg_name = 'read8_reg'
        self.reg_label = 'READ8'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ8:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ8
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cc_i_label = UIObject(name=f'label_{page_name}_{reg_name}_cc_i_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.cc_i_label:UILabelObject = self.cc_i_label.add_label_to_grid_frame(name='Inst. Current:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cc_i_data =  UIObject(name=f'label_{page_name}_{reg_name}_cc_i_data',object_type=UILabelObject,
                            row_index=3,col_index=2,row_span=1,col_span=1,min_width=80,min_height=30)
        self.cc_i_data:UILabelObject = self.cc_i_data.add_label_to_grid_frame(name='0',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
     
    def update_i2c_data(self,rb_u16):
        reg = READ8()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'0x{reg.asbyte:04X}')
        cc_i = process_read8_command(rb_u16)
        self.cc_i_data.setText(f'{cc_i:g}')
        return reg 
    
class INNO4_READ9_REG_UI():
    """Creates an I2C control UI frame for Read9 register"""
    reg_label = 'READ9'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ9()
        reg_name = 'read9_reg'
        self.reg_label = 'READ9'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ9:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ9
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=2,row_span=1,col_span=1,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cv_i_label = UIObject(name=f'label_{page_name}_{reg_name}_cv_i_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.cv_i_label:UILabelObject = self.cv_i_label.add_label_to_grid_frame(name='Inst. Voltage:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cv_i_data =  UIObject(name=f'label_{page_name}_{reg_name}_cv_i_data',object_type=UILabelObject,
                            row_index=3,col_index=2,row_span=1,col_span=1,min_width=80,min_height=30)
        self.cv_i_data:UILabelObject = self.cv_i_data.add_label_to_grid_frame(name='0',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ9()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        cv_i = process_read9_command(rb_u16)
        cv_i_V = cv_i * params.CV_RESOLUTION_MV/1000
        self.cv_i_data.setText(f'{cv_i_V:g} V')
        return reg 
    
class INNO4_READ10_REG_UI():
    """Creates an I2C control UI frame for Read10 register"""
    reg_label = 'READ10'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ10()
        reg_name = 'read10_reg'
        self.reg_label = 'READ10'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ10:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ10
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=4,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=5,row_span=1,col_span=5,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=5,row_span=1,col_span=5,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=4,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_vout_ov_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_vout_ov_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_vout_ov_label:UILabelObject = self.reg_vout_ov_label.add_label_to_grid_frame(name='OV Fault:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_vout_ov_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_vout_ov_data',object_type=UILabelObject,
                            row_index=3,col_index=3,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_vout_ov_data:UILabelObject = self.reg_vout_ov_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        self.reg_vout_uv_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_vout_uv_label',object_type=UILabelObject,
                        row_index=4,col_index=1,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_vout_uv_label:UILabelObject = self.reg_vout_uv_label.add_label_to_grid_frame(name='UV Fault:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_vout_uv_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_vout_uv_data',object_type=UILabelObject,
                            row_index=4,col_index=3,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_vout_uv_data:UILabelObject = self.reg_vout_uv_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_ccsc_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_ccsc_label',object_type=UILabelObject,
                        row_index=5,col_index=1,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_ccsc_label:UILabelObject = self.reg_ccsc_label.add_label_to_grid_frame(name='CCSC Fault:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_ccsc_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_ccsc_data',object_type=UILabelObject,
                            row_index=5,col_index=3,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_ccsc_data:UILabelObject = self.reg_ccsc_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_issc_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_issc_label',object_type=UILabelObject,
                        row_index=6,col_index=1,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_issc_label:UILabelObject = self.reg_issc_label.add_label_to_grid_frame(name='ISSC Fault:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_issc_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_issc_data',object_type=UILabelObject,
                            row_index=6,col_index=3,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_issc_data:UILabelObject = self.reg_issc_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_vout10pct_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_vout10pct_label',object_type=UILabelObject,
                        row_index=3,col_index=4,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_vout10pct_label:UILabelObject = self.reg_vout10pct_label.add_label_to_grid_frame(name='VOUT10PCT:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_vout10pct_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_vout10pct_data',object_type=UILabelObject,
                            row_index=3,col_index=6,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_vout10pct_data:UILabelObject = self.reg_vout10pct_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_voutwk_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_voutwk_label',object_type=UILabelObject,
                        row_index=4,col_index=4,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_voutwk_label:UILabelObject = self.reg_voutwk_label.add_label_to_grid_frame(name='VOUT4PCT:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_voutwk_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_voutwk_data',object_type=UILabelObject,
                            row_index=4,col_index=6,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_voutwk_data:UILabelObject = self.reg_voutwk_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_otp_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_otp_label',object_type=UILabelObject,
                        row_index=5,col_index=4,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_otp_label:UILabelObject = self.reg_otp_label.add_label_to_grid_frame(name='OTP:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_otp_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_otp_data',object_type=UILabelObject,
                            row_index=5,col_index=6,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_otp_data:UILabelObject = self.reg_otp_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_cv_en_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_cv_en_label',object_type=UILabelObject,
                        row_index=6,col_index=4,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_cv_en_label:UILabelObject = self.reg_cv_en_label.add_label_to_grid_frame(name='Auto CV:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_cv_en_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_cv_en_data',object_type=UILabelObject,
                            row_index=6,col_index=6,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_cv_en_data:UILabelObject = self.reg_cv_en_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_high_fsw_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_high_fsw_label',object_type=UILabelObject,
                        row_index=3,col_index=7,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_high_fsw_label:UILabelObject = self.reg_high_fsw_label.add_label_to_grid_frame(name='High Fs:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_high_fsw_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_high_fsw_data',object_type=UILabelObject,
                            row_index=3,col_index=9,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_high_fsw_data:UILabelObject = self.reg_high_fsw_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_vdis_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_vdis_label',object_type=UILabelObject,
                        row_index=4,col_index=7,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_vdis_label:UILabelObject = self.reg_vdis_label.add_label_to_grid_frame(name='VDIS:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_vdis_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_vdis_data',object_type=UILabelObject,
                            row_index=4,col_index=9,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_vdis_data:UILabelObject = self.reg_vdis_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_control_s_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_control_s_label',object_type=UILabelObject,
                        row_index=5,col_index=7,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_control_s_label:UILabelObject = self.reg_control_s_label.add_label_to_grid_frame(name='CTRL S:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_control_s_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_control_s_data',object_type=UILabelObject,
                            row_index=5,col_index=9,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_control_s_data:UILabelObject = self.reg_control_s_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_interrupt_en_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_interrupt_en_label',object_type=UILabelObject,
                        row_index=6,col_index=7,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_interrupt_en_label:UILabelObject = self.reg_interrupt_en_label.add_label_to_grid_frame(name='INTR:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_interrupt_en_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_interrupt_en_data',object_type=UILabelObject,
                            row_index=6,col_index=9,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_interrupt_en_data:UILabelObject = self.reg_interrupt_en_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ10()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        reg_vout_ov, reg_vout_uv, reg_ccsc, reg_issc, reg_vout10pct, reg_voutwk, reg_otp, reg_cv_en, reg_high_fsw, reg_vdis, reg_control_s, reg_interrupt_en = process_read10_command(rb_u16)
        
        self.reg_vout_ov_data.setText(f'{reg_vout_ov:g}')
        self.reg_vout_uv_data.setText(f'{reg_vout_uv:g}')
        self.reg_ccsc_data.setText(f'{reg_ccsc:g}')
        self.reg_issc_data.setText(f'{reg_issc:g}')
        self.reg_vout10pct_data.setText(f'{reg_vout10pct:g}')
        self.reg_voutwk_data.setText(f'{reg_voutwk:g}')
        self.reg_otp_data.setText(f'{reg_otp:g}')
        self.reg_cv_en_data.setText(f'{reg_cv_en:g}')
        self.reg_high_fsw_data.setText(f'{reg_high_fsw:g}')
        self.reg_vdis_data.setText(f'{reg_vdis:g}')
        self.reg_control_s_data.setText(f'{reg_control_s:g}')
        self.reg_interrupt_en_data.setText(f'{reg_interrupt_en:g}')
       
        return reg 
    
class INNO4_READ11_REG_UI():
    """Creates an I2C control UI frame for Read11 register"""
    reg_label = 'READ11'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ11()
        reg_name = 'read11_reg'
        self.reg_label = 'READ11'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ11:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ11
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=2,row_span=1,col_span=1,min_width=30, min_height=20)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=2,row_span=1,col_span=1,min_width=30, min_height=20)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.omf_label = UIObject(name=f'label_{page_name}_{reg_name}_omf_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.omf_label:UILabelObject = self.omf_label.add_label_to_grid_frame(name='OMF:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.omf_data =  UIObject(name=f'label_{page_name}_{reg_name}_omf_data',object_type=UILabelObject,
                            row_index=3,col_index=2,row_span=1,col_span=1,min_width=80,min_height=30)
        self.omf_data:UILabelObject = self.omf_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ11()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        cv_mode, cp_mode, cc_mode = process_read11_command(rb_u16)
        if cv_mode:
            omf_text = 'CV Mode'
        elif cp_mode:
            omf_text = 'CP Mode'
        elif cc_mode: 
            omf_text = 'CC Mode'
        else:
            omf_text = 'Invalid'
        self.omf_data.setText(f'{omf_text}')
        return reg 
    

class INNO4_READ12_REG_UI():
    """Creates an I2C control UI frame for Read12 register"""
    reg_label = 'READ12'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ12()
        reg_name = 'read12_reg'
        self.reg_label = 'READ12'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ12:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ12
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=2,row_span=1,col_span=1,min_width=30, min_height=20)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=2,row_span=1,col_span=1,min_width=30, min_height=20)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cc_ave_label = UIObject(name=f'label_{page_name}_{reg_name}_cc_ave_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.cc_ave_label:UILabelObject = self.cc_ave_label.add_label_to_grid_frame(name='Ave. Current:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cc_ave_data =  UIObject(name=f'label_{page_name}_{reg_name}_cc_ave_data',object_type=UILabelObject,
                            row_index=3,col_index=2,row_span=1,col_span=1,min_width=80,min_height=30)
        self.cc_ave_data:UILabelObject = self.cc_ave_data.add_label_to_grid_frame(name='0',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ12()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        cc_ave = process_read12_command(rb_u16)
        self.cc_ave_data.setText(f'{cc_ave:g}')
        return reg 
    
class INNO4_READ13_REG_UI():
    """Creates an I2C control UI frame for Read13 register"""
    reg_label = 'READ13'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ13()
        reg_name = 'read13_reg'
        self.reg_label = 'READ13'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ13:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ13
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=2,row_span=1,col_span=1,min_width=30, min_height=20)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=2,row_span=1,col_span=1,min_width=30, min_height=20)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cv_ave_label = UIObject(name=f'label_{page_name}_{reg_name}_cv_ave_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.cc_ave_label:UILabelObject = self.cv_ave_label.add_label_to_grid_frame(name='Ave. Voltage:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cv_ave_data =  UIObject(name=f'label_{page_name}_{reg_name}_cv_ave_data',object_type=UILabelObject,
                            row_index=3,col_index=2,row_span=1,col_span=1,min_width=80,min_height=30)
        self.cv_ave_data:UILabelObject = self.cv_ave_data.add_label_to_grid_frame(name='0',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ13()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        cv_ave = process_read13_command(rb_u16)
        cv_ave_V = cv_ave * params.CV_RESOLUTION_MV/1000
        self.cv_ave_data.setText(f'{cv_ave_V:g} V')
        return reg 

class INNO4_READ14_REG_UI():
    """Creates an I2C control UI frame for Read14 register"""
    reg_label = 'READ14'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ14()
        reg_name = 'read14_reg'
        self.reg_label = 'READ14'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ14:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ14
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=2,row_span=1,col_span=1,min_width=30, min_height=20)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=2,row_span=1,col_span=1,min_width=30, min_height=20)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=1,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.vout_dac_label = UIObject(name=f'label_{page_name}_{reg_name}_vout_dac_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=30,min_height=30)
        self.vout_dac_label:UILabelObject = self.vout_dac_label.add_label_to_grid_frame(name='Voltage DAC:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.vout_dac_data =  UIObject(name=f'label_{page_name}_{reg_name}_vout_dac_data',object_type=UILabelObject,
                            row_index=3,col_index=2,row_span=1,col_span=1,min_width=80,min_height=30)
        self.vout_dac_data:UILabelObject = self.vout_dac_data.add_label_to_grid_frame(name='0',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ14()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        vout_dac = process_read14_command(rb_u16)
        self.vout_dac_data.setText(f'{vout_dac:g} V')
        return reg 
    
class INNO4_READ16_REG_UI():
    """Creates an I2C control UI frame for Read16 register"""
    reg_label = 'READ16'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ16()
        reg_name = 'read16_reg'
        self.reg_label = 'READ16'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ16:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ16
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=4,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=5,row_span=1,col_span=5,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=5,row_span=1,col_span=5,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=4,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_lo_bps_ov_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_lo_bps_ov_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_lo_bps_ov_label:UILabelObject = self.reg_lo_bps_ov_label.add_label_to_grid_frame(name='BPS OV LO:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_lo_bps_ov_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_lo_bps_ov_data',object_type=UILabelObject,
                            row_index=3,col_index=3,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_lo_bps_ov_data:UILabelObject = self.reg_lo_bps_ov_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        self.reg_lo_vout_uv_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_lo_vout_uv_label',object_type=UILabelObject,
                        row_index=4,col_index=1,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_lo_vout_uv_label:UILabelObject = self.reg_lo_vout_uv_label.add_label_to_grid_frame(name='UV LO:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_lo_vout_uv_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_lo_vout_uv_data',object_type=UILabelObject,
                            row_index=4,col_index=3,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_lo_vout_uv_data:UILabelObject = self.reg_lo_vout_uv_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_lo_vout_ov_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_lo_vout_ov_label',object_type=UILabelObject,
                        row_index=5,col_index=1,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_lo_vout_ov_label:UILabelObject = self.reg_lo_vout_ov_label.add_label_to_grid_frame(name='OV LO:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_lo_vout_ov_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_lo_vout_ov_data',object_type=UILabelObject,
                            row_index=5,col_index=3,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_lo_vout_ov_data:UILabelObject = self.reg_lo_vout_ov_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_lo_issc_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_lo_issc_label',object_type=UILabelObject,
                        row_index=6,col_index=1,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_lo_issc_label:UILabelObject = self.reg_lo_issc_label.add_label_to_grid_frame(name='ISSC LO:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_lo_issc_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_lo_issc_data',object_type=UILabelObject,
                            row_index=6,col_index=3,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_lo_issc_data:UILabelObject = self.reg_lo_issc_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_psuoff_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_psuoff_label',object_type=UILabelObject,
                        row_index=3,col_index=4,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_psuoff_label:UILabelObject = self.reg_psuoff_label.add_label_to_grid_frame(name='PSU OFF:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_psuoff_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_psuoff_data',object_type=UILabelObject,
                            row_index=3,col_index=6,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_psuoff_data:UILabelObject = self.reg_psuoff_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_lo_cvo_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_lo_cvo_label',object_type=UILabelObject,
                        row_index=4,col_index=4,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_lo_cvo_label:UILabelObject = self.reg_lo_cvo_label.add_label_to_grid_frame(name='CVO LO:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_lo_cvo_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_lo_cvo_data',object_type=UILabelObject,
                            row_index=4,col_index=6,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_lo_cvo_data:UILabelObject = self.reg_lo_cvo_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
        self.reg_lo_fault_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_lo_fault_label',object_type=UILabelObject,
                        row_index=5,col_index=4,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_lo_fault_label:UILabelObject = self.reg_lo_fault_label.add_label_to_grid_frame(name='LO:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_lo_fault_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_lo_fault_data',object_type=UILabelObject,
                            row_index=5,col_index=6,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_lo_fault_data:UILabelObject = self.reg_lo_fault_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)

        self.reg_ar_vout_uv_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_ar_vout_uv_label',object_type=UILabelObject,
                        row_index=6,col_index=4,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_ar_vout_uv_label:UILabelObject = self.reg_ar_vout_uv_label.add_label_to_grid_frame(name='UV AR:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_ar_vout_uv_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_ar_vout_uv_data',object_type=UILabelObject,
                            row_index=6,col_index=6,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_ar_vout_uv_data:UILabelObject = self.reg_ar_vout_uv_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_ar_vout_ov_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_ar_vout_ov_label',object_type=UILabelObject,
                        row_index=3,col_index=7,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_ar_vout_ov_label:UILabelObject = self.reg_ar_vout_ov_label.add_label_to_grid_frame(name='OV AR:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_ar_vout_ov_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_ar_vout_ov_data',object_type=UILabelObject,
                            row_index=3,col_index=9,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_ar_vout_ov_data:UILabelObject = self.reg_ar_vout_ov_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_ar_ccsc_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_ar_ccsc_label',object_type=UILabelObject,
                        row_index=4,col_index=7,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_ar_ccsc_label:UILabelObject = self.reg_ar_ccsc_label.add_label_to_grid_frame(name='CCSC AR:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_ar_ccsc_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_ar_ccsc_data',object_type=UILabelObject,
                            row_index=4,col_index=9,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_ar_ccsc_data:UILabelObject = self.reg_ar_ccsc_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_ar_issc_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_ar_issc_label',object_type=UILabelObject,
                        row_index=5,col_index=7,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_ar_issc_label:UILabelObject = self.reg_ar_issc_label.add_label_to_grid_frame(name='ISSC AR:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_ar_issc_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_ar_issc_data',object_type=UILabelObject,
                            row_index=5,col_index=9,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_ar_issc_data:UILabelObject = self.reg_ar_issc_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        # self.reg_ar_vbussc_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_ar_vbussc_label',object_type=UILabelObject,
        #                 row_index=6,col_index=7,row_span=1,col_span=2,min_width=100,min_height=30)
        # self.reg_ar_vbussc_label:UILabelObject = self.reg_ar_vbussc_label.add_label_to_grid_frame(name='VBUSSC AR:',frame=self.frame,grid_layout=self.gridLayout)
        
        # self.reg_ar_vbussc_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_ar_vbussc_data',object_type=UILabelObject,
        #                     row_index=6,col_index=9,row_span=1,col_span=1,min_width=10,min_height=30)
        # self.reg_ar_vbussc_data:UILabelObject = self.reg_ar_vbussc_data.add_label_to_grid_frame(name='',\
        #                                     frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_ar_cvo_label = UIObject(name=f'label_{page_name}_{reg_name}_reg_ar_cvo_label',object_type=UILabelObject,
                        row_index=6,col_index=7,row_span=1,col_span=2,min_width=100,min_height=30)
        self.reg_ar_cvo_label:UILabelObject = self.reg_ar_cvo_label.add_label_to_grid_frame(name='CVO AR:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.reg_ar_cvo_data =  UIObject(name=f'label_{page_name}_{reg_name}_reg_ar_cvo_data',object_type=UILabelObject,
                            row_index=6,col_index=9,row_span=1,col_span=1,min_width=10,min_height=30)
        self.reg_ar_cvo_data:UILabelObject = self.reg_ar_cvo_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ16()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        reg_lo_bps_ov, reg_lo_vout_uv, reg_lo_vout_ov, reg_lo_issc, reg_psuoff, reg_lo_cvo, reg_lo_fault, reg_ar_vout_uv, reg_ar_vout_ov, reg_ar_ccsc, reg_ar_issc, reg_ar_cvo = process_read16_command(rb_u16)
        
        self.reg_lo_bps_ov_data.setText(f'{reg_lo_bps_ov:g}')
        self.reg_lo_vout_uv_data.setText(f'{reg_lo_vout_uv:g}')
        self.reg_lo_vout_ov_data.setText(f'{reg_lo_vout_ov:g}')
        self.reg_lo_issc_data.setText(f'{reg_lo_issc:g}')
        self.reg_psuoff_data.setText(f'{reg_psuoff:g}')
        self.reg_lo_cvo_data.setText(f'{reg_lo_cvo:g}')
        self.reg_lo_fault_data.setText(f'{reg_lo_fault:g}')
        self.reg_ar_vout_uv_data.setText(f'{reg_ar_vout_uv:g}')
        self.reg_ar_vout_ov_data.setText(f'{reg_ar_vout_ov:g}')
        self.reg_ar_ccsc_data.setText(f'{reg_ar_ccsc:g}')
        self.reg_ar_issc_data.setText(f'{reg_ar_issc:g}')
        # self.reg_ar_vbussc_data.setText(f'{reg_ar_vbussc:g}')
        self.reg_ar_cvo_data.setText(f'{reg_ar_cvo:g}')       
        return reg 
    
class INNO4_READ17_REG_UI():
    """Creates an I2C control UI frame for Read17 register"""
    reg_label = 'READ17'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ17()
        reg_name = 'read17_reg'
        self.reg_label = 'READ17'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ17:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ17
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=4,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=5,row_span=2,col_span=5,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=5,row_span=1,col_span=5,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=4,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.control_s_int_mask_label = UIObject(name=f'label_{page_name}_{reg_name}_control_s_int_mask_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=2,min_width=100,min_height=30)
        self.control_s_int_mask_label:UILabelObject = self.control_s_int_mask_label.add_label_to_grid_frame(name='CTRL S Mask:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.control_s_int_mask_data =  UIObject(name=f'label_{page_name}_{reg_name}_control_s_int_mask_data',object_type=UILabelObject,
                            row_index=3,col_index=3,row_span=1,col_span=1,min_width=10,min_height=30)
        self.control_s_int_mask_data:UILabelObject = self.control_s_int_mask_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        self.lo_fault_int_mask_label = UIObject(name=f'label_{page_name}_{reg_name}_lo_fault_int_mask_label',object_type=UILabelObject,
                        row_index=4,col_index=1,row_span=1,col_span=2,min_width=100,min_height=30)
        self.lo_fault_int_mask_label:UILabelObject = self.lo_fault_int_mask_label.add_label_to_grid_frame(name='LO Mask:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.lo_fault_int_mask_data =  UIObject(name=f'label_{page_name}_{reg_name}_lo_fault_int_mask_data',object_type=UILabelObject,
                            row_index=4,col_index=3,row_span=1,col_span=1,min_width=10,min_height=30)
        self.lo_fault_int_mask_data:UILabelObject = self.lo_fault_int_mask_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cvo_ar_int_mask_label = UIObject(name=f'label_{page_name}_{reg_name}_cvo_ar_int_mask_label',object_type=UILabelObject,
                        row_index=5,col_index=1,row_span=1,col_span=2,min_width=100,min_height=30)
        self.cvo_ar_int_mask_label:UILabelObject = self.cvo_ar_int_mask_label.add_label_to_grid_frame(name='CVO AR Mask:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cvo_ar_int_mask_data =  UIObject(name=f'label_{page_name}_{reg_name}_cvo_ar_int_mask_data',object_type=UILabelObject,
                            row_index=5,col_index=3,row_span=1,col_span=1,min_width=10,min_height=30)
        self.cvo_ar_int_mask_data:UILabelObject = self.cvo_ar_int_mask_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.issc_int_mask_label = UIObject(name=f'label_{page_name}_{reg_name}_issc_int_mask_label',object_type=UILabelObject,
                        row_index=6,col_index=1,row_span=1,col_span=2,min_width=100,min_height=30)
        self.issc_int_mask_label:UILabelObject = self.issc_int_mask_label.add_label_to_grid_frame(name='ISSC Mask:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.issc_int_mask_data =  UIObject(name=f'label_{page_name}_{reg_name}_issc_int_mask_data',object_type=UILabelObject,
                            row_index=6,col_index=3,row_span=1,col_span=1,min_width=10,min_height=30)
        self.issc_int_mask_data:UILabelObject = self.issc_int_mask_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.ccsc_int_mask_label = UIObject(name=f'label_{page_name}_{reg_name}_ccsc_int_mask_label',object_type=UILabelObject,
                        row_index=7,col_index=1,row_span=1,col_span=2,min_width=100,min_height=30)
        self.ccsc_int_mask_label:UILabelObject = self.ccsc_int_mask_label.add_label_to_grid_frame(name='CCSC Mask:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.ccsc_int_mask_data =  UIObject(name=f'label_{page_name}_{reg_name}_ccsc_int_mask_data',object_type=UILabelObject,
                            row_index=7,col_index=3,row_span=1,col_span=1,min_width=10,min_height=30)
        self.ccsc_int_mask_data:UILabelObject = self.ccsc_int_mask_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.uv_int_mask_label = UIObject(name=f'label_{page_name}_{reg_name}_uv_int_mask_label',object_type=UILabelObject,
                        row_index=8,col_index=1,row_span=1,col_span=2,min_width=100,min_height=30)
        self.uv_int_mask_label:UILabelObject = self.uv_int_mask_label.add_label_to_grid_frame(name='UV Mask:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.uv_int_mask_data =  UIObject(name=f'label_{page_name}_{reg_name}_uv_int_mask_data',object_type=UILabelObject,
                            row_index=8,col_index=3,row_span=1,col_span=1,min_width=10,min_height=30)
        self.uv_int_mask_data:UILabelObject = self.uv_int_mask_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.ov_int_mask_label = UIObject(name=f'label_{page_name}_{reg_name}_ov_int_mask_label',object_type=UILabelObject,
                        row_index=4,col_index=4,row_span=1,col_span=2,min_width=100,min_height=30)
        self.ov_int_mask_label:UILabelObject = self.ov_int_mask_label.add_label_to_grid_frame(name='OV Mask:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.ov_int_mask_data =  UIObject(name=f'label_{page_name}_{reg_name}_ov_int_mask_data',object_type=UILabelObject,
                            row_index=4,col_index=6,row_span=1,col_span=1,min_width=10,min_height=30)
        self.ov_int_mask_data:UILabelObject = self.ov_int_mask_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
        self.omf_int_status_label = UIObject(name=f'label_{page_name}_{reg_name}_omf_int_status_label',object_type=UILabelObject,
                        row_index=5,col_index=4,row_span=1,col_span=2,min_width=100,min_height=30)
        self.omf_int_status_label:UILabelObject = self.omf_int_status_label.add_label_to_grid_frame(name='OMF:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.omf_int_status_data =  UIObject(name=f'label_{page_name}_{reg_name}_omf_int_status_data',object_type=UILabelObject,
                            row_index=5,col_index=6,row_span=1,col_span=1,min_width=10,min_height=30)
        self.omf_int_status_data:UILabelObject = self.omf_int_status_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)

        self.vbussc_int_status_label = UIObject(name=f'label_{page_name}_{reg_name}_vbussc_int_status_label',object_type=UILabelObject,
                        row_index=6,col_index=4,row_span=1,col_span=2,min_width=100,min_height=30)
        self.vbussc_int_status_label:UILabelObject = self.vbussc_int_status_label.add_label_to_grid_frame(name='VBUSSC:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.vbussc_int_status_data =  UIObject(name=f'label_{page_name}_{reg_name}_vbussc_int_status_data',object_type=UILabelObject,
                            row_index=6,col_index=6,row_span=1,col_span=1,min_width=10,min_height=30)
        self.vbussc_int_status_data:UILabelObject = self.vbussc_int_status_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.control_s_int_status_label = UIObject(name=f'label_{page_name}_{reg_name}_control_s_int_status_label',object_type=UILabelObject,
                        row_index=7,col_index=4,row_span=1,col_span=2,min_width=100,min_height=30)
        self.control_s_int_status_label:UILabelObject = self.control_s_int_status_label.add_label_to_grid_frame(name='CTRL S:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.control_s_int_status_data =  UIObject(name=f'label_{page_name}_{reg_name}_control_s_int_status_data',object_type=UILabelObject,
                            row_index=7,col_index=6,row_span=1,col_span=1,min_width=10,min_height=30)
        self.control_s_int_status_data:UILabelObject = self.control_s_int_status_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cvo_ar_int_status_label = UIObject(name=f'label_{page_name}_{reg_name}_cvo_ar_int_status_label',object_type=UILabelObject,
                        row_index=8,col_index=4,row_span=1,col_span=2,min_width=100,min_height=30)
        self.cvo_ar_int_status_label:UILabelObject = self.cvo_ar_int_status_label.add_label_to_grid_frame(name='CVO AR:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cvo_ar_int_status_data =  UIObject(name=f'label_{page_name}_{reg_name}_cvo_ar_int_status_data',object_type=UILabelObject,
                            row_index=8,col_index=6,row_span=1,col_span=1,min_width=10,min_height=30)
        self.cvo_ar_int_status_data:UILabelObject = self.cvo_ar_int_status_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.issc_int_status_label = UIObject(name=f'label_{page_name}_{reg_name}_issc_int_status_label',object_type=UILabelObject,
                        row_index=4,col_index=7,row_span=1,col_span=2,min_width=100,min_height=30)
        self.issc_int_status_label:UILabelObject = self.issc_int_status_label.add_label_to_grid_frame(name='ISSC:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.issc_int_status_data =  UIObject(name=f'label_{page_name}_{reg_name}_issc_int_status_data',object_type=UILabelObject,
                            row_index=4,col_index=9,row_span=1,col_span=1,min_width=10,min_height=30)
        self.issc_int_status_data:UILabelObject = self.issc_int_status_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.ccsc_int_status_label = UIObject(name=f'label_{page_name}_{reg_name}_ccsc_int_status_label',object_type=UILabelObject,
                        row_index=5,col_index=7,row_span=1,col_span=2,min_width=100,min_height=30)
        self.ccsc_int_status_label:UILabelObject = self.ccsc_int_status_label.add_label_to_grid_frame(name='CCSC:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.ccsc_int_status_data =  UIObject(name=f'label_{page_name}_{reg_name}_ccsc_int_status_data',object_type=UILabelObject,
                            row_index=5,col_index=9,row_span=1,col_span=1,min_width=10,min_height=30)
        self.ccsc_int_status_data:UILabelObject = self.ccsc_int_status_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.lo_fault_int_status_label = UIObject(name=f'label_{page_name}_{reg_name}_lo_fault_int_status_label',object_type=UILabelObject,
                        row_index=6,col_index=7,row_span=1,col_span=2,min_width=100,min_height=30)
        self.lo_fault_int_status_label:UILabelObject = self.lo_fault_int_status_label.add_label_to_grid_frame(name='LO Fault:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.lo_fault_int_status_data =  UIObject(name=f'label_{page_name}_{reg_name}_lo_fault_int_status_data',object_type=UILabelObject,
                            row_index=6,col_index=9,row_span=1,col_span=1,min_width=10,min_height=30)
        self.lo_fault_int_status_data:UILabelObject = self.lo_fault_int_status_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.uv_int_status_label = UIObject(name=f'label_{page_name}_{reg_name}_uv_int_status_label',object_type=UILabelObject,
                        row_index=7,col_index=7,row_span=1,col_span=2,min_width=100,min_height=30)
        self.uv_int_status_label:UILabelObject = self.uv_int_status_label.add_label_to_grid_frame(name='UV:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.uv_int_status_data =  UIObject(name=f'label_{page_name}_{reg_name}_uv_int_status_data',object_type=UILabelObject,
                            row_index=7,col_index=9,row_span=1,col_span=1,min_width=10,min_height=30)
        self.uv_int_status_data:UILabelObject = self.uv_int_status_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.ov_int_status_label = UIObject(name=f'label_{page_name}_{reg_name}_ov_int_status_label',object_type=UILabelObject,
                        row_index=8,col_index=7,row_span=1,col_span=2,min_width=100,min_height=30)
        self.ov_int_status_label:UILabelObject = self.ov_int_status_label.add_label_to_grid_frame(name='OV:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.ov_int_status_data =  UIObject(name=f'label_{page_name}_{reg_name}_ov_int_status_data',object_type=UILabelObject,
                            row_index=8,col_index=9,row_span=1,col_span=1,min_width=10,min_height=30)
        self.ov_int_status_data:UILabelObject = self.ov_int_status_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ17()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        control_s_int_mask, lo_fault_int_mask, cvo_ar_int_mask, issc_int_mask, ccsc_int_mask, uv_int_mask, ov_int_mask, omf_int_status, vbussc_int_status, control_s_int_status, cvo_ar_int_status, issc_int_status, ccsc_int_status, lo_fault_int_status, uv_int_status, ov_int_status = process_read17_command(rb_u16)
        
        self.control_s_int_mask_data.setText(f'{control_s_int_mask:g}')
        self.lo_fault_int_mask_data.setText(f'{lo_fault_int_mask:g}')
        self.cvo_ar_int_mask_data.setText(f'{cvo_ar_int_mask:g}')
        self.issc_int_mask_data.setText(f'{issc_int_mask:g}')
        self.ccsc_int_mask_data.setText(f'{ccsc_int_mask:g}')
        self.uv_int_mask_data.setText(f'{uv_int_mask:g}')
        self.ov_int_mask_data.setText(f'{ov_int_mask:g}')
        self.omf_int_status_data.setText(f'{omf_int_status:g}')
        self.vbussc_int_status_data.setText(f'{vbussc_int_status:g}')
        self.control_s_int_status_data.setText(f'{control_s_int_status:g}')
        self.cvo_ar_int_status_data.setText(f'{cvo_ar_int_status:g}')
        self.issc_int_status_data.setText(f'{issc_int_status:g}')
        self.ccsc_int_status_data.setText(f'{ccsc_int_status:g}')
        self.lo_fault_int_status_data.setText(f'{lo_fault_int_status:g}')
        self.uv_int_status_data.setText(f'{uv_int_status:g}')
        self.ov_int_status_data.setText(f'{ov_int_status:g}')

        return reg 

class INNO4_READ18_REG_UI():
    """Creates an I2C control UI frame for Read18 register"""
    reg_label = 'READ18'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ18()
        reg_name = 'read18_reg'
        self.reg_label = 'READ18'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ18:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ18
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=2,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=3,row_span=2,col_span=2,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=3,row_span=1,col_span=2,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=2,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.fast_cc_offset_label = UIObject(name=f'label_{page_name}_{reg_name}_fast_cc_offset_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=100,min_height=30)
        self.fast_cc_offset_label:UILabelObject = self.fast_cc_offset_label.add_label_to_grid_frame(name='Fast CC Offset:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.fast_cc_offset_data =  UIObject(name=f'label_{page_name}_{reg_name}_fast_cc_offset_data',object_type=UILabelObject,
                            row_index=3,col_index=2,row_span=1,col_span=1,min_width=10,min_height=30)
        self.fast_cc_offset_data:UILabelObject = self.fast_cc_offset_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.fast_cc_enable_label = UIObject(name=f'label_{page_name}_{reg_name}_fast_cc_enable_label',object_type=UILabelObject,
                        row_index=4,col_index=1,row_span=1,col_span=1,min_width=100,min_height=30)
        self.fast_cc_enable_label:UILabelObject = self.fast_cc_enable_label.add_label_to_grid_frame(name='Fast CC:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.fast_cc_enable_data =  UIObject(name=f'label_{page_name}_{reg_name}_fast_cc_enable_data',object_type=UILabelObject,
                            row_index=4,col_index=2,row_span=1,col_span=1,min_width=10,min_height=30)
        self.fast_cc_enable_data:UILabelObject = self.fast_cc_enable_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.slow_cc_offset_label = UIObject(name=f'label_{page_name}_{reg_name}_slow_cc_offset_label',object_type=UILabelObject,
                        row_index=4,col_index=3,row_span=1,col_span=1,min_width=100,min_height=30)
        self.slow_cc_offset_label:UILabelObject = self.slow_cc_offset_label.add_label_to_grid_frame(name='Slow CC offset:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.slow_cc_offset_data =  UIObject(name=f'label_{page_name}_{reg_name}_slow_cc_offset_data',object_type=UILabelObject,
                            row_index=4,col_index=4,row_span=1,col_span=1,min_width=10,min_height=30)
        self.slow_cc_offset_data:UILabelObject = self.slow_cc_offset_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ18()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        fast_cc_offset, fast_cc_enable, slow_cc_offset = process_read18_command(rb_u16)

        self.fast_cc_offset_data.setText(f'{fast_cc_offset:g}')
        if fast_cc_enable:
            fast_cc_enable_text = 'Enabled'
        else:
            fast_cc_enable_text = 'Disabled'
        self.fast_cc_enable_data.setText(f'{fast_cc_enable_text}')
        self.slow_cc_offset_data.setText(f'{slow_cc_offset:g}')
        return reg 
    
class INNO4_READ19_REG_UI():
    """Creates an I2C control UI frame for Read19 register"""
    reg_label = 'READ19'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ19()
        reg_name = 'read19_reg'
        self.reg_label = 'READ19'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ19:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ19
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=2,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=3,row_span=2,col_span=2,min_width=30, min_height=30)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=3,row_span=1,col_span=2,min_width=30, min_height=30)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=2,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cv_small_step_thresh_label = UIObject(name=f'label_{page_name}_{reg_name}_cv_small_step_thresh_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=100,min_height=30)
        self.cv_small_step_thresh_label:UILabelObject = self.cv_small_step_thresh_label.add_label_to_grid_frame(name='CV Sml Step:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cv_small_step_thresh_data =  UIObject(name=f'label_{page_name}_{reg_name}_cv_small_step_thresh_data',object_type=UILabelObject,
                            row_index=3,col_index=2,row_span=1,col_span=1,min_width=10,min_height=30)
        self.cv_small_step_thresh_data:UILabelObject = self.cv_small_step_thresh_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cv_large_step_thresh_label = UIObject(name=f'label_{page_name}_{reg_name}_cv_large_step_thresh_label',object_type=UILabelObject,
                        row_index=4,col_index=1,row_span=1,col_span=1,min_width=100,min_height=30)
        self.cv_large_step_thresh_label:UILabelObject = self.cv_large_step_thresh_label.add_label_to_grid_frame(name='CV Lrg Step:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cv_large_step_thresh_data =  UIObject(name=f'label_{page_name}_{reg_name}cv_large_step_thresh_data',object_type=UILabelObject,
                            row_index=4,col_index=2,row_span=1,col_span=1,min_width=10,min_height=30)
        self.cv_large_step_thresh_data:UILabelObject = self.cv_large_step_thresh_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass    
         
    def update_i2c_data(self,rb_u16):
        reg = READ19()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        cv_small_step_thresh, cv_large_step_thresh = process_read19_command(rb_u16)
        cv_small_step_thresh_mV = cv_small_step_thresh*params.LS1_THRESH_RESOLUTION_MV
        cv_large_step_thresh_mV = cv_large_step_thresh*params.LS1_THRESH_RESOLUTION_MV

        self.cv_small_step_thresh_data.setText(f'{cv_small_step_thresh_mV:g} mV')
        self.cv_large_step_thresh_data.setText(f'{cv_large_step_thresh_mV:g} mV')
        return reg 
    
class INNO4_READ20_REG_UI():
    """Creates an I2C control UI frame for Read20 register"""
    reg_label = 'READ20'
    def __init__(self, frame:QFrame, gridLayout:QGridLayout, *args, **kwargs):
        self.frame:QFrame = frame
        self.gridLayout = gridLayout
        self.reg_type = READ20()
        reg_name = 'read20_reg'
        self.reg_label = 'READ20'
        label = f'{self.reg_label}, 0x{Inno4Pro_I2C_Readback_Registers.READ20:02X}'
        self.reg_address_byte = Inno4Pro_I2C_Readback_Registers.READ20
        # Add Register Name
        self.name = UIObject(name=f'label_{page_name}_{reg_name}_name',object_type=UILabelObject,
                        row_index=1,col_index=1,row_span=1,col_span=2,min_width=30,min_height=30)
        self.name:UILabelObject = self.name.add_label_to_grid_frame(name=label,frame=self.frame,grid_layout=self.gridLayout)
        
        self.send =  UIObject(name = f'btn_{page_name}_{reg_name}_send',object_type=UIPushButtonObject,
                            row_index=2,col_index=3,row_span=1,col_span=2,min_width=30, min_height=20)
        self.send:UIPushButtonObject = self.send.add_pushbutton_to_grid_frame(name="Send",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.queue =  UIObject(name = f'btn_{page_name}_{reg_name}_queue',object_type=UIPushButtonObject,
                            row_index=1,col_index=3,row_span=1,col_span=2,min_width=30, min_height=20)
        self.queue:UIPushButtonObject = self.queue.add_pushbutton_to_grid_frame(name="Queue",\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.i2c_data =  UIObject(name=f'label_{page_name}_{reg_name}_i2c_data',object_type=UILabelObject,
                            row_index=2,col_index=1,row_span=1,col_span=2,min_width=80,min_height=30)
        self.i2c_data:UILabelObject = self.i2c_data.add_label_to_grid_frame(name='Data: 0x0000',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cc_small_step_thresh_label = UIObject(name=f'label_{page_name}_{reg_name}_cc_small_step_thresh_label',object_type=UILabelObject,
                        row_index=3,col_index=1,row_span=1,col_span=1,min_width=100,min_height=30)
        self.cc_small_step_thresh_label:UILabelObject = self.cc_small_step_thresh_label.add_label_to_grid_frame(name='CC Sml Step:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cc_small_step_thresh_data =  UIObject(name=f'label_{page_name}_{reg_name}_cc_small_step_thresh_data',object_type=UILabelObject,
                            row_index=3,col_index=2,row_span=1,col_span=1,min_width=10,min_height=30)
        self.cc_small_step_thresh_data:UILabelObject = self.cc_small_step_thresh_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.cc_large_step_thresh_label = UIObject(name=f'label_{page_name}_{reg_name}_cc_large_step_thresh_label',object_type=UILabelObject,
                        row_index=4,col_index=1,row_span=1,col_span=1,min_width=100,min_height=30)
        self.cc_large_step_thresh_label:UILabelObject = self.cc_large_step_thresh_label.add_label_to_grid_frame(name='CC Lrg Step:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.cc_large_step_thresh_data =  UIObject(name=f'label_{page_name}_{reg_name}_cc_large_step_thresh_data',object_type=UILabelObject,
                            row_index=4,col_index=2,row_span=1,col_span=1,min_width=10,min_height=30)
        self.cc_large_step_thresh_data:UILabelObject = self.cc_large_step_thresh_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.small_step_size_label = UIObject(name=f'label_{page_name}_{reg_name}_small_step_size_label',object_type=UILabelObject,
                        row_index=3,col_index=3,row_span=1,col_span=1,min_width=100,min_height=30)
        self.small_step_size_label:UILabelObject = self.small_step_size_label.add_label_to_grid_frame(name='Sml Step:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.small_step_size_data =  UIObject(name=f'label_{page_name}_{reg_name}_small_step_size_data',object_type=UILabelObject,
                            row_index=3,col_index=4,row_span=1,col_span=1,min_width=10,min_height=30)
        self.small_step_size_data:UILabelObject = self.small_step_size_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
        
        self.large_step_size_label = UIObject(name=f'label_{page_name}_{reg_name}_large_step_size_label',object_type=UILabelObject,
                        row_index=4,col_index=3,row_span=1,col_span=1,min_width=100,min_height=30)
        self.large_step_size_label:UILabelObject = self.large_step_size_label.add_label_to_grid_frame(name='Lrg Step:',frame=self.frame,grid_layout=self.gridLayout)
        
        self.large_step_size_data =  UIObject(name=f'label_{page_name}_{reg_name}_large_step_size_data',object_type=UILabelObject,
                            row_index=4,col_index=4,row_span=1,col_span=1,min_width=10,min_height=30)
        self.large_step_size_data:UILabelObject = self.large_step_size_data.add_label_to_grid_frame(name='',\
                                            frame=self.frame,grid_layout=self.gridLayout)
    
    def validate(self):
        pass
         
    def update_i2c_data(self,rb_u16):
        reg = READ20()
        reg.asbyte = rb_u16
        self.i2c_data.setText(f'Data: 0x{reg.asbyte:04X}')
        cc_small_step_thresh, cc_large_step_thresh, small_step_size, large_step_size = process_read20_command(rb_u16)
        small_step_size_mV = small_step_size*params.LS2_STEP_RESOLUTION_MV
        large_step_size_mV = large_step_size*params.LS2_STEP_RESOLUTION_MV

        self.cc_small_step_thresh_data.setText(f'{cc_small_step_thresh:g}')
        self.cc_large_step_thresh_data.setText(f'{cc_large_step_thresh:g}')
        self.small_step_size_data.setText(f'{small_step_size_mV:g} mV')
        self.large_step_size_data.setText(f'{large_step_size_mV:g} mV')
        return reg 
    
INNO4_I2C_COMMAND_REG_LIST = [
    INNO4_CV_Reg_UI,
    INNO4_CC_Reg_UI,
    INNO4_CDC_Reg_UI,
    INNO4_VKP_Reg_UI,
    INNO4_CVO_Reg_UI,
    INNO4_OVA_Reg_UI,
    INNO4_UVA_Reg_UI,
    INNO4_VBUSSC_Reg_UI,
    INNO4_CCSC_Reg_UI,
    INNO4_ISSC_Reg_UI,
    INNO4_VDIS_Reg_UI,
    INNO4_BLEEDER_Reg_UI,
    INNO4_FAST_VI_Reg_UI,
    INNO4_TURN_OFF_PSU_Reg_UI,
    None,
    INNO4_WRITE_REG_UI,
    None,
    INNO4_DCM_ONLY_Reg_UI,
    None,
    INNO4_INT_MASK_Reg_UI,
    INNO4_LOOP_SPEED_1_Reg_UI,
    INNO4_LOOP_SPEED_2_Reg_UI,
    INNO4_FWD_PEAK_Reg_UI,
    INNO4_FAST_CC_Reg_UI,   
]

INNO4_I2C_READBACK_REG_LIST = [
    INNO4_READ_REG_UI,
    INNO4_READ0_REG_UI,
    INNO4_READ1_REG_UI,
    INNO4_READ2_REG_UI,
    INNO4_READ3_REG_UI,
    INNO4_READ4_REG_UI,
    INNO4_READ5_REG_UI,
    INNO4_READ6_REG_UI,
    INNO4_READ7_REG_UI,
    INNO4_READ8_REG_UI,
    INNO4_READ9_REG_UI,
    INNO4_READ10_REG_UI,
    INNO4_READ11_REG_UI,
    INNO4_READ12_REG_UI,
    INNO4_READ13_REG_UI,
    INNO4_READ14_REG_UI,
    None,
    INNO4_READ16_REG_UI,
    INNO4_READ17_REG_UI,
    INNO4_READ18_REG_UI,
    INNO4_READ19_REG_UI,
    INNO4_READ20_REG_UI,
]