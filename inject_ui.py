from PySide2 import QtCore
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

def inject_ui(self):

    # --- SETUP TAB WIDGETS ---
    if not hasattr(self.ui, 'tabWidget_pml'):
        self.ui.tabWidget_pml = QTabWidget(self.ui.frame_manual_control_upper)
        self.ui.tabWidget_pml.setStyleSheet("QTabWidget::pane { border: 1px solid #3f4657; top: -1px; background-color: transparent; } QTabBar::tab { height: 30px; width: 100px; font-weight: bold; background-color: #1f232a; color: #8a95aa; border: 1px solid #3f4657; border-bottom: none; border-top-left-radius: 4px; border-top-right-radius: 4px; } QTabBar::tab:selected { background-color: #2c313c; color: white; }")
        idx_pml = self.ui.horizontalLayout_9.indexOf(self.ui.frame_manual_control_pml)
        self.ui.horizontalLayout_9.insertWidget(idx_pml, self.ui.tabWidget_pml)
        self.ui.tabWidget_pml.addTab(self.ui.frame_manual_control_pml, "CH 1")

    if not hasattr(self.ui, 'tabWidget_eload'):
        self.ui.tabWidget_eload = QTabWidget(self.ui.frame_manual_control_lower)
        self.ui.tabWidget_eload.setStyleSheet("QTabWidget::pane { border: 1px solid #3f4657; top: -1px; background-color: transparent; } QTabBar::tab { height: 30px; width: 100px; font-weight: bold; background-color: #1f232a; color: #8a95aa; border: 1px solid #3f4657; border-bottom: none; border-top-left-radius: 4px; border-top-right-radius: 4px; } QTabBar::tab:selected { background-color: #2c313c; color: white; }")
        idx_eload = self.ui.horizontalLayout_13.indexOf(self.ui.frame_manual_control_eload)
        self.ui.horizontalLayout_13.insertWidget(idx_eload, self.ui.tabWidget_eload)
        self.ui.tabWidget_eload.addTab(self.ui.frame_manual_control_eload, "CH 1")
    # -------------------------

    icon8 = QIcon()
    icon9 = QIcon()
    sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    sizePolicy11 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    sizePolicy19 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
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
    self.ui.frame_manual_control_eload_2.setMinimumSize(QtCore.QSize(300, 0))
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
    self.ui.frame_manual_control_eload_2_contents.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_2_contents.setObjectName(u"frame_manual_control_eload_contents_2")
    self.ui.frame_manual_control_eload_2_contents.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_contents.setFrameShadow(QFrame.Raised)
    self.verticalLayout_77_2 = QVBoxLayout(self.ui.frame_manual_control_eload_2_contents)
    self.verticalLayout_77_2.setObjectName(u"verticalLayout_77_2")
    self.ui.frame_manual_control_eload_2_top = QFrame(self.ui.frame_manual_control_eload_2_contents)
    self.ui.frame_manual_control_eload_2_top.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_2_top.setObjectName(u"frame_manual_control_eload_top_2")
    self.ui.frame_manual_control_eload_2_top.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_top.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_47_2 = QHBoxLayout(self.ui.frame_manual_control_eload_2_top)
    self.ui.horizontalLayout_47_2.setObjectName(u"horizontalLayout_47")
    self.ui.cbx_manual_control_eload_type_2 = QComboBox(self.ui.frame_manual_control_eload_2_top)
    self.ui.cbx_manual_control_eload_type_2.addItem("")
    self.ui.cbx_manual_control_eload_type_2.addItem("")
    self.ui.cbx_manual_control_eload_type_2.addItem("")
    self.ui.cbx_manual_control_eload_type_2.setObjectName(u"cbx_manual_control_eload_type")
    self.ui.cbx_manual_control_eload_type_2.setMaximumSize(QtCore.QSize(16777215, 40))
    self.ui.cbx_manual_control_eload_type_2.setFont(font10)
    self.ui.cbx_manual_control_eload_type_2.setStyleSheet(u"QComboBox{\n"
    "border: 2px solid black;\n"
    "border-radius:5px;\n"
    "}\n"
    "\n"
    "QComboBox:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    
    self.ui.horizontalLayout_47_2.addWidget(self.ui.cbx_manual_control_eload_type_2)
    
    self.ui.btn_manual_control_eload_a_b_swap_2 = QPushButton(self.ui.frame_manual_control_eload_2_top)
    self.ui.btn_manual_control_eload_a_b_swap_2.setObjectName(u"btn_manual_control_eload_a_b_swap_2")
    self.ui.btn_manual_control_eload_a_b_swap_2.setMinimumSize(QtCore.QSize(80, 40))
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
    
    self.ui.horizontalLayout_47_2.addWidget(self.ui.btn_manual_control_eload_a_b_swap_2)
    
    
    self.verticalLayout_77_2.addWidget(self.ui.frame_manual_control_eload_2_top)
    
    self.ui.frame_manual_control_eload_2_center = QFrame(self.ui.frame_manual_control_eload_2_contents)
    self.ui.frame_manual_control_eload_2_center.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_2_center.setObjectName(u"frame_manual_control_eload_center_2")
    self.ui.frame_manual_control_eload_2_center.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_center.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_46_2 = QHBoxLayout(self.ui.frame_manual_control_eload_2_center)
    self.ui.horizontalLayout_46_2.setObjectName(u"horizontalLayout_46")
    self.ui.frame_manual_control_eload_2_level = QFrame(self.ui.frame_manual_control_eload_2_center)
    self.ui.frame_manual_control_eload_2_level.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_2_level.setObjectName(u"frame_manual_control_eload_level_2")
    self.ui.frame_manual_control_eload_2_level.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_level.setFrameShadow(QFrame.Raised)
    self.verticalLayout_70_2 = QVBoxLayout(self.ui.frame_manual_control_eload_2_level)
    self.verticalLayout_70_2.setObjectName(u"verticalLayout_70_2")
    self.ui.frame_manual_control_eload_2_a = QFrame(self.ui.frame_manual_control_eload_2_level)
    self.ui.frame_manual_control_eload_2_a.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_2_a.setObjectName(u"frame_manual_control_eload_a_2")
    self.ui.frame_manual_control_eload_2_a.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_a.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_45_2 = QHBoxLayout(self.ui.frame_manual_control_eload_2_a)
    self.ui.horizontalLayout_45_2.setObjectName(u"horizontalLayout_45")
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
    
    self.ui.horizontalLayout_45_2.addWidget(self.ui.label_manual_control_eload_2_a)
    
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
    
    self.ui.horizontalLayout_45_2.addWidget(self.ui.lineedit_manual_control_eload_a_level_2)
    
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
    
    self.ui.horizontalLayout_45_2.addWidget(self.ui.label_manual_control_eload_2_a_level_unit)
    
    self.ui.btn_manual_control_eload_set_A_2 = QPushButton(self.ui.frame_manual_control_eload_2_a)
    self.ui.btn_manual_control_eload_set_A_2.setObjectName(u"btn_manual_control_eload_set_A")
    self.ui.btn_manual_control_eload_set_A_2.setMinimumSize(QtCore.QSize(50, 30))
    self.ui.btn_manual_control_eload_set_A_2.setFont(font4)
    self.ui.btn_manual_control_eload_set_A_2.setStyleSheet(u"QPushButton {\n"
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
    self.ui.btn_manual_control_eload_set_A_2.setCheckable(False)
    self.ui.btn_manual_control_eload_set_A_2.setChecked(False)
    
    self.ui.horizontalLayout_45_2.addWidget(self.ui.btn_manual_control_eload_set_A_2)
    
    
    self.verticalLayout_70_2.addWidget(self.ui.frame_manual_control_eload_2_a)
    
    self.ui.frame_manual_control_eload_2_b = QFrame(self.ui.frame_manual_control_eload_2_level)
    self.ui.frame_manual_control_eload_2_b.setStyleSheet(u"border:none;")
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
    
    self.ui.btn_manual_control_eload_set_B_2 = QPushButton(self.ui.frame_manual_control_eload_2_b)
    self.ui.btn_manual_control_eload_set_B_2.setObjectName(u"btn_manual_control_eload_set_B")
    self.ui.btn_manual_control_eload_set_B_2.setMinimumSize(QtCore.QSize(50, 30))
    self.ui.btn_manual_control_eload_set_B_2.setFont(font4)
    self.ui.btn_manual_control_eload_set_B_2.setStyleSheet(u"QPushButton {\n"
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
    self.ui.btn_manual_control_eload_set_B_2.setCheckable(False)
    self.ui.btn_manual_control_eload_set_B_2.setChecked(False)
    
    self.ui.horizontalLayout_39_2.addWidget(self.ui.btn_manual_control_eload_set_B_2)
    
    
    self.verticalLayout_70_2.addWidget(self.ui.frame_manual_control_eload_2_b)
    
    
    self.ui.horizontalLayout_46_2.addWidget(self.ui.frame_manual_control_eload_2_level)
    
    self.ui.frame_manual_control_eload_2_slew = QFrame(self.ui.frame_manual_control_eload_2_center)
    self.ui.frame_manual_control_eload_2_slew.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_2_slew.setObjectName(u"frame_manual_control_eload_slew_2")
    self.ui.frame_manual_control_eload_2_slew.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_slew.setFrameShadow(QFrame.Raised)
    self.gridLayout_29_2 = QGridLayout(self.ui.frame_manual_control_eload_2_slew)
    self.gridLayout_29_2.setObjectName(u"gridLayout_29_2")
    self.ui.frame_manual_control_eload_2_slew_fall = QFrame(self.ui.frame_manual_control_eload_2_slew)
    self.ui.frame_manual_control_eload_2_slew_fall.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_2_slew_fall.setObjectName(u"frame_manual_control_eload_slew_fall_2")
    self.ui.frame_manual_control_eload_2_slew_fall.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_slew_fall.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_38_2 = QHBoxLayout(self.ui.frame_manual_control_eload_2_slew_fall)
    self.ui.horizontalLayout_38_2.setObjectName(u"horizontalLayout_38_2")
    self.label_manual_control_electronic_load_fall_2 = QLabel(self.ui.frame_manual_control_eload_2_slew_fall)
    self.label_manual_control_electronic_load_fall_2.setObjectName(u"label_manual_control_electronic_load_fall_2")
    self.label_manual_control_electronic_load_fall_2.setMaximumSize(QtCore.QSize(16777215, 30))
    self.label_manual_control_electronic_load_fall_2.setFont(font10)
    self.label_manual_control_electronic_load_fall_2.setLayoutDirection(Qt.LeftToRight)
    self.label_manual_control_electronic_load_fall_2.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.label_manual_control_electronic_load_fall_2.setAlignment(Qt.AlignCenter)
    
    self.ui.horizontalLayout_38_2.addWidget(self.label_manual_control_electronic_load_fall_2)
    
    self.ui.lineedit_manual_control_eload_slew_fall_2 = QLineEdit(self.ui.frame_manual_control_eload_2_slew_fall)
    self.ui.lineedit_manual_control_eload_slew_fall_2.setObjectName(u"lineedit_manual_control_eload_slew_fall")
    sizePolicy21.setHeightForWidth(self.ui.lineedit_manual_control_eload_slew_fall_2.sizePolicy().hasHeightForWidth())
    self.ui.lineedit_manual_control_eload_slew_fall_2.setSizePolicy(sizePolicy21)
    self.ui.lineedit_manual_control_eload_slew_fall_2.setMinimumSize(QtCore.QSize(0, 40))
    self.ui.lineedit_manual_control_eload_slew_fall_2.setFont(font10)
    self.ui.lineedit_manual_control_eload_slew_fall_2.setStyleSheet(u"QLineEdit {\n"
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
    
    self.ui.horizontalLayout_38_2.addWidget(self.ui.lineedit_manual_control_eload_slew_fall_2)
    
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
    
    
    self.gridLayout_29_2.addWidget(self.ui.frame_manual_control_eload_2_slew_fall, 1, 0, 1, 1)
    
    self.ui.frame_manual_control_eload_2_slew_rise = QFrame(self.ui.frame_manual_control_eload_2_slew)
    self.ui.frame_manual_control_eload_2_slew_rise.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_2_slew_rise.setObjectName(u"frame_manual_control_eload_slew_rise_2")
    self.ui.frame_manual_control_eload_2_slew_rise.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_slew_rise.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_36_2 = QHBoxLayout(self.ui.frame_manual_control_eload_2_slew_rise)
    self.ui.horizontalLayout_36_2.setObjectName(u"horizontalLayout_36_2")
    self.label_manual_control_electronic_load_rise_2 = QLabel(self.ui.frame_manual_control_eload_2_slew_rise)
    self.label_manual_control_electronic_load_rise_2.setObjectName(u"label_manual_control_electronic_load_rise_2")
    self.label_manual_control_electronic_load_rise_2.setMaximumSize(QtCore.QSize(16777215, 30))
    self.label_manual_control_electronic_load_rise_2.setFont(font10)
    self.label_manual_control_electronic_load_rise_2.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.label_manual_control_electronic_load_rise_2.setAlignment(Qt.AlignCenter)
    
    self.ui.horizontalLayout_36_2.addWidget(self.label_manual_control_electronic_load_rise_2)
    
    self.ui.lineedit_manual_control_eload_slew_rise_2 = QLineEdit(self.ui.frame_manual_control_eload_2_slew_rise)
    self.ui.lineedit_manual_control_eload_slew_rise_2.setObjectName(u"lineedit_manual_control_eload_slew_rise")
    sizePolicy21.setHeightForWidth(self.ui.lineedit_manual_control_eload_slew_rise_2.sizePolicy().hasHeightForWidth())
    self.ui.lineedit_manual_control_eload_slew_rise_2.setSizePolicy(sizePolicy21)
    self.ui.lineedit_manual_control_eload_slew_rise_2.setMinimumSize(QtCore.QSize(0, 40))
    self.ui.lineedit_manual_control_eload_slew_rise_2.setFont(font10)
    self.ui.lineedit_manual_control_eload_slew_rise_2.setStyleSheet(u"QLineEdit {\n"
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
    
    self.ui.horizontalLayout_36_2.addWidget(self.ui.lineedit_manual_control_eload_slew_rise_2)
    
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
    
    
    self.gridLayout_29_2.addWidget(self.ui.frame_manual_control_eload_2_slew_rise, 0, 0, 1, 1)
    
    self.ui.btn_manual_control_eload_set_slew_2 = QPushButton(self.ui.frame_manual_control_eload_2_slew)
    self.ui.btn_manual_control_eload_set_slew_2.setObjectName(u"btn_manual_control_eload_set_slew")
    sizePolicy19.setHeightForWidth(self.ui.btn_manual_control_eload_set_slew_2.sizePolicy().hasHeightForWidth())
    self.ui.btn_manual_control_eload_set_slew_2.setSizePolicy(sizePolicy19)
    self.ui.btn_manual_control_eload_set_slew_2.setMinimumSize(QtCore.QSize(50, 60))
    self.ui.btn_manual_control_eload_set_slew_2.setFont(font4)
    self.ui.btn_manual_control_eload_set_slew_2.setStyleSheet(u"QPushButton {\n"
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
    self.ui.btn_manual_control_eload_set_slew_2.setCheckable(False)
    self.ui.btn_manual_control_eload_set_slew_2.setChecked(False)
    
    self.gridLayout_29_2.addWidget(self.ui.btn_manual_control_eload_set_slew_2, 0, 1, 2, 1)
    
    
    self.ui.horizontalLayout_46_2.addWidget(self.ui.frame_manual_control_eload_2_slew)
    
    
    self.verticalLayout_77_2.addWidget(self.ui.frame_manual_control_eload_2_center)
    
    self.ui.frame_manual_control_eload_2_bottom = QFrame(self.ui.frame_manual_control_eload_2_contents)
    self.ui.frame_manual_control_eload_2_bottom.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_2_bottom.setObjectName(u"frame_manual_control_eload_bottom_2")
    self.ui.frame_manual_control_eload_2_bottom.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_2_bottom.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_56_2 = QHBoxLayout(self.ui.frame_manual_control_eload_2_bottom)
    self.ui.horizontalLayout_56_2.setObjectName(u"horizontalLayout_56")
    self.ui.btn_manual_control_eload_turn_on_2 = QPushButton(self.ui.frame_manual_control_eload_2_bottom)
    self.ui.btn_manual_control_eload_turn_on_2.setObjectName(u"btn_manual_control_eload_turn_on")
    self.ui.btn_manual_control_eload_turn_on_2.setMinimumSize(QtCore.QSize(80, 40))
    self.ui.btn_manual_control_eload_turn_on_2.setFont(font13)
    self.ui.btn_manual_control_eload_turn_on_2.setStyleSheet(u"QPushButton {\n"
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
    self.ui.btn_manual_control_eload_turn_on_2.setIcon(icon8)
    self.ui.btn_manual_control_eload_turn_on_2.setCheckable(False)
    self.ui.btn_manual_control_eload_turn_on_2.setChecked(False)
    
    self.ui.horizontalLayout_56_2.addWidget(self.ui.btn_manual_control_eload_turn_on_2)
    
    self.ui.btn_manual_control_eload_turn_off_2 = QPushButton(self.ui.frame_manual_control_eload_2_bottom)
    self.ui.btn_manual_control_eload_turn_off_2.setObjectName(u"btn_manual_control_eload_turn_off")
    self.ui.btn_manual_control_eload_turn_off_2.setMinimumSize(QtCore.QSize(80, 40))
    self.ui.btn_manual_control_eload_turn_off_2.setFont(font13)
    self.ui.btn_manual_control_eload_turn_off_2.setStyleSheet(u"QPushButton {\n"
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
    self.ui.btn_manual_control_eload_turn_off_2.setIcon(icon9)
    self.ui.btn_manual_control_eload_turn_off_2.setCheckable(False)
    self.ui.btn_manual_control_eload_turn_off_2.setChecked(False)
    
    self.ui.horizontalLayout_56_2.addWidget(self.ui.btn_manual_control_eload_turn_off_2)
    
    
    self.verticalLayout_77_2.addWidget(self.ui.frame_manual_control_eload_2_bottom)
    
    
    self.ui.verticalLayout_23_2.addWidget(self.ui.frame_manual_control_eload_2_contents)
    
    
    self.ui.tabWidget_eload.addTab(self.ui.frame_manual_control_eload_2, 'CH 2')

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
    self.ui.label_load_power_meter_2 = QLabel(self.ui.frame_manual_control_pml_2)
    self.ui.label_load_power_meter_2.setObjectName(u"label_load_power_meter")
    self.ui.label_load_power_meter_2.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_load_power_meter_2.setFont(font1)
    self.ui.label_load_power_meter_2.setCursor(QCursor(Qt.ArrowCursor))
    self.ui.label_load_power_meter_2.setStyleSheet(u"QLabel{border:none;}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_load_power_meter_2.setAlignment(Qt.AlignCenter)
    
    self.ui.verticalLayout_19_2.addWidget(self.ui.label_load_power_meter_2)
    
    self.ui.frame_pml_contents_2 = QFrame(self.ui.frame_manual_control_pml_2)
    self.ui.frame_pml_contents_2.setStyleSheet(u"border:none;")
    self.ui.frame_pml_contents_2.setObjectName(u"frame_pml_contents_2")
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
    "\tfont: 700 24pt \"Segoe UI\";\n"
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
    "\tfont: 700 24pt \"Segoe UI\";\n"
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
    "\tfont: 700 24pt \"Segoe UI\";\n"
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
    "\tfont: 700 24pt \"Segoe UI\";\n"
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
    "\tfont: 700 24pt \"Segoe UI\";\n"
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
    self.ui.verticalLayout_21_2 = QVBoxLayout(self.ui.frame_pml_display_2_select)
    self.ui.verticalLayout_21_2.setSpacing(0)
    self.ui.verticalLayout_21_2.setObjectName(u"verticalLayout_21")
    self.ui.verticalLayout_21_2.setContentsMargins(0, 0, 0, 0)
    self.ui.cbx_pml_display_a_2 = QComboBox(self.ui.frame_pml_display_2_select)
    self.ui.cbx_pml_display_a_2.setObjectName(u"cbx_pml_display_a")
    self.ui.cbx_pml_display_a_2.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.ui.verticalLayout_21_2.addWidget(self.ui.cbx_pml_display_a_2)
    
    self.ui.cbx_pml_display_b_2 = QComboBox(self.ui.frame_pml_display_2_select)
    self.ui.cbx_pml_display_b_2.setObjectName(u"cbx_pml_display_b")
    self.ui.cbx_pml_display_b_2.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.ui.verticalLayout_21_2.addWidget(self.ui.cbx_pml_display_b_2)
    
    self.ui.cbx_pml_display_c_2 = QComboBox(self.ui.frame_pml_display_2_select)
    self.ui.cbx_pml_display_c_2.setObjectName(u"cbx_pml_display_c")
    self.ui.cbx_pml_display_c_2.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.ui.verticalLayout_21_2.addWidget(self.ui.cbx_pml_display_c_2)
    
    self.ui.cbx_pml_display_d_2 = QComboBox(self.ui.frame_pml_display_2_select)
    self.ui.cbx_pml_display_d_2.setObjectName(u"cbx_pml_display_d")
    self.ui.cbx_pml_display_d_2.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.ui.verticalLayout_21_2.addWidget(self.ui.cbx_pml_display_d_2)
    
    
    self.ui.horizontalLayout_15_2.addWidget(self.ui.frame_pml_display_2_select)
    
    self.ui.frame_pml_control_2 = QFrame(self.ui.frame_pml_contents_2)
    self.ui.frame_pml_control_2.setObjectName(u"frame_pml_control_2")
    self.ui.frame_pml_control_2.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "")
    self.ui.frame_pml_control_2.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_2.setFrameShadow(QFrame.Raised)
    self.ui.verticalLayout_29_2 = QVBoxLayout(self.ui.frame_pml_control_2)
    self.ui.verticalLayout_29_2.setSpacing(0)
    self.ui.verticalLayout_29_2.setObjectName(u"verticalLayout_29")
    self.ui.verticalLayout_29_2.setContentsMargins(0, 0, 0, 0)
    self.ui.frame_pml_control_2__range = QFrame(self.ui.frame_pml_control_2)
    self.ui.frame_pml_control_2__range.setStyleSheet(u"border:none;")
    self.ui.frame_pml_control_2__range.setObjectName(u"frame_pml_control__range")
    self.ui.frame_pml_control_2__range.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_2__range.setFrameShadow(QFrame.Raised)
    self.ui.formLayout_2_2 = QFormLayout(self.ui.frame_pml_control_2__range)
    self.ui.formLayout_2_2.setObjectName(u"formLayout_2")
    self.ui.label_pml_voltage_range_2 = QLabel(self.ui.frame_pml_control_2__range)
    self.ui.label_pml_voltage_range_2.setObjectName(u"label_pml_voltage_range")
    self.ui.label_pml_voltage_range_2.setFont(font10)
        
    self.ui.formLayout_2_2.setWidget(0, QFormLayout.LabelRole, self.ui.label_pml_voltage_range_2)
    
    self.ui.cbx_pml_voltage_range_2 = QComboBox(self.ui.frame_pml_control_2__range)
    self.ui.cbx_pml_voltage_range_2.addItem("")
    self.ui.cbx_pml_voltage_range_2.addItem("")
    self.ui.cbx_pml_voltage_range_2.setObjectName(u"cbx_pml_voltage_range")
    self.ui.cbx_pml_voltage_range_2.setMaximumSize(QtCore.QSize(16777215, 54))
    self.ui.cbx_pml_voltage_range_2.setFont(font10)
    
    self.ui.formLayout_2_2.setWidget(0, QFormLayout.FieldRole, self.ui.cbx_pml_voltage_range_2)
    
    self.ui.label_pml_current_range_2 = QLabel(self.ui.frame_pml_control_2__range)
    self.ui.label_pml_current_range_2.setObjectName(u"label_pml_current_range")
    self.ui.label_pml_current_range_2.setFont(font10)
        
    self.ui.formLayout_2_2.setWidget(1, QFormLayout.LabelRole, self.ui.label_pml_current_range_2)
    
    self.ui.cbx_pml_current_range_2 = QComboBox(self.ui.frame_pml_control_2__range)
    self.ui.cbx_pml_current_range_2.addItem("")
    self.ui.cbx_pml_current_range_2.addItem("")
    self.ui.cbx_pml_current_range_2.setObjectName(u"cbx_pml_current_range")
    self.ui.cbx_pml_current_range_2.setMaximumSize(QtCore.QSize(16777215, 54))
    self.ui.cbx_pml_current_range_2.setFont(font10)
    
    self.ui.formLayout_2_2.setWidget(1, QFormLayout.FieldRole, self.ui.cbx_pml_current_range_2)
    
    
    self.ui.verticalLayout_29_2.addWidget(self.ui.frame_pml_control_2__range)
    
    self.ui.frame_pml_control_2_lower = QFrame(self.ui.frame_pml_control_2)
    self.ui.frame_pml_control_2_lower.setStyleSheet(u"border:none;")
    self.ui.frame_pml_control_2_lower.setObjectName(u"frame_pml_control_lower")
    self.ui.frame_pml_control_2_lower.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_2_lower.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_19_2 = QHBoxLayout(self.ui.frame_pml_control_2_lower)
    self.ui.horizontalLayout_19_2.setSpacing(0)
    self.ui.horizontalLayout_19_2.setObjectName(u"horizontalLayout_19_2")
    self.ui.horizontalLayout_19_2.setContentsMargins(0, 0, 0, 0)
    self.ui.frame_pml_integration_2 = QFrame(self.ui.frame_pml_control_2_lower)
    self.ui.frame_pml_integration_2.setObjectName(u"frame_pml_integration")
    self.ui.frame_pml_integration_2.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.ui.frame_pml_integration_2.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_integration_2.setFrameShadow(QFrame.Raised)
    self.verticalLayout_30_2 = QVBoxLayout(self.ui.frame_pml_integration_2)
    self.verticalLayout_30_2.setObjectName(u"verticalLayout_30_2")
    self.ui.label_pml_integration_2 = QLabel(self.ui.frame_pml_integration_2)
    self.ui.label_pml_integration_2.setObjectName(u"label_pml_integration")
    sizePolicy.setHeightForWidth(self.ui.label_pml_integration_2.sizePolicy().hasHeightForWidth())
    self.ui.label_pml_integration_2.setSizePolicy(sizePolicy)
    self.ui.label_pml_integration_2.setMinimumSize(QtCore.QSize(0, 20))
    self.ui.label_pml_integration_2.setMaximumSize(QtCore.QSize(16777215, 20))
    self.ui.label_pml_integration_2.setFont(font10)
        
    self.verticalLayout_30_2.addWidget(self.ui.label_pml_integration_2)
    
    self.btn_pml_integration_start_2 = QPushButton(self.ui.frame_pml_integration_2)
    self.btn_pml_integration_start_2.setObjectName(u"btn_pml_integration_start_2")
    self.btn_pml_integration_start_2.setFont(font10)
    self.btn_pml_integration_start_2.setStyleSheet(u"QPushButton {\n"
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
    
    self.verticalLayout_30_2.addWidget(self.btn_pml_integration_start_2)
    
    self.btn_pml_integration_stop_2 = QPushButton(self.ui.frame_pml_integration_2)
    self.btn_pml_integration_stop_2.setObjectName(u"btn_pml_integration_stop_2")
    self.btn_pml_integration_stop_2.setFont(font10)
    self.btn_pml_integration_stop_2.setStyleSheet(u"QPushButton {\n"
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
    
    self.verticalLayout_30_2.addWidget(self.btn_pml_integration_stop_2)
    
    self.btn_pml_integration_reset_2 = QPushButton(self.ui.frame_pml_integration_2)
    self.btn_pml_integration_reset_2.setObjectName(u"btn_pml_integration_reset_2")
    self.btn_pml_integration_reset_2.setFont(font10)
    self.btn_pml_integration_reset_2.setStyleSheet(u"QPushButton {\n"
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
    
    self.verticalLayout_30_2.addWidget(self.btn_pml_integration_reset_2)
    
    
    self.ui.horizontalLayout_19_2.addWidget(self.ui.frame_pml_integration_2)
    
    self.ui.frame_pml_averaging_2 = QFrame(self.ui.frame_pml_control_2_lower)
    self.ui.frame_pml_averaging_2.setObjectName(u"frame_pml_averaging")
    self.ui.frame_pml_averaging_2.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.ui.frame_pml_averaging_2.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_averaging_2.setFrameShadow(QFrame.Raised)
    self.verticalLayout_31_2 = QVBoxLayout(self.ui.frame_pml_averaging_2)
    self.verticalLayout_31_2.setSpacing(2)
    self.verticalLayout_31_2.setObjectName(u"verticalLayout_31_2")
    self.verticalLayout_31_2.setContentsMargins(-1, 5, -1, 5)
    self.ui.label_pml_averaging_2 = QLabel(self.ui.frame_pml_averaging_2)
    self.ui.label_pml_averaging_2.setObjectName(u"label_pml_averaging")
    sizePolicy.setHeightForWidth(self.ui.label_pml_averaging_2.sizePolicy().hasHeightForWidth())
    self.ui.label_pml_averaging_2.setSizePolicy(sizePolicy)
    self.ui.label_pml_averaging_2.setMinimumSize(QtCore.QSize(0, 20))
    self.ui.label_pml_averaging_2.setMaximumSize(QtCore.QSize(16777215, 20))
    self.ui.label_pml_averaging_2.setFont(font10)
        
    self.verticalLayout_31_2.addWidget(self.ui.label_pml_averaging_2)
    
    self.btn_pml_averaging_toggle_2 = QPushButton(self.ui.frame_pml_averaging_2)
    self.btn_pml_averaging_toggle_2.setObjectName(u"btn_pml_averaging_toggle_2")
    self.btn_pml_averaging_toggle_2.setFont(font10)
    self.btn_pml_averaging_toggle_2.setStyleSheet(u"QPushButton {\n"
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
    
    self.verticalLayout_31_2.addWidget(self.btn_pml_averaging_toggle_2)
    
    self.cbx_pml_averaging_count_2 = QComboBox(self.ui.frame_pml_averaging_2)
    self.cbx_pml_averaging_count_2.addItem("")
    self.cbx_pml_averaging_count_2.addItem("")
    self.cbx_pml_averaging_count_2.addItem("")
    self.cbx_pml_averaging_count_2.setObjectName(u"cbx_pml_averaging_count_2")
    self.cbx_pml_averaging_count_2.setMaximumSize(QtCore.QSize(16777215, 40))
    self.cbx_pml_averaging_count_2.setFont(font10)
    
    self.verticalLayout_31_2.addWidget(self.cbx_pml_averaging_count_2)
    
    self.cbx_pml_averaging_mode_2 = QComboBox(self.ui.frame_pml_averaging_2)
    self.cbx_pml_averaging_mode_2.addItem("")
    self.cbx_pml_averaging_mode_2.addItem("")
    self.cbx_pml_averaging_mode_2.setObjectName(u"cbx_pml_averaging_mode_2")
    self.cbx_pml_averaging_mode_2.setMaximumSize(QtCore.QSize(16777215, 40))
    self.cbx_pml_averaging_mode_2.setFont(font10)
    
    self.verticalLayout_31_2.addWidget(self.cbx_pml_averaging_mode_2)
    
    
    self.ui.horizontalLayout_19_2.addWidget(self.ui.frame_pml_averaging_2)
    
    self.ui.frame_pml_measure_mode_2 = QFrame(self.ui.frame_pml_control_2_lower)
    self.ui.frame_pml_measure_mode_2.setObjectName(u"frame_pml_measure_mode")
    self.ui.frame_pml_measure_mode_2.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.ui.frame_pml_measure_mode_2.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_measure_mode_2.setFrameShadow(QFrame.Raised)
    self.ui.verticalLayout_32_2 = QVBoxLayout(self.ui.frame_pml_measure_mode_2)
    self.ui.verticalLayout_32_2.setSpacing(13)
    self.ui.verticalLayout_32_2.setObjectName(u"verticalLayout_32")
    self.ui.verticalLayout_32_2.setContentsMargins(13, 13, 13, 13)
    self.ui.label_pml_measure_mode_2 = QLabel(self.ui.frame_pml_measure_mode_2)
    self.ui.label_pml_measure_mode_2.setObjectName(u"label_pml_measure_mode")
    sizePolicy.setHeightForWidth(self.ui.label_pml_measure_mode_2.sizePolicy().hasHeightForWidth())
    self.ui.label_pml_measure_mode_2.setSizePolicy(sizePolicy)
    self.ui.label_pml_measure_mode_2.setMaximumSize(QtCore.QSize(16777215, 20))
    self.ui.label_pml_measure_mode_2.setFont(font10)
        
    self.ui.verticalLayout_32_2.addWidget(self.ui.label_pml_measure_mode_2)
    
    self.ui.btn_pml_measure_mode_2 = QPushButton(self.ui.frame_pml_measure_mode_2)
    self.ui.btn_pml_measure_mode_2.setObjectName(u"btn_pml_measure_mode")
    self.ui.btn_pml_measure_mode_2.setFont(font10)
    self.ui.btn_pml_measure_mode_2.setStyleSheet(u"QPushButton {\n"
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
    
    self.ui.verticalLayout_32_2.addWidget(self.ui.btn_pml_measure_mode_2)
    
    
    self.ui.horizontalLayout_19_2.addWidget(self.ui.frame_pml_measure_mode_2)
    
    
    self.ui.verticalLayout_29_2.addWidget(self.ui.frame_pml_control_2_lower)
    
    
    self.ui.horizontalLayout_15_2.addWidget(self.ui.frame_pml_control_2)
    
    
    self.ui.verticalLayout_19_2.addWidget(self.ui.frame_pml_contents_2)
    
    
    self.ui.tabWidget_pml.addTab(self.ui.frame_manual_control_pml_2, 'CH 2')

    # ELOAD 3
    self.ui.frame_manual_control_eload_3 = QFrame(self.ui.frame_manual_control_lower)
    self.ui.frame_manual_control_eload_3.setObjectName(u"frame_manual_control_eload_3")
    sizePolicy20 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
    sizePolicy20.setHorizontalStretch(3)
    sizePolicy20.setVerticalStretch(0)
    sizePolicy20.setHeightForWidth(self.ui.frame_manual_control_eload_3.sizePolicy().hasHeightForWidth())
    self.ui.frame_manual_control_eload_3.setSizePolicy(sizePolicy20)
    self.ui.frame_manual_control_eload_3.setMinimumSize(QtCore.QSize(300, 0))
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
    self.ui.frame_manual_control_eload_3_contents.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_3_contents.setObjectName(u"frame_manual_control_eload_contents_3")
    self.ui.frame_manual_control_eload_3_contents.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_contents.setFrameShadow(QFrame.Raised)
    self.verticalLayout_77_3 = QVBoxLayout(self.ui.frame_manual_control_eload_3_contents)
    self.verticalLayout_77_3.setObjectName(u"verticalLayout_77_3")
    self.ui.frame_manual_control_eload_3_top = QFrame(self.ui.frame_manual_control_eload_3_contents)
    self.ui.frame_manual_control_eload_3_top.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_3_top.setObjectName(u"frame_manual_control_eload_top_3")
    self.ui.frame_manual_control_eload_3_top.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_top.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_47_3 = QHBoxLayout(self.ui.frame_manual_control_eload_3_top)
    self.ui.horizontalLayout_47_3.setObjectName(u"horizontalLayout_47")
    self.ui.cbx_manual_control_eload_type_3 = QComboBox(self.ui.frame_manual_control_eload_3_top)
    self.ui.cbx_manual_control_eload_type_3.addItem("")
    self.ui.cbx_manual_control_eload_type_3.addItem("")
    self.ui.cbx_manual_control_eload_type_3.addItem("")
    self.ui.cbx_manual_control_eload_type_3.setObjectName(u"cbx_manual_control_eload_type")
    self.ui.cbx_manual_control_eload_type_3.setMaximumSize(QtCore.QSize(16777215, 40))
    self.ui.cbx_manual_control_eload_type_3.setFont(font10)
    self.ui.cbx_manual_control_eload_type_3.setStyleSheet(u"QComboBox{\n"
    "border: 2px solid black;\n"
    "border-radius:5px;\n"
    "}\n"
    "\n"
    "QComboBox:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    
    self.ui.horizontalLayout_47_3.addWidget(self.ui.cbx_manual_control_eload_type_3)
    
    self.ui.btn_manual_control_eload_a_b_swap_3 = QPushButton(self.ui.frame_manual_control_eload_3_top)
    self.ui.btn_manual_control_eload_a_b_swap_3.setObjectName(u"btn_manual_control_eload_a_b_swap_3")
    self.ui.btn_manual_control_eload_a_b_swap_3.setMinimumSize(QtCore.QSize(80, 40))
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
    
    self.ui.horizontalLayout_47_3.addWidget(self.ui.btn_manual_control_eload_a_b_swap_3)
    
    
    self.verticalLayout_77_3.addWidget(self.ui.frame_manual_control_eload_3_top)
    
    self.ui.frame_manual_control_eload_3_center = QFrame(self.ui.frame_manual_control_eload_3_contents)
    self.ui.frame_manual_control_eload_3_center.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_3_center.setObjectName(u"frame_manual_control_eload_center_3")
    self.ui.frame_manual_control_eload_3_center.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_center.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_46_3 = QHBoxLayout(self.ui.frame_manual_control_eload_3_center)
    self.ui.horizontalLayout_46_3.setObjectName(u"horizontalLayout_46")
    self.ui.frame_manual_control_eload_3_level = QFrame(self.ui.frame_manual_control_eload_3_center)
    self.ui.frame_manual_control_eload_3_level.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_3_level.setObjectName(u"frame_manual_control_eload_level_3")
    self.ui.frame_manual_control_eload_3_level.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_level.setFrameShadow(QFrame.Raised)
    self.verticalLayout_70_3 = QVBoxLayout(self.ui.frame_manual_control_eload_3_level)
    self.verticalLayout_70_3.setObjectName(u"verticalLayout_70_3")
    self.ui.frame_manual_control_eload_3_a = QFrame(self.ui.frame_manual_control_eload_3_level)
    self.ui.frame_manual_control_eload_3_a.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_3_a.setObjectName(u"frame_manual_control_eload_a_3")
    self.ui.frame_manual_control_eload_3_a.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_a.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_45_3 = QHBoxLayout(self.ui.frame_manual_control_eload_3_a)
    self.ui.horizontalLayout_45_3.setObjectName(u"horizontalLayout_45")
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
    
    self.ui.horizontalLayout_45_3.addWidget(self.ui.label_manual_control_eload_3_a)
    
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
    
    self.ui.horizontalLayout_45_3.addWidget(self.ui.lineedit_manual_control_eload_a_level_3)
    
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
    
    self.ui.horizontalLayout_45_3.addWidget(self.ui.label_manual_control_eload_3_a_level_unit)
    
    self.ui.btn_manual_control_eload_set_A_3 = QPushButton(self.ui.frame_manual_control_eload_3_a)
    self.ui.btn_manual_control_eload_set_A_3.setObjectName(u"btn_manual_control_eload_set_A")
    self.ui.btn_manual_control_eload_set_A_3.setMinimumSize(QtCore.QSize(50, 30))
    self.ui.btn_manual_control_eload_set_A_3.setFont(font4)
    self.ui.btn_manual_control_eload_set_A_3.setStyleSheet(u"QPushButton {\n"
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
    self.ui.btn_manual_control_eload_set_A_3.setCheckable(False)
    self.ui.btn_manual_control_eload_set_A_3.setChecked(False)
    
    self.ui.horizontalLayout_45_3.addWidget(self.ui.btn_manual_control_eload_set_A_3)
    
    
    self.verticalLayout_70_3.addWidget(self.ui.frame_manual_control_eload_3_a)
    
    self.ui.frame_manual_control_eload_3_b = QFrame(self.ui.frame_manual_control_eload_3_level)
    self.ui.frame_manual_control_eload_3_b.setStyleSheet(u"border:none;")
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
    
    self.ui.btn_manual_control_eload_set_B_3 = QPushButton(self.ui.frame_manual_control_eload_3_b)
    self.ui.btn_manual_control_eload_set_B_3.setObjectName(u"btn_manual_control_eload_set_B")
    self.ui.btn_manual_control_eload_set_B_3.setMinimumSize(QtCore.QSize(50, 30))
    self.ui.btn_manual_control_eload_set_B_3.setFont(font4)
    self.ui.btn_manual_control_eload_set_B_3.setStyleSheet(u"QPushButton {\n"
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
    self.ui.btn_manual_control_eload_set_B_3.setCheckable(False)
    self.ui.btn_manual_control_eload_set_B_3.setChecked(False)
    
    self.ui.horizontalLayout_39_3.addWidget(self.ui.btn_manual_control_eload_set_B_3)
    
    
    self.verticalLayout_70_3.addWidget(self.ui.frame_manual_control_eload_3_b)
    
    
    self.ui.horizontalLayout_46_3.addWidget(self.ui.frame_manual_control_eload_3_level)
    
    self.ui.frame_manual_control_eload_3_slew = QFrame(self.ui.frame_manual_control_eload_3_center)
    self.ui.frame_manual_control_eload_3_slew.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_3_slew.setObjectName(u"frame_manual_control_eload_slew_3")
    self.ui.frame_manual_control_eload_3_slew.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_slew.setFrameShadow(QFrame.Raised)
    self.gridLayout_29_3 = QGridLayout(self.ui.frame_manual_control_eload_3_slew)
    self.gridLayout_29_3.setObjectName(u"gridLayout_29_3")
    self.ui.frame_manual_control_eload_3_slew_fall = QFrame(self.ui.frame_manual_control_eload_3_slew)
    self.ui.frame_manual_control_eload_3_slew_fall.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_3_slew_fall.setObjectName(u"frame_manual_control_eload_slew_fall_3")
    self.ui.frame_manual_control_eload_3_slew_fall.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_slew_fall.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_38_3 = QHBoxLayout(self.ui.frame_manual_control_eload_3_slew_fall)
    self.ui.horizontalLayout_38_3.setObjectName(u"horizontalLayout_38_3")
    self.label_manual_control_electronic_load_fall_3 = QLabel(self.ui.frame_manual_control_eload_3_slew_fall)
    self.label_manual_control_electronic_load_fall_3.setObjectName(u"label_manual_control_electronic_load_fall_3")
    self.label_manual_control_electronic_load_fall_3.setMaximumSize(QtCore.QSize(16777215, 30))
    self.label_manual_control_electronic_load_fall_3.setFont(font10)
    self.label_manual_control_electronic_load_fall_3.setLayoutDirection(Qt.LeftToRight)
    self.label_manual_control_electronic_load_fall_3.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.label_manual_control_electronic_load_fall_3.setAlignment(Qt.AlignCenter)
    
    self.ui.horizontalLayout_38_3.addWidget(self.label_manual_control_electronic_load_fall_3)
    
    self.ui.lineedit_manual_control_eload_slew_fall_3 = QLineEdit(self.ui.frame_manual_control_eload_3_slew_fall)
    self.ui.lineedit_manual_control_eload_slew_fall_3.setObjectName(u"lineedit_manual_control_eload_slew_fall")
    sizePolicy21.setHeightForWidth(self.ui.lineedit_manual_control_eload_slew_fall_3.sizePolicy().hasHeightForWidth())
    self.ui.lineedit_manual_control_eload_slew_fall_3.setSizePolicy(sizePolicy21)
    self.ui.lineedit_manual_control_eload_slew_fall_3.setMinimumSize(QtCore.QSize(0, 40))
    self.ui.lineedit_manual_control_eload_slew_fall_3.setFont(font10)
    self.ui.lineedit_manual_control_eload_slew_fall_3.setStyleSheet(u"QLineEdit {\n"
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
    
    self.ui.horizontalLayout_38_3.addWidget(self.ui.lineedit_manual_control_eload_slew_fall_3)
    
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
    
    
    self.gridLayout_29_3.addWidget(self.ui.frame_manual_control_eload_3_slew_fall, 1, 0, 1, 1)
    
    self.ui.frame_manual_control_eload_3_slew_rise = QFrame(self.ui.frame_manual_control_eload_3_slew)
    self.ui.frame_manual_control_eload_3_slew_rise.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_3_slew_rise.setObjectName(u"frame_manual_control_eload_slew_rise_3")
    self.ui.frame_manual_control_eload_3_slew_rise.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_slew_rise.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_36_3 = QHBoxLayout(self.ui.frame_manual_control_eload_3_slew_rise)
    self.ui.horizontalLayout_36_3.setObjectName(u"horizontalLayout_36_3")
    self.label_manual_control_electronic_load_rise_3 = QLabel(self.ui.frame_manual_control_eload_3_slew_rise)
    self.label_manual_control_electronic_load_rise_3.setObjectName(u"label_manual_control_electronic_load_rise_3")
    self.label_manual_control_electronic_load_rise_3.setMaximumSize(QtCore.QSize(16777215, 30))
    self.label_manual_control_electronic_load_rise_3.setFont(font10)
    self.label_manual_control_electronic_load_rise_3.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.label_manual_control_electronic_load_rise_3.setAlignment(Qt.AlignCenter)
    
    self.ui.horizontalLayout_36_3.addWidget(self.label_manual_control_electronic_load_rise_3)
    
    self.ui.lineedit_manual_control_eload_slew_rise_3 = QLineEdit(self.ui.frame_manual_control_eload_3_slew_rise)
    self.ui.lineedit_manual_control_eload_slew_rise_3.setObjectName(u"lineedit_manual_control_eload_slew_rise")
    sizePolicy21.setHeightForWidth(self.ui.lineedit_manual_control_eload_slew_rise_3.sizePolicy().hasHeightForWidth())
    self.ui.lineedit_manual_control_eload_slew_rise_3.setSizePolicy(sizePolicy21)
    self.ui.lineedit_manual_control_eload_slew_rise_3.setMinimumSize(QtCore.QSize(0, 40))
    self.ui.lineedit_manual_control_eload_slew_rise_3.setFont(font10)
    self.ui.lineedit_manual_control_eload_slew_rise_3.setStyleSheet(u"QLineEdit {\n"
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
    
    self.ui.horizontalLayout_36_3.addWidget(self.ui.lineedit_manual_control_eload_slew_rise_3)
    
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
    
    
    self.gridLayout_29_3.addWidget(self.ui.frame_manual_control_eload_3_slew_rise, 0, 0, 1, 1)
    
    self.ui.btn_manual_control_eload_set_slew_3 = QPushButton(self.ui.frame_manual_control_eload_3_slew)
    self.ui.btn_manual_control_eload_set_slew_3.setObjectName(u"btn_manual_control_eload_set_slew")
    sizePolicy19.setHeightForWidth(self.ui.btn_manual_control_eload_set_slew_3.sizePolicy().hasHeightForWidth())
    self.ui.btn_manual_control_eload_set_slew_3.setSizePolicy(sizePolicy19)
    self.ui.btn_manual_control_eload_set_slew_3.setMinimumSize(QtCore.QSize(50, 60))
    self.ui.btn_manual_control_eload_set_slew_3.setFont(font4)
    self.ui.btn_manual_control_eload_set_slew_3.setStyleSheet(u"QPushButton {\n"
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
    self.ui.btn_manual_control_eload_set_slew_3.setCheckable(False)
    self.ui.btn_manual_control_eload_set_slew_3.setChecked(False)
    
    self.gridLayout_29_3.addWidget(self.ui.btn_manual_control_eload_set_slew_3, 0, 1, 2, 1)
    
    
    self.ui.horizontalLayout_46_3.addWidget(self.ui.frame_manual_control_eload_3_slew)
    
    
    self.verticalLayout_77_3.addWidget(self.ui.frame_manual_control_eload_3_center)
    
    self.ui.frame_manual_control_eload_3_bottom = QFrame(self.ui.frame_manual_control_eload_3_contents)
    self.ui.frame_manual_control_eload_3_bottom.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_3_bottom.setObjectName(u"frame_manual_control_eload_bottom_3")
    self.ui.frame_manual_control_eload_3_bottom.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_3_bottom.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_56_3 = QHBoxLayout(self.ui.frame_manual_control_eload_3_bottom)
    self.ui.horizontalLayout_56_3.setObjectName(u"horizontalLayout_56")
    self.ui.btn_manual_control_eload_turn_on_3 = QPushButton(self.ui.frame_manual_control_eload_3_bottom)
    self.ui.btn_manual_control_eload_turn_on_3.setObjectName(u"btn_manual_control_eload_turn_on")
    self.ui.btn_manual_control_eload_turn_on_3.setMinimumSize(QtCore.QSize(80, 40))
    self.ui.btn_manual_control_eload_turn_on_3.setFont(font13)
    self.ui.btn_manual_control_eload_turn_on_3.setStyleSheet(u"QPushButton {\n"
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
    self.ui.btn_manual_control_eload_turn_on_3.setIcon(icon8)
    self.ui.btn_manual_control_eload_turn_on_3.setCheckable(False)
    self.ui.btn_manual_control_eload_turn_on_3.setChecked(False)
    
    self.ui.horizontalLayout_56_3.addWidget(self.ui.btn_manual_control_eload_turn_on_3)
    
    self.ui.btn_manual_control_eload_turn_off_3 = QPushButton(self.ui.frame_manual_control_eload_3_bottom)
    self.ui.btn_manual_control_eload_turn_off_3.setObjectName(u"btn_manual_control_eload_turn_off")
    self.ui.btn_manual_control_eload_turn_off_3.setMinimumSize(QtCore.QSize(80, 40))
    self.ui.btn_manual_control_eload_turn_off_3.setFont(font13)
    self.ui.btn_manual_control_eload_turn_off_3.setStyleSheet(u"QPushButton {\n"
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
    self.ui.btn_manual_control_eload_turn_off_3.setIcon(icon9)
    self.ui.btn_manual_control_eload_turn_off_3.setCheckable(False)
    self.ui.btn_manual_control_eload_turn_off_3.setChecked(False)
    
    self.ui.horizontalLayout_56_3.addWidget(self.ui.btn_manual_control_eload_turn_off_3)
    
    
    self.verticalLayout_77_3.addWidget(self.ui.frame_manual_control_eload_3_bottom)
    
    
    self.ui.verticalLayout_23_3.addWidget(self.ui.frame_manual_control_eload_3_contents)
    
    
    self.ui.tabWidget_eload.addTab(self.ui.frame_manual_control_eload_3, 'CH 3')

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
    self.ui.label_load_power_meter_3 = QLabel(self.ui.frame_manual_control_pml_3)
    self.ui.label_load_power_meter_3.setObjectName(u"label_load_power_meter")
    self.ui.label_load_power_meter_3.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_load_power_meter_3.setFont(font1)
    self.ui.label_load_power_meter_3.setCursor(QCursor(Qt.ArrowCursor))
    self.ui.label_load_power_meter_3.setStyleSheet(u"QLabel{border:none;}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_load_power_meter_3.setAlignment(Qt.AlignCenter)
    
    self.ui.verticalLayout_19_3.addWidget(self.ui.label_load_power_meter_3)
    
    self.ui.frame_pml_contents_3 = QFrame(self.ui.frame_manual_control_pml_3)
    self.ui.frame_pml_contents_3.setStyleSheet(u"border:none;")
    self.ui.frame_pml_contents_3.setObjectName(u"frame_pml_contents_3")
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
    "\tfont: 700 24pt \"Segoe UI\";\n"
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
    "\tfont: 700 24pt \"Segoe UI\";\n"
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
    "\tfont: 700 24pt \"Segoe UI\";\n"
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
    "\tfont: 700 24pt \"Segoe UI\";\n"
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
    "\tfont: 700 24pt \"Segoe UI\";\n"
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
    self.ui.verticalLayout_21_3 = QVBoxLayout(self.ui.frame_pml_display_3_select)
    self.ui.verticalLayout_21_3.setSpacing(0)
    self.ui.verticalLayout_21_3.setObjectName(u"verticalLayout_21")
    self.ui.verticalLayout_21_3.setContentsMargins(0, 0, 0, 0)
    self.ui.cbx_pml_display_a_3 = QComboBox(self.ui.frame_pml_display_3_select)
    self.ui.cbx_pml_display_a_3.setObjectName(u"cbx_pml_display_a")
    self.ui.cbx_pml_display_a_3.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.ui.verticalLayout_21_3.addWidget(self.ui.cbx_pml_display_a_3)
    
    self.ui.cbx_pml_display_b_3 = QComboBox(self.ui.frame_pml_display_3_select)
    self.ui.cbx_pml_display_b_3.setObjectName(u"cbx_pml_display_b")
    self.ui.cbx_pml_display_b_3.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.ui.verticalLayout_21_3.addWidget(self.ui.cbx_pml_display_b_3)
    
    self.ui.cbx_pml_display_c_3 = QComboBox(self.ui.frame_pml_display_3_select)
    self.ui.cbx_pml_display_c_3.setObjectName(u"cbx_pml_display_c")
    self.ui.cbx_pml_display_c_3.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.ui.verticalLayout_21_3.addWidget(self.ui.cbx_pml_display_c_3)
    
    self.ui.cbx_pml_display_d_3 = QComboBox(self.ui.frame_pml_display_3_select)
    self.ui.cbx_pml_display_d_3.setObjectName(u"cbx_pml_display_d")
    self.ui.cbx_pml_display_d_3.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.ui.verticalLayout_21_3.addWidget(self.ui.cbx_pml_display_d_3)
    
    
    self.ui.horizontalLayout_15_3.addWidget(self.ui.frame_pml_display_3_select)
    
    self.ui.frame_pml_control_3 = QFrame(self.ui.frame_pml_contents_3)
    self.ui.frame_pml_control_3.setObjectName(u"frame_pml_control_3")
    self.ui.frame_pml_control_3.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "")
    self.ui.frame_pml_control_3.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_3.setFrameShadow(QFrame.Raised)
    self.ui.verticalLayout_29_3 = QVBoxLayout(self.ui.frame_pml_control_3)
    self.ui.verticalLayout_29_3.setSpacing(0)
    self.ui.verticalLayout_29_3.setObjectName(u"verticalLayout_29")
    self.ui.verticalLayout_29_3.setContentsMargins(0, 0, 0, 0)
    self.ui.frame_pml_control_3__range = QFrame(self.ui.frame_pml_control_3)
    self.ui.frame_pml_control_3__range.setStyleSheet(u"border:none;")
    self.ui.frame_pml_control_3__range.setObjectName(u"frame_pml_control__range")
    self.ui.frame_pml_control_3__range.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_3__range.setFrameShadow(QFrame.Raised)
    self.ui.formLayout_2_3 = QFormLayout(self.ui.frame_pml_control_3__range)
    self.ui.formLayout_2_3.setObjectName(u"formLayout_2")
    self.ui.label_pml_voltage_range_3 = QLabel(self.ui.frame_pml_control_3__range)
    self.ui.label_pml_voltage_range_3.setObjectName(u"label_pml_voltage_range")
    self.ui.label_pml_voltage_range_3.setFont(font10)
        
    self.ui.formLayout_2_3.setWidget(0, QFormLayout.LabelRole, self.ui.label_pml_voltage_range_3)
    
    self.ui.cbx_pml_voltage_range_3 = QComboBox(self.ui.frame_pml_control_3__range)
    self.ui.cbx_pml_voltage_range_3.addItem("")
    self.ui.cbx_pml_voltage_range_3.addItem("")
    self.ui.cbx_pml_voltage_range_3.setObjectName(u"cbx_pml_voltage_range")
    self.ui.cbx_pml_voltage_range_3.setMaximumSize(QtCore.QSize(16777215, 54))
    self.ui.cbx_pml_voltage_range_3.setFont(font10)
    
    self.ui.formLayout_2_3.setWidget(0, QFormLayout.FieldRole, self.ui.cbx_pml_voltage_range_3)
    
    self.ui.label_pml_current_range_3 = QLabel(self.ui.frame_pml_control_3__range)
    self.ui.label_pml_current_range_3.setObjectName(u"label_pml_current_range")
    self.ui.label_pml_current_range_3.setFont(font10)
        
    self.ui.formLayout_2_3.setWidget(1, QFormLayout.LabelRole, self.ui.label_pml_current_range_3)
    
    self.ui.cbx_pml_current_range_3 = QComboBox(self.ui.frame_pml_control_3__range)
    self.ui.cbx_pml_current_range_3.addItem("")
    self.ui.cbx_pml_current_range_3.addItem("")
    self.ui.cbx_pml_current_range_3.setObjectName(u"cbx_pml_current_range")
    self.ui.cbx_pml_current_range_3.setMaximumSize(QtCore.QSize(16777215, 54))
    self.ui.cbx_pml_current_range_3.setFont(font10)
    
    self.ui.formLayout_2_3.setWidget(1, QFormLayout.FieldRole, self.ui.cbx_pml_current_range_3)
    
    
    self.ui.verticalLayout_29_3.addWidget(self.ui.frame_pml_control_3__range)
    
    self.ui.frame_pml_control_3_lower = QFrame(self.ui.frame_pml_control_3)
    self.ui.frame_pml_control_3_lower.setStyleSheet(u"border:none;")
    self.ui.frame_pml_control_3_lower.setObjectName(u"frame_pml_control_lower")
    self.ui.frame_pml_control_3_lower.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_3_lower.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_19_3 = QHBoxLayout(self.ui.frame_pml_control_3_lower)
    self.ui.horizontalLayout_19_3.setSpacing(0)
    self.ui.horizontalLayout_19_3.setObjectName(u"horizontalLayout_19_3")
    self.ui.horizontalLayout_19_3.setContentsMargins(0, 0, 0, 0)
    self.ui.frame_pml_integration_3 = QFrame(self.ui.frame_pml_control_3_lower)
    self.ui.frame_pml_integration_3.setObjectName(u"frame_pml_integration")
    self.ui.frame_pml_integration_3.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.ui.frame_pml_integration_3.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_integration_3.setFrameShadow(QFrame.Raised)
    self.verticalLayout_30_3 = QVBoxLayout(self.ui.frame_pml_integration_3)
    self.verticalLayout_30_3.setObjectName(u"verticalLayout_30_3")
    self.ui.label_pml_integration_3 = QLabel(self.ui.frame_pml_integration_3)
    self.ui.label_pml_integration_3.setObjectName(u"label_pml_integration")
    sizePolicy.setHeightForWidth(self.ui.label_pml_integration_3.sizePolicy().hasHeightForWidth())
    self.ui.label_pml_integration_3.setSizePolicy(sizePolicy)
    self.ui.label_pml_integration_3.setMinimumSize(QtCore.QSize(0, 20))
    self.ui.label_pml_integration_3.setMaximumSize(QtCore.QSize(16777215, 20))
    self.ui.label_pml_integration_3.setFont(font10)
        
    self.verticalLayout_30_3.addWidget(self.ui.label_pml_integration_3)
    
    self.btn_pml_integration_start_3 = QPushButton(self.ui.frame_pml_integration_3)
    self.btn_pml_integration_start_3.setObjectName(u"btn_pml_integration_start_3")
    self.btn_pml_integration_start_3.setFont(font10)
    self.btn_pml_integration_start_3.setStyleSheet(u"QPushButton {\n"
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
    
    self.verticalLayout_30_3.addWidget(self.btn_pml_integration_start_3)
    
    self.btn_pml_integration_stop_3 = QPushButton(self.ui.frame_pml_integration_3)
    self.btn_pml_integration_stop_3.setObjectName(u"btn_pml_integration_stop_3")
    self.btn_pml_integration_stop_3.setFont(font10)
    self.btn_pml_integration_stop_3.setStyleSheet(u"QPushButton {\n"
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
    
    self.verticalLayout_30_3.addWidget(self.btn_pml_integration_stop_3)
    
    self.btn_pml_integration_reset_3 = QPushButton(self.ui.frame_pml_integration_3)
    self.btn_pml_integration_reset_3.setObjectName(u"btn_pml_integration_reset_3")
    self.btn_pml_integration_reset_3.setFont(font10)
    self.btn_pml_integration_reset_3.setStyleSheet(u"QPushButton {\n"
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
    
    self.verticalLayout_30_3.addWidget(self.btn_pml_integration_reset_3)
    
    
    self.ui.horizontalLayout_19_3.addWidget(self.ui.frame_pml_integration_3)
    
    self.ui.frame_pml_averaging_3 = QFrame(self.ui.frame_pml_control_3_lower)
    self.ui.frame_pml_averaging_3.setObjectName(u"frame_pml_averaging")
    self.ui.frame_pml_averaging_3.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.ui.frame_pml_averaging_3.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_averaging_3.setFrameShadow(QFrame.Raised)
    self.verticalLayout_31_3 = QVBoxLayout(self.ui.frame_pml_averaging_3)
    self.verticalLayout_31_3.setSpacing(2)
    self.verticalLayout_31_3.setObjectName(u"verticalLayout_31_3")
    self.verticalLayout_31_3.setContentsMargins(-1, 5, -1, 5)
    self.ui.label_pml_averaging_3 = QLabel(self.ui.frame_pml_averaging_3)
    self.ui.label_pml_averaging_3.setObjectName(u"label_pml_averaging")
    sizePolicy.setHeightForWidth(self.ui.label_pml_averaging_3.sizePolicy().hasHeightForWidth())
    self.ui.label_pml_averaging_3.setSizePolicy(sizePolicy)
    self.ui.label_pml_averaging_3.setMinimumSize(QtCore.QSize(0, 20))
    self.ui.label_pml_averaging_3.setMaximumSize(QtCore.QSize(16777215, 20))
    self.ui.label_pml_averaging_3.setFont(font10)
        
    self.verticalLayout_31_3.addWidget(self.ui.label_pml_averaging_3)
    
    self.btn_pml_averaging_toggle_3 = QPushButton(self.ui.frame_pml_averaging_3)
    self.btn_pml_averaging_toggle_3.setObjectName(u"btn_pml_averaging_toggle_3")
    self.btn_pml_averaging_toggle_3.setFont(font10)
    self.btn_pml_averaging_toggle_3.setStyleSheet(u"QPushButton {\n"
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
    
    self.verticalLayout_31_3.addWidget(self.btn_pml_averaging_toggle_3)
    
    self.cbx_pml_averaging_count_3 = QComboBox(self.ui.frame_pml_averaging_3)
    self.cbx_pml_averaging_count_3.addItem("")
    self.cbx_pml_averaging_count_3.addItem("")
    self.cbx_pml_averaging_count_3.addItem("")
    self.cbx_pml_averaging_count_3.setObjectName(u"cbx_pml_averaging_count_3")
    self.cbx_pml_averaging_count_3.setMaximumSize(QtCore.QSize(16777215, 40))
    self.cbx_pml_averaging_count_3.setFont(font10)
    
    self.verticalLayout_31_3.addWidget(self.cbx_pml_averaging_count_3)
    
    self.cbx_pml_averaging_mode_3 = QComboBox(self.ui.frame_pml_averaging_3)
    self.cbx_pml_averaging_mode_3.addItem("")
    self.cbx_pml_averaging_mode_3.addItem("")
    self.cbx_pml_averaging_mode_3.setObjectName(u"cbx_pml_averaging_mode_3")
    self.cbx_pml_averaging_mode_3.setMaximumSize(QtCore.QSize(16777215, 40))
    self.cbx_pml_averaging_mode_3.setFont(font10)
    
    self.verticalLayout_31_3.addWidget(self.cbx_pml_averaging_mode_3)
    
    
    self.ui.horizontalLayout_19_3.addWidget(self.ui.frame_pml_averaging_3)
    
    self.ui.frame_pml_measure_mode_3 = QFrame(self.ui.frame_pml_control_3_lower)
    self.ui.frame_pml_measure_mode_3.setObjectName(u"frame_pml_measure_mode")
    self.ui.frame_pml_measure_mode_3.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.ui.frame_pml_measure_mode_3.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_measure_mode_3.setFrameShadow(QFrame.Raised)
    self.ui.verticalLayout_32_3 = QVBoxLayout(self.ui.frame_pml_measure_mode_3)
    self.ui.verticalLayout_32_3.setSpacing(13)
    self.ui.verticalLayout_32_3.setObjectName(u"verticalLayout_32")
    self.ui.verticalLayout_32_3.setContentsMargins(13, 13, 13, 13)
    self.ui.label_pml_measure_mode_3 = QLabel(self.ui.frame_pml_measure_mode_3)
    self.ui.label_pml_measure_mode_3.setObjectName(u"label_pml_measure_mode")
    sizePolicy.setHeightForWidth(self.ui.label_pml_measure_mode_3.sizePolicy().hasHeightForWidth())
    self.ui.label_pml_measure_mode_3.setSizePolicy(sizePolicy)
    self.ui.label_pml_measure_mode_3.setMaximumSize(QtCore.QSize(16777215, 20))
    self.ui.label_pml_measure_mode_3.setFont(font10)
        
    self.ui.verticalLayout_32_3.addWidget(self.ui.label_pml_measure_mode_3)
    
    self.ui.btn_pml_measure_mode_3 = QPushButton(self.ui.frame_pml_measure_mode_3)
    self.ui.btn_pml_measure_mode_3.setObjectName(u"btn_pml_measure_mode")
    self.ui.btn_pml_measure_mode_3.setFont(font10)
    self.ui.btn_pml_measure_mode_3.setStyleSheet(u"QPushButton {\n"
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
    
    self.ui.verticalLayout_32_3.addWidget(self.ui.btn_pml_measure_mode_3)
    
    
    self.ui.horizontalLayout_19_3.addWidget(self.ui.frame_pml_measure_mode_3)
    
    
    self.ui.verticalLayout_29_3.addWidget(self.ui.frame_pml_control_3_lower)
    
    
    self.ui.horizontalLayout_15_3.addWidget(self.ui.frame_pml_control_3)
    
    
    self.ui.verticalLayout_19_3.addWidget(self.ui.frame_pml_contents_3)
    
    
    self.ui.tabWidget_pml.addTab(self.ui.frame_manual_control_pml_3, 'CH 3')

    # ELOAD 4
    self.ui.frame_manual_control_eload_4 = QFrame(self.ui.frame_manual_control_lower)
    self.ui.frame_manual_control_eload_4.setObjectName(u"frame_manual_control_eload_4")
    sizePolicy20 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
    sizePolicy20.setHorizontalStretch(3)
    sizePolicy20.setVerticalStretch(0)
    sizePolicy20.setHeightForWidth(self.ui.frame_manual_control_eload_4.sizePolicy().hasHeightForWidth())
    self.ui.frame_manual_control_eload_4.setSizePolicy(sizePolicy20)
    self.ui.frame_manual_control_eload_4.setMinimumSize(QtCore.QSize(300, 0))
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
    self.ui.frame_manual_control_eload_4_contents.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_4_contents.setObjectName(u"frame_manual_control_eload_contents_4")
    self.ui.frame_manual_control_eload_4_contents.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_contents.setFrameShadow(QFrame.Raised)
    self.verticalLayout_77_4 = QVBoxLayout(self.ui.frame_manual_control_eload_4_contents)
    self.verticalLayout_77_4.setObjectName(u"verticalLayout_77_4")
    self.ui.frame_manual_control_eload_4_top = QFrame(self.ui.frame_manual_control_eload_4_contents)
    self.ui.frame_manual_control_eload_4_top.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_4_top.setObjectName(u"frame_manual_control_eload_top_4")
    self.ui.frame_manual_control_eload_4_top.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_top.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_47_4 = QHBoxLayout(self.ui.frame_manual_control_eload_4_top)
    self.ui.horizontalLayout_47_4.setObjectName(u"horizontalLayout_47")
    self.ui.cbx_manual_control_eload_type_4 = QComboBox(self.ui.frame_manual_control_eload_4_top)
    self.ui.cbx_manual_control_eload_type_4.addItem("")
    self.ui.cbx_manual_control_eload_type_4.addItem("")
    self.ui.cbx_manual_control_eload_type_4.addItem("")
    self.ui.cbx_manual_control_eload_type_4.setObjectName(u"cbx_manual_control_eload_type")
    self.ui.cbx_manual_control_eload_type_4.setMaximumSize(QtCore.QSize(16777215, 40))
    self.ui.cbx_manual_control_eload_type_4.setFont(font10)
    self.ui.cbx_manual_control_eload_type_4.setStyleSheet(u"QComboBox{\n"
    "border: 2px solid black;\n"
    "border-radius:5px;\n"
    "}\n"
    "\n"
    "QComboBox:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}")
    
    self.ui.horizontalLayout_47_4.addWidget(self.ui.cbx_manual_control_eload_type_4)
    
    self.ui.btn_manual_control_eload_a_b_swap_4 = QPushButton(self.ui.frame_manual_control_eload_4_top)
    self.ui.btn_manual_control_eload_a_b_swap_4.setObjectName(u"btn_manual_control_eload_a_b_swap_4")
    self.ui.btn_manual_control_eload_a_b_swap_4.setMinimumSize(QtCore.QSize(80, 40))
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
    
    self.ui.horizontalLayout_47_4.addWidget(self.ui.btn_manual_control_eload_a_b_swap_4)
    
    
    self.verticalLayout_77_4.addWidget(self.ui.frame_manual_control_eload_4_top)
    
    self.ui.frame_manual_control_eload_4_center = QFrame(self.ui.frame_manual_control_eload_4_contents)
    self.ui.frame_manual_control_eload_4_center.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_4_center.setObjectName(u"frame_manual_control_eload_center_4")
    self.ui.frame_manual_control_eload_4_center.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_center.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_46_4 = QHBoxLayout(self.ui.frame_manual_control_eload_4_center)
    self.ui.horizontalLayout_46_4.setObjectName(u"horizontalLayout_46")
    self.ui.frame_manual_control_eload_4_level = QFrame(self.ui.frame_manual_control_eload_4_center)
    self.ui.frame_manual_control_eload_4_level.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_4_level.setObjectName(u"frame_manual_control_eload_level_4")
    self.ui.frame_manual_control_eload_4_level.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_level.setFrameShadow(QFrame.Raised)
    self.verticalLayout_70_4 = QVBoxLayout(self.ui.frame_manual_control_eload_4_level)
    self.verticalLayout_70_4.setObjectName(u"verticalLayout_70_4")
    self.ui.frame_manual_control_eload_4_a = QFrame(self.ui.frame_manual_control_eload_4_level)
    self.ui.frame_manual_control_eload_4_a.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_4_a.setObjectName(u"frame_manual_control_eload_a_4")
    self.ui.frame_manual_control_eload_4_a.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_a.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_45_4 = QHBoxLayout(self.ui.frame_manual_control_eload_4_a)
    self.ui.horizontalLayout_45_4.setObjectName(u"horizontalLayout_45")
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
    
    self.ui.horizontalLayout_45_4.addWidget(self.ui.label_manual_control_eload_4_a)
    
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
    
    self.ui.horizontalLayout_45_4.addWidget(self.ui.lineedit_manual_control_eload_a_level_4)
    
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
    
    self.ui.horizontalLayout_45_4.addWidget(self.ui.label_manual_control_eload_4_a_level_unit)
    
    self.ui.btn_manual_control_eload_set_A_4 = QPushButton(self.ui.frame_manual_control_eload_4_a)
    self.ui.btn_manual_control_eload_set_A_4.setObjectName(u"btn_manual_control_eload_set_A")
    self.ui.btn_manual_control_eload_set_A_4.setMinimumSize(QtCore.QSize(50, 30))
    self.ui.btn_manual_control_eload_set_A_4.setFont(font4)
    self.ui.btn_manual_control_eload_set_A_4.setStyleSheet(u"QPushButton {\n"
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
    self.ui.btn_manual_control_eload_set_A_4.setCheckable(False)
    self.ui.btn_manual_control_eload_set_A_4.setChecked(False)
    
    self.ui.horizontalLayout_45_4.addWidget(self.ui.btn_manual_control_eload_set_A_4)
    
    
    self.verticalLayout_70_4.addWidget(self.ui.frame_manual_control_eload_4_a)
    
    self.ui.frame_manual_control_eload_4_b = QFrame(self.ui.frame_manual_control_eload_4_level)
    self.ui.frame_manual_control_eload_4_b.setStyleSheet(u"border:none;")
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
    
    self.ui.btn_manual_control_eload_set_B_4 = QPushButton(self.ui.frame_manual_control_eload_4_b)
    self.ui.btn_manual_control_eload_set_B_4.setObjectName(u"btn_manual_control_eload_set_B")
    self.ui.btn_manual_control_eload_set_B_4.setMinimumSize(QtCore.QSize(50, 30))
    self.ui.btn_manual_control_eload_set_B_4.setFont(font4)
    self.ui.btn_manual_control_eload_set_B_4.setStyleSheet(u"QPushButton {\n"
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
    self.ui.btn_manual_control_eload_set_B_4.setCheckable(False)
    self.ui.btn_manual_control_eload_set_B_4.setChecked(False)
    
    self.ui.horizontalLayout_39_4.addWidget(self.ui.btn_manual_control_eload_set_B_4)
    
    
    self.verticalLayout_70_4.addWidget(self.ui.frame_manual_control_eload_4_b)
    
    
    self.ui.horizontalLayout_46_4.addWidget(self.ui.frame_manual_control_eload_4_level)
    
    self.ui.frame_manual_control_eload_4_slew = QFrame(self.ui.frame_manual_control_eload_4_center)
    self.ui.frame_manual_control_eload_4_slew.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_4_slew.setObjectName(u"frame_manual_control_eload_slew_4")
    self.ui.frame_manual_control_eload_4_slew.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_slew.setFrameShadow(QFrame.Raised)
    self.gridLayout_29_4 = QGridLayout(self.ui.frame_manual_control_eload_4_slew)
    self.gridLayout_29_4.setObjectName(u"gridLayout_29_4")
    self.ui.frame_manual_control_eload_4_slew_fall = QFrame(self.ui.frame_manual_control_eload_4_slew)
    self.ui.frame_manual_control_eload_4_slew_fall.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_4_slew_fall.setObjectName(u"frame_manual_control_eload_slew_fall_4")
    self.ui.frame_manual_control_eload_4_slew_fall.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_slew_fall.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_38_4 = QHBoxLayout(self.ui.frame_manual_control_eload_4_slew_fall)
    self.ui.horizontalLayout_38_4.setObjectName(u"horizontalLayout_38_4")
    self.label_manual_control_electronic_load_fall_4 = QLabel(self.ui.frame_manual_control_eload_4_slew_fall)
    self.label_manual_control_electronic_load_fall_4.setObjectName(u"label_manual_control_electronic_load_fall_4")
    self.label_manual_control_electronic_load_fall_4.setMaximumSize(QtCore.QSize(16777215, 30))
    self.label_manual_control_electronic_load_fall_4.setFont(font10)
    self.label_manual_control_electronic_load_fall_4.setLayoutDirection(Qt.LeftToRight)
    self.label_manual_control_electronic_load_fall_4.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.label_manual_control_electronic_load_fall_4.setAlignment(Qt.AlignCenter)
    
    self.ui.horizontalLayout_38_4.addWidget(self.label_manual_control_electronic_load_fall_4)
    
    self.ui.lineedit_manual_control_eload_slew_fall_4 = QLineEdit(self.ui.frame_manual_control_eload_4_slew_fall)
    self.ui.lineedit_manual_control_eload_slew_fall_4.setObjectName(u"lineedit_manual_control_eload_slew_fall")
    sizePolicy21.setHeightForWidth(self.ui.lineedit_manual_control_eload_slew_fall_4.sizePolicy().hasHeightForWidth())
    self.ui.lineedit_manual_control_eload_slew_fall_4.setSizePolicy(sizePolicy21)
    self.ui.lineedit_manual_control_eload_slew_fall_4.setMinimumSize(QtCore.QSize(0, 40))
    self.ui.lineedit_manual_control_eload_slew_fall_4.setFont(font10)
    self.ui.lineedit_manual_control_eload_slew_fall_4.setStyleSheet(u"QLineEdit {\n"
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
    
    self.ui.horizontalLayout_38_4.addWidget(self.ui.lineedit_manual_control_eload_slew_fall_4)
    
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
    
    
    self.gridLayout_29_4.addWidget(self.ui.frame_manual_control_eload_4_slew_fall, 1, 0, 1, 1)
    
    self.ui.frame_manual_control_eload_4_slew_rise = QFrame(self.ui.frame_manual_control_eload_4_slew)
    self.ui.frame_manual_control_eload_4_slew_rise.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_4_slew_rise.setObjectName(u"frame_manual_control_eload_slew_rise_4")
    self.ui.frame_manual_control_eload_4_slew_rise.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_slew_rise.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_36_4 = QHBoxLayout(self.ui.frame_manual_control_eload_4_slew_rise)
    self.ui.horizontalLayout_36_4.setObjectName(u"horizontalLayout_36_4")
    self.label_manual_control_electronic_load_rise_4 = QLabel(self.ui.frame_manual_control_eload_4_slew_rise)
    self.label_manual_control_electronic_load_rise_4.setObjectName(u"label_manual_control_electronic_load_rise_4")
    self.label_manual_control_electronic_load_rise_4.setMaximumSize(QtCore.QSize(16777215, 30))
    self.label_manual_control_electronic_load_rise_4.setFont(font10)
    self.label_manual_control_electronic_load_rise_4.setStyleSheet(u"QLabel:disabled{\n"
    "	color: rgb(71, 71, 71);\n"
    "}\n"
    "\n"
    "QLabel{\n"
    "border:none\n"
    "}")
    self.label_manual_control_electronic_load_rise_4.setAlignment(Qt.AlignCenter)
    
    self.ui.horizontalLayout_36_4.addWidget(self.label_manual_control_electronic_load_rise_4)
    
    self.ui.lineedit_manual_control_eload_slew_rise_4 = QLineEdit(self.ui.frame_manual_control_eload_4_slew_rise)
    self.ui.lineedit_manual_control_eload_slew_rise_4.setObjectName(u"lineedit_manual_control_eload_slew_rise")
    sizePolicy21.setHeightForWidth(self.ui.lineedit_manual_control_eload_slew_rise_4.sizePolicy().hasHeightForWidth())
    self.ui.lineedit_manual_control_eload_slew_rise_4.setSizePolicy(sizePolicy21)
    self.ui.lineedit_manual_control_eload_slew_rise_4.setMinimumSize(QtCore.QSize(0, 40))
    self.ui.lineedit_manual_control_eload_slew_rise_4.setFont(font10)
    self.ui.lineedit_manual_control_eload_slew_rise_4.setStyleSheet(u"QLineEdit {\n"
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
    
    self.ui.horizontalLayout_36_4.addWidget(self.ui.lineedit_manual_control_eload_slew_rise_4)
    
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
    
    
    self.gridLayout_29_4.addWidget(self.ui.frame_manual_control_eload_4_slew_rise, 0, 0, 1, 1)
    
    self.ui.btn_manual_control_eload_set_slew_4 = QPushButton(self.ui.frame_manual_control_eload_4_slew)
    self.ui.btn_manual_control_eload_set_slew_4.setObjectName(u"btn_manual_control_eload_set_slew")
    sizePolicy19.setHeightForWidth(self.ui.btn_manual_control_eload_set_slew_4.sizePolicy().hasHeightForWidth())
    self.ui.btn_manual_control_eload_set_slew_4.setSizePolicy(sizePolicy19)
    self.ui.btn_manual_control_eload_set_slew_4.setMinimumSize(QtCore.QSize(50, 60))
    self.ui.btn_manual_control_eload_set_slew_4.setFont(font4)
    self.ui.btn_manual_control_eload_set_slew_4.setStyleSheet(u"QPushButton {\n"
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
    self.ui.btn_manual_control_eload_set_slew_4.setCheckable(False)
    self.ui.btn_manual_control_eload_set_slew_4.setChecked(False)
    
    self.gridLayout_29_4.addWidget(self.ui.btn_manual_control_eload_set_slew_4, 0, 1, 2, 1)
    
    
    self.ui.horizontalLayout_46_4.addWidget(self.ui.frame_manual_control_eload_4_slew)
    
    
    self.verticalLayout_77_4.addWidget(self.ui.frame_manual_control_eload_4_center)
    
    self.ui.frame_manual_control_eload_4_bottom = QFrame(self.ui.frame_manual_control_eload_4_contents)
    self.ui.frame_manual_control_eload_4_bottom.setStyleSheet(u"border:none;")
    self.ui.frame_manual_control_eload_4_bottom.setObjectName(u"frame_manual_control_eload_bottom_4")
    self.ui.frame_manual_control_eload_4_bottom.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_manual_control_eload_4_bottom.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_56_4 = QHBoxLayout(self.ui.frame_manual_control_eload_4_bottom)
    self.ui.horizontalLayout_56_4.setObjectName(u"horizontalLayout_56")
    self.ui.btn_manual_control_eload_turn_on_4 = QPushButton(self.ui.frame_manual_control_eload_4_bottom)
    self.ui.btn_manual_control_eload_turn_on_4.setObjectName(u"btn_manual_control_eload_turn_on")
    self.ui.btn_manual_control_eload_turn_on_4.setMinimumSize(QtCore.QSize(80, 40))
    self.ui.btn_manual_control_eload_turn_on_4.setFont(font13)
    self.ui.btn_manual_control_eload_turn_on_4.setStyleSheet(u"QPushButton {\n"
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
    self.ui.btn_manual_control_eload_turn_on_4.setIcon(icon8)
    self.ui.btn_manual_control_eload_turn_on_4.setCheckable(False)
    self.ui.btn_manual_control_eload_turn_on_4.setChecked(False)
    
    self.ui.horizontalLayout_56_4.addWidget(self.ui.btn_manual_control_eload_turn_on_4)
    
    self.ui.btn_manual_control_eload_turn_off_4 = QPushButton(self.ui.frame_manual_control_eload_4_bottom)
    self.ui.btn_manual_control_eload_turn_off_4.setObjectName(u"btn_manual_control_eload_turn_off")
    self.ui.btn_manual_control_eload_turn_off_4.setMinimumSize(QtCore.QSize(80, 40))
    self.ui.btn_manual_control_eload_turn_off_4.setFont(font13)
    self.ui.btn_manual_control_eload_turn_off_4.setStyleSheet(u"QPushButton {\n"
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
    self.ui.btn_manual_control_eload_turn_off_4.setIcon(icon9)
    self.ui.btn_manual_control_eload_turn_off_4.setCheckable(False)
    self.ui.btn_manual_control_eload_turn_off_4.setChecked(False)
    
    self.ui.horizontalLayout_56_4.addWidget(self.ui.btn_manual_control_eload_turn_off_4)
    
    
    self.verticalLayout_77_4.addWidget(self.ui.frame_manual_control_eload_4_bottom)
    
    
    self.ui.verticalLayout_23_4.addWidget(self.ui.frame_manual_control_eload_4_contents)
    
    
    self.ui.tabWidget_eload.addTab(self.ui.frame_manual_control_eload_4, 'CH 4')

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
    self.ui.label_load_power_meter_4 = QLabel(self.ui.frame_manual_control_pml_4)
    self.ui.label_load_power_meter_4.setObjectName(u"label_load_power_meter")
    self.ui.label_load_power_meter_4.setMaximumSize(QtCore.QSize(16777215, 30))
    self.ui.label_load_power_meter_4.setFont(font1)
    self.ui.label_load_power_meter_4.setCursor(QCursor(Qt.ArrowCursor))
    self.ui.label_load_power_meter_4.setStyleSheet(u"QLabel{border:none;}\n"
    "QLabel:disabled{\n"
    "	color: rgb(71, 71, 71)\n"
    "}")
    self.ui.label_load_power_meter_4.setAlignment(Qt.AlignCenter)
    
    self.ui.verticalLayout_19_4.addWidget(self.ui.label_load_power_meter_4)
    
    self.ui.frame_pml_contents_4 = QFrame(self.ui.frame_manual_control_pml_4)
    self.ui.frame_pml_contents_4.setStyleSheet(u"border:none;")
    self.ui.frame_pml_contents_4.setObjectName(u"frame_pml_contents_4")
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
    "\tfont: 700 24pt \"Segoe UI\";\n"
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
    "\tfont: 700 24pt \"Segoe UI\";\n"
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
    "\tfont: 700 24pt \"Segoe UI\";\n"
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
    "\tfont: 700 24pt \"Segoe UI\";\n"
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
    "\tfont: 700 24pt \"Segoe UI\";\n"
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
    self.ui.verticalLayout_21_4 = QVBoxLayout(self.ui.frame_pml_display_4_select)
    self.ui.verticalLayout_21_4.setSpacing(0)
    self.ui.verticalLayout_21_4.setObjectName(u"verticalLayout_21")
    self.ui.verticalLayout_21_4.setContentsMargins(0, 0, 0, 0)
    self.ui.cbx_pml_display_a_4 = QComboBox(self.ui.frame_pml_display_4_select)
    self.ui.cbx_pml_display_a_4.setObjectName(u"cbx_pml_display_a")
    self.ui.cbx_pml_display_a_4.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.ui.verticalLayout_21_4.addWidget(self.ui.cbx_pml_display_a_4)
    
    self.ui.cbx_pml_display_b_4 = QComboBox(self.ui.frame_pml_display_4_select)
    self.ui.cbx_pml_display_b_4.setObjectName(u"cbx_pml_display_b")
    self.ui.cbx_pml_display_b_4.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.ui.verticalLayout_21_4.addWidget(self.ui.cbx_pml_display_b_4)
    
    self.ui.cbx_pml_display_c_4 = QComboBox(self.ui.frame_pml_display_4_select)
    self.ui.cbx_pml_display_c_4.setObjectName(u"cbx_pml_display_c")
    self.ui.cbx_pml_display_c_4.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.ui.verticalLayout_21_4.addWidget(self.ui.cbx_pml_display_c_4)
    
    self.ui.cbx_pml_display_d_4 = QComboBox(self.ui.frame_pml_display_4_select)
    self.ui.cbx_pml_display_d_4.setObjectName(u"cbx_pml_display_d")
    self.ui.cbx_pml_display_d_4.setMaximumSize(QtCore.QSize(16777215, 54))
    
    self.ui.verticalLayout_21_4.addWidget(self.ui.cbx_pml_display_d_4)
    
    
    self.ui.horizontalLayout_15_4.addWidget(self.ui.frame_pml_display_4_select)
    
    self.ui.frame_pml_control_4 = QFrame(self.ui.frame_pml_contents_4)
    self.ui.frame_pml_control_4.setObjectName(u"frame_pml_control_4")
    self.ui.frame_pml_control_4.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;\n"
    "background-color: rgb(29,34, 44);\n"
    "")
    self.ui.frame_pml_control_4.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_4.setFrameShadow(QFrame.Raised)
    self.ui.verticalLayout_29_4 = QVBoxLayout(self.ui.frame_pml_control_4)
    self.ui.verticalLayout_29_4.setSpacing(0)
    self.ui.verticalLayout_29_4.setObjectName(u"verticalLayout_29")
    self.ui.verticalLayout_29_4.setContentsMargins(0, 0, 0, 0)
    self.ui.frame_pml_control_4__range = QFrame(self.ui.frame_pml_control_4)
    self.ui.frame_pml_control_4__range.setStyleSheet(u"border:none;")
    self.ui.frame_pml_control_4__range.setObjectName(u"frame_pml_control__range")
    self.ui.frame_pml_control_4__range.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_4__range.setFrameShadow(QFrame.Raised)
    self.ui.formLayout_2_4 = QFormLayout(self.ui.frame_pml_control_4__range)
    self.ui.formLayout_2_4.setObjectName(u"formLayout_2")
    self.ui.label_pml_voltage_range_4 = QLabel(self.ui.frame_pml_control_4__range)
    self.ui.label_pml_voltage_range_4.setObjectName(u"label_pml_voltage_range")
    self.ui.label_pml_voltage_range_4.setFont(font10)
        
    self.ui.formLayout_2_4.setWidget(0, QFormLayout.LabelRole, self.ui.label_pml_voltage_range_4)
    
    self.ui.cbx_pml_voltage_range_4 = QComboBox(self.ui.frame_pml_control_4__range)
    self.ui.cbx_pml_voltage_range_4.addItem("")
    self.ui.cbx_pml_voltage_range_4.addItem("")
    self.ui.cbx_pml_voltage_range_4.setObjectName(u"cbx_pml_voltage_range")
    self.ui.cbx_pml_voltage_range_4.setMaximumSize(QtCore.QSize(16777215, 54))
    self.ui.cbx_pml_voltage_range_4.setFont(font10)
    
    self.ui.formLayout_2_4.setWidget(0, QFormLayout.FieldRole, self.ui.cbx_pml_voltage_range_4)
    
    self.ui.label_pml_current_range_4 = QLabel(self.ui.frame_pml_control_4__range)
    self.ui.label_pml_current_range_4.setObjectName(u"label_pml_current_range")
    self.ui.label_pml_current_range_4.setFont(font10)
        
    self.ui.formLayout_2_4.setWidget(1, QFormLayout.LabelRole, self.ui.label_pml_current_range_4)
    
    self.ui.cbx_pml_current_range_4 = QComboBox(self.ui.frame_pml_control_4__range)
    self.ui.cbx_pml_current_range_4.addItem("")
    self.ui.cbx_pml_current_range_4.addItem("")
    self.ui.cbx_pml_current_range_4.setObjectName(u"cbx_pml_current_range")
    self.ui.cbx_pml_current_range_4.setMaximumSize(QtCore.QSize(16777215, 54))
    self.ui.cbx_pml_current_range_4.setFont(font10)
    
    self.ui.formLayout_2_4.setWidget(1, QFormLayout.FieldRole, self.ui.cbx_pml_current_range_4)
    
    
    self.ui.verticalLayout_29_4.addWidget(self.ui.frame_pml_control_4__range)
    
    self.ui.frame_pml_control_4_lower = QFrame(self.ui.frame_pml_control_4)
    self.ui.frame_pml_control_4_lower.setStyleSheet(u"border:none;")
    self.ui.frame_pml_control_4_lower.setObjectName(u"frame_pml_control_lower")
    self.ui.frame_pml_control_4_lower.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_control_4_lower.setFrameShadow(QFrame.Raised)
    self.ui.horizontalLayout_19_4 = QHBoxLayout(self.ui.frame_pml_control_4_lower)
    self.ui.horizontalLayout_19_4.setSpacing(0)
    self.ui.horizontalLayout_19_4.setObjectName(u"horizontalLayout_19_4")
    self.ui.horizontalLayout_19_4.setContentsMargins(0, 0, 0, 0)
    self.ui.frame_pml_integration_4 = QFrame(self.ui.frame_pml_control_4_lower)
    self.ui.frame_pml_integration_4.setObjectName(u"frame_pml_integration")
    self.ui.frame_pml_integration_4.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.ui.frame_pml_integration_4.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_integration_4.setFrameShadow(QFrame.Raised)
    self.verticalLayout_30_4 = QVBoxLayout(self.ui.frame_pml_integration_4)
    self.verticalLayout_30_4.setObjectName(u"verticalLayout_30_4")
    self.ui.label_pml_integration_4 = QLabel(self.ui.frame_pml_integration_4)
    self.ui.label_pml_integration_4.setObjectName(u"label_pml_integration")
    sizePolicy.setHeightForWidth(self.ui.label_pml_integration_4.sizePolicy().hasHeightForWidth())
    self.ui.label_pml_integration_4.setSizePolicy(sizePolicy)
    self.ui.label_pml_integration_4.setMinimumSize(QtCore.QSize(0, 20))
    self.ui.label_pml_integration_4.setMaximumSize(QtCore.QSize(16777215, 20))
    self.ui.label_pml_integration_4.setFont(font10)
        
    self.verticalLayout_30_4.addWidget(self.ui.label_pml_integration_4)
    
    self.btn_pml_integration_start_4 = QPushButton(self.ui.frame_pml_integration_4)
    self.btn_pml_integration_start_4.setObjectName(u"btn_pml_integration_start_4")
    self.btn_pml_integration_start_4.setFont(font10)
    self.btn_pml_integration_start_4.setStyleSheet(u"QPushButton {\n"
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
    
    self.verticalLayout_30_4.addWidget(self.btn_pml_integration_start_4)
    
    self.btn_pml_integration_stop_4 = QPushButton(self.ui.frame_pml_integration_4)
    self.btn_pml_integration_stop_4.setObjectName(u"btn_pml_integration_stop_4")
    self.btn_pml_integration_stop_4.setFont(font10)
    self.btn_pml_integration_stop_4.setStyleSheet(u"QPushButton {\n"
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
    
    self.verticalLayout_30_4.addWidget(self.btn_pml_integration_stop_4)
    
    self.btn_pml_integration_reset_4 = QPushButton(self.ui.frame_pml_integration_4)
    self.btn_pml_integration_reset_4.setObjectName(u"btn_pml_integration_reset_4")
    self.btn_pml_integration_reset_4.setFont(font10)
    self.btn_pml_integration_reset_4.setStyleSheet(u"QPushButton {\n"
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
    
    self.verticalLayout_30_4.addWidget(self.btn_pml_integration_reset_4)
    
    
    self.ui.horizontalLayout_19_4.addWidget(self.ui.frame_pml_integration_4)
    
    self.ui.frame_pml_averaging_4 = QFrame(self.ui.frame_pml_control_4_lower)
    self.ui.frame_pml_averaging_4.setObjectName(u"frame_pml_averaging")
    self.ui.frame_pml_averaging_4.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.ui.frame_pml_averaging_4.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_averaging_4.setFrameShadow(QFrame.Raised)
    self.verticalLayout_31_4 = QVBoxLayout(self.ui.frame_pml_averaging_4)
    self.verticalLayout_31_4.setSpacing(2)
    self.verticalLayout_31_4.setObjectName(u"verticalLayout_31_4")
    self.verticalLayout_31_4.setContentsMargins(-1, 5, -1, 5)
    self.ui.label_pml_averaging_4 = QLabel(self.ui.frame_pml_averaging_4)
    self.ui.label_pml_averaging_4.setObjectName(u"label_pml_averaging")
    sizePolicy.setHeightForWidth(self.ui.label_pml_averaging_4.sizePolicy().hasHeightForWidth())
    self.ui.label_pml_averaging_4.setSizePolicy(sizePolicy)
    self.ui.label_pml_averaging_4.setMinimumSize(QtCore.QSize(0, 20))
    self.ui.label_pml_averaging_4.setMaximumSize(QtCore.QSize(16777215, 20))
    self.ui.label_pml_averaging_4.setFont(font10)
        
    self.verticalLayout_31_4.addWidget(self.ui.label_pml_averaging_4)
    
    self.btn_pml_averaging_toggle_4 = QPushButton(self.ui.frame_pml_averaging_4)
    self.btn_pml_averaging_toggle_4.setObjectName(u"btn_pml_averaging_toggle_4")
    self.btn_pml_averaging_toggle_4.setFont(font10)
    self.btn_pml_averaging_toggle_4.setStyleSheet(u"QPushButton {\n"
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
    
    self.verticalLayout_31_4.addWidget(self.btn_pml_averaging_toggle_4)
    
    self.cbx_pml_averaging_count_4 = QComboBox(self.ui.frame_pml_averaging_4)
    self.cbx_pml_averaging_count_4.addItem("")
    self.cbx_pml_averaging_count_4.addItem("")
    self.cbx_pml_averaging_count_4.addItem("")
    self.cbx_pml_averaging_count_4.setObjectName(u"cbx_pml_averaging_count_4")
    self.cbx_pml_averaging_count_4.setMaximumSize(QtCore.QSize(16777215, 40))
    self.cbx_pml_averaging_count_4.setFont(font10)
    
    self.verticalLayout_31_4.addWidget(self.cbx_pml_averaging_count_4)
    
    self.cbx_pml_averaging_mode_4 = QComboBox(self.ui.frame_pml_averaging_4)
    self.cbx_pml_averaging_mode_4.addItem("")
    self.cbx_pml_averaging_mode_4.addItem("")
    self.cbx_pml_averaging_mode_4.setObjectName(u"cbx_pml_averaging_mode_4")
    self.cbx_pml_averaging_mode_4.setMaximumSize(QtCore.QSize(16777215, 40))
    self.cbx_pml_averaging_mode_4.setFont(font10)
    
    self.verticalLayout_31_4.addWidget(self.cbx_pml_averaging_mode_4)
    
    
    self.ui.horizontalLayout_19_4.addWidget(self.ui.frame_pml_averaging_4)
    
    self.ui.frame_pml_measure_mode_4 = QFrame(self.ui.frame_pml_control_4_lower)
    self.ui.frame_pml_measure_mode_4.setObjectName(u"frame_pml_measure_mode")
    self.ui.frame_pml_measure_mode_4.setStyleSheet(u"border: 2px solid black;\n"
    "border-radius: 10px;")
    self.ui.frame_pml_measure_mode_4.setFrameShape(QFrame.StyledPanel)
    self.ui.frame_pml_measure_mode_4.setFrameShadow(QFrame.Raised)
    self.ui.verticalLayout_32_4 = QVBoxLayout(self.ui.frame_pml_measure_mode_4)
    self.ui.verticalLayout_32_4.setSpacing(13)
    self.ui.verticalLayout_32_4.setObjectName(u"verticalLayout_32")
    self.ui.verticalLayout_32_4.setContentsMargins(13, 13, 13, 13)
    self.ui.label_pml_measure_mode_4 = QLabel(self.ui.frame_pml_measure_mode_4)
    self.ui.label_pml_measure_mode_4.setObjectName(u"label_pml_measure_mode")
    sizePolicy.setHeightForWidth(self.ui.label_pml_measure_mode_4.sizePolicy().hasHeightForWidth())
    self.ui.label_pml_measure_mode_4.setSizePolicy(sizePolicy)
    self.ui.label_pml_measure_mode_4.setMaximumSize(QtCore.QSize(16777215, 20))
    self.ui.label_pml_measure_mode_4.setFont(font10)
        
    self.ui.verticalLayout_32_4.addWidget(self.ui.label_pml_measure_mode_4)
    
    self.ui.btn_pml_measure_mode_4 = QPushButton(self.ui.frame_pml_measure_mode_4)
    self.ui.btn_pml_measure_mode_4.setObjectName(u"btn_pml_measure_mode")
    self.ui.btn_pml_measure_mode_4.setFont(font10)
    self.ui.btn_pml_measure_mode_4.setStyleSheet(u"QPushButton {\n"
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
    
    self.ui.verticalLayout_32_4.addWidget(self.ui.btn_pml_measure_mode_4)
    
    
    self.ui.horizontalLayout_19_4.addWidget(self.ui.frame_pml_measure_mode_4)
    
    
    self.ui.verticalLayout_29_4.addWidget(self.ui.frame_pml_control_4_lower)
    
    
    self.ui.horizontalLayout_15_4.addWidget(self.ui.frame_pml_control_4)
    
    
    self.ui.verticalLayout_19_4.addWidget(self.ui.frame_pml_contents_4)
    
    
    self.ui.tabWidget_pml.addTab(self.ui.frame_manual_control_pml_4, 'CH 4')

    # --- AUTOMATIC TEXT INJECTION ---
    from PySide2.QtCore import QCoreApplication

    for ch in [2, 3, 4]:
        # Combo boxes
        cbx_type = getattr(self.ui, f'cbx_manual_control_eload_type_{ch}')
        cbx_type.clear()
        cbx_type.addItem(QCoreApplication.translate("MainWindow", "CC", None))
        cbx_type.addItem(QCoreApplication.translate("MainWindow", "CV", None))
        cbx_type.addItem(QCoreApplication.translate("MainWindow", "CR", None))
        cbx_type.addItem(QCoreApplication.translate("MainWindow", "CP", None))
        
        cbx_v_range = getattr(self.ui, f'cbx_pml_voltage_range_{ch}')
        cbx_v_range.clear()
        cbx_v_range.addItem(QCoreApplication.translate("MainWindow", "AUTO", None))
        cbx_v_range.addItem(QCoreApplication.translate("MainWindow", "300V", None))
        
        cbx_c_range = getattr(self.ui, f'cbx_pml_current_range_{ch}')
        cbx_c_range.clear()
        cbx_c_range.addItem(QCoreApplication.translate("MainWindow", "AUTO", None))
        cbx_c_range.addItem(QCoreApplication.translate("MainWindow", "20A", None))
        
        # Labels and Buttons for PML
        getattr(self.ui, f'label_pml_display_a_{ch}').setText("None")
        getattr(self.ui, f'label_pml_display_b_{ch}').setText("None")
        getattr(self.ui, f'label_pml_display_c_{ch}').setText("None")
        getattr(self.ui, f'label_pml_display_d_{ch}').setText("None")
        
        getattr(self.ui, f'label_pml_voltage_range_{ch}').setText(QCoreApplication.translate("MainWindow", "Voltage Range", None))
        getattr(self.ui, f'label_pml_current_range_{ch}').setText(QCoreApplication.translate("MainWindow", "Current Range", None))
        getattr(self.ui, f'label_pml_integration_{ch}').setText(QCoreApplication.translate("MainWindow", "Integration", None))
        getattr(self.ui, f'label_pml_averaging_{ch}').setText(QCoreApplication.translate("MainWindow", "Averaging", None))
        getattr(self.ui, f'label_pml_measure_mode_{ch}').setText(QCoreApplication.translate("MainWindow", "Mode", None))
        getattr(self.ui, f'btn_pml_measure_mode_{ch}').setText(QCoreApplication.translate("MainWindow", "RMS", None))

        getattr(self, f'label_manual_control_electronic_load_rise_{ch}').setText(QCoreApplication.translate("MainWindow", "Rise", None))
        getattr(self, f'label_manual_control_electronic_load_fall_{ch}').setText(QCoreApplication.translate("MainWindow", "Fall", None))

        cbx_avg_count = getattr(self, f'cbx_pml_averaging_count_{ch}')
        cbx_avg_count.clear()
        cbx_avg_count.addItem(QCoreApplication.translate("MainWindow", "8", None))
        cbx_avg_count.addItem(QCoreApplication.translate("MainWindow", "16", None))
        cbx_avg_count.addItem(QCoreApplication.translate("MainWindow", "64", None))
        
        cbx_avg_mode = getattr(self, f'cbx_pml_averaging_mode_{ch}')
        cbx_avg_mode.clear()
        cbx_avg_mode.addItem(QCoreApplication.translate("MainWindow", "LIN", None))
        cbx_avg_mode.addItem(QCoreApplication.translate("MainWindow", "EXP", None))

        getattr(self, f'btn_pml_integration_start_{ch}').setText(QCoreApplication.translate("MainWindow", "START", None))
        getattr(self, f'btn_pml_integration_stop_{ch}').setText(QCoreApplication.translate("MainWindow", "STOP", None))
        getattr(self, f'btn_pml_integration_reset_{ch}').setText(QCoreApplication.translate("MainWindow", "RESET", None))
        getattr(self, f'btn_pml_averaging_toggle_{ch}').setText(QCoreApplication.translate("MainWindow", "OFF", None))
        
        # Adding labels for Load power meters
        getattr(self.ui, f'label_load_power_meter_{ch}').setText(QCoreApplication.translate("MainWindow", f"LOAD POWER METER {ch}", None))

        # Labels and Buttons for E-Load
        getattr(self.ui, f'label_manual_control_eload_{ch}').setText(QCoreApplication.translate("MainWindow", f"ELECTRONIC LOAD {ch}", None))
        getattr(self.ui, f'btn_manual_control_eload_a_b_swap_{ch}').setText(QCoreApplication.translate("MainWindow", "A / B", None))
        
        getattr(self.ui, f'label_manual_control_eload_{ch}_a').setText(QCoreApplication.translate("MainWindow", "Level A", None))
        getattr(self.ui, f'label_manual_control_eload_{ch}_a_level_unit').setText(QCoreApplication.translate("MainWindow", "A", None))
        getattr(self.ui, f'btn_manual_control_eload_set_A_{ch}').setText(QCoreApplication.translate("MainWindow", "Set", None))
        
        getattr(self.ui, f'label_manual_control_eload_{ch}_b').setText(QCoreApplication.translate("MainWindow", "Level B", None))
        getattr(self.ui, f'label_manual_control_eload_{ch}_b_level_unit').setText(QCoreApplication.translate("MainWindow", "A", None))
        getattr(self.ui, f'btn_manual_control_eload_set_B_{ch}').setText(QCoreApplication.translate("MainWindow", "Set", None))
        
        # Missing label_manual_control_eload_{ch}_slew_rise
        # I'll just set unit labels
        getattr(self.ui, f'label_manual_control_eload_{ch}_slew_fall_unit').setText(QCoreApplication.translate("MainWindow", "A / µs", None))
        getattr(self.ui, f'label_manual_control_eload_{ch}_slew_rise_unit').setText(QCoreApplication.translate("MainWindow", "A / µs", None))
        getattr(self.ui, f'btn_manual_control_eload_set_slew_{ch}').setText(QCoreApplication.translate("MainWindow", "Set", None))
        
        getattr(self.ui, f'btn_manual_control_eload_turn_on_{ch}').setText(QCoreApplication.translate("MainWindow", "Load ON", None))
        getattr(self.ui, f'btn_manual_control_eload_turn_off_{ch}').setText(QCoreApplication.translate("MainWindow", "Load OFF", None))
        
