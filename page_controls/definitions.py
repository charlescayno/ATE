from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *



import files_rc

# Definition of th page numbers in the stack widgets

class StackWidget1Pages:
    EmptyPage = 0
    LineVoltageRange = 1
    LineRamp = 2

class StackWidget2Pages:
    EmptyPage = 0
    LoadCurrentRange = 1
    CVCCSettings = 2

class StackWidget3Pages:
    EmptyPage = 0
    USBPD_Options = 1
    I2C_Options = 2
    
class StackWidgetI2CControlsPages:
    EmptyPage = 0
    Registers = 1
    ReadbackRegisters = 2

UIPushButtonObject = QPushButton
UILineEditObject = QLineEdit
UIComboBoxObject = QComboBox
UILabelObject = QLabel
UICheckboxObject = QCheckBox

class UIObjectStyle():
    
    PushButtonStyle:str = u"QPushButton {\n" \
        "	border: 2px solid rgb(52, 59, 72);\n" \
        "	border-radius: 5px;	\n" \
        "	background-color: rgb(52, 59, 72);\n" \
        "}\n" \
        "QPushButton:hover {\n" \
        "	background-color: rgb(57, 65, 80);\n" \
        "	border: 2px solid rgb(61, 70, 86);\n" \
        "}\n" \
        "QPushButton:pressed {	\n" \
        "	background-color: rgb(35, 40, 49);\n" \
        "	border: 2px solid rgb(43, 50, 61);\n" \
        "}\n" \
        "QPushButton:disabled {	\n" \
        "	background-color: rgb(25, 30, 39);\n" \
        "	border: 2px solid rgb(33, 40, 51);\n" \
        "	color: rgb(71, 71, 71);\n" \
        "}"

    PushButtonStyle_Success:str = u"QPushButton {\n" \
        "	border: 2px solid green;\n" \
        "	border-radius: 5px;	\n" \
        "	background-color: rgb(52, 59, 72);\n" \
        "}\n" \
        "QPushButton:hover {\n" \
        "	background-color: rgb(57, 65, 80);\n" \
        "	border: 2px solid rgb(61, 70, 86);\n" \
        "}\n" \
        "QPushButton:pressed {	\n" \
        "	background-color: rgb(35, 40, 49);\n" \
        "	border: 2px solid rgb(43, 50, 61);\n" \
        "}\n" \
        "QPushButton:disabled {	\n" \
        "	background-color: rgb(25, 30, 39);\n" \
        "	border: 2px solid rgb(33, 40, 51);\n" \
        "	color: rgb(71, 71, 71);\n" \
        "}"
        
    PushButtonStyle_Fail:str = u"QPushButton {\n" \
        "	border: 2px solid red;\n" \
        "	border-radius: 5px;	\n" \
        "	background-color: rgb(52, 59, 72);\n" \
        "}\n" \
        "QPushButton:hover {\n" \
        "	background-color: rgb(57, 65, 80);\n" \
        "	border: 2px solid rgb(61, 70, 86);\n" \
        "}\n" \
        "QPushButton:pressed {	\n" \
        "	background-color: rgb(35, 40, 49);\n" \
        "	border: 2px solid rgb(43, 50, 61);\n" \
        "}\n" \
        "QPushButton:disabled {	\n" \
        "	background-color: rgb(25, 30, 39);\n" \
        "	border: 2px solid rgb(33, 40, 51);\n" \
        "	color: rgb(71, 71, 71);\n" \
        "}"
    
    LineEditStyle:str = u"QLineEdit {\n" \
        "	background-color: rgb(27, 29, 35);\n" \
        "	border-radius: 5px;\n" \
        "	border: 2px solid rgb(27, 29, 35);\n" \
        "	padding-left: 10px;\n" \
        "}\n" \
        "QLineEdit:hover {\n" \
        "	border: 2px solid rgb(64, 71, 88);\n" \
        "}\n" \
        "QLineEdit:focus {\n" \
        "	border: 2px solid rgb(91, 101, 124);\n" \
        "}\n" \
        "QLineEdit:disabled{\n" \
        "	color: rgb(71, 71, 71);\n" \
        "	background-color: rgb(37, 39, 45);\n" \
        "	border-radius: 5px;\n" \
        "	border: 2px solid rgb(37, 39, 45);\n" \
        "	padding-left: 10px;\n" \
        "}"

    ComboBoxStyle:str = u"QComboBox:disabled{\n" \
        "   color: rgb(71, 71, 71)\n" \
        "}"
            
    
    LabelStyle:str = u"QLabel:disabled{\n" \
        "	color: rgb(71, 71, 71)\n" \
        "}"
    
    CheckboxStyle:str = u"QCheckBox:disabled{\n" \
        "	color: rgb(71, 71, 71)\n" \
        "}"
        

UIObjectStyleList:list = [
        UIObjectStyle.PushButtonStyle,
        UIObjectStyle.LineEditStyle,
        UIObjectStyle.ComboBoxStyle,
        UIObjectStyle.LabelStyle,
        UIObjectStyle.CheckboxStyle,
    ]
    
