from PySide2 import QtCore
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

def inject_ui(self):
    font = QFont()
    font.setFamily(u"Segoe UI")
    font.setPointSize(10)
    font1 = QFont()
    font1.setFamily(u"Segoe UI")
    font1.setPointSize(10)
    font1.setBold(True)
    font1.setWeight(75)
    font2 = QFont()
    font2.setFamily(u"Segoe UI")
    font3 = QFont()
    font3.setFamily(u"Segoe UI")
    font3.setBold(True)
    font3.setWeight(75)
    font4 = QFont()
    font4.setFamily(u"Segoe UI")
    font4.setPointSize(12)
    font5 = QFont()
    font5.setPointSize(14)
    font6 = QFont()
    font6.setFamily(u"Segoe UI")
    font6.setPointSize(18)
    font7 = QFont()
    font7.setFamily(u"Segoe UI")
    font7.setPointSize(15)
    font8 = QFont()
    font8.setFamily(u"Segoe UI")
    font8.setPointSize(40)
    font9 = QFont()
    font9.setFamily(u"Segoe UI")
    font9.setPointSize(14)
    font9.setBold(True)
    font9.setWeight(75)
    font10 = QFont()
    font10.setPointSize(12)
    font11 = QFont()
    font11.setFamily(u"Segoe UI")
    font11.setPointSize(10)
    font11.setBold(False)
    font11.setWeight(50)
    font12 = QFont()
    font12.setFamily(u"Consolas")
    font12.setPointSize(25)
    font12.setBold(False)
    font12.setItalic(False)
    font12.setWeight(50)
    font12.setKerning(False)
    font13 = QFont()
    font13.setFamily(u"Segoe UI")
    font13.setPointSize(9)
    font14 = QFont()
    font14.setPointSize(9)
    font15 = QFont()
    font15.setFamily(u"Consolas")
    font15.setPointSize(14)
    font16 = QFont()
    font16.setPointSize(8)
    font17 = QFont()
    font17.setFamily(u"MS Shell Dlg 2")
    font17.setPointSize(12)
    font18 = QFont()
    font18.setFamily(u"Segoe UI")
    font18.setPointSize(16)
    font18.setBold(True)
    font18.setWeight(75)
    font19 = QFont()
    font19.setPointSize(10)
    font20 = QFont()
    font20.setFamily(u"MS Shell Dlg 2")
    font20.setPointSize(12)
    font20.setBold(True)
    font20.setWeight(75)
    font21 = QFont()
    font21.setFamily(u"Consolas")
    font21.setPointSize(20)
    font21.setBold(False)
    font21.setItalic(False)
    font21.setWeight(50)
    font21.setKerning(False)
    font22 = QFont()
    font22.setPointSize(12)
    font22.setBold(True)
    font22.setWeight(75)

    # ELOAD 2
    self.ui.frame_manual_control_eload_2 = QFrame(self.ui.frame_manual_control_lower)
    self.ui.frame_manual_control_eload_2.setObjectName(u"frame_manual_control_eload_2")
    sizePolicy20 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
    sizePolicy20.setHorizontalStretch(3)
    sizePolicy20.setVerticalStretch(0)
    sizePolicy20.setHeightForWidth(self.ui.frame_manual_control_eload_2.sizePolicy().hasHeightForWidth())
    self.ui.frame_manual_control_eload_2.setSizePolicy(sizePolicy20)
    self.ui.frame_manual_control_eload_2.setMinimumSize(QtCore.QSize(400, 0))
    self.ui.frame_manual_control_eload_2.setStyleSheet(u"QFrame{\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "}")
    self.ui.frame_manual_control_eload_2.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2.setFrameShadow(QFrame.Raised)
    self.ui.verticalLayout_23_2 = QVBoxLayout(self.ui.frame_manual_control_eload_2)
    self.ui.verticalLayout_23_2.setObjectName(u"verticalLayout_23_2")
    self.ui.label_manual_control_eload_2 = QLabel(self.ui.frame_manual_control_eload_2)
    self.ui.label_manual_control_eload_2.setObjectName(u"label_manual_control_eload_2")
    self.ui.label_manual_control_eload_2.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_2.setFont(font1)
    self.ui.label_manual_control_eload_2.setCursor(QCursor(Qt.UpArrowCursor))
    self.ui.label_manual_control_eload_2.setStyleSheet(u"QLabel{border:none;}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_manual_control_eload_2.setAlignment(Qt.AlignCenter)
    
    self.ui.verticalLayout_23_2.addWidget(self.ui.label_manual_control_eload_2)
    
    self.ui.frame_manual_control_eload_2_contents = QFrame(self.ui.frame_manual_control_eload_2)
    self.ui.frame_manual_control_eload_2_contents.setObjectName(u"frame_manual_control_eload_contents_2")
    self.ui.frame_manual_control_eload_2_contents.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_2_contents.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_contents.setFrameShadow(QFrame.Raised)
    self.verticalLayout_77 = QVBoxLayout(self.ui.frame_manual_control_eload_2_contents)
    self.verticalLayout_77.setObjectName(u"verticalLayout_77")
    self.ui.frame_manual_control_eload_2_top = QFrame(self.ui.frame_manual_control_eload_2_contents)
    self.ui.frame_manual_control_eload_2_top.setObjectName(u"frame_manual_control_eload_top_2")
    self.ui.frame_manual_control_eload_2_top.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_top.setFrameShadow(QFrame.Raised)
    self.horizontalLayout_47 = QHBoxLayout(self.ui.frame_manual_control_eload_2_top)
    self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
    self.cbx_manual_control_eload_type = QComboBox(self.ui.frame_manual_control_eload_2_top)
    self.cbx_manual_control_eload_type.addItem("")
    self.cbx_manual_control_eload_type.addItem("")
    self.cbx_manual_control_eload_type.addItem("")
    self.cbx_manual_control_eload_type.setObjectName(u"cbx_manual_control_eload_type")
    self.cbx_manual_control_eload_type.setMaximumSize(QtCore.QSize(16777215, 40))
    self.cbx_manual_control_eload_type.setFont(font10)
    self.cbx_manual_control_eload_type.setStyleSheet(u"QComboBox{\n"
    "border: 2px solid black;\n"
    "border-radius:5px;\n"
    "}\n"
    "\n"
    "QComboBox:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    
    self.horizontalLayout_47.addWidget(self.cbx_manual_control_eload_type)
    
    self.ui.btn_manual_control_eload_a_b_swap_2 = QPushButton(self.ui.frame_manual_control_eload_2_top)
    self.ui.btn_manual_control_eload_a_b_swap_2.setObjectName(u"btn_manual_control_eload_a_b_swap_2")
    self.ui.btn_manual_control_eload_a_b_swap_2.setMinimumSize(QtCore.QSize(120, 40))
    self.ui.btn_manual_control_eload_a_b_swap_2.setFont(font13)
    self.ui.btn_manual_control_eload_a_b_swap_2.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    icon10 = QIcon()
    icon10.addFile(u":/20x20/icons/20x20/cil-swap-horizontal.png", QtCore.QSize(), QIcon.Normal, QIcon.Off)
    self.ui.btn_manual_control_eload_a_b_swap_2.setIcon(icon10)
    self.ui.btn_manual_control_eload_a_b_swap_2.setCheckable(False)
    self.ui.btn_manual_control_eload_a_b_swap_2.setChecked(False)
    
    self.horizontalLayout_47.addWidget(self.ui.btn_manual_control_eload_a_b_swap_2)
    
    
    self.verticalLayout_77.addWidget(self.ui.frame_manual_control_eload_2_top)
    
    self.ui.frame_manual_control_eload_2_center = QFrame(self.ui.frame_manual_control_eload_2_contents)
    self.ui.frame_manual_control_eload_2_center.setObjectName(u"frame_manual_control_eload_center_2")
    self.ui.frame_manual_control_eload_2_center.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_center.setFrameShadow(QFrame.Raised)
    self.horizontalLayout_46 = QHBoxLayout(self.ui.frame_manual_control_eload_2_center)
    self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
    self.ui.frame_manual_control_eload_2_level = QFrame(self.ui.frame_manual_control_eload_2_center)
    self.ui.frame_manual_control_eload_2_level.setObjectName(u"frame_manual_control_eload_level_2")
    self.ui.frame_manual_control_eload_2_level.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_level.setFrameShadow(QFrame.Raised)
    self.verticalLayout_70 = QVBoxLayout(self.ui.frame_manual_control_eload_2_level)
    self.verticalLayout_70.setObjectName(u"verticalLayout_70")
    self.ui.frame_manual_control_eload_2_a = QFrame(self.ui.frame_manual_control_eload_2_level)
    self.ui.frame_manual_control_eload_2_a.setObjectName(u"frame_manual_control_eload_a_2")
    self.ui.frame_manual_control_eload_2_a.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_a.setFrameShadow(QFrame.Raised)
    self.horizontalLayout_45 = QHBoxLayout(self.ui.frame_manual_control_eload_2_a)
    self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
    self.ui.label_manual_control_eload_2_a = QLabel(self.ui.frame_manual_control_eload_2_a)
    self.ui.label_manual_control_eload_2_a.setObjectName(u"label_manual_control_eload_a_2")
    self.ui.label_manual_control_eload_2_a.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_2_a.setFont(font10)
    self.ui.label_manual_control_eload_2_a.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.ui.label_manual_control_eload_2_a.setAlignment(Qt.AlignCenter)
    
    self.horizontalLayout_45.addWidget(self.ui.label_manual_control_eload_2_a)
    
    self.ui.lineedit_manual_control_eload_a_level_2 = QLineEdit(self.ui.frame_manual_control_eload_2_a)
    self.ui.lineedit_manual_control_eload_a_level_2.setObjectName(u"lineedit_manual_control_eload_a_level_2")
    sizePolicy21 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    sizePolicy21.setHorizontalStretch(4)
    sizePolicy21.setVerticalStretch(0)
    sizePolicy21.setHeightForWidth(self.ui.lineedit_manual_control_eload_a_level_2.sizePolicy().hasHeightForWidth())
    self.ui.lineedit_manual_control_eload_a_level_2.setSizePolicy(sizePolicy21)
    self.ui.lineedit_manual_control_eload_a_level_2.setMinimumSize(QtCore.QSize(0, 40))
    self.ui.lineedit_manual_control_eload_a_level_2.setFont(font10)
    self.ui.lineedit_manual_control_eload_a_level_2.setStyleSheet(u"QLineEdit {\n"
    "	background-color: rgb(27, 29, 35);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(27, 29, 35);\n"
    "	padding-left: 10px;\n"
    "}\n"
    "QLineEdit:hover {\n"
    "	border: 2px solid rgb(64, 71, 88);\n"
    "}\n"
    "QLineEdit:focus {\n"
    "	border: 2px solid rgb(91, 101, 124);\n"
    "}\n"
    "\n"
    "QLineEdit:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "	background-color: rgb(37, 39, 45);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(37, 39, 45);\n"
    "	padding-left: 10px;\n"
    "}")
    
    self.horizontalLayout_45.addWidget(self.ui.lineedit_manual_control_eload_a_level_2)
    
    self.ui.label_manual_control_eload_2_a_level_unit = QLabel(self.ui.frame_manual_control_eload_2_a)
    self.ui.label_manual_control_eload_2_a_level_unit.setObjectName(u"label_manual_control_eload_a_level_unit")
    sizePolicy11.setHeightForWidth(self.ui.label_manual_control_eload_2_a_level_unit.sizePolicy().hasHeightForWidth())
    self.ui.label_manual_control_eload_2_a_level_unit.setSizePolicy(sizePolicy11)
    self.ui.label_manual_control_eload_2_a_level_unit.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_2_a_level_unit.setFont(font10)
    self.ui.label_manual_control_eload_2_a_level_unit.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    
    self.horizontalLayout_45.addWidget(self.ui.label_manual_control_eload_2_a_level_unit)
    
    self.btn_manual_control_eload_set_A = QPushButton(self.ui.frame_manual_control_eload_2_a)
    self.btn_manual_control_eload_set_A.setObjectName(u"btn_manual_control_eload_set_A")
    self.btn_manual_control_eload_set_A.setMinimumSize(QtCore.QSize(50, 30))
    self.btn_manual_control_eload_set_A.setFont(font4)
    self.btn_manual_control_eload_set_A.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    self.btn_manual_control_eload_set_A.setCheckable(False)
    self.btn_manual_control_eload_set_A.setChecked(False)
    
    self.horizontalLayout_45.addWidget(self.btn_manual_control_eload_set_A)
    
    
    self.verticalLayout_70.addWidget(self.ui.frame_manual_control_eload_2_a)
    
    self.ui.frame_manual_control_eload_2_b = QFrame(self.ui.frame_manual_control_eload_2_level)
    self.ui.frame_manual_control_eload_2_b.setObjectName(u"frame_manual_control_eload_b_2")
    self.ui.frame_manual_control_eload_2_b.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_b.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_39_2 = QHBoxLayout(self.ui.frame_manual_control_eload_2_b)
    self.ui.horizontalLayout_39_2.setObjectName(u"horizontalLayout_39_2")
    self.ui.label_manual_control_eload_2_b = QLabel(self.ui.frame_manual_control_eload_2_b)
    self.ui.label_manual_control_eload_2_b.setObjectName(u"label_manual_control_eload_b_2")
    self.ui.label_manual_control_eload_2_b.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_2_b.setFont(font10)
    self.ui.label_manual_control_eload_2_b.setLayoutDirection(Qt.LeftToRight)
    self.ui.label_manual_control_eload_2_b.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.ui.label_manual_control_eload_2_b.setAlignment(Qt.AlignCenter)
    
    self.ui.horizontalLayout_39_2.addWidget(self.ui.label_manual_control_eload_2_b)
    
    self.ui.lineedit_manual_control_eload_b_level_2 = QLineEdit(self.ui.frame_manual_control_eload_2_b)
    self.ui.lineedit_manual_control_eload_b_level_2.setObjectName(u"lineedit_manual_control_eload_b_level_2")
    sizePolicy21.setHeightForWidth(self.ui.lineedit_manual_control_eload_b_level_2.sizePolicy().hasHeightForWidth())
    self.ui.lineedit_manual_control_eload_b_level_2.setSizePolicy(sizePolicy21)
    self.ui.lineedit_manual_control_eload_b_level_2.setMinimumSize(QtCore.QSize(0, 40))
    self.ui.lineedit_manual_control_eload_b_level_2.setFont(font10)
    self.ui.lineedit_manual_control_eload_b_level_2.setStyleSheet(u"QLineEdit {\n"
    "	background-color: rgb(27, 29, 35);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(27, 29, 35);\n"
    "	padding-left: 10px;\n"
    "}\n"
    "QLineEdit:hover {\n"
    "	border: 2px solid rgb(64, 71, 88);\n"
    "}\n"
    "QLineEdit:focus {\n"
    "	border: 2px solid rgb(91, 101, 124);\n"
    "}\n"
    "\n"
    "QLineEdit:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "	background-color: rgb(37, 39, 45);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(37, 39, 45);\n"
    "	padding-left: 10px;\n"
    "}")
    
    self.ui.horizontalLayout_39_2.addWidget(self.ui.lineedit_manual_control_eload_b_level_2)
    
    self.ui.label_manual_control_eload_2_b_level_unit = QLabel(self.ui.frame_manual_control_eload_2_b)
    self.ui.label_manual_control_eload_2_b_level_unit.setObjectName(u"label_manual_control_eload_b_level_unit")
    sizePolicy11.setHeightForWidth(self.ui.label_manual_control_eload_2_b_level_unit.sizePolicy().hasHeightForWidth())
    self.ui.label_manual_control_eload_2_b_level_unit.setSizePolicy(sizePolicy11)
    self.ui.label_manual_control_eload_2_b_level_unit.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_2_b_level_unit.setFont(font10)
    self.ui.label_manual_control_eload_2_b_level_unit.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    
    self.ui.horizontalLayout_39_2.addWidget(self.ui.label_manual_control_eload_2_b_level_unit)
    
    self.btn_manual_control_eload_set_B = QPushButton(self.ui.frame_manual_control_eload_2_b)
    self.btn_manual_control_eload_set_B.setObjectName(u"btn_manual_control_eload_set_B")
    self.btn_manual_control_eload_set_B.setMinimumSize(QtCore.QSize(50, 30))
    self.btn_manual_control_eload_set_B.setFont(font4)
    self.btn_manual_control_eload_set_B.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    self.btn_manual_control_eload_set_B.setCheckable(False)
    self.btn_manual_control_eload_set_B.setChecked(False)
    
    self.ui.horizontalLayout_39_2.addWidget(self.btn_manual_control_eload_set_B)
    
    
    self.verticalLayout_70.addWidget(self.ui.frame_manual_control_eload_2_b)
    
    
    self.horizontalLayout_46.addWidget(self.ui.frame_manual_control_eload_2_level)
    
    self.ui.frame_manual_control_eload_2_slew = QFrame(self.ui.frame_manual_control_eload_2_center)
    self.ui.frame_manual_control_eload_2_slew.setObjectName(u"frame_manual_control_eload_slew_2")
    self.ui.frame_manual_control_eload_2_slew.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_slew.setFrameShadow(QFrame.Raised)
    self.gridLayout_29 = QGridLayout(self.ui.frame_manual_control_eload_2_slew)
    self.gridLayout_29.setObjectName(u"gridLayout_29")
    self.ui.frame_manual_control_eload_2_slew_fall = QFrame(self.ui.frame_manual_control_eload_2_slew)
    self.ui.frame_manual_control_eload_2_slew_fall.setObjectName(u"frame_manual_control_eload_slew_fall_2")
    self.ui.frame_manual_control_eload_2_slew_fall.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_slew_fall.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_38_2 = QHBoxLayout(self.ui.frame_manual_control_eload_2_slew_fall)
    self.ui.horizontalLayout_38_2.setObjectName(u"horizontalLayout_38_2")
    self.label_manual_control_electronic_load_fall = QLabel(self.ui.frame_manual_control_eload_2_slew_fall)
    self.label_manual_control_electronic_load_fall.setObjectName(u"label_manual_control_electronic_load_fall")
    self.label_manual_control_electronic_load_fall.setMaximumSize(QtCore.QSize(16777215, 30))
    self.label_manual_control_electronic_load_fall.setFont(font10)
    self.label_manual_control_electronic_load_fall.setLayoutDirection(Qt.LeftToRight)
    self.label_manual_control_electronic_load_fall.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.label_manual_control_electronic_load_fall.setAlignment(Qt.AlignCenter)
    
    self.ui.horizontalLayout_38_2.addWidget(self.label_manual_control_electronic_load_fall)
    
    self.lineedit_manual_control_eload_slew_fall = QLineEdit(self.ui.frame_manual_control_eload_2_slew_fall)
    self.lineedit_manual_control_eload_slew_fall.setObjectName(u"lineedit_manual_control_eload_slew_fall")
    sizePolicy21.setHeightForWidth(self.lineedit_manual_control_eload_slew_fall.sizePolicy().hasHeightForWidth())
    self.lineedit_manual_control_eload_slew_fall.setSizePolicy(sizePolicy21)
    self.lineedit_manual_control_eload_slew_fall.setMinimumSize(QtCore.QSize(0, 40))
    self.lineedit_manual_control_eload_slew_fall.setFont(font10)
    self.lineedit_manual_control_eload_slew_fall.setStyleSheet(u"QLineEdit {\n"
    "	background-color: rgb(27, 29, 35);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(27, 29, 35);\n"
    "	padding-left: 10px;\n"
    "}\n"
    "QLineEdit:hover {\n"
    "	border: 2px solid rgb(64, 71, 88);\n"
    "}\n"
    "QLineEdit:focus {\n"
    "	border: 2px solid rgb(91, 101, 124);\n"
    "}\n"
    "\n"
    "QLineEdit:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "	background-color: rgb(37, 39, 45);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(37, 39, 45);\n"
    "	padding-left: 10px;\n"
    "}")
    
    self.ui.horizontalLayout_38_2.addWidget(self.lineedit_manual_control_eload_slew_fall)
    
    self.ui.label_manual_control_eload_2_slew_fall_unit = QLabel(self.ui.frame_manual_control_eload_2_slew_fall)
    self.ui.label_manual_control_eload_2_slew_fall_unit.setObjectName(u"label_manual_control_eload_slew_fall_unit")
    sizePolicy11.setHeightForWidth(self.ui.label_manual_control_eload_2_slew_fall_unit.sizePolicy().hasHeightForWidth())
    self.ui.label_manual_control_eload_2_slew_fall_unit.setSizePolicy(sizePolicy11)
    self.ui.label_manual_control_eload_2_slew_fall_unit.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_2_slew_fall_unit.setFont(font10)
    self.ui.label_manual_control_eload_2_slew_fall_unit.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    
    self.ui.horizontalLayout_38_2.addWidget(self.ui.label_manual_control_eload_2_slew_fall_unit)
    
    
    self.gridLayout_29.addWidget(self.ui.frame_manual_control_eload_2_slew_fall, 1, 0, 1, 1)
    
    self.ui.frame_manual_control_eload_2_slew_rise = QFrame(self.ui.frame_manual_control_eload_2_slew)
    self.ui.frame_manual_control_eload_2_slew_rise.setObjectName(u"frame_manual_control_eload_slew_rise_2")
    self.ui.frame_manual_control_eload_2_slew_rise.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_slew_rise.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_36_2 = QHBoxLayout(self.ui.frame_manual_control_eload_2_slew_rise)
    self.ui.horizontalLayout_36_2.setObjectName(u"horizontalLayout_36_2")
    self.label_manual_control_electronic_load_rise = QLabel(self.ui.frame_manual_control_eload_2_slew_rise)
    self.label_manual_control_electronic_load_rise.setObjectName(u"label_manual_control_electronic_load_rise")
    self.label_manual_control_electronic_load_rise.setMaximumSize(QtCore.QSize(16777215, 30))
    self.label_manual_control_electronic_load_rise.setFont(font10)
    self.label_manual_control_electronic_load_rise.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.label_manual_control_electronic_load_rise.setAlignment(Qt.AlignCenter)
    
    self.ui.horizontalLayout_36_2.addWidget(self.label_manual_control_electronic_load_rise)
    
    self.lineedit_manual_control_eload_slew_rise = QLineEdit(self.ui.frame_manual_control_eload_2_slew_rise)
    self.lineedit_manual_control_eload_slew_rise.setObjectName(u"lineedit_manual_control_eload_slew_rise")
    sizePolicy21.setHeightForWidth(self.lineedit_manual_control_eload_slew_rise.sizePolicy().hasHeightForWidth())
    self.lineedit_manual_control_eload_slew_rise.setSizePolicy(sizePolicy21)
    self.lineedit_manual_control_eload_slew_rise.setMinimumSize(QtCore.QSize(0, 40))
    self.lineedit_manual_control_eload_slew_rise.setFont(font10)
    self.lineedit_manual_control_eload_slew_rise.setStyleSheet(u"QLineEdit {\n"
    "	background-color: rgb(27, 29, 35);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(27, 29, 35);\n"
    "	padding-left: 10px;\n"
    "}\n"
    "QLineEdit:hover {\n"
    "	border: 2px solid rgb(64, 71, 88);\n"
    "}\n"
    "QLineEdit:focus {\n"
    "	border: 2px solid rgb(91, 101, 124);\n"
    "}\n"
    "\n"
    "QLineEdit:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "	background-color: rgb(37, 39, 45);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(37, 39, 45);\n"
    "	padding-left: 10px;\n"
    "}")
    
    self.ui.horizontalLayout_36_2.addWidget(self.lineedit_manual_control_eload_slew_rise)
    
    self.ui.label_manual_control_eload_2_slew_rise_unit = QLabel(self.ui.frame_manual_control_eload_2_slew_rise)
    self.ui.label_manual_control_eload_2_slew_rise_unit.setObjectName(u"label_manual_control_eload_slew_rise_unit")
    sizePolicy11.setHeightForWidth(self.ui.label_manual_control_eload_2_slew_rise_unit.sizePolicy().hasHeightForWidth())
    self.ui.label_manual_control_eload_2_slew_rise_unit.setSizePolicy(sizePolicy11)
    self.ui.label_manual_control_eload_2_slew_rise_unit.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_2_slew_rise_unit.setFont(font10)
    self.ui.label_manual_control_eload_2_slew_rise_unit.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    
    self.ui.horizontalLayout_36_2.addWidget(self.ui.label_manual_control_eload_2_slew_rise_unit)
    
    
    self.gridLayout_29.addWidget(self.ui.frame_manual_control_eload_2_slew_rise, 0, 0, 1, 1)
    
    self.btn_manual_control_eload_set_slew = QPushButton(self.ui.frame_manual_control_eload_2_slew)
    self.btn_manual_control_eload_set_slew.setObjectName(u"btn_manual_control_eload_set_slew")
    sizePolicy19.setHeightForWidth(self.btn_manual_control_eload_set_slew.sizePolicy().hasHeightForWidth())
    self.btn_manual_control_eload_set_slew.setSizePolicy(sizePolicy19)
    self.btn_manual_control_eload_set_slew.setMinimumSize(QtCore.QSize(50, 60))
    self.btn_manual_control_eload_set_slew.setFont(font4)
    self.btn_manual_control_eload_set_slew.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    self.btn_manual_control_eload_set_slew.setCheckable(False)
    self.btn_manual_control_eload_set_slew.setChecked(False)
    
    self.gridLayout_29.addWidget(self.btn_manual_control_eload_set_slew, 0, 1, 2, 1)
    
    
    self.horizontalLayout_46.addWidget(self.ui.frame_manual_control_eload_2_slew)
    
    
    self.verticalLayout_77.addWidget(self.ui.frame_manual_control_eload_2_center)
    
    self.ui.frame_manual_control_eload_2_bottom = QFrame(self.ui.frame_manual_control_eload_2_contents)
    self.ui.frame_manual_control_eload_2_bottom.setObjectName(u"frame_manual_control_eload_bottom_2")
    self.ui.frame_manual_control_eload_2_bottom.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_bottom.setFrameShadow(QFrame.Raised)
    self.horizontalLayout_56 = QHBoxLayout(self.ui.frame_manual_control_eload_2_bottom)
    self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
    self.btn_manual_control_eload_turn_on = QPushButton(self.ui.frame_manual_control_eload_2_bottom)
    self.btn_manual_control_eload_turn_on.setObjectName(u"btn_manual_control_eload_turn_on")
    self.btn_manual_control_eload_turn_on.setMinimumSize(QtCore.QSize(120, 40))
    self.btn_manual_control_eload_turn_on.setFont(font13)
    self.btn_manual_control_eload_turn_on.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    self.btn_manual_control_eload_turn_on.setIcon(icon8)
    self.btn_manual_control_eload_turn_on.setCheckable(False)
    self.btn_manual_control_eload_turn_on.setChecked(False)
    
    self.horizontalLayout_56.addWidget(self.btn_manual_control_eload_turn_on)
    
    self.btn_manual_control_eload_turn_off = QPushButton(self.ui.frame_manual_control_eload_2_bottom)
    self.btn_manual_control_eload_turn_off.setObjectName(u"btn_manual_control_eload_turn_off")
    self.btn_manual_control_eload_turn_off.setMinimumSize(QtCore.QSize(120, 40))
    self.btn_manual_control_eload_turn_off.setFont(font13)
    self.btn_manual_control_eload_turn_off.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    self.btn_manual_control_eload_turn_off.setIcon(icon9)
    self.btn_manual_control_eload_turn_off.setCheckable(False)
    self.btn_manual_control_eload_turn_off.setChecked(False)
    
    self.horizontalLayout_56.addWidget(self.btn_manual_control_eload_turn_off)
    
    
    self.verticalLayout_77.addWidget(self.ui.frame_manual_control_eload_2_bottom)
    
    
    self.ui.verticalLayout_23_2.addWidget(self.ui.frame_manual_control_eload_2_contents)
    
    
    self.ui.horizontalLayout_13.addWidget(self.ui.frame_manual_control_eload_2)

    # PML 2
    self.ui.frame_manual_control_pml_2 = QFrame(self.ui.frame_manual_control_upper)
    self.ui.frame_manual_control_pml_2.setObjectName(u"frame_manual_control_pml_2")
    self.ui.frame_manual_control_pml_2.setEnabled(True)
    self.ui.frame_manual_control_pml_2.setMinimumSize(QtCore.QSize(300, 0))
    self.ui.frame_manual_control_pml_2.setStyleSheet(u"QFrame{\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "};")
    self.ui.frame_manual_control_pml_2.setFrameShape(QFrame.NoFrame)
    self.ui.frame_manual_control_pml_2.setFrameShadow(QFrame.Sunken)
    self.ui.verticalLayout_19_2 = QVBoxLayout(self.ui.frame_manual_control_pml_2)
    self.ui.verticalLayout_19_2.setObjectName(u"verticalLayout_19_2")
    self.label_load_power_meter = QLabel(self.ui.frame_manual_control_pml_2)
    self.label_load_power_meter.setObjectName(u"label_load_power_meter")
    self.label_load_power_meter.setMaximumSize(QtCore.QSize(16777215, 30))
    self.label_load_power_meter.setFont(font1)
    self.label_load_power_meter.setCursor(QCursor(Qt.ArrowCursor))
    self.label_load_power_meter.setStyleSheet(u"QLabel{border:none;}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.label_load_power_meter.setAlignment(Qt.AlignCenter)
    
    self.ui.verticalLayout_19_2.addWidget(self.label_load_power_meter)
    
    self.ui.frame_pml_contents_2 = QFrame(self.ui.frame_manual_control_pml_2)
    self.ui.frame_pml_contents_2.setObjectName(u"frame_pml_contents_2")
    self.ui.frame_pml_contents_2.setStyleSheet(u"border:none;")
    self.ui.frame_pml_contents_2.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_contents_2.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_15_2 = QHBoxLayout(self.ui.frame_pml_contents_2)
    self.ui.horizontalLayout_15_2.setObjectName(u"horizontalLayout_15_2")
    self.ui.frame_pml_display_2 = QFrame(self.ui.frame_pml_contents_2)
    self.ui.frame_pml_display_2.setObjectName(u"frame_pml_display_2")
    self.ui.frame_pml_display_2.setMinimumSize(QtCore.QSize(0, 280))
    self.ui.frame_pml_display_2.setMaximumSize(QtCore.QSize(300, 16777215))
    self.ui.frame_pml_display_2.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "QLabel{\n"
    "	font-family: \"Calibri\"\n"
    "}")
    self.ui.frame_pml_display_2.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_display_2.setFrameShadow(QFrame.Raised)
    self.ui.verticalLayout_20_2 = QVBoxLayout(self.ui.frame_pml_display_2)
    self.ui.verticalLayout_20_2.setSpacing(0)
    self.ui.verticalLayout_20_2.setObjectName(u"verticalLayout_20_2")
    self.ui.verticalLayout_20_2.setContentsMargins(0, 0, 0, 0)
    self.ui.label_pml_display_a_2 = QLabel(self.ui.frame_pml_display_2)
    self.ui.label_pml_display_a_2.setObjectName(u"label_pml_display_a_2")
    self.ui.label_pml_display_a_2.setMinimumSize(QtCore.QSize(0, 70))
    self.ui.label_pml_display_a_2.setMaximumSize(QtCore.QSize(16777215, 70))
    self.ui.label_pml_display_a_2.setFont(font12)
    self.ui.label_pml_display_a_2.setStyleSheet(u"color: rgb(255, 0, 0);\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "QLabel{\n"
    "	font-family: \"Calibri\"\n"
    "}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_pml_display_a_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
    
    self.ui.verticalLayout_20_2.addWidget(self.ui.label_pml_display_a_2)
    
    self.ui.label_pml_display_b_2 = QLabel(self.ui.frame_pml_display_2)
    self.ui.label_pml_display_b_2.setObjectName(u"label_pml_display_b_2")
    self.ui.label_pml_display_b_2.setMinimumSize(QtCore.QSize(0, 70))
    self.ui.label_pml_display_b_2.setMaximumSize(QtCore.QSize(16777215, 70))
    self.ui.label_pml_display_b_2.setFont(font12)
    self.ui.label_pml_display_b_2.setStyleSheet(u"color: rgb(255, 0, 0);\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "QLabel{\n"
    "	font-family: \"Calibri\"\n"
    "}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_pml_display_b_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
    
    self.ui.verticalLayout_20_2.addWidget(self.ui.label_pml_display_b_2)
    
    self.ui.label_pml_display_c_2 = QLabel(self.ui.frame_pml_display_2)
    self.ui.label_pml_display_c_2.setObjectName(u"label_pml_display_c_2")
    self.ui.label_pml_display_c_2.setMinimumSize(QtCore.QSize(0, 70))
    self.ui.label_pml_display_c_2.setMaximumSize(QtCore.QSize(16777215, 70))
    self.ui.label_pml_display_c_2.setFont(font12)
    self.ui.label_pml_display_c_2.setStyleSheet(u"color: rgb(255, 0, 0);\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "QLabel{\n"
    "	font-family: \"Calibri\"\n"
    "}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_pml_display_c_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
    
    self.ui.verticalLayout_20_2.addWidget(self.ui.label_pml_display_c_2)
    
    self.ui.label_pml_display_d_2 = QLabel(self.ui.frame_pml_display_2)
    self.ui.label_pml_display_d_2.setObjectName(u"label_pml_display_d_2")
    self.ui.label_pml_display_d_2.setMinimumSize(QtCore.QSize(0, 70))
    self.ui.label_pml_display_d_2.setMaximumSize(QtCore.QSize(16777215, 70))
    self.ui.label_pml_display_d_2.setFont(font12)
    self.ui.label_pml_display_d_2.setStyleSheet(u"color: rgb(255, 0, 0);\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "QLabel{\n"
    "	font-family: \"Calibri\"\n"
    "}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_pml_display_d_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
    
    self.ui.verticalLayout_20_2.addWidget(self.ui.label_pml_display_d_2)
    
    
    self.ui.horizontalLayout_15_2.addWidget(self.ui.frame_pml_display_2)
    
    self.ui.frame_pml_display_2_select = QFrame(self.ui.frame_pml_contents_2)
    self.ui.frame_pml_display_2_select.setObjectName(u"frame_pml_display_select_2")
    self.ui.frame_pml_display_2_select.setMaximumSize(QtCore.QSize(100, 16777215))
    self.ui.frame_pml_display_2_select.setStyleSheet(u"QFrame{\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "}")
    self.ui.frame_pml_display_2_select.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_display_2_select.setFrameShadow(QFrame.Raised)
    self.verticalLayout_21 = QVBoxLayout(self.ui.frame_pml_display_2_select)
    self.verticalLayout_21.setSpacing(0)
    self.verticalLayout_21.setObjectName(u"verticalLayout_21")
    self.verticalLayout_21.setContentsMargins(0, 0, 0, 0)
    self.cbx_pml_display_a = QComboBox(self.ui.frame_pml_display_2_select)
    self.cbx_pml_display_a.setObjectName(u"cbx_pml_display_a")
    self.cbx_pml_display_a.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.verticalLayout_21.addWidget(self.cbx_pml_display_a)
    
    self.cbx_pml_display_b = QComboBox(self.ui.frame_pml_display_2_select)
    self.cbx_pml_display_b.setObjectName(u"cbx_pml_display_b")
    self.cbx_pml_display_b.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.verticalLayout_21.addWidget(self.cbx_pml_display_b)
    
    self.cbx_pml_display_c = QComboBox(self.ui.frame_pml_display_2_select)
    self.cbx_pml_display_c.setObjectName(u"cbx_pml_display_c")
    self.cbx_pml_display_c.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.verticalLayout_21.addWidget(self.cbx_pml_display_c)
    
    self.cbx_pml_display_d = QComboBox(self.ui.frame_pml_display_2_select)
    self.cbx_pml_display_d.setObjectName(u"cbx_pml_display_d")
    self.cbx_pml_display_d.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.verticalLayout_21.addWidget(self.cbx_pml_display_d)
    
    
    self.ui.horizontalLayout_15_2.addWidget(self.ui.frame_pml_display_2_select)
    
    self.ui.frame_pml_control_2 = QFrame(self.ui.frame_pml_contents_2)
    self.ui.frame_pml_control_2.setObjectName(u"frame_pml_control_2")
    self.ui.frame_pml_control_2.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "")
    self.ui.frame_pml_control_2.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_2.setFrameShadow(QFrame.Raised)
    self.verticalLayout_29 = QVBoxLayout(self.ui.frame_pml_control_2)
    self.verticalLayout_29.setSpacing(0)
    self.verticalLayout_29.setObjectName(u"verticalLayout_29")
    self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
    self.ui.frame_pml_control_2__range = QFrame(self.ui.frame_pml_control_2)
    self.ui.frame_pml_control_2__range.setObjectName(u"frame_pml_control__range")
    self.ui.frame_pml_control_2__range.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_2__range.setFrameShadow(QFrame.Raised)
    self.formLayout_2 = QFormLayout(self.ui.frame_pml_control_2__range)
    self.formLayout_2.setObjectName(u"formLayout_2")
    self.label_pml_voltage_range = QLabel(self.ui.frame_pml_control_2__range)
    self.label_pml_voltage_range.setObjectName(u"label_pml_voltage_range")
    self.label_pml_voltage_range.setFont(font10)
    self.label_pml_voltage_range.setStyleSheet(u"border:none;")
    
    self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_pml_voltage_range)
    
    self.cbx_pml_voltage_range = QComboBox(self.ui.frame_pml_control_2__range)
    self.cbx_pml_voltage_range.addItem("")
    self.cbx_pml_voltage_range.addItem("")
    self.cbx_pml_voltage_range.setObjectName(u"cbx_pml_voltage_range")
    self.cbx_pml_voltage_range.setMaximumSize(QtCore.QSize(16777215, 54))
    self.cbx_pml_voltage_range.setFont(font10)
    
    self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.cbx_pml_voltage_range)
    
    self.label_pml_current_range = QLabel(self.ui.frame_pml_control_2__range)
    self.label_pml_current_range.setObjectName(u"label_pml_current_range")
    self.label_pml_current_range.setFont(font10)
    self.label_pml_current_range.setStyleSheet(u"border:none;")
    
    self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_pml_current_range)
    
    self.cbx_pml_current_range = QComboBox(self.ui.frame_pml_control_2__range)
    self.cbx_pml_current_range.addItem("")
    self.cbx_pml_current_range.addItem("")
    self.cbx_pml_current_range.setObjectName(u"cbx_pml_current_range")
    self.cbx_pml_current_range.setMaximumSize(QtCore.QSize(16777215, 54))
    self.cbx_pml_current_range.setFont(font10)
    
    self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.cbx_pml_current_range)
    
    
    self.verticalLayout_29.addWidget(self.ui.frame_pml_control_2__range)
    
    self.ui.frame_pml_control_2_lower = QFrame(self.ui.frame_pml_control_2)
    self.ui.frame_pml_control_2_lower.setObjectName(u"frame_pml_control_lower")
    self.ui.frame_pml_control_2_lower.setStyleSheet(u"border:none;")
    self.ui.frame_pml_control_2_lower.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_2_lower.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_19_2 = QHBoxLayout(self.ui.frame_pml_control_2_lower)
    self.ui.horizontalLayout_19_2.setSpacing(0)
    self.ui.horizontalLayout_19_2.setObjectName(u"horizontalLayout_19_2")
    self.ui.horizontalLayout_19_2.setContentsMargins(0, 0, 0, 0)
    self.frame_pml_integration = QFrame(self.ui.frame_pml_control_2_lower)
    self.frame_pml_integration.setObjectName(u"frame_pml_integration")
    self.frame_pml_integration.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.frame_pml_integration.setFrameShape(QFrame.StyledPanel)
    self.frame_pml_integration.setFrameShadow(QFrame.Raised)
    self.verticalLayout_30 = QVBoxLayout(self.frame_pml_integration)
    self.verticalLayout_30.setObjectName(u"verticalLayout_30")
    self.label_pml_integration = QLabel(self.frame_pml_integration)
    self.label_pml_integration.setObjectName(u"label_pml_integration")
    sizePolicy.setHeightForWidth(self.label_pml_integration.sizePolicy().hasHeightForWidth())
    self.label_pml_integration.setSizePolicy(sizePolicy)
    self.label_pml_integration.setMinimumSize(QtCore.QSize(0, 20))
    self.label_pml_integration.setMaximumSize(QtCore.QSize(16777215, 20))
    self.label_pml_integration.setFont(font10)
    self.label_pml_integration.setStyleSheet(u"border:none;")
    
    self.verticalLayout_30.addWidget(self.label_pml_integration)
    
    self.btn_pml_integration_start = QPushButton(self.frame_pml_integration)
    self.btn_pml_integration_start.setObjectName(u"btn_pml_integration_start")
    self.btn_pml_integration_start.setFont(font10)
    self.btn_pml_integration_start.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}")
    
    self.verticalLayout_30.addWidget(self.btn_pml_integration_start)
    
    self.btn_pml_integration_stop = QPushButton(self.frame_pml_integration)
    self.btn_pml_integration_stop.setObjectName(u"btn_pml_integration_stop")
    self.btn_pml_integration_stop.setFont(font10)
    self.btn_pml_integration_stop.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}")
    
    self.verticalLayout_30.addWidget(self.btn_pml_integration_stop)
    
    self.btn_pml_integration_reset = QPushButton(self.frame_pml_integration)
    self.btn_pml_integration_reset.setObjectName(u"btn_pml_integration_reset")
    self.btn_pml_integration_reset.setFont(font10)
    self.btn_pml_integration_reset.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}")
    
    self.verticalLayout_30.addWidget(self.btn_pml_integration_reset)
    
    
    self.ui.horizontalLayout_19_2.addWidget(self.frame_pml_integration)
    
    self.frame_pml_averaging = QFrame(self.ui.frame_pml_control_2_lower)
    self.frame_pml_averaging.setObjectName(u"frame_pml_averaging")
    self.frame_pml_averaging.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.frame_pml_averaging.setFrameShape(QFrame.StyledPanel)
    self.frame_pml_averaging.setFrameShadow(QFrame.Raised)
    self.verticalLayout_31 = QVBoxLayout(self.frame_pml_averaging)
    self.verticalLayout_31.setSpacing(2)
    self.verticalLayout_31.setObjectName(u"verticalLayout_31")
    self.verticalLayout_31.setContentsMargins(-1, 5, -1, 5)
    self.label_pml_averaging = QLabel(self.frame_pml_averaging)
    self.label_pml_averaging.setObjectName(u"label_pml_averaging")
    sizePolicy.setHeightForWidth(self.label_pml_averaging.sizePolicy().hasHeightForWidth())
    self.label_pml_averaging.setSizePolicy(sizePolicy)
    self.label_pml_averaging.setMinimumSize(QtCore.QSize(0, 20))
    self.label_pml_averaging.setMaximumSize(QtCore.QSize(16777215, 20))
    self.label_pml_averaging.setFont(font10)
    self.label_pml_averaging.setStyleSheet(u"border:none;")
    
    self.verticalLayout_31.addWidget(self.label_pml_averaging)
    
    self.btn_pml_averaging_toggle = QPushButton(self.frame_pml_averaging)
    self.btn_pml_averaging_toggle.setObjectName(u"btn_pml_averaging_toggle")
    self.btn_pml_averaging_toggle.setFont(font10)
    self.btn_pml_averaging_toggle.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}")
    
    self.verticalLayout_31.addWidget(self.btn_pml_averaging_toggle)
    
    self.cbx_pml_averaging_count = QComboBox(self.frame_pml_averaging)
    self.cbx_pml_averaging_count.addItem("")
    self.cbx_pml_averaging_count.addItem("")
    self.cbx_pml_averaging_count.addItem("")
    self.cbx_pml_averaging_count.setObjectName(u"cbx_pml_averaging_count")
    self.cbx_pml_averaging_count.setMaximumSize(QtCore.QSize(16777215, 40))
    self.cbx_pml_averaging_count.setFont(font10)
    
    self.verticalLayout_31.addWidget(self.cbx_pml_averaging_count)
    
    self.cbx_pml_averaging_mode = QComboBox(self.frame_pml_averaging)
    self.cbx_pml_averaging_mode.addItem("")
    self.cbx_pml_averaging_mode.addItem("")
    self.cbx_pml_averaging_mode.setObjectName(u"cbx_pml_averaging_mode")
    self.cbx_pml_averaging_mode.setMaximumSize(QtCore.QSize(16777215, 40))
    self.cbx_pml_averaging_mode.setFont(font10)
    
    self.verticalLayout_31.addWidget(self.cbx_pml_averaging_mode)
    
    
    self.ui.horizontalLayout_19_2.addWidget(self.frame_pml_averaging)
    
    self.frame_pml_measure_mode = QFrame(self.ui.frame_pml_control_2_lower)
    self.frame_pml_measure_mode.setObjectName(u"frame_pml_measure_mode")
    self.frame_pml_measure_mode.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.frame_pml_measure_mode.setFrameShape(QFrame.StyledPanel)
    self.frame_pml_measure_mode.setFrameShadow(QFrame.Raised)
    self.verticalLayout_32 = QVBoxLayout(self.frame_pml_measure_mode)
    self.verticalLayout_32.setSpacing(13)
    self.verticalLayout_32.setObjectName(u"verticalLayout_32")
    self.verticalLayout_32.setContentsMargins(13, 13, 13, 13)
    self.label_pml_measure_mode = QLabel(self.frame_pml_measure_mode)
    self.label_pml_measure_mode.setObjectName(u"label_pml_measure_mode")
    sizePolicy.setHeightForWidth(self.label_pml_measure_mode.sizePolicy().hasHeightForWidth())
    self.label_pml_measure_mode.setSizePolicy(sizePolicy)
    self.label_pml_measure_mode.setMaximumSize(QtCore.QSize(16777215, 20))
    self.label_pml_measure_mode.setFont(font10)
    self.label_pml_measure_mode.setStyleSheet(u"border:none;")
    
    self.verticalLayout_32.addWidget(self.label_pml_measure_mode)
    
    self.btn_pml_measure_mode = QPushButton(self.frame_pml_measure_mode)
    self.btn_pml_measure_mode.setObjectName(u"btn_pml_measure_mode")
    self.btn_pml_measure_mode.setFont(font10)
    self.btn_pml_measure_mode.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}")
    
    self.verticalLayout_32.addWidget(self.btn_pml_measure_mode)
    
    
    self.ui.horizontalLayout_19_2.addWidget(self.frame_pml_measure_mode)
    
    
    self.verticalLayout_29.addWidget(self.ui.frame_pml_control_2_lower)
    
    
    self.ui.horizontalLayout_15_2.addWidget(self.ui.frame_pml_control_2)
    
    
    self.ui.verticalLayout_19_2.addWidget(self.ui.frame_pml_contents_2)
    
    
    self.ui.horizontalLayout_9.addWidget(self.ui.frame_manual_control_pml_2)

    # ELOAD 3
    self.ui.frame_manual_control_eload_3 = QFrame(self.ui.frame_manual_control_lower)
    self.ui.frame_manual_control_eload_3.setObjectName(u"frame_manual_control_eload_3")
    sizePolicy20 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
    sizePolicy20.setHorizontalStretch(3)
    sizePolicy20.setVerticalStretch(0)
    sizePolicy20.setHeightForWidth(self.ui.frame_manual_control_eload_3.sizePolicy().hasHeightForWidth())
    self.ui.frame_manual_control_eload_3.setSizePolicy(sizePolicy20)
    self.ui.frame_manual_control_eload_3.setMinimumSize(QtCore.QSize(400, 0))
    self.ui.frame_manual_control_eload_3.setStyleSheet(u"QFrame{\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "}")
    self.ui.frame_manual_control_eload_3.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3.setFrameShadow(QFrame.Raised)
    self.ui.verticalLayout_23_3 = QVBoxLayout(self.ui.frame_manual_control_eload_3)
    self.ui.verticalLayout_23_3.setObjectName(u"verticalLayout_23_3")
    self.ui.label_manual_control_eload_3 = QLabel(self.ui.frame_manual_control_eload_3)
    self.ui.label_manual_control_eload_3.setObjectName(u"label_manual_control_eload_3")
    self.ui.label_manual_control_eload_3.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_3.setFont(font1)
    self.ui.label_manual_control_eload_3.setCursor(QCursor(Qt.UpArrowCursor))
    self.ui.label_manual_control_eload_3.setStyleSheet(u"QLabel{border:none;}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_manual_control_eload_3.setAlignment(Qt.AlignCenter)
    
    self.ui.verticalLayout_23_3.addWidget(self.ui.label_manual_control_eload_3)
    
    self.ui.frame_manual_control_eload_3_contents = QFrame(self.ui.frame_manual_control_eload_3)
    self.ui.frame_manual_control_eload_3_contents.setObjectName(u"frame_manual_control_eload_contents_3")
    self.ui.frame_manual_control_eload_3_contents.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_3_contents.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_contents.setFrameShadow(QFrame.Raised)
    self.verticalLayout_77 = QVBoxLayout(self.ui.frame_manual_control_eload_3_contents)
    self.verticalLayout_77.setObjectName(u"verticalLayout_77")
    self.ui.frame_manual_control_eload_3_top = QFrame(self.ui.frame_manual_control_eload_3_contents)
    self.ui.frame_manual_control_eload_3_top.setObjectName(u"frame_manual_control_eload_top_3")
    self.ui.frame_manual_control_eload_3_top.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_top.setFrameShadow(QFrame.Raised)
    self.horizontalLayout_47 = QHBoxLayout(self.ui.frame_manual_control_eload_3_top)
    self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
    self.cbx_manual_control_eload_type = QComboBox(self.ui.frame_manual_control_eload_3_top)
    self.cbx_manual_control_eload_type.addItem("")
    self.cbx_manual_control_eload_type.addItem("")
    self.cbx_manual_control_eload_type.addItem("")
    self.cbx_manual_control_eload_type.setObjectName(u"cbx_manual_control_eload_type")
    self.cbx_manual_control_eload_type.setMaximumSize(QtCore.QSize(16777215, 40))
    self.cbx_manual_control_eload_type.setFont(font10)
    self.cbx_manual_control_eload_type.setStyleSheet(u"QComboBox{\n"
    "border: 2px solid black;\n"
    "border-radius:5px;\n"
    "}\n"
    "\n"
    "QComboBox:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    
    self.horizontalLayout_47.addWidget(self.cbx_manual_control_eload_type)
    
    self.ui.btn_manual_control_eload_a_b_swap_3 = QPushButton(self.ui.frame_manual_control_eload_3_top)
    self.ui.btn_manual_control_eload_a_b_swap_3.setObjectName(u"btn_manual_control_eload_a_b_swap_3")
    self.ui.btn_manual_control_eload_a_b_swap_3.setMinimumSize(QtCore.QSize(120, 40))
    self.ui.btn_manual_control_eload_a_b_swap_3.setFont(font13)
    self.ui.btn_manual_control_eload_a_b_swap_3.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    icon10 = QIcon()
    icon10.addFile(u":/20x20/icons/20x20/cil-swap-horizontal.png", QtCore.QSize(), QIcon.Normal, QIcon.Off)
    self.ui.btn_manual_control_eload_a_b_swap_3.setIcon(icon10)
    self.ui.btn_manual_control_eload_a_b_swap_3.setCheckable(False)
    self.ui.btn_manual_control_eload_a_b_swap_3.setChecked(False)
    
    self.horizontalLayout_47.addWidget(self.ui.btn_manual_control_eload_a_b_swap_3)
    
    
    self.verticalLayout_77.addWidget(self.ui.frame_manual_control_eload_3_top)
    
    self.ui.frame_manual_control_eload_3_center = QFrame(self.ui.frame_manual_control_eload_3_contents)
    self.ui.frame_manual_control_eload_3_center.setObjectName(u"frame_manual_control_eload_center_3")
    self.ui.frame_manual_control_eload_3_center.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_center.setFrameShadow(QFrame.Raised)
    self.horizontalLayout_46 = QHBoxLayout(self.ui.frame_manual_control_eload_3_center)
    self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
    self.ui.frame_manual_control_eload_3_level = QFrame(self.ui.frame_manual_control_eload_3_center)
    self.ui.frame_manual_control_eload_3_level.setObjectName(u"frame_manual_control_eload_level_3")
    self.ui.frame_manual_control_eload_3_level.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_level.setFrameShadow(QFrame.Raised)
    self.verticalLayout_70 = QVBoxLayout(self.ui.frame_manual_control_eload_3_level)
    self.verticalLayout_70.setObjectName(u"verticalLayout_70")
    self.ui.frame_manual_control_eload_3_a = QFrame(self.ui.frame_manual_control_eload_3_level)
    self.ui.frame_manual_control_eload_3_a.setObjectName(u"frame_manual_control_eload_a_3")
    self.ui.frame_manual_control_eload_3_a.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_a.setFrameShadow(QFrame.Raised)
    self.horizontalLayout_45 = QHBoxLayout(self.ui.frame_manual_control_eload_3_a)
    self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
    self.ui.label_manual_control_eload_3_a = QLabel(self.ui.frame_manual_control_eload_3_a)
    self.ui.label_manual_control_eload_3_a.setObjectName(u"label_manual_control_eload_a_3")
    self.ui.label_manual_control_eload_3_a.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_3_a.setFont(font10)
    self.ui.label_manual_control_eload_3_a.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.ui.label_manual_control_eload_3_a.setAlignment(Qt.AlignCenter)
    
    self.horizontalLayout_45.addWidget(self.ui.label_manual_control_eload_3_a)
    
    self.ui.lineedit_manual_control_eload_a_level_3 = QLineEdit(self.ui.frame_manual_control_eload_3_a)
    self.ui.lineedit_manual_control_eload_a_level_3.setObjectName(u"lineedit_manual_control_eload_a_level_3")
    sizePolicy21 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    sizePolicy21.setHorizontalStretch(4)
    sizePolicy21.setVerticalStretch(0)
    sizePolicy21.setHeightForWidth(self.ui.lineedit_manual_control_eload_a_level_3.sizePolicy().hasHeightForWidth())
    self.ui.lineedit_manual_control_eload_a_level_3.setSizePolicy(sizePolicy21)
    self.ui.lineedit_manual_control_eload_a_level_3.setMinimumSize(QtCore.QSize(0, 40))
    self.ui.lineedit_manual_control_eload_a_level_3.setFont(font10)
    self.ui.lineedit_manual_control_eload_a_level_3.setStyleSheet(u"QLineEdit {\n"
    "	background-color: rgb(27, 29, 35);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(27, 29, 35);\n"
    "	padding-left: 10px;\n"
    "}\n"
    "QLineEdit:hover {\n"
    "	border: 2px solid rgb(64, 71, 88);\n"
    "}\n"
    "QLineEdit:focus {\n"
    "	border: 2px solid rgb(91, 101, 124);\n"
    "}\n"
    "\n"
    "QLineEdit:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "	background-color: rgb(37, 39, 45);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(37, 39, 45);\n"
    "	padding-left: 10px;\n"
    "}")
    
    self.horizontalLayout_45.addWidget(self.ui.lineedit_manual_control_eload_a_level_3)
    
    self.ui.label_manual_control_eload_3_a_level_unit = QLabel(self.ui.frame_manual_control_eload_3_a)
    self.ui.label_manual_control_eload_3_a_level_unit.setObjectName(u"label_manual_control_eload_a_level_unit")
    sizePolicy11.setHeightForWidth(self.ui.label_manual_control_eload_3_a_level_unit.sizePolicy().hasHeightForWidth())
    self.ui.label_manual_control_eload_3_a_level_unit.setSizePolicy(sizePolicy11)
    self.ui.label_manual_control_eload_3_a_level_unit.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_3_a_level_unit.setFont(font10)
    self.ui.label_manual_control_eload_3_a_level_unit.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    
    self.horizontalLayout_45.addWidget(self.ui.label_manual_control_eload_3_a_level_unit)
    
    self.btn_manual_control_eload_set_A = QPushButton(self.ui.frame_manual_control_eload_3_a)
    self.btn_manual_control_eload_set_A.setObjectName(u"btn_manual_control_eload_set_A")
    self.btn_manual_control_eload_set_A.setMinimumSize(QtCore.QSize(50, 30))
    self.btn_manual_control_eload_set_A.setFont(font4)
    self.btn_manual_control_eload_set_A.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    self.btn_manual_control_eload_set_A.setCheckable(False)
    self.btn_manual_control_eload_set_A.setChecked(False)
    
    self.horizontalLayout_45.addWidget(self.btn_manual_control_eload_set_A)
    
    
    self.verticalLayout_70.addWidget(self.ui.frame_manual_control_eload_3_a)
    
    self.ui.frame_manual_control_eload_3_b = QFrame(self.ui.frame_manual_control_eload_3_level)
    self.ui.frame_manual_control_eload_3_b.setObjectName(u"frame_manual_control_eload_b_3")
    self.ui.frame_manual_control_eload_3_b.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_b.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_39_3 = QHBoxLayout(self.ui.frame_manual_control_eload_3_b)
    self.ui.horizontalLayout_39_3.setObjectName(u"horizontalLayout_39_3")
    self.ui.label_manual_control_eload_3_b = QLabel(self.ui.frame_manual_control_eload_3_b)
    self.ui.label_manual_control_eload_3_b.setObjectName(u"label_manual_control_eload_b_3")
    self.ui.label_manual_control_eload_3_b.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_3_b.setFont(font10)
    self.ui.label_manual_control_eload_3_b.setLayoutDirection(Qt.LeftToRight)
    self.ui.label_manual_control_eload_3_b.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.ui.label_manual_control_eload_3_b.setAlignment(Qt.AlignCenter)
    
    self.ui.horizontalLayout_39_3.addWidget(self.ui.label_manual_control_eload_3_b)
    
    self.ui.lineedit_manual_control_eload_b_level_3 = QLineEdit(self.ui.frame_manual_control_eload_3_b)
    self.ui.lineedit_manual_control_eload_b_level_3.setObjectName(u"lineedit_manual_control_eload_b_level_3")
    sizePolicy21.setHeightForWidth(self.ui.lineedit_manual_control_eload_b_level_3.sizePolicy().hasHeightForWidth())
    self.ui.lineedit_manual_control_eload_b_level_3.setSizePolicy(sizePolicy21)
    self.ui.lineedit_manual_control_eload_b_level_3.setMinimumSize(QtCore.QSize(0, 40))
    self.ui.lineedit_manual_control_eload_b_level_3.setFont(font10)
    self.ui.lineedit_manual_control_eload_b_level_3.setStyleSheet(u"QLineEdit {\n"
    "	background-color: rgb(27, 29, 35);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(27, 29, 35);\n"
    "	padding-left: 10px;\n"
    "}\n"
    "QLineEdit:hover {\n"
    "	border: 2px solid rgb(64, 71, 88);\n"
    "}\n"
    "QLineEdit:focus {\n"
    "	border: 2px solid rgb(91, 101, 124);\n"
    "}\n"
    "\n"
    "QLineEdit:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "	background-color: rgb(37, 39, 45);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(37, 39, 45);\n"
    "	padding-left: 10px;\n"
    "}")
    
    self.ui.horizontalLayout_39_3.addWidget(self.ui.lineedit_manual_control_eload_b_level_3)
    
    self.ui.label_manual_control_eload_3_b_level_unit = QLabel(self.ui.frame_manual_control_eload_3_b)
    self.ui.label_manual_control_eload_3_b_level_unit.setObjectName(u"label_manual_control_eload_b_level_unit")
    sizePolicy11.setHeightForWidth(self.ui.label_manual_control_eload_3_b_level_unit.sizePolicy().hasHeightForWidth())
    self.ui.label_manual_control_eload_3_b_level_unit.setSizePolicy(sizePolicy11)
    self.ui.label_manual_control_eload_3_b_level_unit.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_3_b_level_unit.setFont(font10)
    self.ui.label_manual_control_eload_3_b_level_unit.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    
    self.ui.horizontalLayout_39_3.addWidget(self.ui.label_manual_control_eload_3_b_level_unit)
    
    self.btn_manual_control_eload_set_B = QPushButton(self.ui.frame_manual_control_eload_3_b)
    self.btn_manual_control_eload_set_B.setObjectName(u"btn_manual_control_eload_set_B")
    self.btn_manual_control_eload_set_B.setMinimumSize(QtCore.QSize(50, 30))
    self.btn_manual_control_eload_set_B.setFont(font4)
    self.btn_manual_control_eload_set_B.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    self.btn_manual_control_eload_set_B.setCheckable(False)
    self.btn_manual_control_eload_set_B.setChecked(False)
    
    self.ui.horizontalLayout_39_3.addWidget(self.btn_manual_control_eload_set_B)
    
    
    self.verticalLayout_70.addWidget(self.ui.frame_manual_control_eload_3_b)
    
    
    self.horizontalLayout_46.addWidget(self.ui.frame_manual_control_eload_3_level)
    
    self.ui.frame_manual_control_eload_3_slew = QFrame(self.ui.frame_manual_control_eload_3_center)
    self.ui.frame_manual_control_eload_3_slew.setObjectName(u"frame_manual_control_eload_slew_3")
    self.ui.frame_manual_control_eload_3_slew.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_slew.setFrameShadow(QFrame.Raised)
    self.gridLayout_29 = QGridLayout(self.ui.frame_manual_control_eload_3_slew)
    self.gridLayout_29.setObjectName(u"gridLayout_29")
    self.ui.frame_manual_control_eload_3_slew_fall = QFrame(self.ui.frame_manual_control_eload_3_slew)
    self.ui.frame_manual_control_eload_3_slew_fall.setObjectName(u"frame_manual_control_eload_slew_fall_3")
    self.ui.frame_manual_control_eload_3_slew_fall.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_slew_fall.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_38_3 = QHBoxLayout(self.ui.frame_manual_control_eload_3_slew_fall)
    self.ui.horizontalLayout_38_3.setObjectName(u"horizontalLayout_38_3")
    self.label_manual_control_electronic_load_fall = QLabel(self.ui.frame_manual_control_eload_3_slew_fall)
    self.label_manual_control_electronic_load_fall.setObjectName(u"label_manual_control_electronic_load_fall")
    self.label_manual_control_electronic_load_fall.setMaximumSize(QtCore.QSize(16777215, 30))
    self.label_manual_control_electronic_load_fall.setFont(font10)
    self.label_manual_control_electronic_load_fall.setLayoutDirection(Qt.LeftToRight)
    self.label_manual_control_electronic_load_fall.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.label_manual_control_electronic_load_fall.setAlignment(Qt.AlignCenter)
    
    self.ui.horizontalLayout_38_3.addWidget(self.label_manual_control_electronic_load_fall)
    
    self.lineedit_manual_control_eload_slew_fall = QLineEdit(self.ui.frame_manual_control_eload_3_slew_fall)
    self.lineedit_manual_control_eload_slew_fall.setObjectName(u"lineedit_manual_control_eload_slew_fall")
    sizePolicy21.setHeightForWidth(self.lineedit_manual_control_eload_slew_fall.sizePolicy().hasHeightForWidth())
    self.lineedit_manual_control_eload_slew_fall.setSizePolicy(sizePolicy21)
    self.lineedit_manual_control_eload_slew_fall.setMinimumSize(QtCore.QSize(0, 40))
    self.lineedit_manual_control_eload_slew_fall.setFont(font10)
    self.lineedit_manual_control_eload_slew_fall.setStyleSheet(u"QLineEdit {\n"
    "	background-color: rgb(27, 29, 35);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(27, 29, 35);\n"
    "	padding-left: 10px;\n"
    "}\n"
    "QLineEdit:hover {\n"
    "	border: 2px solid rgb(64, 71, 88);\n"
    "}\n"
    "QLineEdit:focus {\n"
    "	border: 2px solid rgb(91, 101, 124);\n"
    "}\n"
    "\n"
    "QLineEdit:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "	background-color: rgb(37, 39, 45);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(37, 39, 45);\n"
    "	padding-left: 10px;\n"
    "}")
    
    self.ui.horizontalLayout_38_3.addWidget(self.lineedit_manual_control_eload_slew_fall)
    
    self.ui.label_manual_control_eload_3_slew_fall_unit = QLabel(self.ui.frame_manual_control_eload_3_slew_fall)
    self.ui.label_manual_control_eload_3_slew_fall_unit.setObjectName(u"label_manual_control_eload_slew_fall_unit")
    sizePolicy11.setHeightForWidth(self.ui.label_manual_control_eload_3_slew_fall_unit.sizePolicy().hasHeightForWidth())
    self.ui.label_manual_control_eload_3_slew_fall_unit.setSizePolicy(sizePolicy11)
    self.ui.label_manual_control_eload_3_slew_fall_unit.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_3_slew_fall_unit.setFont(font10)
    self.ui.label_manual_control_eload_3_slew_fall_unit.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    
    self.ui.horizontalLayout_38_3.addWidget(self.ui.label_manual_control_eload_3_slew_fall_unit)
    
    
    self.gridLayout_29.addWidget(self.ui.frame_manual_control_eload_3_slew_fall, 1, 0, 1, 1)
    
    self.ui.frame_manual_control_eload_3_slew_rise = QFrame(self.ui.frame_manual_control_eload_3_slew)
    self.ui.frame_manual_control_eload_3_slew_rise.setObjectName(u"frame_manual_control_eload_slew_rise_3")
    self.ui.frame_manual_control_eload_3_slew_rise.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_slew_rise.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_36_3 = QHBoxLayout(self.ui.frame_manual_control_eload_3_slew_rise)
    self.ui.horizontalLayout_36_3.setObjectName(u"horizontalLayout_36_3")
    self.label_manual_control_electronic_load_rise = QLabel(self.ui.frame_manual_control_eload_3_slew_rise)
    self.label_manual_control_electronic_load_rise.setObjectName(u"label_manual_control_electronic_load_rise")
    self.label_manual_control_electronic_load_rise.setMaximumSize(QtCore.QSize(16777215, 30))
    self.label_manual_control_electronic_load_rise.setFont(font10)
    self.label_manual_control_electronic_load_rise.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.label_manual_control_electronic_load_rise.setAlignment(Qt.AlignCenter)
    
    self.ui.horizontalLayout_36_3.addWidget(self.label_manual_control_electronic_load_rise)
    
    self.lineedit_manual_control_eload_slew_rise = QLineEdit(self.ui.frame_manual_control_eload_3_slew_rise)
    self.lineedit_manual_control_eload_slew_rise.setObjectName(u"lineedit_manual_control_eload_slew_rise")
    sizePolicy21.setHeightForWidth(self.lineedit_manual_control_eload_slew_rise.sizePolicy().hasHeightForWidth())
    self.lineedit_manual_control_eload_slew_rise.setSizePolicy(sizePolicy21)
    self.lineedit_manual_control_eload_slew_rise.setMinimumSize(QtCore.QSize(0, 40))
    self.lineedit_manual_control_eload_slew_rise.setFont(font10)
    self.lineedit_manual_control_eload_slew_rise.setStyleSheet(u"QLineEdit {\n"
    "	background-color: rgb(27, 29, 35);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(27, 29, 35);\n"
    "	padding-left: 10px;\n"
    "}\n"
    "QLineEdit:hover {\n"
    "	border: 2px solid rgb(64, 71, 88);\n"
    "}\n"
    "QLineEdit:focus {\n"
    "	border: 2px solid rgb(91, 101, 124);\n"
    "}\n"
    "\n"
    "QLineEdit:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "	background-color: rgb(37, 39, 45);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(37, 39, 45);\n"
    "	padding-left: 10px;\n"
    "}")
    
    self.ui.horizontalLayout_36_3.addWidget(self.lineedit_manual_control_eload_slew_rise)
    
    self.ui.label_manual_control_eload_3_slew_rise_unit = QLabel(self.ui.frame_manual_control_eload_3_slew_rise)
    self.ui.label_manual_control_eload_3_slew_rise_unit.setObjectName(u"label_manual_control_eload_slew_rise_unit")
    sizePolicy11.setHeightForWidth(self.ui.label_manual_control_eload_3_slew_rise_unit.sizePolicy().hasHeightForWidth())
    self.ui.label_manual_control_eload_3_slew_rise_unit.setSizePolicy(sizePolicy11)
    self.ui.label_manual_control_eload_3_slew_rise_unit.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_3_slew_rise_unit.setFont(font10)
    self.ui.label_manual_control_eload_3_slew_rise_unit.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    
    self.ui.horizontalLayout_36_3.addWidget(self.ui.label_manual_control_eload_3_slew_rise_unit)
    
    
    self.gridLayout_29.addWidget(self.ui.frame_manual_control_eload_3_slew_rise, 0, 0, 1, 1)
    
    self.btn_manual_control_eload_set_slew = QPushButton(self.ui.frame_manual_control_eload_3_slew)
    self.btn_manual_control_eload_set_slew.setObjectName(u"btn_manual_control_eload_set_slew")
    sizePolicy19.setHeightForWidth(self.btn_manual_control_eload_set_slew.sizePolicy().hasHeightForWidth())
    self.btn_manual_control_eload_set_slew.setSizePolicy(sizePolicy19)
    self.btn_manual_control_eload_set_slew.setMinimumSize(QtCore.QSize(50, 60))
    self.btn_manual_control_eload_set_slew.setFont(font4)
    self.btn_manual_control_eload_set_slew.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    self.btn_manual_control_eload_set_slew.setCheckable(False)
    self.btn_manual_control_eload_set_slew.setChecked(False)
    
    self.gridLayout_29.addWidget(self.btn_manual_control_eload_set_slew, 0, 1, 2, 1)
    
    
    self.horizontalLayout_46.addWidget(self.ui.frame_manual_control_eload_3_slew)
    
    
    self.verticalLayout_77.addWidget(self.ui.frame_manual_control_eload_3_center)
    
    self.ui.frame_manual_control_eload_3_bottom = QFrame(self.ui.frame_manual_control_eload_3_contents)
    self.ui.frame_manual_control_eload_3_bottom.setObjectName(u"frame_manual_control_eload_bottom_3")
    self.ui.frame_manual_control_eload_3_bottom.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_bottom.setFrameShadow(QFrame.Raised)
    self.horizontalLayout_56 = QHBoxLayout(self.ui.frame_manual_control_eload_3_bottom)
    self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
    self.btn_manual_control_eload_turn_on = QPushButton(self.ui.frame_manual_control_eload_3_bottom)
    self.btn_manual_control_eload_turn_on.setObjectName(u"btn_manual_control_eload_turn_on")
    self.btn_manual_control_eload_turn_on.setMinimumSize(QtCore.QSize(120, 40))
    self.btn_manual_control_eload_turn_on.setFont(font13)
    self.btn_manual_control_eload_turn_on.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    self.btn_manual_control_eload_turn_on.setIcon(icon8)
    self.btn_manual_control_eload_turn_on.setCheckable(False)
    self.btn_manual_control_eload_turn_on.setChecked(False)
    
    self.horizontalLayout_56.addWidget(self.btn_manual_control_eload_turn_on)
    
    self.btn_manual_control_eload_turn_off = QPushButton(self.ui.frame_manual_control_eload_3_bottom)
    self.btn_manual_control_eload_turn_off.setObjectName(u"btn_manual_control_eload_turn_off")
    self.btn_manual_control_eload_turn_off.setMinimumSize(QtCore.QSize(120, 40))
    self.btn_manual_control_eload_turn_off.setFont(font13)
    self.btn_manual_control_eload_turn_off.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    self.btn_manual_control_eload_turn_off.setIcon(icon9)
    self.btn_manual_control_eload_turn_off.setCheckable(False)
    self.btn_manual_control_eload_turn_off.setChecked(False)
    
    self.horizontalLayout_56.addWidget(self.btn_manual_control_eload_turn_off)
    
    
    self.verticalLayout_77.addWidget(self.ui.frame_manual_control_eload_3_bottom)
    
    
    self.ui.verticalLayout_23_3.addWidget(self.ui.frame_manual_control_eload_3_contents)
    
    
    self.ui.horizontalLayout_13.addWidget(self.ui.frame_manual_control_eload_3)

    # PML 3
    self.ui.frame_manual_control_pml_3 = QFrame(self.ui.frame_manual_control_upper)
    self.ui.frame_manual_control_pml_3.setObjectName(u"frame_manual_control_pml_3")
    self.ui.frame_manual_control_pml_3.setEnabled(True)
    self.ui.frame_manual_control_pml_3.setMinimumSize(QtCore.QSize(300, 0))
    self.ui.frame_manual_control_pml_3.setStyleSheet(u"QFrame{\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "};")
    self.ui.frame_manual_control_pml_3.setFrameShape(QFrame.NoFrame)
    self.ui.frame_manual_control_pml_3.setFrameShadow(QFrame.Sunken)
    self.ui.verticalLayout_19_3 = QVBoxLayout(self.ui.frame_manual_control_pml_3)
    self.ui.verticalLayout_19_3.setObjectName(u"verticalLayout_19_3")
    self.label_load_power_meter = QLabel(self.ui.frame_manual_control_pml_3)
    self.label_load_power_meter.setObjectName(u"label_load_power_meter")
    self.label_load_power_meter.setMaximumSize(QtCore.QSize(16777215, 30))
    self.label_load_power_meter.setFont(font1)
    self.label_load_power_meter.setCursor(QCursor(Qt.ArrowCursor))
    self.label_load_power_meter.setStyleSheet(u"QLabel{border:none;}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.label_load_power_meter.setAlignment(Qt.AlignCenter)
    
    self.ui.verticalLayout_19_3.addWidget(self.label_load_power_meter)
    
    self.ui.frame_pml_contents_3 = QFrame(self.ui.frame_manual_control_pml_3)
    self.ui.frame_pml_contents_3.setObjectName(u"frame_pml_contents_3")
    self.ui.frame_pml_contents_3.setStyleSheet(u"border:none;")
    self.ui.frame_pml_contents_3.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_contents_3.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_15_3 = QHBoxLayout(self.ui.frame_pml_contents_3)
    self.ui.horizontalLayout_15_3.setObjectName(u"horizontalLayout_15_3")
    self.ui.frame_pml_display_3 = QFrame(self.ui.frame_pml_contents_3)
    self.ui.frame_pml_display_3.setObjectName(u"frame_pml_display_3")
    self.ui.frame_pml_display_3.setMinimumSize(QtCore.QSize(0, 280))
    self.ui.frame_pml_display_3.setMaximumSize(QtCore.QSize(300, 16777215))
    self.ui.frame_pml_display_3.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "QLabel{\n"
    "	font-family: \"Calibri\"\n"
    "}")
    self.ui.frame_pml_display_3.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_display_3.setFrameShadow(QFrame.Raised)
    self.ui.verticalLayout_20_3 = QVBoxLayout(self.ui.frame_pml_display_3)
    self.ui.verticalLayout_20_3.setSpacing(0)
    self.ui.verticalLayout_20_3.setObjectName(u"verticalLayout_20_3")
    self.ui.verticalLayout_20_3.setContentsMargins(0, 0, 0, 0)
    self.ui.label_pml_display_a_3 = QLabel(self.ui.frame_pml_display_3)
    self.ui.label_pml_display_a_3.setObjectName(u"label_pml_display_a_3")
    self.ui.label_pml_display_a_3.setMinimumSize(QtCore.QSize(0, 70))
    self.ui.label_pml_display_a_3.setMaximumSize(QtCore.QSize(16777215, 70))
    self.ui.label_pml_display_a_3.setFont(font12)
    self.ui.label_pml_display_a_3.setStyleSheet(u"color: rgb(255, 0, 0);\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "QLabel{\n"
    "	font-family: \"Calibri\"\n"
    "}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_pml_display_a_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
    
    self.ui.verticalLayout_20_3.addWidget(self.ui.label_pml_display_a_3)
    
    self.ui.label_pml_display_b_3 = QLabel(self.ui.frame_pml_display_3)
    self.ui.label_pml_display_b_3.setObjectName(u"label_pml_display_b_3")
    self.ui.label_pml_display_b_3.setMinimumSize(QtCore.QSize(0, 70))
    self.ui.label_pml_display_b_3.setMaximumSize(QtCore.QSize(16777215, 70))
    self.ui.label_pml_display_b_3.setFont(font12)
    self.ui.label_pml_display_b_3.setStyleSheet(u"color: rgb(255, 0, 0);\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "QLabel{\n"
    "	font-family: \"Calibri\"\n"
    "}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_pml_display_b_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
    
    self.ui.verticalLayout_20_3.addWidget(self.ui.label_pml_display_b_3)
    
    self.ui.label_pml_display_c_3 = QLabel(self.ui.frame_pml_display_3)
    self.ui.label_pml_display_c_3.setObjectName(u"label_pml_display_c_3")
    self.ui.label_pml_display_c_3.setMinimumSize(QtCore.QSize(0, 70))
    self.ui.label_pml_display_c_3.setMaximumSize(QtCore.QSize(16777215, 70))
    self.ui.label_pml_display_c_3.setFont(font12)
    self.ui.label_pml_display_c_3.setStyleSheet(u"color: rgb(255, 0, 0);\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "QLabel{\n"
    "	font-family: \"Calibri\"\n"
    "}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_pml_display_c_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
    
    self.ui.verticalLayout_20_3.addWidget(self.ui.label_pml_display_c_3)
    
    self.ui.label_pml_display_d_3 = QLabel(self.ui.frame_pml_display_3)
    self.ui.label_pml_display_d_3.setObjectName(u"label_pml_display_d_3")
    self.ui.label_pml_display_d_3.setMinimumSize(QtCore.QSize(0, 70))
    self.ui.label_pml_display_d_3.setMaximumSize(QtCore.QSize(16777215, 70))
    self.ui.label_pml_display_d_3.setFont(font12)
    self.ui.label_pml_display_d_3.setStyleSheet(u"color: rgb(255, 0, 0);\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "QLabel{\n"
    "	font-family: \"Calibri\"\n"
    "}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_pml_display_d_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
    
    self.ui.verticalLayout_20_3.addWidget(self.ui.label_pml_display_d_3)
    
    
    self.ui.horizontalLayout_15_3.addWidget(self.ui.frame_pml_display_3)
    
    self.ui.frame_pml_display_3_select = QFrame(self.ui.frame_pml_contents_3)
    self.ui.frame_pml_display_3_select.setObjectName(u"frame_pml_display_select_3")
    self.ui.frame_pml_display_3_select.setMaximumSize(QtCore.QSize(100, 16777215))
    self.ui.frame_pml_display_3_select.setStyleSheet(u"QFrame{\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "}")
    self.ui.frame_pml_display_3_select.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_display_3_select.setFrameShadow(QFrame.Raised)
    self.verticalLayout_21 = QVBoxLayout(self.ui.frame_pml_display_3_select)
    self.verticalLayout_21.setSpacing(0)
    self.verticalLayout_21.setObjectName(u"verticalLayout_21")
    self.verticalLayout_21.setContentsMargins(0, 0, 0, 0)
    self.cbx_pml_display_a = QComboBox(self.ui.frame_pml_display_3_select)
    self.cbx_pml_display_a.setObjectName(u"cbx_pml_display_a")
    self.cbx_pml_display_a.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.verticalLayout_21.addWidget(self.cbx_pml_display_a)
    
    self.cbx_pml_display_b = QComboBox(self.ui.frame_pml_display_3_select)
    self.cbx_pml_display_b.setObjectName(u"cbx_pml_display_b")
    self.cbx_pml_display_b.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.verticalLayout_21.addWidget(self.cbx_pml_display_b)
    
    self.cbx_pml_display_c = QComboBox(self.ui.frame_pml_display_3_select)
    self.cbx_pml_display_c.setObjectName(u"cbx_pml_display_c")
    self.cbx_pml_display_c.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.verticalLayout_21.addWidget(self.cbx_pml_display_c)
    
    self.cbx_pml_display_d = QComboBox(self.ui.frame_pml_display_3_select)
    self.cbx_pml_display_d.setObjectName(u"cbx_pml_display_d")
    self.cbx_pml_display_d.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.verticalLayout_21.addWidget(self.cbx_pml_display_d)
    
    
    self.ui.horizontalLayout_15_3.addWidget(self.ui.frame_pml_display_3_select)
    
    self.ui.frame_pml_control_3 = QFrame(self.ui.frame_pml_contents_3)
    self.ui.frame_pml_control_3.setObjectName(u"frame_pml_control_3")
    self.ui.frame_pml_control_3.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "")
    self.ui.frame_pml_control_3.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_3.setFrameShadow(QFrame.Raised)
    self.verticalLayout_29 = QVBoxLayout(self.ui.frame_pml_control_3)
    self.verticalLayout_29.setSpacing(0)
    self.verticalLayout_29.setObjectName(u"verticalLayout_29")
    self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
    self.ui.frame_pml_control_3__range = QFrame(self.ui.frame_pml_control_3)
    self.ui.frame_pml_control_3__range.setObjectName(u"frame_pml_control__range")
    self.ui.frame_pml_control_3__range.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_3__range.setFrameShadow(QFrame.Raised)
    self.formLayout_2 = QFormLayout(self.ui.frame_pml_control_3__range)
    self.formLayout_2.setObjectName(u"formLayout_2")
    self.label_pml_voltage_range = QLabel(self.ui.frame_pml_control_3__range)
    self.label_pml_voltage_range.setObjectName(u"label_pml_voltage_range")
    self.label_pml_voltage_range.setFont(font10)
    self.label_pml_voltage_range.setStyleSheet(u"border:none;")
    
    self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_pml_voltage_range)
    
    self.cbx_pml_voltage_range = QComboBox(self.ui.frame_pml_control_3__range)
    self.cbx_pml_voltage_range.addItem("")
    self.cbx_pml_voltage_range.addItem("")
    self.cbx_pml_voltage_range.setObjectName(u"cbx_pml_voltage_range")
    self.cbx_pml_voltage_range.setMaximumSize(QtCore.QSize(16777215, 54))
    self.cbx_pml_voltage_range.setFont(font10)
    
    self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.cbx_pml_voltage_range)
    
    self.label_pml_current_range = QLabel(self.ui.frame_pml_control_3__range)
    self.label_pml_current_range.setObjectName(u"label_pml_current_range")
    self.label_pml_current_range.setFont(font10)
    self.label_pml_current_range.setStyleSheet(u"border:none;")
    
    self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_pml_current_range)
    
    self.cbx_pml_current_range = QComboBox(self.ui.frame_pml_control_3__range)
    self.cbx_pml_current_range.addItem("")
    self.cbx_pml_current_range.addItem("")
    self.cbx_pml_current_range.setObjectName(u"cbx_pml_current_range")
    self.cbx_pml_current_range.setMaximumSize(QtCore.QSize(16777215, 54))
    self.cbx_pml_current_range.setFont(font10)
    
    self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.cbx_pml_current_range)
    
    
    self.verticalLayout_29.addWidget(self.ui.frame_pml_control_3__range)
    
    self.ui.frame_pml_control_3_lower = QFrame(self.ui.frame_pml_control_3)
    self.ui.frame_pml_control_3_lower.setObjectName(u"frame_pml_control_lower")
    self.ui.frame_pml_control_3_lower.setStyleSheet(u"border:none;")
    self.ui.frame_pml_control_3_lower.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_3_lower.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_19_3 = QHBoxLayout(self.ui.frame_pml_control_3_lower)
    self.ui.horizontalLayout_19_3.setSpacing(0)
    self.ui.horizontalLayout_19_3.setObjectName(u"horizontalLayout_19_3")
    self.ui.horizontalLayout_19_3.setContentsMargins(0, 0, 0, 0)
    self.frame_pml_integration = QFrame(self.ui.frame_pml_control_3_lower)
    self.frame_pml_integration.setObjectName(u"frame_pml_integration")
    self.frame_pml_integration.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.frame_pml_integration.setFrameShape(QFrame.StyledPanel)
    self.frame_pml_integration.setFrameShadow(QFrame.Raised)
    self.verticalLayout_30 = QVBoxLayout(self.frame_pml_integration)
    self.verticalLayout_30.setObjectName(u"verticalLayout_30")
    self.label_pml_integration = QLabel(self.frame_pml_integration)
    self.label_pml_integration.setObjectName(u"label_pml_integration")
    sizePolicy.setHeightForWidth(self.label_pml_integration.sizePolicy().hasHeightForWidth())
    self.label_pml_integration.setSizePolicy(sizePolicy)
    self.label_pml_integration.setMinimumSize(QtCore.QSize(0, 20))
    self.label_pml_integration.setMaximumSize(QtCore.QSize(16777215, 20))
    self.label_pml_integration.setFont(font10)
    self.label_pml_integration.setStyleSheet(u"border:none;")
    
    self.verticalLayout_30.addWidget(self.label_pml_integration)
    
    self.btn_pml_integration_start = QPushButton(self.frame_pml_integration)
    self.btn_pml_integration_start.setObjectName(u"btn_pml_integration_start")
    self.btn_pml_integration_start.setFont(font10)
    self.btn_pml_integration_start.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}")
    
    self.verticalLayout_30.addWidget(self.btn_pml_integration_start)
    
    self.btn_pml_integration_stop = QPushButton(self.frame_pml_integration)
    self.btn_pml_integration_stop.setObjectName(u"btn_pml_integration_stop")
    self.btn_pml_integration_stop.setFont(font10)
    self.btn_pml_integration_stop.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}")
    
    self.verticalLayout_30.addWidget(self.btn_pml_integration_stop)
    
    self.btn_pml_integration_reset = QPushButton(self.frame_pml_integration)
    self.btn_pml_integration_reset.setObjectName(u"btn_pml_integration_reset")
    self.btn_pml_integration_reset.setFont(font10)
    self.btn_pml_integration_reset.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}")
    
    self.verticalLayout_30.addWidget(self.btn_pml_integration_reset)
    
    
    self.ui.horizontalLayout_19_3.addWidget(self.frame_pml_integration)
    
    self.frame_pml_averaging = QFrame(self.ui.frame_pml_control_3_lower)
    self.frame_pml_averaging.setObjectName(u"frame_pml_averaging")
    self.frame_pml_averaging.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.frame_pml_averaging.setFrameShape(QFrame.StyledPanel)
    self.frame_pml_averaging.setFrameShadow(QFrame.Raised)
    self.verticalLayout_31 = QVBoxLayout(self.frame_pml_averaging)
    self.verticalLayout_31.setSpacing(2)
    self.verticalLayout_31.setObjectName(u"verticalLayout_31")
    self.verticalLayout_31.setContentsMargins(-1, 5, -1, 5)
    self.label_pml_averaging = QLabel(self.frame_pml_averaging)
    self.label_pml_averaging.setObjectName(u"label_pml_averaging")
    sizePolicy.setHeightForWidth(self.label_pml_averaging.sizePolicy().hasHeightForWidth())
    self.label_pml_averaging.setSizePolicy(sizePolicy)
    self.label_pml_averaging.setMinimumSize(QtCore.QSize(0, 20))
    self.label_pml_averaging.setMaximumSize(QtCore.QSize(16777215, 20))
    self.label_pml_averaging.setFont(font10)
    self.label_pml_averaging.setStyleSheet(u"border:none;")
    
    self.verticalLayout_31.addWidget(self.label_pml_averaging)
    
    self.btn_pml_averaging_toggle = QPushButton(self.frame_pml_averaging)
    self.btn_pml_averaging_toggle.setObjectName(u"btn_pml_averaging_toggle")
    self.btn_pml_averaging_toggle.setFont(font10)
    self.btn_pml_averaging_toggle.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}")
    
    self.verticalLayout_31.addWidget(self.btn_pml_averaging_toggle)
    
    self.cbx_pml_averaging_count = QComboBox(self.frame_pml_averaging)
    self.cbx_pml_averaging_count.addItem("")
    self.cbx_pml_averaging_count.addItem("")
    self.cbx_pml_averaging_count.addItem("")
    self.cbx_pml_averaging_count.setObjectName(u"cbx_pml_averaging_count")
    self.cbx_pml_averaging_count.setMaximumSize(QtCore.QSize(16777215, 40))
    self.cbx_pml_averaging_count.setFont(font10)
    
    self.verticalLayout_31.addWidget(self.cbx_pml_averaging_count)
    
    self.cbx_pml_averaging_mode = QComboBox(self.frame_pml_averaging)
    self.cbx_pml_averaging_mode.addItem("")
    self.cbx_pml_averaging_mode.addItem("")
    self.cbx_pml_averaging_mode.setObjectName(u"cbx_pml_averaging_mode")
    self.cbx_pml_averaging_mode.setMaximumSize(QtCore.QSize(16777215, 40))
    self.cbx_pml_averaging_mode.setFont(font10)
    
    self.verticalLayout_31.addWidget(self.cbx_pml_averaging_mode)
    
    
    self.ui.horizontalLayout_19_3.addWidget(self.frame_pml_averaging)
    
    self.frame_pml_measure_mode = QFrame(self.ui.frame_pml_control_3_lower)
    self.frame_pml_measure_mode.setObjectName(u"frame_pml_measure_mode")
    self.frame_pml_measure_mode.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.frame_pml_measure_mode.setFrameShape(QFrame.StyledPanel)
    self.frame_pml_measure_mode.setFrameShadow(QFrame.Raised)
    self.verticalLayout_32 = QVBoxLayout(self.frame_pml_measure_mode)
    self.verticalLayout_32.setSpacing(13)
    self.verticalLayout_32.setObjectName(u"verticalLayout_32")
    self.verticalLayout_32.setContentsMargins(13, 13, 13, 13)
    self.label_pml_measure_mode = QLabel(self.frame_pml_measure_mode)
    self.label_pml_measure_mode.setObjectName(u"label_pml_measure_mode")
    sizePolicy.setHeightForWidth(self.label_pml_measure_mode.sizePolicy().hasHeightForWidth())
    self.label_pml_measure_mode.setSizePolicy(sizePolicy)
    self.label_pml_measure_mode.setMaximumSize(QtCore.QSize(16777215, 20))
    self.label_pml_measure_mode.setFont(font10)
    self.label_pml_measure_mode.setStyleSheet(u"border:none;")
    
    self.verticalLayout_32.addWidget(self.label_pml_measure_mode)
    
    self.btn_pml_measure_mode = QPushButton(self.frame_pml_measure_mode)
    self.btn_pml_measure_mode.setObjectName(u"btn_pml_measure_mode")
    self.btn_pml_measure_mode.setFont(font10)
    self.btn_pml_measure_mode.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}")
    
    self.verticalLayout_32.addWidget(self.btn_pml_measure_mode)
    
    
    self.ui.horizontalLayout_19_3.addWidget(self.frame_pml_measure_mode)
    
    
    self.verticalLayout_29.addWidget(self.ui.frame_pml_control_3_lower)
    
    
    self.ui.horizontalLayout_15_3.addWidget(self.ui.frame_pml_control_3)
    
    
    self.ui.verticalLayout_19_3.addWidget(self.ui.frame_pml_contents_3)
    
    
    self.ui.horizontalLayout_9.addWidget(self.ui.frame_manual_control_pml_3)

    # ELOAD 4
    self.ui.frame_manual_control_eload_4 = QFrame(self.ui.frame_manual_control_lower)
    self.ui.frame_manual_control_eload_4.setObjectName(u"frame_manual_control_eload_4")
    sizePolicy20 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
    sizePolicy20.setHorizontalStretch(3)
    sizePolicy20.setVerticalStretch(0)
    sizePolicy20.setHeightForWidth(self.ui.frame_manual_control_eload_4.sizePolicy().hasHeightForWidth())
    self.ui.frame_manual_control_eload_4.setSizePolicy(sizePolicy20)
    self.ui.frame_manual_control_eload_4.setMinimumSize(QtCore.QSize(400, 0))
    self.ui.frame_manual_control_eload_4.setStyleSheet(u"QFrame{\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "}")
    self.ui.frame_manual_control_eload_4.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4.setFrameShadow(QFrame.Raised)
    self.ui.verticalLayout_23_4 = QVBoxLayout(self.ui.frame_manual_control_eload_4)
    self.ui.verticalLayout_23_4.setObjectName(u"verticalLayout_23_4")
    self.ui.label_manual_control_eload_4 = QLabel(self.ui.frame_manual_control_eload_4)
    self.ui.label_manual_control_eload_4.setObjectName(u"label_manual_control_eload_4")
    self.ui.label_manual_control_eload_4.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_4.setFont(font1)
    self.ui.label_manual_control_eload_4.setCursor(QCursor(Qt.UpArrowCursor))
    self.ui.label_manual_control_eload_4.setStyleSheet(u"QLabel{border:none;}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_manual_control_eload_4.setAlignment(Qt.AlignCenter)
    
    self.ui.verticalLayout_23_4.addWidget(self.ui.label_manual_control_eload_4)
    
    self.ui.frame_manual_control_eload_4_contents = QFrame(self.ui.frame_manual_control_eload_4)
    self.ui.frame_manual_control_eload_4_contents.setObjectName(u"frame_manual_control_eload_contents_4")
    self.ui.frame_manual_control_eload_4_contents.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_4_contents.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_contents.setFrameShadow(QFrame.Raised)
    self.verticalLayout_77 = QVBoxLayout(self.ui.frame_manual_control_eload_4_contents)
    self.verticalLayout_77.setObjectName(u"verticalLayout_77")
    self.ui.frame_manual_control_eload_4_top = QFrame(self.ui.frame_manual_control_eload_4_contents)
    self.ui.frame_manual_control_eload_4_top.setObjectName(u"frame_manual_control_eload_top_4")
    self.ui.frame_manual_control_eload_4_top.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_top.setFrameShadow(QFrame.Raised)
    self.horizontalLayout_47 = QHBoxLayout(self.ui.frame_manual_control_eload_4_top)
    self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
    self.cbx_manual_control_eload_type = QComboBox(self.ui.frame_manual_control_eload_4_top)
    self.cbx_manual_control_eload_type.addItem("")
    self.cbx_manual_control_eload_type.addItem("")
    self.cbx_manual_control_eload_type.addItem("")
    self.cbx_manual_control_eload_type.setObjectName(u"cbx_manual_control_eload_type")
    self.cbx_manual_control_eload_type.setMaximumSize(QtCore.QSize(16777215, 40))
    self.cbx_manual_control_eload_type.setFont(font10)
    self.cbx_manual_control_eload_type.setStyleSheet(u"QComboBox{\n"
    "border: 2px solid black;\n"
    "border-radius:5px;\n"
    "}\n"
    "\n"
    "QComboBox:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    
    self.horizontalLayout_47.addWidget(self.cbx_manual_control_eload_type)
    
    self.ui.btn_manual_control_eload_a_b_swap_4 = QPushButton(self.ui.frame_manual_control_eload_4_top)
    self.ui.btn_manual_control_eload_a_b_swap_4.setObjectName(u"btn_manual_control_eload_a_b_swap_4")
    self.ui.btn_manual_control_eload_a_b_swap_4.setMinimumSize(QtCore.QSize(120, 40))
    self.ui.btn_manual_control_eload_a_b_swap_4.setFont(font13)
    self.ui.btn_manual_control_eload_a_b_swap_4.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    icon10 = QIcon()
    icon10.addFile(u":/20x20/icons/20x20/cil-swap-horizontal.png", QtCore.QSize(), QIcon.Normal, QIcon.Off)
    self.ui.btn_manual_control_eload_a_b_swap_4.setIcon(icon10)
    self.ui.btn_manual_control_eload_a_b_swap_4.setCheckable(False)
    self.ui.btn_manual_control_eload_a_b_swap_4.setChecked(False)
    
    self.horizontalLayout_47.addWidget(self.ui.btn_manual_control_eload_a_b_swap_4)
    
    
    self.verticalLayout_77.addWidget(self.ui.frame_manual_control_eload_4_top)
    
    self.ui.frame_manual_control_eload_4_center = QFrame(self.ui.frame_manual_control_eload_4_contents)
    self.ui.frame_manual_control_eload_4_center.setObjectName(u"frame_manual_control_eload_center_4")
    self.ui.frame_manual_control_eload_4_center.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_center.setFrameShadow(QFrame.Raised)
    self.horizontalLayout_46 = QHBoxLayout(self.ui.frame_manual_control_eload_4_center)
    self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
    self.ui.frame_manual_control_eload_4_level = QFrame(self.ui.frame_manual_control_eload_4_center)
    self.ui.frame_manual_control_eload_4_level.setObjectName(u"frame_manual_control_eload_level_4")
    self.ui.frame_manual_control_eload_4_level.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_level.setFrameShadow(QFrame.Raised)
    self.verticalLayout_70 = QVBoxLayout(self.ui.frame_manual_control_eload_4_level)
    self.verticalLayout_70.setObjectName(u"verticalLayout_70")
    self.ui.frame_manual_control_eload_4_a = QFrame(self.ui.frame_manual_control_eload_4_level)
    self.ui.frame_manual_control_eload_4_a.setObjectName(u"frame_manual_control_eload_a_4")
    self.ui.frame_manual_control_eload_4_a.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_a.setFrameShadow(QFrame.Raised)
    self.horizontalLayout_45 = QHBoxLayout(self.ui.frame_manual_control_eload_4_a)
    self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
    self.ui.label_manual_control_eload_4_a = QLabel(self.ui.frame_manual_control_eload_4_a)
    self.ui.label_manual_control_eload_4_a.setObjectName(u"label_manual_control_eload_a_4")
    self.ui.label_manual_control_eload_4_a.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_4_a.setFont(font10)
    self.ui.label_manual_control_eload_4_a.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.ui.label_manual_control_eload_4_a.setAlignment(Qt.AlignCenter)
    
    self.horizontalLayout_45.addWidget(self.ui.label_manual_control_eload_4_a)
    
    self.ui.lineedit_manual_control_eload_a_level_4 = QLineEdit(self.ui.frame_manual_control_eload_4_a)
    self.ui.lineedit_manual_control_eload_a_level_4.setObjectName(u"lineedit_manual_control_eload_a_level_4")
    sizePolicy21 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    sizePolicy21.setHorizontalStretch(4)
    sizePolicy21.setVerticalStretch(0)
    sizePolicy21.setHeightForWidth(self.ui.lineedit_manual_control_eload_a_level_4.sizePolicy().hasHeightForWidth())
    self.ui.lineedit_manual_control_eload_a_level_4.setSizePolicy(sizePolicy21)
    self.ui.lineedit_manual_control_eload_a_level_4.setMinimumSize(QtCore.QSize(0, 40))
    self.ui.lineedit_manual_control_eload_a_level_4.setFont(font10)
    self.ui.lineedit_manual_control_eload_a_level_4.setStyleSheet(u"QLineEdit {\n"
    "	background-color: rgb(27, 29, 35);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(27, 29, 35);\n"
    "	padding-left: 10px;\n"
    "}\n"
    "QLineEdit:hover {\n"
    "	border: 2px solid rgb(64, 71, 88);\n"
    "}\n"
    "QLineEdit:focus {\n"
    "	border: 2px solid rgb(91, 101, 124);\n"
    "}\n"
    "\n"
    "QLineEdit:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "	background-color: rgb(37, 39, 45);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(37, 39, 45);\n"
    "	padding-left: 10px;\n"
    "}")
    
    self.horizontalLayout_45.addWidget(self.ui.lineedit_manual_control_eload_a_level_4)
    
    self.ui.label_manual_control_eload_4_a_level_unit = QLabel(self.ui.frame_manual_control_eload_4_a)
    self.ui.label_manual_control_eload_4_a_level_unit.setObjectName(u"label_manual_control_eload_a_level_unit")
    sizePolicy11.setHeightForWidth(self.ui.label_manual_control_eload_4_a_level_unit.sizePolicy().hasHeightForWidth())
    self.ui.label_manual_control_eload_4_a_level_unit.setSizePolicy(sizePolicy11)
    self.ui.label_manual_control_eload_4_a_level_unit.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_4_a_level_unit.setFont(font10)
    self.ui.label_manual_control_eload_4_a_level_unit.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    
    self.horizontalLayout_45.addWidget(self.ui.label_manual_control_eload_4_a_level_unit)
    
    self.btn_manual_control_eload_set_A = QPushButton(self.ui.frame_manual_control_eload_4_a)
    self.btn_manual_control_eload_set_A.setObjectName(u"btn_manual_control_eload_set_A")
    self.btn_manual_control_eload_set_A.setMinimumSize(QtCore.QSize(50, 30))
    self.btn_manual_control_eload_set_A.setFont(font4)
    self.btn_manual_control_eload_set_A.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    self.btn_manual_control_eload_set_A.setCheckable(False)
    self.btn_manual_control_eload_set_A.setChecked(False)
    
    self.horizontalLayout_45.addWidget(self.btn_manual_control_eload_set_A)
    
    
    self.verticalLayout_70.addWidget(self.ui.frame_manual_control_eload_4_a)
    
    self.ui.frame_manual_control_eload_4_b = QFrame(self.ui.frame_manual_control_eload_4_level)
    self.ui.frame_manual_control_eload_4_b.setObjectName(u"frame_manual_control_eload_b_4")
    self.ui.frame_manual_control_eload_4_b.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_b.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_39_4 = QHBoxLayout(self.ui.frame_manual_control_eload_4_b)
    self.ui.horizontalLayout_39_4.setObjectName(u"horizontalLayout_39_4")
    self.ui.label_manual_control_eload_4_b = QLabel(self.ui.frame_manual_control_eload_4_b)
    self.ui.label_manual_control_eload_4_b.setObjectName(u"label_manual_control_eload_b_4")
    self.ui.label_manual_control_eload_4_b.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_4_b.setFont(font10)
    self.ui.label_manual_control_eload_4_b.setLayoutDirection(Qt.LeftToRight)
    self.ui.label_manual_control_eload_4_b.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.ui.label_manual_control_eload_4_b.setAlignment(Qt.AlignCenter)
    
    self.ui.horizontalLayout_39_4.addWidget(self.ui.label_manual_control_eload_4_b)
    
    self.ui.lineedit_manual_control_eload_b_level_4 = QLineEdit(self.ui.frame_manual_control_eload_4_b)
    self.ui.lineedit_manual_control_eload_b_level_4.setObjectName(u"lineedit_manual_control_eload_b_level_4")
    sizePolicy21.setHeightForWidth(self.ui.lineedit_manual_control_eload_b_level_4.sizePolicy().hasHeightForWidth())
    self.ui.lineedit_manual_control_eload_b_level_4.setSizePolicy(sizePolicy21)
    self.ui.lineedit_manual_control_eload_b_level_4.setMinimumSize(QtCore.QSize(0, 40))
    self.ui.lineedit_manual_control_eload_b_level_4.setFont(font10)
    self.ui.lineedit_manual_control_eload_b_level_4.setStyleSheet(u"QLineEdit {\n"
    "	background-color: rgb(27, 29, 35);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(27, 29, 35);\n"
    "	padding-left: 10px;\n"
    "}\n"
    "QLineEdit:hover {\n"
    "	border: 2px solid rgb(64, 71, 88);\n"
    "}\n"
    "QLineEdit:focus {\n"
    "	border: 2px solid rgb(91, 101, 124);\n"
    "}\n"
    "\n"
    "QLineEdit:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "	background-color: rgb(37, 39, 45);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(37, 39, 45);\n"
    "	padding-left: 10px;\n"
    "}")
    
    self.ui.horizontalLayout_39_4.addWidget(self.ui.lineedit_manual_control_eload_b_level_4)
    
    self.ui.label_manual_control_eload_4_b_level_unit = QLabel(self.ui.frame_manual_control_eload_4_b)
    self.ui.label_manual_control_eload_4_b_level_unit.setObjectName(u"label_manual_control_eload_b_level_unit")
    sizePolicy11.setHeightForWidth(self.ui.label_manual_control_eload_4_b_level_unit.sizePolicy().hasHeightForWidth())
    self.ui.label_manual_control_eload_4_b_level_unit.setSizePolicy(sizePolicy11)
    self.ui.label_manual_control_eload_4_b_level_unit.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_4_b_level_unit.setFont(font10)
    self.ui.label_manual_control_eload_4_b_level_unit.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    
    self.ui.horizontalLayout_39_4.addWidget(self.ui.label_manual_control_eload_4_b_level_unit)
    
    self.btn_manual_control_eload_set_B = QPushButton(self.ui.frame_manual_control_eload_4_b)
    self.btn_manual_control_eload_set_B.setObjectName(u"btn_manual_control_eload_set_B")
    self.btn_manual_control_eload_set_B.setMinimumSize(QtCore.QSize(50, 30))
    self.btn_manual_control_eload_set_B.setFont(font4)
    self.btn_manual_control_eload_set_B.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    self.btn_manual_control_eload_set_B.setCheckable(False)
    self.btn_manual_control_eload_set_B.setChecked(False)
    
    self.ui.horizontalLayout_39_4.addWidget(self.btn_manual_control_eload_set_B)
    
    
    self.verticalLayout_70.addWidget(self.ui.frame_manual_control_eload_4_b)
    
    
    self.horizontalLayout_46.addWidget(self.ui.frame_manual_control_eload_4_level)
    
    self.ui.frame_manual_control_eload_4_slew = QFrame(self.ui.frame_manual_control_eload_4_center)
    self.ui.frame_manual_control_eload_4_slew.setObjectName(u"frame_manual_control_eload_slew_4")
    self.ui.frame_manual_control_eload_4_slew.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_slew.setFrameShadow(QFrame.Raised)
    self.gridLayout_29 = QGridLayout(self.ui.frame_manual_control_eload_4_slew)
    self.gridLayout_29.setObjectName(u"gridLayout_29")
    self.ui.frame_manual_control_eload_4_slew_fall = QFrame(self.ui.frame_manual_control_eload_4_slew)
    self.ui.frame_manual_control_eload_4_slew_fall.setObjectName(u"frame_manual_control_eload_slew_fall_4")
    self.ui.frame_manual_control_eload_4_slew_fall.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_slew_fall.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_38_4 = QHBoxLayout(self.ui.frame_manual_control_eload_4_slew_fall)
    self.ui.horizontalLayout_38_4.setObjectName(u"horizontalLayout_38_4")
    self.label_manual_control_electronic_load_fall = QLabel(self.ui.frame_manual_control_eload_4_slew_fall)
    self.label_manual_control_electronic_load_fall.setObjectName(u"label_manual_control_electronic_load_fall")
    self.label_manual_control_electronic_load_fall.setMaximumSize(QtCore.QSize(16777215, 30))
    self.label_manual_control_electronic_load_fall.setFont(font10)
    self.label_manual_control_electronic_load_fall.setLayoutDirection(Qt.LeftToRight)
    self.label_manual_control_electronic_load_fall.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.label_manual_control_electronic_load_fall.setAlignment(Qt.AlignCenter)
    
    self.ui.horizontalLayout_38_4.addWidget(self.label_manual_control_electronic_load_fall)
    
    self.lineedit_manual_control_eload_slew_fall = QLineEdit(self.ui.frame_manual_control_eload_4_slew_fall)
    self.lineedit_manual_control_eload_slew_fall.setObjectName(u"lineedit_manual_control_eload_slew_fall")
    sizePolicy21.setHeightForWidth(self.lineedit_manual_control_eload_slew_fall.sizePolicy().hasHeightForWidth())
    self.lineedit_manual_control_eload_slew_fall.setSizePolicy(sizePolicy21)
    self.lineedit_manual_control_eload_slew_fall.setMinimumSize(QtCore.QSize(0, 40))
    self.lineedit_manual_control_eload_slew_fall.setFont(font10)
    self.lineedit_manual_control_eload_slew_fall.setStyleSheet(u"QLineEdit {\n"
    "	background-color: rgb(27, 29, 35);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(27, 29, 35);\n"
    "	padding-left: 10px;\n"
    "}\n"
    "QLineEdit:hover {\n"
    "	border: 2px solid rgb(64, 71, 88);\n"
    "}\n"
    "QLineEdit:focus {\n"
    "	border: 2px solid rgb(91, 101, 124);\n"
    "}\n"
    "\n"
    "QLineEdit:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "	background-color: rgb(37, 39, 45);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(37, 39, 45);\n"
    "	padding-left: 10px;\n"
    "}")
    
    self.ui.horizontalLayout_38_4.addWidget(self.lineedit_manual_control_eload_slew_fall)
    
    self.ui.label_manual_control_eload_4_slew_fall_unit = QLabel(self.ui.frame_manual_control_eload_4_slew_fall)
    self.ui.label_manual_control_eload_4_slew_fall_unit.setObjectName(u"label_manual_control_eload_slew_fall_unit")
    sizePolicy11.setHeightForWidth(self.ui.label_manual_control_eload_4_slew_fall_unit.sizePolicy().hasHeightForWidth())
    self.ui.label_manual_control_eload_4_slew_fall_unit.setSizePolicy(sizePolicy11)
    self.ui.label_manual_control_eload_4_slew_fall_unit.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_4_slew_fall_unit.setFont(font10)
    self.ui.label_manual_control_eload_4_slew_fall_unit.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    
    self.ui.horizontalLayout_38_4.addWidget(self.ui.label_manual_control_eload_4_slew_fall_unit)
    
    
    self.gridLayout_29.addWidget(self.ui.frame_manual_control_eload_4_slew_fall, 1, 0, 1, 1)
    
    self.ui.frame_manual_control_eload_4_slew_rise = QFrame(self.ui.frame_manual_control_eload_4_slew)
    self.ui.frame_manual_control_eload_4_slew_rise.setObjectName(u"frame_manual_control_eload_slew_rise_4")
    self.ui.frame_manual_control_eload_4_slew_rise.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_slew_rise.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_36_4 = QHBoxLayout(self.ui.frame_manual_control_eload_4_slew_rise)
    self.ui.horizontalLayout_36_4.setObjectName(u"horizontalLayout_36_4")
    self.label_manual_control_electronic_load_rise = QLabel(self.ui.frame_manual_control_eload_4_slew_rise)
    self.label_manual_control_electronic_load_rise.setObjectName(u"label_manual_control_electronic_load_rise")
    self.label_manual_control_electronic_load_rise.setMaximumSize(QtCore.QSize(16777215, 30))
    self.label_manual_control_electronic_load_rise.setFont(font10)
    self.label_manual_control_electronic_load_rise.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.label_manual_control_electronic_load_rise.setAlignment(Qt.AlignCenter)
    
    self.ui.horizontalLayout_36_4.addWidget(self.label_manual_control_electronic_load_rise)
    
    self.lineedit_manual_control_eload_slew_rise = QLineEdit(self.ui.frame_manual_control_eload_4_slew_rise)
    self.lineedit_manual_control_eload_slew_rise.setObjectName(u"lineedit_manual_control_eload_slew_rise")
    sizePolicy21.setHeightForWidth(self.lineedit_manual_control_eload_slew_rise.sizePolicy().hasHeightForWidth())
    self.lineedit_manual_control_eload_slew_rise.setSizePolicy(sizePolicy21)
    self.lineedit_manual_control_eload_slew_rise.setMinimumSize(QtCore.QSize(0, 40))
    self.lineedit_manual_control_eload_slew_rise.setFont(font10)
    self.lineedit_manual_control_eload_slew_rise.setStyleSheet(u"QLineEdit {\n"
    "	background-color: rgb(27, 29, 35);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(27, 29, 35);\n"
    "	padding-left: 10px;\n"
    "}\n"
    "QLineEdit:hover {\n"
    "	border: 2px solid rgb(64, 71, 88);\n"
    "}\n"
    "QLineEdit:focus {\n"
    "	border: 2px solid rgb(91, 101, 124);\n"
    "}\n"
    "\n"
    "QLineEdit:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "	background-color: rgb(37, 39, 45);\n"
    "	border-radius: 5px;\n"
    "	border: 2px solid rgb(37, 39, 45);\n"
    "	padding-left: 10px;\n"
    "}")
    
    self.ui.horizontalLayout_36_4.addWidget(self.lineedit_manual_control_eload_slew_rise)
    
    self.ui.label_manual_control_eload_4_slew_rise_unit = QLabel(self.ui.frame_manual_control_eload_4_slew_rise)
    self.ui.label_manual_control_eload_4_slew_rise_unit.setObjectName(u"label_manual_control_eload_slew_rise_unit")
    sizePolicy11.setHeightForWidth(self.ui.label_manual_control_eload_4_slew_rise_unit.sizePolicy().hasHeightForWidth())
    self.ui.label_manual_control_eload_4_slew_rise_unit.setSizePolicy(sizePolicy11)
    self.ui.label_manual_control_eload_4_slew_rise_unit.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_manual_control_eload_4_slew_rise_unit.setFont(font10)
    self.ui.label_manual_control_eload_4_slew_rise_unit.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    
    self.ui.horizontalLayout_36_4.addWidget(self.ui.label_manual_control_eload_4_slew_rise_unit)
    
    
    self.gridLayout_29.addWidget(self.ui.frame_manual_control_eload_4_slew_rise, 0, 0, 1, 1)
    
    self.btn_manual_control_eload_set_slew = QPushButton(self.ui.frame_manual_control_eload_4_slew)
    self.btn_manual_control_eload_set_slew.setObjectName(u"btn_manual_control_eload_set_slew")
    sizePolicy19.setHeightForWidth(self.btn_manual_control_eload_set_slew.sizePolicy().hasHeightForWidth())
    self.btn_manual_control_eload_set_slew.setSizePolicy(sizePolicy19)
    self.btn_manual_control_eload_set_slew.setMinimumSize(QtCore.QSize(50, 60))
    self.btn_manual_control_eload_set_slew.setFont(font4)
    self.btn_manual_control_eload_set_slew.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    self.btn_manual_control_eload_set_slew.setCheckable(False)
    self.btn_manual_control_eload_set_slew.setChecked(False)
    
    self.gridLayout_29.addWidget(self.btn_manual_control_eload_set_slew, 0, 1, 2, 1)
    
    
    self.horizontalLayout_46.addWidget(self.ui.frame_manual_control_eload_4_slew)
    
    
    self.verticalLayout_77.addWidget(self.ui.frame_manual_control_eload_4_center)
    
    self.ui.frame_manual_control_eload_4_bottom = QFrame(self.ui.frame_manual_control_eload_4_contents)
    self.ui.frame_manual_control_eload_4_bottom.setObjectName(u"frame_manual_control_eload_bottom_4")
    self.ui.frame_manual_control_eload_4_bottom.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_bottom.setFrameShadow(QFrame.Raised)
    self.horizontalLayout_56 = QHBoxLayout(self.ui.frame_manual_control_eload_4_bottom)
    self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
    self.btn_manual_control_eload_turn_on = QPushButton(self.ui.frame_manual_control_eload_4_bottom)
    self.btn_manual_control_eload_turn_on.setObjectName(u"btn_manual_control_eload_turn_on")
    self.btn_manual_control_eload_turn_on.setMinimumSize(QtCore.QSize(120, 40))
    self.btn_manual_control_eload_turn_on.setFont(font13)
    self.btn_manual_control_eload_turn_on.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    self.btn_manual_control_eload_turn_on.setIcon(icon8)
    self.btn_manual_control_eload_turn_on.setCheckable(False)
    self.btn_manual_control_eload_turn_on.setChecked(False)
    
    self.horizontalLayout_56.addWidget(self.btn_manual_control_eload_turn_on)
    
    self.btn_manual_control_eload_turn_off = QPushButton(self.ui.frame_manual_control_eload_4_bottom)
    self.btn_manual_control_eload_turn_off.setObjectName(u"btn_manual_control_eload_turn_off")
    self.btn_manual_control_eload_turn_off.setMinimumSize(QtCore.QSize(120, 40))
    self.btn_manual_control_eload_turn_off.setFont(font13)
    self.btn_manual_control_eload_turn_off.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}\n"
    "QPushButton:disabled {	\n"
    "	background-color: rgb(25, 30, 39);\n"
    "	border: 2px solid rgb(33, 40, 51);\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    self.btn_manual_control_eload_turn_off.setIcon(icon9)
    self.btn_manual_control_eload_turn_off.setCheckable(False)
    self.btn_manual_control_eload_turn_off.setChecked(False)
    
    self.horizontalLayout_56.addWidget(self.btn_manual_control_eload_turn_off)
    
    
    self.verticalLayout_77.addWidget(self.ui.frame_manual_control_eload_4_bottom)
    
    
    self.ui.verticalLayout_23_4.addWidget(self.ui.frame_manual_control_eload_4_contents)
    
    
    self.ui.horizontalLayout_13.addWidget(self.ui.frame_manual_control_eload_4)

    # PML 4
    self.ui.frame_manual_control_pml_4 = QFrame(self.ui.frame_manual_control_upper)
    self.ui.frame_manual_control_pml_4.setObjectName(u"frame_manual_control_pml_4")
    self.ui.frame_manual_control_pml_4.setEnabled(True)
    self.ui.frame_manual_control_pml_4.setMinimumSize(QtCore.QSize(300, 0))
    self.ui.frame_manual_control_pml_4.setStyleSheet(u"QFrame{\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "};")
    self.ui.frame_manual_control_pml_4.setFrameShape(QFrame.NoFrame)
    self.ui.frame_manual_control_pml_4.setFrameShadow(QFrame.Sunken)
    self.ui.verticalLayout_19_4 = QVBoxLayout(self.ui.frame_manual_control_pml_4)
    self.ui.verticalLayout_19_4.setObjectName(u"verticalLayout_19_4")
    self.label_load_power_meter = QLabel(self.ui.frame_manual_control_pml_4)
    self.label_load_power_meter.setObjectName(u"label_load_power_meter")
    self.label_load_power_meter.setMaximumSize(QtCore.QSize(16777215, 30))
    self.label_load_power_meter.setFont(font1)
    self.label_load_power_meter.setCursor(QCursor(Qt.ArrowCursor))
    self.label_load_power_meter.setStyleSheet(u"QLabel{border:none;}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.label_load_power_meter.setAlignment(Qt.AlignCenter)
    
    self.ui.verticalLayout_19_4.addWidget(self.label_load_power_meter)
    
    self.ui.frame_pml_contents_4 = QFrame(self.ui.frame_manual_control_pml_4)
    self.ui.frame_pml_contents_4.setObjectName(u"frame_pml_contents_4")
    self.ui.frame_pml_contents_4.setStyleSheet(u"border:none;")
    self.ui.frame_pml_contents_4.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_contents_4.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_15_4 = QHBoxLayout(self.ui.frame_pml_contents_4)
    self.ui.horizontalLayout_15_4.setObjectName(u"horizontalLayout_15_4")
    self.ui.frame_pml_display_4 = QFrame(self.ui.frame_pml_contents_4)
    self.ui.frame_pml_display_4.setObjectName(u"frame_pml_display_4")
    self.ui.frame_pml_display_4.setMinimumSize(QtCore.QSize(0, 280))
    self.ui.frame_pml_display_4.setMaximumSize(QtCore.QSize(300, 16777215))
    self.ui.frame_pml_display_4.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "QLabel{\n"
    "	font-family: \"Calibri\"\n"
    "}")
    self.ui.frame_pml_display_4.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_display_4.setFrameShadow(QFrame.Raised)
    self.ui.verticalLayout_20_4 = QVBoxLayout(self.ui.frame_pml_display_4)
    self.ui.verticalLayout_20_4.setSpacing(0)
    self.ui.verticalLayout_20_4.setObjectName(u"verticalLayout_20_4")
    self.ui.verticalLayout_20_4.setContentsMargins(0, 0, 0, 0)
    self.ui.label_pml_display_a_4 = QLabel(self.ui.frame_pml_display_4)
    self.ui.label_pml_display_a_4.setObjectName(u"label_pml_display_a_4")
    self.ui.label_pml_display_a_4.setMinimumSize(QtCore.QSize(0, 70))
    self.ui.label_pml_display_a_4.setMaximumSize(QtCore.QSize(16777215, 70))
    self.ui.label_pml_display_a_4.setFont(font12)
    self.ui.label_pml_display_a_4.setStyleSheet(u"color: rgb(255, 0, 0);\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "QLabel{\n"
    "	font-family: \"Calibri\"\n"
    "}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_pml_display_a_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
    
    self.ui.verticalLayout_20_4.addWidget(self.ui.label_pml_display_a_4)
    
    self.ui.label_pml_display_b_4 = QLabel(self.ui.frame_pml_display_4)
    self.ui.label_pml_display_b_4.setObjectName(u"label_pml_display_b_4")
    self.ui.label_pml_display_b_4.setMinimumSize(QtCore.QSize(0, 70))
    self.ui.label_pml_display_b_4.setMaximumSize(QtCore.QSize(16777215, 70))
    self.ui.label_pml_display_b_4.setFont(font12)
    self.ui.label_pml_display_b_4.setStyleSheet(u"color: rgb(255, 0, 0);\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "QLabel{\n"
    "	font-family: \"Calibri\"\n"
    "}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_pml_display_b_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
    
    self.ui.verticalLayout_20_4.addWidget(self.ui.label_pml_display_b_4)
    
    self.ui.label_pml_display_c_4 = QLabel(self.ui.frame_pml_display_4)
    self.ui.label_pml_display_c_4.setObjectName(u"label_pml_display_c_4")
    self.ui.label_pml_display_c_4.setMinimumSize(QtCore.QSize(0, 70))
    self.ui.label_pml_display_c_4.setMaximumSize(QtCore.QSize(16777215, 70))
    self.ui.label_pml_display_c_4.setFont(font12)
    self.ui.label_pml_display_c_4.setStyleSheet(u"color: rgb(255, 0, 0);\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "QLabel{\n"
    "	font-family: \"Calibri\"\n"
    "}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_pml_display_c_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
    
    self.ui.verticalLayout_20_4.addWidget(self.ui.label_pml_display_c_4)
    
    self.ui.label_pml_display_d_4 = QLabel(self.ui.frame_pml_display_4)
    self.ui.label_pml_display_d_4.setObjectName(u"label_pml_display_d_4")
    self.ui.label_pml_display_d_4.setMinimumSize(QtCore.QSize(0, 70))
    self.ui.label_pml_display_d_4.setMaximumSize(QtCore.QSize(16777215, 70))
    self.ui.label_pml_display_d_4.setFont(font12)
    self.ui.label_pml_display_d_4.setStyleSheet(u"color: rgb(255, 0, 0);\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "QLabel{\n"
    "	font-family: \"Calibri\"\n"
    "}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_pml_display_d_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
    
    self.ui.verticalLayout_20_4.addWidget(self.ui.label_pml_display_d_4)
    
    
    self.ui.horizontalLayout_15_4.addWidget(self.ui.frame_pml_display_4)
    
    self.ui.frame_pml_display_4_select = QFrame(self.ui.frame_pml_contents_4)
    self.ui.frame_pml_display_4_select.setObjectName(u"frame_pml_display_select_4")
    self.ui.frame_pml_display_4_select.setMaximumSize(QtCore.QSize(100, 16777215))
    self.ui.frame_pml_display_4_select.setStyleSheet(u"QFrame{\n"
    "border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "}")
    self.ui.frame_pml_display_4_select.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_display_4_select.setFrameShadow(QFrame.Raised)
    self.verticalLayout_21 = QVBoxLayout(self.ui.frame_pml_display_4_select)
    self.verticalLayout_21.setSpacing(0)
    self.verticalLayout_21.setObjectName(u"verticalLayout_21")
    self.verticalLayout_21.setContentsMargins(0, 0, 0, 0)
    self.cbx_pml_display_a = QComboBox(self.ui.frame_pml_display_4_select)
    self.cbx_pml_display_a.setObjectName(u"cbx_pml_display_a")
    self.cbx_pml_display_a.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.verticalLayout_21.addWidget(self.cbx_pml_display_a)
    
    self.cbx_pml_display_b = QComboBox(self.ui.frame_pml_display_4_select)
    self.cbx_pml_display_b.setObjectName(u"cbx_pml_display_b")
    self.cbx_pml_display_b.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.verticalLayout_21.addWidget(self.cbx_pml_display_b)
    
    self.cbx_pml_display_c = QComboBox(self.ui.frame_pml_display_4_select)
    self.cbx_pml_display_c.setObjectName(u"cbx_pml_display_c")
    self.cbx_pml_display_c.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.verticalLayout_21.addWidget(self.cbx_pml_display_c)
    
    self.cbx_pml_display_d = QComboBox(self.ui.frame_pml_display_4_select)
    self.cbx_pml_display_d.setObjectName(u"cbx_pml_display_d")
    self.cbx_pml_display_d.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.verticalLayout_21.addWidget(self.cbx_pml_display_d)
    
    
    self.ui.horizontalLayout_15_4.addWidget(self.ui.frame_pml_display_4_select)
    
    self.ui.frame_pml_control_4 = QFrame(self.ui.frame_pml_contents_4)
    self.ui.frame_pml_control_4.setObjectName(u"frame_pml_control_4")
    self.ui.frame_pml_control_4.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "")
    self.ui.frame_pml_control_4.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_4.setFrameShadow(QFrame.Raised)
    self.verticalLayout_29 = QVBoxLayout(self.ui.frame_pml_control_4)
    self.verticalLayout_29.setSpacing(0)
    self.verticalLayout_29.setObjectName(u"verticalLayout_29")
    self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
    self.ui.frame_pml_control_4__range = QFrame(self.ui.frame_pml_control_4)
    self.ui.frame_pml_control_4__range.setObjectName(u"frame_pml_control__range")
    self.ui.frame_pml_control_4__range.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_4__range.setFrameShadow(QFrame.Raised)
    self.formLayout_2 = QFormLayout(self.ui.frame_pml_control_4__range)
    self.formLayout_2.setObjectName(u"formLayout_2")
    self.label_pml_voltage_range = QLabel(self.ui.frame_pml_control_4__range)
    self.label_pml_voltage_range.setObjectName(u"label_pml_voltage_range")
    self.label_pml_voltage_range.setFont(font10)
    self.label_pml_voltage_range.setStyleSheet(u"border:none;")
    
    self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_pml_voltage_range)
    
    self.cbx_pml_voltage_range = QComboBox(self.ui.frame_pml_control_4__range)
    self.cbx_pml_voltage_range.addItem("")
    self.cbx_pml_voltage_range.addItem("")
    self.cbx_pml_voltage_range.setObjectName(u"cbx_pml_voltage_range")
    self.cbx_pml_voltage_range.setMaximumSize(QtCore.QSize(16777215, 54))
    self.cbx_pml_voltage_range.setFont(font10)
    
    self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.cbx_pml_voltage_range)
    
    self.label_pml_current_range = QLabel(self.ui.frame_pml_control_4__range)
    self.label_pml_current_range.setObjectName(u"label_pml_current_range")
    self.label_pml_current_range.setFont(font10)
    self.label_pml_current_range.setStyleSheet(u"border:none;")
    
    self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_pml_current_range)
    
    self.cbx_pml_current_range = QComboBox(self.ui.frame_pml_control_4__range)
    self.cbx_pml_current_range.addItem("")
    self.cbx_pml_current_range.addItem("")
    self.cbx_pml_current_range.setObjectName(u"cbx_pml_current_range")
    self.cbx_pml_current_range.setMaximumSize(QtCore.QSize(16777215, 54))
    self.cbx_pml_current_range.setFont(font10)
    
    self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.cbx_pml_current_range)
    
    
    self.verticalLayout_29.addWidget(self.ui.frame_pml_control_4__range)
    
    self.ui.frame_pml_control_4_lower = QFrame(self.ui.frame_pml_control_4)
    self.ui.frame_pml_control_4_lower.setObjectName(u"frame_pml_control_lower")
    self.ui.frame_pml_control_4_lower.setStyleSheet(u"border:none;")
    self.ui.frame_pml_control_4_lower.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_4_lower.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_19_4 = QHBoxLayout(self.ui.frame_pml_control_4_lower)
    self.ui.horizontalLayout_19_4.setSpacing(0)
    self.ui.horizontalLayout_19_4.setObjectName(u"horizontalLayout_19_4")
    self.ui.horizontalLayout_19_4.setContentsMargins(0, 0, 0, 0)
    self.frame_pml_integration = QFrame(self.ui.frame_pml_control_4_lower)
    self.frame_pml_integration.setObjectName(u"frame_pml_integration")
    self.frame_pml_integration.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.frame_pml_integration.setFrameShape(QFrame.StyledPanel)
    self.frame_pml_integration.setFrameShadow(QFrame.Raised)
    self.verticalLayout_30 = QVBoxLayout(self.frame_pml_integration)
    self.verticalLayout_30.setObjectName(u"verticalLayout_30")
    self.label_pml_integration = QLabel(self.frame_pml_integration)
    self.label_pml_integration.setObjectName(u"label_pml_integration")
    sizePolicy.setHeightForWidth(self.label_pml_integration.sizePolicy().hasHeightForWidth())
    self.label_pml_integration.setSizePolicy(sizePolicy)
    self.label_pml_integration.setMinimumSize(QtCore.QSize(0, 20))
    self.label_pml_integration.setMaximumSize(QtCore.QSize(16777215, 20))
    self.label_pml_integration.setFont(font10)
    self.label_pml_integration.setStyleSheet(u"border:none;")
    
    self.verticalLayout_30.addWidget(self.label_pml_integration)
    
    self.btn_pml_integration_start = QPushButton(self.frame_pml_integration)
    self.btn_pml_integration_start.setObjectName(u"btn_pml_integration_start")
    self.btn_pml_integration_start.setFont(font10)
    self.btn_pml_integration_start.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}")
    
    self.verticalLayout_30.addWidget(self.btn_pml_integration_start)
    
    self.btn_pml_integration_stop = QPushButton(self.frame_pml_integration)
    self.btn_pml_integration_stop.setObjectName(u"btn_pml_integration_stop")
    self.btn_pml_integration_stop.setFont(font10)
    self.btn_pml_integration_stop.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}")
    
    self.verticalLayout_30.addWidget(self.btn_pml_integration_stop)
    
    self.btn_pml_integration_reset = QPushButton(self.frame_pml_integration)
    self.btn_pml_integration_reset.setObjectName(u"btn_pml_integration_reset")
    self.btn_pml_integration_reset.setFont(font10)
    self.btn_pml_integration_reset.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}")
    
    self.verticalLayout_30.addWidget(self.btn_pml_integration_reset)
    
    
    self.ui.horizontalLayout_19_4.addWidget(self.frame_pml_integration)
    
    self.frame_pml_averaging = QFrame(self.ui.frame_pml_control_4_lower)
    self.frame_pml_averaging.setObjectName(u"frame_pml_averaging")
    self.frame_pml_averaging.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.frame_pml_averaging.setFrameShape(QFrame.StyledPanel)
    self.frame_pml_averaging.setFrameShadow(QFrame.Raised)
    self.verticalLayout_31 = QVBoxLayout(self.frame_pml_averaging)
    self.verticalLayout_31.setSpacing(2)
    self.verticalLayout_31.setObjectName(u"verticalLayout_31")
    self.verticalLayout_31.setContentsMargins(-1, 5, -1, 5)
    self.label_pml_averaging = QLabel(self.frame_pml_averaging)
    self.label_pml_averaging.setObjectName(u"label_pml_averaging")
    sizePolicy.setHeightForWidth(self.label_pml_averaging.sizePolicy().hasHeightForWidth())
    self.label_pml_averaging.setSizePolicy(sizePolicy)
    self.label_pml_averaging.setMinimumSize(QtCore.QSize(0, 20))
    self.label_pml_averaging.setMaximumSize(QtCore.QSize(16777215, 20))
    self.label_pml_averaging.setFont(font10)
    self.label_pml_averaging.setStyleSheet(u"border:none;")
    
    self.verticalLayout_31.addWidget(self.label_pml_averaging)
    
    self.btn_pml_averaging_toggle = QPushButton(self.frame_pml_averaging)
    self.btn_pml_averaging_toggle.setObjectName(u"btn_pml_averaging_toggle")
    self.btn_pml_averaging_toggle.setFont(font10)
    self.btn_pml_averaging_toggle.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}")
    
    self.verticalLayout_31.addWidget(self.btn_pml_averaging_toggle)
    
    self.cbx_pml_averaging_count = QComboBox(self.frame_pml_averaging)
    self.cbx_pml_averaging_count.addItem("")
    self.cbx_pml_averaging_count.addItem("")
    self.cbx_pml_averaging_count.addItem("")
    self.cbx_pml_averaging_count.setObjectName(u"cbx_pml_averaging_count")
    self.cbx_pml_averaging_count.setMaximumSize(QtCore.QSize(16777215, 40))
    self.cbx_pml_averaging_count.setFont(font10)
    
    self.verticalLayout_31.addWidget(self.cbx_pml_averaging_count)
    
    self.cbx_pml_averaging_mode = QComboBox(self.frame_pml_averaging)
    self.cbx_pml_averaging_mode.addItem("")
    self.cbx_pml_averaging_mode.addItem("")
    self.cbx_pml_averaging_mode.setObjectName(u"cbx_pml_averaging_mode")
    self.cbx_pml_averaging_mode.setMaximumSize(QtCore.QSize(16777215, 40))
    self.cbx_pml_averaging_mode.setFont(font10)
    
    self.verticalLayout_31.addWidget(self.cbx_pml_averaging_mode)
    
    
    self.ui.horizontalLayout_19_4.addWidget(self.frame_pml_averaging)
    
    self.frame_pml_measure_mode = QFrame(self.ui.frame_pml_control_4_lower)
    self.frame_pml_measure_mode.setObjectName(u"frame_pml_measure_mode")
    self.frame_pml_measure_mode.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.frame_pml_measure_mode.setFrameShape(QFrame.StyledPanel)
    self.frame_pml_measure_mode.setFrameShadow(QFrame.Raised)
    self.verticalLayout_32 = QVBoxLayout(self.frame_pml_measure_mode)
    self.verticalLayout_32.setSpacing(13)
    self.verticalLayout_32.setObjectName(u"verticalLayout_32")
    self.verticalLayout_32.setContentsMargins(13, 13, 13, 13)
    self.label_pml_measure_mode = QLabel(self.frame_pml_measure_mode)
    self.label_pml_measure_mode.setObjectName(u"label_pml_measure_mode")
    sizePolicy.setHeightForWidth(self.label_pml_measure_mode.sizePolicy().hasHeightForWidth())
    self.label_pml_measure_mode.setSizePolicy(sizePolicy)
    self.label_pml_measure_mode.setMaximumSize(QtCore.QSize(16777215, 20))
    self.label_pml_measure_mode.setFont(font10)
    self.label_pml_measure_mode.setStyleSheet(u"border:none;")
    
    self.verticalLayout_32.addWidget(self.label_pml_measure_mode)
    
    self.btn_pml_measure_mode = QPushButton(self.frame_pml_measure_mode)
    self.btn_pml_measure_mode.setObjectName(u"btn_pml_measure_mode")
    self.btn_pml_measure_mode.setFont(font10)
    self.btn_pml_measure_mode.setStyleSheet(u"QPushButton {\n"
    "	border: 2px solid rgb(52, 59, 72);\n"
    "	border-radius: 5px;	\n"
    "	background-color: rgb(52, 59, 72);\n"
    "}\n"
    "QPushButton:hover {\n"
    "	background-color: rgb(57, 65, 80);\n"
    "	border: 2px solid rgb(61, 70, 86);\n"
    "}\n"
    "QPushButton:pressed {	\n"
    "	background-color: rgb(35, 40, 49);\n"
    "	border: 2px solid rgb(43, 50, 61);\n"
    "}")
    
    self.verticalLayout_32.addWidget(self.btn_pml_measure_mode)
    
    
    self.ui.horizontalLayout_19_4.addWidget(self.frame_pml_measure_mode)
    
    
    self.verticalLayout_29.addWidget(self.ui.frame_pml_control_4_lower)
    
    
    self.ui.horizontalLayout_15_4.addWidget(self.ui.frame_pml_control_4)
    
    
    self.ui.verticalLayout_19_4.addWidget(self.ui.frame_pml_contents_4)
    
    
    self.ui.horizontalLayout_9.addWidget(self.ui.frame_manual_control_pml_4)