UIObjectTypes = [
    UIPushButtonObject,
    UILineEditObject,
    UIComboBoxObject,
    UILabelObject,
    UICheckboxObject,
]

class UIObject():
    """ Creates a QT Widget. Can be added to a frame with a layout"""
    
    def __init__(self, name:str, object_type:UIPushButtonObject, row_index:int=1, col_index:int=1,row_span:int=1, col_span:int=1, min_width:int = 0, min_height:int = 0, *args, **kwargs):
        self.name:str = name
        self.object_type:UIPushButtonObject = object_type
        self.row_index:int = row_index
        self.col_index:int = col_index
        self.row_span:int = row_span
        self.col_span:int = col_span
        self.min_width:int = min_width
        self.min_height:int = min_height
        
        self.sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        
        self.font = QFont()
        self.font.setPointSize(12)

    
    def add_to_grid_frame(self,frame:QFrame,grid_layout:QGridLayout):
        """ Adds the QT Widget to frame in a grid layout"""
        self.object:QWidget = self.object_type(frame)
        self.object.setObjectName(self.name)
        self.object.setEnabled(True)
        self.sizePolicy.setHeightForWidth(self.object.sizePolicy().hasHeightForWidth())
        self.object.setSizePolicy(self.sizePolicy)
        self.object.setMinimumSize(QSize(self.min_width, self.min_height))
        self.object.setMaximumSize(QSize(16777215, 16777215))
        self.object.setFont(self.font)
        self.object.setStyleSheet(UIObjectStyleList[UIObjectTypes.index(self.object_type)])
        grid_layout.addWidget(self.object, self.row_index, self.col_index, self.row_span, self.col_span)
        
        return self.object
    
    def add_pushbutton_to_grid_frame(self,name,frame:QFrame,grid_layout:QGridLayout):
        self.object:UIPushButtonObject = self.add_to_grid_frame(frame = frame,grid_layout = grid_layout)
        self.object.setText(QCoreApplication.translate("MainWindow", name, None))
        return self.object
        
    def add_lineedit_to_grid_frame(self,placeholder, max_value:float, min_value:float,frame:QFrame,grid_layout:QGridLayout):
        self.object:UILineEditObject = self.add_to_grid_frame(frame = frame,grid_layout = grid_layout)
        self.object.setPlaceholderText(QCoreApplication.translate("MainWindow", placeholder, None))
        validator = QDoubleValidator(min_value, max_value, 3)
        self.object.setValidator(validator)
        return self.object
    
    def add_checkbox_to_grid_frame(self,name,init_state,tristate,frame:QFrame,grid_layout:QGridLayout):
        self.object:UICheckboxObject = self.add_to_grid_frame(frame = frame,grid_layout = grid_layout)
        self.object.setText(QCoreApplication.translate("MainWindow", name, None))
        self.object.setChecked(init_state)
        self.object.setTristate(tristate)
        return self.object
    
    def add_combobox_to_grid_frame(self,options_list,frame:QFrame,grid_layout:QGridLayout):
        self.object:UIComboBoxObject = self.add_to_grid_frame(frame = frame,grid_layout = grid_layout)
        self.object.clear()
        self.object.addItems(options_list)
        return self.object
    
    def add_label_to_grid_frame(self,name,frame:QFrame,grid_layout:QGridLayout):
        self.object:UILabelObject = self.add_to_grid_frame(frame = frame,grid_layout = grid_layout)
        self.object.setText(name)
        self.object.setAlignment(Qt.AlignCenter)
        return self.object
    
    def add_to_vertical_frame(self,frame:QFrame,vert_layout:QVBoxLayout):
        """ Adds the QT Widget to frame in a vertical layout"""
        # row span in this instance correspond to vertical stretch, and objects are added sequentially
        self.object:QWidget = self.object_type(frame)
        self.object.setObjectName(self.name)
        self.object.setEnabled(True)
        self.sizePolicy.setHeightForWidth(self.object.sizePolicy().hasHeightForWidth())
        self.object.setSizePolicy(self.sizePolicy)
        self.object.setMinimumSize(QSize(self.min_width, self.min_height))
        self.object.setMaximumSize(QSize(16777215, 16777215))
        self.object.setFont(self.font)
        self.object.setStyleSheet(UIObjectStyleList[UIObjectTypes.index(self.object_type)])
        vert_layout.addWidget(self.object, self.row_span)
        
        return self.object
    
    def add_pushbutton_to_vertical_frame(self,name,frame:QFrame,vert_layout:QVBoxLayout):
        self.object:UIPushButtonObject = self.add_to_vertical_frame(frame = frame,vert_layout = vert_layout)
        self.object.setText(QCoreApplication.translate("MainWindow", name, None))
        return self.object
        
    def add_lineedit_to_vertical_frame(self,placeholder, max_value:float, min_value:float,frame:QFrame,vert_layout:QVBoxLayout):
        self.object:UILineEditObject = self.add_to_vertical_frame(frame = frame,vert_layout = vert_layout)
        self.object.setPlaceholderText(QCoreApplication.translate("MainWindow", placeholder, None))
        validator = QDoubleValidator(min_value, max_value, 3)
        self.object.setValidator(validator)
        return self.object
    
    def add_checkbox_to_vertical_frame(self,name,init_state,tristate,frame:QFrame,vert_layout:QVBoxLayout):
        self.object:UICheckboxObject = self.add_to_vertical_frame(frame = frame,vert_layout = vert_layout)
        self.object.setText(QCoreApplication.translate("MainWindow", name, None))
        self.object.setChecked(init_state)
        self.object.setTristate(tristate)
        return self.object
    
    def add_combobox_to_vertical_frame(self,options_list,frame:QFrame,vert_layout:QVBoxLayout):
        self.object:UIComboBoxObject = self.add_to_vertical_frame(frame = frame,vert_layout = vert_layout)
        self.object.clear()
        self.object.addItems(options_list)
        return self.object
    
    def add_label_to_vertical_frame(self,name,frame:QFrame,vert_layout:QVBoxLayout):
        self.object:UILabelObject = self.add_to_vertical_frame(frame = frame,vert_layout = vert_layout)
        self.object.setText(name)
        self.object.setAlignment(Qt.AlignCenter)
        return self.object
    
    def add_to_horizontal_frame(self,frame:QFrame,horz_layout:QHBoxLayout):
        """ Adds the QT Widget to frame in a horizontal layout"""
        # col span in this instance correspond to horizontal stretch, and objects are added sequentially
        self.object:QWidget = self.object_type(frame)
        self.object.setObjectName(self.name)
        self.object.setEnabled(True)
        self.sizePolicy.setHeightForWidth(self.object.sizePolicy().hasHeightForWidth())
        self.object.setSizePolicy(self.sizePolicy)
        self.object.setMinimumSize(QSize(self.min_width, self.min_height))
        self.object.setMaximumSize(QSize(16777215, 16777215))
        self.object.setFont(self.font)
        self.object.setStyleSheet(UIObjectStyleList[UIObjectTypes.index(self.object_type)])
        horz_layout.addWidget(self.object, self.col_span)
        
        return self.object
    
    def add_pushbutton_to_horizontal_frame(self,name,frame:QFrame,horz_layout:QHBoxLayout):
        self.object:UIPushButtonObject = self.add_to_horizontal_frame(frame = frame,horz_layout = horz_layout)
        self.object.setText(QCoreApplication.translate("MainWindow", name, None))
        return self.object
        
    def add_lineedit_to_horizontal_frame(self,placeholder, max_value:float, min_value:float,frame:QFrame,horz_layout:QHBoxLayout):
        self.object:UILineEditObject = self.add_to_horizontal_frame(frame = frame,horz_layout = horz_layout)
        self.object.setPlaceholderText(QCoreApplication.translate("MainWindow", placeholder, None))
        validator = QDoubleValidator(min_value, max_value, 3)
        self.object.setValidator(validator)
        return self.object
    
    def add_checkbox_to_horizontal_frame(self,name,init_state,tristate,frame:QFrame,horz_layout:QHBoxLayout):
        self.object:UICheckboxObject = self.add_to_horizontal_frame(frame = frame,horz_layout = horz_layout)
        self.object.setText(QCoreApplication.translate("MainWindow", name, None))
        self.object.setChecked(init_state)
        self.object.setTristate(tristate)
        return self.object
    
    def add_combobox_to_horizontal_frame(self,options_list,frame:QFrame,horz_layout:QHBoxLayout):
        self.object:UIComboBoxObject = self.add_to_horizontal_frame(frame = frame,horz_layout = horz_layout)
        self.object.clear()
        self.object.addItems(options_list)
        return self.object
    
    def add_label_to_horizontal_frame(self,name,frame:QFrame,horz_layout:QHBoxLayout):
        self.object:UILabelObject = self.add_to_horizontal_frame(frame = frame,horz_layout = horz_layout)
        self.object.setText(name)
        self.object.setAlignment(Qt.AlignCenter)
        return self.object

class I2CCommandObject():
    """ Creates an I2C Command Object Used in i2c_controls page for the i2c command table"""
    def __init__(self, name:str = None, value:str = None, extra_params:list = None, *args, **kwargs):
        self.name = name
        self.value = value
        self.extra_params = extra_params
    
    def get_dict(self)->dict:
        """" Create dictionary based on parameters"""
        d = {'COMMAND_NAME':            self.name, 
            'COMMAND_VALUE':            self.value,
            'COMMAND_EXTRA_PARAMS':     self.extra_params}
        return d
    
    def extract_params_from_dict(self,d:dict):
        """" Update parameters based on dictionary"""
        self.name = d['COMMAND_NAME']
        self.value = d['COMMAND_VALUE']
        self.extra_params = d['COMMAND_EXTRA_PARAMS']
        
        
    
    
        
    
    