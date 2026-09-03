# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GUI_BASE.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pyqtgraph import PlotWidget

import files_rc
import files_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(2190, 1042)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1000, 900))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(0, 0, 0, 0))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(66, 73, 90, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        brush3 = QBrush(QColor(55, 61, 75, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        brush4 = QBrush(QColor(22, 24, 30, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush4)
        brush5 = QBrush(QColor(29, 32, 40, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush5)
        brush6 = QBrush(QColor(210, 210, 210, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush7 = QBrush(QColor(0, 0, 0, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush7)
        brush8 = QBrush(QColor(85, 170, 255, 255))
        brush8.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush8)
        palette.setBrush(QPalette.Active, QPalette.Link, brush8)
        brush9 = QBrush(QColor(255, 0, 127, 255))
        brush9.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush4)
        brush10 = QBrush(QColor(44, 49, 60, 255))
        brush10.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush6)
        brush11 = QBrush(QColor(210, 210, 210, 128))
        brush11.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush11)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush7)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.Link, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush6)
        brush12 = QBrush(QColor(210, 210, 210, 128))
        brush12.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush12)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush7)
        brush13 = QBrush(QColor(51, 153, 255, 255))
        brush13.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush13)
        palette.setBrush(QPalette.Disabled, QPalette.Link, brush8)
        palette.setBrush(QPalette.Disabled, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush6)
        brush14 = QBrush(QColor(210, 210, 210, 128))
        brush14.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush14)
#endif
        MainWindow.setPalette(palette)
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"QMainWindow {background: transparent; }\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(27, 29, 35, 160);\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background: transparent;\n"
"color: rgb(210, 210, 210);")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_main = QFrame(self.centralwidget)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setStyleSheet(u"/* LINE EDIT */\n"
"QLineEdit {\n"
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
"/* SCROLL BARS */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(85, 170, 255);\n"
"    min-width: 25px;\n"
"	border-radius: 7px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
""
                        "	border-top-left-radius: 7px;\n"
"    border-bottom-left-radius: 7px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(85, 170, 255);\n"
"    min-height: 25px;\n"
"	border-radius: 7px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63"
                        ", 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* CHECKBOX */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	background-image: url(:/16x16/icons/16x16/cil-check-alt.png);\n"
"}\n"
"\n"
"/* RADIO BUTTON */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius"
                        ": 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* COMBOBOX */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/16x16/icons/16x16/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb("
                        "85, 170, 255);	\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* SLIDERS */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 9px;\n"
"    height: 18px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(85, 170, 255);\n"
"    border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	border-radius: 9px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 9px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:verti"
                        "cal {\n"
"    background-color: rgb(85, 170, 255);\n"
"	border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	border-radius: 9px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"")
        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_main)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(self.frame_main)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(0, 65))
        self.frame_top.setMaximumSize(QSize(16777215, 65))
        self.frame_top.setStyleSheet(u"background-color: transparent;")
        self.frame_top.setFrameShape(QFrame.NoFrame)
        self.frame_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_top)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_toggle = QFrame(self.frame_top)
        self.frame_toggle.setObjectName(u"frame_toggle")
        self.frame_toggle.setMaximumSize(QSize(70, 16777215))
        self.frame_toggle.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.frame_toggle.setFrameShape(QFrame.NoFrame)
        self.frame_toggle.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_toggle)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_toggle_menu = QPushButton(self.frame_toggle)
        self.btn_toggle_menu.setObjectName(u"btn_toggle_menu")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_toggle_menu.sizePolicy().hasHeightForWidth())
        self.btn_toggle_menu.setSizePolicy(sizePolicy1)
        self.btn_toggle_menu.setStyleSheet(u"QPushButton {\n"
"	background-image: url(:/24x24/icons/24x24/cil-menu.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
"	border: none;\n"
"	background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")

        self.verticalLayout_3.addWidget(self.btn_toggle_menu)


        self.horizontalLayout_3.addWidget(self.frame_toggle)

        self.frame_top_right = QFrame(self.frame_top)
        self.frame_top_right.setObjectName(u"frame_top_right")
        self.frame_top_right.setStyleSheet(u"background: transparent;")
        self.frame_top_right.setFrameShape(QFrame.NoFrame)
        self.frame_top_right.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_top_right)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_top_btns = QFrame(self.frame_top_right)
        self.frame_top_btns.setObjectName(u"frame_top_btns")
        self.frame_top_btns.setMaximumSize(QSize(16777215, 42))
        self.frame_top_btns.setStyleSheet(u"background-color: rgba(27, 29, 35, 200)")
        self.frame_top_btns.setFrameShape(QFrame.NoFrame)
        self.frame_top_btns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_top_btns)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_label_top_btns = QFrame(self.frame_top_btns)
        self.frame_label_top_btns.setObjectName(u"frame_label_top_btns")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_label_top_btns.sizePolicy().hasHeightForWidth())
        self.frame_label_top_btns.setSizePolicy(sizePolicy2)
        self.frame_label_top_btns.setFrameShape(QFrame.NoFrame)
        self.frame_label_top_btns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_label_top_btns)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(5, 0, 10, 0)
        self.frame_icon_top_bar = QFrame(self.frame_label_top_btns)
        self.frame_icon_top_bar.setObjectName(u"frame_icon_top_bar")
        self.frame_icon_top_bar.setMaximumSize(QSize(30, 30))
        self.frame_icon_top_bar.setStyleSheet(u"background: transparent;\n"
"background-image: url(:/16x16/icons/16x16/cil-terminal.png);\n"
"background-position: center;\n"
"background-repeat: no-repeat;\n"
"")
        self.frame_icon_top_bar.setFrameShape(QFrame.StyledPanel)
        self.frame_icon_top_bar.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_10.addWidget(self.frame_icon_top_bar)

        self.label_title_bar_top = QLabel(self.frame_label_top_btns)
        self.label_title_bar_top.setObjectName(u"label_title_bar_top")
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setWeight(75)
        self.label_title_bar_top.setFont(font1)
        self.label_title_bar_top.setStyleSheet(u"background: transparent;\n"
"")

        self.horizontalLayout_10.addWidget(self.label_title_bar_top)


        self.horizontalLayout_4.addWidget(self.frame_label_top_btns)

        self.frame_btns_right = QFrame(self.frame_top_btns)
        self.frame_btns_right.setObjectName(u"frame_btns_right")
        sizePolicy2.setHeightForWidth(self.frame_btns_right.sizePolicy().hasHeightForWidth())
        self.frame_btns_right.setSizePolicy(sizePolicy2)
        self.frame_btns_right.setMaximumSize(QSize(120, 16777215))
        self.frame_btns_right.setFrameShape(QFrame.NoFrame)
        self.frame_btns_right.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_btns_right)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.btn_minimize = QPushButton(self.frame_btns_right)
        self.btn_minimize.setObjectName(u"btn_minimize")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btn_minimize.sizePolicy().hasHeightForWidth())
        self.btn_minimize.setSizePolicy(sizePolicy3)
        self.btn_minimize.setMinimumSize(QSize(40, 0))
        self.btn_minimize.setMaximumSize(QSize(40, 16777215))
        self.btn_minimize.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon = QIcon()
        icon.addFile(u":/16x16/icons/16x16/cil-window-minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_minimize.setIcon(icon)

        self.horizontalLayout_5.addWidget(self.btn_minimize)

        self.btn_maximize_restore = QPushButton(self.frame_btns_right)
        self.btn_maximize_restore.setObjectName(u"btn_maximize_restore")
        sizePolicy3.setHeightForWidth(self.btn_maximize_restore.sizePolicy().hasHeightForWidth())
        self.btn_maximize_restore.setSizePolicy(sizePolicy3)
        self.btn_maximize_restore.setMinimumSize(QSize(40, 0))
        self.btn_maximize_restore.setMaximumSize(QSize(40, 16777215))
        self.btn_maximize_restore.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/16x16/icons/16x16/cil-window-maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_maximize_restore.setIcon(icon1)

        self.horizontalLayout_5.addWidget(self.btn_maximize_restore)

        self.btn_close = QPushButton(self.frame_btns_right)
        self.btn_close.setObjectName(u"btn_close")
        sizePolicy3.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy3)
        self.btn_close.setMinimumSize(QSize(40, 0))
        self.btn_close.setMaximumSize(QSize(40, 16777215))
        self.btn_close.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/16x16/icons/16x16/cil-x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon2)

        self.horizontalLayout_5.addWidget(self.btn_close)


        self.horizontalLayout_4.addWidget(self.frame_btns_right, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.frame_top_btns)

        self.frame_top_info = QFrame(self.frame_top_right)
        self.frame_top_info.setObjectName(u"frame_top_info")
        self.frame_top_info.setMaximumSize(QSize(16777215, 65))
        self.frame_top_info.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_top_info.setFrameShape(QFrame.NoFrame)
        self.frame_top_info.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_top_info)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(10, 0, 10, 0)
        self.label_top_info_1 = QLabel(self.frame_top_info)
        self.label_top_info_1.setObjectName(u"label_top_info_1")
        self.label_top_info_1.setMaximumSize(QSize(16777215, 15))
        font2 = QFont()
        font2.setFamily(u"Segoe UI")
        self.label_top_info_1.setFont(font2)
        self.label_top_info_1.setStyleSheet(u"color: rgb(98, 103, 111); ")

        self.horizontalLayout_8.addWidget(self.label_top_info_1)

        self.label_top_info_2 = QLabel(self.frame_top_info)
        self.label_top_info_2.setObjectName(u"label_top_info_2")
        self.label_top_info_2.setMinimumSize(QSize(0, 0))
        self.label_top_info_2.setMaximumSize(QSize(250, 20))
        font3 = QFont()
        font3.setFamily(u"Segoe UI")
        font3.setBold(True)
        font3.setWeight(75)
        self.label_top_info_2.setFont(font3)
        self.label_top_info_2.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.label_top_info_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_top_info_2)


        self.verticalLayout_2.addWidget(self.frame_top_info)


        self.horizontalLayout_3.addWidget(self.frame_top_right)


        self.verticalLayout.addWidget(self.frame_top)

        self.frame_center = QFrame(self.frame_main)
        self.frame_center.setObjectName(u"frame_center")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_center.sizePolicy().hasHeightForWidth())
        self.frame_center.setSizePolicy(sizePolicy4)
        self.frame_center.setStyleSheet(u"background-color: rgb(40, 44, 52);")
        self.frame_center.setFrameShape(QFrame.NoFrame)
        self.frame_center.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_center)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_left_menu = QFrame(self.frame_center)
        self.frame_left_menu.setObjectName(u"frame_left_menu")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.frame_left_menu.sizePolicy().hasHeightForWidth())
        self.frame_left_menu.setSizePolicy(sizePolicy5)
        self.frame_left_menu.setMinimumSize(QSize(70, 0))
        self.frame_left_menu.setMaximumSize(QSize(70, 16777215))
        self.frame_left_menu.setLayoutDirection(Qt.LeftToRight)
        self.frame_left_menu.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.frame_left_menu.setFrameShape(QFrame.NoFrame)
        self.frame_left_menu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_left_menu)
        self.verticalLayout_5.setSpacing(1)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_menus = QFrame(self.frame_left_menu)
        self.frame_menus.setObjectName(u"frame_menus")
        self.frame_menus.setFrameShape(QFrame.NoFrame)
        self.frame_menus.setFrameShadow(QFrame.Raised)
        self.layout_menus = QVBoxLayout(self.frame_menus)
        self.layout_menus.setSpacing(0)
        self.layout_menus.setObjectName(u"layout_menus")
        self.layout_menus.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_5.addWidget(self.frame_menus, 0, Qt.AlignTop)

        self.frame_extra_menus = QFrame(self.frame_left_menu)
        self.frame_extra_menus.setObjectName(u"frame_extra_menus")
        sizePolicy5.setHeightForWidth(self.frame_extra_menus.sizePolicy().hasHeightForWidth())
        self.frame_extra_menus.setSizePolicy(sizePolicy5)
        self.frame_extra_menus.setFrameShape(QFrame.NoFrame)
        self.frame_extra_menus.setFrameShadow(QFrame.Raised)
        self.layout_menu_bottom = QVBoxLayout(self.frame_extra_menus)
        self.layout_menu_bottom.setSpacing(10)
        self.layout_menu_bottom.setObjectName(u"layout_menu_bottom")
        self.layout_menu_bottom.setContentsMargins(0, 0, 0, 25)
        self.label_user_icon = QLabel(self.frame_extra_menus)
        self.label_user_icon.setObjectName(u"label_user_icon")
        sizePolicy6 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_user_icon.sizePolicy().hasHeightForWidth())
        self.label_user_icon.setSizePolicy(sizePolicy6)
        self.label_user_icon.setMinimumSize(QSize(60, 60))
        self.label_user_icon.setMaximumSize(QSize(60, 60))
        font4 = QFont()
        font4.setFamily(u"Segoe UI")
        font4.setPointSize(12)
        self.label_user_icon.setFont(font4)
        self.label_user_icon.setStyleSheet(u"QLabel {\n"
"	border-radius: 30px;\n"
"	background-color: rgb(44, 49, 60);\n"
"	border: 5px solid rgb(39, 44, 54);\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"}")
        self.label_user_icon.setAlignment(Qt.AlignCenter)

        self.layout_menu_bottom.addWidget(self.label_user_icon, 0, Qt.AlignHCenter)


        self.verticalLayout_5.addWidget(self.frame_extra_menus, 0, Qt.AlignBottom)


        self.horizontalLayout_2.addWidget(self.frame_left_menu)

        self.frame_content_right = QFrame(self.frame_center)
        self.frame_content_right.setObjectName(u"frame_content_right")
        self.frame_content_right.setStyleSheet(u"background-color: rgb(44, 49, 60);")
        self.frame_content_right.setFrameShape(QFrame.NoFrame)
        self.frame_content_right.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_content_right)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_content = QFrame(self.frame_content_right)
        self.frame_content.setObjectName(u"frame_content")
        self.frame_content.setEnabled(True)
        self.frame_content.setFrameShape(QFrame.NoFrame)
        self.frame_content.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_content)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.stackedWidget = QStackedWidget(self.frame_content)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMaximumSize(QSize(16777215, 16777215))
        font5 = QFont()
        font5.setPointSize(14)
        self.stackedWidget.setFont(font5)
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        self.gridLayout_31 = QGridLayout(self.page_home)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.verticalSpacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_31.addItem(self.verticalSpacer, 3, 0, 1, 3)

        self.btn_page_test_results = QPushButton(self.page_home)
        self.btn_page_test_results.setObjectName(u"btn_page_test_results")
        sizePolicy7 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(1)
        sizePolicy7.setVerticalStretch(1)
        sizePolicy7.setHeightForWidth(self.btn_page_test_results.sizePolicy().hasHeightForWidth())
        self.btn_page_test_results.setSizePolicy(sizePolicy7)
        self.btn_page_test_results.setMinimumSize(QSize(100, 125))
        font6 = QFont()
        font6.setFamily(u"Segoe UI")
        font6.setPointSize(18)
        self.btn_page_test_results.setFont(font6)
        self.btn_page_test_results.setStyleSheet(u"QPushButton {\n"
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
        icon3 = QIcon()
        icon3.addFile(u":/20x20/icons/20x20/cil-library.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_page_test_results.setIcon(icon3)
        self.btn_page_test_results.setIconSize(QSize(20, 20))
        self.btn_page_test_results.setCheckable(False)
        self.btn_page_test_results.setChecked(False)

        self.gridLayout_31.addWidget(self.btn_page_test_results, 8, 1, 1, 1)

        self.btn_page_manual_control = QPushButton(self.page_home)
        self.btn_page_manual_control.setObjectName(u"btn_page_manual_control")
        sizePolicy7.setHeightForWidth(self.btn_page_manual_control.sizePolicy().hasHeightForWidth())
        self.btn_page_manual_control.setSizePolicy(sizePolicy7)
        self.btn_page_manual_control.setMinimumSize(QSize(100, 125))
        self.btn_page_manual_control.setFont(font6)
        self.btn_page_manual_control.setStyleSheet(u"QPushButton {\n"
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
        icon4 = QIcon()
        icon4.addFile(u":/20x20/icons/20x20/cil-touch-app.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_page_manual_control.setIcon(icon4)
        self.btn_page_manual_control.setIconSize(QSize(20, 20))
        self.btn_page_manual_control.setCheckable(False)
        self.btn_page_manual_control.setChecked(False)

        self.gridLayout_31.addWidget(self.btn_page_manual_control, 5, 1, 1, 1)

        self.btn_page_equipment_setup = QPushButton(self.page_home)
        self.btn_page_equipment_setup.setObjectName(u"btn_page_equipment_setup")
        sizePolicy7.setHeightForWidth(self.btn_page_equipment_setup.sizePolicy().hasHeightForWidth())
        self.btn_page_equipment_setup.setSizePolicy(sizePolicy7)
        self.btn_page_equipment_setup.setMinimumSize(QSize(100, 125))
        self.btn_page_equipment_setup.setFont(font6)
        self.btn_page_equipment_setup.setStyleSheet(u"QPushButton {\n"
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
        icon5 = QIcon()
        icon5.addFile(u":/20x20/icons/20x20/cil-equalizer.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_page_equipment_setup.setIcon(icon5)
        self.btn_page_equipment_setup.setIconSize(QSize(20, 20))
        self.btn_page_equipment_setup.setCheckable(False)
        self.btn_page_equipment_setup.setChecked(False)

        self.gridLayout_31.addWidget(self.btn_page_equipment_setup, 4, 1, 1, 1)

        self.label_7 = QLabel(self.page_home)
        self.label_7.setObjectName(u"label_7")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(1)
        sizePolicy8.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy8)
        font7 = QFont()
        font7.setFamily(u"Segoe UI")
        font7.setPointSize(15)
        self.label_7.setFont(font7)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_31.addWidget(self.label_7, 12, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(500, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_31.addItem(self.horizontalSpacer_2, 4, 0, 8, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_31.addItem(self.verticalSpacer_2, 1, 0, 1, 3)

        self.label_6 = QLabel(self.page_home)
        self.label_6.setObjectName(u"label_6")
        sizePolicy8.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy8)
        font8 = QFont()
        font8.setFamily(u"Segoe UI")
        font8.setPointSize(40)
        self.label_6.setFont(font8)
        self.label_6.setStyleSheet(u"")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_31.addWidget(self.label_6, 2, 0, 1, 3)

        self.btn_page_i2c_controls = QPushButton(self.page_home)
        self.btn_page_i2c_controls.setObjectName(u"btn_page_i2c_controls")
        sizePolicy7.setHeightForWidth(self.btn_page_i2c_controls.sizePolicy().hasHeightForWidth())
        self.btn_page_i2c_controls.setSizePolicy(sizePolicy7)
        self.btn_page_i2c_controls.setMinimumSize(QSize(100, 125))
        self.btn_page_i2c_controls.setFont(font6)
        self.btn_page_i2c_controls.setStyleSheet(u"QPushButton {\n"
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
        icon6 = QIcon()
        icon6.addFile(u":/20x20/icons/20x20/cil-lightbulb.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_page_i2c_controls.setIcon(icon6)
        self.btn_page_i2c_controls.setIconSize(QSize(20, 20))
        self.btn_page_i2c_controls.setCheckable(False)
        self.btn_page_i2c_controls.setChecked(False)

        self.gridLayout_31.addWidget(self.btn_page_i2c_controls, 6, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(500, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_31.addItem(self.horizontalSpacer, 4, 2, 8, 1)

        self.btn_page_add_tests = QPushButton(self.page_home)
        self.btn_page_add_tests.setObjectName(u"btn_page_add_tests")
        sizePolicy7.setHeightForWidth(self.btn_page_add_tests.sizePolicy().hasHeightForWidth())
        self.btn_page_add_tests.setSizePolicy(sizePolicy7)
        self.btn_page_add_tests.setMinimumSize(QSize(100, 125))
        self.btn_page_add_tests.setFont(font6)
        self.btn_page_add_tests.setStyleSheet(u"QPushButton {\n"
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
        icon7 = QIcon()
        icon7.addFile(u":/20x20/icons/20x20/cil-library-add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_page_add_tests.setIcon(icon7)
        self.btn_page_add_tests.setIconSize(QSize(20, 20))
        self.btn_page_add_tests.setCheckable(False)
        self.btn_page_add_tests.setChecked(False)

        self.gridLayout_31.addWidget(self.btn_page_add_tests, 7, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_home)
        self.page_equipment_setup = QWidget()
        self.page_equipment_setup.setObjectName(u"page_equipment_setup")
        self.horizontalLayout_21 = QHBoxLayout(self.page_equipment_setup)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.frame_equip_setup = QFrame(self.page_equipment_setup)
        self.frame_equip_setup.setObjectName(u"frame_equip_setup")
        self.frame_equip_setup.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup.setFrameShadow(QFrame.Raised)
        self.verticalLayout_51 = QVBoxLayout(self.frame_equip_setup)
        self.verticalLayout_51.setSpacing(0)
        self.verticalLayout_51.setObjectName(u"verticalLayout_51")
        self.verticalLayout_51.setContentsMargins(0, 0, 0, 0)
        self.frame_equip_setup_top = QFrame(self.frame_equip_setup)
        self.frame_equip_setup_top.setObjectName(u"frame_equip_setup_top")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(4)
        sizePolicy9.setHeightForWidth(self.frame_equip_setup_top.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_top.setSizePolicy(sizePolicy9)
        self.frame_equip_setup_top.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_equip_setup_top)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.frame_equip_setup_sources = QFrame(self.frame_equip_setup_top)
        self.frame_equip_setup_sources.setObjectName(u"frame_equip_setup_sources")
        sizePolicy10 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy10.setHorizontalStretch(1)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.frame_equip_setup_sources.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_sources.setSizePolicy(sizePolicy10)
        self.frame_equip_setup_sources.setMinimumSize(QSize(400, 0))
        self.frame_equip_setup_sources.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_equip_setup_sources.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_sources.setFrameShadow(QFrame.Raised)
        self.verticalLayout_38 = QVBoxLayout(self.frame_equip_setup_sources)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.label_equip_setup_sources = QLabel(self.frame_equip_setup_sources)
        self.label_equip_setup_sources.setObjectName(u"label_equip_setup_sources")
        self.label_equip_setup_sources.setMaximumSize(QSize(16777215, 30))
        font9 = QFont()
        font9.setFamily(u"Segoe UI")
        font9.setPointSize(14)
        font9.setBold(True)
        font9.setWeight(75)
        self.label_equip_setup_sources.setFont(font9)
        self.label_equip_setup_sources.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_sources.setStyleSheet(u"border:none;")
        self.label_equip_setup_sources.setAlignment(Qt.AlignCenter)

        self.verticalLayout_38.addWidget(self.label_equip_setup_sources)

        self.frame_equip_setup_sources_contents = QFrame(self.frame_equip_setup_sources)
        self.frame_equip_setup_sources_contents.setObjectName(u"frame_equip_setup_sources_contents")
        self.frame_equip_setup_sources_contents.setStyleSheet(u"border:none;")
        self.frame_equip_setup_sources_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_sources_contents.setFrameShadow(QFrame.Raised)
        self.verticalLayout_58 = QVBoxLayout(self.frame_equip_setup_sources_contents)
        self.verticalLayout_58.setObjectName(u"verticalLayout_58")
        self.frame_equip_setup_sources_acsource = QFrame(self.frame_equip_setup_sources_contents)
        self.frame_equip_setup_sources_acsource.setObjectName(u"frame_equip_setup_sources_acsource")
        self.frame_equip_setup_sources_acsource.setStyleSheet(u"QFrame{\n"
"	border: 1px solid black;\n"
"\n"
"}")
        self.frame_equip_setup_sources_acsource.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_sources_acsource.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.frame_equip_setup_sources_acsource)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.label_equip_setup_sources_acsource = QLabel(self.frame_equip_setup_sources_acsource)
        self.label_equip_setup_sources_acsource.setObjectName(u"label_equip_setup_sources_acsource")
        self.label_equip_setup_sources_acsource.setMaximumSize(QSize(100, 30))
        self.label_equip_setup_sources_acsource.setFont(font1)
        self.label_equip_setup_sources_acsource.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_sources_acsource.setStyleSheet(u"border:none;")
        self.label_equip_setup_sources_acsource.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_29.addWidget(self.label_equip_setup_sources_acsource)

        self.frame_equip_setup_sources_acsource_details = QFrame(self.frame_equip_setup_sources_acsource)
        self.frame_equip_setup_sources_acsource_details.setObjectName(u"frame_equip_setup_sources_acsource_details")
        self.frame_equip_setup_sources_acsource_details.setStyleSheet(u"border: None;")
        self.frame_equip_setup_sources_acsource_details.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_sources_acsource_details.setFrameShadow(QFrame.Raised)
        self.verticalLayout_52 = QVBoxLayout(self.frame_equip_setup_sources_acsource_details)
        self.verticalLayout_52.setObjectName(u"verticalLayout_52")
        self.cbx_equip_setup_sources_acsource = QComboBox(self.frame_equip_setup_sources_acsource_details)
        self.cbx_equip_setup_sources_acsource.setObjectName(u"cbx_equip_setup_sources_acsource")
        self.cbx_equip_setup_sources_acsource.setMaximumSize(QSize(16777215, 40))
        font10 = QFont()
        font10.setPointSize(12)
        self.cbx_equip_setup_sources_acsource.setFont(font10)
        self.cbx_equip_setup_sources_acsource.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.verticalLayout_52.addWidget(self.cbx_equip_setup_sources_acsource)

        self.label_equip_setup_sources_acsource_details = QLabel(self.frame_equip_setup_sources_acsource_details)
        self.label_equip_setup_sources_acsource_details.setObjectName(u"label_equip_setup_sources_acsource_details")
        sizePolicy.setHeightForWidth(self.label_equip_setup_sources_acsource_details.sizePolicy().hasHeightForWidth())
        self.label_equip_setup_sources_acsource_details.setSizePolicy(sizePolicy)
        self.label_equip_setup_sources_acsource_details.setMaximumSize(QSize(16777215, 16777215))
        font11 = QFont()
        font11.setFamily(u"Segoe UI")
        font11.setPointSize(10)
        font11.setBold(False)
        font11.setWeight(50)
        self.label_equip_setup_sources_acsource_details.setFont(font11)
        self.label_equip_setup_sources_acsource_details.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_sources_acsource_details.setStyleSheet(u"border:none;")
        self.label_equip_setup_sources_acsource_details.setAlignment(Qt.AlignCenter)

        self.verticalLayout_52.addWidget(self.label_equip_setup_sources_acsource_details)


        self.horizontalLayout_29.addWidget(self.frame_equip_setup_sources_acsource_details)


        self.verticalLayout_58.addWidget(self.frame_equip_setup_sources_acsource)

        self.frame_equip_setup_sources_dcsource = QFrame(self.frame_equip_setup_sources_contents)
        self.frame_equip_setup_sources_dcsource.setObjectName(u"frame_equip_setup_sources_dcsource")
        self.frame_equip_setup_sources_dcsource.setStyleSheet(u"QFrame{\n"
"	border: 1px solid black;\n"
"\n"
"}")
        self.frame_equip_setup_sources_dcsource.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_sources_dcsource.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_35 = QHBoxLayout(self.frame_equip_setup_sources_dcsource)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.label_equip_setup_sources_dcsource = QLabel(self.frame_equip_setup_sources_dcsource)
        self.label_equip_setup_sources_dcsource.setObjectName(u"label_equip_setup_sources_dcsource")
        self.label_equip_setup_sources_dcsource.setMaximumSize(QSize(100, 30))
        self.label_equip_setup_sources_dcsource.setFont(font1)
        self.label_equip_setup_sources_dcsource.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_sources_dcsource.setStyleSheet(u"border:none;")
        self.label_equip_setup_sources_dcsource.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_35.addWidget(self.label_equip_setup_sources_dcsource)

        self.frame_equip_setup_sources_dcsource_contents = QFrame(self.frame_equip_setup_sources_dcsource)
        self.frame_equip_setup_sources_dcsource_contents.setObjectName(u"frame_equip_setup_sources_dcsource_contents")
        self.frame_equip_setup_sources_dcsource_contents.setStyleSheet(u"border: None;")
        self.frame_equip_setup_sources_dcsource_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_sources_dcsource_contents.setFrameShadow(QFrame.Raised)
        self.verticalLayout_56 = QVBoxLayout(self.frame_equip_setup_sources_dcsource_contents)
        self.verticalLayout_56.setObjectName(u"verticalLayout_56")
        self.cbx_equip_setup_sources_dcsource = QComboBox(self.frame_equip_setup_sources_dcsource_contents)
        self.cbx_equip_setup_sources_dcsource.setObjectName(u"cbx_equip_setup_sources_dcsource")
        self.cbx_equip_setup_sources_dcsource.setMaximumSize(QSize(16777215, 40))
        self.cbx_equip_setup_sources_dcsource.setFont(font10)
        self.cbx_equip_setup_sources_dcsource.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.verticalLayout_56.addWidget(self.cbx_equip_setup_sources_dcsource)

        self.label_equip_setup_sources_dcsource_details = QLabel(self.frame_equip_setup_sources_dcsource_contents)
        self.label_equip_setup_sources_dcsource_details.setObjectName(u"label_equip_setup_sources_dcsource_details")
        sizePolicy.setHeightForWidth(self.label_equip_setup_sources_dcsource_details.sizePolicy().hasHeightForWidth())
        self.label_equip_setup_sources_dcsource_details.setSizePolicy(sizePolicy)
        self.label_equip_setup_sources_dcsource_details.setMaximumSize(QSize(16777215, 16777215))
        self.label_equip_setup_sources_dcsource_details.setFont(font11)
        self.label_equip_setup_sources_dcsource_details.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_sources_dcsource_details.setStyleSheet(u"border:none;")
        self.label_equip_setup_sources_dcsource_details.setAlignment(Qt.AlignCenter)

        self.verticalLayout_56.addWidget(self.label_equip_setup_sources_dcsource_details)


        self.horizontalLayout_35.addWidget(self.frame_equip_setup_sources_dcsource_contents)


        self.verticalLayout_58.addWidget(self.frame_equip_setup_sources_dcsource)


        self.verticalLayout_38.addWidget(self.frame_equip_setup_sources_contents)


        self.horizontalLayout_23.addWidget(self.frame_equip_setup_sources)

        self.frame_equip_setup_top_middle = QFrame(self.frame_equip_setup_top)
        self.frame_equip_setup_top_middle.setObjectName(u"frame_equip_setup_top_middle")
        sizePolicy11 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy11.setHorizontalStretch(1)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.frame_equip_setup_top_middle.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_top_middle.setSizePolicy(sizePolicy11)
        self.frame_equip_setup_top_middle.setLayoutDirection(Qt.LeftToRight)
        self.frame_equip_setup_top_middle.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_top_middle.setFrameShadow(QFrame.Raised)
        self.frame_equip_setup_top_middle.setLineWidth(0)
        self.verticalLayout_61 = QVBoxLayout(self.frame_equip_setup_top_middle)
        self.verticalLayout_61.setSpacing(6)
        self.verticalLayout_61.setObjectName(u"verticalLayout_61")
        self.verticalLayout_61.setContentsMargins(0, 0, 0, 0)
        self.frame_equip_setup_sinkcontroller = QFrame(self.frame_equip_setup_top_middle)
        self.frame_equip_setup_sinkcontroller.setObjectName(u"frame_equip_setup_sinkcontroller")
        sizePolicy12 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.frame_equip_setup_sinkcontroller.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_sinkcontroller.setSizePolicy(sizePolicy12)
        self.frame_equip_setup_sinkcontroller.setMinimumSize(QSize(400, 0))
        self.frame_equip_setup_sinkcontroller.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_equip_setup_sinkcontroller.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_sinkcontroller.setFrameShadow(QFrame.Raised)
        self.verticalLayout_55 = QVBoxLayout(self.frame_equip_setup_sinkcontroller)
        self.verticalLayout_55.setObjectName(u"verticalLayout_55")
        self.label_equip_setup_sinkcontroller = QLabel(self.frame_equip_setup_sinkcontroller)
        self.label_equip_setup_sinkcontroller.setObjectName(u"label_equip_setup_sinkcontroller")
        self.label_equip_setup_sinkcontroller.setMaximumSize(QSize(16777215, 30))
        self.label_equip_setup_sinkcontroller.setFont(font9)
        self.label_equip_setup_sinkcontroller.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_sinkcontroller.setStyleSheet(u"border:none;")
        self.label_equip_setup_sinkcontroller.setAlignment(Qt.AlignCenter)

        self.verticalLayout_55.addWidget(self.label_equip_setup_sinkcontroller)

        self.frame_equip_setup_sinkcontroller_contents = QFrame(self.frame_equip_setup_sinkcontroller)
        self.frame_equip_setup_sinkcontroller_contents.setObjectName(u"frame_equip_setup_sinkcontroller_contents")
        self.frame_equip_setup_sinkcontroller_contents.setStyleSheet(u"border: 1px solid black;")
        self.frame_equip_setup_sinkcontroller_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_sinkcontroller_contents.setFrameShadow(QFrame.Raised)
        self.verticalLayout_60 = QVBoxLayout(self.frame_equip_setup_sinkcontroller_contents)
        self.verticalLayout_60.setObjectName(u"verticalLayout_60")
        self.frame_equip_setup_sinkcontroller_details = QFrame(self.frame_equip_setup_sinkcontroller_contents)
        self.frame_equip_setup_sinkcontroller_details.setObjectName(u"frame_equip_setup_sinkcontroller_details")
        self.frame_equip_setup_sinkcontroller_details.setStyleSheet(u"border:none;")
        self.frame_equip_setup_sinkcontroller_details.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_sinkcontroller_details.setFrameShadow(QFrame.Raised)
        self.gridLayout_27 = QGridLayout(self.frame_equip_setup_sinkcontroller_details)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.gridLayout_27.setContentsMargins(0, 0, 0, 0)
        self.label_equip_setup_sinkcontrollerdetails = QLabel(self.frame_equip_setup_sinkcontroller_details)
        self.label_equip_setup_sinkcontrollerdetails.setObjectName(u"label_equip_setup_sinkcontrollerdetails")
        sizePolicy13 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy13.setHorizontalStretch(2)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.label_equip_setup_sinkcontrollerdetails.sizePolicy().hasHeightForWidth())
        self.label_equip_setup_sinkcontrollerdetails.setSizePolicy(sizePolicy13)
        self.label_equip_setup_sinkcontrollerdetails.setMaximumSize(QSize(16777215, 16777215))
        self.label_equip_setup_sinkcontrollerdetails.setFont(font11)
        self.label_equip_setup_sinkcontrollerdetails.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_sinkcontrollerdetails.setStyleSheet(u"border:none;")
        self.label_equip_setup_sinkcontrollerdetails.setAlignment(Qt.AlignCenter)

        self.gridLayout_27.addWidget(self.label_equip_setup_sinkcontrollerdetails, 2, 0, 1, 1)

        self.cbx_equip_setup_sinkcontroller = QComboBox(self.frame_equip_setup_sinkcontroller_details)
        self.cbx_equip_setup_sinkcontroller.setObjectName(u"cbx_equip_setup_sinkcontroller")
        sizePolicy14 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy14.setHorizontalStretch(2)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.cbx_equip_setup_sinkcontroller.sizePolicy().hasHeightForWidth())
        self.cbx_equip_setup_sinkcontroller.setSizePolicy(sizePolicy14)
        self.cbx_equip_setup_sinkcontroller.setMaximumSize(QSize(16777215, 40))
        self.cbx_equip_setup_sinkcontroller.setFont(font10)
        self.cbx_equip_setup_sinkcontroller.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.gridLayout_27.addWidget(self.cbx_equip_setup_sinkcontroller, 0, 0, 1, 1)

        self.cbx_equip_setup_i2ccontroller = QComboBox(self.frame_equip_setup_sinkcontroller_details)
        self.cbx_equip_setup_i2ccontroller.setObjectName(u"cbx_equip_setup_i2ccontroller")
        sizePolicy14.setHeightForWidth(self.cbx_equip_setup_i2ccontroller.sizePolicy().hasHeightForWidth())
        self.cbx_equip_setup_i2ccontroller.setSizePolicy(sizePolicy14)
        self.cbx_equip_setup_i2ccontroller.setMaximumSize(QSize(16777215, 40))
        self.cbx_equip_setup_i2ccontroller.setFont(font10)
        self.cbx_equip_setup_i2ccontroller.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.gridLayout_27.addWidget(self.cbx_equip_setup_i2ccontroller, 0, 1, 1, 1)

        self.label_equip_setup_i2ccontrollerdetails = QLabel(self.frame_equip_setup_sinkcontroller_details)
        self.label_equip_setup_i2ccontrollerdetails.setObjectName(u"label_equip_setup_i2ccontrollerdetails")
        sizePolicy13.setHeightForWidth(self.label_equip_setup_i2ccontrollerdetails.sizePolicy().hasHeightForWidth())
        self.label_equip_setup_i2ccontrollerdetails.setSizePolicy(sizePolicy13)
        self.label_equip_setup_i2ccontrollerdetails.setMaximumSize(QSize(16777215, 16777215))
        self.label_equip_setup_i2ccontrollerdetails.setFont(font11)
        self.label_equip_setup_i2ccontrollerdetails.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_i2ccontrollerdetails.setStyleSheet(u"border:none;")
        self.label_equip_setup_i2ccontrollerdetails.setAlignment(Qt.AlignCenter)

        self.gridLayout_27.addWidget(self.label_equip_setup_i2ccontrollerdetails, 2, 1, 1, 1)

        self.btn_equip_setup_sinkcontroller_check_availability = QPushButton(self.frame_equip_setup_sinkcontroller_details)
        self.btn_equip_setup_sinkcontroller_check_availability.setObjectName(u"btn_equip_setup_sinkcontroller_check_availability")
        sizePolicy15 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy15.setHorizontalStretch(1)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.btn_equip_setup_sinkcontroller_check_availability.sizePolicy().hasHeightForWidth())
        self.btn_equip_setup_sinkcontroller_check_availability.setSizePolicy(sizePolicy15)
        self.btn_equip_setup_sinkcontroller_check_availability.setMinimumSize(QSize(0, 40))
        self.btn_equip_setup_sinkcontroller_check_availability.setMaximumSize(QSize(16777215, 16777215))
        self.btn_equip_setup_sinkcontroller_check_availability.setFont(font10)
        self.btn_equip_setup_sinkcontroller_check_availability.setStyleSheet(u"QPushButton {\n"
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

        self.gridLayout_27.addWidget(self.btn_equip_setup_sinkcontroller_check_availability, 1, 0, 1, 2)


        self.verticalLayout_60.addWidget(self.frame_equip_setup_sinkcontroller_details)


        self.verticalLayout_55.addWidget(self.frame_equip_setup_sinkcontroller_contents)


        self.verticalLayout_61.addWidget(self.frame_equip_setup_sinkcontroller)

        self.frame_equip_setup_oscilloscope = QFrame(self.frame_equip_setup_top_middle)
        self.frame_equip_setup_oscilloscope.setObjectName(u"frame_equip_setup_oscilloscope")
        sizePolicy12.setHeightForWidth(self.frame_equip_setup_oscilloscope.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_oscilloscope.setSizePolicy(sizePolicy12)
        self.frame_equip_setup_oscilloscope.setMinimumSize(QSize(500, 0))
        self.frame_equip_setup_oscilloscope.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_equip_setup_oscilloscope.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_oscilloscope.setFrameShadow(QFrame.Raised)
        self.verticalLayout_59 = QVBoxLayout(self.frame_equip_setup_oscilloscope)
        self.verticalLayout_59.setObjectName(u"verticalLayout_59")
        self.label_equip_setup_oscilloscope = QLabel(self.frame_equip_setup_oscilloscope)
        self.label_equip_setup_oscilloscope.setObjectName(u"label_equip_setup_oscilloscope")
        self.label_equip_setup_oscilloscope.setMaximumSize(QSize(16777215, 30))
        self.label_equip_setup_oscilloscope.setFont(font9)
        self.label_equip_setup_oscilloscope.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_oscilloscope.setStyleSheet(u"border:none;")
        self.label_equip_setup_oscilloscope.setAlignment(Qt.AlignCenter)

        self.verticalLayout_59.addWidget(self.label_equip_setup_oscilloscope)

        self.frame_equip_setup_oscilloscope_contents = QFrame(self.frame_equip_setup_oscilloscope)
        self.frame_equip_setup_oscilloscope_contents.setObjectName(u"frame_equip_setup_oscilloscope_contents")
        self.frame_equip_setup_oscilloscope_contents.setStyleSheet(u"border: 1px solid black;")
        self.frame_equip_setup_oscilloscope_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_oscilloscope_contents.setFrameShadow(QFrame.Raised)
        self.verticalLayout_62 = QVBoxLayout(self.frame_equip_setup_oscilloscope_contents)
        self.verticalLayout_62.setObjectName(u"verticalLayout_62")
        self.lineedit_equip_setup_oscilloscope = QLineEdit(self.frame_equip_setup_oscilloscope_contents)
        self.lineedit_equip_setup_oscilloscope.setObjectName(u"lineedit_equip_setup_oscilloscope")
        self.lineedit_equip_setup_oscilloscope.setMinimumSize(QSize(0, 30))
        self.lineedit_equip_setup_oscilloscope.setFont(font10)
        self.lineedit_equip_setup_oscilloscope.setStyleSheet(u"QLineEdit {\n"
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
"}")

        self.verticalLayout_62.addWidget(self.lineedit_equip_setup_oscilloscope)

        self.frame_equip_setup_oscilloscope_details = QFrame(self.frame_equip_setup_oscilloscope_contents)
        self.frame_equip_setup_oscilloscope_details.setObjectName(u"frame_equip_setup_oscilloscope_details")
        self.frame_equip_setup_oscilloscope_details.setStyleSheet(u"border:none;")
        self.frame_equip_setup_oscilloscope_details.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_oscilloscope_details.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_55 = QHBoxLayout(self.frame_equip_setup_oscilloscope_details)
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.horizontalLayout_55.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_62.addWidget(self.frame_equip_setup_oscilloscope_details)

        self.btn_equip_setup_oscilloscope_check_availability = QPushButton(self.frame_equip_setup_oscilloscope_contents)
        self.btn_equip_setup_oscilloscope_check_availability.setObjectName(u"btn_equip_setup_oscilloscope_check_availability")
        sizePolicy15.setHeightForWidth(self.btn_equip_setup_oscilloscope_check_availability.sizePolicy().hasHeightForWidth())
        self.btn_equip_setup_oscilloscope_check_availability.setSizePolicy(sizePolicy15)
        self.btn_equip_setup_oscilloscope_check_availability.setMinimumSize(QSize(0, 40))
        self.btn_equip_setup_oscilloscope_check_availability.setMaximumSize(QSize(16777215, 16777215))
        self.btn_equip_setup_oscilloscope_check_availability.setFont(font10)
        self.btn_equip_setup_oscilloscope_check_availability.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_62.addWidget(self.btn_equip_setup_oscilloscope_check_availability)

        self.label_equip_setup_oscilloscope_details = QLabel(self.frame_equip_setup_oscilloscope_contents)
        self.label_equip_setup_oscilloscope_details.setObjectName(u"label_equip_setup_oscilloscope_details")
        sizePolicy13.setHeightForWidth(self.label_equip_setup_oscilloscope_details.sizePolicy().hasHeightForWidth())
        self.label_equip_setup_oscilloscope_details.setSizePolicy(sizePolicy13)
        self.label_equip_setup_oscilloscope_details.setMaximumSize(QSize(16777215, 16777215))
        self.label_equip_setup_oscilloscope_details.setFont(font11)
        self.label_equip_setup_oscilloscope_details.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_oscilloscope_details.setStyleSheet(u"border:none;")
        self.label_equip_setup_oscilloscope_details.setAlignment(Qt.AlignCenter)

        self.verticalLayout_62.addWidget(self.label_equip_setup_oscilloscope_details)


        self.verticalLayout_59.addWidget(self.frame_equip_setup_oscilloscope_contents)


        self.verticalLayout_61.addWidget(self.frame_equip_setup_oscilloscope)


        self.horizontalLayout_23.addWidget(self.frame_equip_setup_top_middle)

        self.frame_equip_setup_top_right = QFrame(self.frame_equip_setup_top)
        self.frame_equip_setup_top_right.setObjectName(u"frame_equip_setup_top_right")
        sizePolicy10.setHeightForWidth(self.frame_equip_setup_top_right.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_top_right.setSizePolicy(sizePolicy10)
        self.frame_equip_setup_top_right.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_top_right.setFrameShadow(QFrame.Raised)
        self.verticalLayout_67 = QVBoxLayout(self.frame_equip_setup_top_right)
        self.verticalLayout_67.setObjectName(u"verticalLayout_67")
        self.verticalLayout_67.setContentsMargins(0, 0, 0, 0)
        self.frame_equip_setup_settings = QFrame(self.frame_equip_setup_top_right)
        self.frame_equip_setup_settings.setObjectName(u"frame_equip_setup_settings")
        sizePolicy12.setHeightForWidth(self.frame_equip_setup_settings.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_settings.setSizePolicy(sizePolicy12)
        self.frame_equip_setup_settings.setMinimumSize(QSize(400, 0))
        self.frame_equip_setup_settings.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_equip_setup_settings.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_settings.setFrameShadow(QFrame.Raised)
        self.verticalLayout_63 = QVBoxLayout(self.frame_equip_setup_settings)
        self.verticalLayout_63.setObjectName(u"verticalLayout_63")
        self.label_equip_setup_settings_contents = QLabel(self.frame_equip_setup_settings)
        self.label_equip_setup_settings_contents.setObjectName(u"label_equip_setup_settings_contents")
        self.label_equip_setup_settings_contents.setMaximumSize(QSize(16777215, 30))
        self.label_equip_setup_settings_contents.setFont(font9)
        self.label_equip_setup_settings_contents.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_settings_contents.setStyleSheet(u"border:none;")
        self.label_equip_setup_settings_contents.setAlignment(Qt.AlignCenter)

        self.verticalLayout_63.addWidget(self.label_equip_setup_settings_contents)

        self.frame_equip_setup_settings_contents = QFrame(self.frame_equip_setup_settings)
        self.frame_equip_setup_settings_contents.setObjectName(u"frame_equip_setup_settings_contents")
        self.frame_equip_setup_settings_contents.setStyleSheet(u"border:none;")
        self.frame_equip_setup_settings_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_settings_contents.setFrameShadow(QFrame.Raised)
        self.verticalLayout_64 = QVBoxLayout(self.frame_equip_setup_settings_contents)
        self.verticalLayout_64.setObjectName(u"verticalLayout_64")
        self.btn_equip_setup_previous_pag = QPushButton(self.frame_equip_setup_settings_contents)
        self.btn_equip_setup_previous_pag.setObjectName(u"btn_equip_setup_previous_pag")
        self.btn_equip_setup_previous_pag.setMinimumSize(QSize(0, 40))
        self.btn_equip_setup_previous_pag.setFont(font10)
        self.btn_equip_setup_previous_pag.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_64.addWidget(self.btn_equip_setup_previous_pag)


        self.verticalLayout_63.addWidget(self.frame_equip_setup_settings_contents)


        self.verticalLayout_67.addWidget(self.frame_equip_setup_settings)

        self.frame_equip_setup_detect = QFrame(self.frame_equip_setup_top_right)
        self.frame_equip_setup_detect.setObjectName(u"frame_equip_setup_detect")
        sizePolicy12.setHeightForWidth(self.frame_equip_setup_detect.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_detect.setSizePolicy(sizePolicy12)
        self.frame_equip_setup_detect.setMinimumSize(QSize(400, 0))
        self.frame_equip_setup_detect.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_equip_setup_detect.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_detect.setFrameShadow(QFrame.Raised)
        self.verticalLayout_65 = QVBoxLayout(self.frame_equip_setup_detect)
        self.verticalLayout_65.setObjectName(u"verticalLayout_65")
        self.label_equip_setup_detect = QLabel(self.frame_equip_setup_detect)
        self.label_equip_setup_detect.setObjectName(u"label_equip_setup_detect")
        self.label_equip_setup_detect.setMaximumSize(QSize(16777215, 30))
        self.label_equip_setup_detect.setFont(font9)
        self.label_equip_setup_detect.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_detect.setStyleSheet(u"border:none;")
        self.label_equip_setup_detect.setAlignment(Qt.AlignCenter)

        self.verticalLayout_65.addWidget(self.label_equip_setup_detect)

        self.frame_equip_setup_detect_contents = QFrame(self.frame_equip_setup_detect)
        self.frame_equip_setup_detect_contents.setObjectName(u"frame_equip_setup_detect_contents")
        self.frame_equip_setup_detect_contents.setStyleSheet(u"border:none;")
        self.frame_equip_setup_detect_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_detect_contents.setFrameShadow(QFrame.Raised)
        self.verticalLayout_66 = QVBoxLayout(self.frame_equip_setup_detect_contents)
        self.verticalLayout_66.setObjectName(u"verticalLayout_66")
        self.btn_equip_setup_detect_equipment = QPushButton(self.frame_equip_setup_detect_contents)
        self.btn_equip_setup_detect_equipment.setObjectName(u"btn_equip_setup_detect_equipment")
        self.btn_equip_setup_detect_equipment.setMinimumSize(QSize(0, 80))
        self.btn_equip_setup_detect_equipment.setFont(font10)
        self.btn_equip_setup_detect_equipment.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_66.addWidget(self.btn_equip_setup_detect_equipment)


        self.verticalLayout_65.addWidget(self.frame_equip_setup_detect_contents)


        self.verticalLayout_67.addWidget(self.frame_equip_setup_detect)


        self.horizontalLayout_23.addWidget(self.frame_equip_setup_top_right)


        self.verticalLayout_51.addWidget(self.frame_equip_setup_top)

        self.frame_equip_setup_bot = QFrame(self.frame_equip_setup)
        self.frame_equip_setup_bot.setObjectName(u"frame_equip_setup_bot")
        sizePolicy16 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy16.setHorizontalStretch(0)
        sizePolicy16.setVerticalStretch(5)
        sizePolicy16.setHeightForWidth(self.frame_equip_setup_bot.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_bot.setSizePolicy(sizePolicy16)
        self.frame_equip_setup_bot.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_bot.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.frame_equip_setup_bot)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(0, 3, 0, 0)
        self.frame_equip_setup_power_meters = QFrame(self.frame_equip_setup_bot)
        self.frame_equip_setup_power_meters.setObjectName(u"frame_equip_setup_power_meters")
        sizePolicy10.setHeightForWidth(self.frame_equip_setup_power_meters.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_power_meters.setSizePolicy(sizePolicy10)
        self.frame_equip_setup_power_meters.setMinimumSize(QSize(400, 0))
        self.frame_equip_setup_power_meters.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_equip_setup_power_meters.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_power_meters.setFrameShadow(QFrame.Raised)
        self.verticalLayout_53 = QVBoxLayout(self.frame_equip_setup_power_meters)
        self.verticalLayout_53.setObjectName(u"verticalLayout_53")
        self.label_equip_setup_power_meters = QLabel(self.frame_equip_setup_power_meters)
        self.label_equip_setup_power_meters.setObjectName(u"label_equip_setup_power_meters")
        self.label_equip_setup_power_meters.setMaximumSize(QSize(16777215, 30))
        self.label_equip_setup_power_meters.setFont(font9)
        self.label_equip_setup_power_meters.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_power_meters.setStyleSheet(u"border:none;")
        self.label_equip_setup_power_meters.setAlignment(Qt.AlignCenter)

        self.verticalLayout_53.addWidget(self.label_equip_setup_power_meters)

        self.frame_equip_setup_power_meters_contents = QFrame(self.frame_equip_setup_power_meters)
        self.frame_equip_setup_power_meters_contents.setObjectName(u"frame_equip_setup_power_meters_contents")
        self.frame_equip_setup_power_meters_contents.setStyleSheet(u"border:none;")
        self.frame_equip_setup_power_meters_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_power_meters_contents.setFrameShadow(QFrame.Raised)
        self.verticalLayout_68 = QVBoxLayout(self.frame_equip_setup_power_meters_contents)
        self.verticalLayout_68.setObjectName(u"verticalLayout_68")
        self.frame_equip_setup_power_meter_source = QFrame(self.frame_equip_setup_power_meters_contents)
        self.frame_equip_setup_power_meter_source.setObjectName(u"frame_equip_setup_power_meter_source")
        sizePolicy17 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy17.setHorizontalStretch(1)
        sizePolicy17.setVerticalStretch(1)
        sizePolicy17.setHeightForWidth(self.frame_equip_setup_power_meter_source.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_power_meter_source.setSizePolicy(sizePolicy17)
        self.frame_equip_setup_power_meter_source.setStyleSheet(u"QFrame{\n"
"	border: 1px solid black;\n"
"\n"
"}")
        self.frame_equip_setup_power_meter_source.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_power_meter_source.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_37 = QHBoxLayout(self.frame_equip_setup_power_meter_source)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.label_equip_setup_power_meter_source = QLabel(self.frame_equip_setup_power_meter_source)
        self.label_equip_setup_power_meter_source.setObjectName(u"label_equip_setup_power_meter_source")
        self.label_equip_setup_power_meter_source.setMinimumSize(QSize(100, 0))
        self.label_equip_setup_power_meter_source.setMaximumSize(QSize(100, 30))
        self.label_equip_setup_power_meter_source.setFont(font1)
        self.label_equip_setup_power_meter_source.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_power_meter_source.setStyleSheet(u"border:none;")
        self.label_equip_setup_power_meter_source.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_37.addWidget(self.label_equip_setup_power_meter_source)

        self.frame_equip_setup_power_meter_contents_source = QFrame(self.frame_equip_setup_power_meter_source)
        self.frame_equip_setup_power_meter_contents_source.setObjectName(u"frame_equip_setup_power_meter_contents_source")
        self.frame_equip_setup_power_meter_contents_source.setStyleSheet(u"border: None;")
        self.frame_equip_setup_power_meter_contents_source.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_power_meter_contents_source.setFrameShadow(QFrame.Raised)
        self.verticalLayout_69 = QVBoxLayout(self.frame_equip_setup_power_meter_contents_source)
        self.verticalLayout_69.setSpacing(0)
        self.verticalLayout_69.setObjectName(u"verticalLayout_69")
        self.verticalLayout_69.setContentsMargins(0, 0, 0, 0)
        self.cbx_equip_setup_power_meter_source = QComboBox(self.frame_equip_setup_power_meter_contents_source)
        self.cbx_equip_setup_power_meter_source.setObjectName(u"cbx_equip_setup_power_meter_source")
        self.cbx_equip_setup_power_meter_source.setMaximumSize(QSize(16777215, 40))
        self.cbx_equip_setup_power_meter_source.setFont(font10)
        self.cbx_equip_setup_power_meter_source.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.verticalLayout_69.addWidget(self.cbx_equip_setup_power_meter_source)


        self.horizontalLayout_37.addWidget(self.frame_equip_setup_power_meter_contents_source)


        self.verticalLayout_68.addWidget(self.frame_equip_setup_power_meter_source)

        self.frame_equip_setup_power_meter_load_1 = QFrame(self.frame_equip_setup_power_meters_contents)
        self.frame_equip_setup_power_meter_load_1.setObjectName(u"frame_equip_setup_power_meter_load_1")
        sizePolicy17.setHeightForWidth(self.frame_equip_setup_power_meter_load_1.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_power_meter_load_1.setSizePolicy(sizePolicy17)
        self.frame_equip_setup_power_meter_load_1.setStyleSheet(u"QFrame{\n"
"	border: 1px solid black;\n"
"\n"
"}")
        self.frame_equip_setup_power_meter_load_1.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_power_meter_load_1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_40 = QHBoxLayout(self.frame_equip_setup_power_meter_load_1)
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.label_equip_setup_power_meter_load_1 = QLabel(self.frame_equip_setup_power_meter_load_1)
        self.label_equip_setup_power_meter_load_1.setObjectName(u"label_equip_setup_power_meter_load_1")
        self.label_equip_setup_power_meter_load_1.setMinimumSize(QSize(100, 0))
        self.label_equip_setup_power_meter_load_1.setMaximumSize(QSize(100, 30))
        self.label_equip_setup_power_meter_load_1.setFont(font1)
        self.label_equip_setup_power_meter_load_1.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_power_meter_load_1.setStyleSheet(u"border:none;")
        self.label_equip_setup_power_meter_load_1.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_40.addWidget(self.label_equip_setup_power_meter_load_1)

        self.frame_equip_setup_power_meter_contents_load_1 = QFrame(self.frame_equip_setup_power_meter_load_1)
        self.frame_equip_setup_power_meter_contents_load_1.setObjectName(u"frame_equip_setup_power_meter_contents_load_1")
        self.frame_equip_setup_power_meter_contents_load_1.setStyleSheet(u"border: None;")
        self.frame_equip_setup_power_meter_contents_load_1.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_power_meter_contents_load_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_72 = QVBoxLayout(self.frame_equip_setup_power_meter_contents_load_1)
        self.verticalLayout_72.setSpacing(0)
        self.verticalLayout_72.setObjectName(u"verticalLayout_72")
        self.verticalLayout_72.setContentsMargins(0, 0, 0, 0)
        self.cbx_equip_setup_power_meter_load_1 = QComboBox(self.frame_equip_setup_power_meter_contents_load_1)
        self.cbx_equip_setup_power_meter_load_1.setObjectName(u"cbx_equip_setup_power_meter_load_1")
        self.cbx_equip_setup_power_meter_load_1.setMaximumSize(QSize(16777215, 40))
        self.cbx_equip_setup_power_meter_load_1.setFont(font10)
        self.cbx_equip_setup_power_meter_load_1.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.verticalLayout_72.addWidget(self.cbx_equip_setup_power_meter_load_1)


        self.horizontalLayout_40.addWidget(self.frame_equip_setup_power_meter_contents_load_1)


        self.verticalLayout_68.addWidget(self.frame_equip_setup_power_meter_load_1)

        self.frame_equip_setup_power_meter_load_2 = QFrame(self.frame_equip_setup_power_meters_contents)
        self.frame_equip_setup_power_meter_load_2.setObjectName(u"frame_equip_setup_power_meter_load_2")
        sizePolicy17.setHeightForWidth(self.frame_equip_setup_power_meter_load_2.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_power_meter_load_2.setSizePolicy(sizePolicy17)
        self.frame_equip_setup_power_meter_load_2.setStyleSheet(u"QFrame{\n"
"	border: 1px solid black;\n"
"\n"
"}")
        self.frame_equip_setup_power_meter_load_2.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_power_meter_load_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_41 = QHBoxLayout(self.frame_equip_setup_power_meter_load_2)
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.label_equip_setup_power_meter_load_2 = QLabel(self.frame_equip_setup_power_meter_load_2)
        self.label_equip_setup_power_meter_load_2.setObjectName(u"label_equip_setup_power_meter_load_2")
        self.label_equip_setup_power_meter_load_2.setMinimumSize(QSize(100, 0))
        self.label_equip_setup_power_meter_load_2.setMaximumSize(QSize(100, 30))
        self.label_equip_setup_power_meter_load_2.setFont(font1)
        self.label_equip_setup_power_meter_load_2.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_power_meter_load_2.setStyleSheet(u"border:none;")
        self.label_equip_setup_power_meter_load_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_41.addWidget(self.label_equip_setup_power_meter_load_2)

        self.frame_equip_setup_power_meter_contents_load_2 = QFrame(self.frame_equip_setup_power_meter_load_2)
        self.frame_equip_setup_power_meter_contents_load_2.setObjectName(u"frame_equip_setup_power_meter_contents_load_2")
        self.frame_equip_setup_power_meter_contents_load_2.setStyleSheet(u"border: None;")
        self.frame_equip_setup_power_meter_contents_load_2.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_power_meter_contents_load_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_73 = QVBoxLayout(self.frame_equip_setup_power_meter_contents_load_2)
        self.verticalLayout_73.setSpacing(0)
        self.verticalLayout_73.setObjectName(u"verticalLayout_73")
        self.verticalLayout_73.setContentsMargins(0, 0, 0, 0)
        self.cbx_equip_setup_power_meter_load_2 = QComboBox(self.frame_equip_setup_power_meter_contents_load_2)
        self.cbx_equip_setup_power_meter_load_2.setObjectName(u"cbx_equip_setup_power_meter_load_2")
        self.cbx_equip_setup_power_meter_load_2.setMaximumSize(QSize(16777215, 40))
        self.cbx_equip_setup_power_meter_load_2.setFont(font10)
        self.cbx_equip_setup_power_meter_load_2.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.verticalLayout_73.addWidget(self.cbx_equip_setup_power_meter_load_2)


        self.horizontalLayout_41.addWidget(self.frame_equip_setup_power_meter_contents_load_2)


        self.verticalLayout_68.addWidget(self.frame_equip_setup_power_meter_load_2)

        self.frame_equip_setup_power_meter_load_3 = QFrame(self.frame_equip_setup_power_meters_contents)
        self.frame_equip_setup_power_meter_load_3.setObjectName(u"frame_equip_setup_power_meter_load_3")
        sizePolicy17.setHeightForWidth(self.frame_equip_setup_power_meter_load_3.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_power_meter_load_3.setSizePolicy(sizePolicy17)
        self.frame_equip_setup_power_meter_load_3.setStyleSheet(u"QFrame{\n"
"	border: 1px solid black;\n"
"\n"
"}")
        self.frame_equip_setup_power_meter_load_3.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_power_meter_load_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_42 = QHBoxLayout(self.frame_equip_setup_power_meter_load_3)
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.label_equip_setup_power_meter_load_3 = QLabel(self.frame_equip_setup_power_meter_load_3)
        self.label_equip_setup_power_meter_load_3.setObjectName(u"label_equip_setup_power_meter_load_3")
        self.label_equip_setup_power_meter_load_3.setMinimumSize(QSize(100, 0))
        self.label_equip_setup_power_meter_load_3.setMaximumSize(QSize(100, 30))
        self.label_equip_setup_power_meter_load_3.setFont(font1)
        self.label_equip_setup_power_meter_load_3.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_power_meter_load_3.setStyleSheet(u"border:none;")
        self.label_equip_setup_power_meter_load_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_42.addWidget(self.label_equip_setup_power_meter_load_3)

        self.frame_equip_setup_power_meter_contents_load_3 = QFrame(self.frame_equip_setup_power_meter_load_3)
        self.frame_equip_setup_power_meter_contents_load_3.setObjectName(u"frame_equip_setup_power_meter_contents_load_3")
        self.frame_equip_setup_power_meter_contents_load_3.setStyleSheet(u"border: None;")
        self.frame_equip_setup_power_meter_contents_load_3.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_power_meter_contents_load_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_74 = QVBoxLayout(self.frame_equip_setup_power_meter_contents_load_3)
        self.verticalLayout_74.setSpacing(0)
        self.verticalLayout_74.setObjectName(u"verticalLayout_74")
        self.verticalLayout_74.setContentsMargins(0, 0, 0, 0)
        self.cbx_equip_setup_power_meter_load_3 = QComboBox(self.frame_equip_setup_power_meter_contents_load_3)
        self.cbx_equip_setup_power_meter_load_3.setObjectName(u"cbx_equip_setup_power_meter_load_3")
        self.cbx_equip_setup_power_meter_load_3.setMaximumSize(QSize(16777215, 40))
        self.cbx_equip_setup_power_meter_load_3.setFont(font10)
        self.cbx_equip_setup_power_meter_load_3.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.verticalLayout_74.addWidget(self.cbx_equip_setup_power_meter_load_3)


        self.horizontalLayout_42.addWidget(self.frame_equip_setup_power_meter_contents_load_3)


        self.verticalLayout_68.addWidget(self.frame_equip_setup_power_meter_load_3)

        self.frame_equip_setup_power_meter_load_4 = QFrame(self.frame_equip_setup_power_meters_contents)
        self.frame_equip_setup_power_meter_load_4.setObjectName(u"frame_equip_setup_power_meter_load_4")
        sizePolicy17.setHeightForWidth(self.frame_equip_setup_power_meter_load_4.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_power_meter_load_4.setSizePolicy(sizePolicy17)
        self.frame_equip_setup_power_meter_load_4.setStyleSheet(u"QFrame{\n"
"	border: 1px solid black;\n"
"\n"
"}")
        self.frame_equip_setup_power_meter_load_4.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_power_meter_load_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_43 = QHBoxLayout(self.frame_equip_setup_power_meter_load_4)
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.label_equip_setup_power_meter_load_4 = QLabel(self.frame_equip_setup_power_meter_load_4)
        self.label_equip_setup_power_meter_load_4.setObjectName(u"label_equip_setup_power_meter_load_4")
        self.label_equip_setup_power_meter_load_4.setMinimumSize(QSize(100, 0))
        self.label_equip_setup_power_meter_load_4.setMaximumSize(QSize(100, 30))
        self.label_equip_setup_power_meter_load_4.setFont(font1)
        self.label_equip_setup_power_meter_load_4.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_power_meter_load_4.setStyleSheet(u"border:none;")
        self.label_equip_setup_power_meter_load_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_43.addWidget(self.label_equip_setup_power_meter_load_4)

        self.frame_equip_setup_power_meter_contents_load_4 = QFrame(self.frame_equip_setup_power_meter_load_4)
        self.frame_equip_setup_power_meter_contents_load_4.setObjectName(u"frame_equip_setup_power_meter_contents_load_4")
        self.frame_equip_setup_power_meter_contents_load_4.setStyleSheet(u"border: None;")
        self.frame_equip_setup_power_meter_contents_load_4.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_power_meter_contents_load_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_75 = QVBoxLayout(self.frame_equip_setup_power_meter_contents_load_4)
        self.verticalLayout_75.setSpacing(0)
        self.verticalLayout_75.setObjectName(u"verticalLayout_75")
        self.verticalLayout_75.setContentsMargins(0, 0, 0, 0)
        self.cbx_equip_setup_power_meter_load_4 = QComboBox(self.frame_equip_setup_power_meter_contents_load_4)
        self.cbx_equip_setup_power_meter_load_4.setObjectName(u"cbx_equip_setup_power_meter_load_4")
        self.cbx_equip_setup_power_meter_load_4.setMaximumSize(QSize(16777215, 40))
        self.cbx_equip_setup_power_meter_load_4.setFont(font10)
        self.cbx_equip_setup_power_meter_load_4.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.verticalLayout_75.addWidget(self.cbx_equip_setup_power_meter_load_4)


        self.horizontalLayout_43.addWidget(self.frame_equip_setup_power_meter_contents_load_4)


        self.verticalLayout_68.addWidget(self.frame_equip_setup_power_meter_load_4)

        self.frame_equip_setup_power_meter_load_5 = QFrame(self.frame_equip_setup_power_meters_contents)
        self.frame_equip_setup_power_meter_load_5.setObjectName(u"frame_equip_setup_power_meter_load_5")
        sizePolicy17.setHeightForWidth(self.frame_equip_setup_power_meter_load_5.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_power_meter_load_5.setSizePolicy(sizePolicy17)
        self.frame_equip_setup_power_meter_load_5.setStyleSheet(u"QFrame{\n"
"	border: 1px solid black;\n"
"\n"
"}")
        self.frame_equip_setup_power_meter_load_5.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_power_meter_load_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_44 = QHBoxLayout(self.frame_equip_setup_power_meter_load_5)
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.label_equip_setup_power_meter_load_5 = QLabel(self.frame_equip_setup_power_meter_load_5)
        self.label_equip_setup_power_meter_load_5.setObjectName(u"label_equip_setup_power_meter_load_5")
        self.label_equip_setup_power_meter_load_5.setMinimumSize(QSize(100, 0))
        self.label_equip_setup_power_meter_load_5.setMaximumSize(QSize(100, 30))
        self.label_equip_setup_power_meter_load_5.setFont(font1)
        self.label_equip_setup_power_meter_load_5.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_power_meter_load_5.setStyleSheet(u"border:none;")
        self.label_equip_setup_power_meter_load_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_44.addWidget(self.label_equip_setup_power_meter_load_5)

        self.frame_equip_setup_power_meter_contents_load_5 = QFrame(self.frame_equip_setup_power_meter_load_5)
        self.frame_equip_setup_power_meter_contents_load_5.setObjectName(u"frame_equip_setup_power_meter_contents_load_5")
        self.frame_equip_setup_power_meter_contents_load_5.setStyleSheet(u"border: None;")
        self.frame_equip_setup_power_meter_contents_load_5.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_power_meter_contents_load_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_76 = QVBoxLayout(self.frame_equip_setup_power_meter_contents_load_5)
        self.verticalLayout_76.setSpacing(0)
        self.verticalLayout_76.setObjectName(u"verticalLayout_76")
        self.verticalLayout_76.setContentsMargins(0, 0, 0, 0)
        self.cbx_equip_setup_power_meter_load_5 = QComboBox(self.frame_equip_setup_power_meter_contents_load_5)
        self.cbx_equip_setup_power_meter_load_5.setObjectName(u"cbx_equip_setup_power_meter_load_5")
        self.cbx_equip_setup_power_meter_load_5.setMaximumSize(QSize(16777215, 40))
        self.cbx_equip_setup_power_meter_load_5.setFont(font10)
        self.cbx_equip_setup_power_meter_load_5.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.verticalLayout_76.addWidget(self.cbx_equip_setup_power_meter_load_5)


        self.horizontalLayout_44.addWidget(self.frame_equip_setup_power_meter_contents_load_5)


        self.verticalLayout_68.addWidget(self.frame_equip_setup_power_meter_load_5)


        self.verticalLayout_53.addWidget(self.frame_equip_setup_power_meters_contents)


        self.horizontalLayout_24.addWidget(self.frame_equip_setup_power_meters)

        self.frame_equip_setup_eloads = QFrame(self.frame_equip_setup_bot)
        self.frame_equip_setup_eloads.setObjectName(u"frame_equip_setup_eloads")
        sizePolicy10.setHeightForWidth(self.frame_equip_setup_eloads.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_eloads.setSizePolicy(sizePolicy10)
        self.frame_equip_setup_eloads.setMinimumSize(QSize(400, 0))
        self.frame_equip_setup_eloads.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_equip_setup_eloads.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_eloads.setFrameShadow(QFrame.Raised)
        self.verticalLayout_57 = QVBoxLayout(self.frame_equip_setup_eloads)
        self.verticalLayout_57.setObjectName(u"verticalLayout_57")
        self.label_equip_setup_eloads = QLabel(self.frame_equip_setup_eloads)
        self.label_equip_setup_eloads.setObjectName(u"label_equip_setup_eloads")
        self.label_equip_setup_eloads.setMaximumSize(QSize(16777215, 30))
        self.label_equip_setup_eloads.setFont(font1)
        self.label_equip_setup_eloads.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_eloads.setStyleSheet(u"border:none;")
        self.label_equip_setup_eloads.setAlignment(Qt.AlignCenter)

        self.verticalLayout_57.addWidget(self.label_equip_setup_eloads)

        self.frame_equip_setup_eloads_contents = QFrame(self.frame_equip_setup_eloads)
        self.frame_equip_setup_eloads_contents.setObjectName(u"frame_equip_setup_eloads_contents")
        self.frame_equip_setup_eloads_contents.setStyleSheet(u"border:none;")
        self.frame_equip_setup_eloads_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_eloads_contents.setFrameShadow(QFrame.Raised)
        self.verticalLayout_54 = QVBoxLayout(self.frame_equip_setup_eloads_contents)
        self.verticalLayout_54.setObjectName(u"verticalLayout_54")
        self.frame_equip_setup_eloads_load_1 = QFrame(self.frame_equip_setup_eloads_contents)
        self.frame_equip_setup_eloads_load_1.setObjectName(u"frame_equip_setup_eloads_load_1")
        sizePolicy17.setHeightForWidth(self.frame_equip_setup_eloads_load_1.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_eloads_load_1.setSizePolicy(sizePolicy17)
        self.frame_equip_setup_eloads_load_1.setStyleSheet(u"QFrame{\n"
"	border: 1px solid black;\n"
"\n"
"}")
        self.frame_equip_setup_eloads_load_1.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_eloads_load_1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_48 = QHBoxLayout(self.frame_equip_setup_eloads_load_1)
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.label_equip_setup_eloads_load_1 = QLabel(self.frame_equip_setup_eloads_load_1)
        self.label_equip_setup_eloads_load_1.setObjectName(u"label_equip_setup_eloads_load_1")
        self.label_equip_setup_eloads_load_1.setMinimumSize(QSize(100, 0))
        self.label_equip_setup_eloads_load_1.setMaximumSize(QSize(100, 30))
        self.label_equip_setup_eloads_load_1.setFont(font1)
        self.label_equip_setup_eloads_load_1.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_eloads_load_1.setStyleSheet(u"border:none;")
        self.label_equip_setup_eloads_load_1.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_48.addWidget(self.label_equip_setup_eloads_load_1)

        self.frame_equip_setup_eloads_contents_load_1 = QFrame(self.frame_equip_setup_eloads_load_1)
        self.frame_equip_setup_eloads_contents_load_1.setObjectName(u"frame_equip_setup_eloads_contents_load_1")
        self.frame_equip_setup_eloads_contents_load_1.setStyleSheet(u"border: None;")
        self.frame_equip_setup_eloads_contents_load_1.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_eloads_contents_load_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_80 = QVBoxLayout(self.frame_equip_setup_eloads_contents_load_1)
        self.verticalLayout_80.setSpacing(0)
        self.verticalLayout_80.setObjectName(u"verticalLayout_80")
        self.verticalLayout_80.setContentsMargins(0, 0, 0, 0)
        self.cbx_equip_setup_eloads_load_1 = QComboBox(self.frame_equip_setup_eloads_contents_load_1)
        self.cbx_equip_setup_eloads_load_1.setObjectName(u"cbx_equip_setup_eloads_load_1")
        self.cbx_equip_setup_eloads_load_1.setMaximumSize(QSize(16777215, 40))
        self.cbx_equip_setup_eloads_load_1.setFont(font10)
        self.cbx_equip_setup_eloads_load_1.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.verticalLayout_80.addWidget(self.cbx_equip_setup_eloads_load_1)


        self.horizontalLayout_48.addWidget(self.frame_equip_setup_eloads_contents_load_1)


        self.verticalLayout_54.addWidget(self.frame_equip_setup_eloads_load_1)

        self.frame_equip_setup_eloads_load_2 = QFrame(self.frame_equip_setup_eloads_contents)
        self.frame_equip_setup_eloads_load_2.setObjectName(u"frame_equip_setup_eloads_load_2")
        sizePolicy17.setHeightForWidth(self.frame_equip_setup_eloads_load_2.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_eloads_load_2.setSizePolicy(sizePolicy17)
        self.frame_equip_setup_eloads_load_2.setStyleSheet(u"QFrame{\n"
"	border: 1px solid black;\n"
"\n"
"}")
        self.frame_equip_setup_eloads_load_2.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_eloads_load_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_49 = QHBoxLayout(self.frame_equip_setup_eloads_load_2)
        self.horizontalLayout_49.setObjectName(u"horizontalLayout_49")
        self.label_equip_setup_eloads_load_2 = QLabel(self.frame_equip_setup_eloads_load_2)
        self.label_equip_setup_eloads_load_2.setObjectName(u"label_equip_setup_eloads_load_2")
        self.label_equip_setup_eloads_load_2.setMinimumSize(QSize(100, 0))
        self.label_equip_setup_eloads_load_2.setMaximumSize(QSize(100, 30))
        self.label_equip_setup_eloads_load_2.setFont(font1)
        self.label_equip_setup_eloads_load_2.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_eloads_load_2.setStyleSheet(u"border:none;")
        self.label_equip_setup_eloads_load_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_49.addWidget(self.label_equip_setup_eloads_load_2)

        self.frame_equip_setup_eloads_contents_load_2 = QFrame(self.frame_equip_setup_eloads_load_2)
        self.frame_equip_setup_eloads_contents_load_2.setObjectName(u"frame_equip_setup_eloads_contents_load_2")
        self.frame_equip_setup_eloads_contents_load_2.setStyleSheet(u"border: None;")
        self.frame_equip_setup_eloads_contents_load_2.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_eloads_contents_load_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_81 = QVBoxLayout(self.frame_equip_setup_eloads_contents_load_2)
        self.verticalLayout_81.setSpacing(0)
        self.verticalLayout_81.setObjectName(u"verticalLayout_81")
        self.verticalLayout_81.setContentsMargins(0, 0, 0, 0)
        self.cbx_equip_setup_eloads_load_2 = QComboBox(self.frame_equip_setup_eloads_contents_load_2)
        self.cbx_equip_setup_eloads_load_2.setObjectName(u"cbx_equip_setup_eloads_load_2")
        self.cbx_equip_setup_eloads_load_2.setMaximumSize(QSize(16777215, 40))
        self.cbx_equip_setup_eloads_load_2.setFont(font10)
        self.cbx_equip_setup_eloads_load_2.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.verticalLayout_81.addWidget(self.cbx_equip_setup_eloads_load_2)


        self.horizontalLayout_49.addWidget(self.frame_equip_setup_eloads_contents_load_2)


        self.verticalLayout_54.addWidget(self.frame_equip_setup_eloads_load_2)

        self.frame_equip_setup_eloads_load_3 = QFrame(self.frame_equip_setup_eloads_contents)
        self.frame_equip_setup_eloads_load_3.setObjectName(u"frame_equip_setup_eloads_load_3")
        sizePolicy17.setHeightForWidth(self.frame_equip_setup_eloads_load_3.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_eloads_load_3.setSizePolicy(sizePolicy17)
        self.frame_equip_setup_eloads_load_3.setStyleSheet(u"QFrame{\n"
"	border: 1px solid black;\n"
"\n"
"}")
        self.frame_equip_setup_eloads_load_3.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_eloads_load_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_50 = QHBoxLayout(self.frame_equip_setup_eloads_load_3)
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.label_equip_setup_eloads_load_3 = QLabel(self.frame_equip_setup_eloads_load_3)
        self.label_equip_setup_eloads_load_3.setObjectName(u"label_equip_setup_eloads_load_3")
        self.label_equip_setup_eloads_load_3.setMinimumSize(QSize(100, 0))
        self.label_equip_setup_eloads_load_3.setMaximumSize(QSize(100, 30))
        self.label_equip_setup_eloads_load_3.setFont(font1)
        self.label_equip_setup_eloads_load_3.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_eloads_load_3.setStyleSheet(u"border:none;")
        self.label_equip_setup_eloads_load_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_50.addWidget(self.label_equip_setup_eloads_load_3)

        self.frame_equip_setup_eloads_contents_load_3 = QFrame(self.frame_equip_setup_eloads_load_3)
        self.frame_equip_setup_eloads_contents_load_3.setObjectName(u"frame_equip_setup_eloads_contents_load_3")
        self.frame_equip_setup_eloads_contents_load_3.setStyleSheet(u"border: None;")
        self.frame_equip_setup_eloads_contents_load_3.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_eloads_contents_load_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_82 = QVBoxLayout(self.frame_equip_setup_eloads_contents_load_3)
        self.verticalLayout_82.setSpacing(0)
        self.verticalLayout_82.setObjectName(u"verticalLayout_82")
        self.verticalLayout_82.setContentsMargins(0, 0, 0, 0)
        self.cbx_equip_setup_eloads_load_3 = QComboBox(self.frame_equip_setup_eloads_contents_load_3)
        self.cbx_equip_setup_eloads_load_3.setObjectName(u"cbx_equip_setup_eloads_load_3")
        self.cbx_equip_setup_eloads_load_3.setMaximumSize(QSize(16777215, 40))
        self.cbx_equip_setup_eloads_load_3.setFont(font10)
        self.cbx_equip_setup_eloads_load_3.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.verticalLayout_82.addWidget(self.cbx_equip_setup_eloads_load_3)


        self.horizontalLayout_50.addWidget(self.frame_equip_setup_eloads_contents_load_3)


        self.verticalLayout_54.addWidget(self.frame_equip_setup_eloads_load_3)

        self.frame_equip_setup_eloads_load_4 = QFrame(self.frame_equip_setup_eloads_contents)
        self.frame_equip_setup_eloads_load_4.setObjectName(u"frame_equip_setup_eloads_load_4")
        sizePolicy17.setHeightForWidth(self.frame_equip_setup_eloads_load_4.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_eloads_load_4.setSizePolicy(sizePolicy17)
        self.frame_equip_setup_eloads_load_4.setStyleSheet(u"QFrame{\n"
"	border: 1px solid black;\n"
"\n"
"}")
        self.frame_equip_setup_eloads_load_4.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_eloads_load_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_51 = QHBoxLayout(self.frame_equip_setup_eloads_load_4)
        self.horizontalLayout_51.setObjectName(u"horizontalLayout_51")
        self.label_equip_setup_eloads_load_4 = QLabel(self.frame_equip_setup_eloads_load_4)
        self.label_equip_setup_eloads_load_4.setObjectName(u"label_equip_setup_eloads_load_4")
        self.label_equip_setup_eloads_load_4.setMinimumSize(QSize(100, 0))
        self.label_equip_setup_eloads_load_4.setMaximumSize(QSize(100, 30))
        self.label_equip_setup_eloads_load_4.setFont(font1)
        self.label_equip_setup_eloads_load_4.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_eloads_load_4.setStyleSheet(u"border:none;")
        self.label_equip_setup_eloads_load_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_51.addWidget(self.label_equip_setup_eloads_load_4)

        self.frame_equip_setup_eloads_contents_load_4 = QFrame(self.frame_equip_setup_eloads_load_4)
        self.frame_equip_setup_eloads_contents_load_4.setObjectName(u"frame_equip_setup_eloads_contents_load_4")
        self.frame_equip_setup_eloads_contents_load_4.setStyleSheet(u"border: None;")
        self.frame_equip_setup_eloads_contents_load_4.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_eloads_contents_load_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_83 = QVBoxLayout(self.frame_equip_setup_eloads_contents_load_4)
        self.verticalLayout_83.setSpacing(0)
        self.verticalLayout_83.setObjectName(u"verticalLayout_83")
        self.verticalLayout_83.setContentsMargins(0, 0, 0, 0)
        self.cbx_equip_setup_eloads_load_4 = QComboBox(self.frame_equip_setup_eloads_contents_load_4)
        self.cbx_equip_setup_eloads_load_4.setObjectName(u"cbx_equip_setup_eloads_load_4")
        self.cbx_equip_setup_eloads_load_4.setMaximumSize(QSize(16777215, 40))
        self.cbx_equip_setup_eloads_load_4.setFont(font10)
        self.cbx_equip_setup_eloads_load_4.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.verticalLayout_83.addWidget(self.cbx_equip_setup_eloads_load_4)


        self.horizontalLayout_51.addWidget(self.frame_equip_setup_eloads_contents_load_4)


        self.verticalLayout_54.addWidget(self.frame_equip_setup_eloads_load_4)

        self.frame_equip_setup_eloads_load_5 = QFrame(self.frame_equip_setup_eloads_contents)
        self.frame_equip_setup_eloads_load_5.setObjectName(u"frame_equip_setup_eloads_load_5")
        sizePolicy17.setHeightForWidth(self.frame_equip_setup_eloads_load_5.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_eloads_load_5.setSizePolicy(sizePolicy17)
        self.frame_equip_setup_eloads_load_5.setStyleSheet(u"QFrame{\n"
"	border: 1px solid black;\n"
"\n"
"}")
        self.frame_equip_setup_eloads_load_5.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_eloads_load_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_52 = QHBoxLayout(self.frame_equip_setup_eloads_load_5)
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.label_equip_setup_eloads_load_5 = QLabel(self.frame_equip_setup_eloads_load_5)
        self.label_equip_setup_eloads_load_5.setObjectName(u"label_equip_setup_eloads_load_5")
        self.label_equip_setup_eloads_load_5.setMinimumSize(QSize(100, 0))
        self.label_equip_setup_eloads_load_5.setMaximumSize(QSize(100, 30))
        self.label_equip_setup_eloads_load_5.setFont(font1)
        self.label_equip_setup_eloads_load_5.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_eloads_load_5.setStyleSheet(u"border:none;")
        self.label_equip_setup_eloads_load_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_52.addWidget(self.label_equip_setup_eloads_load_5)

        self.frame_equip_setup_eloads_contents_load_5 = QFrame(self.frame_equip_setup_eloads_load_5)
        self.frame_equip_setup_eloads_contents_load_5.setObjectName(u"frame_equip_setup_eloads_contents_load_5")
        self.frame_equip_setup_eloads_contents_load_5.setStyleSheet(u"border: None;")
        self.frame_equip_setup_eloads_contents_load_5.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_eloads_contents_load_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_84 = QVBoxLayout(self.frame_equip_setup_eloads_contents_load_5)
        self.verticalLayout_84.setSpacing(0)
        self.verticalLayout_84.setObjectName(u"verticalLayout_84")
        self.verticalLayout_84.setContentsMargins(0, 0, 0, 0)
        self.cbx_equip_setup_eloads_load_5 = QComboBox(self.frame_equip_setup_eloads_contents_load_5)
        self.cbx_equip_setup_eloads_load_5.setObjectName(u"cbx_equip_setup_eloads_load_5")
        self.cbx_equip_setup_eloads_load_5.setMaximumSize(QSize(16777215, 40))
        self.cbx_equip_setup_eloads_load_5.setFont(font10)
        self.cbx_equip_setup_eloads_load_5.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.verticalLayout_84.addWidget(self.cbx_equip_setup_eloads_load_5)


        self.horizontalLayout_52.addWidget(self.frame_equip_setup_eloads_contents_load_5)


        self.verticalLayout_54.addWidget(self.frame_equip_setup_eloads_load_5)

        self.frame_equip_setup_eloads_load_6 = QFrame(self.frame_equip_setup_eloads_contents)
        self.frame_equip_setup_eloads_load_6.setObjectName(u"frame_equip_setup_eloads_load_6")
        sizePolicy17.setHeightForWidth(self.frame_equip_setup_eloads_load_6.sizePolicy().hasHeightForWidth())
        self.frame_equip_setup_eloads_load_6.setSizePolicy(sizePolicy17)
        self.frame_equip_setup_eloads_load_6.setStyleSheet(u"QFrame{\n"
"	border: 1px solid black;\n"
"\n"
"}")
        self.frame_equip_setup_eloads_load_6.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_eloads_load_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_53 = QHBoxLayout(self.frame_equip_setup_eloads_load_6)
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")
        self.label_equip_setup_eloads_load_6 = QLabel(self.frame_equip_setup_eloads_load_6)
        self.label_equip_setup_eloads_load_6.setObjectName(u"label_equip_setup_eloads_load_6")
        self.label_equip_setup_eloads_load_6.setMinimumSize(QSize(100, 0))
        self.label_equip_setup_eloads_load_6.setMaximumSize(QSize(100, 30))
        self.label_equip_setup_eloads_load_6.setFont(font1)
        self.label_equip_setup_eloads_load_6.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_equip_setup_eloads_load_6.setStyleSheet(u"border:none;")
        self.label_equip_setup_eloads_load_6.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_53.addWidget(self.label_equip_setup_eloads_load_6)

        self.frame_equip_setup_eloads_contents_load_6 = QFrame(self.frame_equip_setup_eloads_load_6)
        self.frame_equip_setup_eloads_contents_load_6.setObjectName(u"frame_equip_setup_eloads_contents_load_6")
        self.frame_equip_setup_eloads_contents_load_6.setStyleSheet(u"border: None;")
        self.frame_equip_setup_eloads_contents_load_6.setFrameShape(QFrame.StyledPanel)
        self.frame_equip_setup_eloads_contents_load_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_85 = QVBoxLayout(self.frame_equip_setup_eloads_contents_load_6)
        self.verticalLayout_85.setSpacing(0)
        self.verticalLayout_85.setObjectName(u"verticalLayout_85")
        self.verticalLayout_85.setContentsMargins(0, 0, 0, 0)
        self.cbx_equip_setup_eloads_load_6 = QComboBox(self.frame_equip_setup_eloads_contents_load_6)
        self.cbx_equip_setup_eloads_load_6.setObjectName(u"cbx_equip_setup_eloads_load_6")
        self.cbx_equip_setup_eloads_load_6.setMaximumSize(QSize(16777215, 40))
        self.cbx_equip_setup_eloads_load_6.setFont(font10)
        self.cbx_equip_setup_eloads_load_6.setStyleSheet(u"border: 2px solid black;\n"
"")

        self.verticalLayout_85.addWidget(self.cbx_equip_setup_eloads_load_6)


        self.horizontalLayout_53.addWidget(self.frame_equip_setup_eloads_contents_load_6)


        self.verticalLayout_54.addWidget(self.frame_equip_setup_eloads_load_6)


        self.verticalLayout_57.addWidget(self.frame_equip_setup_eloads_contents)


        self.horizontalLayout_24.addWidget(self.frame_equip_setup_eloads)


        self.verticalLayout_51.addWidget(self.frame_equip_setup_bot)


        self.horizontalLayout_21.addWidget(self.frame_equip_setup)

        self.stackedWidget.addWidget(self.page_equipment_setup)
        self.page_manual_control = QWidget()
        self.page_manual_control.setObjectName(u"page_manual_control")
        self.verticalLayout_12 = QVBoxLayout(self.page_manual_control)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_manual_control = QFrame(self.page_manual_control)
        self.label_manual_control.setObjectName(u"label_manual_control")
        self.label_manual_control.setMaximumSize(QSize(16777215, 50))
        self.label_manual_control.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.label_manual_control.setFrameShape(QFrame.NoFrame)
        self.label_manual_control.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.label_manual_control)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_2 = QLabel(self.label_manual_control)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)
        self.label_2.setCursor(QCursor(Qt.UpArrowCursor))

        self.verticalLayout_14.addWidget(self.label_2)


        self.verticalLayout_12.addWidget(self.label_manual_control)

        self.frame_manual_control_upper = QFrame(self.page_manual_control)
        self.frame_manual_control_upper.setObjectName(u"frame_manual_control_upper")
        self.frame_manual_control_upper.setFrameShape(QFrame.NoFrame)
        self.frame_manual_control_upper.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_manual_control_upper)
        self.horizontalLayout_9.setSpacing(1)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(1, 1, 1, 1)
        self.frame_manual_control_pms = QFrame(self.frame_manual_control_upper)
        self.frame_manual_control_pms.setObjectName(u"frame_manual_control_pms")
        self.frame_manual_control_pms.setEnabled(True)
        self.frame_manual_control_pms.setMinimumSize(QSize(300, 0))
        self.frame_manual_control_pms.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"};")
        self.frame_manual_control_pms.setFrameShape(QFrame.NoFrame)
        self.frame_manual_control_pms.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_17 = QVBoxLayout(self.frame_manual_control_pms)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.label_source_power_meter = QLabel(self.frame_manual_control_pms)
        self.label_source_power_meter.setObjectName(u"label_source_power_meter")
        self.label_source_power_meter.setMaximumSize(QSize(16777215, 30))
        self.label_source_power_meter.setFont(font1)
        self.label_source_power_meter.setCursor(QCursor(Qt.ArrowCursor))
        self.label_source_power_meter.setStyleSheet(u"QLabel{border:none;}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_source_power_meter.setAlignment(Qt.AlignCenter)

        self.verticalLayout_17.addWidget(self.label_source_power_meter)

        self.frame_pms_contents = QFrame(self.frame_manual_control_pms)
        self.frame_pms_contents.setObjectName(u"frame_pms_contents")
        self.frame_pms_contents.setStyleSheet(u"border:none;")
        self.frame_pms_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_contents.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_pms_contents)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.frame_pms_display = QFrame(self.frame_pms_contents)
        self.frame_pms_display.setObjectName(u"frame_pms_display")
        self.frame_pms_display.setMinimumSize(QSize(0, 280))
        self.frame_pms_display.setMaximumSize(QSize(300, 16777215))
        self.frame_pms_display.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}")
        self.frame_pms_display.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_display.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_pms_display)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.label_pms_display_a = QLabel(self.frame_pms_display)
        self.label_pms_display_a.setObjectName(u"label_pms_display_a")
        self.label_pms_display_a.setMinimumSize(QSize(0, 70))
        self.label_pms_display_a.setMaximumSize(QSize(16777215, 70))
        font12 = QFont()
        font12.setFamily(u"Consolas")
        font12.setPointSize(25)
        font12.setBold(False)
        font12.setItalic(False)
        font12.setWeight(50)
        font12.setKerning(False)
        self.label_pms_display_a.setFont(font12)
        self.label_pms_display_a.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_pms_display_a.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_16.addWidget(self.label_pms_display_a)

        self.label_pms_display_b = QLabel(self.frame_pms_display)
        self.label_pms_display_b.setObjectName(u"label_pms_display_b")
        self.label_pms_display_b.setMinimumSize(QSize(0, 70))
        self.label_pms_display_b.setMaximumSize(QSize(16777215, 70))
        self.label_pms_display_b.setFont(font12)
        self.label_pms_display_b.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_pms_display_b.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_16.addWidget(self.label_pms_display_b)

        self.label_pms_display_c = QLabel(self.frame_pms_display)
        self.label_pms_display_c.setObjectName(u"label_pms_display_c")
        self.label_pms_display_c.setMinimumSize(QSize(0, 70))
        self.label_pms_display_c.setMaximumSize(QSize(16777215, 70))
        self.label_pms_display_c.setFont(font12)
        self.label_pms_display_c.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_pms_display_c.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_16.addWidget(self.label_pms_display_c)

        self.label_pms_display_d = QLabel(self.frame_pms_display)
        self.label_pms_display_d.setObjectName(u"label_pms_display_d")
        self.label_pms_display_d.setMinimumSize(QSize(0, 70))
        self.label_pms_display_d.setMaximumSize(QSize(16777215, 70))
        self.label_pms_display_d.setFont(font12)
        self.label_pms_display_d.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_pms_display_d.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_16.addWidget(self.label_pms_display_d)


        self.horizontalLayout_14.addWidget(self.frame_pms_display)

        self.frame_pms_display_select = QFrame(self.frame_pms_contents)
        self.frame_pms_display_select.setObjectName(u"frame_pms_display_select")
        self.frame_pms_display_select.setMaximumSize(QSize(100, 16777215))
        self.frame_pms_display_select.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_pms_display_select.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_display_select.setFrameShadow(QFrame.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.frame_pms_display_select)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.cbx_pms_display_a = QComboBox(self.frame_pms_display_select)
        self.cbx_pms_display_a.setObjectName(u"cbx_pms_display_a")
        self.cbx_pms_display_a.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_18.addWidget(self.cbx_pms_display_a)

        self.cbx_pms_display_b = QComboBox(self.frame_pms_display_select)
        self.cbx_pms_display_b.setObjectName(u"cbx_pms_display_b")
        self.cbx_pms_display_b.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_18.addWidget(self.cbx_pms_display_b)

        self.cbx_pms_display_c = QComboBox(self.frame_pms_display_select)
        self.cbx_pms_display_c.setObjectName(u"cbx_pms_display_c")
        self.cbx_pms_display_c.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_18.addWidget(self.cbx_pms_display_c)

        self.cbx_pms_display_d = QComboBox(self.frame_pms_display_select)
        self.cbx_pms_display_d.setObjectName(u"cbx_pms_display_d")
        self.cbx_pms_display_d.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_18.addWidget(self.cbx_pms_display_d)


        self.horizontalLayout_14.addWidget(self.frame_pms_display_select)

        self.frame_pms_control = QFrame(self.frame_pms_contents)
        self.frame_pms_control.setObjectName(u"frame_pms_control")
        self.frame_pms_control.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"")
        self.frame_pms_control.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_control.setFrameShadow(QFrame.Raised)
        self.verticalLayout_28 = QVBoxLayout(self.frame_pms_control)
        self.verticalLayout_28.setSpacing(0)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.verticalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.frame_pms_control__range = QFrame(self.frame_pms_control)
        self.frame_pms_control__range.setObjectName(u"frame_pms_control__range")
        self.frame_pms_control__range.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_control__range.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.frame_pms_control__range)
        self.formLayout.setObjectName(u"formLayout")
        self.label_pms_voltage_range = QLabel(self.frame_pms_control__range)
        self.label_pms_voltage_range.setObjectName(u"label_pms_voltage_range")
        self.label_pms_voltage_range.setFont(font10)
        self.label_pms_voltage_range.setStyleSheet(u"border:none;")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_pms_voltage_range)

        self.cbx_pms_voltage_range = QComboBox(self.frame_pms_control__range)
        self.cbx_pms_voltage_range.addItem("")
        self.cbx_pms_voltage_range.addItem("")
        self.cbx_pms_voltage_range.setObjectName(u"cbx_pms_voltage_range")
        self.cbx_pms_voltage_range.setMaximumSize(QSize(16777215, 54))
        self.cbx_pms_voltage_range.setFont(font10)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.cbx_pms_voltage_range)

        self.label_pms_current_range = QLabel(self.frame_pms_control__range)
        self.label_pms_current_range.setObjectName(u"label_pms_current_range")
        self.label_pms_current_range.setFont(font10)
        self.label_pms_current_range.setStyleSheet(u"border:none;")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_pms_current_range)

        self.cbx_pms_current_range = QComboBox(self.frame_pms_control__range)
        self.cbx_pms_current_range.addItem("")
        self.cbx_pms_current_range.addItem("")
        self.cbx_pms_current_range.setObjectName(u"cbx_pms_current_range")
        self.cbx_pms_current_range.setMaximumSize(QSize(16777215, 54))
        self.cbx_pms_current_range.setFont(font10)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.cbx_pms_current_range)


        self.verticalLayout_28.addWidget(self.frame_pms_control__range)

        self.frame_pms_control_lower = QFrame(self.frame_pms_control)
        self.frame_pms_control_lower.setObjectName(u"frame_pms_control_lower")
        self.frame_pms_control_lower.setStyleSheet(u"border:none;")
        self.frame_pms_control_lower.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_control_lower.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_pms_control_lower)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.frame_pms_integration = QFrame(self.frame_pms_control_lower)
        self.frame_pms_integration.setObjectName(u"frame_pms_integration")
        self.frame_pms_integration.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;")
        self.frame_pms_integration.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_integration.setFrameShadow(QFrame.Raised)
        self.verticalLayout_25 = QVBoxLayout(self.frame_pms_integration)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.label_pms_integration = QLabel(self.frame_pms_integration)
        self.label_pms_integration.setObjectName(u"label_pms_integration")
        sizePolicy.setHeightForWidth(self.label_pms_integration.sizePolicy().hasHeightForWidth())
        self.label_pms_integration.setSizePolicy(sizePolicy)
        self.label_pms_integration.setMinimumSize(QSize(0, 20))
        self.label_pms_integration.setMaximumSize(QSize(16777215, 20))
        self.label_pms_integration.setFont(font10)
        self.label_pms_integration.setStyleSheet(u"border:none;")

        self.verticalLayout_25.addWidget(self.label_pms_integration)

        self.btn_pms_integration_start = QPushButton(self.frame_pms_integration)
        self.btn_pms_integration_start.setObjectName(u"btn_pms_integration_start")
        self.btn_pms_integration_start.setFont(font10)
        self.btn_pms_integration_start.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_25.addWidget(self.btn_pms_integration_start)

        self.btn_pms_integration_stop = QPushButton(self.frame_pms_integration)
        self.btn_pms_integration_stop.setObjectName(u"btn_pms_integration_stop")
        self.btn_pms_integration_stop.setFont(font10)
        self.btn_pms_integration_stop.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_25.addWidget(self.btn_pms_integration_stop)

        self.btn_pms_integration_reset = QPushButton(self.frame_pms_integration)
        self.btn_pms_integration_reset.setObjectName(u"btn_pms_integration_reset")
        self.btn_pms_integration_reset.setFont(font10)
        self.btn_pms_integration_reset.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_25.addWidget(self.btn_pms_integration_reset)


        self.horizontalLayout_18.addWidget(self.frame_pms_integration)

        self.frame_pms_averaging = QFrame(self.frame_pms_control_lower)
        self.frame_pms_averaging.setObjectName(u"frame_pms_averaging")
        self.frame_pms_averaging.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;")
        self.frame_pms_averaging.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_averaging.setFrameShadow(QFrame.Raised)
        self.verticalLayout_26 = QVBoxLayout(self.frame_pms_averaging)
        self.verticalLayout_26.setSpacing(2)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.verticalLayout_26.setContentsMargins(-1, 5, -1, 5)
        self.label_pms_averaging = QLabel(self.frame_pms_averaging)
        self.label_pms_averaging.setObjectName(u"label_pms_averaging")
        sizePolicy.setHeightForWidth(self.label_pms_averaging.sizePolicy().hasHeightForWidth())
        self.label_pms_averaging.setSizePolicy(sizePolicy)
        self.label_pms_averaging.setMinimumSize(QSize(0, 20))
        self.label_pms_averaging.setMaximumSize(QSize(16777215, 20))
        self.label_pms_averaging.setFont(font10)
        self.label_pms_averaging.setStyleSheet(u"border:none;")

        self.verticalLayout_26.addWidget(self.label_pms_averaging)

        self.btn_pms_averaging_toggle = QPushButton(self.frame_pms_averaging)
        self.btn_pms_averaging_toggle.setObjectName(u"btn_pms_averaging_toggle")
        self.btn_pms_averaging_toggle.setFont(font10)
        self.btn_pms_averaging_toggle.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_26.addWidget(self.btn_pms_averaging_toggle)

        self.cbx_pms_averaging_count = QComboBox(self.frame_pms_averaging)
        self.cbx_pms_averaging_count.addItem("")
        self.cbx_pms_averaging_count.addItem("")
        self.cbx_pms_averaging_count.addItem("")
        self.cbx_pms_averaging_count.setObjectName(u"cbx_pms_averaging_count")
        self.cbx_pms_averaging_count.setMaximumSize(QSize(16777215, 40))
        self.cbx_pms_averaging_count.setFont(font10)

        self.verticalLayout_26.addWidget(self.cbx_pms_averaging_count)

        self.cbx_pms_averaging_mode = QComboBox(self.frame_pms_averaging)
        self.cbx_pms_averaging_mode.addItem("")
        self.cbx_pms_averaging_mode.addItem("")
        self.cbx_pms_averaging_mode.setObjectName(u"cbx_pms_averaging_mode")
        self.cbx_pms_averaging_mode.setMaximumSize(QSize(16777215, 40))
        self.cbx_pms_averaging_mode.setFont(font10)

        self.verticalLayout_26.addWidget(self.cbx_pms_averaging_mode)


        self.horizontalLayout_18.addWidget(self.frame_pms_averaging)

        self.frame_pms_measure_mode = QFrame(self.frame_pms_control_lower)
        self.frame_pms_measure_mode.setObjectName(u"frame_pms_measure_mode")
        self.frame_pms_measure_mode.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;")
        self.frame_pms_measure_mode.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_measure_mode.setFrameShadow(QFrame.Raised)
        self.verticalLayout_27 = QVBoxLayout(self.frame_pms_measure_mode)
        self.verticalLayout_27.setSpacing(13)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(13, 13, 13, 13)
        self.label_pms_measure_mode = QLabel(self.frame_pms_measure_mode)
        self.label_pms_measure_mode.setObjectName(u"label_pms_measure_mode")
        sizePolicy.setHeightForWidth(self.label_pms_measure_mode.sizePolicy().hasHeightForWidth())
        self.label_pms_measure_mode.setSizePolicy(sizePolicy)
        self.label_pms_measure_mode.setMaximumSize(QSize(16777215, 20))
        self.label_pms_measure_mode.setFont(font10)
        self.label_pms_measure_mode.setStyleSheet(u"border:none;")

        self.verticalLayout_27.addWidget(self.label_pms_measure_mode)

        self.btn_pms_measure_mode = QPushButton(self.frame_pms_measure_mode)
        self.btn_pms_measure_mode.setObjectName(u"btn_pms_measure_mode")
        self.btn_pms_measure_mode.setFont(font10)
        self.btn_pms_measure_mode.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_27.addWidget(self.btn_pms_measure_mode)


        self.horizontalLayout_18.addWidget(self.frame_pms_measure_mode)


        self.verticalLayout_28.addWidget(self.frame_pms_control_lower)


        self.horizontalLayout_14.addWidget(self.frame_pms_control)


        self.verticalLayout_17.addWidget(self.frame_pms_contents)


        self.horizontalLayout_9.addWidget(self.frame_manual_control_pms)

        self.frame_manual_control_pml = QFrame(self.frame_manual_control_upper)
        self.frame_manual_control_pml.setObjectName(u"frame_manual_control_pml")
        self.frame_manual_control_pml.setEnabled(True)
        self.frame_manual_control_pml.setMinimumSize(QSize(300, 0))
        self.frame_manual_control_pml.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"};")
        self.frame_manual_control_pml.setFrameShape(QFrame.NoFrame)
        self.frame_manual_control_pml.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_19 = QVBoxLayout(self.frame_manual_control_pml)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.label_load_power_meter = QLabel(self.frame_manual_control_pml)
        self.label_load_power_meter.setObjectName(u"label_load_power_meter")
        self.label_load_power_meter.setMaximumSize(QSize(16777215, 30))
        self.label_load_power_meter.setFont(font1)
        self.label_load_power_meter.setCursor(QCursor(Qt.ArrowCursor))
        self.label_load_power_meter.setStyleSheet(u"QLabel{border:none;}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_load_power_meter.setAlignment(Qt.AlignCenter)

        self.verticalLayout_19.addWidget(self.label_load_power_meter)

        self.frame_pml_contents = QFrame(self.frame_manual_control_pml)
        self.frame_pml_contents.setObjectName(u"frame_pml_contents")
        self.frame_pml_contents.setStyleSheet(u"border:none;")
        self.frame_pml_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_pml_contents.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_pml_contents)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.frame_pml_display = QFrame(self.frame_pml_contents)
        self.frame_pml_display.setObjectName(u"frame_pml_display")
        self.frame_pml_display.setMinimumSize(QSize(0, 280))
        self.frame_pml_display.setMaximumSize(QSize(300, 16777215))
        self.frame_pml_display.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}")
        self.frame_pml_display.setFrameShape(QFrame.StyledPanel)
        self.frame_pml_display.setFrameShadow(QFrame.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.frame_pml_display)
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.label_pml_display_a = QLabel(self.frame_pml_display)
        self.label_pml_display_a.setObjectName(u"label_pml_display_a")
        self.label_pml_display_a.setMinimumSize(QSize(0, 70))
        self.label_pml_display_a.setMaximumSize(QSize(16777215, 70))
        self.label_pml_display_a.setFont(font12)
        self.label_pml_display_a.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_pml_display_a.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_20.addWidget(self.label_pml_display_a)

        self.label_pml_display_b = QLabel(self.frame_pml_display)
        self.label_pml_display_b.setObjectName(u"label_pml_display_b")
        self.label_pml_display_b.setMinimumSize(QSize(0, 70))
        self.label_pml_display_b.setMaximumSize(QSize(16777215, 70))
        self.label_pml_display_b.setFont(font12)
        self.label_pml_display_b.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_pml_display_b.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_20.addWidget(self.label_pml_display_b)

        self.label_pml_display_c = QLabel(self.frame_pml_display)
        self.label_pml_display_c.setObjectName(u"label_pml_display_c")
        self.label_pml_display_c.setMinimumSize(QSize(0, 70))
        self.label_pml_display_c.setMaximumSize(QSize(16777215, 70))
        self.label_pml_display_c.setFont(font12)
        self.label_pml_display_c.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_pml_display_c.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_20.addWidget(self.label_pml_display_c)

        self.label_pml_display_d = QLabel(self.frame_pml_display)
        self.label_pml_display_d.setObjectName(u"label_pml_display_d")
        self.label_pml_display_d.setMinimumSize(QSize(0, 70))
        self.label_pml_display_d.setMaximumSize(QSize(16777215, 70))
        self.label_pml_display_d.setFont(font12)
        self.label_pml_display_d.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_pml_display_d.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_20.addWidget(self.label_pml_display_d)


        self.horizontalLayout_15.addWidget(self.frame_pml_display)

        self.frame_pml_display_select = QFrame(self.frame_pml_contents)
        self.frame_pml_display_select.setObjectName(u"frame_pml_display_select")
        self.frame_pml_display_select.setMaximumSize(QSize(100, 16777215))
        self.frame_pml_display_select.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_pml_display_select.setFrameShape(QFrame.StyledPanel)
        self.frame_pml_display_select.setFrameShadow(QFrame.Raised)
        self.verticalLayout_21 = QVBoxLayout(self.frame_pml_display_select)
        self.verticalLayout_21.setSpacing(0)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.cbx_pml_display_a = QComboBox(self.frame_pml_display_select)
        self.cbx_pml_display_a.setObjectName(u"cbx_pml_display_a")
        self.cbx_pml_display_a.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_21.addWidget(self.cbx_pml_display_a)

        self.cbx_pml_display_b = QComboBox(self.frame_pml_display_select)
        self.cbx_pml_display_b.setObjectName(u"cbx_pml_display_b")
        self.cbx_pml_display_b.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_21.addWidget(self.cbx_pml_display_b)

        self.cbx_pml_display_c = QComboBox(self.frame_pml_display_select)
        self.cbx_pml_display_c.setObjectName(u"cbx_pml_display_c")
        self.cbx_pml_display_c.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_21.addWidget(self.cbx_pml_display_c)

        self.cbx_pml_display_d = QComboBox(self.frame_pml_display_select)
        self.cbx_pml_display_d.setObjectName(u"cbx_pml_display_d")
        self.cbx_pml_display_d.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_21.addWidget(self.cbx_pml_display_d)


        self.horizontalLayout_15.addWidget(self.frame_pml_display_select)

        self.frame_pml_control = QFrame(self.frame_pml_contents)
        self.frame_pml_control.setObjectName(u"frame_pml_control")
        self.frame_pml_control.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"")
        self.frame_pml_control.setFrameShape(QFrame.StyledPanel)
        self.frame_pml_control.setFrameShadow(QFrame.Raised)
        self.verticalLayout_29 = QVBoxLayout(self.frame_pml_control)
        self.verticalLayout_29.setSpacing(0)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.frame_pml_control__range = QFrame(self.frame_pml_control)
        self.frame_pml_control__range.setObjectName(u"frame_pml_control__range")
        self.frame_pml_control__range.setFrameShape(QFrame.StyledPanel)
        self.frame_pml_control__range.setFrameShadow(QFrame.Raised)
        self.formLayout_2 = QFormLayout(self.frame_pml_control__range)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_pml_voltage_range = QLabel(self.frame_pml_control__range)
        self.label_pml_voltage_range.setObjectName(u"label_pml_voltage_range")
        self.label_pml_voltage_range.setFont(font10)
        self.label_pml_voltage_range.setStyleSheet(u"border:none;")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_pml_voltage_range)

        self.cbx_pml_voltage_range = QComboBox(self.frame_pml_control__range)
        self.cbx_pml_voltage_range.addItem("")
        self.cbx_pml_voltage_range.addItem("")
        self.cbx_pml_voltage_range.setObjectName(u"cbx_pml_voltage_range")
        self.cbx_pml_voltage_range.setMaximumSize(QSize(16777215, 54))
        self.cbx_pml_voltage_range.setFont(font10)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.cbx_pml_voltage_range)

        self.label_pml_current_range = QLabel(self.frame_pml_control__range)
        self.label_pml_current_range.setObjectName(u"label_pml_current_range")
        self.label_pml_current_range.setFont(font10)
        self.label_pml_current_range.setStyleSheet(u"border:none;")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_pml_current_range)

        self.cbx_pml_current_range = QComboBox(self.frame_pml_control__range)
        self.cbx_pml_current_range.addItem("")
        self.cbx_pml_current_range.addItem("")
        self.cbx_pml_current_range.setObjectName(u"cbx_pml_current_range")
        self.cbx_pml_current_range.setMaximumSize(QSize(16777215, 54))
        self.cbx_pml_current_range.setFont(font10)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.cbx_pml_current_range)


        self.verticalLayout_29.addWidget(self.frame_pml_control__range)

        self.frame_pml_control_lower = QFrame(self.frame_pml_control)
        self.frame_pml_control_lower.setObjectName(u"frame_pml_control_lower")
        self.frame_pml_control_lower.setStyleSheet(u"border:none;")
        self.frame_pml_control_lower.setFrameShape(QFrame.StyledPanel)
        self.frame_pml_control_lower.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_pml_control_lower)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.frame_pml_integration = QFrame(self.frame_pml_control_lower)
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
        self.label_pml_integration.setMinimumSize(QSize(0, 20))
        self.label_pml_integration.setMaximumSize(QSize(16777215, 20))
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


        self.horizontalLayout_19.addWidget(self.frame_pml_integration)

        self.frame_pml_averaging = QFrame(self.frame_pml_control_lower)
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
        self.label_pml_averaging.setMinimumSize(QSize(0, 20))
        self.label_pml_averaging.setMaximumSize(QSize(16777215, 20))
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
        self.cbx_pml_averaging_count.setMaximumSize(QSize(16777215, 40))
        self.cbx_pml_averaging_count.setFont(font10)

        self.verticalLayout_31.addWidget(self.cbx_pml_averaging_count)

        self.cbx_pml_averaging_mode = QComboBox(self.frame_pml_averaging)
        self.cbx_pml_averaging_mode.addItem("")
        self.cbx_pml_averaging_mode.addItem("")
        self.cbx_pml_averaging_mode.setObjectName(u"cbx_pml_averaging_mode")
        self.cbx_pml_averaging_mode.setMaximumSize(QSize(16777215, 40))
        self.cbx_pml_averaging_mode.setFont(font10)

        self.verticalLayout_31.addWidget(self.cbx_pml_averaging_mode)


        self.horizontalLayout_19.addWidget(self.frame_pml_averaging)

        self.frame_pml_measure_mode = QFrame(self.frame_pml_control_lower)
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
        self.label_pml_measure_mode.setMaximumSize(QSize(16777215, 20))
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


        self.horizontalLayout_19.addWidget(self.frame_pml_measure_mode)


        self.verticalLayout_29.addWidget(self.frame_pml_control_lower)


        self.horizontalLayout_15.addWidget(self.frame_pml_control)


        self.verticalLayout_19.addWidget(self.frame_pml_contents)


        self.horizontalLayout_9.addWidget(self.frame_manual_control_pml)


        self.verticalLayout_12.addWidget(self.frame_manual_control_upper)

        self.frame_manual_control_lower = QFrame(self.page_manual_control)
        self.frame_manual_control_lower.setObjectName(u"frame_manual_control_lower")
        self.frame_manual_control_lower.setStyleSheet(u"")
        self.frame_manual_control_lower.setFrameShape(QFrame.NoFrame)
        self.frame_manual_control_lower.setFrameShadow(QFrame.Raised)
        self.frame_manual_control_lower.setLineWidth(0)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_manual_control_lower)
        self.horizontalLayout_13.setSpacing(1)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(1, 1, 1, 1)
        self.frame_manual_control_setup_equipment = QFrame(self.frame_manual_control_lower)
        self.frame_manual_control_setup_equipment.setObjectName(u"frame_manual_control_setup_equipment")
        sizePolicy5.setHeightForWidth(self.frame_manual_control_setup_equipment.sizePolicy().hasHeightForWidth())
        self.frame_manual_control_setup_equipment.setSizePolicy(sizePolicy5)
        self.frame_manual_control_setup_equipment.setMinimumSize(QSize(100, 0))
        self.frame_manual_control_setup_equipment.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_manual_control_setup_equipment.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_setup_equipment.setFrameShadow(QFrame.Raised)
        self.verticalLayout_34 = QVBoxLayout(self.frame_manual_control_setup_equipment)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.btn_manual_control_setup_equipment = QPushButton(self.frame_manual_control_setup_equipment)
        self.btn_manual_control_setup_equipment.setObjectName(u"btn_manual_control_setup_equipment")
        self.btn_manual_control_setup_equipment.setMinimumSize(QSize(100, 120))
        self.btn_manual_control_setup_equipment.setFont(font4)
        self.btn_manual_control_setup_equipment.setStyleSheet(u"QPushButton {\n"
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
        self.btn_manual_control_setup_equipment.setCheckable(False)
        self.btn_manual_control_setup_equipment.setChecked(False)

        self.verticalLayout_34.addWidget(self.btn_manual_control_setup_equipment)


        self.horizontalLayout_13.addWidget(self.frame_manual_control_setup_equipment)

        self.frame_manual_control_ac_source = QFrame(self.frame_manual_control_lower)
        self.frame_manual_control_ac_source.setObjectName(u"frame_manual_control_ac_source")
        sizePolicy18 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy18.setHorizontalStretch(2)
        sizePolicy18.setVerticalStretch(0)
        sizePolicy18.setHeightForWidth(self.frame_manual_control_ac_source.sizePolicy().hasHeightForWidth())
        self.frame_manual_control_ac_source.setSizePolicy(sizePolicy18)
        self.frame_manual_control_ac_source.setMinimumSize(QSize(300, 0))
        self.frame_manual_control_ac_source.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_manual_control_ac_source.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_ac_source.setFrameShadow(QFrame.Raised)
        self.verticalLayout_24 = QVBoxLayout(self.frame_manual_control_ac_source)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.label_manual_control_ac_source = QLabel(self.frame_manual_control_ac_source)
        self.label_manual_control_ac_source.setObjectName(u"label_manual_control_ac_source")
        self.label_manual_control_ac_source.setMaximumSize(QSize(16777215, 30))
        self.label_manual_control_ac_source.setFont(font1)
        self.label_manual_control_ac_source.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_manual_control_ac_source.setStyleSheet(u"QLabel{border:none;}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_manual_control_ac_source.setAlignment(Qt.AlignCenter)

        self.verticalLayout_24.addWidget(self.label_manual_control_ac_source)

        self.frame_ac_source_contents = QFrame(self.frame_manual_control_ac_source)
        self.frame_ac_source_contents.setObjectName(u"frame_ac_source_contents")
        self.frame_ac_source_contents.setStyleSheet(u"border:none;")
        self.frame_ac_source_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_ac_source_contents.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_ac_source_contents)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.frame_manual_control_ac_source_params = QFrame(self.frame_ac_source_contents)
        self.frame_manual_control_ac_source_params.setObjectName(u"frame_manual_control_ac_source_params")
        self.frame_manual_control_ac_source_params.setStyleSheet(u"QFrame{\n"
"	border:1px solid black;\n"
"	border-radius: 5px;\n"
"};")
        self.frame_manual_control_ac_source_params.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_ac_source_params.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_manual_control_ac_source_params)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lineedit_manual_control_ac_source_frequency = QLineEdit(self.frame_manual_control_ac_source_params)
        self.lineedit_manual_control_ac_source_frequency.setObjectName(u"lineedit_manual_control_ac_source_frequency")
        self.lineedit_manual_control_ac_source_frequency.setMinimumSize(QSize(0, 30))
        self.lineedit_manual_control_ac_source_frequency.setFont(font10)
        self.lineedit_manual_control_ac_source_frequency.setStyleSheet(u"QLineEdit {\n"
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

        self.gridLayout_3.addWidget(self.lineedit_manual_control_ac_source_frequency, 1, 1, 1, 1)

        self.label_manual_control_ac_source_voltage = QLabel(self.frame_manual_control_ac_source_params)
        self.label_manual_control_ac_source_voltage.setObjectName(u"label_manual_control_ac_source_voltage")
        sizePolicy.setHeightForWidth(self.label_manual_control_ac_source_voltage.sizePolicy().hasHeightForWidth())
        self.label_manual_control_ac_source_voltage.setSizePolicy(sizePolicy)
        self.label_manual_control_ac_source_voltage.setMinimumSize(QSize(0, 30))
        self.label_manual_control_ac_source_voltage.setMaximumSize(QSize(16777215, 30))
        self.label_manual_control_ac_source_voltage.setFont(font10)
        self.label_manual_control_ac_source_voltage.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}\n"
"\n"
"QLabel{\n"
"border:none\n"
"}")

        self.gridLayout_3.addWidget(self.label_manual_control_ac_source_voltage, 0, 0, 1, 1)

        self.lineedit_manual_control_ac_source_voltage = QLineEdit(self.frame_manual_control_ac_source_params)
        self.lineedit_manual_control_ac_source_voltage.setObjectName(u"lineedit_manual_control_ac_source_voltage")
        self.lineedit_manual_control_ac_source_voltage.setMinimumSize(QSize(0, 30))
        self.lineedit_manual_control_ac_source_voltage.setFont(font10)
        self.lineedit_manual_control_ac_source_voltage.setStyleSheet(u"QLineEdit {\n"
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

        self.gridLayout_3.addWidget(self.lineedit_manual_control_ac_source_voltage, 0, 1, 1, 1)

        self.label_manual_control_ac_source_frequency = QLabel(self.frame_manual_control_ac_source_params)
        self.label_manual_control_ac_source_frequency.setObjectName(u"label_manual_control_ac_source_frequency")
        sizePolicy.setHeightForWidth(self.label_manual_control_ac_source_frequency.sizePolicy().hasHeightForWidth())
        self.label_manual_control_ac_source_frequency.setSizePolicy(sizePolicy)
        self.label_manual_control_ac_source_frequency.setMinimumSize(QSize(0, 30))
        self.label_manual_control_ac_source_frequency.setMaximumSize(QSize(16777215, 30))
        self.label_manual_control_ac_source_frequency.setFont(font10)
        self.label_manual_control_ac_source_frequency.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}\n"
"\n"
"QLabel{\n"
"border:none\n"
"}")

        self.gridLayout_3.addWidget(self.label_manual_control_ac_source_frequency, 1, 0, 1, 1)

        self.chkbox_manual_control_ac_source_coupling = QCheckBox(self.frame_manual_control_ac_source_params)
        self.chkbox_manual_control_ac_source_coupling.setObjectName(u"chkbox_manual_control_ac_source_coupling")
        sizePolicy19 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy19.setHorizontalStretch(0)
        sizePolicy19.setVerticalStretch(0)
        sizePolicy19.setHeightForWidth(self.chkbox_manual_control_ac_source_coupling.sizePolicy().hasHeightForWidth())
        self.chkbox_manual_control_ac_source_coupling.setSizePolicy(sizePolicy19)
        self.chkbox_manual_control_ac_source_coupling.setMinimumSize(QSize(0, 0))
        self.chkbox_manual_control_ac_source_coupling.setFont(font10)
        self.chkbox_manual_control_ac_source_coupling.setStyleSheet(u"QCheckBox:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_3.addWidget(self.chkbox_manual_control_ac_source_coupling, 2, 0, 1, 1)


        self.horizontalLayout_17.addWidget(self.frame_manual_control_ac_source_params)

        self.frame_manual_control_ac_source_buttons = QFrame(self.frame_ac_source_contents)
        self.frame_manual_control_ac_source_buttons.setObjectName(u"frame_manual_control_ac_source_buttons")
        sizePolicy5.setHeightForWidth(self.frame_manual_control_ac_source_buttons.sizePolicy().hasHeightForWidth())
        self.frame_manual_control_ac_source_buttons.setSizePolicy(sizePolicy5)
        self.frame_manual_control_ac_source_buttons.setStyleSheet(u"QFrame{\n"
"	border:1px solid black;\n"
"	border-radius: 5px;\n"
"};")
        self.frame_manual_control_ac_source_buttons.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_ac_source_buttons.setFrameShadow(QFrame.Raised)
        self.verticalLayout_37 = QVBoxLayout(self.frame_manual_control_ac_source_buttons)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.btn_manual_control_ac_source_turn_on = QPushButton(self.frame_manual_control_ac_source_buttons)
        self.btn_manual_control_ac_source_turn_on.setObjectName(u"btn_manual_control_ac_source_turn_on")
        self.btn_manual_control_ac_source_turn_on.setMinimumSize(QSize(100, 80))
        font13 = QFont()
        font13.setFamily(u"Segoe UI")
        font13.setPointSize(9)
        self.btn_manual_control_ac_source_turn_on.setFont(font13)
        self.btn_manual_control_ac_source_turn_on.setStyleSheet(u"QPushButton {\n"
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
        icon8 = QIcon()
        icon8.addFile(u":/20x20/icons/20x20/cil-power-standby-green.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_manual_control_ac_source_turn_on.setIcon(icon8)
        self.btn_manual_control_ac_source_turn_on.setCheckable(False)
        self.btn_manual_control_ac_source_turn_on.setChecked(False)

        self.verticalLayout_37.addWidget(self.btn_manual_control_ac_source_turn_on)

        self.btn_manual_control_ac_source_turn_off = QPushButton(self.frame_manual_control_ac_source_buttons)
        self.btn_manual_control_ac_source_turn_off.setObjectName(u"btn_manual_control_ac_source_turn_off")
        self.btn_manual_control_ac_source_turn_off.setMinimumSize(QSize(100, 80))
        self.btn_manual_control_ac_source_turn_off.setFont(font13)
        self.btn_manual_control_ac_source_turn_off.setStyleSheet(u"QPushButton {\n"
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
        icon9 = QIcon()
        icon9.addFile(u":/20x20/icons/20x20/cil-power-standby-red.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_manual_control_ac_source_turn_off.setIcon(icon9)
        self.btn_manual_control_ac_source_turn_off.setCheckable(False)
        self.btn_manual_control_ac_source_turn_off.setChecked(False)

        self.verticalLayout_37.addWidget(self.btn_manual_control_ac_source_turn_off)


        self.horizontalLayout_17.addWidget(self.frame_manual_control_ac_source_buttons)


        self.verticalLayout_24.addWidget(self.frame_ac_source_contents)


        self.horizontalLayout_13.addWidget(self.frame_manual_control_ac_source)

        self.frame_manual_control_eload = QFrame(self.frame_manual_control_lower)
        self.frame_manual_control_eload.setObjectName(u"frame_manual_control_eload")
        sizePolicy20 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy20.setHorizontalStretch(3)
        sizePolicy20.setVerticalStretch(0)
        sizePolicy20.setHeightForWidth(self.frame_manual_control_eload.sizePolicy().hasHeightForWidth())
        self.frame_manual_control_eload.setSizePolicy(sizePolicy20)
        self.frame_manual_control_eload.setMinimumSize(QSize(400, 0))
        self.frame_manual_control_eload.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_manual_control_eload.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_eload.setFrameShadow(QFrame.Raised)
        self.verticalLayout_23 = QVBoxLayout(self.frame_manual_control_eload)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.label_manual_control_eload = QLabel(self.frame_manual_control_eload)
        self.label_manual_control_eload.setObjectName(u"label_manual_control_eload")
        self.label_manual_control_eload.setMaximumSize(QSize(16777215, 30))
        self.label_manual_control_eload.setFont(font1)
        self.label_manual_control_eload.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_manual_control_eload.setStyleSheet(u"QLabel{border:none;}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_manual_control_eload.setAlignment(Qt.AlignCenter)

        self.verticalLayout_23.addWidget(self.label_manual_control_eload)

        self.frame_manual_control_eload_contents = QFrame(self.frame_manual_control_eload)
        self.frame_manual_control_eload_contents.setObjectName(u"frame_manual_control_eload_contents")
        self.frame_manual_control_eload_contents.setStyleSheet(u"border:none;")
        self.frame_manual_control_eload_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_eload_contents.setFrameShadow(QFrame.Raised)
        self.verticalLayout_77 = QVBoxLayout(self.frame_manual_control_eload_contents)
        self.verticalLayout_77.setObjectName(u"verticalLayout_77")
        self.frame_manual_control_eload_top = QFrame(self.frame_manual_control_eload_contents)
        self.frame_manual_control_eload_top.setObjectName(u"frame_manual_control_eload_top")
        self.frame_manual_control_eload_top.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_eload_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_47 = QHBoxLayout(self.frame_manual_control_eload_top)
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.cbx_manual_control_eload_type = QComboBox(self.frame_manual_control_eload_top)
        self.cbx_manual_control_eload_type.addItem("")
        self.cbx_manual_control_eload_type.addItem("")
        self.cbx_manual_control_eload_type.addItem("")
        self.cbx_manual_control_eload_type.setObjectName(u"cbx_manual_control_eload_type")
        self.cbx_manual_control_eload_type.setMaximumSize(QSize(16777215, 40))
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

        self.btn_manual_control_eload_a_b_swap = QPushButton(self.frame_manual_control_eload_top)
        self.btn_manual_control_eload_a_b_swap.setObjectName(u"btn_manual_control_eload_a_b_swap")
        self.btn_manual_control_eload_a_b_swap.setMinimumSize(QSize(120, 40))
        self.btn_manual_control_eload_a_b_swap.setFont(font13)
        self.btn_manual_control_eload_a_b_swap.setStyleSheet(u"QPushButton {\n"
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
        icon10.addFile(u":/20x20/icons/20x20/cil-swap-horizontal.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_manual_control_eload_a_b_swap.setIcon(icon10)
        self.btn_manual_control_eload_a_b_swap.setCheckable(False)
        self.btn_manual_control_eload_a_b_swap.setChecked(False)

        self.horizontalLayout_47.addWidget(self.btn_manual_control_eload_a_b_swap)


        self.verticalLayout_77.addWidget(self.frame_manual_control_eload_top)

        self.frame_manual_control_eload_center = QFrame(self.frame_manual_control_eload_contents)
        self.frame_manual_control_eload_center.setObjectName(u"frame_manual_control_eload_center")
        self.frame_manual_control_eload_center.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_eload_center.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_46 = QHBoxLayout(self.frame_manual_control_eload_center)
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.frame_manual_control_eload_level = QFrame(self.frame_manual_control_eload_center)
        self.frame_manual_control_eload_level.setObjectName(u"frame_manual_control_eload_level")
        self.frame_manual_control_eload_level.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_eload_level.setFrameShadow(QFrame.Raised)
        self.verticalLayout_70 = QVBoxLayout(self.frame_manual_control_eload_level)
        self.verticalLayout_70.setObjectName(u"verticalLayout_70")
        self.frame_manual_control_eload_a = QFrame(self.frame_manual_control_eload_level)
        self.frame_manual_control_eload_a.setObjectName(u"frame_manual_control_eload_a")
        self.frame_manual_control_eload_a.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_eload_a.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_45 = QHBoxLayout(self.frame_manual_control_eload_a)
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.label_manual_control_eload_a = QLabel(self.frame_manual_control_eload_a)
        self.label_manual_control_eload_a.setObjectName(u"label_manual_control_eload_a")
        self.label_manual_control_eload_a.setMaximumSize(QSize(16777215, 30))
        self.label_manual_control_eload_a.setFont(font10)
        self.label_manual_control_eload_a.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}\n"
"\n"
"QLabel{\n"
"border:none\n"
"}")
        self.label_manual_control_eload_a.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_45.addWidget(self.label_manual_control_eload_a)

        self.lineedit_manual_control_eload_a_level = QLineEdit(self.frame_manual_control_eload_a)
        self.lineedit_manual_control_eload_a_level.setObjectName(u"lineedit_manual_control_eload_a_level")
        sizePolicy21 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy21.setHorizontalStretch(4)
        sizePolicy21.setVerticalStretch(0)
        sizePolicy21.setHeightForWidth(self.lineedit_manual_control_eload_a_level.sizePolicy().hasHeightForWidth())
        self.lineedit_manual_control_eload_a_level.setSizePolicy(sizePolicy21)
        self.lineedit_manual_control_eload_a_level.setMinimumSize(QSize(0, 40))
        self.lineedit_manual_control_eload_a_level.setFont(font10)
        self.lineedit_manual_control_eload_a_level.setStyleSheet(u"QLineEdit {\n"
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

        self.horizontalLayout_45.addWidget(self.lineedit_manual_control_eload_a_level)

        self.label_manual_control_eload_a_level_unit = QLabel(self.frame_manual_control_eload_a)
        self.label_manual_control_eload_a_level_unit.setObjectName(u"label_manual_control_eload_a_level_unit")
        sizePolicy11.setHeightForWidth(self.label_manual_control_eload_a_level_unit.sizePolicy().hasHeightForWidth())
        self.label_manual_control_eload_a_level_unit.setSizePolicy(sizePolicy11)
        self.label_manual_control_eload_a_level_unit.setMaximumSize(QSize(16777215, 30))
        self.label_manual_control_eload_a_level_unit.setFont(font10)
        self.label_manual_control_eload_a_level_unit.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}\n"
"\n"
"QLabel{\n"
"border:none\n"
"}")

        self.horizontalLayout_45.addWidget(self.label_manual_control_eload_a_level_unit)

        self.btn_manual_control_eload_set_A = QPushButton(self.frame_manual_control_eload_a)
        self.btn_manual_control_eload_set_A.setObjectName(u"btn_manual_control_eload_set_A")
        self.btn_manual_control_eload_set_A.setMinimumSize(QSize(50, 30))
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


        self.verticalLayout_70.addWidget(self.frame_manual_control_eload_a)

        self.frame_manual_control_eload_b = QFrame(self.frame_manual_control_eload_level)
        self.frame_manual_control_eload_b.setObjectName(u"frame_manual_control_eload_b")
        self.frame_manual_control_eload_b.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_eload_b.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_39 = QHBoxLayout(self.frame_manual_control_eload_b)
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.label_manual_control_eload_b = QLabel(self.frame_manual_control_eload_b)
        self.label_manual_control_eload_b.setObjectName(u"label_manual_control_eload_b")
        self.label_manual_control_eload_b.setMaximumSize(QSize(16777215, 30))
        self.label_manual_control_eload_b.setFont(font10)
        self.label_manual_control_eload_b.setLayoutDirection(Qt.LeftToRight)
        self.label_manual_control_eload_b.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}\n"
"\n"
"QLabel{\n"
"border:none\n"
"}")
        self.label_manual_control_eload_b.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_39.addWidget(self.label_manual_control_eload_b)

        self.lineedit_manual_control_eload_b_level = QLineEdit(self.frame_manual_control_eload_b)
        self.lineedit_manual_control_eload_b_level.setObjectName(u"lineedit_manual_control_eload_b_level")
        sizePolicy21.setHeightForWidth(self.lineedit_manual_control_eload_b_level.sizePolicy().hasHeightForWidth())
        self.lineedit_manual_control_eload_b_level.setSizePolicy(sizePolicy21)
        self.lineedit_manual_control_eload_b_level.setMinimumSize(QSize(0, 40))
        self.lineedit_manual_control_eload_b_level.setFont(font10)
        self.lineedit_manual_control_eload_b_level.setStyleSheet(u"QLineEdit {\n"
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

        self.horizontalLayout_39.addWidget(self.lineedit_manual_control_eload_b_level)

        self.label_manual_control_eload_b_level_unit = QLabel(self.frame_manual_control_eload_b)
        self.label_manual_control_eload_b_level_unit.setObjectName(u"label_manual_control_eload_b_level_unit")
        sizePolicy11.setHeightForWidth(self.label_manual_control_eload_b_level_unit.sizePolicy().hasHeightForWidth())
        self.label_manual_control_eload_b_level_unit.setSizePolicy(sizePolicy11)
        self.label_manual_control_eload_b_level_unit.setMaximumSize(QSize(16777215, 30))
        self.label_manual_control_eload_b_level_unit.setFont(font10)
        self.label_manual_control_eload_b_level_unit.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}\n"
"\n"
"QLabel{\n"
"border:none\n"
"}")

        self.horizontalLayout_39.addWidget(self.label_manual_control_eload_b_level_unit)

        self.btn_manual_control_eload_set_B = QPushButton(self.frame_manual_control_eload_b)
        self.btn_manual_control_eload_set_B.setObjectName(u"btn_manual_control_eload_set_B")
        self.btn_manual_control_eload_set_B.setMinimumSize(QSize(50, 30))
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

        self.horizontalLayout_39.addWidget(self.btn_manual_control_eload_set_B)


        self.verticalLayout_70.addWidget(self.frame_manual_control_eload_b)


        self.horizontalLayout_46.addWidget(self.frame_manual_control_eload_level)

        self.frame_manual_control_eload_slew = QFrame(self.frame_manual_control_eload_center)
        self.frame_manual_control_eload_slew.setObjectName(u"frame_manual_control_eload_slew")
        self.frame_manual_control_eload_slew.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_eload_slew.setFrameShadow(QFrame.Raised)
        self.gridLayout_29 = QGridLayout(self.frame_manual_control_eload_slew)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.frame_manual_control_eload_slew_fall = QFrame(self.frame_manual_control_eload_slew)
        self.frame_manual_control_eload_slew_fall.setObjectName(u"frame_manual_control_eload_slew_fall")
        self.frame_manual_control_eload_slew_fall.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_eload_slew_fall.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_38 = QHBoxLayout(self.frame_manual_control_eload_slew_fall)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.label_manual_control_electronic_load_fall = QLabel(self.frame_manual_control_eload_slew_fall)
        self.label_manual_control_electronic_load_fall.setObjectName(u"label_manual_control_electronic_load_fall")
        self.label_manual_control_electronic_load_fall.setMaximumSize(QSize(16777215, 30))
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

        self.horizontalLayout_38.addWidget(self.label_manual_control_electronic_load_fall)

        self.lineedit_manual_control_eload_slew_fall = QLineEdit(self.frame_manual_control_eload_slew_fall)
        self.lineedit_manual_control_eload_slew_fall.setObjectName(u"lineedit_manual_control_eload_slew_fall")
        sizePolicy21.setHeightForWidth(self.lineedit_manual_control_eload_slew_fall.sizePolicy().hasHeightForWidth())
        self.lineedit_manual_control_eload_slew_fall.setSizePolicy(sizePolicy21)
        self.lineedit_manual_control_eload_slew_fall.setMinimumSize(QSize(0, 40))
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

        self.horizontalLayout_38.addWidget(self.lineedit_manual_control_eload_slew_fall)

        self.label_manual_control_eload_slew_fall_unit = QLabel(self.frame_manual_control_eload_slew_fall)
        self.label_manual_control_eload_slew_fall_unit.setObjectName(u"label_manual_control_eload_slew_fall_unit")
        sizePolicy11.setHeightForWidth(self.label_manual_control_eload_slew_fall_unit.sizePolicy().hasHeightForWidth())
        self.label_manual_control_eload_slew_fall_unit.setSizePolicy(sizePolicy11)
        self.label_manual_control_eload_slew_fall_unit.setMaximumSize(QSize(16777215, 30))
        self.label_manual_control_eload_slew_fall_unit.setFont(font10)
        self.label_manual_control_eload_slew_fall_unit.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}\n"
"\n"
"QLabel{\n"
"border:none\n"
"}")

        self.horizontalLayout_38.addWidget(self.label_manual_control_eload_slew_fall_unit)


        self.gridLayout_29.addWidget(self.frame_manual_control_eload_slew_fall, 1, 0, 1, 1)

        self.frame_manual_control_eload_slew_rise = QFrame(self.frame_manual_control_eload_slew)
        self.frame_manual_control_eload_slew_rise.setObjectName(u"frame_manual_control_eload_slew_rise")
        self.frame_manual_control_eload_slew_rise.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_eload_slew_rise.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_36 = QHBoxLayout(self.frame_manual_control_eload_slew_rise)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.label_manual_control_electronic_load_rise = QLabel(self.frame_manual_control_eload_slew_rise)
        self.label_manual_control_electronic_load_rise.setObjectName(u"label_manual_control_electronic_load_rise")
        self.label_manual_control_electronic_load_rise.setMaximumSize(QSize(16777215, 30))
        self.label_manual_control_electronic_load_rise.setFont(font10)
        self.label_manual_control_electronic_load_rise.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}\n"
"\n"
"QLabel{\n"
"border:none\n"
"}")
        self.label_manual_control_electronic_load_rise.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_36.addWidget(self.label_manual_control_electronic_load_rise)

        self.lineedit_manual_control_eload_slew_rise = QLineEdit(self.frame_manual_control_eload_slew_rise)
        self.lineedit_manual_control_eload_slew_rise.setObjectName(u"lineedit_manual_control_eload_slew_rise")
        sizePolicy21.setHeightForWidth(self.lineedit_manual_control_eload_slew_rise.sizePolicy().hasHeightForWidth())
        self.lineedit_manual_control_eload_slew_rise.setSizePolicy(sizePolicy21)
        self.lineedit_manual_control_eload_slew_rise.setMinimumSize(QSize(0, 40))
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

        self.horizontalLayout_36.addWidget(self.lineedit_manual_control_eload_slew_rise)

        self.label_manual_control_eload_slew_rise_unit = QLabel(self.frame_manual_control_eload_slew_rise)
        self.label_manual_control_eload_slew_rise_unit.setObjectName(u"label_manual_control_eload_slew_rise_unit")
        sizePolicy11.setHeightForWidth(self.label_manual_control_eload_slew_rise_unit.sizePolicy().hasHeightForWidth())
        self.label_manual_control_eload_slew_rise_unit.setSizePolicy(sizePolicy11)
        self.label_manual_control_eload_slew_rise_unit.setMaximumSize(QSize(16777215, 30))
        self.label_manual_control_eload_slew_rise_unit.setFont(font10)
        self.label_manual_control_eload_slew_rise_unit.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}\n"
"\n"
"QLabel{\n"
"border:none\n"
"}")

        self.horizontalLayout_36.addWidget(self.label_manual_control_eload_slew_rise_unit)


        self.gridLayout_29.addWidget(self.frame_manual_control_eload_slew_rise, 0, 0, 1, 1)

        self.btn_manual_control_eload_set_slew = QPushButton(self.frame_manual_control_eload_slew)
        self.btn_manual_control_eload_set_slew.setObjectName(u"btn_manual_control_eload_set_slew")
        sizePolicy19.setHeightForWidth(self.btn_manual_control_eload_set_slew.sizePolicy().hasHeightForWidth())
        self.btn_manual_control_eload_set_slew.setSizePolicy(sizePolicy19)
        self.btn_manual_control_eload_set_slew.setMinimumSize(QSize(50, 60))
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


        self.horizontalLayout_46.addWidget(self.frame_manual_control_eload_slew)


        self.verticalLayout_77.addWidget(self.frame_manual_control_eload_center)

        self.frame_manual_control_eload_bottom = QFrame(self.frame_manual_control_eload_contents)
        self.frame_manual_control_eload_bottom.setObjectName(u"frame_manual_control_eload_bottom")
        self.frame_manual_control_eload_bottom.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_eload_bottom.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_56 = QHBoxLayout(self.frame_manual_control_eload_bottom)
        self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
        self.btn_manual_control_eload_turn_on = QPushButton(self.frame_manual_control_eload_bottom)
        self.btn_manual_control_eload_turn_on.setObjectName(u"btn_manual_control_eload_turn_on")
        self.btn_manual_control_eload_turn_on.setMinimumSize(QSize(120, 40))
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

        self.btn_manual_control_eload_turn_off = QPushButton(self.frame_manual_control_eload_bottom)
        self.btn_manual_control_eload_turn_off.setObjectName(u"btn_manual_control_eload_turn_off")
        self.btn_manual_control_eload_turn_off.setMinimumSize(QSize(120, 40))
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


        self.verticalLayout_77.addWidget(self.frame_manual_control_eload_bottom)


        self.verticalLayout_23.addWidget(self.frame_manual_control_eload_contents)


        self.horizontalLayout_13.addWidget(self.frame_manual_control_eload)

        self.frame_manual_control_usb_pd_sink = QFrame(self.frame_manual_control_lower)
        self.frame_manual_control_usb_pd_sink.setObjectName(u"frame_manual_control_usb_pd_sink")
        sizePolicy22 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy22.setHorizontalStretch(3)
        sizePolicy22.setVerticalStretch(0)
        sizePolicy22.setHeightForWidth(self.frame_manual_control_usb_pd_sink.sizePolicy().hasHeightForWidth())
        self.frame_manual_control_usb_pd_sink.setSizePolicy(sizePolicy22)
        self.frame_manual_control_usb_pd_sink.setMinimumSize(QSize(300, 0))
        self.frame_manual_control_usb_pd_sink.setStyleSheet(u"QFrame{\n"
"	border: 2px solid black;\n"
"	border-radius: 10px;\n"
"	background-color: rgb(29,34, 44);\n"
"}")
        self.frame_manual_control_usb_pd_sink.setFrameShape(QFrame.StyledPanel)
        self.frame_manual_control_usb_pd_sink.setFrameShadow(QFrame.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.frame_manual_control_usb_pd_sink)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.label_usbpdsink = QLabel(self.frame_manual_control_usb_pd_sink)
        self.label_usbpdsink.setObjectName(u"label_usbpdsink")
        self.label_usbpdsink.setMaximumSize(QSize(16777215, 30))
        self.label_usbpdsink.setFont(font1)
        self.label_usbpdsink.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_usbpdsink.setStyleSheet(u"QLabel{border:none;}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_usbpdsink.setAlignment(Qt.AlignCenter)

        self.verticalLayout_22.addWidget(self.label_usbpdsink)

        self.frame_usb_pd_sink_contents = QFrame(self.frame_manual_control_usb_pd_sink)
        self.frame_usb_pd_sink_contents.setObjectName(u"frame_usb_pd_sink_contents")
        self.frame_usb_pd_sink_contents.setStyleSheet(u"border:none;")
        self.frame_usb_pd_sink_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_usb_pd_sink_contents.setFrameShadow(QFrame.Raised)
        self.gridLayout_30 = QGridLayout(self.frame_usb_pd_sink_contents)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.label_usbpdsink_connection_status = QLabel(self.frame_usb_pd_sink_contents)
        self.label_usbpdsink_connection_status.setObjectName(u"label_usbpdsink_connection_status")
        sizePolicy11.setHeightForWidth(self.label_usbpdsink_connection_status.sizePolicy().hasHeightForWidth())
        self.label_usbpdsink_connection_status.setSizePolicy(sizePolicy11)
        self.label_usbpdsink_connection_status.setMaximumSize(QSize(16777215, 30))
        font14 = QFont()
        font14.setPointSize(9)
        self.label_usbpdsink_connection_status.setFont(font14)
        self.label_usbpdsink_connection_status.setStyleSheet(u"QLabel{\n"
"	color: rgb(255,0,0)\n"
"}\n"
"\n"
"QLabel:disabled{\n"
"	color: rgb(71,71,71)\n"
"}\n"
"\n"
"QLabel{\n"
"border:none\n"
"}")

        self.gridLayout_30.addWidget(self.label_usbpdsink_connection_status, 1, 1, 1, 1)

        self.label_usbpdsink_status = QLabel(self.frame_usb_pd_sink_contents)
        self.label_usbpdsink_status.setObjectName(u"label_usbpdsink_status")
        self.label_usbpdsink_status.setMaximumSize(QSize(16777215, 30))
        self.label_usbpdsink_status.setFont(font14)
        self.label_usbpdsink_status.setStyleSheet(u"QLabel{\n"
"	color: rgb(255,0,0)\n"
"}\n"
"\n"
"QLabel:disabled{\n"
"	color: rgb(71,71,71)\n"
"}\n"
"\n"
"QLabel{\n"
"border:none\n"
"}")

        self.gridLayout_30.addWidget(self.label_usbpdsink_status, 1, 2, 1, 1)

        self.frame_usbpdsink_request_sourcecaps = QFrame(self.frame_usb_pd_sink_contents)
        self.frame_usbpdsink_request_sourcecaps.setObjectName(u"frame_usbpdsink_request_sourcecaps")
        self.frame_usbpdsink_request_sourcecaps.setFrameShape(QFrame.StyledPanel)
        self.frame_usbpdsink_request_sourcecaps.setFrameShadow(QFrame.Raised)
        self.verticalLayout_33 = QVBoxLayout(self.frame_usbpdsink_request_sourcecaps)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.label_usbpdsink_sourcecaps = QLabel(self.frame_usbpdsink_request_sourcecaps)
        self.label_usbpdsink_sourcecaps.setObjectName(u"label_usbpdsink_sourcecaps")
        self.label_usbpdsink_sourcecaps.setMaximumSize(QSize(16777215, 30))
        self.label_usbpdsink_sourcecaps.setFont(font1)
        self.label_usbpdsink_sourcecaps.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_usbpdsink_sourcecaps.setStyleSheet(u"QLabel{border:none;}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_usbpdsink_sourcecaps.setAlignment(Qt.AlignCenter)

        self.verticalLayout_33.addWidget(self.label_usbpdsink_sourcecaps)

        self.list_usbpdsink_sourcecaps = QListWidget(self.frame_usbpdsink_request_sourcecaps)
        self.list_usbpdsink_sourcecaps.setObjectName(u"list_usbpdsink_sourcecaps")
        font15 = QFont()
        font15.setFamily(u"Consolas")
        font15.setPointSize(14)
        self.list_usbpdsink_sourcecaps.setFont(font15)
        self.list_usbpdsink_sourcecaps.setStyleSheet(u"background-color: rgb(19,24, 34);")

        self.verticalLayout_33.addWidget(self.list_usbpdsink_sourcecaps)


        self.gridLayout_30.addWidget(self.frame_usbpdsink_request_sourcecaps, 0, 0, 1, 3)

        self.frame_usbpdsink_request_param = QFrame(self.frame_usb_pd_sink_contents)
        self.frame_usbpdsink_request_param.setObjectName(u"frame_usbpdsink_request_param")
        self.frame_usbpdsink_request_param.setFrameShape(QFrame.StyledPanel)
        self.frame_usbpdsink_request_param.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_usbpdsink_request_param)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.frame_usbpdsink_request_param1 = QFrame(self.frame_usbpdsink_request_param)
        self.frame_usbpdsink_request_param1.setObjectName(u"frame_usbpdsink_request_param1")
        self.frame_usbpdsink_request_param1.setFrameShape(QFrame.StyledPanel)
        self.frame_usbpdsink_request_param1.setFrameShadow(QFrame.Raised)
        self.gridLayout_28 = QGridLayout(self.frame_usbpdsink_request_param1)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.chkbox_manual_control_no_usb_suspend = QCheckBox(self.frame_usbpdsink_request_param1)
        self.chkbox_manual_control_no_usb_suspend.setObjectName(u"chkbox_manual_control_no_usb_suspend")
        sizePolicy15.setHeightForWidth(self.chkbox_manual_control_no_usb_suspend.sizePolicy().hasHeightForWidth())
        self.chkbox_manual_control_no_usb_suspend.setSizePolicy(sizePolicy15)
        self.chkbox_manual_control_no_usb_suspend.setMinimumSize(QSize(0, 0))
        self.chkbox_manual_control_no_usb_suspend.setFont(font10)
        self.chkbox_manual_control_no_usb_suspend.setStyleSheet(u"QCheckBox:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_28.addWidget(self.chkbox_manual_control_no_usb_suspend, 7, 1, 1, 1)

        self.chkbox_manual_control_usb_comm_capable = QCheckBox(self.frame_usbpdsink_request_param1)
        self.chkbox_manual_control_usb_comm_capable.setObjectName(u"chkbox_manual_control_usb_comm_capable")
        sizePolicy15.setHeightForWidth(self.chkbox_manual_control_usb_comm_capable.sizePolicy().hasHeightForWidth())
        self.chkbox_manual_control_usb_comm_capable.setSizePolicy(sizePolicy15)
        self.chkbox_manual_control_usb_comm_capable.setMinimumSize(QSize(0, 0))
        self.chkbox_manual_control_usb_comm_capable.setFont(font10)
        self.chkbox_manual_control_usb_comm_capable.setStyleSheet(u"QCheckBox:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_28.addWidget(self.chkbox_manual_control_usb_comm_capable, 6, 1, 1, 1)

        self.chkbox_manual_control_capability_mismatch = QCheckBox(self.frame_usbpdsink_request_param1)
        self.chkbox_manual_control_capability_mismatch.setObjectName(u"chkbox_manual_control_capability_mismatch")
        sizePolicy15.setHeightForWidth(self.chkbox_manual_control_capability_mismatch.sizePolicy().hasHeightForWidth())
        self.chkbox_manual_control_capability_mismatch.setSizePolicy(sizePolicy15)
        self.chkbox_manual_control_capability_mismatch.setMinimumSize(QSize(0, 0))
        self.chkbox_manual_control_capability_mismatch.setFont(font10)
        self.chkbox_manual_control_capability_mismatch.setStyleSheet(u"QCheckBox:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_28.addWidget(self.chkbox_manual_control_capability_mismatch, 6, 0, 1, 1)

        self.chkbox_manual_control_enable_giveback = QCheckBox(self.frame_usbpdsink_request_param1)
        self.chkbox_manual_control_enable_giveback.setObjectName(u"chkbox_manual_control_enable_giveback")
        sizePolicy15.setHeightForWidth(self.chkbox_manual_control_enable_giveback.sizePolicy().hasHeightForWidth())
        self.chkbox_manual_control_enable_giveback.setSizePolicy(sizePolicy15)
        self.chkbox_manual_control_enable_giveback.setMinimumSize(QSize(0, 0))
        self.chkbox_manual_control_enable_giveback.setFont(font10)
        self.chkbox_manual_control_enable_giveback.setStyleSheet(u"QCheckBox:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_28.addWidget(self.chkbox_manual_control_enable_giveback, 7, 0, 1, 1)

        self.lineedit_manual_usbpd_request_param1 = QLineEdit(self.frame_usbpdsink_request_param1)
        self.lineedit_manual_usbpd_request_param1.setObjectName(u"lineedit_manual_usbpd_request_param1")
        self.lineedit_manual_usbpd_request_param1.setMinimumSize(QSize(0, 30))
        self.lineedit_manual_usbpd_request_param1.setFont(font10)
        self.lineedit_manual_usbpd_request_param1.setStyleSheet(u"QLineEdit {\n"
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

        self.gridLayout_28.addWidget(self.lineedit_manual_usbpd_request_param1, 2, 1, 1, 1)

        self.lineedit_manual_usbpd_request_param2 = QLineEdit(self.frame_usbpdsink_request_param1)
        self.lineedit_manual_usbpd_request_param2.setObjectName(u"lineedit_manual_usbpd_request_param2")
        self.lineedit_manual_usbpd_request_param2.setMinimumSize(QSize(0, 30))
        self.lineedit_manual_usbpd_request_param2.setFont(font10)
        self.lineedit_manual_usbpd_request_param2.setStyleSheet(u"QLineEdit {\n"
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

        self.gridLayout_28.addWidget(self.lineedit_manual_usbpd_request_param2, 5, 1, 1, 1)

        self.label_usbpdsink_request_param2 = QLabel(self.frame_usbpdsink_request_param1)
        self.label_usbpdsink_request_param2.setObjectName(u"label_usbpdsink_request_param2")
        self.label_usbpdsink_request_param2.setMinimumSize(QSize(0, 30))
        self.label_usbpdsink_request_param2.setMaximumSize(QSize(16777215, 30))
        self.label_usbpdsink_request_param2.setFont(font10)
        self.label_usbpdsink_request_param2.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}\n"
"\n"
"QLabel{\n"
"border:none\n"
"}")

        self.gridLayout_28.addWidget(self.label_usbpdsink_request_param2, 5, 0, 1, 1)

        self.label_usbpdsink_request_param1 = QLabel(self.frame_usbpdsink_request_param1)
        self.label_usbpdsink_request_param1.setObjectName(u"label_usbpdsink_request_param1")
        self.label_usbpdsink_request_param1.setMaximumSize(QSize(16777215, 30))
        self.label_usbpdsink_request_param1.setFont(font10)
        self.label_usbpdsink_request_param1.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}\n"
"\n"
"QLabel{\n"
"border:none\n"
"}")

        self.gridLayout_28.addWidget(self.label_usbpdsink_request_param1, 2, 0, 1, 1)


        self.horizontalLayout_16.addWidget(self.frame_usbpdsink_request_param1)

        self.frame_usbpdsink_request_buttons = QFrame(self.frame_usbpdsink_request_param)
        self.frame_usbpdsink_request_buttons.setObjectName(u"frame_usbpdsink_request_buttons")
        self.frame_usbpdsink_request_buttons.setFrameShape(QFrame.StyledPanel)
        self.frame_usbpdsink_request_buttons.setFrameShadow(QFrame.Raised)
        self.verticalLayout_35 = QVBoxLayout(self.frame_usbpdsink_request_buttons)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.btn_usbpdsink_request = QPushButton(self.frame_usbpdsink_request_buttons)
        self.btn_usbpdsink_request.setObjectName(u"btn_usbpdsink_request")
        self.btn_usbpdsink_request.setFont(font10)
        self.btn_usbpdsink_request.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_35.addWidget(self.btn_usbpdsink_request)

        self.btn_usbpdsink_epr_entry = QPushButton(self.frame_usbpdsink_request_buttons)
        self.btn_usbpdsink_epr_entry.setObjectName(u"btn_usbpdsink_epr_entry")
        self.btn_usbpdsink_epr_entry.setFont(font10)
        self.btn_usbpdsink_epr_entry.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_35.addWidget(self.btn_usbpdsink_epr_entry)

        self.btn_usbpdsink_epr_exit = QPushButton(self.frame_usbpdsink_request_buttons)
        self.btn_usbpdsink_epr_exit.setObjectName(u"btn_usbpdsink_epr_exit")
        self.btn_usbpdsink_epr_exit.setFont(font10)
        self.btn_usbpdsink_epr_exit.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_35.addWidget(self.btn_usbpdsink_epr_exit)


        self.horizontalLayout_16.addWidget(self.frame_usbpdsink_request_buttons)


        self.gridLayout_30.addWidget(self.frame_usbpdsink_request_param, 2, 0, 1, 3)


        self.verticalLayout_22.addWidget(self.frame_usb_pd_sink_contents)


        self.horizontalLayout_13.addWidget(self.frame_manual_control_usb_pd_sink)


        self.verticalLayout_12.addWidget(self.frame_manual_control_lower)

        self.stackedWidget.addWidget(self.page_manual_control)
        self.page_add_tests = QWidget()
        self.page_add_tests.setObjectName(u"page_add_tests")
        self.page_add_tests.setEnabled(True)
        self.horizontalLayout_33 = QHBoxLayout(self.page_add_tests)
        self.horizontalLayout_33.setSpacing(0)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setContentsMargins(0, 0, 0, 0)
        self.frame_add_tests = QFrame(self.page_add_tests)
        self.frame_add_tests.setObjectName(u"frame_add_tests")
        self.frame_add_tests.setEnabled(True)
        self.frame_add_tests.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests.setFrameShadow(QFrame.Raised)
        self.verticalLayout_89 = QVBoxLayout(self.frame_add_tests)
        self.verticalLayout_89.setSpacing(10)
        self.verticalLayout_89.setObjectName(u"verticalLayout_89")
        self.verticalLayout_89.setContentsMargins(0, 0, 0, 0)
        self.frame_add_tests_directory = QFrame(self.frame_add_tests)
        self.frame_add_tests_directory.setObjectName(u"frame_add_tests_directory")
        sizePolicy18.setHeightForWidth(self.frame_add_tests_directory.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_directory.setSizePolicy(sizePolicy18)
        self.frame_add_tests_directory.setMinimumSize(QSize(0, 58))
        self.frame_add_tests_directory.setMaximumSize(QSize(16777215, 30))
        self.frame_add_tests_directory.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(39, 44, 54);\n"
"	border-radius: 5px;\n"
"};")
        self.frame_add_tests_directory.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_directory.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_add_tests_directory)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(6, 4, 6, 4)
        self.chkbox_add_tests_results_folder = QCheckBox(self.frame_add_tests_directory)
        self.chkbox_add_tests_results_folder.setObjectName(u"chkbox_add_tests_results_folder")
        sizePolicy23 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy23.setHorizontalStretch(15)
        sizePolicy23.setVerticalStretch(0)
        sizePolicy23.setHeightForWidth(self.chkbox_add_tests_results_folder.sizePolicy().hasHeightForWidth())
        self.chkbox_add_tests_results_folder.setSizePolicy(sizePolicy23)
        self.chkbox_add_tests_results_folder.setMaximumSize(QSize(200, 16777215))
        self.chkbox_add_tests_results_folder.setFont(font10)
        self.chkbox_add_tests_results_folder.setAutoFillBackground(False)
        self.chkbox_add_tests_results_folder.setStyleSheet(u"")

        self.horizontalLayout_22.addWidget(self.chkbox_add_tests_results_folder)

        self.frame_add_tests_output_folder_location = QFrame(self.frame_add_tests_directory)
        self.frame_add_tests_output_folder_location.setObjectName(u"frame_add_tests_output_folder_location")
        sizePolicy24 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy24.setHorizontalStretch(6)
        sizePolicy24.setVerticalStretch(0)
        sizePolicy24.setHeightForWidth(self.frame_add_tests_output_folder_location.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_output_folder_location.setSizePolicy(sizePolicy24)
        self.frame_add_tests_output_folder_location.setStyleSheet(u"")
        self.frame_add_tests_output_folder_location.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_output_folder_location.setFrameShadow(QFrame.Raised)
        self.verticalLayout_39 = QVBoxLayout(self.frame_add_tests_output_folder_location)
        self.verticalLayout_39.setSpacing(0)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.verticalLayout_39.setContentsMargins(0, 0, 0, 0)
        self.label_add_tests_output_folder_location = QLabel(self.frame_add_tests_output_folder_location)
        self.label_add_tests_output_folder_location.setObjectName(u"label_add_tests_output_folder_location")
        sizePolicy25 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy25.setHorizontalStretch(0)
        sizePolicy25.setVerticalStretch(0)
        sizePolicy25.setHeightForWidth(self.label_add_tests_output_folder_location.sizePolicy().hasHeightForWidth())
        self.label_add_tests_output_folder_location.setSizePolicy(sizePolicy25)
        font16 = QFont()
        font16.setPointSize(8)
        self.label_add_tests_output_folder_location.setFont(font16)

        self.verticalLayout_39.addWidget(self.label_add_tests_output_folder_location)

        self.lineedit_add_tests_output_folder_location = QLineEdit(self.frame_add_tests_output_folder_location)
        self.lineedit_add_tests_output_folder_location.setObjectName(u"lineedit_add_tests_output_folder_location")
        sizePolicy26 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy26.setHorizontalStretch(6)
        sizePolicy26.setVerticalStretch(0)
        sizePolicy26.setHeightForWidth(self.lineedit_add_tests_output_folder_location.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_output_folder_location.setSizePolicy(sizePolicy26)
        self.lineedit_add_tests_output_folder_location.setMinimumSize(QSize(100, 33))
        self.lineedit_add_tests_output_folder_location.setFont(font10)
        self.lineedit_add_tests_output_folder_location.setStyleSheet(u"QLineEdit {\n"
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
"}")

        self.verticalLayout_39.addWidget(self.lineedit_add_tests_output_folder_location)


        self.horizontalLayout_22.addWidget(self.frame_add_tests_output_folder_location)

        self.frame_add_tests_results_folder = QFrame(self.frame_add_tests_directory)
        self.frame_add_tests_results_folder.setObjectName(u"frame_add_tests_results_folder")
        sizePolicy22.setHeightForWidth(self.frame_add_tests_results_folder.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_results_folder.setSizePolicy(sizePolicy22)
        self.frame_add_tests_results_folder.setStyleSheet(u"")
        self.frame_add_tests_results_folder.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_results_folder.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_add_tests_results_folder)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_add_tests_results_folder = QLabel(self.frame_add_tests_results_folder)
        self.label_add_tests_results_folder.setObjectName(u"label_add_tests_results_folder")
        sizePolicy25.setHeightForWidth(self.label_add_tests_results_folder.sizePolicy().hasHeightForWidth())
        self.label_add_tests_results_folder.setSizePolicy(sizePolicy25)
        self.label_add_tests_results_folder.setFont(font16)

        self.verticalLayout_13.addWidget(self.label_add_tests_results_folder)

        self.cbx_add_tests_results_folder = QComboBox(self.frame_add_tests_results_folder)
        self.cbx_add_tests_results_folder.setObjectName(u"cbx_add_tests_results_folder")
        sizePolicy27 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy27.setHorizontalStretch(3)
        sizePolicy27.setVerticalStretch(0)
        sizePolicy27.setHeightForWidth(self.cbx_add_tests_results_folder.sizePolicy().hasHeightForWidth())
        self.cbx_add_tests_results_folder.setSizePolicy(sizePolicy27)
        self.cbx_add_tests_results_folder.setMinimumSize(QSize(0, 33))
        self.cbx_add_tests_results_folder.setMaximumSize(QSize(16777215, 30))
        self.cbx_add_tests_results_folder.setFont(font10)
        self.cbx_add_tests_results_folder.setStyleSheet(u"QComboBox:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}")

        self.verticalLayout_13.addWidget(self.cbx_add_tests_results_folder)


        self.horizontalLayout_22.addWidget(self.frame_add_tests_results_folder)

        self.frame_4 = QFrame(self.frame_add_tests_directory)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(150, 0))
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_44 = QVBoxLayout(self.frame_4)
        self.verticalLayout_44.setSpacing(0)
        self.verticalLayout_44.setObjectName(u"verticalLayout_44")
        self.verticalLayout_44.setContentsMargins(0, 0, 0, 0)
        self.label_add_tests_output_folder_spacer = QLabel(self.frame_4)
        self.label_add_tests_output_folder_spacer.setObjectName(u"label_add_tests_output_folder_spacer")
        sizePolicy25.setHeightForWidth(self.label_add_tests_output_folder_spacer.sizePolicy().hasHeightForWidth())
        self.label_add_tests_output_folder_spacer.setSizePolicy(sizePolicy25)
        self.label_add_tests_output_folder_spacer.setFont(font16)

        self.verticalLayout_44.addWidget(self.label_add_tests_output_folder_spacer)

        self.btn_add_tests_output_folder_location = QPushButton(self.frame_4)
        self.btn_add_tests_output_folder_location.setObjectName(u"btn_add_tests_output_folder_location")
        sizePolicy28 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy28.setHorizontalStretch(0)
        sizePolicy28.setVerticalStretch(0)
        sizePolicy28.setHeightForWidth(self.btn_add_tests_output_folder_location.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_output_folder_location.setSizePolicy(sizePolicy28)
        self.btn_add_tests_output_folder_location.setMinimumSize(QSize(150, 33))
        self.btn_add_tests_output_folder_location.setFont(font13)
        self.btn_add_tests_output_folder_location.setStyleSheet(u"QPushButton {\n"
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
        icon11 = QIcon()
        icon11.addFile(u":/16x16/icons/16x16/cil-folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_output_folder_location.setIcon(icon11)

        self.verticalLayout_44.addWidget(self.btn_add_tests_output_folder_location)


        self.horizontalLayout_22.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame_add_tests_directory)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(20, 0))
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_87 = QVBoxLayout(self.frame_5)
        self.verticalLayout_87.setSpacing(0)
        self.verticalLayout_87.setObjectName(u"verticalLayout_87")
        self.verticalLayout_87.setContentsMargins(0, 0, 0, 0)
        self.label_add_tests_output_folder_spacer_2 = QLabel(self.frame_5)
        self.label_add_tests_output_folder_spacer_2.setObjectName(u"label_add_tests_output_folder_spacer_2")
        sizePolicy25.setHeightForWidth(self.label_add_tests_output_folder_spacer_2.sizePolicy().hasHeightForWidth())
        self.label_add_tests_output_folder_spacer_2.setSizePolicy(sizePolicy25)
        self.label_add_tests_output_folder_spacer_2.setFont(font16)

        self.verticalLayout_87.addWidget(self.label_add_tests_output_folder_spacer_2)

        self.btn_add_tests_open_output_folder = QPushButton(self.frame_5)
        self.btn_add_tests_open_output_folder.setObjectName(u"btn_add_tests_open_output_folder")
        sizePolicy19.setHeightForWidth(self.btn_add_tests_open_output_folder.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_open_output_folder.setSizePolicy(sizePolicy19)
        self.btn_add_tests_open_output_folder.setMinimumSize(QSize(20, 33))
        self.btn_add_tests_open_output_folder.setFont(font13)
        self.btn_add_tests_open_output_folder.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_open_output_folder.setIcon(icon11)

        self.verticalLayout_87.addWidget(self.btn_add_tests_open_output_folder)


        self.horizontalLayout_22.addWidget(self.frame_5)


        self.verticalLayout_89.addWidget(self.frame_add_tests_directory)

        self.frame_add_tests_maincontent = QFrame(self.frame_add_tests)
        self.frame_add_tests_maincontent.setObjectName(u"frame_add_tests_maincontent")
        self.frame_add_tests_maincontent.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_maincontent.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_60 = QHBoxLayout(self.frame_add_tests_maincontent)
        self.horizontalLayout_60.setSpacing(6)
        self.horizontalLayout_60.setObjectName(u"horizontalLayout_60")
        self.horizontalLayout_60.setContentsMargins(0, 0, 0, 0)
        self.frame_add_tests_left = QFrame(self.frame_add_tests_maincontent)
        self.frame_add_tests_left.setObjectName(u"frame_add_tests_left")
        sizePolicy29 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy29.setHorizontalStretch(1)
        sizePolicy29.setVerticalStretch(0)
        sizePolicy29.setHeightForWidth(self.frame_add_tests_left.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_left.setSizePolicy(sizePolicy29)
        self.frame_add_tests_left.setMaximumSize(QSize(600, 16777215))
        self.frame_add_tests_left.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_left.setFrameShadow(QFrame.Raised)
        self.verticalLayout_47 = QVBoxLayout(self.frame_add_tests_left)
        self.verticalLayout_47.setSpacing(6)
        self.verticalLayout_47.setObjectName(u"verticalLayout_47")
        self.verticalLayout_47.setContentsMargins(0, 6, 0, 0)
        self.frame_add_tests_testtype = QFrame(self.frame_add_tests_left)
        self.frame_add_tests_testtype.setObjectName(u"frame_add_tests_testtype")
        sizePolicy30 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy30.setHorizontalStretch(0)
        sizePolicy30.setVerticalStretch(1)
        sizePolicy30.setHeightForWidth(self.frame_add_tests_testtype.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_testtype.setSizePolicy(sizePolicy30)
        self.frame_add_tests_testtype.setMinimumSize(QSize(0, 55))
        self.frame_add_tests_testtype.setMaximumSize(QSize(16777215, 55))
        self.frame_add_tests_testtype.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(39, 44, 54);\n"
"	border-radius: 5px;\n"
"};")
        self.frame_add_tests_testtype.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_testtype.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_31 = QHBoxLayout(self.frame_add_tests_testtype)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.label_add_tests_testtype = QLabel(self.frame_add_tests_testtype)
        self.label_add_tests_testtype.setObjectName(u"label_add_tests_testtype")
        sizePolicy31 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy31.setHorizontalStretch(1)
        sizePolicy31.setVerticalStretch(0)
        sizePolicy31.setHeightForWidth(self.label_add_tests_testtype.sizePolicy().hasHeightForWidth())
        self.label_add_tests_testtype.setSizePolicy(sizePolicy31)
        self.label_add_tests_testtype.setMaximumSize(QSize(16777215, 40))
        self.label_add_tests_testtype.setFont(font10)
        self.label_add_tests_testtype.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_31.addWidget(self.label_add_tests_testtype)

        self.cbx_add_tests_testtype = QComboBox(self.frame_add_tests_testtype)
        self.cbx_add_tests_testtype.setObjectName(u"cbx_add_tests_testtype")
        sizePolicy31.setHeightForWidth(self.cbx_add_tests_testtype.sizePolicy().hasHeightForWidth())
        self.cbx_add_tests_testtype.setSizePolicy(sizePolicy31)
        self.cbx_add_tests_testtype.setMinimumSize(QSize(0, 40))
        self.cbx_add_tests_testtype.setMaximumSize(QSize(16777215, 40))
        self.cbx_add_tests_testtype.setFont(font10)
        self.cbx_add_tests_testtype.setStyleSheet(u"QComboBox:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}")

        self.horizontalLayout_31.addWidget(self.cbx_add_tests_testtype)


        self.verticalLayout_47.addWidget(self.frame_add_tests_testtype)

        self.frame_add_tests_testparams = QFrame(self.frame_add_tests_left)
        self.frame_add_tests_testparams.setObjectName(u"frame_add_tests_testparams")
        self.frame_add_tests_testparams.setEnabled(True)
        self.frame_add_tests_testparams.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_testparams.setFrameShadow(QFrame.Raised)
        self.verticalLayout_48 = QVBoxLayout(self.frame_add_tests_testparams)
        self.verticalLayout_48.setSpacing(6)
        self.verticalLayout_48.setObjectName(u"verticalLayout_48")
        self.verticalLayout_48.setContentsMargins(0, 0, 0, 0)
        self.stackedwidget_add_tests_params_top = QStackedWidget(self.frame_add_tests_testparams)
        self.stackedwidget_add_tests_params_top.setObjectName(u"stackedwidget_add_tests_params_top")
        sizePolicy16.setHeightForWidth(self.stackedwidget_add_tests_params_top.sizePolicy().hasHeightForWidth())
        self.stackedwidget_add_tests_params_top.setSizePolicy(sizePolicy16)
        self.page_add_tests_sp1_empty = QWidget()
        self.page_add_tests_sp1_empty.setObjectName(u"page_add_tests_sp1_empty")
        self.stackedwidget_add_tests_params_top.addWidget(self.page_add_tests_sp1_empty)
        self.page_add_tests_sp1_line_range = QWidget()
        self.page_add_tests_sp1_line_range.setObjectName(u"page_add_tests_sp1_line_range")
        self.gridLayout_7 = QGridLayout(self.page_add_tests_sp1_line_range)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_add_tests_line_range = QFrame(self.page_add_tests_sp1_line_range)
        self.frame_add_tests_line_range.setObjectName(u"frame_add_tests_line_range")
        sizePolicy12.setHeightForWidth(self.frame_add_tests_line_range.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_line_range.setSizePolicy(sizePolicy12)
        self.frame_add_tests_line_range.setMinimumSize(QSize(500, 300))
        self.frame_add_tests_line_range.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(39, 44, 54);\n"
"	border-radius: 5px;\n"
"};")
        self.frame_add_tests_line_range.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_line_range.setFrameShadow(QFrame.Raised)
        self.verticalLayout_43 = QVBoxLayout(self.frame_add_tests_line_range)
        self.verticalLayout_43.setSpacing(0)
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.verticalLayout_43.setContentsMargins(0, 0, 0, 0)
        self.frame_add_tests_line_range_top = QFrame(self.frame_add_tests_line_range)
        self.frame_add_tests_line_range_top.setObjectName(u"frame_add_tests_line_range_top")
        sizePolicy25.setHeightForWidth(self.frame_add_tests_line_range_top.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_line_range_top.setSizePolicy(sizePolicy25)
        self.frame_add_tests_line_range_top.setMaximumSize(QSize(16777215, 16777215))
        self.frame_add_tests_line_range_top.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_line_range_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_add_tests_line_range_top)
        self.horizontalLayout_25.setSpacing(6)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(6, 6, 6, 6)
        self.label_add_tests_line_range = QLabel(self.frame_add_tests_line_range_top)
        self.label_add_tests_line_range.setObjectName(u"label_add_tests_line_range")
        sizePolicy32 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy32.setHorizontalStretch(5)
        sizePolicy32.setVerticalStretch(0)
        sizePolicy32.setHeightForWidth(self.label_add_tests_line_range.sizePolicy().hasHeightForWidth())
        self.label_add_tests_line_range.setSizePolicy(sizePolicy32)
        self.label_add_tests_line_range.setMaximumSize(QSize(16777215, 50))
        self.label_add_tests_line_range.setFont(font10)
        self.label_add_tests_line_range.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_25.addWidget(self.label_add_tests_line_range)

        self.cbx_add_tests_line_range_type = QComboBox(self.frame_add_tests_line_range_top)
        self.cbx_add_tests_line_range_type.setObjectName(u"cbx_add_tests_line_range_type")
        sizePolicy32.setHeightForWidth(self.cbx_add_tests_line_range_type.sizePolicy().hasHeightForWidth())
        self.cbx_add_tests_line_range_type.setSizePolicy(sizePolicy32)
        self.cbx_add_tests_line_range_type.setMinimumSize(QSize(0, 40))
        self.cbx_add_tests_line_range_type.setMaximumSize(QSize(16777215, 40))
        self.cbx_add_tests_line_range_type.setFont(font10)
        self.cbx_add_tests_line_range_type.setStyleSheet(u"QComboBox:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}")

        self.horizontalLayout_25.addWidget(self.cbx_add_tests_line_range_type)

        self.btn_add_tests_line_range_add_setting = QPushButton(self.frame_add_tests_line_range_top)
        self.btn_add_tests_line_range_add_setting.setObjectName(u"btn_add_tests_line_range_add_setting")
        sizePolicy15.setHeightForWidth(self.btn_add_tests_line_range_add_setting.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_line_range_add_setting.setSizePolicy(sizePolicy15)
        self.btn_add_tests_line_range_add_setting.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_line_range_add_setting.setFont(font13)
        self.btn_add_tests_line_range_add_setting.setStyleSheet(u"QPushButton {\n"
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
        icon12 = QIcon()
        icon12.addFile(u":/20x20/icons/20x20/cil-plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_line_range_add_setting.setIcon(icon12)

        self.horizontalLayout_25.addWidget(self.btn_add_tests_line_range_add_setting)

        self.btn_add_tests_line_range_duplicate_setting = QPushButton(self.frame_add_tests_line_range_top)
        self.btn_add_tests_line_range_duplicate_setting.setObjectName(u"btn_add_tests_line_range_duplicate_setting")
        sizePolicy15.setHeightForWidth(self.btn_add_tests_line_range_duplicate_setting.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_line_range_duplicate_setting.setSizePolicy(sizePolicy15)
        self.btn_add_tests_line_range_duplicate_setting.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_line_range_duplicate_setting.setFont(font13)
        self.btn_add_tests_line_range_duplicate_setting.setStyleSheet(u"QPushButton {\n"
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
        icon13 = QIcon()
        icon13.addFile(u":/20x20/icons/20x20/cil-copy.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_line_range_duplicate_setting.setIcon(icon13)

        self.horizontalLayout_25.addWidget(self.btn_add_tests_line_range_duplicate_setting)

        self.btn_add_tests_line_range_remove_setting = QPushButton(self.frame_add_tests_line_range_top)
        self.btn_add_tests_line_range_remove_setting.setObjectName(u"btn_add_tests_line_range_remove_setting")
        sizePolicy15.setHeightForWidth(self.btn_add_tests_line_range_remove_setting.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_line_range_remove_setting.setSizePolicy(sizePolicy15)
        self.btn_add_tests_line_range_remove_setting.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_line_range_remove_setting.setFont(font13)
        self.btn_add_tests_line_range_remove_setting.setStyleSheet(u"QPushButton {\n"
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
        icon14 = QIcon()
        icon14.addFile(u":/20x20/icons/20x20/cil-minus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_line_range_remove_setting.setIcon(icon14)

        self.horizontalLayout_25.addWidget(self.btn_add_tests_line_range_remove_setting)


        self.verticalLayout_43.addWidget(self.frame_add_tests_line_range_top)

        self.table_add_tests_line_range = QTableWidget(self.frame_add_tests_line_range)
        if (self.table_add_tests_line_range.columnCount() < 2):
            self.table_add_tests_line_range.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_add_tests_line_range.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_add_tests_line_range.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.table_add_tests_line_range.rowCount() < 3):
            self.table_add_tests_line_range.setRowCount(3)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_add_tests_line_range.setItem(0, 0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_add_tests_line_range.setItem(0, 1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_add_tests_line_range.setItem(1, 0, __qtablewidgetitem4)
        self.table_add_tests_line_range.setObjectName(u"table_add_tests_line_range")
        self.table_add_tests_line_range.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.table_add_tests_line_range.sizePolicy().hasHeightForWidth())
        self.table_add_tests_line_range.setSizePolicy(sizePolicy1)
        self.table_add_tests_line_range.setMaximumSize(QSize(16777215, 16777215))
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush6)
        brush15 = QBrush(QColor(39, 44, 54, 255))
        brush15.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush15)
        palette1.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush6)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush15)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush15)
        brush16 = QBrush(QColor(210, 210, 210, 128))
        brush16.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Active, QPalette.PlaceholderText, brush16)
#endif
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush15)
        palette1.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush15)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush15)
        brush17 = QBrush(QColor(210, 210, 210, 128))
        brush17.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush17)
#endif
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush15)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush15)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush15)
        brush18 = QBrush(QColor(210, 210, 210, 128))
        brush18.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush18)
#endif
        self.table_add_tests_line_range.setPalette(palette1)
        self.table_add_tests_line_range.setFont(font10)
        self.table_add_tests_line_range.setStyleSheet(u"QTableWidget {	\n"
"	background-color: rgb(39, 44, 54);\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
"\n"
"QHeaderView::section{\n"
"	background-color: rgb(39, 44, 54);\n"
"\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWid"
                        "get::horizontalHeader {	\n"
"	background-color: rgb(81, 255, 0);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"")
        self.table_add_tests_line_range.setFrameShape(QFrame.NoFrame)
        self.table_add_tests_line_range.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table_add_tests_line_range.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_add_tests_line_range.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_add_tests_line_range.setAlternatingRowColors(False)
        self.table_add_tests_line_range.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_add_tests_line_range.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_add_tests_line_range.setShowGrid(True)
        self.table_add_tests_line_range.setGridStyle(Qt.SolidLine)
        self.table_add_tests_line_range.setSortingEnabled(False)
        self.table_add_tests_line_range.setCornerButtonEnabled(True)
        self.table_add_tests_line_range.setRowCount(3)
        self.table_add_tests_line_range.horizontalHeader().setVisible(False)
        self.table_add_tests_line_range.horizontalHeader().setCascadingSectionResizes(True)
        self.table_add_tests_line_range.horizontalHeader().setDefaultSectionSize(200)
        self.table_add_tests_line_range.horizontalHeader().setStretchLastSection(False)
        self.table_add_tests_line_range.verticalHeader().setVisible(False)
        self.table_add_tests_line_range.verticalHeader().setCascadingSectionResizes(True)
        self.table_add_tests_line_range.verticalHeader().setMinimumSectionSize(30)
        self.table_add_tests_line_range.verticalHeader().setDefaultSectionSize(30)
        self.table_add_tests_line_range.verticalHeader().setHighlightSections(True)
        self.table_add_tests_line_range.verticalHeader().setProperty("showSortIndicator", True)
        self.table_add_tests_line_range.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_43.addWidget(self.table_add_tests_line_range)

        self.frame_add_tests_line_range_params = QFrame(self.frame_add_tests_line_range)
        self.frame_add_tests_line_range_params.setObjectName(u"frame_add_tests_line_range_params")
        sizePolicy33 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy33.setHorizontalStretch(0)
        sizePolicy33.setVerticalStretch(0)
        sizePolicy33.setHeightForWidth(self.frame_add_tests_line_range_params.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_line_range_params.setSizePolicy(sizePolicy33)
        self.frame_add_tests_line_range_params.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_line_range_params.setFrameShadow(QFrame.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_add_tests_line_range_params)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(9, 0, 0, 0)
        self.frame_add_tests_line_range_buttons = QFrame(self.frame_add_tests_line_range_params)
        self.frame_add_tests_line_range_buttons.setObjectName(u"frame_add_tests_line_range_buttons")
        sizePolicy34 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy34.setHorizontalStretch(1)
        sizePolicy34.setVerticalStretch(0)
        sizePolicy34.setHeightForWidth(self.frame_add_tests_line_range_buttons.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_line_range_buttons.setSizePolicy(sizePolicy34)
        self.frame_add_tests_line_range_buttons.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_line_range_buttons.setFrameShadow(QFrame.Raised)
        self.verticalLayout_40 = QVBoxLayout(self.frame_add_tests_line_range_buttons)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.verticalLayout_40.setContentsMargins(3, -1, -1, -1)
        self.btn_add_tests_line_range_add = QPushButton(self.frame_add_tests_line_range_buttons)
        self.btn_add_tests_line_range_add.setObjectName(u"btn_add_tests_line_range_add")
        self.btn_add_tests_line_range_add.setMinimumSize(QSize(150, 30))
        self.btn_add_tests_line_range_add.setFont(font13)
        self.btn_add_tests_line_range_add.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_line_range_add.setIcon(icon12)

        self.verticalLayout_40.addWidget(self.btn_add_tests_line_range_add)

        self.btn_add_tests_line_range_remove = QPushButton(self.frame_add_tests_line_range_buttons)
        self.btn_add_tests_line_range_remove.setObjectName(u"btn_add_tests_line_range_remove")
        self.btn_add_tests_line_range_remove.setMinimumSize(QSize(150, 30))
        self.btn_add_tests_line_range_remove.setFont(font13)
        self.btn_add_tests_line_range_remove.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_line_range_remove.setIcon(icon14)

        self.verticalLayout_40.addWidget(self.btn_add_tests_line_range_remove)

        self.btn_add_tests_line_range_clear = QPushButton(self.frame_add_tests_line_range_buttons)
        self.btn_add_tests_line_range_clear.setObjectName(u"btn_add_tests_line_range_clear")
        self.btn_add_tests_line_range_clear.setMinimumSize(QSize(150, 30))
        self.btn_add_tests_line_range_clear.setFont(font13)
        self.btn_add_tests_line_range_clear.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_line_range_clear.setIcon(icon2)

        self.verticalLayout_40.addWidget(self.btn_add_tests_line_range_clear)


        self.gridLayout_16.addWidget(self.frame_add_tests_line_range_buttons, 0, 2, 2, 1)

        self.lineedit_add_tests_line_range_voltage_2 = QLineEdit(self.frame_add_tests_line_range_params)
        self.lineedit_add_tests_line_range_voltage_2.setObjectName(u"lineedit_add_tests_line_range_voltage_2")
        sizePolicy15.setHeightForWidth(self.lineedit_add_tests_line_range_voltage_2.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_line_range_voltage_2.setSizePolicy(sizePolicy15)
        self.lineedit_add_tests_line_range_voltage_2.setMinimumSize(QSize(0, 30))
        self.lineedit_add_tests_line_range_voltage_2.setFont(font10)
        self.lineedit_add_tests_line_range_voltage_2.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_16.addWidget(self.lineedit_add_tests_line_range_voltage_2, 1, 0, 1, 1)

        self.frame_add_tests_line_range_coupling = QFrame(self.frame_add_tests_line_range_params)
        self.frame_add_tests_line_range_coupling.setObjectName(u"frame_add_tests_line_range_coupling")
        sizePolicy5.setHeightForWidth(self.frame_add_tests_line_range_coupling.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_line_range_coupling.setSizePolicy(sizePolicy5)
        self.frame_add_tests_line_range_coupling.setMinimumSize(QSize(0, 0))
        self.frame_add_tests_line_range_coupling.setMaximumSize(QSize(16777215, 16777215))
        self.frame_add_tests_line_range_coupling.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_line_range_coupling.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_91 = QHBoxLayout(self.frame_add_tests_line_range_coupling)
        self.horizontalLayout_91.setObjectName(u"horizontalLayout_91")
        self.widget_toggle_add_tests_line_range_coupling = QCheckBox(self.frame_add_tests_line_range_coupling)
        self.widget_toggle_add_tests_line_range_coupling.setObjectName(u"widget_toggle_add_tests_line_range_coupling")
        self.widget_toggle_add_tests_line_range_coupling.setFont(font10)

        self.horizontalLayout_91.addWidget(self.widget_toggle_add_tests_line_range_coupling)


        self.gridLayout_16.addWidget(self.frame_add_tests_line_range_coupling, 1, 1, 1, 1)

        self.lineedit_add_tests_line_range_voltage = QLineEdit(self.frame_add_tests_line_range_params)
        self.lineedit_add_tests_line_range_voltage.setObjectName(u"lineedit_add_tests_line_range_voltage")
        sizePolicy15.setHeightForWidth(self.lineedit_add_tests_line_range_voltage.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_line_range_voltage.setSizePolicy(sizePolicy15)
        self.lineedit_add_tests_line_range_voltage.setMinimumSize(QSize(0, 30))
        self.lineedit_add_tests_line_range_voltage.setFont(font10)
        self.lineedit_add_tests_line_range_voltage.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_16.addWidget(self.lineedit_add_tests_line_range_voltage, 0, 0, 1, 1)

        self.lineedit_add_tests_line_range_frequency = QLineEdit(self.frame_add_tests_line_range_params)
        self.lineedit_add_tests_line_range_frequency.setObjectName(u"lineedit_add_tests_line_range_frequency")
        sizePolicy15.setHeightForWidth(self.lineedit_add_tests_line_range_frequency.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_line_range_frequency.setSizePolicy(sizePolicy15)
        self.lineedit_add_tests_line_range_frequency.setMinimumSize(QSize(0, 30))
        self.lineedit_add_tests_line_range_frequency.setFont(font10)
        self.lineedit_add_tests_line_range_frequency.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_16.addWidget(self.lineedit_add_tests_line_range_frequency, 0, 1, 1, 1)


        self.verticalLayout_43.addWidget(self.frame_add_tests_line_range_params)


        self.gridLayout_7.addWidget(self.frame_add_tests_line_range, 0, 0, 1, 1)

        self.stackedwidget_add_tests_params_top.addWidget(self.page_add_tests_sp1_line_range)
        self.page_add_tests_sp1_line_ramp = QWidget()
        self.page_add_tests_sp1_line_ramp.setObjectName(u"page_add_tests_sp1_line_ramp")
        self.gridLayout_10 = QGridLayout(self.page_add_tests_sp1_line_ramp)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.frame_add_tests_line_ramp = QFrame(self.page_add_tests_sp1_line_ramp)
        self.frame_add_tests_line_ramp.setObjectName(u"frame_add_tests_line_ramp")
        sizePolicy12.setHeightForWidth(self.frame_add_tests_line_ramp.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_line_ramp.setSizePolicy(sizePolicy12)
        self.frame_add_tests_line_ramp.setMinimumSize(QSize(500, 300))
        self.frame_add_tests_line_ramp.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(39, 44, 54);\n"
"	border-radius: 5px;\n"
"};")
        self.frame_add_tests_line_ramp.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_line_ramp.setFrameShadow(QFrame.Raised)
        self.verticalLayout_99 = QVBoxLayout(self.frame_add_tests_line_ramp)
        self.verticalLayout_99.setSpacing(0)
        self.verticalLayout_99.setObjectName(u"verticalLayout_99")
        self.verticalLayout_99.setContentsMargins(0, 0, 0, 0)
        self.frame_add_tests_line_ramp_top = QFrame(self.frame_add_tests_line_ramp)
        self.frame_add_tests_line_ramp_top.setObjectName(u"frame_add_tests_line_ramp_top")
        sizePolicy25.setHeightForWidth(self.frame_add_tests_line_ramp_top.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_line_ramp_top.setSizePolicy(sizePolicy25)
        self.frame_add_tests_line_ramp_top.setMaximumSize(QSize(16777215, 16777215))
        self.frame_add_tests_line_ramp_top.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_line_ramp_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_72 = QHBoxLayout(self.frame_add_tests_line_ramp_top)
        self.horizontalLayout_72.setSpacing(6)
        self.horizontalLayout_72.setObjectName(u"horizontalLayout_72")
        self.horizontalLayout_72.setContentsMargins(6, 6, 6, 6)
        self.label_add_tests_line_ramp = QLabel(self.frame_add_tests_line_ramp_top)
        self.label_add_tests_line_ramp.setObjectName(u"label_add_tests_line_ramp")
        sizePolicy32.setHeightForWidth(self.label_add_tests_line_ramp.sizePolicy().hasHeightForWidth())
        self.label_add_tests_line_ramp.setSizePolicy(sizePolicy32)
        self.label_add_tests_line_ramp.setMaximumSize(QSize(16777215, 50))
        self.label_add_tests_line_ramp.setFont(font10)
        self.label_add_tests_line_ramp.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_72.addWidget(self.label_add_tests_line_ramp)

        self.cbx_add_tests_line_ramp_type = QComboBox(self.frame_add_tests_line_ramp_top)
        self.cbx_add_tests_line_ramp_type.setObjectName(u"cbx_add_tests_line_ramp_type")
        sizePolicy32.setHeightForWidth(self.cbx_add_tests_line_ramp_type.sizePolicy().hasHeightForWidth())
        self.cbx_add_tests_line_ramp_type.setSizePolicy(sizePolicy32)
        self.cbx_add_tests_line_ramp_type.setMinimumSize(QSize(0, 40))
        self.cbx_add_tests_line_ramp_type.setMaximumSize(QSize(16777215, 40))
        self.cbx_add_tests_line_ramp_type.setFont(font10)
        self.cbx_add_tests_line_ramp_type.setStyleSheet(u"QComboBox:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}")

        self.horizontalLayout_72.addWidget(self.cbx_add_tests_line_ramp_type)

        self.btn_add_tests_line_ramp_add_setting = QPushButton(self.frame_add_tests_line_ramp_top)
        self.btn_add_tests_line_ramp_add_setting.setObjectName(u"btn_add_tests_line_ramp_add_setting")
        sizePolicy15.setHeightForWidth(self.btn_add_tests_line_ramp_add_setting.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_line_ramp_add_setting.setSizePolicy(sizePolicy15)
        self.btn_add_tests_line_ramp_add_setting.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_line_ramp_add_setting.setFont(font13)
        self.btn_add_tests_line_ramp_add_setting.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_line_ramp_add_setting.setIcon(icon12)

        self.horizontalLayout_72.addWidget(self.btn_add_tests_line_ramp_add_setting)

        self.btn_add_tests_line_ramp_duplicate_setting = QPushButton(self.frame_add_tests_line_ramp_top)
        self.btn_add_tests_line_ramp_duplicate_setting.setObjectName(u"btn_add_tests_line_ramp_duplicate_setting")
        sizePolicy15.setHeightForWidth(self.btn_add_tests_line_ramp_duplicate_setting.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_line_ramp_duplicate_setting.setSizePolicy(sizePolicy15)
        self.btn_add_tests_line_ramp_duplicate_setting.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_line_ramp_duplicate_setting.setFont(font13)
        self.btn_add_tests_line_ramp_duplicate_setting.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_line_ramp_duplicate_setting.setIcon(icon13)

        self.horizontalLayout_72.addWidget(self.btn_add_tests_line_ramp_duplicate_setting)

        self.btn_add_tests_line_ramp_remove_setting = QPushButton(self.frame_add_tests_line_ramp_top)
        self.btn_add_tests_line_ramp_remove_setting.setObjectName(u"btn_add_tests_line_ramp_remove_setting")
        sizePolicy15.setHeightForWidth(self.btn_add_tests_line_ramp_remove_setting.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_line_ramp_remove_setting.setSizePolicy(sizePolicy15)
        self.btn_add_tests_line_ramp_remove_setting.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_line_ramp_remove_setting.setFont(font13)
        self.btn_add_tests_line_ramp_remove_setting.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_line_ramp_remove_setting.setIcon(icon14)

        self.horizontalLayout_72.addWidget(self.btn_add_tests_line_ramp_remove_setting)


        self.verticalLayout_99.addWidget(self.frame_add_tests_line_ramp_top)

        self.table_add_tests_line_ramp = QTableWidget(self.frame_add_tests_line_ramp)
        if (self.table_add_tests_line_ramp.columnCount() < 2):
            self.table_add_tests_line_ramp.setColumnCount(2)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_add_tests_line_ramp.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_add_tests_line_ramp.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        if (self.table_add_tests_line_ramp.rowCount() < 3):
            self.table_add_tests_line_ramp.setRowCount(3)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.table_add_tests_line_ramp.setItem(0, 0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setTextAlignment(Qt.AlignCenter);
        self.table_add_tests_line_ramp.setItem(0, 1, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.table_add_tests_line_ramp.setItem(1, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setTextAlignment(Qt.AlignCenter);
        self.table_add_tests_line_ramp.setItem(1, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setTextAlignment(Qt.AlignCenter);
        self.table_add_tests_line_ramp.setItem(2, 1, __qtablewidgetitem11)
        self.table_add_tests_line_ramp.setObjectName(u"table_add_tests_line_ramp")
        self.table_add_tests_line_ramp.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.table_add_tests_line_ramp.sizePolicy().hasHeightForWidth())
        self.table_add_tests_line_ramp.setSizePolicy(sizePolicy1)
        self.table_add_tests_line_ramp.setMaximumSize(QSize(16777215, 16777215))
        palette2 = QPalette()
        palette2.setBrush(QPalette.Active, QPalette.WindowText, brush6)
        palette2.setBrush(QPalette.Active, QPalette.Button, brush15)
        palette2.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette2.setBrush(QPalette.Active, QPalette.ButtonText, brush6)
        palette2.setBrush(QPalette.Active, QPalette.Base, brush15)
        palette2.setBrush(QPalette.Active, QPalette.Window, brush15)
        brush19 = QBrush(QColor(210, 210, 210, 128))
        brush19.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette.Active, QPalette.PlaceholderText, brush19)
#endif
        palette2.setBrush(QPalette.Inactive, QPalette.WindowText, brush6)
        palette2.setBrush(QPalette.Inactive, QPalette.Button, brush15)
        palette2.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette2.setBrush(QPalette.Inactive, QPalette.ButtonText, brush6)
        palette2.setBrush(QPalette.Inactive, QPalette.Base, brush15)
        palette2.setBrush(QPalette.Inactive, QPalette.Window, brush15)
        brush20 = QBrush(QColor(210, 210, 210, 128))
        brush20.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush20)
#endif
        palette2.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette2.setBrush(QPalette.Disabled, QPalette.Button, brush15)
        palette2.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette2.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette2.setBrush(QPalette.Disabled, QPalette.Base, brush15)
        palette2.setBrush(QPalette.Disabled, QPalette.Window, brush15)
        brush21 = QBrush(QColor(210, 210, 210, 128))
        brush21.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush21)
#endif
        self.table_add_tests_line_ramp.setPalette(palette2)
        self.table_add_tests_line_ramp.setFont(font10)
        self.table_add_tests_line_ramp.setStyleSheet(u"QTableWidget {	\n"
"	background-color: rgb(39, 44, 54);\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
"\n"
"QHeaderView::section{\n"
"	background-color: rgb(39, 44, 54);\n"
"\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWid"
                        "get::horizontalHeader {	\n"
"	background-color: rgb(81, 255, 0);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"")
        self.table_add_tests_line_ramp.setFrameShape(QFrame.NoFrame)
        self.table_add_tests_line_ramp.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table_add_tests_line_ramp.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_add_tests_line_ramp.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_add_tests_line_ramp.setAlternatingRowColors(False)
        self.table_add_tests_line_ramp.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_add_tests_line_ramp.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_add_tests_line_ramp.setShowGrid(True)
        self.table_add_tests_line_ramp.setGridStyle(Qt.SolidLine)
        self.table_add_tests_line_ramp.setSortingEnabled(False)
        self.table_add_tests_line_ramp.setCornerButtonEnabled(True)
        self.table_add_tests_line_ramp.setRowCount(3)
        self.table_add_tests_line_ramp.horizontalHeader().setVisible(False)
        self.table_add_tests_line_ramp.horizontalHeader().setCascadingSectionResizes(True)
        self.table_add_tests_line_ramp.horizontalHeader().setDefaultSectionSize(200)
        self.table_add_tests_line_ramp.horizontalHeader().setStretchLastSection(False)
        self.table_add_tests_line_ramp.verticalHeader().setVisible(False)
        self.table_add_tests_line_ramp.verticalHeader().setCascadingSectionResizes(True)
        self.table_add_tests_line_ramp.verticalHeader().setMinimumSectionSize(30)
        self.table_add_tests_line_ramp.verticalHeader().setDefaultSectionSize(30)
        self.table_add_tests_line_ramp.verticalHeader().setHighlightSections(True)
        self.table_add_tests_line_ramp.verticalHeader().setProperty("showSortIndicator", True)
        self.table_add_tests_line_ramp.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_99.addWidget(self.table_add_tests_line_ramp)

        self.frame_add_tests_line_ramp_params = QFrame(self.frame_add_tests_line_ramp)
        self.frame_add_tests_line_ramp_params.setObjectName(u"frame_add_tests_line_ramp_params")
        sizePolicy33.setHeightForWidth(self.frame_add_tests_line_ramp_params.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_line_ramp_params.setSizePolicy(sizePolicy33)
        self.frame_add_tests_line_ramp_params.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_line_ramp_params.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_add_tests_line_ramp_params)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(9, 0, 0, 0)
        self.frame_add_tests_line_ramp_buttons = QFrame(self.frame_add_tests_line_ramp_params)
        self.frame_add_tests_line_ramp_buttons.setObjectName(u"frame_add_tests_line_ramp_buttons")
        sizePolicy34.setHeightForWidth(self.frame_add_tests_line_ramp_buttons.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_line_ramp_buttons.setSizePolicy(sizePolicy34)
        self.frame_add_tests_line_ramp_buttons.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_line_ramp_buttons.setFrameShadow(QFrame.Raised)
        self.verticalLayout_100 = QVBoxLayout(self.frame_add_tests_line_ramp_buttons)
        self.verticalLayout_100.setObjectName(u"verticalLayout_100")
        self.verticalLayout_100.setContentsMargins(3, -1, -1, -1)
        self.btn_add_tests_line_ramp_add = QPushButton(self.frame_add_tests_line_ramp_buttons)
        self.btn_add_tests_line_ramp_add.setObjectName(u"btn_add_tests_line_ramp_add")
        self.btn_add_tests_line_ramp_add.setMinimumSize(QSize(150, 30))
        self.btn_add_tests_line_ramp_add.setFont(font13)
        self.btn_add_tests_line_ramp_add.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_line_ramp_add.setIcon(icon12)

        self.verticalLayout_100.addWidget(self.btn_add_tests_line_ramp_add)

        self.btn_add_tests_line_ramp_remove = QPushButton(self.frame_add_tests_line_ramp_buttons)
        self.btn_add_tests_line_ramp_remove.setObjectName(u"btn_add_tests_line_ramp_remove")
        self.btn_add_tests_line_ramp_remove.setMinimumSize(QSize(150, 30))
        self.btn_add_tests_line_ramp_remove.setFont(font13)
        self.btn_add_tests_line_ramp_remove.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_line_ramp_remove.setIcon(icon14)

        self.verticalLayout_100.addWidget(self.btn_add_tests_line_ramp_remove)

        self.btn_add_tests_line_ramp_clear = QPushButton(self.frame_add_tests_line_ramp_buttons)
        self.btn_add_tests_line_ramp_clear.setObjectName(u"btn_add_tests_line_ramp_clear")
        self.btn_add_tests_line_ramp_clear.setMinimumSize(QSize(150, 30))
        self.btn_add_tests_line_ramp_clear.setFont(font13)
        self.btn_add_tests_line_ramp_clear.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_line_ramp_clear.setIcon(icon2)

        self.verticalLayout_100.addWidget(self.btn_add_tests_line_ramp_clear)


        self.gridLayout_11.addWidget(self.frame_add_tests_line_ramp_buttons, 0, 2, 2, 1)

        self.lineedit_add_tests_line_ramp_frequency = QLineEdit(self.frame_add_tests_line_ramp_params)
        self.lineedit_add_tests_line_ramp_frequency.setObjectName(u"lineedit_add_tests_line_ramp_frequency")
        sizePolicy15.setHeightForWidth(self.lineedit_add_tests_line_ramp_frequency.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_line_ramp_frequency.setSizePolicy(sizePolicy15)
        self.lineedit_add_tests_line_ramp_frequency.setMinimumSize(QSize(0, 30))
        self.lineedit_add_tests_line_ramp_frequency.setFont(font10)
        self.lineedit_add_tests_line_ramp_frequency.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_11.addWidget(self.lineedit_add_tests_line_ramp_frequency, 1, 0, 1, 1)

        self.lineedit_add_tests_line_ramp_voltage = QLineEdit(self.frame_add_tests_line_ramp_params)
        self.lineedit_add_tests_line_ramp_voltage.setObjectName(u"lineedit_add_tests_line_ramp_voltage")
        sizePolicy15.setHeightForWidth(self.lineedit_add_tests_line_ramp_voltage.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_line_ramp_voltage.setSizePolicy(sizePolicy15)
        self.lineedit_add_tests_line_ramp_voltage.setMinimumSize(QSize(0, 30))
        self.lineedit_add_tests_line_ramp_voltage.setFont(font10)
        self.lineedit_add_tests_line_ramp_voltage.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_11.addWidget(self.lineedit_add_tests_line_ramp_voltage, 0, 0, 1, 1)

        self.frame_add_tests_line_ramp_coupling = QFrame(self.frame_add_tests_line_ramp_params)
        self.frame_add_tests_line_ramp_coupling.setObjectName(u"frame_add_tests_line_ramp_coupling")
        self.frame_add_tests_line_ramp_coupling.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_line_ramp_coupling.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_73 = QHBoxLayout(self.frame_add_tests_line_ramp_coupling)
        self.horizontalLayout_73.setObjectName(u"horizontalLayout_73")
        self.widget_toggle_add_tests_line_ramp_coupling = QCheckBox(self.frame_add_tests_line_ramp_coupling)
        self.widget_toggle_add_tests_line_ramp_coupling.setObjectName(u"widget_toggle_add_tests_line_ramp_coupling")
        self.widget_toggle_add_tests_line_ramp_coupling.setFont(font10)

        self.horizontalLayout_73.addWidget(self.widget_toggle_add_tests_line_ramp_coupling)


        self.gridLayout_11.addWidget(self.frame_add_tests_line_ramp_coupling, 1, 1, 1, 1)

        self.lineedit_add_tests_line_ramp_slew_rate = QLineEdit(self.frame_add_tests_line_ramp_params)
        self.lineedit_add_tests_line_ramp_slew_rate.setObjectName(u"lineedit_add_tests_line_ramp_slew_rate")
        sizePolicy15.setHeightForWidth(self.lineedit_add_tests_line_ramp_slew_rate.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_line_ramp_slew_rate.setSizePolicy(sizePolicy15)
        self.lineedit_add_tests_line_ramp_slew_rate.setMinimumSize(QSize(0, 30))
        self.lineedit_add_tests_line_ramp_slew_rate.setFont(font10)
        self.lineedit_add_tests_line_ramp_slew_rate.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_11.addWidget(self.lineedit_add_tests_line_ramp_slew_rate, 0, 1, 1, 1)


        self.verticalLayout_99.addWidget(self.frame_add_tests_line_ramp_params)


        self.gridLayout_10.addWidget(self.frame_add_tests_line_ramp, 0, 0, 1, 1)

        self.stackedwidget_add_tests_params_top.addWidget(self.page_add_tests_sp1_line_ramp)

        self.verticalLayout_48.addWidget(self.stackedwidget_add_tests_params_top)

        self.stackedwidget_add_tests_params_bot = QStackedWidget(self.frame_add_tests_testparams)
        self.stackedwidget_add_tests_params_bot.setObjectName(u"stackedwidget_add_tests_params_bot")
        sizePolicy16.setHeightForWidth(self.stackedwidget_add_tests_params_bot.sizePolicy().hasHeightForWidth())
        self.stackedwidget_add_tests_params_bot.setSizePolicy(sizePolicy16)
        self.page_add_tests_sp2_empty = QWidget()
        self.page_add_tests_sp2_empty.setObjectName(u"page_add_tests_sp2_empty")
        self.stackedwidget_add_tests_params_bot.addWidget(self.page_add_tests_sp2_empty)
        self.page_add_tests_sp2_load_range = QWidget()
        self.page_add_tests_sp2_load_range.setObjectName(u"page_add_tests_sp2_load_range")
        self.gridLayout_6 = QGridLayout(self.page_add_tests_sp2_load_range)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_add_tests_load_range = QFrame(self.page_add_tests_sp2_load_range)
        self.frame_add_tests_load_range.setObjectName(u"frame_add_tests_load_range")
        self.frame_add_tests_load_range.setEnabled(True)
        sizePolicy12.setHeightForWidth(self.frame_add_tests_load_range.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_load_range.setSizePolicy(sizePolicy12)
        self.frame_add_tests_load_range.setMinimumSize(QSize(0, 300))
        self.frame_add_tests_load_range.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(39, 44, 54);\n"
"	border-radius: 5px;\n"
"}")
        self.frame_add_tests_load_range.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_load_range.setFrameShadow(QFrame.Raised)
        self.verticalLayout_42 = QVBoxLayout(self.frame_add_tests_load_range)
        self.verticalLayout_42.setSpacing(0)
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.verticalLayout_42.setContentsMargins(0, 0, 0, 0)
        self.frame_add_tests_load_range_top = QFrame(self.frame_add_tests_load_range)
        self.frame_add_tests_load_range_top.setObjectName(u"frame_add_tests_load_range_top")
        sizePolicy25.setHeightForWidth(self.frame_add_tests_load_range_top.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_load_range_top.setSizePolicy(sizePolicy25)
        self.frame_add_tests_load_range_top.setMaximumSize(QSize(16777215, 16777215))
        self.frame_add_tests_load_range_top.setToolTipDuration(2)
        self.frame_add_tests_load_range_top.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_load_range_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_add_tests_load_range_top)
        self.horizontalLayout_27.setSpacing(6)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(6, 6, 6, 6)
        self.label_add_tests_load_range = QLabel(self.frame_add_tests_load_range_top)
        self.label_add_tests_load_range.setObjectName(u"label_add_tests_load_range")
        sizePolicy32.setHeightForWidth(self.label_add_tests_load_range.sizePolicy().hasHeightForWidth())
        self.label_add_tests_load_range.setSizePolicy(sizePolicy32)
        self.label_add_tests_load_range.setFont(font10)
        self.label_add_tests_load_range.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_27.addWidget(self.label_add_tests_load_range)

        self.cbx_add_tests_load_range_type = QComboBox(self.frame_add_tests_load_range_top)
        self.cbx_add_tests_load_range_type.setObjectName(u"cbx_add_tests_load_range_type")
        self.cbx_add_tests_load_range_type.setEnabled(True)
        sizePolicy32.setHeightForWidth(self.cbx_add_tests_load_range_type.sizePolicy().hasHeightForWidth())
        self.cbx_add_tests_load_range_type.setSizePolicy(sizePolicy32)
        self.cbx_add_tests_load_range_type.setMinimumSize(QSize(0, 40))
        self.cbx_add_tests_load_range_type.setMaximumSize(QSize(16777215, 40))
        self.cbx_add_tests_load_range_type.setFont(font10)
        self.cbx_add_tests_load_range_type.setStyleSheet(u"QComboBox:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}")

        self.horizontalLayout_27.addWidget(self.cbx_add_tests_load_range_type)

        self.btn_add_tests_load_range_add_setting = QPushButton(self.frame_add_tests_load_range_top)
        self.btn_add_tests_load_range_add_setting.setObjectName(u"btn_add_tests_load_range_add_setting")
        sizePolicy15.setHeightForWidth(self.btn_add_tests_load_range_add_setting.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_load_range_add_setting.setSizePolicy(sizePolicy15)
        self.btn_add_tests_load_range_add_setting.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_load_range_add_setting.setFont(font13)
        self.btn_add_tests_load_range_add_setting.setToolTipDuration(-1)
        self.btn_add_tests_load_range_add_setting.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_load_range_add_setting.setIcon(icon12)

        self.horizontalLayout_27.addWidget(self.btn_add_tests_load_range_add_setting)

        self.btn_add_tests_load_range_duplicate_setting = QPushButton(self.frame_add_tests_load_range_top)
        self.btn_add_tests_load_range_duplicate_setting.setObjectName(u"btn_add_tests_load_range_duplicate_setting")
        sizePolicy15.setHeightForWidth(self.btn_add_tests_load_range_duplicate_setting.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_load_range_duplicate_setting.setSizePolicy(sizePolicy15)
        self.btn_add_tests_load_range_duplicate_setting.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_load_range_duplicate_setting.setFont(font13)
        self.btn_add_tests_load_range_duplicate_setting.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_load_range_duplicate_setting.setIcon(icon13)

        self.horizontalLayout_27.addWidget(self.btn_add_tests_load_range_duplicate_setting)

        self.btn_add_tests_load_range_remove_setting = QPushButton(self.frame_add_tests_load_range_top)
        self.btn_add_tests_load_range_remove_setting.setObjectName(u"btn_add_tests_load_range_remove_setting")
        sizePolicy15.setHeightForWidth(self.btn_add_tests_load_range_remove_setting.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_load_range_remove_setting.setSizePolicy(sizePolicy15)
        self.btn_add_tests_load_range_remove_setting.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_load_range_remove_setting.setFont(font13)
        self.btn_add_tests_load_range_remove_setting.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_load_range_remove_setting.setIcon(icon14)

        self.horizontalLayout_27.addWidget(self.btn_add_tests_load_range_remove_setting)


        self.verticalLayout_42.addWidget(self.frame_add_tests_load_range_top)

        self.table_add_tests_load_range = QTableWidget(self.frame_add_tests_load_range)
        if (self.table_add_tests_load_range.columnCount() < 2):
            self.table_add_tests_load_range.setColumnCount(2)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.table_add_tests_load_range.setHorizontalHeaderItem(0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.table_add_tests_load_range.setHorizontalHeaderItem(1, __qtablewidgetitem13)
        if (self.table_add_tests_load_range.rowCount() < 3):
            self.table_add_tests_load_range.setRowCount(3)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.table_add_tests_load_range.setItem(0, 0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.table_add_tests_load_range.setItem(1, 0, __qtablewidgetitem15)
        self.table_add_tests_load_range.setObjectName(u"table_add_tests_load_range")
        sizePolicy3.setHeightForWidth(self.table_add_tests_load_range.sizePolicy().hasHeightForWidth())
        self.table_add_tests_load_range.setSizePolicy(sizePolicy3)
        palette3 = QPalette()
        palette3.setBrush(QPalette.Active, QPalette.WindowText, brush6)
        palette3.setBrush(QPalette.Active, QPalette.Button, brush15)
        palette3.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette3.setBrush(QPalette.Active, QPalette.ButtonText, brush6)
        palette3.setBrush(QPalette.Active, QPalette.Base, brush15)
        palette3.setBrush(QPalette.Active, QPalette.Window, brush15)
        brush22 = QBrush(QColor(210, 210, 210, 128))
        brush22.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.Active, QPalette.PlaceholderText, brush22)
#endif
        palette3.setBrush(QPalette.Inactive, QPalette.WindowText, brush6)
        palette3.setBrush(QPalette.Inactive, QPalette.Button, brush15)
        palette3.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette3.setBrush(QPalette.Inactive, QPalette.ButtonText, brush6)
        palette3.setBrush(QPalette.Inactive, QPalette.Base, brush15)
        palette3.setBrush(QPalette.Inactive, QPalette.Window, brush15)
        brush23 = QBrush(QColor(210, 210, 210, 128))
        brush23.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush23)
#endif
        palette3.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette3.setBrush(QPalette.Disabled, QPalette.Button, brush15)
        palette3.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette3.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette3.setBrush(QPalette.Disabled, QPalette.Base, brush15)
        palette3.setBrush(QPalette.Disabled, QPalette.Window, brush15)
        brush24 = QBrush(QColor(210, 210, 210, 128))
        brush24.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush24)
#endif
        self.table_add_tests_load_range.setPalette(palette3)
        self.table_add_tests_load_range.setFont(font10)
        self.table_add_tests_load_range.setStyleSheet(u"QTableWidget {	\n"
"	background-color: rgb(39, 44, 54);\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
"\n"
"QHeaderView::section{\n"
"	background-color: rgb(39, 44, 54);\n"
"\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWid"
                        "get::horizontalHeader {	\n"
"	background-color: rgb(81, 255, 0);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"")
        self.table_add_tests_load_range.setFrameShape(QFrame.NoFrame)
        self.table_add_tests_load_range.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table_add_tests_load_range.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_add_tests_load_range.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_add_tests_load_range.setAlternatingRowColors(False)
        self.table_add_tests_load_range.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_add_tests_load_range.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_add_tests_load_range.setShowGrid(True)
        self.table_add_tests_load_range.setGridStyle(Qt.SolidLine)
        self.table_add_tests_load_range.setSortingEnabled(False)
        self.table_add_tests_load_range.setCornerButtonEnabled(True)
        self.table_add_tests_load_range.setRowCount(3)
        self.table_add_tests_load_range.horizontalHeader().setVisible(False)
        self.table_add_tests_load_range.horizontalHeader().setCascadingSectionResizes(True)
        self.table_add_tests_load_range.horizontalHeader().setDefaultSectionSize(200)
        self.table_add_tests_load_range.horizontalHeader().setStretchLastSection(False)
        self.table_add_tests_load_range.verticalHeader().setVisible(False)
        self.table_add_tests_load_range.verticalHeader().setCascadingSectionResizes(True)
        self.table_add_tests_load_range.verticalHeader().setDefaultSectionSize(23)
        self.table_add_tests_load_range.verticalHeader().setHighlightSections(True)
        self.table_add_tests_load_range.verticalHeader().setProperty("showSortIndicator", True)
        self.table_add_tests_load_range.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_42.addWidget(self.table_add_tests_load_range)

        self.frame_add_tests_load_range_params = QFrame(self.frame_add_tests_load_range)
        self.frame_add_tests_load_range_params.setObjectName(u"frame_add_tests_load_range_params")
        sizePolicy33.setHeightForWidth(self.frame_add_tests_load_range_params.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_load_range_params.setSizePolicy(sizePolicy33)
        self.frame_add_tests_load_range_params.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_load_range_params.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_add_tests_load_range_params)
        self.horizontalLayout_28.setSpacing(6)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(9, 0, 0, 0)
        self.frame_add_tests_load_range_params_options = QFrame(self.frame_add_tests_load_range_params)
        self.frame_add_tests_load_range_params_options.setObjectName(u"frame_add_tests_load_range_params_options")
        sizePolicy18.setHeightForWidth(self.frame_add_tests_load_range_params_options.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_load_range_params_options.setSizePolicy(sizePolicy18)
        self.frame_add_tests_load_range_params_options.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_load_range_params_options.setFrameShadow(QFrame.Raised)
        self.formLayout_4 = QFormLayout(self.frame_add_tests_load_range_params_options)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_add_tests_soak_per_load_4 = QLabel(self.frame_add_tests_load_range_params_options)
        self.label_add_tests_soak_per_load_4.setObjectName(u"label_add_tests_soak_per_load_4")
        self.label_add_tests_soak_per_load_4.setFont(font10)
        self.label_add_tests_soak_per_load_4.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_add_tests_soak_per_load_4)

        self.lineedit_add_tests_load_range_percent = QLineEdit(self.frame_add_tests_load_range_params_options)
        self.lineedit_add_tests_load_range_percent.setObjectName(u"lineedit_add_tests_load_range_percent")
        sizePolicy35 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy35.setHorizontalStretch(2)
        sizePolicy35.setVerticalStretch(0)
        sizePolicy35.setHeightForWidth(self.lineedit_add_tests_load_range_percent.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_load_range_percent.setSizePolicy(sizePolicy35)
        self.lineedit_add_tests_load_range_percent.setMinimumSize(QSize(0, 30))
        self.lineedit_add_tests_load_range_percent.setFont(font10)
        self.lineedit_add_tests_load_range_percent.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.lineedit_add_tests_load_range_percent)

        self.label_add_tests_soak_per_load_2 = QLabel(self.frame_add_tests_load_range_params_options)
        self.label_add_tests_soak_per_load_2.setObjectName(u"label_add_tests_soak_per_load_2")
        self.label_add_tests_soak_per_load_2.setFont(font10)
        self.label_add_tests_soak_per_load_2.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.label_add_tests_soak_per_load_2)

        self.cbx_add_tests_load_range_direction = QComboBox(self.frame_add_tests_load_range_params_options)
        self.cbx_add_tests_load_range_direction.setObjectName(u"cbx_add_tests_load_range_direction")
        self.cbx_add_tests_load_range_direction.setEnabled(True)
        sizePolicy25.setHeightForWidth(self.cbx_add_tests_load_range_direction.sizePolicy().hasHeightForWidth())
        self.cbx_add_tests_load_range_direction.setSizePolicy(sizePolicy25)
        self.cbx_add_tests_load_range_direction.setMinimumSize(QSize(0, 30))
        self.cbx_add_tests_load_range_direction.setMaximumSize(QSize(16777215, 30))
        self.cbx_add_tests_load_range_direction.setFont(font10)
        self.cbx_add_tests_load_range_direction.setStyleSheet(u"QComboBox:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}")

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.cbx_add_tests_load_range_direction)


        self.horizontalLayout_28.addWidget(self.frame_add_tests_load_range_params_options)

        self.frame_add_tests_load_range_buttons = QFrame(self.frame_add_tests_load_range_params)
        self.frame_add_tests_load_range_buttons.setObjectName(u"frame_add_tests_load_range_buttons")
        sizePolicy11.setHeightForWidth(self.frame_add_tests_load_range_buttons.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_load_range_buttons.setSizePolicy(sizePolicy11)
        self.frame_add_tests_load_range_buttons.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_load_range_buttons.setFrameShadow(QFrame.Raised)
        self.verticalLayout_41 = QVBoxLayout(self.frame_add_tests_load_range_buttons)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.verticalLayout_41.setContentsMargins(3, -1, -1, -1)
        self.btn_add_tests_load_range_add = QPushButton(self.frame_add_tests_load_range_buttons)
        self.btn_add_tests_load_range_add.setObjectName(u"btn_add_tests_load_range_add")
        self.btn_add_tests_load_range_add.setEnabled(True)
        self.btn_add_tests_load_range_add.setMinimumSize(QSize(150, 30))
        self.btn_add_tests_load_range_add.setFont(font13)
        self.btn_add_tests_load_range_add.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_load_range_add.setIcon(icon12)

        self.verticalLayout_41.addWidget(self.btn_add_tests_load_range_add)

        self.btn_add_tests_load_range_remove = QPushButton(self.frame_add_tests_load_range_buttons)
        self.btn_add_tests_load_range_remove.setObjectName(u"btn_add_tests_load_range_remove")
        self.btn_add_tests_load_range_remove.setMinimumSize(QSize(150, 30))
        self.btn_add_tests_load_range_remove.setFont(font13)
        self.btn_add_tests_load_range_remove.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_load_range_remove.setIcon(icon14)

        self.verticalLayout_41.addWidget(self.btn_add_tests_load_range_remove)

        self.btn_add_tests_load_range_clear = QPushButton(self.frame_add_tests_load_range_buttons)
        self.btn_add_tests_load_range_clear.setObjectName(u"btn_add_tests_load_range_clear")
        self.btn_add_tests_load_range_clear.setMinimumSize(QSize(150, 30))
        self.btn_add_tests_load_range_clear.setFont(font13)
        self.btn_add_tests_load_range_clear.setStyleSheet(u"QPushButton {\n"
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
        icon15 = QIcon()
        icon15.addFile(u":/20x20/icons/20x20/cil-x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_load_range_clear.setIcon(icon15)

        self.verticalLayout_41.addWidget(self.btn_add_tests_load_range_clear)


        self.horizontalLayout_28.addWidget(self.frame_add_tests_load_range_buttons)


        self.verticalLayout_42.addWidget(self.frame_add_tests_load_range_params)


        self.gridLayout_6.addWidget(self.frame_add_tests_load_range, 0, 0, 1, 1)

        self.stackedwidget_add_tests_params_bot.addWidget(self.page_add_tests_sp2_load_range)
        self.page_add_tests_sp2_cvcc = QWidget()
        self.page_add_tests_sp2_cvcc.setObjectName(u"page_add_tests_sp2_cvcc")
        self.verticalLayout_45 = QVBoxLayout(self.page_add_tests_sp2_cvcc)
        self.verticalLayout_45.setSpacing(0)
        self.verticalLayout_45.setObjectName(u"verticalLayout_45")
        self.verticalLayout_45.setContentsMargins(0, 0, 0, 0)
        self.frame_add_tests_cvcc = QFrame(self.page_add_tests_sp2_cvcc)
        self.frame_add_tests_cvcc.setObjectName(u"frame_add_tests_cvcc")
        self.frame_add_tests_cvcc.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(39, 44, 54);\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"")
        self.frame_add_tests_cvcc.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_cvcc.setFrameShadow(QFrame.Raised)
        self.verticalLayout_90 = QVBoxLayout(self.frame_add_tests_cvcc)
        self.verticalLayout_90.setObjectName(u"verticalLayout_90")
        self.frame_add_tests_cvcc_top = QFrame(self.frame_add_tests_cvcc)
        self.frame_add_tests_cvcc_top.setObjectName(u"frame_add_tests_cvcc_top")
        self.frame_add_tests_cvcc_top.setEnabled(True)
        self.frame_add_tests_cvcc_top.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_cvcc_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_61 = QHBoxLayout(self.frame_add_tests_cvcc_top)
        self.horizontalLayout_61.setObjectName(u"horizontalLayout_61")
        self.label_add_tests_cvcc_settings = QLabel(self.frame_add_tests_cvcc_top)
        self.label_add_tests_cvcc_settings.setObjectName(u"label_add_tests_cvcc_settings")
        sizePolicy25.setHeightForWidth(self.label_add_tests_cvcc_settings.sizePolicy().hasHeightForWidth())
        self.label_add_tests_cvcc_settings.setSizePolicy(sizePolicy25)
        self.label_add_tests_cvcc_settings.setMaximumSize(QSize(16777215, 40))
        self.label_add_tests_cvcc_settings.setFont(font10)
        self.label_add_tests_cvcc_settings.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_61.addWidget(self.label_add_tests_cvcc_settings)

        self.chkbox_add_tests_cvcc_multi_setpoints = QCheckBox(self.frame_add_tests_cvcc_top)
        self.chkbox_add_tests_cvcc_multi_setpoints.setObjectName(u"chkbox_add_tests_cvcc_multi_setpoints")
        self.chkbox_add_tests_cvcc_multi_setpoints.setEnabled(True)
        sizePolicy36 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy36.setHorizontalStretch(0)
        sizePolicy36.setVerticalStretch(0)
        sizePolicy36.setHeightForWidth(self.chkbox_add_tests_cvcc_multi_setpoints.sizePolicy().hasHeightForWidth())
        self.chkbox_add_tests_cvcc_multi_setpoints.setSizePolicy(sizePolicy36)
        self.chkbox_add_tests_cvcc_multi_setpoints.setFont(font10)
        self.chkbox_add_tests_cvcc_multi_setpoints.setLayoutDirection(Qt.LeftToRight)
        self.chkbox_add_tests_cvcc_multi_setpoints.setAutoFillBackground(False)
        self.chkbox_add_tests_cvcc_multi_setpoints.setStyleSheet(u"QCheckBox:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.chkbox_add_tests_cvcc_multi_setpoints.setChecked(True)
        self.chkbox_add_tests_cvcc_multi_setpoints.setTristate(False)

        self.horizontalLayout_61.addWidget(self.chkbox_add_tests_cvcc_multi_setpoints)


        self.verticalLayout_90.addWidget(self.frame_add_tests_cvcc_top)

        self.frame_add_tests_cvcc_bot = QFrame(self.frame_add_tests_cvcc)
        self.frame_add_tests_cvcc_bot.setObjectName(u"frame_add_tests_cvcc_bot")
        self.frame_add_tests_cvcc_bot.setEnabled(True)
        self.frame_add_tests_cvcc_bot.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_cvcc_bot.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_add_tests_cvcc_bot)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_add_tests_cvcc_nom_voltage = QLabel(self.frame_add_tests_cvcc_bot)
        self.label_add_tests_cvcc_nom_voltage.setObjectName(u"label_add_tests_cvcc_nom_voltage")
        self.label_add_tests_cvcc_nom_voltage.setEnabled(True)
        self.label_add_tests_cvcc_nom_voltage.setFont(font10)
        self.label_add_tests_cvcc_nom_voltage.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_4.addWidget(self.label_add_tests_cvcc_nom_voltage, 0, 0, 1, 1)

        self.label_add_tests_cvcc_max_current = QLabel(self.frame_add_tests_cvcc_bot)
        self.label_add_tests_cvcc_max_current.setObjectName(u"label_add_tests_cvcc_max_current")
        self.label_add_tests_cvcc_max_current.setFont(font10)
        self.label_add_tests_cvcc_max_current.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_4.addWidget(self.label_add_tests_cvcc_max_current, 1, 0, 1, 1)

        self.lineedit_add_tests_cvcc_max_current = QLineEdit(self.frame_add_tests_cvcc_bot)
        self.lineedit_add_tests_cvcc_max_current.setObjectName(u"lineedit_add_tests_cvcc_max_current")
        self.lineedit_add_tests_cvcc_max_current.setEnabled(True)
        sizePolicy37 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy37.setHorizontalStretch(0)
        sizePolicy37.setVerticalStretch(0)
        sizePolicy37.setHeightForWidth(self.lineedit_add_tests_cvcc_max_current.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_cvcc_max_current.setSizePolicy(sizePolicy37)
        self.lineedit_add_tests_cvcc_max_current.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_cvcc_max_current.setFont(font10)
        self.lineedit_add_tests_cvcc_max_current.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_4.addWidget(self.lineedit_add_tests_cvcc_max_current, 1, 2, 1, 1)

        self.lineedit_add_tests_cvcc_nom_voltage = QLineEdit(self.frame_add_tests_cvcc_bot)
        self.lineedit_add_tests_cvcc_nom_voltage.setObjectName(u"lineedit_add_tests_cvcc_nom_voltage")
        self.lineedit_add_tests_cvcc_nom_voltage.setEnabled(True)
        sizePolicy37.setHeightForWidth(self.lineedit_add_tests_cvcc_nom_voltage.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_cvcc_nom_voltage.setSizePolicy(sizePolicy37)
        self.lineedit_add_tests_cvcc_nom_voltage.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_cvcc_nom_voltage.setFont(font10)
        self.lineedit_add_tests_cvcc_nom_voltage.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_4.addWidget(self.lineedit_add_tests_cvcc_nom_voltage, 0, 2, 1, 1)

        self.lineedit_add_tests_cvcc_step_size = QLineEdit(self.frame_add_tests_cvcc_bot)
        self.lineedit_add_tests_cvcc_step_size.setObjectName(u"lineedit_add_tests_cvcc_step_size")
        sizePolicy37.setHeightForWidth(self.lineedit_add_tests_cvcc_step_size.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_cvcc_step_size.setSizePolicy(sizePolicy37)
        self.lineedit_add_tests_cvcc_step_size.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_cvcc_step_size.setFont(font10)
        self.lineedit_add_tests_cvcc_step_size.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_4.addWidget(self.lineedit_add_tests_cvcc_step_size, 4, 2, 1, 1)

        self.label_add_tests_cvcc_step_size = QLabel(self.frame_add_tests_cvcc_bot)
        self.label_add_tests_cvcc_step_size.setObjectName(u"label_add_tests_cvcc_step_size")
        self.label_add_tests_cvcc_step_size.setFont(font10)
        self.label_add_tests_cvcc_step_size.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_4.addWidget(self.label_add_tests_cvcc_step_size, 4, 0, 1, 1)

        self.lineedit_add_tests_cvcc_min_current = QLineEdit(self.frame_add_tests_cvcc_bot)
        self.lineedit_add_tests_cvcc_min_current.setObjectName(u"lineedit_add_tests_cvcc_min_current")
        sizePolicy37.setHeightForWidth(self.lineedit_add_tests_cvcc_min_current.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_cvcc_min_current.setSizePolicy(sizePolicy37)
        self.lineedit_add_tests_cvcc_min_current.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_cvcc_min_current.setFont(font10)
        self.lineedit_add_tests_cvcc_min_current.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_4.addWidget(self.lineedit_add_tests_cvcc_min_current, 2, 2, 1, 1)

        self.label_add_tests_cvcc_min_current = QLabel(self.frame_add_tests_cvcc_bot)
        self.label_add_tests_cvcc_min_current.setObjectName(u"label_add_tests_cvcc_min_current")
        self.label_add_tests_cvcc_min_current.setFont(font10)
        self.label_add_tests_cvcc_min_current.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_4.addWidget(self.label_add_tests_cvcc_min_current, 2, 0, 1, 1)


        self.verticalLayout_90.addWidget(self.frame_add_tests_cvcc_bot)


        self.verticalLayout_45.addWidget(self.frame_add_tests_cvcc)

        self.stackedwidget_add_tests_params_bot.addWidget(self.page_add_tests_sp2_cvcc)

        self.verticalLayout_48.addWidget(self.stackedwidget_add_tests_params_bot)


        self.verticalLayout_47.addWidget(self.frame_add_tests_testparams)


        self.horizontalLayout_60.addWidget(self.frame_add_tests_left)

        self.frame_add_tests_middle = QFrame(self.frame_add_tests_maincontent)
        self.frame_add_tests_middle.setObjectName(u"frame_add_tests_middle")
        sizePolicy29.setHeightForWidth(self.frame_add_tests_middle.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_middle.setSizePolicy(sizePolicy29)
        self.frame_add_tests_middle.setMaximumSize(QSize(600, 16777215))
        self.frame_add_tests_middle.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_middle.setFrameShadow(QFrame.Raised)
        self.verticalLayout_78 = QVBoxLayout(self.frame_add_tests_middle)
        self.verticalLayout_78.setObjectName(u"verticalLayout_78")
        self.verticalLayout_78.setContentsMargins(0, 6, 0, 0)
        self.frame_add_tests_timing_params = QFrame(self.frame_add_tests_middle)
        self.frame_add_tests_timing_params.setObjectName(u"frame_add_tests_timing_params")
        sizePolicy38 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy38.setHorizontalStretch(0)
        sizePolicy38.setVerticalStretch(3)
        sizePolicy38.setHeightForWidth(self.frame_add_tests_timing_params.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_timing_params.setSizePolicy(sizePolicy38)
        self.frame_add_tests_timing_params.setMinimumSize(QSize(0, 150))
        self.frame_add_tests_timing_params.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(39, 44, 54);\n"
"	border-radius: 5px;\n"
"};")
        self.frame_add_tests_timing_params.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_timing_params.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_add_tests_timing_params)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.frame_add_tests_timing_params_select = QFrame(self.frame_add_tests_timing_params)
        self.frame_add_tests_timing_params_select.setObjectName(u"frame_add_tests_timing_params_select")
        self.frame_add_tests_timing_params_select.setMinimumSize(QSize(0, 40))
        self.frame_add_tests_timing_params_select.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.frame_add_tests_timing_params_select.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_timing_params_select.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_add_tests_timing_params_select)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_add_tests_timing_params = QLabel(self.frame_add_tests_timing_params_select)
        self.label_add_tests_timing_params.setObjectName(u"label_add_tests_timing_params")
        sizePolicy32.setHeightForWidth(self.label_add_tests_timing_params.sizePolicy().hasHeightForWidth())
        self.label_add_tests_timing_params.setSizePolicy(sizePolicy32)
        self.label_add_tests_timing_params.setFont(font10)

        self.horizontalLayout_20.addWidget(self.label_add_tests_timing_params)

        self.cbx_add_tests_timing_params = QComboBox(self.frame_add_tests_timing_params_select)
        self.cbx_add_tests_timing_params.setObjectName(u"cbx_add_tests_timing_params")
        self.cbx_add_tests_timing_params.setEnabled(True)
        sizePolicy32.setHeightForWidth(self.cbx_add_tests_timing_params.sizePolicy().hasHeightForWidth())
        self.cbx_add_tests_timing_params.setSizePolicy(sizePolicy32)
        self.cbx_add_tests_timing_params.setMinimumSize(QSize(0, 40))
        self.cbx_add_tests_timing_params.setMaximumSize(QSize(16777215, 40))
        self.cbx_add_tests_timing_params.setFont(font10)
        self.cbx_add_tests_timing_params.setStyleSheet(u"QComboBox:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}")

        self.horizontalLayout_20.addWidget(self.cbx_add_tests_timing_params)

        self.btn_add_tests_timing_params_add_setting = QPushButton(self.frame_add_tests_timing_params_select)
        self.btn_add_tests_timing_params_add_setting.setObjectName(u"btn_add_tests_timing_params_add_setting")
        sizePolicy15.setHeightForWidth(self.btn_add_tests_timing_params_add_setting.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_timing_params_add_setting.setSizePolicy(sizePolicy15)
        self.btn_add_tests_timing_params_add_setting.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_timing_params_add_setting.setFont(font13)
        self.btn_add_tests_timing_params_add_setting.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_timing_params_add_setting.setIcon(icon12)

        self.horizontalLayout_20.addWidget(self.btn_add_tests_timing_params_add_setting)

        self.btn_add_tests_timing_params_duplicate_setting = QPushButton(self.frame_add_tests_timing_params_select)
        self.btn_add_tests_timing_params_duplicate_setting.setObjectName(u"btn_add_tests_timing_params_duplicate_setting")
        sizePolicy15.setHeightForWidth(self.btn_add_tests_timing_params_duplicate_setting.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_timing_params_duplicate_setting.setSizePolicy(sizePolicy15)
        self.btn_add_tests_timing_params_duplicate_setting.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_timing_params_duplicate_setting.setFont(font13)
        self.btn_add_tests_timing_params_duplicate_setting.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_timing_params_duplicate_setting.setIcon(icon13)

        self.horizontalLayout_20.addWidget(self.btn_add_tests_timing_params_duplicate_setting)

        self.btn_add_tests_timing_params_remove_setting = QPushButton(self.frame_add_tests_timing_params_select)
        self.btn_add_tests_timing_params_remove_setting.setObjectName(u"btn_add_tests_timing_params_remove_setting")
        sizePolicy15.setHeightForWidth(self.btn_add_tests_timing_params_remove_setting.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_timing_params_remove_setting.setSizePolicy(sizePolicy15)
        self.btn_add_tests_timing_params_remove_setting.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_timing_params_remove_setting.setFont(font13)
        self.btn_add_tests_timing_params_remove_setting.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_timing_params_remove_setting.setIcon(icon14)

        self.horizontalLayout_20.addWidget(self.btn_add_tests_timing_params_remove_setting)


        self.verticalLayout_9.addWidget(self.frame_add_tests_timing_params_select)

        self.frame_add_tests_timing_params_vals = QFrame(self.frame_add_tests_timing_params)
        self.frame_add_tests_timing_params_vals.setObjectName(u"frame_add_tests_timing_params_vals")
        self.frame_add_tests_timing_params_vals.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_timing_params_vals.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_65 = QHBoxLayout(self.frame_add_tests_timing_params_vals)
        self.horizontalLayout_65.setSpacing(0)
        self.horizontalLayout_65.setObjectName(u"horizontalLayout_65")
        self.horizontalLayout_65.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.frame_add_tests_timing_params_vals)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_6)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(-1, 0, 20, 0)
        self.lineedit_add_tests_testtime_param1 = QLineEdit(self.frame_6)
        self.lineedit_add_tests_testtime_param1.setObjectName(u"lineedit_add_tests_testtime_param1")
        self.lineedit_add_tests_testtime_param1.setEnabled(True)
        sizePolicy37.setHeightForWidth(self.lineedit_add_tests_testtime_param1.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_testtime_param1.setSizePolicy(sizePolicy37)
        self.lineedit_add_tests_testtime_param1.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_testtime_param1.setMaximumSize(QSize(50, 16777215))
        self.lineedit_add_tests_testtime_param1.setFont(font10)
        self.lineedit_add_tests_testtime_param1.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_13.addWidget(self.lineedit_add_tests_testtime_param1, 0, 1, 1, 1)

        self.lineedit_add_tests_testtime_param2 = QLineEdit(self.frame_6)
        self.lineedit_add_tests_testtime_param2.setObjectName(u"lineedit_add_tests_testtime_param2")
        sizePolicy37.setHeightForWidth(self.lineedit_add_tests_testtime_param2.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_testtime_param2.setSizePolicy(sizePolicy37)
        self.lineedit_add_tests_testtime_param2.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_testtime_param2.setMaximumSize(QSize(50, 16777215))
        self.lineedit_add_tests_testtime_param2.setFont(font10)
        self.lineedit_add_tests_testtime_param2.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_13.addWidget(self.lineedit_add_tests_testtime_param2, 1, 1, 1, 1)

        self.label_add_tests_testtime_param1 = QLabel(self.frame_6)
        self.label_add_tests_testtime_param1.setObjectName(u"label_add_tests_testtime_param1")
        self.label_add_tests_testtime_param1.setFont(font10)
        self.label_add_tests_testtime_param1.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_13.addWidget(self.label_add_tests_testtime_param1, 0, 0, 1, 1)

        self.label_add_tests_testtime_param2 = QLabel(self.frame_6)
        self.label_add_tests_testtime_param2.setObjectName(u"label_add_tests_testtime_param2")
        self.label_add_tests_testtime_param2.setFont(font10)
        self.label_add_tests_testtime_param2.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_13.addWidget(self.label_add_tests_testtime_param2, 1, 0, 1, 1)


        self.horizontalLayout_65.addWidget(self.frame_6)

        self.frame_7 = QFrame(self.frame_add_tests_timing_params_vals)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_7)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(-1, 0, 20, 0)
        self.label_add_tests_testtime_param3 = QLabel(self.frame_7)
        self.label_add_tests_testtime_param3.setObjectName(u"label_add_tests_testtime_param3")
        self.label_add_tests_testtime_param3.setFont(font10)
        self.label_add_tests_testtime_param3.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_14.addWidget(self.label_add_tests_testtime_param3, 0, 0, 1, 1)

        self.lineedit_add_tests_testtime_param3 = QLineEdit(self.frame_7)
        self.lineedit_add_tests_testtime_param3.setObjectName(u"lineedit_add_tests_testtime_param3")
        sizePolicy19.setHeightForWidth(self.lineedit_add_tests_testtime_param3.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_testtime_param3.setSizePolicy(sizePolicy19)
        self.lineedit_add_tests_testtime_param3.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_testtime_param3.setMaximumSize(QSize(50, 16777215))
        self.lineedit_add_tests_testtime_param3.setFont(font10)
        self.lineedit_add_tests_testtime_param3.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_14.addWidget(self.lineedit_add_tests_testtime_param3, 0, 1, 1, 1)

        self.label_add_tests_testtime_param4 = QLabel(self.frame_7)
        self.label_add_tests_testtime_param4.setObjectName(u"label_add_tests_testtime_param4")
        self.label_add_tests_testtime_param4.setFont(font10)
        self.label_add_tests_testtime_param4.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_14.addWidget(self.label_add_tests_testtime_param4, 1, 0, 1, 1)

        self.lineedit_add_tests_testtime_param4 = QLineEdit(self.frame_7)
        self.lineedit_add_tests_testtime_param4.setObjectName(u"lineedit_add_tests_testtime_param4")
        sizePolicy19.setHeightForWidth(self.lineedit_add_tests_testtime_param4.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_testtime_param4.setSizePolicy(sizePolicy19)
        self.lineedit_add_tests_testtime_param4.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_testtime_param4.setMaximumSize(QSize(50, 16777215))
        self.lineedit_add_tests_testtime_param4.setFont(font10)
        self.lineedit_add_tests_testtime_param4.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_14.addWidget(self.lineedit_add_tests_testtime_param4, 1, 1, 1, 1)


        self.horizontalLayout_65.addWidget(self.frame_7)

        self.frame_7.raise_()
        self.frame_6.raise_()

        self.verticalLayout_9.addWidget(self.frame_add_tests_timing_params_vals)


        self.verticalLayout_78.addWidget(self.frame_add_tests_timing_params)

        self.stackedwidget_add_tests_middle = QStackedWidget(self.frame_add_tests_middle)
        self.stackedwidget_add_tests_middle.setObjectName(u"stackedwidget_add_tests_middle")
        sizePolicy39 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy39.setHorizontalStretch(0)
        sizePolicy39.setVerticalStretch(8)
        sizePolicy39.setHeightForWidth(self.stackedwidget_add_tests_middle.sizePolicy().hasHeightForWidth())
        self.stackedwidget_add_tests_middle.setSizePolicy(sizePolicy39)
        self.stackedwidget_add_tests_middle.setMinimumSize(QSize(0, 450))
        self.page_add_tests_sp3_empty = QWidget()
        self.page_add_tests_sp3_empty.setObjectName(u"page_add_tests_sp3_empty")
        sizePolicy39.setHeightForWidth(self.page_add_tests_sp3_empty.sizePolicy().hasHeightForWidth())
        self.page_add_tests_sp3_empty.setSizePolicy(sizePolicy39)
        self.page_add_tests_sp3_empty.setMinimumSize(QSize(0, 450))
        self.stackedwidget_add_tests_middle.addWidget(self.page_add_tests_sp3_empty)
        self.page_add_tests_sp3_usbpd = QWidget()
        self.page_add_tests_sp3_usbpd.setObjectName(u"page_add_tests_sp3_usbpd")
        sizePolicy39.setHeightForWidth(self.page_add_tests_sp3_usbpd.sizePolicy().hasHeightForWidth())
        self.page_add_tests_sp3_usbpd.setSizePolicy(sizePolicy39)
        self.page_add_tests_sp3_usbpd.setMinimumSize(QSize(0, 450))
        self.horizontalLayout_69 = QHBoxLayout(self.page_add_tests_sp3_usbpd)
        self.horizontalLayout_69.setSpacing(0)
        self.horizontalLayout_69.setObjectName(u"horizontalLayout_69")
        self.horizontalLayout_69.setContentsMargins(0, 0, 0, 0)
        self.frame_add_tests_usbpd = QFrame(self.page_add_tests_sp3_usbpd)
        self.frame_add_tests_usbpd.setObjectName(u"frame_add_tests_usbpd")
        self.frame_add_tests_usbpd.setEnabled(True)
        sizePolicy40 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy40.setHorizontalStretch(0)
        sizePolicy40.setVerticalStretch(9)
        sizePolicy40.setHeightForWidth(self.frame_add_tests_usbpd.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_usbpd.setSizePolicy(sizePolicy40)
        self.frame_add_tests_usbpd.setMinimumSize(QSize(0, 450))
        self.frame_add_tests_usbpd.setMaximumSize(QSize(16777215, 16777215))
        self.frame_add_tests_usbpd.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(39, 44, 54);\n"
"	border-radius: 5px;\n"
"};")
        self.frame_add_tests_usbpd.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_usbpd.setFrameShadow(QFrame.Raised)
        self.verticalLayout_46 = QVBoxLayout(self.frame_add_tests_usbpd)
        self.verticalLayout_46.setObjectName(u"verticalLayout_46")
        self.frame_add_tests_usbpd_top = QFrame(self.frame_add_tests_usbpd)
        self.frame_add_tests_usbpd_top.setObjectName(u"frame_add_tests_usbpd_top")
        sizePolicy19.setHeightForWidth(self.frame_add_tests_usbpd_top.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_usbpd_top.setSizePolicy(sizePolicy19)
        self.frame_add_tests_usbpd_top.setMinimumSize(QSize(0, 50))
        self.frame_add_tests_usbpd_top.setMaximumSize(QSize(16777215, 50))
        self.frame_add_tests_usbpd_top.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_usbpd_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_57 = QHBoxLayout(self.frame_add_tests_usbpd_top)
        self.horizontalLayout_57.setObjectName(u"horizontalLayout_57")
        self.chkbox_add_tests_usbpd_device = QCheckBox(self.frame_add_tests_usbpd_top)
        self.chkbox_add_tests_usbpd_device.setObjectName(u"chkbox_add_tests_usbpd_device")
        self.chkbox_add_tests_usbpd_device.setEnabled(True)
        sizePolicy36.setHeightForWidth(self.chkbox_add_tests_usbpd_device.sizePolicy().hasHeightForWidth())
        self.chkbox_add_tests_usbpd_device.setSizePolicy(sizePolicy36)
        self.chkbox_add_tests_usbpd_device.setFont(font10)
        self.chkbox_add_tests_usbpd_device.setLayoutDirection(Qt.LeftToRight)
        self.chkbox_add_tests_usbpd_device.setAutoFillBackground(False)
        self.chkbox_add_tests_usbpd_device.setStyleSheet(u"QCheckBox:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.chkbox_add_tests_usbpd_device.setChecked(True)
        self.chkbox_add_tests_usbpd_device.setTristate(False)

        self.horizontalLayout_57.addWidget(self.chkbox_add_tests_usbpd_device)

        self.btn_add_tests_usbpd_get_source_caps = QPushButton(self.frame_add_tests_usbpd_top)
        self.btn_add_tests_usbpd_get_source_caps.setObjectName(u"btn_add_tests_usbpd_get_source_caps")
        self.btn_add_tests_usbpd_get_source_caps.setMinimumSize(QSize(150, 30))
        self.btn_add_tests_usbpd_get_source_caps.setFont(font13)
        self.btn_add_tests_usbpd_get_source_caps.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_usbpd_get_source_caps.setIcon(icon11)
        self.btn_add_tests_usbpd_get_source_caps.setCheckable(True)
        self.btn_add_tests_usbpd_get_source_caps.setChecked(True)

        self.horizontalLayout_57.addWidget(self.btn_add_tests_usbpd_get_source_caps)


        self.verticalLayout_46.addWidget(self.frame_add_tests_usbpd_top)

        self.frame_add_tests_nominal_output_setting = QFrame(self.frame_add_tests_usbpd)
        self.frame_add_tests_nominal_output_setting.setObjectName(u"frame_add_tests_nominal_output_setting")
        self.frame_add_tests_nominal_output_setting.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_nominal_output_setting.setFrameShadow(QFrame.Raised)
        self.verticalLayout_92 = QVBoxLayout(self.frame_add_tests_nominal_output_setting)
        self.verticalLayout_92.setObjectName(u"verticalLayout_92")
        self.vspacer_add_tests_usbpd = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_92.addItem(self.vspacer_add_tests_usbpd)

        self.table_add_tests_source_caps = QTableWidget(self.frame_add_tests_nominal_output_setting)
        if (self.table_add_tests_source_caps.columnCount() < 5):
            self.table_add_tests_source_caps.setColumnCount(5)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setFont(font10);
        self.table_add_tests_source_caps.setHorizontalHeaderItem(0, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setFont(font10);
        self.table_add_tests_source_caps.setHorizontalHeaderItem(1, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        __qtablewidgetitem18.setFont(font10);
        self.table_add_tests_source_caps.setHorizontalHeaderItem(2, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        __qtablewidgetitem19.setFont(font10);
        self.table_add_tests_source_caps.setHorizontalHeaderItem(3, __qtablewidgetitem19)
        font17 = QFont()
        font17.setFamily(u"MS Shell Dlg 2")
        font17.setPointSize(12)
        __qtablewidgetitem20 = QTableWidgetItem()
        __qtablewidgetitem20.setFont(font17);
        self.table_add_tests_source_caps.setHorizontalHeaderItem(4, __qtablewidgetitem20)
        if (self.table_add_tests_source_caps.rowCount() < 6):
            self.table_add_tests_source_caps.setRowCount(6)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.table_add_tests_source_caps.setItem(0, 0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.table_add_tests_source_caps.setItem(1, 0, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.table_add_tests_source_caps.setItem(2, 0, __qtablewidgetitem23)
        self.table_add_tests_source_caps.setObjectName(u"table_add_tests_source_caps")
        sizePolicy41 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy41.setHorizontalStretch(1)
        sizePolicy41.setVerticalStretch(0)
        sizePolicy41.setHeightForWidth(self.table_add_tests_source_caps.sizePolicy().hasHeightForWidth())
        self.table_add_tests_source_caps.setSizePolicy(sizePolicy41)
        palette4 = QPalette()
        palette4.setBrush(QPalette.Active, QPalette.WindowText, brush6)
        palette4.setBrush(QPalette.Active, QPalette.Button, brush15)
        brush25 = QBrush(QColor(127, 213, 255, 255))
        brush25.setStyle(Qt.SolidPattern)
        palette4.setBrush(QPalette.Active, QPalette.Light, brush25)
        brush26 = QBrush(QColor(63, 191, 255, 255))
        brush26.setStyle(Qt.SolidPattern)
        palette4.setBrush(QPalette.Active, QPalette.Midlight, brush26)
        brush27 = QBrush(QColor(0, 85, 127, 255))
        brush27.setStyle(Qt.SolidPattern)
        palette4.setBrush(QPalette.Active, QPalette.Dark, brush27)
        brush28 = QBrush(QColor(0, 113, 170, 255))
        brush28.setStyle(Qt.SolidPattern)
        palette4.setBrush(QPalette.Active, QPalette.Mid, brush28)
        palette4.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette4.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette4.setBrush(QPalette.Active, QPalette.ButtonText, brush6)
        palette4.setBrush(QPalette.Active, QPalette.Base, brush15)
        palette4.setBrush(QPalette.Active, QPalette.Window, brush15)
        palette4.setBrush(QPalette.Active, QPalette.Shadow, brush7)
        brush29 = QBrush(QColor(127, 212, 255, 255))
        brush29.setStyle(Qt.SolidPattern)
        palette4.setBrush(QPalette.Active, QPalette.AlternateBase, brush29)
        brush30 = QBrush(QColor(255, 255, 220, 255))
        brush30.setStyle(Qt.SolidPattern)
        palette4.setBrush(QPalette.Active, QPalette.ToolTipBase, brush30)
        palette4.setBrush(QPalette.Active, QPalette.ToolTipText, brush7)
        brush31 = QBrush(QColor(210, 210, 210, 128))
        brush31.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.Active, QPalette.PlaceholderText, brush31)
#endif
        palette4.setBrush(QPalette.Inactive, QPalette.WindowText, brush6)
        palette4.setBrush(QPalette.Inactive, QPalette.Button, brush15)
        palette4.setBrush(QPalette.Inactive, QPalette.Light, brush25)
        palette4.setBrush(QPalette.Inactive, QPalette.Midlight, brush26)
        palette4.setBrush(QPalette.Inactive, QPalette.Dark, brush27)
        palette4.setBrush(QPalette.Inactive, QPalette.Mid, brush28)
        palette4.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette4.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette4.setBrush(QPalette.Inactive, QPalette.ButtonText, brush6)
        palette4.setBrush(QPalette.Inactive, QPalette.Base, brush15)
        palette4.setBrush(QPalette.Inactive, QPalette.Window, brush15)
        palette4.setBrush(QPalette.Inactive, QPalette.Shadow, brush7)
        palette4.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush29)
        palette4.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush30)
        palette4.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush7)
        brush32 = QBrush(QColor(210, 210, 210, 128))
        brush32.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush32)
#endif
        palette4.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette4.setBrush(QPalette.Disabled, QPalette.Button, brush15)
        palette4.setBrush(QPalette.Disabled, QPalette.Light, brush25)
        palette4.setBrush(QPalette.Disabled, QPalette.Midlight, brush26)
        palette4.setBrush(QPalette.Disabled, QPalette.Dark, brush27)
        palette4.setBrush(QPalette.Disabled, QPalette.Mid, brush28)
        palette4.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette4.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette4.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette4.setBrush(QPalette.Disabled, QPalette.Base, brush15)
        palette4.setBrush(QPalette.Disabled, QPalette.Window, brush15)
        palette4.setBrush(QPalette.Disabled, QPalette.Shadow, brush7)
        brush33 = QBrush(QColor(0, 170, 255, 255))
        brush33.setStyle(Qt.SolidPattern)
        palette4.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush33)
        palette4.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush30)
        palette4.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush7)
        brush34 = QBrush(QColor(210, 210, 210, 128))
        brush34.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush34)
#endif
        self.table_add_tests_source_caps.setPalette(palette4)
        self.table_add_tests_source_caps.setFont(font10)
        self.table_add_tests_source_caps.setStyleSheet(u"QTableWidget {	\n"
"	background-color: rgb(39, 44, 54);\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
"\n"
"QHeaderView::section{\n"
"	background-color: rgb(39, 44, 54);\n"
"\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWid"
                        "get::horizontalHeader {	\n"
"	background-color: rgb(81, 255, 0);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"")
        self.table_add_tests_source_caps.setFrameShape(QFrame.NoFrame)
        self.table_add_tests_source_caps.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table_add_tests_source_caps.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_add_tests_source_caps.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.table_add_tests_source_caps.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_add_tests_source_caps.setAlternatingRowColors(False)
        self.table_add_tests_source_caps.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_add_tests_source_caps.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_add_tests_source_caps.setShowGrid(True)
        self.table_add_tests_source_caps.setGridStyle(Qt.SolidLine)
        self.table_add_tests_source_caps.setSortingEnabled(False)
        self.table_add_tests_source_caps.setCornerButtonEnabled(True)
        self.table_add_tests_source_caps.setRowCount(6)
        self.table_add_tests_source_caps.horizontalHeader().setVisible(False)
        self.table_add_tests_source_caps.horizontalHeader().setCascadingSectionResizes(False)
        self.table_add_tests_source_caps.horizontalHeader().setMinimumSectionSize(100)
        self.table_add_tests_source_caps.horizontalHeader().setDefaultSectionSize(130)
        self.table_add_tests_source_caps.horizontalHeader().setProperty("showSortIndicator", False)
        self.table_add_tests_source_caps.horizontalHeader().setStretchLastSection(False)
        self.table_add_tests_source_caps.verticalHeader().setVisible(False)
        self.table_add_tests_source_caps.verticalHeader().setCascadingSectionResizes(True)
        self.table_add_tests_source_caps.verticalHeader().setMinimumSectionSize(23)
        self.table_add_tests_source_caps.verticalHeader().setDefaultSectionSize(50)
        self.table_add_tests_source_caps.verticalHeader().setHighlightSections(True)
        self.table_add_tests_source_caps.verticalHeader().setProperty("showSortIndicator", True)
        self.table_add_tests_source_caps.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_92.addWidget(self.table_add_tests_source_caps)

        self.frame_add_tests_nominal_output_parameters = QFrame(self.frame_add_tests_nominal_output_setting)
        self.frame_add_tests_nominal_output_parameters.setObjectName(u"frame_add_tests_nominal_output_parameters")
        self.frame_add_tests_nominal_output_parameters.setMinimumSize(QSize(0, 0))
        self.frame_add_tests_nominal_output_parameters.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_nominal_output_parameters.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_add_tests_nominal_output_parameters)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.frame_add_tests_nominal_output_voltage = QFrame(self.frame_add_tests_nominal_output_parameters)
        self.frame_add_tests_nominal_output_voltage.setObjectName(u"frame_add_tests_nominal_output_voltage")
        sizePolicy11.setHeightForWidth(self.frame_add_tests_nominal_output_voltage.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_nominal_output_voltage.setSizePolicy(sizePolicy11)
        self.frame_add_tests_nominal_output_voltage.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_nominal_output_voltage.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_88 = QHBoxLayout(self.frame_add_tests_nominal_output_voltage)
        self.horizontalLayout_88.setObjectName(u"horizontalLayout_88")
        self.label_add_tests_nominal_output_voltage = QLabel(self.frame_add_tests_nominal_output_voltage)
        self.label_add_tests_nominal_output_voltage.setObjectName(u"label_add_tests_nominal_output_voltage")
        self.label_add_tests_nominal_output_voltage.setEnabled(True)
        sizePolicy42 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy42.setHorizontalStretch(0)
        sizePolicy42.setVerticalStretch(0)
        sizePolicy42.setHeightForWidth(self.label_add_tests_nominal_output_voltage.sizePolicy().hasHeightForWidth())
        self.label_add_tests_nominal_output_voltage.setSizePolicy(sizePolicy42)
        self.label_add_tests_nominal_output_voltage.setFont(font10)
        self.label_add_tests_nominal_output_voltage.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_88.addWidget(self.label_add_tests_nominal_output_voltage)

        self.lineedit_add_tests_nominal_output_voltage = QLineEdit(self.frame_add_tests_nominal_output_voltage)
        self.lineedit_add_tests_nominal_output_voltage.setObjectName(u"lineedit_add_tests_nominal_output_voltage")
        sizePolicy42.setHeightForWidth(self.lineedit_add_tests_nominal_output_voltage.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_nominal_output_voltage.setSizePolicy(sizePolicy42)
        self.lineedit_add_tests_nominal_output_voltage.setMinimumSize(QSize(0, 30))
        self.lineedit_add_tests_nominal_output_voltage.setFont(font10)
        self.lineedit_add_tests_nominal_output_voltage.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.horizontalLayout_88.addWidget(self.lineedit_add_tests_nominal_output_voltage)


        self.gridLayout_15.addWidget(self.frame_add_tests_nominal_output_voltage, 0, 0, 1, 1)

        self.frame_add_tests_nominal_output_current = QFrame(self.frame_add_tests_nominal_output_parameters)
        self.frame_add_tests_nominal_output_current.setObjectName(u"frame_add_tests_nominal_output_current")
        sizePolicy11.setHeightForWidth(self.frame_add_tests_nominal_output_current.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_nominal_output_current.setSizePolicy(sizePolicy11)
        self.frame_add_tests_nominal_output_current.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_nominal_output_current.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_87 = QHBoxLayout(self.frame_add_tests_nominal_output_current)
        self.horizontalLayout_87.setObjectName(u"horizontalLayout_87")
        self.label_add_tests_nominal_output_current = QLabel(self.frame_add_tests_nominal_output_current)
        self.label_add_tests_nominal_output_current.setObjectName(u"label_add_tests_nominal_output_current")
        sizePolicy42.setHeightForWidth(self.label_add_tests_nominal_output_current.sizePolicy().hasHeightForWidth())
        self.label_add_tests_nominal_output_current.setSizePolicy(sizePolicy42)
        self.label_add_tests_nominal_output_current.setFont(font10)
        self.label_add_tests_nominal_output_current.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_87.addWidget(self.label_add_tests_nominal_output_current)

        self.lineedit_add_tests_nominal_output_current = QLineEdit(self.frame_add_tests_nominal_output_current)
        self.lineedit_add_tests_nominal_output_current.setObjectName(u"lineedit_add_tests_nominal_output_current")
        sizePolicy42.setHeightForWidth(self.lineedit_add_tests_nominal_output_current.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_nominal_output_current.setSizePolicy(sizePolicy42)
        self.lineedit_add_tests_nominal_output_current.setMinimumSize(QSize(0, 30))
        self.lineedit_add_tests_nominal_output_current.setFont(font10)
        self.lineedit_add_tests_nominal_output_current.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.horizontalLayout_87.addWidget(self.lineedit_add_tests_nominal_output_current)


        self.gridLayout_15.addWidget(self.frame_add_tests_nominal_output_current, 0, 1, 1, 1)


        self.verticalLayout_92.addWidget(self.frame_add_tests_nominal_output_parameters)

        self.chkbox_add_tests_proportional_current_request = QCheckBox(self.frame_add_tests_nominal_output_setting)
        self.chkbox_add_tests_proportional_current_request.setObjectName(u"chkbox_add_tests_proportional_current_request")
        sizePolicy19.setHeightForWidth(self.chkbox_add_tests_proportional_current_request.sizePolicy().hasHeightForWidth())
        self.chkbox_add_tests_proportional_current_request.setSizePolicy(sizePolicy19)
        self.chkbox_add_tests_proportional_current_request.setFont(font10)
        self.chkbox_add_tests_proportional_current_request.setAutoFillBackground(False)
        self.chkbox_add_tests_proportional_current_request.setStyleSheet(u"QCheckBox:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.verticalLayout_92.addWidget(self.chkbox_add_tests_proportional_current_request)


        self.verticalLayout_46.addWidget(self.frame_add_tests_nominal_output_setting)


        self.horizontalLayout_69.addWidget(self.frame_add_tests_usbpd)

        self.stackedwidget_add_tests_middle.addWidget(self.page_add_tests_sp3_usbpd)
        self.page_add_tests_sp3_i2c = QWidget()
        self.page_add_tests_sp3_i2c.setObjectName(u"page_add_tests_sp3_i2c")
        sizePolicy39.setHeightForWidth(self.page_add_tests_sp3_i2c.sizePolicy().hasHeightForWidth())
        self.page_add_tests_sp3_i2c.setSizePolicy(sizePolicy39)
        self.page_add_tests_sp3_i2c.setMinimumSize(QSize(0, 450))
        self.horizontalLayout_70 = QHBoxLayout(self.page_add_tests_sp3_i2c)
        self.horizontalLayout_70.setSpacing(0)
        self.horizontalLayout_70.setObjectName(u"horizontalLayout_70")
        self.horizontalLayout_70.setContentsMargins(0, 0, 0, 0)
        self.frame_add_tests_i2c = QFrame(self.page_add_tests_sp3_i2c)
        self.frame_add_tests_i2c.setObjectName(u"frame_add_tests_i2c")
        sizePolicy39.setHeightForWidth(self.frame_add_tests_i2c.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_i2c.setSizePolicy(sizePolicy39)
        self.frame_add_tests_i2c.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(39, 44, 54);\n"
"	border-radius: 5px;\n"
"};")
        self.frame_add_tests_i2c.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_i2c.setFrameShadow(QFrame.Raised)
        self.verticalLayout_94 = QVBoxLayout(self.frame_add_tests_i2c)
        self.verticalLayout_94.setObjectName(u"verticalLayout_94")
        self.label_add_tests_i2c_settings = QLabel(self.frame_add_tests_i2c)
        self.label_add_tests_i2c_settings.setObjectName(u"label_add_tests_i2c_settings")
        self.label_add_tests_i2c_settings.setMaximumSize(QSize(16777215, 20))
        self.label_add_tests_i2c_settings.setFont(font10)
        self.label_add_tests_i2c_settings.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.verticalLayout_94.addWidget(self.label_add_tests_i2c_settings)

        self.frame_28 = QFrame(self.frame_add_tests_i2c)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setFrameShape(QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_28)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setVerticalSpacing(0)
        self.frame_add_tests_i2c_param_2 = QFrame(self.frame_28)
        self.frame_add_tests_i2c_param_2.setObjectName(u"frame_add_tests_i2c_param_2")
        sizePolicy11.setHeightForWidth(self.frame_add_tests_i2c_param_2.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_i2c_param_2.setSizePolicy(sizePolicy11)
        self.frame_add_tests_i2c_param_2.setStyleSheet(u"")
        self.frame_add_tests_i2c_param_2.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_i2c_param_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_74 = QHBoxLayout(self.frame_add_tests_i2c_param_2)
        self.horizontalLayout_74.setSpacing(0)
        self.horizontalLayout_74.setObjectName(u"horizontalLayout_74")
        self.horizontalLayout_74.setContentsMargins(10, 0, 0, 0)
        self.label_add_tests_i2c_param_2 = QLabel(self.frame_add_tests_i2c_param_2)
        self.label_add_tests_i2c_param_2.setObjectName(u"label_add_tests_i2c_param_2")
        sizePolicy5.setHeightForWidth(self.label_add_tests_i2c_param_2.sizePolicy().hasHeightForWidth())
        self.label_add_tests_i2c_param_2.setSizePolicy(sizePolicy5)
        self.label_add_tests_i2c_param_2.setFont(font10)
        self.label_add_tests_i2c_param_2.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_74.addWidget(self.label_add_tests_i2c_param_2)

        self.lineedit_add_tests_i2c_param_2 = QLineEdit(self.frame_add_tests_i2c_param_2)
        self.lineedit_add_tests_i2c_param_2.setObjectName(u"lineedit_add_tests_i2c_param_2")
        self.lineedit_add_tests_i2c_param_2.setEnabled(True)
        sizePolicy37.setHeightForWidth(self.lineedit_add_tests_i2c_param_2.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_i2c_param_2.setSizePolicy(sizePolicy37)
        self.lineedit_add_tests_i2c_param_2.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_i2c_param_2.setMaximumSize(QSize(100, 16777215))
        self.lineedit_add_tests_i2c_param_2.setFont(font10)
        self.lineedit_add_tests_i2c_param_2.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.horizontalLayout_74.addWidget(self.lineedit_add_tests_i2c_param_2)


        self.gridLayout_12.addWidget(self.frame_add_tests_i2c_param_2, 0, 1, 1, 1)

        self.frame_add_tests_i2c_param_4 = QFrame(self.frame_28)
        self.frame_add_tests_i2c_param_4.setObjectName(u"frame_add_tests_i2c_param_4")
        self.frame_add_tests_i2c_param_4.setStyleSheet(u"")
        self.frame_add_tests_i2c_param_4.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_i2c_param_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_76 = QHBoxLayout(self.frame_add_tests_i2c_param_4)
        self.horizontalLayout_76.setSpacing(0)
        self.horizontalLayout_76.setObjectName(u"horizontalLayout_76")
        self.horizontalLayout_76.setContentsMargins(10, 0, 0, 0)
        self.label_add_tests_i2c_param_4 = QLabel(self.frame_add_tests_i2c_param_4)
        self.label_add_tests_i2c_param_4.setObjectName(u"label_add_tests_i2c_param_4")
        sizePolicy43 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy43.setHorizontalStretch(1)
        sizePolicy43.setVerticalStretch(0)
        sizePolicy43.setHeightForWidth(self.label_add_tests_i2c_param_4.sizePolicy().hasHeightForWidth())
        self.label_add_tests_i2c_param_4.setSizePolicy(sizePolicy43)
        self.label_add_tests_i2c_param_4.setFont(font10)
        self.label_add_tests_i2c_param_4.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_76.addWidget(self.label_add_tests_i2c_param_4)

        self.lineedit_add_tests_i2c_param_4 = QLineEdit(self.frame_add_tests_i2c_param_4)
        self.lineedit_add_tests_i2c_param_4.setObjectName(u"lineedit_add_tests_i2c_param_4")
        self.lineedit_add_tests_i2c_param_4.setEnabled(True)
        sizePolicy44 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy44.setHorizontalStretch(1)
        sizePolicy44.setVerticalStretch(0)
        sizePolicy44.setHeightForWidth(self.lineedit_add_tests_i2c_param_4.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_i2c_param_4.setSizePolicy(sizePolicy44)
        self.lineedit_add_tests_i2c_param_4.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_i2c_param_4.setMaximumSize(QSize(100, 16777215))
        self.lineedit_add_tests_i2c_param_4.setFont(font10)
        self.lineedit_add_tests_i2c_param_4.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.horizontalLayout_76.addWidget(self.lineedit_add_tests_i2c_param_4)


        self.gridLayout_12.addWidget(self.frame_add_tests_i2c_param_4, 1, 1, 1, 1)

        self.frame_add_tests_i2c_param_1 = QFrame(self.frame_28)
        self.frame_add_tests_i2c_param_1.setObjectName(u"frame_add_tests_i2c_param_1")
        sizePolicy11.setHeightForWidth(self.frame_add_tests_i2c_param_1.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_i2c_param_1.setSizePolicy(sizePolicy11)
        self.frame_add_tests_i2c_param_1.setStyleSheet(u"")
        self.frame_add_tests_i2c_param_1.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_i2c_param_1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_71 = QHBoxLayout(self.frame_add_tests_i2c_param_1)
        self.horizontalLayout_71.setSpacing(0)
        self.horizontalLayout_71.setObjectName(u"horizontalLayout_71")
        self.horizontalLayout_71.setContentsMargins(0, 0, 0, 0)
        self.label_add_tests_i2c_param_1 = QLabel(self.frame_add_tests_i2c_param_1)
        self.label_add_tests_i2c_param_1.setObjectName(u"label_add_tests_i2c_param_1")
        sizePolicy45 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy45.setHorizontalStretch(0)
        sizePolicy45.setVerticalStretch(0)
        sizePolicy45.setHeightForWidth(self.label_add_tests_i2c_param_1.sizePolicy().hasHeightForWidth())
        self.label_add_tests_i2c_param_1.setSizePolicy(sizePolicy45)
        self.label_add_tests_i2c_param_1.setFont(font10)
        self.label_add_tests_i2c_param_1.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_71.addWidget(self.label_add_tests_i2c_param_1)

        self.lineedit_add_tests_i2c_param_1 = QLineEdit(self.frame_add_tests_i2c_param_1)
        self.lineedit_add_tests_i2c_param_1.setObjectName(u"lineedit_add_tests_i2c_param_1")
        self.lineedit_add_tests_i2c_param_1.setEnabled(True)
        sizePolicy37.setHeightForWidth(self.lineedit_add_tests_i2c_param_1.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_i2c_param_1.setSizePolicy(sizePolicy37)
        self.lineedit_add_tests_i2c_param_1.setMinimumSize(QSize(0, 30))
        self.lineedit_add_tests_i2c_param_1.setMaximumSize(QSize(100, 16777215))
        self.lineedit_add_tests_i2c_param_1.setFont(font10)
        self.lineedit_add_tests_i2c_param_1.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.horizontalLayout_71.addWidget(self.lineedit_add_tests_i2c_param_1)


        self.gridLayout_12.addWidget(self.frame_add_tests_i2c_param_1, 0, 0, 1, 1)

        self.frame_add_tests_i2c_cbxparam_4 = QFrame(self.frame_28)
        self.frame_add_tests_i2c_cbxparam_4.setObjectName(u"frame_add_tests_i2c_cbxparam_4")
        self.frame_add_tests_i2c_cbxparam_4.setStyleSheet(u"")
        self.frame_add_tests_i2c_cbxparam_4.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_i2c_cbxparam_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_84 = QHBoxLayout(self.frame_add_tests_i2c_cbxparam_4)
        self.horizontalLayout_84.setSpacing(0)
        self.horizontalLayout_84.setObjectName(u"horizontalLayout_84")
        self.horizontalLayout_84.setContentsMargins(10, 0, 0, 0)
        self.label_add_tests_i2c_cbxparam_4 = QLabel(self.frame_add_tests_i2c_cbxparam_4)
        self.label_add_tests_i2c_cbxparam_4.setObjectName(u"label_add_tests_i2c_cbxparam_4")
        sizePolicy43.setHeightForWidth(self.label_add_tests_i2c_cbxparam_4.sizePolicy().hasHeightForWidth())
        self.label_add_tests_i2c_cbxparam_4.setSizePolicy(sizePolicy43)
        self.label_add_tests_i2c_cbxparam_4.setFont(font10)
        self.label_add_tests_i2c_cbxparam_4.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_84.addWidget(self.label_add_tests_i2c_cbxparam_4)

        self.cbx_add_tests_i2c_cbxparam_4 = QComboBox(self.frame_add_tests_i2c_cbxparam_4)
        self.cbx_add_tests_i2c_cbxparam_4.setObjectName(u"cbx_add_tests_i2c_cbxparam_4")
        self.cbx_add_tests_i2c_cbxparam_4.setEnabled(True)
        sizePolicy31.setHeightForWidth(self.cbx_add_tests_i2c_cbxparam_4.sizePolicy().hasHeightForWidth())
        self.cbx_add_tests_i2c_cbxparam_4.setSizePolicy(sizePolicy31)
        self.cbx_add_tests_i2c_cbxparam_4.setMinimumSize(QSize(100, 35))
        self.cbx_add_tests_i2c_cbxparam_4.setMaximumSize(QSize(100, 35))
        self.cbx_add_tests_i2c_cbxparam_4.setFont(font10)
        self.cbx_add_tests_i2c_cbxparam_4.setStyleSheet(u"QComboBox:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}")

        self.horizontalLayout_84.addWidget(self.cbx_add_tests_i2c_cbxparam_4)


        self.gridLayout_12.addWidget(self.frame_add_tests_i2c_cbxparam_4, 6, 1, 1, 1)

        self.frame_add_tests_i2c_param_3 = QFrame(self.frame_28)
        self.frame_add_tests_i2c_param_3.setObjectName(u"frame_add_tests_i2c_param_3")
        self.frame_add_tests_i2c_param_3.setStyleSheet(u"")
        self.frame_add_tests_i2c_param_3.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_i2c_param_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_75 = QHBoxLayout(self.frame_add_tests_i2c_param_3)
        self.horizontalLayout_75.setSpacing(0)
        self.horizontalLayout_75.setObjectName(u"horizontalLayout_75")
        self.horizontalLayout_75.setContentsMargins(0, 0, 0, 0)
        self.label_add_tests_i2c_param_3 = QLabel(self.frame_add_tests_i2c_param_3)
        self.label_add_tests_i2c_param_3.setObjectName(u"label_add_tests_i2c_param_3")
        sizePolicy43.setHeightForWidth(self.label_add_tests_i2c_param_3.sizePolicy().hasHeightForWidth())
        self.label_add_tests_i2c_param_3.setSizePolicy(sizePolicy43)
        self.label_add_tests_i2c_param_3.setFont(font10)
        self.label_add_tests_i2c_param_3.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_75.addWidget(self.label_add_tests_i2c_param_3)

        self.lineedit_add_tests_i2c_param_3 = QLineEdit(self.frame_add_tests_i2c_param_3)
        self.lineedit_add_tests_i2c_param_3.setObjectName(u"lineedit_add_tests_i2c_param_3")
        self.lineedit_add_tests_i2c_param_3.setEnabled(True)
        sizePolicy44.setHeightForWidth(self.lineedit_add_tests_i2c_param_3.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_i2c_param_3.setSizePolicy(sizePolicy44)
        self.lineedit_add_tests_i2c_param_3.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_i2c_param_3.setMaximumSize(QSize(100, 16777215))
        self.lineedit_add_tests_i2c_param_3.setFont(font10)
        self.lineedit_add_tests_i2c_param_3.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.horizontalLayout_75.addWidget(self.lineedit_add_tests_i2c_param_3)


        self.gridLayout_12.addWidget(self.frame_add_tests_i2c_param_3, 1, 0, 1, 1)

        self.frame_add_tests_i2c_param_8 = QFrame(self.frame_28)
        self.frame_add_tests_i2c_param_8.setObjectName(u"frame_add_tests_i2c_param_8")
        self.frame_add_tests_i2c_param_8.setStyleSheet(u"")
        self.frame_add_tests_i2c_param_8.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_i2c_param_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_80 = QHBoxLayout(self.frame_add_tests_i2c_param_8)
        self.horizontalLayout_80.setSpacing(0)
        self.horizontalLayout_80.setObjectName(u"horizontalLayout_80")
        self.horizontalLayout_80.setContentsMargins(10, 0, 0, 0)
        self.label_add_tests_i2c_param_8 = QLabel(self.frame_add_tests_i2c_param_8)
        self.label_add_tests_i2c_param_8.setObjectName(u"label_add_tests_i2c_param_8")
        sizePolicy43.setHeightForWidth(self.label_add_tests_i2c_param_8.sizePolicy().hasHeightForWidth())
        self.label_add_tests_i2c_param_8.setSizePolicy(sizePolicy43)
        self.label_add_tests_i2c_param_8.setFont(font10)
        self.label_add_tests_i2c_param_8.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_80.addWidget(self.label_add_tests_i2c_param_8)

        self.lineedit_add_tests_i2c_param_8 = QLineEdit(self.frame_add_tests_i2c_param_8)
        self.lineedit_add_tests_i2c_param_8.setObjectName(u"lineedit_add_tests_i2c_param_8")
        self.lineedit_add_tests_i2c_param_8.setEnabled(True)
        sizePolicy44.setHeightForWidth(self.lineedit_add_tests_i2c_param_8.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_i2c_param_8.setSizePolicy(sizePolicy44)
        self.lineedit_add_tests_i2c_param_8.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_i2c_param_8.setMaximumSize(QSize(100, 16777215))
        self.lineedit_add_tests_i2c_param_8.setFont(font10)
        self.lineedit_add_tests_i2c_param_8.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.horizontalLayout_80.addWidget(self.lineedit_add_tests_i2c_param_8)


        self.gridLayout_12.addWidget(self.frame_add_tests_i2c_param_8, 3, 1, 1, 1)

        self.frame_add_tests_i2c_param_7 = QFrame(self.frame_28)
        self.frame_add_tests_i2c_param_7.setObjectName(u"frame_add_tests_i2c_param_7")
        self.frame_add_tests_i2c_param_7.setStyleSheet(u"")
        self.frame_add_tests_i2c_param_7.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_i2c_param_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_79 = QHBoxLayout(self.frame_add_tests_i2c_param_7)
        self.horizontalLayout_79.setSpacing(0)
        self.horizontalLayout_79.setObjectName(u"horizontalLayout_79")
        self.horizontalLayout_79.setContentsMargins(0, 0, 0, 0)
        self.label_add_tests_i2c_param_7 = QLabel(self.frame_add_tests_i2c_param_7)
        self.label_add_tests_i2c_param_7.setObjectName(u"label_add_tests_i2c_param_7")
        sizePolicy43.setHeightForWidth(self.label_add_tests_i2c_param_7.sizePolicy().hasHeightForWidth())
        self.label_add_tests_i2c_param_7.setSizePolicy(sizePolicy43)
        self.label_add_tests_i2c_param_7.setFont(font10)
        self.label_add_tests_i2c_param_7.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_79.addWidget(self.label_add_tests_i2c_param_7)

        self.lineedit_add_tests_i2c_param_7 = QLineEdit(self.frame_add_tests_i2c_param_7)
        self.lineedit_add_tests_i2c_param_7.setObjectName(u"lineedit_add_tests_i2c_param_7")
        self.lineedit_add_tests_i2c_param_7.setEnabled(True)
        sizePolicy44.setHeightForWidth(self.lineedit_add_tests_i2c_param_7.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_i2c_param_7.setSizePolicy(sizePolicy44)
        self.lineedit_add_tests_i2c_param_7.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_i2c_param_7.setMaximumSize(QSize(100, 16777215))
        self.lineedit_add_tests_i2c_param_7.setFont(font10)
        self.lineedit_add_tests_i2c_param_7.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.horizontalLayout_79.addWidget(self.lineedit_add_tests_i2c_param_7)


        self.gridLayout_12.addWidget(self.frame_add_tests_i2c_param_7, 3, 0, 1, 1)

        self.frame_add_tests_i2c_cbxparam_3 = QFrame(self.frame_28)
        self.frame_add_tests_i2c_cbxparam_3.setObjectName(u"frame_add_tests_i2c_cbxparam_3")
        self.frame_add_tests_i2c_cbxparam_3.setStyleSheet(u"")
        self.frame_add_tests_i2c_cbxparam_3.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_i2c_cbxparam_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_83 = QHBoxLayout(self.frame_add_tests_i2c_cbxparam_3)
        self.horizontalLayout_83.setSpacing(0)
        self.horizontalLayout_83.setObjectName(u"horizontalLayout_83")
        self.horizontalLayout_83.setContentsMargins(0, 0, 0, 0)
        self.label_add_tests_i2c_cbxparam_3 = QLabel(self.frame_add_tests_i2c_cbxparam_3)
        self.label_add_tests_i2c_cbxparam_3.setObjectName(u"label_add_tests_i2c_cbxparam_3")
        sizePolicy43.setHeightForWidth(self.label_add_tests_i2c_cbxparam_3.sizePolicy().hasHeightForWidth())
        self.label_add_tests_i2c_cbxparam_3.setSizePolicy(sizePolicy43)
        self.label_add_tests_i2c_cbxparam_3.setFont(font10)
        self.label_add_tests_i2c_cbxparam_3.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_83.addWidget(self.label_add_tests_i2c_cbxparam_3)

        self.cbx_add_tests_i2c_cbxparam_3 = QComboBox(self.frame_add_tests_i2c_cbxparam_3)
        self.cbx_add_tests_i2c_cbxparam_3.setObjectName(u"cbx_add_tests_i2c_cbxparam_3")
        self.cbx_add_tests_i2c_cbxparam_3.setEnabled(True)
        sizePolicy31.setHeightForWidth(self.cbx_add_tests_i2c_cbxparam_3.sizePolicy().hasHeightForWidth())
        self.cbx_add_tests_i2c_cbxparam_3.setSizePolicy(sizePolicy31)
        self.cbx_add_tests_i2c_cbxparam_3.setMinimumSize(QSize(0, 35))
        self.cbx_add_tests_i2c_cbxparam_3.setMaximumSize(QSize(100, 35))
        self.cbx_add_tests_i2c_cbxparam_3.setFont(font10)
        self.cbx_add_tests_i2c_cbxparam_3.setStyleSheet(u"QComboBox:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}")

        self.horizontalLayout_83.addWidget(self.cbx_add_tests_i2c_cbxparam_3)


        self.gridLayout_12.addWidget(self.frame_add_tests_i2c_cbxparam_3, 6, 0, 1, 1)

        self.frame_add_tests_i2c_cbxparam_2 = QFrame(self.frame_28)
        self.frame_add_tests_i2c_cbxparam_2.setObjectName(u"frame_add_tests_i2c_cbxparam_2")
        self.frame_add_tests_i2c_cbxparam_2.setStyleSheet(u"")
        self.frame_add_tests_i2c_cbxparam_2.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_i2c_cbxparam_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_82 = QHBoxLayout(self.frame_add_tests_i2c_cbxparam_2)
        self.horizontalLayout_82.setSpacing(0)
        self.horizontalLayout_82.setObjectName(u"horizontalLayout_82")
        self.horizontalLayout_82.setContentsMargins(10, 0, 0, 0)
        self.label_add_tests_i2c_cbxparam_2 = QLabel(self.frame_add_tests_i2c_cbxparam_2)
        self.label_add_tests_i2c_cbxparam_2.setObjectName(u"label_add_tests_i2c_cbxparam_2")
        sizePolicy43.setHeightForWidth(self.label_add_tests_i2c_cbxparam_2.sizePolicy().hasHeightForWidth())
        self.label_add_tests_i2c_cbxparam_2.setSizePolicy(sizePolicy43)
        self.label_add_tests_i2c_cbxparam_2.setFont(font10)
        self.label_add_tests_i2c_cbxparam_2.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_82.addWidget(self.label_add_tests_i2c_cbxparam_2)

        self.cbx_add_tests_i2c_cbxparam_2 = QComboBox(self.frame_add_tests_i2c_cbxparam_2)
        self.cbx_add_tests_i2c_cbxparam_2.setObjectName(u"cbx_add_tests_i2c_cbxparam_2")
        self.cbx_add_tests_i2c_cbxparam_2.setEnabled(True)
        sizePolicy31.setHeightForWidth(self.cbx_add_tests_i2c_cbxparam_2.sizePolicy().hasHeightForWidth())
        self.cbx_add_tests_i2c_cbxparam_2.setSizePolicy(sizePolicy31)
        self.cbx_add_tests_i2c_cbxparam_2.setMinimumSize(QSize(0, 35))
        self.cbx_add_tests_i2c_cbxparam_2.setMaximumSize(QSize(100, 35))
        self.cbx_add_tests_i2c_cbxparam_2.setFont(font10)
        self.cbx_add_tests_i2c_cbxparam_2.setStyleSheet(u"QComboBox:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}")

        self.horizontalLayout_82.addWidget(self.cbx_add_tests_i2c_cbxparam_2)


        self.gridLayout_12.addWidget(self.frame_add_tests_i2c_cbxparam_2, 5, 1, 1, 1)

        self.frame_add_tests_i2c_param_5 = QFrame(self.frame_28)
        self.frame_add_tests_i2c_param_5.setObjectName(u"frame_add_tests_i2c_param_5")
        self.frame_add_tests_i2c_param_5.setStyleSheet(u"")
        self.frame_add_tests_i2c_param_5.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_i2c_param_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_77 = QHBoxLayout(self.frame_add_tests_i2c_param_5)
        self.horizontalLayout_77.setSpacing(0)
        self.horizontalLayout_77.setObjectName(u"horizontalLayout_77")
        self.horizontalLayout_77.setContentsMargins(0, 0, 0, 0)
        self.label_add_tests_i2c_param_5 = QLabel(self.frame_add_tests_i2c_param_5)
        self.label_add_tests_i2c_param_5.setObjectName(u"label_add_tests_i2c_param_5")
        sizePolicy43.setHeightForWidth(self.label_add_tests_i2c_param_5.sizePolicy().hasHeightForWidth())
        self.label_add_tests_i2c_param_5.setSizePolicy(sizePolicy43)
        self.label_add_tests_i2c_param_5.setFont(font10)
        self.label_add_tests_i2c_param_5.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_77.addWidget(self.label_add_tests_i2c_param_5)

        self.lineedit_add_tests_i2c_param_5 = QLineEdit(self.frame_add_tests_i2c_param_5)
        self.lineedit_add_tests_i2c_param_5.setObjectName(u"lineedit_add_tests_i2c_param_5")
        self.lineedit_add_tests_i2c_param_5.setEnabled(True)
        sizePolicy44.setHeightForWidth(self.lineedit_add_tests_i2c_param_5.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_i2c_param_5.setSizePolicy(sizePolicy44)
        self.lineedit_add_tests_i2c_param_5.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_i2c_param_5.setMaximumSize(QSize(100, 16777215))
        self.lineedit_add_tests_i2c_param_5.setFont(font10)
        self.lineedit_add_tests_i2c_param_5.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.horizontalLayout_77.addWidget(self.lineedit_add_tests_i2c_param_5)


        self.gridLayout_12.addWidget(self.frame_add_tests_i2c_param_5, 2, 0, 1, 1)

        self.frame_add_tests_i2c_param_6 = QFrame(self.frame_28)
        self.frame_add_tests_i2c_param_6.setObjectName(u"frame_add_tests_i2c_param_6")
        self.frame_add_tests_i2c_param_6.setStyleSheet(u"")
        self.frame_add_tests_i2c_param_6.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_i2c_param_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_78 = QHBoxLayout(self.frame_add_tests_i2c_param_6)
        self.horizontalLayout_78.setSpacing(0)
        self.horizontalLayout_78.setObjectName(u"horizontalLayout_78")
        self.horizontalLayout_78.setContentsMargins(10, 0, 0, 0)
        self.label_add_tests_i2c_param_6 = QLabel(self.frame_add_tests_i2c_param_6)
        self.label_add_tests_i2c_param_6.setObjectName(u"label_add_tests_i2c_param_6")
        sizePolicy43.setHeightForWidth(self.label_add_tests_i2c_param_6.sizePolicy().hasHeightForWidth())
        self.label_add_tests_i2c_param_6.setSizePolicy(sizePolicy43)
        self.label_add_tests_i2c_param_6.setFont(font10)
        self.label_add_tests_i2c_param_6.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_78.addWidget(self.label_add_tests_i2c_param_6)

        self.lineedit_add_tests_i2c_param_6 = QLineEdit(self.frame_add_tests_i2c_param_6)
        self.lineedit_add_tests_i2c_param_6.setObjectName(u"lineedit_add_tests_i2c_param_6")
        self.lineedit_add_tests_i2c_param_6.setEnabled(True)
        sizePolicy44.setHeightForWidth(self.lineedit_add_tests_i2c_param_6.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_i2c_param_6.setSizePolicy(sizePolicy44)
        self.lineedit_add_tests_i2c_param_6.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_i2c_param_6.setMaximumSize(QSize(100, 16777215))
        self.lineedit_add_tests_i2c_param_6.setFont(font10)
        self.lineedit_add_tests_i2c_param_6.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.horizontalLayout_78.addWidget(self.lineedit_add_tests_i2c_param_6)


        self.gridLayout_12.addWidget(self.frame_add_tests_i2c_param_6, 2, 1, 1, 1)

        self.frame_add_tests_i2c_cbxparam_1 = QFrame(self.frame_28)
        self.frame_add_tests_i2c_cbxparam_1.setObjectName(u"frame_add_tests_i2c_cbxparam_1")
        self.frame_add_tests_i2c_cbxparam_1.setStyleSheet(u"")
        self.frame_add_tests_i2c_cbxparam_1.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_i2c_cbxparam_1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_81 = QHBoxLayout(self.frame_add_tests_i2c_cbxparam_1)
        self.horizontalLayout_81.setSpacing(0)
        self.horizontalLayout_81.setObjectName(u"horizontalLayout_81")
        self.horizontalLayout_81.setContentsMargins(0, 0, 0, 0)
        self.label_add_tests_i2c_cbxparam_1 = QLabel(self.frame_add_tests_i2c_cbxparam_1)
        self.label_add_tests_i2c_cbxparam_1.setObjectName(u"label_add_tests_i2c_cbxparam_1")
        sizePolicy43.setHeightForWidth(self.label_add_tests_i2c_cbxparam_1.sizePolicy().hasHeightForWidth())
        self.label_add_tests_i2c_cbxparam_1.setSizePolicy(sizePolicy43)
        self.label_add_tests_i2c_cbxparam_1.setFont(font10)
        self.label_add_tests_i2c_cbxparam_1.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_81.addWidget(self.label_add_tests_i2c_cbxparam_1)

        self.cbx_add_tests_i2c_cbxparam_1 = QComboBox(self.frame_add_tests_i2c_cbxparam_1)
        self.cbx_add_tests_i2c_cbxparam_1.setObjectName(u"cbx_add_tests_i2c_cbxparam_1")
        self.cbx_add_tests_i2c_cbxparam_1.setEnabled(True)
        sizePolicy31.setHeightForWidth(self.cbx_add_tests_i2c_cbxparam_1.sizePolicy().hasHeightForWidth())
        self.cbx_add_tests_i2c_cbxparam_1.setSizePolicy(sizePolicy31)
        self.cbx_add_tests_i2c_cbxparam_1.setMinimumSize(QSize(0, 35))
        self.cbx_add_tests_i2c_cbxparam_1.setMaximumSize(QSize(100, 35))
        self.cbx_add_tests_i2c_cbxparam_1.setFont(font10)
        self.cbx_add_tests_i2c_cbxparam_1.setStyleSheet(u"QComboBox:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}")

        self.horizontalLayout_81.addWidget(self.cbx_add_tests_i2c_cbxparam_1)


        self.gridLayout_12.addWidget(self.frame_add_tests_i2c_cbxparam_1, 5, 0, 1, 1)

        self.frame_add_tests_i2c_param_9 = QFrame(self.frame_28)
        self.frame_add_tests_i2c_param_9.setObjectName(u"frame_add_tests_i2c_param_9")
        self.frame_add_tests_i2c_param_9.setStyleSheet(u"")
        self.frame_add_tests_i2c_param_9.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_i2c_param_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_85 = QHBoxLayout(self.frame_add_tests_i2c_param_9)
        self.horizontalLayout_85.setSpacing(0)
        self.horizontalLayout_85.setObjectName(u"horizontalLayout_85")
        self.horizontalLayout_85.setContentsMargins(0, 0, 0, 0)
        self.label_add_tests_i2c_param_9 = QLabel(self.frame_add_tests_i2c_param_9)
        self.label_add_tests_i2c_param_9.setObjectName(u"label_add_tests_i2c_param_9")
        sizePolicy43.setHeightForWidth(self.label_add_tests_i2c_param_9.sizePolicy().hasHeightForWidth())
        self.label_add_tests_i2c_param_9.setSizePolicy(sizePolicy43)
        self.label_add_tests_i2c_param_9.setFont(font10)
        self.label_add_tests_i2c_param_9.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_85.addWidget(self.label_add_tests_i2c_param_9)

        self.lineedit_add_tests_i2c_param_9 = QLineEdit(self.frame_add_tests_i2c_param_9)
        self.lineedit_add_tests_i2c_param_9.setObjectName(u"lineedit_add_tests_i2c_param_9")
        self.lineedit_add_tests_i2c_param_9.setEnabled(True)
        sizePolicy44.setHeightForWidth(self.lineedit_add_tests_i2c_param_9.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_i2c_param_9.setSizePolicy(sizePolicy44)
        self.lineedit_add_tests_i2c_param_9.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_i2c_param_9.setMaximumSize(QSize(100, 16777215))
        self.lineedit_add_tests_i2c_param_9.setFont(font10)
        self.lineedit_add_tests_i2c_param_9.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.horizontalLayout_85.addWidget(self.lineedit_add_tests_i2c_param_9)


        self.gridLayout_12.addWidget(self.frame_add_tests_i2c_param_9, 4, 0, 1, 1)

        self.frame_add_tests_i2c_param_10 = QFrame(self.frame_28)
        self.frame_add_tests_i2c_param_10.setObjectName(u"frame_add_tests_i2c_param_10")
        self.frame_add_tests_i2c_param_10.setStyleSheet(u"")
        self.frame_add_tests_i2c_param_10.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_i2c_param_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_86 = QHBoxLayout(self.frame_add_tests_i2c_param_10)
        self.horizontalLayout_86.setSpacing(0)
        self.horizontalLayout_86.setObjectName(u"horizontalLayout_86")
        self.horizontalLayout_86.setContentsMargins(10, 0, 0, 0)
        self.label_add_tests_i2c_param_10 = QLabel(self.frame_add_tests_i2c_param_10)
        self.label_add_tests_i2c_param_10.setObjectName(u"label_add_tests_i2c_param_10")
        sizePolicy43.setHeightForWidth(self.label_add_tests_i2c_param_10.sizePolicy().hasHeightForWidth())
        self.label_add_tests_i2c_param_10.setSizePolicy(sizePolicy43)
        self.label_add_tests_i2c_param_10.setFont(font10)
        self.label_add_tests_i2c_param_10.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_86.addWidget(self.label_add_tests_i2c_param_10)

        self.lineedit_add_tests_i2c_param_10 = QLineEdit(self.frame_add_tests_i2c_param_10)
        self.lineedit_add_tests_i2c_param_10.setObjectName(u"lineedit_add_tests_i2c_param_10")
        self.lineedit_add_tests_i2c_param_10.setEnabled(True)
        sizePolicy44.setHeightForWidth(self.lineedit_add_tests_i2c_param_10.sizePolicy().hasHeightForWidth())
        self.lineedit_add_tests_i2c_param_10.setSizePolicy(sizePolicy44)
        self.lineedit_add_tests_i2c_param_10.setMinimumSize(QSize(100, 30))
        self.lineedit_add_tests_i2c_param_10.setMaximumSize(QSize(100, 16777215))
        self.lineedit_add_tests_i2c_param_10.setFont(font10)
        self.lineedit_add_tests_i2c_param_10.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.horizontalLayout_86.addWidget(self.lineedit_add_tests_i2c_param_10)


        self.gridLayout_12.addWidget(self.frame_add_tests_i2c_param_10, 4, 1, 1, 1)


        self.verticalLayout_94.addWidget(self.frame_28)


        self.horizontalLayout_70.addWidget(self.frame_add_tests_i2c)

        self.stackedwidget_add_tests_middle.addWidget(self.page_add_tests_sp3_i2c)

        self.verticalLayout_78.addWidget(self.stackedwidget_add_tests_middle)

        self.frame_add_tests_usbpd_options = QFrame(self.frame_add_tests_middle)
        self.frame_add_tests_usbpd_options.setObjectName(u"frame_add_tests_usbpd_options")
        sizePolicy8.setHeightForWidth(self.frame_add_tests_usbpd_options.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_usbpd_options.setSizePolicy(sizePolicy8)
        self.frame_add_tests_usbpd_options.setMinimumSize(QSize(0, 0))
        self.frame_add_tests_usbpd_options.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(39, 44, 54);\n"
"	border-radius: 5px;\n"
"};")
        self.frame_add_tests_usbpd_options.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_usbpd_options.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_30 = QHBoxLayout(self.frame_add_tests_usbpd_options)
        self.horizontalLayout_30.setSpacing(0)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.frame_add_tests_usbpd_checkboxes = QFrame(self.frame_add_tests_usbpd_options)
        self.frame_add_tests_usbpd_checkboxes.setObjectName(u"frame_add_tests_usbpd_checkboxes")
        sizePolicy46 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy46.setHorizontalStretch(5)
        sizePolicy46.setVerticalStretch(0)
        sizePolicy46.setHeightForWidth(self.frame_add_tests_usbpd_checkboxes.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_usbpd_checkboxes.setSizePolicy(sizePolicy46)
        self.frame_add_tests_usbpd_checkboxes.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_usbpd_checkboxes.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_add_tests_usbpd_checkboxes)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.vspacer_add_tests_usbpd_5 = QSpacerItem(20, 12, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.vspacer_add_tests_usbpd_5, 0, 0, 1, 2)

        self.vspacer_add_tests_usbpd_4 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.vspacer_add_tests_usbpd_4, 6, 0, 1, 2)

        self.chkbox_add_tests_measure_scope_ripple = QCheckBox(self.frame_add_tests_usbpd_checkboxes)
        self.chkbox_add_tests_measure_scope_ripple.setObjectName(u"chkbox_add_tests_measure_scope_ripple")
        sizePolicy19.setHeightForWidth(self.chkbox_add_tests_measure_scope_ripple.sizePolicy().hasHeightForWidth())
        self.chkbox_add_tests_measure_scope_ripple.setSizePolicy(sizePolicy19)
        self.chkbox_add_tests_measure_scope_ripple.setFont(font10)
        self.chkbox_add_tests_measure_scope_ripple.setLayoutDirection(Qt.LeftToRight)
        self.chkbox_add_tests_measure_scope_ripple.setAutoFillBackground(False)
        self.chkbox_add_tests_measure_scope_ripple.setStyleSheet(u"QCheckBox:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.chkbox_add_tests_measure_scope_ripple.setChecked(False)
        self.chkbox_add_tests_measure_scope_ripple.setTristate(False)

        self.gridLayout_9.addWidget(self.chkbox_add_tests_measure_scope_ripple, 3, 0, 1, 1)

        self.frame_add_tests_eload_type = QFrame(self.frame_add_tests_usbpd_checkboxes)
        self.frame_add_tests_eload_type.setObjectName(u"frame_add_tests_eload_type")
        sizePolicy37.setHeightForWidth(self.frame_add_tests_eload_type.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_eload_type.setSizePolicy(sizePolicy37)
        self.frame_add_tests_eload_type.setMinimumSize(QSize(0, 0))
        self.frame_add_tests_eload_type.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_eload_type.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_90 = QHBoxLayout(self.frame_add_tests_eload_type)
        self.horizontalLayout_90.setSpacing(0)
        self.horizontalLayout_90.setObjectName(u"horizontalLayout_90")
        self.horizontalLayout_90.setContentsMargins(0, 0, 0, 0)
        self.label_add_tests_eload_type = QLabel(self.frame_add_tests_eload_type)
        self.label_add_tests_eload_type.setObjectName(u"label_add_tests_eload_type")
        self.label_add_tests_eload_type.setFont(font10)
        self.label_add_tests_eload_type.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.horizontalLayout_90.addWidget(self.label_add_tests_eload_type)

        self.cbx_add_tests_load_range_eload_type = QComboBox(self.frame_add_tests_eload_type)
        self.cbx_add_tests_load_range_eload_type.setObjectName(u"cbx_add_tests_load_range_eload_type")
        self.cbx_add_tests_load_range_eload_type.setEnabled(True)
        sizePolicy25.setHeightForWidth(self.cbx_add_tests_load_range_eload_type.sizePolicy().hasHeightForWidth())
        self.cbx_add_tests_load_range_eload_type.setSizePolicy(sizePolicy25)
        self.cbx_add_tests_load_range_eload_type.setMinimumSize(QSize(0, 30))
        self.cbx_add_tests_load_range_eload_type.setMaximumSize(QSize(16777215, 30))
        self.cbx_add_tests_load_range_eload_type.setFont(font10)
        self.cbx_add_tests_load_range_eload_type.setStyleSheet(u"QComboBox:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}")

        self.horizontalLayout_90.addWidget(self.cbx_add_tests_load_range_eload_type)


        self.gridLayout_9.addWidget(self.frame_add_tests_eload_type, 1, 0, 1, 2)

        self.chkbox_add_tests_eload_measurement = QCheckBox(self.frame_add_tests_usbpd_checkboxes)
        self.chkbox_add_tests_eload_measurement.setObjectName(u"chkbox_add_tests_eload_measurement")
        sizePolicy19.setHeightForWidth(self.chkbox_add_tests_eload_measurement.sizePolicy().hasHeightForWidth())
        self.chkbox_add_tests_eload_measurement.setSizePolicy(sizePolicy19)
        self.chkbox_add_tests_eload_measurement.setFont(font10)
        self.chkbox_add_tests_eload_measurement.setLayoutDirection(Qt.LeftToRight)
        self.chkbox_add_tests_eload_measurement.setAutoFillBackground(False)
        self.chkbox_add_tests_eload_measurement.setStyleSheet(u"QCheckBox:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.chkbox_add_tests_eload_measurement.setChecked(False)
        self.chkbox_add_tests_eload_measurement.setTristate(False)

        self.gridLayout_9.addWidget(self.chkbox_add_tests_eload_measurement, 2, 0, 1, 1)

        self.vspacer_add_tests_usbpd_2 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.gridLayout_9.addItem(self.vspacer_add_tests_usbpd_2, 2, 1, 4, 1)


        self.horizontalLayout_30.addWidget(self.frame_add_tests_usbpd_checkboxes)

        self.frame_add_tests_pdo_tests = QFrame(self.frame_add_tests_usbpd_options)
        self.frame_add_tests_pdo_tests.setObjectName(u"frame_add_tests_pdo_tests")
        sizePolicy18.setHeightForWidth(self.frame_add_tests_pdo_tests.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_pdo_tests.setSizePolicy(sizePolicy18)
        self.frame_add_tests_pdo_tests.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_pdo_tests.setFrameShadow(QFrame.Raised)
        self.verticalLayout_86 = QVBoxLayout(self.frame_add_tests_pdo_tests)
        self.verticalLayout_86.setObjectName(u"verticalLayout_86")
        self.vspacer_add_tests_usbpd_6 = QSpacerItem(20, 12, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_86.addItem(self.vspacer_add_tests_usbpd_6)

        self.btn_add_tests_option_1 = QPushButton(self.frame_add_tests_pdo_tests)
        self.btn_add_tests_option_1.setObjectName(u"btn_add_tests_option_1")
        self.btn_add_tests_option_1.setMinimumSize(QSize(150, 30))
        self.btn_add_tests_option_1.setFont(font13)
        self.btn_add_tests_option_1.setStyleSheet(u"QPushButton {\n"
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
        icon16 = QIcon()
        icon16.addFile(u":/16x16/icons/16x16/cil-plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_option_1.setIcon(icon16)

        self.verticalLayout_86.addWidget(self.btn_add_tests_option_1)

        self.vspacer_add_tests_usbpd_7 = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.verticalLayout_86.addItem(self.vspacer_add_tests_usbpd_7)

        self.btn_add_tests_option_2 = QPushButton(self.frame_add_tests_pdo_tests)
        self.btn_add_tests_option_2.setObjectName(u"btn_add_tests_option_2")
        self.btn_add_tests_option_2.setMinimumSize(QSize(150, 30))
        self.btn_add_tests_option_2.setFont(font13)
        self.btn_add_tests_option_2.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_option_2.setIcon(icon12)

        self.verticalLayout_86.addWidget(self.btn_add_tests_option_2)

        self.vspacer_add_tests_usbpd_3 = QSpacerItem(20, 12, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_86.addItem(self.vspacer_add_tests_usbpd_3)


        self.horizontalLayout_30.addWidget(self.frame_add_tests_pdo_tests)


        self.verticalLayout_78.addWidget(self.frame_add_tests_usbpd_options)


        self.horizontalLayout_60.addWidget(self.frame_add_tests_middle)

        self.frame_add_tests_right = QFrame(self.frame_add_tests_maincontent)
        self.frame_add_tests_right.setObjectName(u"frame_add_tests_right")
        sizePolicy41.setHeightForWidth(self.frame_add_tests_right.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_right.setSizePolicy(sizePolicy41)
        self.frame_add_tests_right.setMinimumSize(QSize(600, 0))
        self.frame_add_tests_right.setMaximumSize(QSize(16777215, 16777215))
        self.frame_add_tests_right.setStyleSheet(u"")
        self.frame_add_tests_right.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_right.setFrameShadow(QFrame.Raised)
        self.verticalLayout_88 = QVBoxLayout(self.frame_add_tests_right)
        self.verticalLayout_88.setObjectName(u"verticalLayout_88")
        self.verticalLayout_88.setContentsMargins(0, 6, 6, 0)
        self.frame_add_tests_test_list_container = QFrame(self.frame_add_tests_right)
        self.frame_add_tests_test_list_container.setObjectName(u"frame_add_tests_test_list_container")
        self.frame_add_tests_test_list_container.setMinimumSize(QSize(0, 50))
        self.frame_add_tests_test_list_container.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(39, 44, 54);\n"
"	border-radius: 5px;\n"
"};")
        self.frame_add_tests_test_list_container.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_test_list_container.setFrameShadow(QFrame.Raised)
        self.verticalLayout_49 = QVBoxLayout(self.frame_add_tests_test_list_container)
        self.verticalLayout_49.setObjectName(u"verticalLayout_49")
        self.verticalLayout_49.setContentsMargins(0, 0, 0, 0)
        self.frame_add_tests_test_list_table = QFrame(self.frame_add_tests_test_list_container)
        self.frame_add_tests_test_list_table.setObjectName(u"frame_add_tests_test_list_table")
        self.frame_add_tests_test_list_table.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.frame_add_tests_test_list_table.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_test_list_table.setSizePolicy(sizePolicy5)
        self.frame_add_tests_test_list_table.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_test_list_table.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_add_tests_test_list_table)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.frame_add_tests_test_list_table_buttons = QFrame(self.frame_add_tests_test_list_table)
        self.frame_add_tests_test_list_table_buttons.setObjectName(u"frame_add_tests_test_list_table_buttons")
        sizePolicy47 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        sizePolicy47.setHorizontalStretch(0)
        sizePolicy47.setVerticalStretch(0)
        sizePolicy47.setHeightForWidth(self.frame_add_tests_test_list_table_buttons.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_test_list_table_buttons.setSizePolicy(sizePolicy47)
        self.frame_add_tests_test_list_table_buttons.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_test_list_table_buttons.setFrameShadow(QFrame.Raised)
        self.verticalLayout_91 = QVBoxLayout(self.frame_add_tests_test_list_table_buttons)
        self.verticalLayout_91.setObjectName(u"verticalLayout_91")
        self.btn_add_tests_test_item_move_top = QPushButton(self.frame_add_tests_test_list_table_buttons)
        self.btn_add_tests_test_item_move_top.setObjectName(u"btn_add_tests_test_item_move_top")
        sizePolicy48 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy48.setHorizontalStretch(1)
        sizePolicy48.setVerticalStretch(0)
        sizePolicy48.setHeightForWidth(self.btn_add_tests_test_item_move_top.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_test_item_move_top.setSizePolicy(sizePolicy48)
        self.btn_add_tests_test_item_move_top.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_test_item_move_top.setFont(font13)
        self.btn_add_tests_test_item_move_top.setStyleSheet(u"QPushButton {\n"
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
        icon17 = QIcon()
        icon17.addFile(u":/16x16/icons/16x16/cil-chevron-double-up.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_test_item_move_top.setIcon(icon17)

        self.verticalLayout_91.addWidget(self.btn_add_tests_test_item_move_top)

        self.btn_add_tests_test_item_move_up = QPushButton(self.frame_add_tests_test_list_table_buttons)
        self.btn_add_tests_test_item_move_up.setObjectName(u"btn_add_tests_test_item_move_up")
        sizePolicy48.setHeightForWidth(self.btn_add_tests_test_item_move_up.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_test_item_move_up.setSizePolicy(sizePolicy48)
        self.btn_add_tests_test_item_move_up.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_test_item_move_up.setFont(font13)
        self.btn_add_tests_test_item_move_up.setStyleSheet(u"QPushButton {\n"
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
        icon18 = QIcon()
        icon18.addFile(u":/16x16/icons/16x16/cil-chevron-top.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_test_item_move_up.setIcon(icon18)

        self.verticalLayout_91.addWidget(self.btn_add_tests_test_item_move_up)

        self.btn_add_tests_test_item_move_down = QPushButton(self.frame_add_tests_test_list_table_buttons)
        self.btn_add_tests_test_item_move_down.setObjectName(u"btn_add_tests_test_item_move_down")
        sizePolicy48.setHeightForWidth(self.btn_add_tests_test_item_move_down.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_test_item_move_down.setSizePolicy(sizePolicy48)
        self.btn_add_tests_test_item_move_down.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_test_item_move_down.setFont(font13)
        self.btn_add_tests_test_item_move_down.setStyleSheet(u"QPushButton {\n"
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
        icon19 = QIcon()
        icon19.addFile(u":/16x16/icons/16x16/cil-chevron-bottom.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_test_item_move_down.setIcon(icon19)

        self.verticalLayout_91.addWidget(self.btn_add_tests_test_item_move_down)

        self.btn_add_tests_test_item_move_bottom = QPushButton(self.frame_add_tests_test_list_table_buttons)
        self.btn_add_tests_test_item_move_bottom.setObjectName(u"btn_add_tests_test_item_move_bottom")
        sizePolicy48.setHeightForWidth(self.btn_add_tests_test_item_move_bottom.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_test_item_move_bottom.setSizePolicy(sizePolicy48)
        self.btn_add_tests_test_item_move_bottom.setMinimumSize(QSize(0, 30))
        self.btn_add_tests_test_item_move_bottom.setFont(font13)
        self.btn_add_tests_test_item_move_bottom.setStyleSheet(u"QPushButton {\n"
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
        icon20 = QIcon()
        icon20.addFile(u":/16x16/icons/16x16/cil-chevron-double-down.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_test_item_move_bottom.setIcon(icon20)

        self.verticalLayout_91.addWidget(self.btn_add_tests_test_item_move_bottom)


        self.gridLayout_8.addWidget(self.frame_add_tests_test_list_table_buttons, 1, 1, 1, 1)

        self.frame_add_tests_test_list_title = QFrame(self.frame_add_tests_test_list_table)
        self.frame_add_tests_test_list_title.setObjectName(u"frame_add_tests_test_list_title")
        self.frame_add_tests_test_list_title.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_test_list_title.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_63 = QHBoxLayout(self.frame_add_tests_test_list_title)
        self.horizontalLayout_63.setObjectName(u"horizontalLayout_63")
        self.hspacer_add_tests_test_list_title = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_63.addItem(self.hspacer_add_tests_test_list_title)

        self.label_add_tests_test_list = QLabel(self.frame_add_tests_test_list_title)
        self.label_add_tests_test_list.setObjectName(u"label_add_tests_test_list")
        sizePolicy2.setHeightForWidth(self.label_add_tests_test_list.sizePolicy().hasHeightForWidth())
        self.label_add_tests_test_list.setSizePolicy(sizePolicy2)
        font18 = QFont()
        font18.setFamily(u"Segoe UI")
        font18.setPointSize(16)
        font18.setBold(True)
        font18.setWeight(75)
        self.label_add_tests_test_list.setFont(font18)
        self.label_add_tests_test_list.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_add_tests_test_list.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_63.addWidget(self.label_add_tests_test_list)

        self.frame_add_tests_save_load_test_plan = QFrame(self.frame_add_tests_test_list_title)
        self.frame_add_tests_save_load_test_plan.setObjectName(u"frame_add_tests_save_load_test_plan")
        sizePolicy45.setHeightForWidth(self.frame_add_tests_save_load_test_plan.sizePolicy().hasHeightForWidth())
        self.frame_add_tests_save_load_test_plan.setSizePolicy(sizePolicy45)
        self.frame_add_tests_save_load_test_plan.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_save_load_test_plan.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_62 = QHBoxLayout(self.frame_add_tests_save_load_test_plan)
        self.horizontalLayout_62.setObjectName(u"horizontalLayout_62")
        self.btn_add_tests_save_test_plan = QPushButton(self.frame_add_tests_save_load_test_plan)
        self.btn_add_tests_save_test_plan.setObjectName(u"btn_add_tests_save_test_plan")
        sizePolicy19.setHeightForWidth(self.btn_add_tests_save_test_plan.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_save_test_plan.setSizePolicy(sizePolicy19)
        self.btn_add_tests_save_test_plan.setMinimumSize(QSize(100, 30))
        self.btn_add_tests_save_test_plan.setFont(font13)
        self.btn_add_tests_save_test_plan.setStyleSheet(u"QPushButton {\n"
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
        icon21 = QIcon()
        icon21.addFile(u":/20x20/icons/20x20/cil-save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_save_test_plan.setIcon(icon21)

        self.horizontalLayout_62.addWidget(self.btn_add_tests_save_test_plan)

        self.btn_add_tests_load_test_plan = QPushButton(self.frame_add_tests_save_load_test_plan)
        self.btn_add_tests_load_test_plan.setObjectName(u"btn_add_tests_load_test_plan")
        sizePolicy19.setHeightForWidth(self.btn_add_tests_load_test_plan.sizePolicy().hasHeightForWidth())
        self.btn_add_tests_load_test_plan.setSizePolicy(sizePolicy19)
        self.btn_add_tests_load_test_plan.setMinimumSize(QSize(100, 30))
        self.btn_add_tests_load_test_plan.setFont(font13)
        self.btn_add_tests_load_test_plan.setStyleSheet(u"QPushButton {\n"
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
        icon22 = QIcon()
        icon22.addFile(u":/20x20/icons/20x20/cil-vertical-align-bottom.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_load_test_plan.setIcon(icon22)

        self.horizontalLayout_62.addWidget(self.btn_add_tests_load_test_plan)


        self.horizontalLayout_63.addWidget(self.frame_add_tests_save_load_test_plan)


        self.gridLayout_8.addWidget(self.frame_add_tests_test_list_title, 0, 0, 1, 2)

        self.table_add_tests_test_list = QTableWidget(self.frame_add_tests_test_list_table)
        if (self.table_add_tests_test_list.columnCount() < 2):
            self.table_add_tests_test_list.setColumnCount(2)
        __qtablewidgetitem24 = QTableWidgetItem()
        __qtablewidgetitem24.setFont(font10);
        self.table_add_tests_test_list.setHorizontalHeaderItem(0, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        __qtablewidgetitem25.setFont(font10);
        self.table_add_tests_test_list.setHorizontalHeaderItem(1, __qtablewidgetitem25)
        if (self.table_add_tests_test_list.rowCount() < 3):
            self.table_add_tests_test_list.setRowCount(3)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.table_add_tests_test_list.setItem(0, 0, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.table_add_tests_test_list.setItem(1, 0, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.table_add_tests_test_list.setItem(2, 0, __qtablewidgetitem28)
        self.table_add_tests_test_list.setObjectName(u"table_add_tests_test_list")
        sizePolicy1.setHeightForWidth(self.table_add_tests_test_list.sizePolicy().hasHeightForWidth())
        self.table_add_tests_test_list.setSizePolicy(sizePolicy1)
        palette5 = QPalette()
        palette5.setBrush(QPalette.Active, QPalette.WindowText, brush6)
        palette5.setBrush(QPalette.Active, QPalette.Button, brush15)
        palette5.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette5.setBrush(QPalette.Active, QPalette.ButtonText, brush6)
        palette5.setBrush(QPalette.Active, QPalette.Base, brush15)
        palette5.setBrush(QPalette.Active, QPalette.Window, brush15)
        brush35 = QBrush(QColor(210, 210, 210, 128))
        brush35.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette5.setBrush(QPalette.Active, QPalette.PlaceholderText, brush35)
#endif
        palette5.setBrush(QPalette.Inactive, QPalette.WindowText, brush6)
        palette5.setBrush(QPalette.Inactive, QPalette.Button, brush15)
        palette5.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette5.setBrush(QPalette.Inactive, QPalette.ButtonText, brush6)
        palette5.setBrush(QPalette.Inactive, QPalette.Base, brush15)
        palette5.setBrush(QPalette.Inactive, QPalette.Window, brush15)
        brush36 = QBrush(QColor(210, 210, 210, 128))
        brush36.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette5.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush36)
#endif
        palette5.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette5.setBrush(QPalette.Disabled, QPalette.Button, brush15)
        palette5.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette5.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette5.setBrush(QPalette.Disabled, QPalette.Base, brush15)
        palette5.setBrush(QPalette.Disabled, QPalette.Window, brush15)
        brush37 = QBrush(QColor(210, 210, 210, 128))
        brush37.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette5.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush37)
#endif
        self.table_add_tests_test_list.setPalette(palette5)
        font19 = QFont()
        font19.setPointSize(10)
        self.table_add_tests_test_list.setFont(font19)
        self.table_add_tests_test_list.setStyleSheet(u"QTableWidget {	\n"
"	background-color: rgb(39, 44, 54);\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
"\n"
"QHeaderView::section{\n"
"	background-color: rgb(39, 44, 54);\n"
"\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWid"
                        "get::horizontalHeader {	\n"
"	background-color: rgb(81, 255, 0);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"")
        self.table_add_tests_test_list.setFrameShape(QFrame.NoFrame)
        self.table_add_tests_test_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table_add_tests_test_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_add_tests_test_list.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.table_add_tests_test_list.setAutoScroll(True)
        self.table_add_tests_test_list.setAutoScrollMargin(50)
        self.table_add_tests_test_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_add_tests_test_list.setAlternatingRowColors(False)
        self.table_add_tests_test_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_add_tests_test_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_add_tests_test_list.setShowGrid(True)
        self.table_add_tests_test_list.setGridStyle(Qt.SolidLine)
        self.table_add_tests_test_list.setSortingEnabled(False)
        self.table_add_tests_test_list.setCornerButtonEnabled(True)
        self.table_add_tests_test_list.setRowCount(3)
        self.table_add_tests_test_list.horizontalHeader().setVisible(False)
        self.table_add_tests_test_list.horizontalHeader().setCascadingSectionResizes(True)
        self.table_add_tests_test_list.horizontalHeader().setMinimumSectionSize(100)
        self.table_add_tests_test_list.horizontalHeader().setDefaultSectionSize(100)
        self.table_add_tests_test_list.horizontalHeader().setProperty("showSortIndicator", False)
        self.table_add_tests_test_list.horizontalHeader().setStretchLastSection(True)
        self.table_add_tests_test_list.verticalHeader().setVisible(False)
        self.table_add_tests_test_list.verticalHeader().setCascadingSectionResizes(True)
        self.table_add_tests_test_list.verticalHeader().setMinimumSectionSize(50)
        self.table_add_tests_test_list.verticalHeader().setDefaultSectionSize(135)
        self.table_add_tests_test_list.verticalHeader().setHighlightSections(True)
        self.table_add_tests_test_list.verticalHeader().setProperty("showSortIndicator", True)
        self.table_add_tests_test_list.verticalHeader().setStretchLastSection(False)

        self.gridLayout_8.addWidget(self.table_add_tests_test_list, 1, 0, 1, 1)


        self.verticalLayout_49.addWidget(self.frame_add_tests_test_list_table)


        self.verticalLayout_88.addWidget(self.frame_add_tests_test_list_container)

        self.frame_add_tests_test_list_buttons = QFrame(self.frame_add_tests_right)
        self.frame_add_tests_test_list_buttons.setObjectName(u"frame_add_tests_test_list_buttons")
        self.frame_add_tests_test_list_buttons.setMinimumSize(QSize(0, 100))
        self.frame_add_tests_test_list_buttons.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(39, 44, 54);\n"
"	border-radius: 5px;\n"
"};")
        self.frame_add_tests_test_list_buttons.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_test_list_buttons.setFrameShadow(QFrame.Raised)
        self.verticalLayout_50 = QVBoxLayout(self.frame_add_tests_test_list_buttons)
        self.verticalLayout_50.setObjectName(u"verticalLayout_50")
        self.frame_add_tests_selected = QFrame(self.frame_add_tests_test_list_buttons)
        self.frame_add_tests_selected.setObjectName(u"frame_add_tests_selected")
        self.frame_add_tests_selected.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_selected.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_58 = QHBoxLayout(self.frame_add_tests_selected)
        self.horizontalLayout_58.setObjectName(u"horizontalLayout_58")
        self.btn_add_tests_restart_selected_test = QPushButton(self.frame_add_tests_selected)
        self.btn_add_tests_restart_selected_test.setObjectName(u"btn_add_tests_restart_selected_test")
        self.btn_add_tests_restart_selected_test.setMinimumSize(QSize(130, 30))
        self.btn_add_tests_restart_selected_test.setFont(font13)
        self.btn_add_tests_restart_selected_test.setStyleSheet(u"QPushButton {\n"
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
        icon23 = QIcon()
        icon23.addFile(u":/20x20/icons/20x20/cil-reload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_restart_selected_test.setIcon(icon23)

        self.horizontalLayout_58.addWidget(self.btn_add_tests_restart_selected_test)

        self.btn_add_tests_update_selected_test = QPushButton(self.frame_add_tests_selected)
        self.btn_add_tests_update_selected_test.setObjectName(u"btn_add_tests_update_selected_test")
        self.btn_add_tests_update_selected_test.setMinimumSize(QSize(130, 30))
        self.btn_add_tests_update_selected_test.setFont(font13)
        self.btn_add_tests_update_selected_test.setStyleSheet(u"QPushButton {\n"
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
        icon24 = QIcon()
        icon24.addFile(u":/16x16/icons/16x16/cil-data-transfer-up.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_update_selected_test.setIcon(icon24)

        self.horizontalLayout_58.addWidget(self.btn_add_tests_update_selected_test)

        self.btn_add_tests_remove_selected_test = QPushButton(self.frame_add_tests_selected)
        self.btn_add_tests_remove_selected_test.setObjectName(u"btn_add_tests_remove_selected_test")
        self.btn_add_tests_remove_selected_test.setMinimumSize(QSize(130, 30))
        self.btn_add_tests_remove_selected_test.setFont(font13)
        self.btn_add_tests_remove_selected_test.setStyleSheet(u"QPushButton {\n"
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
        icon25 = QIcon()
        icon25.addFile(u":/16x16/icons/16x16/cil-minus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_remove_selected_test.setIcon(icon25)

        self.horizontalLayout_58.addWidget(self.btn_add_tests_remove_selected_test)

        self.btn_add_tests_skip_selected_test = QPushButton(self.frame_add_tests_selected)
        self.btn_add_tests_skip_selected_test.setObjectName(u"btn_add_tests_skip_selected_test")
        self.btn_add_tests_skip_selected_test.setMinimumSize(QSize(130, 30))
        self.btn_add_tests_skip_selected_test.setFont(font13)
        self.btn_add_tests_skip_selected_test.setStyleSheet(u"QPushButton {\n"
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
        icon26 = QIcon()
        icon26.addFile(u":/16x16/icons/16x16/cil-media-skip-forward.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_skip_selected_test.setIcon(icon26)

        self.horizontalLayout_58.addWidget(self.btn_add_tests_skip_selected_test)


        self.verticalLayout_50.addWidget(self.frame_add_tests_selected)

        self.frame_add_tests_selected_all = QFrame(self.frame_add_tests_test_list_buttons)
        self.frame_add_tests_selected_all.setObjectName(u"frame_add_tests_selected_all")
        self.frame_add_tests_selected_all.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_selected_all.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_32 = QHBoxLayout(self.frame_add_tests_selected_all)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.btn_add_tests_restart_all_test = QPushButton(self.frame_add_tests_selected_all)
        self.btn_add_tests_restart_all_test.setObjectName(u"btn_add_tests_restart_all_test")
        self.btn_add_tests_restart_all_test.setMinimumSize(QSize(150, 30))
        self.btn_add_tests_restart_all_test.setFont(font13)
        self.btn_add_tests_restart_all_test.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_restart_all_test.setIcon(icon23)

        self.horizontalLayout_32.addWidget(self.btn_add_tests_restart_all_test)

        self.btn_add_tests_clear_all_test = QPushButton(self.frame_add_tests_selected_all)
        self.btn_add_tests_clear_all_test.setObjectName(u"btn_add_tests_clear_all_test")
        self.btn_add_tests_clear_all_test.setMinimumSize(QSize(150, 30))
        self.btn_add_tests_clear_all_test.setFont(font13)
        self.btn_add_tests_clear_all_test.setStyleSheet(u"QPushButton {\n"
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
        self.btn_add_tests_clear_all_test.setIcon(icon15)

        self.horizontalLayout_32.addWidget(self.btn_add_tests_clear_all_test)


        self.verticalLayout_50.addWidget(self.frame_add_tests_selected_all)

        self.frame_add_tests_run_stop = QFrame(self.frame_add_tests_test_list_buttons)
        self.frame_add_tests_run_stop.setObjectName(u"frame_add_tests_run_stop")
        self.frame_add_tests_run_stop.setFrameShape(QFrame.StyledPanel)
        self.frame_add_tests_run_stop.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_59 = QHBoxLayout(self.frame_add_tests_run_stop)
        self.horizontalLayout_59.setObjectName(u"horizontalLayout_59")
        self.btn_add_tests_run = QPushButton(self.frame_add_tests_run_stop)
        self.btn_add_tests_run.setObjectName(u"btn_add_tests_run")
        self.btn_add_tests_run.setMinimumSize(QSize(150, 60))
        self.btn_add_tests_run.setFont(font13)
        self.btn_add_tests_run.setStyleSheet(u"QPushButton {\n"
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
        icon27 = QIcon()
        icon27.addFile(u":/20x20/icons/20x20/cil-media-play.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_run.setIcon(icon27)

        self.horizontalLayout_59.addWidget(self.btn_add_tests_run)

        self.btn_add_tests_stop = QPushButton(self.frame_add_tests_run_stop)
        self.btn_add_tests_stop.setObjectName(u"btn_add_tests_stop")
        self.btn_add_tests_stop.setMinimumSize(QSize(150, 60))
        self.btn_add_tests_stop.setFont(font13)
        self.btn_add_tests_stop.setStyleSheet(u"QPushButton {\n"
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
        icon28 = QIcon()
        icon28.addFile(u":/16x16/icons/16x16/cil-media-stop.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_tests_stop.setIcon(icon28)

        self.horizontalLayout_59.addWidget(self.btn_add_tests_stop)


        self.verticalLayout_50.addWidget(self.frame_add_tests_run_stop)


        self.verticalLayout_88.addWidget(self.frame_add_tests_test_list_buttons)


        self.horizontalLayout_60.addWidget(self.frame_add_tests_right)


        self.verticalLayout_89.addWidget(self.frame_add_tests_maincontent)


        self.horizontalLayout_33.addWidget(self.frame_add_tests)

        self.stackedWidget.addWidget(self.page_add_tests)
        self.page_test_results = QWidget()
        self.page_test_results.setObjectName(u"page_test_results")
        self.horizontalLayout_64 = QHBoxLayout(self.page_test_results)
        self.horizontalLayout_64.setSpacing(0)
        self.horizontalLayout_64.setObjectName(u"horizontalLayout_64")
        self.horizontalLayout_64.setContentsMargins(0, 0, 0, 0)
        self.frame_test_results = QFrame(self.page_test_results)
        self.frame_test_results.setObjectName(u"frame_test_results")
        self.frame_test_results.setFrameShape(QFrame.StyledPanel)
        self.frame_test_results.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_66 = QHBoxLayout(self.frame_test_results)
        self.horizontalLayout_66.setObjectName(u"horizontalLayout_66")
        self.frame_test_results_left = QFrame(self.frame_test_results)
        self.frame_test_results_left.setObjectName(u"frame_test_results_left")
        sizePolicy18.setHeightForWidth(self.frame_test_results_left.sizePolicy().hasHeightForWidth())
        self.frame_test_results_left.setSizePolicy(sizePolicy18)
        self.frame_test_results_left.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(39, 44, 54);\n"
"	border-radius: 5px;\n"
"};")
        self.frame_test_results_left.setFrameShape(QFrame.StyledPanel)
        self.frame_test_results_left.setFrameShadow(QFrame.Raised)
        self.verticalLayout_93 = QVBoxLayout(self.frame_test_results_left)
        self.verticalLayout_93.setObjectName(u"verticalLayout_93")
        self.frame_test_results_left_buttons = QFrame(self.frame_test_results_left)
        self.frame_test_results_left_buttons.setObjectName(u"frame_test_results_left_buttons")
        self.frame_test_results_left_buttons.setFrameShape(QFrame.StyledPanel)
        self.frame_test_results_left_buttons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_67 = QHBoxLayout(self.frame_test_results_left_buttons)
        self.horizontalLayout_67.setObjectName(u"horizontalLayout_67")
        self.btn_test_results_show_plots = QPushButton(self.frame_test_results_left_buttons)
        self.btn_test_results_show_plots.setObjectName(u"btn_test_results_show_plots")
        self.btn_test_results_show_plots.setMinimumSize(QSize(150, 50))
        self.btn_test_results_show_plots.setFont(font13)
        self.btn_test_results_show_plots.setStyleSheet(u"QPushButton {\n"
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
        icon29 = QIcon()
        icon29.addFile(u":/20x20/icons/20x20/cil-chart-line.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_test_results_show_plots.setIcon(icon29)

        self.horizontalLayout_67.addWidget(self.btn_test_results_show_plots)

        self.btn_test_results_show_data = QPushButton(self.frame_test_results_left_buttons)
        self.btn_test_results_show_data.setObjectName(u"btn_test_results_show_data")
        self.btn_test_results_show_data.setMinimumSize(QSize(150, 50))
        self.btn_test_results_show_data.setFont(font13)
        self.btn_test_results_show_data.setStyleSheet(u"QPushButton {\n"
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
        icon30 = QIcon()
        icon30.addFile(u":/20x20/icons/20x20/cil-view-module.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_test_results_show_data.setIcon(icon30)

        self.horizontalLayout_67.addWidget(self.btn_test_results_show_data)


        self.verticalLayout_93.addWidget(self.frame_test_results_left_buttons)

        self.stacked_widget_test_results = QStackedWidget(self.frame_test_results_left)
        self.stacked_widget_test_results.setObjectName(u"stacked_widget_test_results")
        self.page_test_results_plots = QWidget()
        self.page_test_results_plots.setObjectName(u"page_test_results_plots")
        self.layout_test_results_plot = QVBoxLayout(self.page_test_results_plots)
        self.layout_test_results_plot.setObjectName(u"layout_test_results_plot")
        self.cbx_test_results_plots = QComboBox(self.page_test_results_plots)
        self.cbx_test_results_plots.setObjectName(u"cbx_test_results_plots")
        sizePolicy32.setHeightForWidth(self.cbx_test_results_plots.sizePolicy().hasHeightForWidth())
        self.cbx_test_results_plots.setSizePolicy(sizePolicy32)
        self.cbx_test_results_plots.setMinimumSize(QSize(0, 40))
        self.cbx_test_results_plots.setMaximumSize(QSize(16777215, 40))
        self.cbx_test_results_plots.setFont(font10)

        self.layout_test_results_plot.addWidget(self.cbx_test_results_plots)

        self.plotwidget_test_results_plots = PlotWidget(self.page_test_results_plots)
        self.plotwidget_test_results_plots.setObjectName(u"plotwidget_test_results_plots")
        sizePolicy49 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy49.setHorizontalStretch(0)
        sizePolicy49.setVerticalStretch(0)
        sizePolicy49.setHeightForWidth(self.plotwidget_test_results_plots.sizePolicy().hasHeightForWidth())
        self.plotwidget_test_results_plots.setSizePolicy(sizePolicy49)
        self.plotwidget_test_results_plots.setStyleSheet(u"")

        self.layout_test_results_plot.addWidget(self.plotwidget_test_results_plots)

        self.stacked_widget_test_results.addWidget(self.page_test_results_plots)
        self.page_test_results_data_table = QWidget()
        self.page_test_results_data_table.setObjectName(u"page_test_results_data_table")
        self.horizontalLayout_68 = QHBoxLayout(self.page_test_results_data_table)
        self.horizontalLayout_68.setObjectName(u"horizontalLayout_68")
        self.table_test_results_data = QTableWidget(self.page_test_results_data_table)
        if (self.table_test_results_data.columnCount() < 7):
            self.table_test_results_data.setColumnCount(7)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.table_test_results_data.setHorizontalHeaderItem(0, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.table_test_results_data.setHorizontalHeaderItem(1, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.table_test_results_data.setHorizontalHeaderItem(2, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.table_test_results_data.setHorizontalHeaderItem(3, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.table_test_results_data.setHorizontalHeaderItem(4, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.table_test_results_data.setHorizontalHeaderItem(5, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.table_test_results_data.setHorizontalHeaderItem(6, __qtablewidgetitem35)
        if (self.table_test_results_data.rowCount() < 3):
            self.table_test_results_data.setRowCount(3)
        self.table_test_results_data.setObjectName(u"table_test_results_data")
        sizePolicy1.setHeightForWidth(self.table_test_results_data.sizePolicy().hasHeightForWidth())
        self.table_test_results_data.setSizePolicy(sizePolicy1)
        palette6 = QPalette()
        palette6.setBrush(QPalette.Active, QPalette.WindowText, brush6)
        palette6.setBrush(QPalette.Active, QPalette.Button, brush15)
        palette6.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette6.setBrush(QPalette.Active, QPalette.ButtonText, brush6)
        palette6.setBrush(QPalette.Active, QPalette.Base, brush15)
        palette6.setBrush(QPalette.Active, QPalette.Window, brush15)
        brush38 = QBrush(QColor(210, 210, 210, 128))
        brush38.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette6.setBrush(QPalette.Active, QPalette.PlaceholderText, brush38)
#endif
        palette6.setBrush(QPalette.Inactive, QPalette.WindowText, brush6)
        palette6.setBrush(QPalette.Inactive, QPalette.Button, brush15)
        palette6.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette6.setBrush(QPalette.Inactive, QPalette.ButtonText, brush6)
        palette6.setBrush(QPalette.Inactive, QPalette.Base, brush15)
        palette6.setBrush(QPalette.Inactive, QPalette.Window, brush15)
        brush39 = QBrush(QColor(210, 210, 210, 128))
        brush39.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette6.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush39)
#endif
        palette6.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette6.setBrush(QPalette.Disabled, QPalette.Button, brush15)
        palette6.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette6.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette6.setBrush(QPalette.Disabled, QPalette.Base, brush15)
        palette6.setBrush(QPalette.Disabled, QPalette.Window, brush15)
        brush40 = QBrush(QColor(210, 210, 210, 128))
        brush40.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette6.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush40)
#endif
        self.table_test_results_data.setPalette(palette6)
        self.table_test_results_data.setFont(font19)
        self.table_test_results_data.setStyleSheet(u"QTableWidget {	\n"
"	background-color: rgb(39, 44, 54);\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
"\n"
"QHeaderView::section{\n"
"	background-color: rgb(39, 44, 54);\n"
"\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWid"
                        "get::horizontalHeader {	\n"
"	background-color: rgb(81, 255, 0);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"")
        self.table_test_results_data.setFrameShape(QFrame.NoFrame)
        self.table_test_results_data.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_test_results_data.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_test_results_data.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.table_test_results_data.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_test_results_data.setAlternatingRowColors(False)
        self.table_test_results_data.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_test_results_data.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_test_results_data.setShowGrid(True)
        self.table_test_results_data.setGridStyle(Qt.SolidLine)
        self.table_test_results_data.setSortingEnabled(False)
        self.table_test_results_data.setCornerButtonEnabled(True)
        self.table_test_results_data.setRowCount(3)
        self.table_test_results_data.horizontalHeader().setVisible(False)
        self.table_test_results_data.horizontalHeader().setCascadingSectionResizes(True)
        self.table_test_results_data.horizontalHeader().setMinimumSectionSize(50)
        self.table_test_results_data.horizontalHeader().setDefaultSectionSize(50)
        self.table_test_results_data.horizontalHeader().setProperty("showSortIndicator", False)
        self.table_test_results_data.horizontalHeader().setStretchLastSection(False)
        self.table_test_results_data.verticalHeader().setVisible(False)
        self.table_test_results_data.verticalHeader().setCascadingSectionResizes(True)
        self.table_test_results_data.verticalHeader().setMinimumSectionSize(20)
        self.table_test_results_data.verticalHeader().setDefaultSectionSize(30)
        self.table_test_results_data.verticalHeader().setHighlightSections(True)
        self.table_test_results_data.verticalHeader().setProperty("showSortIndicator", True)
        self.table_test_results_data.verticalHeader().setStretchLastSection(False)

        self.horizontalLayout_68.addWidget(self.table_test_results_data)

        self.stacked_widget_test_results.addWidget(self.page_test_results_data_table)

        self.verticalLayout_93.addWidget(self.stacked_widget_test_results)


        self.horizontalLayout_66.addWidget(self.frame_test_results_left)

        self.frame_test_results_right = QFrame(self.frame_test_results)
        self.frame_test_results_right.setObjectName(u"frame_test_results_right")
        self.frame_test_results_right.setEnabled(True)
        sizePolicy11.setHeightForWidth(self.frame_test_results_right.sizePolicy().hasHeightForWidth())
        self.frame_test_results_right.setSizePolicy(sizePolicy11)
        self.frame_test_results_right.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(39, 44, 54);\n"
"	border-radius: 5px;\n"
"};")
        self.frame_test_results_right.setFrameShape(QFrame.StyledPanel)
        self.frame_test_results_right.setFrameShadow(QFrame.Raised)
        self.verticalLayout_95 = QVBoxLayout(self.frame_test_results_right)
        self.verticalLayout_95.setObjectName(u"verticalLayout_95")
        self.label_test_results_test_list = QLabel(self.frame_test_results_right)
        self.label_test_results_test_list.setObjectName(u"label_test_results_test_list")
        sizePolicy2.setHeightForWidth(self.label_test_results_test_list.sizePolicy().hasHeightForWidth())
        self.label_test_results_test_list.setSizePolicy(sizePolicy2)
        self.label_test_results_test_list.setFont(font18)
        self.label_test_results_test_list.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_test_results_test_list.setAlignment(Qt.AlignCenter)

        self.verticalLayout_95.addWidget(self.label_test_results_test_list)

        self.table_test_results_test_list = QTableWidget(self.frame_test_results_right)
        if (self.table_test_results_test_list.columnCount() < 2):
            self.table_test_results_test_list.setColumnCount(2)
        __qtablewidgetitem36 = QTableWidgetItem()
        __qtablewidgetitem36.setFont(font10);
        self.table_test_results_test_list.setHorizontalHeaderItem(0, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        __qtablewidgetitem37.setFont(font10);
        self.table_test_results_test_list.setHorizontalHeaderItem(1, __qtablewidgetitem37)
        if (self.table_test_results_test_list.rowCount() < 3):
            self.table_test_results_test_list.setRowCount(3)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.table_test_results_test_list.setItem(0, 0, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.table_test_results_test_list.setItem(1, 0, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.table_test_results_test_list.setItem(2, 0, __qtablewidgetitem40)
        self.table_test_results_test_list.setObjectName(u"table_test_results_test_list")
        sizePolicy1.setHeightForWidth(self.table_test_results_test_list.sizePolicy().hasHeightForWidth())
        self.table_test_results_test_list.setSizePolicy(sizePolicy1)
        palette7 = QPalette()
        palette7.setBrush(QPalette.Active, QPalette.WindowText, brush6)
        palette7.setBrush(QPalette.Active, QPalette.Button, brush15)
        palette7.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette7.setBrush(QPalette.Active, QPalette.ButtonText, brush6)
        palette7.setBrush(QPalette.Active, QPalette.Base, brush15)
        palette7.setBrush(QPalette.Active, QPalette.Window, brush15)
        brush41 = QBrush(QColor(210, 210, 210, 128))
        brush41.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette7.setBrush(QPalette.Active, QPalette.PlaceholderText, brush41)
#endif
        palette7.setBrush(QPalette.Inactive, QPalette.WindowText, brush6)
        palette7.setBrush(QPalette.Inactive, QPalette.Button, brush15)
        palette7.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette7.setBrush(QPalette.Inactive, QPalette.ButtonText, brush6)
        palette7.setBrush(QPalette.Inactive, QPalette.Base, brush15)
        palette7.setBrush(QPalette.Inactive, QPalette.Window, brush15)
        brush42 = QBrush(QColor(210, 210, 210, 128))
        brush42.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette7.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush42)
#endif
        palette7.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette7.setBrush(QPalette.Disabled, QPalette.Button, brush15)
        palette7.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette7.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette7.setBrush(QPalette.Disabled, QPalette.Base, brush15)
        palette7.setBrush(QPalette.Disabled, QPalette.Window, brush15)
        brush43 = QBrush(QColor(210, 210, 210, 128))
        brush43.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette7.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush43)
#endif
        self.table_test_results_test_list.setPalette(palette7)
        self.table_test_results_test_list.setFont(font19)
        self.table_test_results_test_list.setStyleSheet(u"QTableWidget {	\n"
"	background-color: rgb(39, 44, 54);\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
"\n"
"QHeaderView::section{\n"
"	background-color: rgb(39, 44, 54);\n"
"\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWid"
                        "get::horizontalHeader {	\n"
"	background-color: rgb(81, 255, 0);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"")
        self.table_test_results_test_list.setFrameShape(QFrame.NoFrame)
        self.table_test_results_test_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_test_results_test_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_test_results_test_list.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.table_test_results_test_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_test_results_test_list.setAlternatingRowColors(False)
        self.table_test_results_test_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_test_results_test_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_test_results_test_list.setShowGrid(True)
        self.table_test_results_test_list.setGridStyle(Qt.SolidLine)
        self.table_test_results_test_list.setSortingEnabled(False)
        self.table_test_results_test_list.setCornerButtonEnabled(True)
        self.table_test_results_test_list.setRowCount(3)
        self.table_test_results_test_list.horizontalHeader().setVisible(False)
        self.table_test_results_test_list.horizontalHeader().setCascadingSectionResizes(True)
        self.table_test_results_test_list.horizontalHeader().setMinimumSectionSize(100)
        self.table_test_results_test_list.horizontalHeader().setDefaultSectionSize(100)
        self.table_test_results_test_list.horizontalHeader().setProperty("showSortIndicator", False)
        self.table_test_results_test_list.horizontalHeader().setStretchLastSection(True)
        self.table_test_results_test_list.verticalHeader().setVisible(False)
        self.table_test_results_test_list.verticalHeader().setCascadingSectionResizes(True)
        self.table_test_results_test_list.verticalHeader().setMinimumSectionSize(50)
        self.table_test_results_test_list.verticalHeader().setDefaultSectionSize(135)
        self.table_test_results_test_list.verticalHeader().setHighlightSections(True)
        self.table_test_results_test_list.verticalHeader().setProperty("showSortIndicator", True)
        self.table_test_results_test_list.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_95.addWidget(self.table_test_results_test_list)


        self.horizontalLayout_66.addWidget(self.frame_test_results_right)


        self.horizontalLayout_64.addWidget(self.frame_test_results)

        self.stackedWidget.addWidget(self.page_test_results)
        self.page_i2c_controls = QWidget()
        self.page_i2c_controls.setObjectName(u"page_i2c_controls")
        self.gridLayout_17 = QGridLayout(self.page_i2c_controls)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setVerticalSpacing(0)
        self.frame_i2c_controls_ribbon = QFrame(self.page_i2c_controls)
        self.frame_i2c_controls_ribbon.setObjectName(u"frame_i2c_controls_ribbon")
        sizePolicy5.setHeightForWidth(self.frame_i2c_controls_ribbon.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_ribbon.setSizePolicy(sizePolicy5)
        self.frame_i2c_controls_ribbon.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_ribbon.setFrameShadow(QFrame.Raised)
        self.gridLayout_ribbon = QGridLayout(self.frame_i2c_controls_ribbon)
        self.gridLayout_ribbon.setSpacing(0)
        self.gridLayout_ribbon.setObjectName(u"gridLayout_ribbon")
        self.gridLayout_ribbon.setContentsMargins(0, 0, 0, 0)
        self.frame_i2c_controls_eload = QFrame(self.frame_i2c_controls_ribbon)
        self.frame_i2c_controls_eload.setObjectName(u"frame_i2c_controls_eload")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_eload.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_eload.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_eload.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_eload.setFrameShadow(QFrame.Plain)
        self.gridLayout_20 = QGridLayout(self.frame_i2c_controls_eload)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setVerticalSpacing(2)
        self.cbx_i2c_controls_eload_type = QComboBox(self.frame_i2c_controls_eload)
        self.cbx_i2c_controls_eload_type.addItem("")
        self.cbx_i2c_controls_eload_type.addItem("")
        self.cbx_i2c_controls_eload_type.addItem("")
        self.cbx_i2c_controls_eload_type.addItem("")
        self.cbx_i2c_controls_eload_type.setObjectName(u"cbx_i2c_controls_eload_type")
        self.cbx_i2c_controls_eload_type.setMinimumSize(QSize(80, 30))
        self.cbx_i2c_controls_eload_type.setMaximumSize(QSize(16777215, 16777215))
        self.cbx_i2c_controls_eload_type.setFont(font10)
        self.cbx_i2c_controls_eload_type.setStyleSheet(u"QComboBox:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}")

        self.gridLayout_20.addWidget(self.cbx_i2c_controls_eload_type, 2, 0, 1, 1)

        self.frame_i2c_controls_eload_a = QFrame(self.frame_i2c_controls_eload)
        self.frame_i2c_controls_eload_a.setObjectName(u"frame_i2c_controls_eload_a")
        self.frame_i2c_controls_eload_a.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_eload_a.setFrameShadow(QFrame.Raised)
        self.gridLayout_21 = QGridLayout(self.frame_i2c_controls_eload_a)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setVerticalSpacing(6)
        self.gridLayout_21.setContentsMargins(-1, 0, -1, 0)
        self.label_i2c_controls_eload_b_level_unit = QLabel(self.frame_i2c_controls_eload_a)
        self.label_i2c_controls_eload_b_level_unit.setObjectName(u"label_i2c_controls_eload_b_level_unit")
        sizePolicy11.setHeightForWidth(self.label_i2c_controls_eload_b_level_unit.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_eload_b_level_unit.setSizePolicy(sizePolicy11)
        self.label_i2c_controls_eload_b_level_unit.setMaximumSize(QSize(16777215, 16777215))
        self.label_i2c_controls_eload_b_level_unit.setFont(font10)
        self.label_i2c_controls_eload_b_level_unit.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_21.addWidget(self.label_i2c_controls_eload_b_level_unit, 2, 3, 1, 1)

        self.lineedit_i2c_controls_eload_b_level = QLineEdit(self.frame_i2c_controls_eload_a)
        self.lineedit_i2c_controls_eload_b_level.setObjectName(u"lineedit_i2c_controls_eload_b_level")
        sizePolicy15.setHeightForWidth(self.lineedit_i2c_controls_eload_b_level.sizePolicy().hasHeightForWidth())
        self.lineedit_i2c_controls_eload_b_level.setSizePolicy(sizePolicy15)
        self.lineedit_i2c_controls_eload_b_level.setMinimumSize(QSize(50, 30))
        self.lineedit_i2c_controls_eload_b_level.setFont(font10)
        self.lineedit_i2c_controls_eload_b_level.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_21.addWidget(self.lineedit_i2c_controls_eload_b_level, 2, 2, 1, 1)

        self.label_i2c_controls_electronic_load_A = QLabel(self.frame_i2c_controls_eload_a)
        self.label_i2c_controls_electronic_load_A.setObjectName(u"label_i2c_controls_electronic_load_A")
        self.label_i2c_controls_electronic_load_A.setMaximumSize(QSize(16777215, 30))
        self.label_i2c_controls_electronic_load_A.setFont(font10)
        self.label_i2c_controls_electronic_load_A.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_electronic_load_A.setAlignment(Qt.AlignCenter)

        self.gridLayout_21.addWidget(self.label_i2c_controls_electronic_load_A, 1, 0, 1, 1)

        self.label_i2c_controls_eload_a_level_unit = QLabel(self.frame_i2c_controls_eload_a)
        self.label_i2c_controls_eload_a_level_unit.setObjectName(u"label_i2c_controls_eload_a_level_unit")
        sizePolicy11.setHeightForWidth(self.label_i2c_controls_eload_a_level_unit.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_eload_a_level_unit.setSizePolicy(sizePolicy11)
        self.label_i2c_controls_eload_a_level_unit.setMaximumSize(QSize(16777215, 16777215))
        self.label_i2c_controls_eload_a_level_unit.setFont(font10)
        self.label_i2c_controls_eload_a_level_unit.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_21.addWidget(self.label_i2c_controls_eload_a_level_unit, 1, 3, 1, 1)

        self.label_i2c_controls_eload_b = QLabel(self.frame_i2c_controls_eload_a)
        self.label_i2c_controls_eload_b.setObjectName(u"label_i2c_controls_eload_b")
        self.label_i2c_controls_eload_b.setMaximumSize(QSize(16777215, 30))
        self.label_i2c_controls_eload_b.setFont(font10)
        self.label_i2c_controls_eload_b.setLayoutDirection(Qt.LeftToRight)
        self.label_i2c_controls_eload_b.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_eload_b.setAlignment(Qt.AlignCenter)

        self.gridLayout_21.addWidget(self.label_i2c_controls_eload_b, 2, 0, 1, 1)

        self.lineedit_i2c_controls_eload_a_level = QLineEdit(self.frame_i2c_controls_eload_a)
        self.lineedit_i2c_controls_eload_a_level.setObjectName(u"lineedit_i2c_controls_eload_a_level")
        sizePolicy15.setHeightForWidth(self.lineedit_i2c_controls_eload_a_level.sizePolicy().hasHeightForWidth())
        self.lineedit_i2c_controls_eload_a_level.setSizePolicy(sizePolicy15)
        self.lineedit_i2c_controls_eload_a_level.setMinimumSize(QSize(50, 30))
        self.lineedit_i2c_controls_eload_a_level.setFont(font10)
        self.lineedit_i2c_controls_eload_a_level.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_21.addWidget(self.lineedit_i2c_controls_eload_a_level, 1, 2, 1, 1)

        self.btn_i2c_controls_eload_set_B = QPushButton(self.frame_i2c_controls_eload_a)
        self.btn_i2c_controls_eload_set_B.setObjectName(u"btn_i2c_controls_eload_set_B")
        self.btn_i2c_controls_eload_set_B.setMinimumSize(QSize(50, 30))
        self.btn_i2c_controls_eload_set_B.setFont(font4)
        self.btn_i2c_controls_eload_set_B.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_eload_set_B.setCheckable(False)
        self.btn_i2c_controls_eload_set_B.setChecked(False)

        self.gridLayout_21.addWidget(self.btn_i2c_controls_eload_set_B, 2, 5, 1, 1)

        self.btn_i2c_controls_eload_set_A = QPushButton(self.frame_i2c_controls_eload_a)
        self.btn_i2c_controls_eload_set_A.setObjectName(u"btn_i2c_controls_eload_set_A")
        self.btn_i2c_controls_eload_set_A.setMinimumSize(QSize(50, 30))
        self.btn_i2c_controls_eload_set_A.setFont(font4)
        self.btn_i2c_controls_eload_set_A.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_eload_set_A.setCheckable(False)
        self.btn_i2c_controls_eload_set_A.setChecked(False)

        self.gridLayout_21.addWidget(self.btn_i2c_controls_eload_set_A, 1, 5, 1, 1)


        self.gridLayout_20.addWidget(self.frame_i2c_controls_eload_a, 4, 0, 1, 1)

        self.btn_i2c_controls_eload_turn_off = QPushButton(self.frame_i2c_controls_eload)
        self.btn_i2c_controls_eload_turn_off.setObjectName(u"btn_i2c_controls_eload_turn_off")
        self.btn_i2c_controls_eload_turn_off.setMinimumSize(QSize(80, 30))
        self.btn_i2c_controls_eload_turn_off.setFont(font4)
        self.btn_i2c_controls_eload_turn_off.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_eload_turn_off.setIcon(icon9)
        self.btn_i2c_controls_eload_turn_off.setCheckable(False)
        self.btn_i2c_controls_eload_turn_off.setChecked(False)

        self.gridLayout_20.addWidget(self.btn_i2c_controls_eload_turn_off, 5, 2, 1, 1)

        self.label_i2c_controls_eload = QLabel(self.frame_i2c_controls_eload)
        self.label_i2c_controls_eload.setObjectName(u"label_i2c_controls_eload")
        self.label_i2c_controls_eload.setMaximumSize(QSize(16777215, 20))
        font20 = QFont()
        font20.setFamily(u"MS Shell Dlg 2")
        font20.setPointSize(12)
        font20.setBold(True)
        font20.setWeight(75)
        self.label_i2c_controls_eload.setFont(font20)
        self.label_i2c_controls_eload.setCursor(QCursor(Qt.ArrowCursor))
        self.label_i2c_controls_eload.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_eload.setAlignment(Qt.AlignCenter)

        self.gridLayout_20.addWidget(self.label_i2c_controls_eload, 0, 0, 1, 3)

        self.btn_i2c_controls_eload_a_b_swap = QPushButton(self.frame_i2c_controls_eload)
        self.btn_i2c_controls_eload_a_b_swap.setObjectName(u"btn_i2c_controls_eload_a_b_swap")
        self.btn_i2c_controls_eload_a_b_swap.setMinimumSize(QSize(80, 30))
        self.btn_i2c_controls_eload_a_b_swap.setFont(font4)
        self.btn_i2c_controls_eload_a_b_swap.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_eload_a_b_swap.setIcon(icon10)
        self.btn_i2c_controls_eload_a_b_swap.setCheckable(False)
        self.btn_i2c_controls_eload_a_b_swap.setChecked(False)

        self.gridLayout_20.addWidget(self.btn_i2c_controls_eload_a_b_swap, 2, 2, 1, 1)

        self.frame_i2c_controls_eload_slew = QFrame(self.frame_i2c_controls_eload)
        self.frame_i2c_controls_eload_slew.setObjectName(u"frame_i2c_controls_eload_slew")
        self.frame_i2c_controls_eload_slew.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_eload_slew.setFrameShadow(QFrame.Raised)
        self.gridLayout_22 = QGridLayout(self.frame_i2c_controls_eload_slew)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_22.setVerticalSpacing(6)
        self.gridLayout_22.setContentsMargins(-1, 0, -1, 0)
        self.label_i2c_controls_electronic_load_rise = QLabel(self.frame_i2c_controls_eload_slew)
        self.label_i2c_controls_electronic_load_rise.setObjectName(u"label_i2c_controls_electronic_load_rise")
        self.label_i2c_controls_electronic_load_rise.setMaximumSize(QSize(16777215, 30))
        self.label_i2c_controls_electronic_load_rise.setFont(font10)
        self.label_i2c_controls_electronic_load_rise.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_electronic_load_rise.setAlignment(Qt.AlignCenter)

        self.gridLayout_22.addWidget(self.label_i2c_controls_electronic_load_rise, 1, 0, 1, 1)

        self.label_i2c_controls_electronic_load_fall = QLabel(self.frame_i2c_controls_eload_slew)
        self.label_i2c_controls_electronic_load_fall.setObjectName(u"label_i2c_controls_electronic_load_fall")
        self.label_i2c_controls_electronic_load_fall.setMaximumSize(QSize(16777215, 30))
        self.label_i2c_controls_electronic_load_fall.setFont(font10)
        self.label_i2c_controls_electronic_load_fall.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_electronic_load_fall.setAlignment(Qt.AlignCenter)

        self.gridLayout_22.addWidget(self.label_i2c_controls_electronic_load_fall, 2, 0, 1, 1)

        self.lineedit_i2c_controls_eload_rise = QLineEdit(self.frame_i2c_controls_eload_slew)
        self.lineedit_i2c_controls_eload_rise.setObjectName(u"lineedit_i2c_controls_eload_rise")
        sizePolicy19.setHeightForWidth(self.lineedit_i2c_controls_eload_rise.sizePolicy().hasHeightForWidth())
        self.lineedit_i2c_controls_eload_rise.setSizePolicy(sizePolicy19)
        self.lineedit_i2c_controls_eload_rise.setMinimumSize(QSize(50, 30))
        self.lineedit_i2c_controls_eload_rise.setFont(font10)
        self.lineedit_i2c_controls_eload_rise.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_22.addWidget(self.lineedit_i2c_controls_eload_rise, 1, 2, 1, 1)

        self.label_i2c_controls_eload_fall_unit = QLabel(self.frame_i2c_controls_eload_slew)
        self.label_i2c_controls_eload_fall_unit.setObjectName(u"label_i2c_controls_eload_fall_unit")
        sizePolicy5.setHeightForWidth(self.label_i2c_controls_eload_fall_unit.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_eload_fall_unit.setSizePolicy(sizePolicy5)
        self.label_i2c_controls_eload_fall_unit.setMaximumSize(QSize(16777215, 16777215))
        self.label_i2c_controls_eload_fall_unit.setFont(font10)
        self.label_i2c_controls_eload_fall_unit.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_22.addWidget(self.label_i2c_controls_eload_fall_unit, 2, 3, 1, 1)

        self.lineedit_i2c_controls_eload_fall = QLineEdit(self.frame_i2c_controls_eload_slew)
        self.lineedit_i2c_controls_eload_fall.setObjectName(u"lineedit_i2c_controls_eload_fall")
        sizePolicy19.setHeightForWidth(self.lineedit_i2c_controls_eload_fall.sizePolicy().hasHeightForWidth())
        self.lineedit_i2c_controls_eload_fall.setSizePolicy(sizePolicy19)
        self.lineedit_i2c_controls_eload_fall.setMinimumSize(QSize(50, 30))
        self.lineedit_i2c_controls_eload_fall.setFont(font10)
        self.lineedit_i2c_controls_eload_fall.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_22.addWidget(self.lineedit_i2c_controls_eload_fall, 2, 2, 1, 1)

        self.label_i2c_controls_eload_rise_unit = QLabel(self.frame_i2c_controls_eload_slew)
        self.label_i2c_controls_eload_rise_unit.setObjectName(u"label_i2c_controls_eload_rise_unit")
        sizePolicy5.setHeightForWidth(self.label_i2c_controls_eload_rise_unit.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_eload_rise_unit.setSizePolicy(sizePolicy5)
        self.label_i2c_controls_eload_rise_unit.setMaximumSize(QSize(16777215, 16777215))
        self.label_i2c_controls_eload_rise_unit.setFont(font10)
        self.label_i2c_controls_eload_rise_unit.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_22.addWidget(self.label_i2c_controls_eload_rise_unit, 1, 3, 1, 1)

        self.btn_i2c_controls_eload_set_slew = QPushButton(self.frame_i2c_controls_eload_slew)
        self.btn_i2c_controls_eload_set_slew.setObjectName(u"btn_i2c_controls_eload_set_slew")
        sizePolicy19.setHeightForWidth(self.btn_i2c_controls_eload_set_slew.sizePolicy().hasHeightForWidth())
        self.btn_i2c_controls_eload_set_slew.setSizePolicy(sizePolicy19)
        self.btn_i2c_controls_eload_set_slew.setMinimumSize(QSize(40, 60))
        self.btn_i2c_controls_eload_set_slew.setFont(font4)
        self.btn_i2c_controls_eload_set_slew.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_eload_set_slew.setCheckable(False)
        self.btn_i2c_controls_eload_set_slew.setChecked(False)

        self.gridLayout_22.addWidget(self.btn_i2c_controls_eload_set_slew, 1, 4, 2, 1)


        self.gridLayout_20.addWidget(self.frame_i2c_controls_eload_slew, 4, 2, 1, 1)

        self.btn_i2c_controls_eload_turn_on = QPushButton(self.frame_i2c_controls_eload)
        self.btn_i2c_controls_eload_turn_on.setObjectName(u"btn_i2c_controls_eload_turn_on")
        self.btn_i2c_controls_eload_turn_on.setMinimumSize(QSize(80, 30))
        self.btn_i2c_controls_eload_turn_on.setFont(font4)
        self.btn_i2c_controls_eload_turn_on.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_eload_turn_on.setIcon(icon8)
        self.btn_i2c_controls_eload_turn_on.setCheckable(False)
        self.btn_i2c_controls_eload_turn_on.setChecked(False)

        self.gridLayout_20.addWidget(self.btn_i2c_controls_eload_turn_on, 5, 0, 1, 1)


        self.gridLayout_ribbon.addWidget(self.frame_i2c_controls_eload, 0, 4, 1, 1)

        self.frame_i2c_controls_power_meter_source = QFrame(self.frame_i2c_controls_ribbon)
        self.frame_i2c_controls_power_meter_source.setObjectName(u"frame_i2c_controls_power_meter_source")
        sizePolicy5.setHeightForWidth(self.frame_i2c_controls_power_meter_source.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_power_meter_source.setSizePolicy(sizePolicy5)
        self.frame_i2c_controls_power_meter_source.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_power_meter_source.setFrameShadow(QFrame.Plain)
        self.gridLayout_23 = QGridLayout(self.frame_i2c_controls_power_meter_source)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.gridLayout_23.setVerticalSpacing(2)
        self.label_i2c_controls_pms_display_d = QLabel(self.frame_i2c_controls_power_meter_source)
        self.label_i2c_controls_pms_display_d.setObjectName(u"label_i2c_controls_pms_display_d")
        sizePolicy12.setHeightForWidth(self.label_i2c_controls_pms_display_d.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_pms_display_d.setSizePolicy(sizePolicy12)
        self.label_i2c_controls_pms_display_d.setMinimumSize(QSize(180, 30))
        self.label_i2c_controls_pms_display_d.setMaximumSize(QSize(16777215, 40))
        font21 = QFont()
        font21.setFamily(u"Consolas")
        font21.setPointSize(20)
        font21.setBold(False)
        font21.setItalic(False)
        font21.setWeight(50)
        font21.setKerning(False)
        self.label_i2c_controls_pms_display_d.setFont(font21)
        self.label_i2c_controls_pms_display_d.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_pms_display_d.setFrameShape(QFrame.NoFrame)
        self.label_i2c_controls_pms_display_d.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_i2c_controls_pms_display_d, 4, 0, 1, 1)

        self.label_i2c_controls_pms_display_b = QLabel(self.frame_i2c_controls_power_meter_source)
        self.label_i2c_controls_pms_display_b.setObjectName(u"label_i2c_controls_pms_display_b")
        sizePolicy12.setHeightForWidth(self.label_i2c_controls_pms_display_b.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_pms_display_b.setSizePolicy(sizePolicy12)
        self.label_i2c_controls_pms_display_b.setMinimumSize(QSize(180, 30))
        self.label_i2c_controls_pms_display_b.setMaximumSize(QSize(16777215, 40))
        self.label_i2c_controls_pms_display_b.setFont(font21)
        self.label_i2c_controls_pms_display_b.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_pms_display_b.setFrameShape(QFrame.NoFrame)
        self.label_i2c_controls_pms_display_b.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_i2c_controls_pms_display_b, 2, 0, 1, 1)

        self.label_i2c_controls_power_meter_source = QLabel(self.frame_i2c_controls_power_meter_source)
        self.label_i2c_controls_power_meter_source.setObjectName(u"label_i2c_controls_power_meter_source")
        self.label_i2c_controls_power_meter_source.setMaximumSize(QSize(16777215, 20))
        self.label_i2c_controls_power_meter_source.setFont(font20)
        self.label_i2c_controls_power_meter_source.setCursor(QCursor(Qt.ArrowCursor))
        self.label_i2c_controls_power_meter_source.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_power_meter_source.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.label_i2c_controls_power_meter_source, 0, 0, 1, 1)

        self.label_i2c_controls_pms_display_a = QLabel(self.frame_i2c_controls_power_meter_source)
        self.label_i2c_controls_pms_display_a.setObjectName(u"label_i2c_controls_pms_display_a")
        sizePolicy12.setHeightForWidth(self.label_i2c_controls_pms_display_a.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_pms_display_a.setSizePolicy(sizePolicy12)
        self.label_i2c_controls_pms_display_a.setMinimumSize(QSize(180, 30))
        self.label_i2c_controls_pms_display_a.setMaximumSize(QSize(16777215, 40))
        self.label_i2c_controls_pms_display_a.setFont(font21)
        self.label_i2c_controls_pms_display_a.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_pms_display_a.setFrameShape(QFrame.NoFrame)
        self.label_i2c_controls_pms_display_a.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_i2c_controls_pms_display_a, 1, 0, 1, 1)

        self.label_i2c_controls_pms_display_c = QLabel(self.frame_i2c_controls_power_meter_source)
        self.label_i2c_controls_pms_display_c.setObjectName(u"label_i2c_controls_pms_display_c")
        sizePolicy12.setHeightForWidth(self.label_i2c_controls_pms_display_c.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_pms_display_c.setSizePolicy(sizePolicy12)
        self.label_i2c_controls_pms_display_c.setMinimumSize(QSize(180, 30))
        self.label_i2c_controls_pms_display_c.setMaximumSize(QSize(16777215, 40))
        self.label_i2c_controls_pms_display_c.setFont(font21)
        self.label_i2c_controls_pms_display_c.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_pms_display_c.setFrameShape(QFrame.NoFrame)
        self.label_i2c_controls_pms_display_c.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_i2c_controls_pms_display_c, 3, 0, 1, 1)


        self.gridLayout_ribbon.addWidget(self.frame_i2c_controls_power_meter_source, 0, 5, 1, 1)

        self.frame_i2c_controls_power_meter_load = QFrame(self.frame_i2c_controls_ribbon)
        self.frame_i2c_controls_power_meter_load.setObjectName(u"frame_i2c_controls_power_meter_load")
        sizePolicy5.setHeightForWidth(self.frame_i2c_controls_power_meter_load.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_power_meter_load.setSizePolicy(sizePolicy5)
        self.frame_i2c_controls_power_meter_load.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_power_meter_load.setFrameShadow(QFrame.Plain)
        self.gridLayout_24 = QGridLayout(self.frame_i2c_controls_power_meter_load)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_24.setVerticalSpacing(2)
        self.label_i2c_controls_epower_meter_load = QLabel(self.frame_i2c_controls_power_meter_load)
        self.label_i2c_controls_epower_meter_load.setObjectName(u"label_i2c_controls_epower_meter_load")
        self.label_i2c_controls_epower_meter_load.setMaximumSize(QSize(16777215, 20))
        self.label_i2c_controls_epower_meter_load.setFont(font20)
        self.label_i2c_controls_epower_meter_load.setCursor(QCursor(Qt.ArrowCursor))
        self.label_i2c_controls_epower_meter_load.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_epower_meter_load.setAlignment(Qt.AlignCenter)

        self.gridLayout_24.addWidget(self.label_i2c_controls_epower_meter_load, 0, 0, 1, 1)

        self.label_i2c_controls_pml_display_c = QLabel(self.frame_i2c_controls_power_meter_load)
        self.label_i2c_controls_pml_display_c.setObjectName(u"label_i2c_controls_pml_display_c")
        sizePolicy12.setHeightForWidth(self.label_i2c_controls_pml_display_c.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_pml_display_c.setSizePolicy(sizePolicy12)
        self.label_i2c_controls_pml_display_c.setMinimumSize(QSize(180, 30))
        self.label_i2c_controls_pml_display_c.setMaximumSize(QSize(16777215, 40))
        self.label_i2c_controls_pml_display_c.setFont(font21)
        self.label_i2c_controls_pml_display_c.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_pml_display_c.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_i2c_controls_pml_display_c, 3, 0, 1, 1)

        self.label_i2c_controls_pml_display_a = QLabel(self.frame_i2c_controls_power_meter_load)
        self.label_i2c_controls_pml_display_a.setObjectName(u"label_i2c_controls_pml_display_a")
        sizePolicy12.setHeightForWidth(self.label_i2c_controls_pml_display_a.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_pml_display_a.setSizePolicy(sizePolicy12)
        self.label_i2c_controls_pml_display_a.setMinimumSize(QSize(180, 30))
        self.label_i2c_controls_pml_display_a.setMaximumSize(QSize(16777215, 40))
        self.label_i2c_controls_pml_display_a.setFont(font21)
        self.label_i2c_controls_pml_display_a.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_pml_display_a.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_i2c_controls_pml_display_a, 1, 0, 1, 1)

        self.label_i2c_controls_pml_display_b = QLabel(self.frame_i2c_controls_power_meter_load)
        self.label_i2c_controls_pml_display_b.setObjectName(u"label_i2c_controls_pml_display_b")
        sizePolicy12.setHeightForWidth(self.label_i2c_controls_pml_display_b.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_pml_display_b.setSizePolicy(sizePolicy12)
        self.label_i2c_controls_pml_display_b.setMinimumSize(QSize(180, 30))
        self.label_i2c_controls_pml_display_b.setMaximumSize(QSize(16777215, 40))
        self.label_i2c_controls_pml_display_b.setFont(font21)
        self.label_i2c_controls_pml_display_b.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_pml_display_b.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_i2c_controls_pml_display_b, 2, 0, 1, 1)

        self.label_i2c_controls_pml_display_d = QLabel(self.frame_i2c_controls_power_meter_load)
        self.label_i2c_controls_pml_display_d.setObjectName(u"label_i2c_controls_pml_display_d")
        sizePolicy12.setHeightForWidth(self.label_i2c_controls_pml_display_d.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_pml_display_d.setSizePolicy(sizePolicy12)
        self.label_i2c_controls_pml_display_d.setMinimumSize(QSize(180, 30))
        self.label_i2c_controls_pml_display_d.setMaximumSize(QSize(16777215, 40))
        self.label_i2c_controls_pml_display_d.setFont(font21)
        self.label_i2c_controls_pml_display_d.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}\n"
"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_pml_display_d.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_i2c_controls_pml_display_d, 4, 0, 1, 1)


        self.gridLayout_ribbon.addWidget(self.frame_i2c_controls_power_meter_load, 0, 6, 1, 1)

        self.frame_i2c_controls_setup_equipment = QFrame(self.frame_i2c_controls_ribbon)
        self.frame_i2c_controls_setup_equipment.setObjectName(u"frame_i2c_controls_setup_equipment")
        sizePolicy5.setHeightForWidth(self.frame_i2c_controls_setup_equipment.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_setup_equipment.setSizePolicy(sizePolicy5)
        self.frame_i2c_controls_setup_equipment.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_setup_equipment.setFrameShadow(QFrame.Plain)
        self.gridLayout_34 = QGridLayout(self.frame_i2c_controls_setup_equipment)
        self.gridLayout_34.setObjectName(u"gridLayout_34")
        self.gridLayout_34.setVerticalSpacing(2)
        self.btn_i2c_controls_setup_equipment = QPushButton(self.frame_i2c_controls_setup_equipment)
        self.btn_i2c_controls_setup_equipment.setObjectName(u"btn_i2c_controls_setup_equipment")
        self.btn_i2c_controls_setup_equipment.setMinimumSize(QSize(80, 120))
        self.btn_i2c_controls_setup_equipment.setFont(font4)
        self.btn_i2c_controls_setup_equipment.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_setup_equipment.setCheckable(False)
        self.btn_i2c_controls_setup_equipment.setChecked(False)

        self.gridLayout_34.addWidget(self.btn_i2c_controls_setup_equipment, 3, 2, 1, 1)


        self.gridLayout_ribbon.addWidget(self.frame_i2c_controls_setup_equipment, 0, 1, 1, 1)

        self.frame_i2c_controls_ac_source = QFrame(self.frame_i2c_controls_ribbon)
        self.frame_i2c_controls_ac_source.setObjectName(u"frame_i2c_controls_ac_source")
        sizePolicy12.setHeightForWidth(self.frame_i2c_controls_ac_source.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_ac_source.setSizePolicy(sizePolicy12)
        self.frame_i2c_controls_ac_source.setMinimumSize(QSize(100, 0))
        self.frame_i2c_controls_ac_source.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_ac_source.setFrameShadow(QFrame.Plain)
        self.gridLayout_18 = QGridLayout(self.frame_i2c_controls_ac_source)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setVerticalSpacing(2)
        self.frame_i2c_controls_ac_source_buttons = QFrame(self.frame_i2c_controls_ac_source)
        self.frame_i2c_controls_ac_source_buttons.setObjectName(u"frame_i2c_controls_ac_source_buttons")
        sizePolicy12.setHeightForWidth(self.frame_i2c_controls_ac_source_buttons.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_ac_source_buttons.setSizePolicy(sizePolicy12)
        self.frame_i2c_controls_ac_source_buttons.setStyleSheet(u"QFrame{\n"
"	border:1px solid black;\n"
"	border-radius: 5px;\n"
"};")
        self.frame_i2c_controls_ac_source_buttons.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_ac_source_buttons.setFrameShadow(QFrame.Raised)
        self.verticalLayout_96 = QVBoxLayout(self.frame_i2c_controls_ac_source_buttons)
        self.verticalLayout_96.setObjectName(u"verticalLayout_96")
        self.btn_i2c_controls_ac_source_turn_on = QPushButton(self.frame_i2c_controls_ac_source_buttons)
        self.btn_i2c_controls_ac_source_turn_on.setObjectName(u"btn_i2c_controls_ac_source_turn_on")
        self.btn_i2c_controls_ac_source_turn_on.setMinimumSize(QSize(50, 50))
        self.btn_i2c_controls_ac_source_turn_on.setFont(font13)
        self.btn_i2c_controls_ac_source_turn_on.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_ac_source_turn_on.setIcon(icon8)
        self.btn_i2c_controls_ac_source_turn_on.setCheckable(False)
        self.btn_i2c_controls_ac_source_turn_on.setChecked(False)

        self.verticalLayout_96.addWidget(self.btn_i2c_controls_ac_source_turn_on)

        self.btn_i2c_controls_ac_source_turn_off = QPushButton(self.frame_i2c_controls_ac_source_buttons)
        self.btn_i2c_controls_ac_source_turn_off.setObjectName(u"btn_i2c_controls_ac_source_turn_off")
        self.btn_i2c_controls_ac_source_turn_off.setMinimumSize(QSize(50, 50))
        self.btn_i2c_controls_ac_source_turn_off.setFont(font13)
        self.btn_i2c_controls_ac_source_turn_off.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_ac_source_turn_off.setIcon(icon9)
        self.btn_i2c_controls_ac_source_turn_off.setCheckable(False)
        self.btn_i2c_controls_ac_source_turn_off.setChecked(False)

        self.verticalLayout_96.addWidget(self.btn_i2c_controls_ac_source_turn_off)


        self.gridLayout_18.addWidget(self.frame_i2c_controls_ac_source_buttons, 1, 2, 3, 1)

        self.lineedit_i2c_controls_ac_source_voltage = QLineEdit(self.frame_i2c_controls_ac_source)
        self.lineedit_i2c_controls_ac_source_voltage.setObjectName(u"lineedit_i2c_controls_ac_source_voltage")
        sizePolicy19.setHeightForWidth(self.lineedit_i2c_controls_ac_source_voltage.sizePolicy().hasHeightForWidth())
        self.lineedit_i2c_controls_ac_source_voltage.setSizePolicy(sizePolicy19)
        self.lineedit_i2c_controls_ac_source_voltage.setMinimumSize(QSize(50, 30))
        self.lineedit_i2c_controls_ac_source_voltage.setFont(font10)
        self.lineedit_i2c_controls_ac_source_voltage.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_18.addWidget(self.lineedit_i2c_controls_ac_source_voltage, 1, 1, 1, 1)

        self.lineedit_i2c_controls_ac_source_frequency = QLineEdit(self.frame_i2c_controls_ac_source)
        self.lineedit_i2c_controls_ac_source_frequency.setObjectName(u"lineedit_i2c_controls_ac_source_frequency")
        sizePolicy19.setHeightForWidth(self.lineedit_i2c_controls_ac_source_frequency.sizePolicy().hasHeightForWidth())
        self.lineedit_i2c_controls_ac_source_frequency.setSizePolicy(sizePolicy19)
        self.lineedit_i2c_controls_ac_source_frequency.setMinimumSize(QSize(50, 30))
        self.lineedit_i2c_controls_ac_source_frequency.setFont(font10)
        self.lineedit_i2c_controls_ac_source_frequency.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_18.addWidget(self.lineedit_i2c_controls_ac_source_frequency, 2, 1, 1, 1)

        self.label_i2c_controls_ac_source_frequency = QLabel(self.frame_i2c_controls_ac_source)
        self.label_i2c_controls_ac_source_frequency.setObjectName(u"label_i2c_controls_ac_source_frequency")
        sizePolicy36.setHeightForWidth(self.label_i2c_controls_ac_source_frequency.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_ac_source_frequency.setSizePolicy(sizePolicy36)
        self.label_i2c_controls_ac_source_frequency.setMinimumSize(QSize(72, 30))
        self.label_i2c_controls_ac_source_frequency.setMaximumSize(QSize(16777215, 30))
        self.label_i2c_controls_ac_source_frequency.setFont(font10)
        self.label_i2c_controls_ac_source_frequency.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_18.addWidget(self.label_i2c_controls_ac_source_frequency, 2, 0, 1, 1)

        self.label_i2c_controls_ac_source_voltage = QLabel(self.frame_i2c_controls_ac_source)
        self.label_i2c_controls_ac_source_voltage.setObjectName(u"label_i2c_controls_ac_source_voltage")
        sizePolicy36.setHeightForWidth(self.label_i2c_controls_ac_source_voltage.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_ac_source_voltage.setSizePolicy(sizePolicy36)
        self.label_i2c_controls_ac_source_voltage.setMinimumSize(QSize(72, 30))
        self.label_i2c_controls_ac_source_voltage.setMaximumSize(QSize(16777215, 30))
        self.label_i2c_controls_ac_source_voltage.setFont(font10)
        self.label_i2c_controls_ac_source_voltage.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_18.addWidget(self.label_i2c_controls_ac_source_voltage, 1, 0, 1, 1)

        self.chkbox_i2c_controls_ac_source_coupling = QCheckBox(self.frame_i2c_controls_ac_source)
        self.chkbox_i2c_controls_ac_source_coupling.setObjectName(u"chkbox_i2c_controls_ac_source_coupling")
        sizePolicy19.setHeightForWidth(self.chkbox_i2c_controls_ac_source_coupling.sizePolicy().hasHeightForWidth())
        self.chkbox_i2c_controls_ac_source_coupling.setSizePolicy(sizePolicy19)
        self.chkbox_i2c_controls_ac_source_coupling.setMinimumSize(QSize(0, 0))
        self.chkbox_i2c_controls_ac_source_coupling.setFont(font10)
        self.chkbox_i2c_controls_ac_source_coupling.setStyleSheet(u"QCheckBox:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_18.addWidget(self.chkbox_i2c_controls_ac_source_coupling, 3, 0, 1, 2)

        self.label_i2c_controls_ac_source = QLabel(self.frame_i2c_controls_ac_source)
        self.label_i2c_controls_ac_source.setObjectName(u"label_i2c_controls_ac_source")
        sizePolicy36.setHeightForWidth(self.label_i2c_controls_ac_source.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_ac_source.setSizePolicy(sizePolicy36)
        self.label_i2c_controls_ac_source.setMinimumSize(QSize(120, 20))
        self.label_i2c_controls_ac_source.setMaximumSize(QSize(16777215, 20))
        font22 = QFont()
        font22.setPointSize(12)
        font22.setBold(True)
        font22.setWeight(75)
        self.label_i2c_controls_ac_source.setFont(font22)
        self.label_i2c_controls_ac_source.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_ac_source.setAlignment(Qt.AlignCenter)

        self.gridLayout_18.addWidget(self.label_i2c_controls_ac_source, 0, 0, 1, 3)


        self.gridLayout_ribbon.addWidget(self.frame_i2c_controls_ac_source, 0, 2, 1, 1)

        self.frame_i2c_controls_default_reg = QFrame(self.frame_i2c_controls_ribbon)
        self.frame_i2c_controls_default_reg.setObjectName(u"frame_i2c_controls_default_reg")
        sizePolicy22.setHeightForWidth(self.frame_i2c_controls_default_reg.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_default_reg.setSizePolicy(sizePolicy22)
        self.frame_i2c_controls_default_reg.setMinimumSize(QSize(0, 220))
        self.frame_i2c_controls_default_reg.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_default_reg.setFrameShadow(QFrame.Plain)
        self.gridLayout_19 = QGridLayout(self.frame_i2c_controls_default_reg)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setVerticalSpacing(2)
        self.cbx_i2c_controls_inno_pro_family = QComboBox(self.frame_i2c_controls_default_reg)
        self.cbx_i2c_controls_inno_pro_family.addItem("")
        self.cbx_i2c_controls_inno_pro_family.addItem("")
        self.cbx_i2c_controls_inno_pro_family.setObjectName(u"cbx_i2c_controls_inno_pro_family")
        sizePolicy28.setHeightForWidth(self.cbx_i2c_controls_inno_pro_family.sizePolicy().hasHeightForWidth())
        self.cbx_i2c_controls_inno_pro_family.setSizePolicy(sizePolicy28)
        self.cbx_i2c_controls_inno_pro_family.setMinimumSize(QSize(100, 30))
        self.cbx_i2c_controls_inno_pro_family.setMaximumSize(QSize(16777215, 16777215))
        self.cbx_i2c_controls_inno_pro_family.setFont(font4)
        self.cbx_i2c_controls_inno_pro_family.setFocusPolicy(Qt.WheelFocus)
        self.cbx_i2c_controls_inno_pro_family.setStyleSheet(u"QComboBox:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}")

        self.gridLayout_19.addWidget(self.cbx_i2c_controls_inno_pro_family, 3, 0, 1, 1)

        self.btn_i2c_controls_initialize = QPushButton(self.frame_i2c_controls_default_reg)
        self.btn_i2c_controls_initialize.setObjectName(u"btn_i2c_controls_initialize")
        sizePolicy28.setHeightForWidth(self.btn_i2c_controls_initialize.sizePolicy().hasHeightForWidth())
        self.btn_i2c_controls_initialize.setSizePolicy(sizePolicy28)
        self.btn_i2c_controls_initialize.setMinimumSize(QSize(100, 50))
        self.btn_i2c_controls_initialize.setFont(font4)
        self.btn_i2c_controls_initialize.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_initialize.setCheckable(False)
        self.btn_i2c_controls_initialize.setChecked(False)

        self.gridLayout_19.addWidget(self.btn_i2c_controls_initialize, 1, 0, 1, 1)

        self.frame_i2c_controls_vben_reg = QFrame(self.frame_i2c_controls_default_reg)
        self.frame_i2c_controls_vben_reg.setObjectName(u"frame_i2c_controls_vben_reg")
        sizePolicy42.setHeightForWidth(self.frame_i2c_controls_vben_reg.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_vben_reg.setSizePolicy(sizePolicy42)
        self.frame_i2c_controls_vben_reg.setMinimumSize(QSize(140, 0))
        self.frame_i2c_controls_vben_reg.setMaximumSize(QSize(16777215, 200))
        self.frame_i2c_controls_vben_reg.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_vben_reg.setFrameShadow(QFrame.Raised)
        self.gridLayout_vben_reg = QGridLayout(self.frame_i2c_controls_vben_reg)
        self.gridLayout_vben_reg.setObjectName(u"gridLayout_vben_reg")

        self.gridLayout_19.addWidget(self.frame_i2c_controls_vben_reg, 1, 1, 3, 1)

        self.btn_i2c_controls_set_nr = QPushButton(self.frame_i2c_controls_default_reg)
        self.btn_i2c_controls_set_nr.setObjectName(u"btn_i2c_controls_set_nr")
        sizePolicy28.setHeightForWidth(self.btn_i2c_controls_set_nr.sizePolicy().hasHeightForWidth())
        self.btn_i2c_controls_set_nr.setSizePolicy(sizePolicy28)
        self.btn_i2c_controls_set_nr.setMinimumSize(QSize(100, 50))
        self.btn_i2c_controls_set_nr.setFont(font4)
        self.btn_i2c_controls_set_nr.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_set_nr.setCheckable(False)
        self.btn_i2c_controls_set_nr.setChecked(False)

        self.gridLayout_19.addWidget(self.btn_i2c_controls_set_nr, 2, 0, 1, 1)

        self.btn_i2c_controls_registers = QPushButton(self.frame_i2c_controls_default_reg)
        self.btn_i2c_controls_registers.setObjectName(u"btn_i2c_controls_registers")
        self.btn_i2c_controls_registers.setMinimumSize(QSize(80, 50))
        self.btn_i2c_controls_registers.setFont(font4)
        self.btn_i2c_controls_registers.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_registers.setCheckable(False)
        self.btn_i2c_controls_registers.setChecked(False)

        self.gridLayout_19.addWidget(self.btn_i2c_controls_registers, 1, 4, 1, 1)

        self.frame_i2c_controls_watchdog_reg = QFrame(self.frame_i2c_controls_default_reg)
        self.frame_i2c_controls_watchdog_reg.setObjectName(u"frame_i2c_controls_watchdog_reg")
        sizePolicy42.setHeightForWidth(self.frame_i2c_controls_watchdog_reg.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_watchdog_reg.setSizePolicy(sizePolicy42)
        self.frame_i2c_controls_watchdog_reg.setMinimumSize(QSize(150, 0))
        self.frame_i2c_controls_watchdog_reg.setMaximumSize(QSize(16777215, 200))
        self.frame_i2c_controls_watchdog_reg.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_watchdog_reg.setFrameShadow(QFrame.Raised)
        self.gridLayout_watchdog_reg = QGridLayout(self.frame_i2c_controls_watchdog_reg)
        self.gridLayout_watchdog_reg.setObjectName(u"gridLayout_watchdog_reg")

        self.gridLayout_19.addWidget(self.frame_i2c_controls_watchdog_reg, 1, 2, 3, 1)

        self.frame_i2c_controls_loop_option_reg = QFrame(self.frame_i2c_controls_default_reg)
        self.frame_i2c_controls_loop_option_reg.setObjectName(u"frame_i2c_controls_loop_option_reg")
        sizePolicy45.setHeightForWidth(self.frame_i2c_controls_loop_option_reg.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_loop_option_reg.setSizePolicy(sizePolicy45)
        self.frame_i2c_controls_loop_option_reg.setMinimumSize(QSize(175, 0))
        self.frame_i2c_controls_loop_option_reg.setMaximumSize(QSize(16777215, 200))
        self.frame_i2c_controls_loop_option_reg.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_loop_option_reg.setFrameShadow(QFrame.Raised)
        self.gridLayout_loop_option_reg = QGridLayout(self.frame_i2c_controls_loop_option_reg)
        self.gridLayout_loop_option_reg.setObjectName(u"gridLayout_loop_option_reg")

        self.gridLayout_19.addWidget(self.frame_i2c_controls_loop_option_reg, 1, 3, 3, 1)

        self.label_i2c_controls_common_commands = QLabel(self.frame_i2c_controls_default_reg)
        self.label_i2c_controls_common_commands.setObjectName(u"label_i2c_controls_common_commands")
        sizePolicy.setHeightForWidth(self.label_i2c_controls_common_commands.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_common_commands.setSizePolicy(sizePolicy)
        self.label_i2c_controls_common_commands.setMinimumSize(QSize(0, 20))
        self.label_i2c_controls_common_commands.setMaximumSize(QSize(16777215, 20))
        self.label_i2c_controls_common_commands.setFont(font22)
        self.label_i2c_controls_common_commands.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")
        self.label_i2c_controls_common_commands.setAlignment(Qt.AlignCenter)
        self.label_i2c_controls_common_commands.setMargin(0)

        self.gridLayout_19.addWidget(self.label_i2c_controls_common_commands, 0, 0, 1, 5)

        self.btn_i2c_controls_readback_registers = QPushButton(self.frame_i2c_controls_default_reg)
        self.btn_i2c_controls_readback_registers.setObjectName(u"btn_i2c_controls_readback_registers")
        self.btn_i2c_controls_readback_registers.setMinimumSize(QSize(80, 50))
        self.btn_i2c_controls_readback_registers.setFont(font4)
        self.btn_i2c_controls_readback_registers.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_readback_registers.setCheckable(False)
        self.btn_i2c_controls_readback_registers.setChecked(False)

        self.gridLayout_19.addWidget(self.btn_i2c_controls_readback_registers, 2, 4, 1, 1)

        self.cbx_i2c_controls_message_type = QComboBox(self.frame_i2c_controls_default_reg)
        self.cbx_i2c_controls_message_type.addItem("")
        self.cbx_i2c_controls_message_type.addItem("")
        self.cbx_i2c_controls_message_type.addItem("")
        self.cbx_i2c_controls_message_type.setObjectName(u"cbx_i2c_controls_message_type")
        self.cbx_i2c_controls_message_type.setMinimumSize(QSize(80, 30))
        self.cbx_i2c_controls_message_type.setMaximumSize(QSize(16777215, 16777215))
        self.cbx_i2c_controls_message_type.setFont(font10)
        self.cbx_i2c_controls_message_type.setStyleSheet(u"QComboBox:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"}")

        self.gridLayout_19.addWidget(self.cbx_i2c_controls_message_type, 3, 4, 1, 1)


        self.gridLayout_ribbon.addWidget(self.frame_i2c_controls_default_reg, 0, 3, 1, 1)


        self.gridLayout_17.addWidget(self.frame_i2c_controls_ribbon, 1, 0, 1, 2)

        self.stackedWidget_i2c_controls = QStackedWidget(self.page_i2c_controls)
        self.stackedWidget_i2c_controls.setObjectName(u"stackedWidget_i2c_controls")
        sizePolicy50 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy50.setHorizontalStretch(12)
        sizePolicy50.setVerticalStretch(12)
        sizePolicy50.setHeightForWidth(self.stackedWidget_i2c_controls.sizePolicy().hasHeightForWidth())
        self.stackedWidget_i2c_controls.setSizePolicy(sizePolicy50)
        self.page_i2c_controls_empty = QWidget()
        self.page_i2c_controls_empty.setObjectName(u"page_i2c_controls_empty")
        self.stackedWidget_i2c_controls.addWidget(self.page_i2c_controls_empty)
        self.page_i2c_controls_reg = QWidget()
        self.page_i2c_controls_reg.setObjectName(u"page_i2c_controls_reg")
        self.gridLayout_25 = QGridLayout(self.page_i2c_controls_reg)
        self.gridLayout_25.setSpacing(0)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_25.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_25.setContentsMargins(0, 0, 0, 0)
        self.frame_i2c_control_reg_console = QFrame(self.page_i2c_controls_reg)
        self.frame_i2c_control_reg_console.setObjectName(u"frame_i2c_control_reg_console")
        sizePolicy38.setHeightForWidth(self.frame_i2c_control_reg_console.sizePolicy().hasHeightForWidth())
        self.frame_i2c_control_reg_console.setSizePolicy(sizePolicy38)
        self.frame_i2c_control_reg_console.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_control_reg_console.setFrameShadow(QFrame.Raised)
        self.gridLayout_reg_console = QGridLayout(self.frame_i2c_control_reg_console)
        self.gridLayout_reg_console.setSpacing(0)
        self.gridLayout_reg_console.setObjectName(u"gridLayout_reg_console")
        self.gridLayout_reg_console.setContentsMargins(0, 0, 0, 0)
        self.frame_i2c_controls_reg3 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg3.setObjectName(u"frame_i2c_controls_reg3")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg3.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg3.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg3.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg3.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg3 = QGridLayout(self.frame_i2c_controls_reg3)
        self.gridLayout_reg3.setObjectName(u"gridLayout_reg3")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg3, 6, 0, 3, 1)

        self.frame_i2c_controls_reg13 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg13.setObjectName(u"frame_i2c_controls_reg13")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg13.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg13.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg13.setMinimumSize(QSize(0, 0))
        self.frame_i2c_controls_reg13.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg13.setFrameShadow(QFrame.Plain)
        self.frame_i2c_controls_reg13.setLineWidth(1)
        self.frame_i2c_controls_reg13.setMidLineWidth(0)
        self.gridLayout_reg13 = QGridLayout(self.frame_i2c_controls_reg13)
        self.gridLayout_reg13.setObjectName(u"gridLayout_reg13")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg13, 5, 3, 2, 2)

        self.frame_i2c_controls_reg23 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg23.setObjectName(u"frame_i2c_controls_reg23")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg23.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg23.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg23.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg23.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg23 = QGridLayout(self.frame_i2c_controls_reg23)
        self.gridLayout_reg23.setObjectName(u"gridLayout_reg23")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg23, 8, 7, 3, 2)

        self.frame_i2c_controls_reg24 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg24.setObjectName(u"frame_i2c_controls_reg24")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg24.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg24.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg24.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg24.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg24 = QGridLayout(self.frame_i2c_controls_reg24)
        self.gridLayout_reg24.setObjectName(u"gridLayout_reg24")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg24, 11, 7, 4, 2)

        self.frame_i2c_controls_reg7 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg7.setObjectName(u"frame_i2c_controls_reg7")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg7.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg7.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg7.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg7.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg7 = QGridLayout(self.frame_i2c_controls_reg7)
        self.gridLayout_reg7.setObjectName(u"gridLayout_reg7")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg7, 3, 1, 4, 2)

        self.frame_i2c_controls_reg16 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg16.setObjectName(u"frame_i2c_controls_reg16")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg16.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg16.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg16.setStyleSheet(u"")
        self.frame_i2c_controls_reg16.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg16.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg16 = QGridLayout(self.frame_i2c_controls_reg16)
        self.gridLayout_reg16.setObjectName(u"gridLayout_reg16")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg16, 11, 3, 4, 2)

        self.frame_i2c_controls_reg18 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg18.setObjectName(u"frame_i2c_controls_reg18")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg18.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg18.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg18.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg18.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg18 = QGridLayout(self.frame_i2c_controls_reg18)
        self.gridLayout_reg18.setObjectName(u"gridLayout_reg18")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg18, 4, 5, 3, 2)

        self.frame_i2c_controls_reg21 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg21.setObjectName(u"frame_i2c_controls_reg21")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg21.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg21.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg21.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg21.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg21 = QGridLayout(self.frame_i2c_controls_reg21)
        self.gridLayout_reg21.setObjectName(u"gridLayout_reg21")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg21, 0, 7, 3, 2)

        self.frame_i2c_controls_reg14 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg14.setObjectName(u"frame_i2c_controls_reg14")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg14.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg14.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg14.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg14.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg14 = QGridLayout(self.frame_i2c_controls_reg14)
        self.gridLayout_reg14.setObjectName(u"gridLayout_reg14")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg14, 7, 3, 2, 2)

        self.frame_i2c_controls_reg19 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg19.setObjectName(u"frame_i2c_controls_reg19")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg19.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg19.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg19.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg19.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg19 = QGridLayout(self.frame_i2c_controls_reg19)
        self.gridLayout_reg19.setObjectName(u"gridLayout_reg19")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg19, 7, 5, 4, 2)

        self.frame_i2c_controls_reg2 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg2.setObjectName(u"frame_i2c_controls_reg2")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg2.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg2.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg2.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg2.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg2 = QGridLayout(self.frame_i2c_controls_reg2)
        self.gridLayout_reg2.setObjectName(u"gridLayout_reg2")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg2, 3, 0, 3, 1)

        self.frame_i2c_controls_reg8 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg8.setObjectName(u"frame_i2c_controls_reg8")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg8.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg8.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg8.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg8.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg8 = QGridLayout(self.frame_i2c_controls_reg8)
        self.gridLayout_reg8.setObjectName(u"gridLayout_reg8")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg8, 7, 1, 3, 2)

        self.frame_i2c_controls_reg5 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg5.setObjectName(u"frame_i2c_controls_reg5")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg5.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg5.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg5.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg5.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg5 = QGridLayout(self.frame_i2c_controls_reg5)
        self.gridLayout_reg5.setObjectName(u"gridLayout_reg5")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg5, 12, 0, 3, 1)

        self.frame_i2c_controls_reg9 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg9.setObjectName(u"frame_i2c_controls_reg9")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg9.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg9.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg9.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg9.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg9 = QGridLayout(self.frame_i2c_controls_reg9)
        self.gridLayout_reg9.setObjectName(u"gridLayout_reg9")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg9, 10, 1, 2, 2)

        self.frame_i2c_controls_reg11 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg11.setObjectName(u"frame_i2c_controls_reg11")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg11.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg11.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg11.setMinimumSize(QSize(120, 0))
        self.frame_i2c_controls_reg11.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg11.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg11 = QGridLayout(self.frame_i2c_controls_reg11)
        self.gridLayout_reg11.setObjectName(u"gridLayout_reg11")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg11, 0, 3, 2, 2)

        self.frame_i2c_controls_reg15 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg15.setObjectName(u"frame_i2c_controls_reg15")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg15.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg15.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg15.setStyleSheet(u"")
        self.frame_i2c_controls_reg15.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg15.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg15 = QGridLayout(self.frame_i2c_controls_reg15)
        self.gridLayout_reg15.setObjectName(u"gridLayout_reg15")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg15, 9, 3, 2, 2)

        self.frame_i2c_controls_reg12 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg12.setObjectName(u"frame_i2c_controls_reg12")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg12.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg12.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg12.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg12.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg12 = QGridLayout(self.frame_i2c_controls_reg12)
        self.gridLayout_reg12.setObjectName(u"gridLayout_reg12")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg12, 2, 3, 3, 2)

        self.frame_i2c_controls_reg17 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg17.setObjectName(u"frame_i2c_controls_reg17")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg17.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg17.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg17.setStyleSheet(u"")
        self.frame_i2c_controls_reg17.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg17.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg17 = QGridLayout(self.frame_i2c_controls_reg17)
        self.gridLayout_reg17.setObjectName(u"gridLayout_reg17")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg17, 0, 5, 4, 2)

        self.frame_i2c_controls_reg6 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg6.setObjectName(u"frame_i2c_controls_reg6")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg6.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg6.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg6.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg6.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg6 = QGridLayout(self.frame_i2c_controls_reg6)
        self.gridLayout_reg6.setObjectName(u"gridLayout_reg6")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg6, 0, 1, 3, 2)

        self.frame_i2c_controls_reg22 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg22.setObjectName(u"frame_i2c_controls_reg22")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg22.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg22.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg22.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg22.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg22 = QGridLayout(self.frame_i2c_controls_reg22)
        self.gridLayout_reg22.setObjectName(u"gridLayout_reg22")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg22, 3, 7, 5, 2)

        self.frame_i2c_controls_reg4 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg4.setObjectName(u"frame_i2c_controls_reg4")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg4.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg4.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg4.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg4.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg4 = QGridLayout(self.frame_i2c_controls_reg4)
        self.gridLayout_reg4.setObjectName(u"gridLayout_reg4")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg4, 9, 0, 3, 1)

        self.frame_i2c_controls_reg10 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg10.setObjectName(u"frame_i2c_controls_reg10")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg10.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg10.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg10.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg10.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg10 = QGridLayout(self.frame_i2c_controls_reg10)
        self.gridLayout_reg10.setObjectName(u"gridLayout_reg10")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg10, 12, 1, 3, 2)

        self.frame_i2c_controls_reg1 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg1.setObjectName(u"frame_i2c_controls_reg1")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg1.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg1.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg1.setMinimumSize(QSize(0, 0))
        self.frame_i2c_controls_reg1.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg1.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg1 = QGridLayout(self.frame_i2c_controls_reg1)
        self.gridLayout_reg1.setObjectName(u"gridLayout_reg1")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg1, 0, 0, 3, 1)

        self.frame_i2c_controls_reg20 = QFrame(self.frame_i2c_control_reg_console)
        self.frame_i2c_controls_reg20.setObjectName(u"frame_i2c_controls_reg20")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_reg20.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_reg20.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_reg20.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_reg20.setFrameShadow(QFrame.Plain)
        self.gridLayout_reg20 = QGridLayout(self.frame_i2c_controls_reg20)
        self.gridLayout_reg20.setObjectName(u"gridLayout_reg20")

        self.gridLayout_reg_console.addWidget(self.frame_i2c_controls_reg20, 11, 5, 4, 2)


        self.gridLayout_25.addWidget(self.frame_i2c_control_reg_console, 0, 0, 1, 1)

        self.stackedWidget_i2c_controls.addWidget(self.page_i2c_controls_reg)
        self.page_i2c_controls_readback_reg = QWidget()
        self.page_i2c_controls_readback_reg.setObjectName(u"page_i2c_controls_readback_reg")
        self.gridLayout_26 = QGridLayout(self.page_i2c_controls_readback_reg)
        self.gridLayout_26.setSpacing(0)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_26.setContentsMargins(0, 0, 0, 0)
        self.frame_i2c_control_readback_reg_cosole = QFrame(self.page_i2c_controls_readback_reg)
        self.frame_i2c_control_readback_reg_cosole.setObjectName(u"frame_i2c_control_readback_reg_cosole")
        sizePolicy38.setHeightForWidth(self.frame_i2c_control_readback_reg_cosole.sizePolicy().hasHeightForWidth())
        self.frame_i2c_control_readback_reg_cosole.setSizePolicy(sizePolicy38)
        self.frame_i2c_control_readback_reg_cosole.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_control_readback_reg_cosole.setFrameShadow(QFrame.Raised)
        self.gridLayout_reg_console_2 = QGridLayout(self.frame_i2c_control_readback_reg_cosole)
        self.gridLayout_reg_console_2.setSpacing(0)
        self.gridLayout_reg_console_2.setObjectName(u"gridLayout_reg_console_2")
        self.gridLayout_reg_console_2.setContentsMargins(0, 0, 0, 0)
        self.frame_i2c_controls_readback_reg0 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg0.setObjectName(u"frame_i2c_controls_readback_reg0")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg0.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg0.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg0.setMinimumSize(QSize(0, 0))
        self.frame_i2c_controls_readback_reg0.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg0.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg0 = QGridLayout(self.frame_i2c_controls_readback_reg0)
        self.gridLayout_readback_reg0.setObjectName(u"gridLayout_readback_reg0")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg0, 2, 0, 4, 2)

        self.frame_i2c_controls_readback_reg10 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg10.setObjectName(u"frame_i2c_controls_readback_reg10")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg10.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg10.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg10.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg10.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg10 = QGridLayout(self.frame_i2c_controls_readback_reg10)
        self.gridLayout_readback_reg10.setObjectName(u"gridLayout_readback_reg10")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg10, 2, 5, 8, 3)

        self.frame_i2c_controls_readback_reg6 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg6.setObjectName(u"frame_i2c_controls_readback_reg6")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg6.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg6.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg6.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg6.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg6 = QGridLayout(self.frame_i2c_controls_readback_reg6)
        self.gridLayout_readback_reg6.setObjectName(u"gridLayout_readback_reg6")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg6, 2, 2, 8, 3)

        self.frame_i2c_controls_readback_reg1 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg1.setObjectName(u"frame_i2c_controls_readback_reg1")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg1.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg1.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg1.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg1.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg1 = QGridLayout(self.frame_i2c_controls_readback_reg1)
        self.gridLayout_readback_reg1.setObjectName(u"gridLayout_readback_reg1")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg1, 6, 0, 4, 2)

        self.frame_i2c_controls_readback_reg2 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg2.setObjectName(u"frame_i2c_controls_readback_reg2")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg2.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg2.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg2.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg2.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg2 = QGridLayout(self.frame_i2c_controls_readback_reg2)
        self.gridLayout_readback_reg2.setObjectName(u"gridLayout_readback_reg2")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg2, 10, 0, 4, 2)

        self.frame_i2c_controls_readback_reg3 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg3.setObjectName(u"frame_i2c_controls_readback_reg3")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg3.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg3.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg3.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg3.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg3 = QGridLayout(self.frame_i2c_controls_readback_reg3)
        self.gridLayout_readback_reg3.setObjectName(u"gridLayout_readback_reg3")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg3, 14, 0, 4, 2)

        self.frame_i2c_controls_readback_reg4 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg4.setObjectName(u"frame_i2c_controls_readback_reg4")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg4.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg4.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg4.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg4.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg4 = QGridLayout(self.frame_i2c_controls_readback_reg4)
        self.gridLayout_readback_reg4.setObjectName(u"gridLayout_readback_reg4")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg4, 18, 0, 4, 2)

        self.frame_i2c_controls_readback_reg8 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg8.setObjectName(u"frame_i2c_controls_readback_reg8")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg8.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg8.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg8.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg8.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg8 = QGridLayout(self.frame_i2c_controls_readback_reg8)
        self.gridLayout_readback_reg8.setObjectName(u"gridLayout_readback_reg8")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg8, 18, 2, 4, 3)

        self.frame_i2c_controls_readback_reg7 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg7.setObjectName(u"frame_i2c_controls_readback_reg7")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg7.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg7.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg7.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg7.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg7 = QGridLayout(self.frame_i2c_controls_readback_reg7)
        self.gridLayout_readback_reg7.setObjectName(u"gridLayout_readback_reg7")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg7, 10, 2, 8, 3)

        self.frame_i2c_controls_readback_reg5 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg5.setObjectName(u"frame_i2c_controls_readback_reg5")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg5.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg5.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg5.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg5.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg5 = QGridLayout(self.frame_i2c_controls_readback_reg5)
        self.gridLayout_readback_reg5.setObjectName(u"gridLayout_readback_reg5")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg5, 23, 0, 4, 2)

        self.frame_i2c_controls_readback_reg9 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg9.setObjectName(u"frame_i2c_controls_readback_reg9")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg9.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg9.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg9.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg9.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg9 = QGridLayout(self.frame_i2c_controls_readback_reg9)
        self.gridLayout_readback_reg9.setObjectName(u"gridLayout_readback_reg9")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg9, 23, 2, 4, 3)

        self.frame_i2c_controls_readback_reg11 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg11.setObjectName(u"frame_i2c_controls_readback_reg11")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg11.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg11.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg11.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg11.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg11 = QGridLayout(self.frame_i2c_controls_readback_reg11)
        self.gridLayout_readback_reg11.setObjectName(u"gridLayout_readback_reg11")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg11, 10, 5, 3, 3)

        self.frame_i2c_controls_readback_reg12 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg12.setObjectName(u"frame_i2c_controls_readback_reg12")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg12.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg12.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg12.setMinimumSize(QSize(0, 0))
        self.frame_i2c_controls_readback_reg12.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg12.setFrameShadow(QFrame.Plain)
        self.frame_i2c_controls_readback_reg12.setLineWidth(1)
        self.frame_i2c_controls_readback_reg12.setMidLineWidth(0)
        self.gridLayout_readback_reg12 = QGridLayout(self.frame_i2c_controls_readback_reg12)
        self.gridLayout_readback_reg12.setObjectName(u"gridLayout_readback_reg12")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg12, 13, 5, 3, 3)

        self.frame_i2c_controls_readback_reg13 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg13.setObjectName(u"frame_i2c_controls_readback_reg13")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg13.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg13.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg13.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg13.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg13 = QGridLayout(self.frame_i2c_controls_readback_reg13)
        self.gridLayout_readback_reg13.setObjectName(u"gridLayout_readback_reg13")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg13, 16, 5, 3, 3)

        self.frame_i2c_controls_readback_reg14 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg14.setObjectName(u"frame_i2c_controls_readback_reg14")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg14.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg14.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg14.setStyleSheet(u"")
        self.frame_i2c_controls_readback_reg14.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg14.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg14 = QGridLayout(self.frame_i2c_controls_readback_reg14)
        self.gridLayout_readback_reg14.setObjectName(u"gridLayout_readback_reg14")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg14, 19, 5, 3, 3)

        self.frame_i2c_controls_readback_reg_any = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg_any.setObjectName(u"frame_i2c_controls_readback_reg_any")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg_any.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg_any.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg_any.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg_any.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg_any = QGridLayout(self.frame_i2c_controls_readback_reg_any)
        self.gridLayout_readback_reg_any.setObjectName(u"gridLayout_readback_reg_any")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg_any, 23, 5, 4, 3)

        self.frame_i2c_controls_readback_reg15 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg15.setObjectName(u"frame_i2c_controls_readback_reg15")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg15.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg15.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg15.setStyleSheet(u"")
        self.frame_i2c_controls_readback_reg15.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg15.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg15 = QGridLayout(self.frame_i2c_controls_readback_reg15)
        self.gridLayout_readback_reg15.setObjectName(u"gridLayout_readback_reg15")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg15, 2, 8, 4, 3)

        self.frame_i2c_controls_readback_reg16 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg16.setObjectName(u"frame_i2c_controls_readback_reg16")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg16.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg16.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg16.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg16.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg16 = QGridLayout(self.frame_i2c_controls_readback_reg16)
        self.gridLayout_readback_reg16.setObjectName(u"gridLayout_readback_reg16")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg16, 6, 8, 8, 3)

        self.frame_i2c_controls_readback_reg17 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg17.setObjectName(u"frame_i2c_controls_readback_reg17")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg17.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg17.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg17.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg17.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg17 = QGridLayout(self.frame_i2c_controls_readback_reg17)
        self.gridLayout_readback_reg17.setObjectName(u"gridLayout_readback_reg17")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg17, 14, 8, 8, 3)

        self.frame_i2c_controls_readback_reg19 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg19.setObjectName(u"frame_i2c_controls_readback_reg19")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg19.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg19.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg19.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg19.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg19 = QGridLayout(self.frame_i2c_controls_readback_reg19)
        self.gridLayout_readback_reg19.setObjectName(u"gridLayout_readback_reg19")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg19, 2, 11, 4, 3)

        self.frame_i2c_controls_readback_reg20 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg20.setObjectName(u"frame_i2c_controls_readback_reg20")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg20.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg20.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg20.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg20.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg20 = QGridLayout(self.frame_i2c_controls_readback_reg20)
        self.gridLayout_readback_reg20.setObjectName(u"gridLayout_readback_reg20")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg20, 6, 11, 4, 3)

        self.frame_i2c_controls_readback_reg21 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg21.setObjectName(u"frame_i2c_controls_readback_reg21")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg21.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg21.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg21.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg21.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg21 = QGridLayout(self.frame_i2c_controls_readback_reg21)
        self.gridLayout_readback_reg21.setObjectName(u"gridLayout_readback_reg21")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg21, 10, 11, 4, 3)

        self.frame_i2c_controls_readback_reg22 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg22.setObjectName(u"frame_i2c_controls_readback_reg22")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg22.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg22.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg22.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg22.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg22 = QGridLayout(self.frame_i2c_controls_readback_reg22)
        self.gridLayout_readback_reg22.setObjectName(u"gridLayout_readback_reg22")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg22, 14, 11, 4, 3)

        self.frame_i2c_controls_readback_reg23 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg23.setObjectName(u"frame_i2c_controls_readback_reg23")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg23.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg23.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg23.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg23.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg23 = QGridLayout(self.frame_i2c_controls_readback_reg23)
        self.gridLayout_readback_reg23.setObjectName(u"gridLayout_readback_reg23")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg23, 18, 11, 4, 3)

        self.frame_i2c_controls_readback_reg18 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg18.setObjectName(u"frame_i2c_controls_readback_reg18")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg18.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg18.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg18.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg18.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg18 = QGridLayout(self.frame_i2c_controls_readback_reg18)
        self.gridLayout_readback_reg18.setObjectName(u"gridLayout_readback_reg18")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg18, 23, 8, 4, 3)

        self.frame_i2c_controls_readback_reg24 = QFrame(self.frame_i2c_control_readback_reg_cosole)
        self.frame_i2c_controls_readback_reg24.setObjectName(u"frame_i2c_controls_readback_reg24")
        sizePolicy11.setHeightForWidth(self.frame_i2c_controls_readback_reg24.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_readback_reg24.setSizePolicy(sizePolicy11)
        self.frame_i2c_controls_readback_reg24.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_readback_reg24.setFrameShadow(QFrame.Plain)
        self.gridLayout_readback_reg24 = QGridLayout(self.frame_i2c_controls_readback_reg24)
        self.gridLayout_readback_reg24.setObjectName(u"gridLayout_readback_reg24")

        self.gridLayout_reg_console_2.addWidget(self.frame_i2c_controls_readback_reg24, 23, 11, 4, 3)


        self.gridLayout_26.addWidget(self.frame_i2c_control_readback_reg_cosole, 0, 0, 1, 1)

        self.stackedWidget_i2c_controls.addWidget(self.page_i2c_controls_readback_reg)

        self.gridLayout_17.addWidget(self.stackedWidget_i2c_controls, 2, 0, 1, 1)

        self.frame_i2c_controls_command_list = QFrame(self.page_i2c_controls)
        self.frame_i2c_controls_command_list.setObjectName(u"frame_i2c_controls_command_list")
        sizePolicy51 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy51.setHorizontalStretch(1)
        sizePolicy51.setVerticalStretch(12)
        sizePolicy51.setHeightForWidth(self.frame_i2c_controls_command_list.sizePolicy().hasHeightForWidth())
        self.frame_i2c_controls_command_list.setSizePolicy(sizePolicy51)
        self.frame_i2c_controls_command_list.setFrameShape(QFrame.StyledPanel)
        self.frame_i2c_controls_command_list.setFrameShadow(QFrame.Plain)
        self.gridLayout_i2c_controls_command_list = QGridLayout(self.frame_i2c_controls_command_list)
        self.gridLayout_i2c_controls_command_list.setObjectName(u"gridLayout_i2c_controls_command_list")
        self.btn_i2c_controls_command_load = QPushButton(self.frame_i2c_controls_command_list)
        self.btn_i2c_controls_command_load.setObjectName(u"btn_i2c_controls_command_load")
        self.btn_i2c_controls_command_load.setMinimumSize(QSize(80, 30))
        self.btn_i2c_controls_command_load.setFont(font4)
        self.btn_i2c_controls_command_load.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_command_load.setIcon(icon22)
        self.btn_i2c_controls_command_load.setCheckable(False)
        self.btn_i2c_controls_command_load.setChecked(False)

        self.gridLayout_i2c_controls_command_list.addWidget(self.btn_i2c_controls_command_load, 0, 1, 1, 1)

        self.btn_i2c_controls_command_run_all = QPushButton(self.frame_i2c_controls_command_list)
        self.btn_i2c_controls_command_run_all.setObjectName(u"btn_i2c_controls_command_run_all")
        self.btn_i2c_controls_command_run_all.setMinimumSize(QSize(80, 30))
        self.btn_i2c_controls_command_run_all.setFont(font4)
        self.btn_i2c_controls_command_run_all.setStyleSheet(u"QPushButton {\n"
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
        icon31 = QIcon()
        icon31.addFile(u":/20x20/icons/20x20/cil-media-skip-forward.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_i2c_controls_command_run_all.setIcon(icon31)
        self.btn_i2c_controls_command_run_all.setCheckable(False)
        self.btn_i2c_controls_command_run_all.setChecked(False)

        self.gridLayout_i2c_controls_command_list.addWidget(self.btn_i2c_controls_command_run_all, 5, 0, 1, 1)

        self.btn_i2c_controls_command_run_single = QPushButton(self.frame_i2c_controls_command_list)
        self.btn_i2c_controls_command_run_single.setObjectName(u"btn_i2c_controls_command_run_single")
        self.btn_i2c_controls_command_run_single.setMinimumSize(QSize(80, 30))
        self.btn_i2c_controls_command_run_single.setFont(font4)
        self.btn_i2c_controls_command_run_single.setStyleSheet(u"QPushButton {\n"
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
        icon32 = QIcon()
        icon32.addFile(u":/20x20/icons/20x20/cil-media-step-forward.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_i2c_controls_command_run_single.setIcon(icon32)
        self.btn_i2c_controls_command_run_single.setCheckable(False)
        self.btn_i2c_controls_command_run_single.setChecked(False)

        self.gridLayout_i2c_controls_command_list.addWidget(self.btn_i2c_controls_command_run_single, 5, 1, 1, 1)

        self.lineedit_i2c_controls_command_delay = QLineEdit(self.frame_i2c_controls_command_list)
        self.lineedit_i2c_controls_command_delay.setObjectName(u"lineedit_i2c_controls_command_delay")
        sizePolicy19.setHeightForWidth(self.lineedit_i2c_controls_command_delay.sizePolicy().hasHeightForWidth())
        self.lineedit_i2c_controls_command_delay.setSizePolicy(sizePolicy19)
        self.lineedit_i2c_controls_command_delay.setMinimumSize(QSize(80, 30))
        self.lineedit_i2c_controls_command_delay.setFont(font10)
        self.lineedit_i2c_controls_command_delay.setStyleSheet(u"QLineEdit {\n"
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
"QLineEdit:disabled{\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: rgb(37, 39, 45);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(37, 39, 45);\n"
"	padding-left: 10px;\n"
"}")

        self.gridLayout_i2c_controls_command_list.addWidget(self.lineedit_i2c_controls_command_delay, 2, 0, 1, 1)

        self.btn_i2c_controls_command_add_delay = QPushButton(self.frame_i2c_controls_command_list)
        self.btn_i2c_controls_command_add_delay.setObjectName(u"btn_i2c_controls_command_add_delay")
        self.btn_i2c_controls_command_add_delay.setMinimumSize(QSize(80, 30))
        self.btn_i2c_controls_command_add_delay.setFont(font4)
        self.btn_i2c_controls_command_add_delay.setStyleSheet(u"QPushButton {\n"
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
        icon33 = QIcon()
        icon33.addFile(u":/20x20/icons/20x20/cil-media-pause.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_i2c_controls_command_add_delay.setIcon(icon33)
        self.btn_i2c_controls_command_add_delay.setCheckable(False)
        self.btn_i2c_controls_command_add_delay.setChecked(False)

        self.gridLayout_i2c_controls_command_list.addWidget(self.btn_i2c_controls_command_add_delay, 1, 0, 1, 2)

        self.btn_i2c_controls_command_save = QPushButton(self.frame_i2c_controls_command_list)
        self.btn_i2c_controls_command_save.setObjectName(u"btn_i2c_controls_command_save")
        self.btn_i2c_controls_command_save.setMinimumSize(QSize(80, 30))
        self.btn_i2c_controls_command_save.setFont(font4)
        self.btn_i2c_controls_command_save.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_command_save.setIcon(icon21)
        self.btn_i2c_controls_command_save.setCheckable(False)
        self.btn_i2c_controls_command_save.setChecked(False)

        self.gridLayout_i2c_controls_command_list.addWidget(self.btn_i2c_controls_command_save, 0, 0, 1, 1)

        self.btn_i2c_controls_command_clear = QPushButton(self.frame_i2c_controls_command_list)
        self.btn_i2c_controls_command_clear.setObjectName(u"btn_i2c_controls_command_clear")
        self.btn_i2c_controls_command_clear.setMinimumSize(QSize(80, 30))
        self.btn_i2c_controls_command_clear.setFont(font4)
        self.btn_i2c_controls_command_clear.setStyleSheet(u"QPushButton {\n"
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
        icon34 = QIcon()
        icon34.addFile(u":/20x20/icons/20x20/cil-menu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_i2c_controls_command_clear.setIcon(icon34)
        self.btn_i2c_controls_command_clear.setCheckable(False)
        self.btn_i2c_controls_command_clear.setChecked(False)

        self.gridLayout_i2c_controls_command_list.addWidget(self.btn_i2c_controls_command_clear, 4, 0, 1, 1)

        self.label_i2c_controls_command_delay_unit = QLabel(self.frame_i2c_controls_command_list)
        self.label_i2c_controls_command_delay_unit.setObjectName(u"label_i2c_controls_command_delay_unit")
        sizePolicy5.setHeightForWidth(self.label_i2c_controls_command_delay_unit.sizePolicy().hasHeightForWidth())
        self.label_i2c_controls_command_delay_unit.setSizePolicy(sizePolicy5)
        self.label_i2c_controls_command_delay_unit.setMaximumSize(QSize(16777215, 16777215))
        self.label_i2c_controls_command_delay_unit.setFont(font10)
        self.label_i2c_controls_command_delay_unit.setStyleSheet(u"QLabel:disabled{\n"
"	color: rgb(71, 71, 71)\n"
"}")

        self.gridLayout_i2c_controls_command_list.addWidget(self.label_i2c_controls_command_delay_unit, 2, 1, 1, 1)

        self.btn_i2c_controls_command_delete = QPushButton(self.frame_i2c_controls_command_list)
        self.btn_i2c_controls_command_delete.setObjectName(u"btn_i2c_controls_command_delete")
        self.btn_i2c_controls_command_delete.setMinimumSize(QSize(80, 30))
        self.btn_i2c_controls_command_delete.setFont(font4)
        self.btn_i2c_controls_command_delete.setStyleSheet(u"QPushButton {\n"
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
        self.btn_i2c_controls_command_delete.setIcon(icon14)
        self.btn_i2c_controls_command_delete.setCheckable(False)
        self.btn_i2c_controls_command_delete.setChecked(False)

        self.gridLayout_i2c_controls_command_list.addWidget(self.btn_i2c_controls_command_delete, 4, 1, 1, 1)

        self.table_i2c_controls_command_list = QTableWidget(self.frame_i2c_controls_command_list)
        if (self.table_i2c_controls_command_list.columnCount() < 2):
            self.table_i2c_controls_command_list.setColumnCount(2)
        __qtablewidgetitem41 = QTableWidgetItem()
        __qtablewidgetitem41.setFont(font10);
        self.table_i2c_controls_command_list.setHorizontalHeaderItem(0, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        __qtablewidgetitem42.setFont(font10);
        self.table_i2c_controls_command_list.setHorizontalHeaderItem(1, __qtablewidgetitem42)
        self.table_i2c_controls_command_list.setObjectName(u"table_i2c_controls_command_list")
        sizePolicy1.setHeightForWidth(self.table_i2c_controls_command_list.sizePolicy().hasHeightForWidth())
        self.table_i2c_controls_command_list.setSizePolicy(sizePolicy1)
        palette8 = QPalette()
        palette8.setBrush(QPalette.Active, QPalette.WindowText, brush6)
        palette8.setBrush(QPalette.Active, QPalette.Button, brush15)
        palette8.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette8.setBrush(QPalette.Active, QPalette.ButtonText, brush6)
        palette8.setBrush(QPalette.Active, QPalette.Base, brush15)
        palette8.setBrush(QPalette.Active, QPalette.Window, brush15)
        brush44 = QBrush(QColor(210, 210, 210, 128))
        brush44.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette8.setBrush(QPalette.Active, QPalette.PlaceholderText, brush44)
#endif
        palette8.setBrush(QPalette.Inactive, QPalette.WindowText, brush6)
        palette8.setBrush(QPalette.Inactive, QPalette.Button, brush15)
        palette8.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette8.setBrush(QPalette.Inactive, QPalette.ButtonText, brush6)
        palette8.setBrush(QPalette.Inactive, QPalette.Base, brush15)
        palette8.setBrush(QPalette.Inactive, QPalette.Window, brush15)
        brush45 = QBrush(QColor(210, 210, 210, 128))
        brush45.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette8.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush45)
#endif
        palette8.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette8.setBrush(QPalette.Disabled, QPalette.Button, brush15)
        palette8.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette8.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette8.setBrush(QPalette.Disabled, QPalette.Base, brush15)
        palette8.setBrush(QPalette.Disabled, QPalette.Window, brush15)
        brush46 = QBrush(QColor(210, 210, 210, 128))
        brush46.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette8.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush46)
#endif
        self.table_i2c_controls_command_list.setPalette(palette8)
        self.table_i2c_controls_command_list.setFont(font19)
        self.table_i2c_controls_command_list.setStyleSheet(u"QTableWidget {	\n"
"	background-color: rgb(39, 44, 54);\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
"\n"
"QHeaderView::section{\n"
"	background-color: rgb(39, 44, 54);\n"
"\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWid"
                        "get::horizontalHeader {	\n"
"	background-color: rgb(81, 255, 0);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"")
        self.table_i2c_controls_command_list.setFrameShape(QFrame.NoFrame)
        self.table_i2c_controls_command_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_i2c_controls_command_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_i2c_controls_command_list.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.table_i2c_controls_command_list.setAutoScroll(True)
        self.table_i2c_controls_command_list.setAutoScrollMargin(50)
        self.table_i2c_controls_command_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_i2c_controls_command_list.setDragEnabled(False)
        self.table_i2c_controls_command_list.setDragDropOverwriteMode(False)
        self.table_i2c_controls_command_list.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.table_i2c_controls_command_list.setAlternatingRowColors(False)
        self.table_i2c_controls_command_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_i2c_controls_command_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_i2c_controls_command_list.setShowGrid(True)
        self.table_i2c_controls_command_list.setGridStyle(Qt.SolidLine)
        self.table_i2c_controls_command_list.setSortingEnabled(False)
        self.table_i2c_controls_command_list.setWordWrap(True)
        self.table_i2c_controls_command_list.setCornerButtonEnabled(True)
        self.table_i2c_controls_command_list.setRowCount(0)
        self.table_i2c_controls_command_list.horizontalHeader().setVisible(False)
        self.table_i2c_controls_command_list.horizontalHeader().setCascadingSectionResizes(True)
        self.table_i2c_controls_command_list.horizontalHeader().setMinimumSectionSize(35)
        self.table_i2c_controls_command_list.horizontalHeader().setDefaultSectionSize(120)
        self.table_i2c_controls_command_list.horizontalHeader().setHighlightSections(True)
        self.table_i2c_controls_command_list.horizontalHeader().setProperty("showSortIndicator", False)
        self.table_i2c_controls_command_list.horizontalHeader().setStretchLastSection(False)
        self.table_i2c_controls_command_list.verticalHeader().setVisible(False)
        self.table_i2c_controls_command_list.verticalHeader().setCascadingSectionResizes(True)
        self.table_i2c_controls_command_list.verticalHeader().setMinimumSectionSize(30)
        self.table_i2c_controls_command_list.verticalHeader().setDefaultSectionSize(30)
        self.table_i2c_controls_command_list.verticalHeader().setHighlightSections(True)
        self.table_i2c_controls_command_list.verticalHeader().setProperty("showSortIndicator", True)
        self.table_i2c_controls_command_list.verticalHeader().setStretchLastSection(False)

        self.gridLayout_i2c_controls_command_list.addWidget(self.table_i2c_controls_command_list, 6, 0, 1, 2)


        self.gridLayout_17.addWidget(self.frame_i2c_controls_command_list, 2, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_i2c_controls)
        self.page_view_logs = QWidget()
        self.page_view_logs.setObjectName(u"page_view_logs")
        self.stackedWidget.addWidget(self.page_view_logs)
        self.page_save_load_configs = QWidget()
        self.page_save_load_configs.setObjectName(u"page_save_load_configs")
        self.stackedWidget.addWidget(self.page_save_load_configs)
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        self.stackedWidget.addWidget(self.page_settings)
        self.page_widgets = QWidget()
        self.page_widgets.setObjectName(u"page_widgets")
        self.verticalLayout_6 = QVBoxLayout(self.page_widgets)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame = QFrame(self.page_widgets)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"border-radius: 5px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.frame)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.frame_div_content_1 = QFrame(self.frame)
        self.frame_div_content_1.setObjectName(u"frame_div_content_1")
        self.frame_div_content_1.setMinimumSize(QSize(0, 110))
        self.frame_div_content_1.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_1.setStyleSheet(u"background-color: rgb(41, 45, 56);\n"
"border-radius: 5px;\n"
"")
        self.frame_div_content_1.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_div_content_1)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_title_wid_1.setObjectName(u"frame_title_wid_1")
        self.frame_title_wid_1.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_1.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_title_wid_1.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_title_wid_1)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.labelBoxBlenderInstalation = QLabel(self.frame_title_wid_1)
        self.labelBoxBlenderInstalation.setObjectName(u"labelBoxBlenderInstalation")
        self.labelBoxBlenderInstalation.setFont(font1)
        self.labelBoxBlenderInstalation.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.labelBoxBlenderInstalation)


        self.verticalLayout_7.addWidget(self.frame_title_wid_1)

        self.frame_content_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_content_wid_1.setObjectName(u"frame_content_wid_1")
        self.frame_content_wid_1.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_content_wid_1)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.labelVersion_3 = QLabel(self.frame_content_wid_1)
        self.labelVersion_3.setObjectName(u"labelVersion_3")
        self.labelVersion_3.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.labelVersion_3.setLineWidth(1)
        self.labelVersion_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelVersion_3, 1, 0, 1, 2)

        self.lineEdit = QLineEdit(self.frame_content_wid_1)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setStyleSheet(u"QLineEdit {\n"
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
"}")

        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.frame_content_wid_1)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(150, 30))
        self.pushButton.setFont(font13)
        self.pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton.setIcon(icon11)

        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)


        self.horizontalLayout_11.addLayout(self.gridLayout)


        self.verticalLayout_7.addWidget(self.frame_content_wid_1)


        self.verticalLayout_15.addWidget(self.frame_div_content_1)


        self.verticalLayout_6.addWidget(self.frame)

        self.frame_2 = QFrame(self.page_widgets)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 150))
        self.frame_2.setStyleSheet(u"background-color: rgb(39, 44, 54);\n"
"border-radius: 5px;")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frame_2)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSlider = QSlider(self.frame_2)
        self.verticalSlider.setObjectName(u"verticalSlider")
        self.verticalSlider.setStyleSheet(u"")
        self.verticalSlider.setOrientation(Qt.Vertical)

        self.gridLayout_2.addWidget(self.verticalSlider, 0, 2, 3, 1)

        self.horizontalSlider = QSlider(self.frame_2)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setStyleSheet(u"")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.horizontalSlider, 2, 0, 1, 2)

        self.checkBox = QCheckBox(self.frame_2)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setAutoFillBackground(False)
        self.checkBox.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.checkBox, 0, 0, 1, 1)

        self.radioButton = QRadioButton(self.frame_2)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.radioButton, 0, 1, 1, 1)

        self.horizontalScrollBar = QScrollBar(self.frame_2)
        self.horizontalScrollBar.setObjectName(u"horizontalScrollBar")
        sizePolicy52 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy52.setHorizontalStretch(0)
        sizePolicy52.setVerticalStretch(0)
        sizePolicy52.setHeightForWidth(self.horizontalScrollBar.sizePolicy().hasHeightForWidth())
        self.horizontalScrollBar.setSizePolicy(sizePolicy52)
        self.horizontalScrollBar.setStyleSheet(u"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"")
        self.horizontalScrollBar.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.horizontalScrollBar, 1, 3, 1, 1)

        self.verticalScrollBar = QScrollBar(self.frame_2)
        self.verticalScrollBar.setObjectName(u"verticalScrollBar")
        self.verticalScrollBar.setStyleSheet(u" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }")
        self.verticalScrollBar.setOrientation(Qt.Vertical)

        self.gridLayout_2.addWidget(self.verticalScrollBar, 0, 4, 3, 1)

        self.scrollArea = QScrollArea(self.frame_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"QScrollArea {\n"
"	border: none;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
"")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 218, 218))
        self.horizontalLayout_12 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.plainTextEdit = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setMinimumSize(QSize(200, 200))
        self.plainTextEdit.setStyleSheet(u"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"}\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")

        self.horizontalLayout_12.addWidget(self.plainTextEdit)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 5, 3, 1)

        self.comboBox = QComboBox(self.frame_2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setFont(font13)
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setStyleSheet(u"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(85, 170, 255);	\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}")
        self.comboBox.setIconSize(QSize(16, 16))
        self.comboBox.setFrame(True)

        self.gridLayout_2.addWidget(self.comboBox, 1, 0, 1, 2)

        self.commandLinkButton = QCommandLinkButton(self.frame_2)
        self.commandLinkButton.setObjectName(u"commandLinkButton")
        self.commandLinkButton.setStyleSheet(u"QCommandLinkButton {	\n"
"	color: rgb(85, 170, 255);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(210, 210, 210);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(210, 210, 210);\n"
"	background-color: rgb(52, 58, 71);\n"
"}")
        icon35 = QIcon()
        icon35.addFile(u":/16x16/icons/16x16/cil-link.png", QSize(), QIcon.Normal, QIcon.Off)
        self.commandLinkButton.setIcon(icon35)

        self.gridLayout_2.addWidget(self.commandLinkButton, 1, 6, 1, 1)


        self.verticalLayout_11.addLayout(self.gridLayout_2)


        self.verticalLayout_6.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.page_widgets)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 150))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_34 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_34.setSpacing(0)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.frame_3)
        if (self.tableWidget.columnCount() < 4):
            self.tableWidget.setColumnCount(4)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem44)
        __qtablewidgetitem45 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem45)
        __qtablewidgetitem46 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem46)
        if (self.tableWidget.rowCount() < 16):
            self.tableWidget.setRowCount(16)
        __qtablewidgetitem47 = QTableWidgetItem()
        __qtablewidgetitem47.setFont(font2);
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem47)
        __qtablewidgetitem48 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem48)
        __qtablewidgetitem49 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem49)
        __qtablewidgetitem50 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem50)
        __qtablewidgetitem51 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, __qtablewidgetitem51)
        __qtablewidgetitem52 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, __qtablewidgetitem52)
        __qtablewidgetitem53 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, __qtablewidgetitem53)
        __qtablewidgetitem54 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, __qtablewidgetitem54)
        __qtablewidgetitem55 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, __qtablewidgetitem55)
        __qtablewidgetitem56 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, __qtablewidgetitem56)
        __qtablewidgetitem57 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(10, __qtablewidgetitem57)
        __qtablewidgetitem58 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(11, __qtablewidgetitem58)
        __qtablewidgetitem59 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(12, __qtablewidgetitem59)
        __qtablewidgetitem60 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(13, __qtablewidgetitem60)
        __qtablewidgetitem61 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(14, __qtablewidgetitem61)
        __qtablewidgetitem62 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(15, __qtablewidgetitem62)
        __qtablewidgetitem63 = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem63)
        __qtablewidgetitem64 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem64)
        __qtablewidgetitem65 = QTableWidgetItem()
        self.tableWidget.setItem(0, 2, __qtablewidgetitem65)
        __qtablewidgetitem66 = QTableWidgetItem()
        self.tableWidget.setItem(0, 3, __qtablewidgetitem66)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy1.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy1)
        palette9 = QPalette()
        palette9.setBrush(QPalette.Active, QPalette.WindowText, brush6)
        palette9.setBrush(QPalette.Active, QPalette.Button, brush15)
        palette9.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette9.setBrush(QPalette.Active, QPalette.ButtonText, brush6)
        palette9.setBrush(QPalette.Active, QPalette.Base, brush15)
        palette9.setBrush(QPalette.Active, QPalette.Window, brush15)
        brush47 = QBrush(QColor(210, 210, 210, 128))
        brush47.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette9.setBrush(QPalette.Active, QPalette.PlaceholderText, brush47)
#endif
        palette9.setBrush(QPalette.Inactive, QPalette.WindowText, brush6)
        palette9.setBrush(QPalette.Inactive, QPalette.Button, brush15)
        palette9.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette9.setBrush(QPalette.Inactive, QPalette.ButtonText, brush6)
        palette9.setBrush(QPalette.Inactive, QPalette.Base, brush15)
        palette9.setBrush(QPalette.Inactive, QPalette.Window, brush15)
        brush48 = QBrush(QColor(210, 210, 210, 128))
        brush48.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette9.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush48)
#endif
        palette9.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette9.setBrush(QPalette.Disabled, QPalette.Button, brush15)
        palette9.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette9.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette9.setBrush(QPalette.Disabled, QPalette.Base, brush15)
        palette9.setBrush(QPalette.Disabled, QPalette.Window, brush15)
        brush49 = QBrush(QColor(210, 210, 210, 128))
        brush49.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette9.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush49)
#endif
        self.tableWidget.setPalette(palette9)
        self.tableWidget.setStyleSheet(u"QTableWidget {	\n"
"	background-color: rgb(39, 44, 54);\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
"QHeaderView::section{\n"
"	Background-color: rgb(39, 44, 54);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
""
                        "QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(81, 255, 0);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"")
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setStretchLastSection(True)

        self.horizontalLayout_34.addWidget(self.tableWidget)


        self.verticalLayout_6.addWidget(self.frame_3)

        self.stackedWidget.addWidget(self.page_widgets)

        self.gridLayout_5.addWidget(self.stackedWidget, 2, 1, 1, 1)


        self.verticalLayout_4.addWidget(self.frame_content)

        self.frame_grip = QFrame(self.frame_content_right)
        self.frame_grip.setObjectName(u"frame_grip")
        self.frame_grip.setMinimumSize(QSize(0, 25))
        self.frame_grip.setMaximumSize(QSize(16777215, 25))
        self.frame_grip.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.frame_grip.setFrameShape(QFrame.NoFrame)
        self.frame_grip.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_grip)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 2, 0)
        self.frame_label_bottom = QFrame(self.frame_grip)
        self.frame_label_bottom.setObjectName(u"frame_label_bottom")
        self.frame_label_bottom.setFrameShape(QFrame.NoFrame)
        self.frame_label_bottom.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_label_bottom)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(10, 0, 10, 0)
        self.label_credits = QLabel(self.frame_label_bottom)
        self.label_credits.setObjectName(u"label_credits")
        self.label_credits.setFont(font2)
        self.label_credits.setStyleSheet(u"color: rgb(98, 103, 111);")

        self.horizontalLayout_7.addWidget(self.label_credits)

        self.label_version = QLabel(self.frame_label_bottom)
        self.label_version.setObjectName(u"label_version")
        self.label_version.setMaximumSize(QSize(200, 16777215))
        self.label_version.setFont(font2)
        self.label_version.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.label_version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_version)


        self.horizontalLayout_6.addWidget(self.frame_label_bottom)

        self.frame_size_grip = QFrame(self.frame_grip)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMaximumSize(QSize(20, 20))
        self.frame_size_grip.setStyleSheet(u"QSizeGrip {\n"
"	background-image: url(:/16x16/icons/16x16/cil-size-grip.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
"}")
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_6.addWidget(self.frame_size_grip)


        self.verticalLayout_4.addWidget(self.frame_grip)


        self.horizontalLayout_2.addWidget(self.frame_content_right)


        self.verticalLayout.addWidget(self.frame_center)


        self.horizontalLayout.addWidget(self.frame_main)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.btn_minimize, self.btn_maximize_restore)
        QWidget.setTabOrder(self.btn_maximize_restore, self.btn_close)
        QWidget.setTabOrder(self.btn_close, self.btn_toggle_menu)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)
        self.stackedwidget_add_tests_params_top.setCurrentIndex(1)
        self.stackedwidget_add_tests_params_bot.setCurrentIndex(2)
        self.stackedwidget_add_tests_middle.setCurrentIndex(1)
        self.stacked_widget_test_results.setCurrentIndex(0)
        self.stackedWidget_i2c_controls.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_toggle_menu.setText("")
        self.label_title_bar_top.setText(QCoreApplication.translate("MainWindow", u"ATE & USB-PD Tester - Power Integrations", None))
#if QT_CONFIG(tooltip)
        self.btn_minimize.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.btn_minimize.setText("")
#if QT_CONFIG(tooltip)
        self.btn_maximize_restore.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.btn_maximize_restore.setText("")
#if QT_CONFIG(tooltip)
        self.btn_close.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.btn_close.setText("")
        self.label_top_info_1.setText("")
        self.label_top_info_2.setText(QCoreApplication.translate("MainWindow", u"| HOME", None))
        self.label_user_icon.setText(QCoreApplication.translate("MainWindow", u"PI", None))
        self.btn_page_test_results.setText(QCoreApplication.translate("MainWindow", u" Test Results", None))
        self.btn_page_manual_control.setText(QCoreApplication.translate("MainWindow", u" Manual Control", None))
        self.btn_page_equipment_setup.setText(QCoreApplication.translate("MainWindow", u" Equipment Setup", None))
        self.label_7.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"PI ATE", None))
        self.btn_page_i2c_controls.setText(QCoreApplication.translate("MainWindow", u" I2C Controls", None))
        self.btn_page_add_tests.setText(QCoreApplication.translate("MainWindow", u" Add Tests", None))
        self.label_equip_setup_sources.setText(QCoreApplication.translate("MainWindow", u"Sources", None))
        self.label_equip_setup_sources_acsource.setText(QCoreApplication.translate("MainWindow", u"AC Source", None))
        self.label_equip_setup_sources_acsource_details.setText(QCoreApplication.translate("MainWindow", u"AC Source Details", None))
        self.label_equip_setup_sources_dcsource.setText(QCoreApplication.translate("MainWindow", u"DC Source", None))
        self.label_equip_setup_sources_dcsource_details.setText(QCoreApplication.translate("MainWindow", u"DC Source Details", None))
        self.label_equip_setup_sinkcontroller.setText(QCoreApplication.translate("MainWindow", u"Sink Controller", None))
        self.label_equip_setup_sinkcontrollerdetails.setText(QCoreApplication.translate("MainWindow", u"Sink Controller Details", None))
        self.label_equip_setup_i2ccontrollerdetails.setText(QCoreApplication.translate("MainWindow", u"I2C Controller Details", None))
        self.btn_equip_setup_sinkcontroller_check_availability.setText(QCoreApplication.translate("MainWindow", u"Check Availability", None))
        self.label_equip_setup_oscilloscope.setText(QCoreApplication.translate("MainWindow", u"Oscilloscope", None))
        self.lineedit_equip_setup_oscilloscope.setText("")
        self.lineedit_equip_setup_oscilloscope.setPlaceholderText("")
        self.btn_equip_setup_oscilloscope_check_availability.setText(QCoreApplication.translate("MainWindow", u"Check Availability", None))
        self.label_equip_setup_oscilloscope_details.setText(QCoreApplication.translate("MainWindow", u"Oscilloscope Details", None))
        self.label_equip_setup_settings_contents.setText(QCoreApplication.translate("MainWindow", u"Page Control", None))
        self.btn_equip_setup_previous_pag.setText(QCoreApplication.translate("MainWindow", u"Go Back To Previous Page", None))
        self.label_equip_setup_detect.setText(QCoreApplication.translate("MainWindow", u"Detect", None))
        self.btn_equip_setup_detect_equipment.setText(QCoreApplication.translate("MainWindow", u"Detect Equipment", None))
        self.label_equip_setup_power_meters.setText(QCoreApplication.translate("MainWindow", u"Power Meters", None))
        self.label_equip_setup_power_meter_source.setText(QCoreApplication.translate("MainWindow", u"Source", None))
        self.label_equip_setup_power_meter_load_1.setText(QCoreApplication.translate("MainWindow", u"Load 1", None))
        self.label_equip_setup_power_meter_load_2.setText(QCoreApplication.translate("MainWindow", u"Load 2", None))
        self.label_equip_setup_power_meter_load_3.setText(QCoreApplication.translate("MainWindow", u"Load 3", None))
        self.label_equip_setup_power_meter_load_4.setText(QCoreApplication.translate("MainWindow", u"Load 4", None))
        self.label_equip_setup_power_meter_load_5.setText(QCoreApplication.translate("MainWindow", u"Load 5", None))
        self.label_equip_setup_eloads.setText(QCoreApplication.translate("MainWindow", u"Electronic Loads", None))
        self.label_equip_setup_eloads_load_1.setText(QCoreApplication.translate("MainWindow", u"Load 1", None))
        self.label_equip_setup_eloads_load_2.setText(QCoreApplication.translate("MainWindow", u"Load 2", None))
        self.label_equip_setup_eloads_load_3.setText(QCoreApplication.translate("MainWindow", u"Load 3", None))
        self.label_equip_setup_eloads_load_4.setText(QCoreApplication.translate("MainWindow", u"Load 4", None))
        self.label_equip_setup_eloads_load_5.setText(QCoreApplication.translate("MainWindow", u"Load 5", None))
        self.label_equip_setup_eloads_load_6.setText(QCoreApplication.translate("MainWindow", u"Load 6", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"MANUAL EQUIPMENT CONTROL", None))
        self.label_source_power_meter.setText(QCoreApplication.translate("MainWindow", u"SOURCE POWER METER", None))
        self.label_pms_display_a.setText("")
        self.label_pms_display_b.setText("")
        self.label_pms_display_c.setText("")
        self.label_pms_display_d.setText("")
        self.label_pms_voltage_range.setText(QCoreApplication.translate("MainWindow", u"Voltage Range", None))
        self.cbx_pms_voltage_range.setItemText(0, QCoreApplication.translate("MainWindow", u"AUTO", None))
        self.cbx_pms_voltage_range.setItemText(1, QCoreApplication.translate("MainWindow", u"10 mA", None))

        self.label_pms_current_range.setText(QCoreApplication.translate("MainWindow", u"Current Range", None))
        self.cbx_pms_current_range.setItemText(0, QCoreApplication.translate("MainWindow", u"AUTO", None))
        self.cbx_pms_current_range.setItemText(1, QCoreApplication.translate("MainWindow", u"10 mA", None))

        self.label_pms_integration.setText(QCoreApplication.translate("MainWindow", u"Integration", None))
        self.btn_pms_integration_start.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.btn_pms_integration_stop.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.btn_pms_integration_reset.setText(QCoreApplication.translate("MainWindow", u"RESET", None))
        self.label_pms_averaging.setText(QCoreApplication.translate("MainWindow", u"Averaging", None))
        self.btn_pms_averaging_toggle.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.cbx_pms_averaging_count.setItemText(0, QCoreApplication.translate("MainWindow", u"8", None))
        self.cbx_pms_averaging_count.setItemText(1, QCoreApplication.translate("MainWindow", u"16", None))
        self.cbx_pms_averaging_count.setItemText(2, QCoreApplication.translate("MainWindow", u"64", None))

        self.cbx_pms_averaging_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"LIN", None))
        self.cbx_pms_averaging_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"EXP", None))

        self.label_pms_measure_mode.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.btn_pms_measure_mode.setText(QCoreApplication.translate("MainWindow", u"RMS", None))
        self.label_load_power_meter.setText(QCoreApplication.translate("MainWindow", u"LOAD POWER METER", None))
        self.label_pml_display_a.setText("")
        self.label_pml_display_b.setText("")
        self.label_pml_display_c.setText("")
        self.label_pml_display_d.setText("")
        self.label_pml_voltage_range.setText(QCoreApplication.translate("MainWindow", u"Voltage Range", None))
        self.cbx_pml_voltage_range.setItemText(0, QCoreApplication.translate("MainWindow", u"AUTO", None))
        self.cbx_pml_voltage_range.setItemText(1, QCoreApplication.translate("MainWindow", u"10 mA", None))

        self.label_pml_current_range.setText(QCoreApplication.translate("MainWindow", u"Current Range", None))
        self.cbx_pml_current_range.setItemText(0, QCoreApplication.translate("MainWindow", u"AUTO", None))
        self.cbx_pml_current_range.setItemText(1, QCoreApplication.translate("MainWindow", u"10 mA", None))

        self.label_pml_integration.setText(QCoreApplication.translate("MainWindow", u"Integration", None))
        self.btn_pml_integration_start.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.btn_pml_integration_stop.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.btn_pml_integration_reset.setText(QCoreApplication.translate("MainWindow", u"RESET", None))
        self.label_pml_averaging.setText(QCoreApplication.translate("MainWindow", u"Averaging", None))
        self.btn_pml_averaging_toggle.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.cbx_pml_averaging_count.setItemText(0, QCoreApplication.translate("MainWindow", u"8", None))
        self.cbx_pml_averaging_count.setItemText(1, QCoreApplication.translate("MainWindow", u"16", None))
        self.cbx_pml_averaging_count.setItemText(2, QCoreApplication.translate("MainWindow", u"64", None))

        self.cbx_pml_averaging_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"LIN", None))
        self.cbx_pml_averaging_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"EXP", None))

        self.label_pml_measure_mode.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.btn_pml_measure_mode.setText(QCoreApplication.translate("MainWindow", u"RMS", None))
        self.btn_manual_control_setup_equipment.setText(QCoreApplication.translate("MainWindow", u"Setup \n"
"Equipment", None))
        self.label_manual_control_ac_source.setText(QCoreApplication.translate("MainWindow", u"AC SOURCE", None))
        self.lineedit_manual_control_ac_source_frequency.setText(QCoreApplication.translate("MainWindow", u"60", None))
        self.lineedit_manual_control_ac_source_frequency.setPlaceholderText("")
        self.label_manual_control_ac_source_voltage.setText(QCoreApplication.translate("MainWindow", u"Voltage", None))
        self.lineedit_manual_control_ac_source_voltage.setText(QCoreApplication.translate("MainWindow", u"90", None))
        self.lineedit_manual_control_ac_source_voltage.setPlaceholderText("")
        self.label_manual_control_ac_source_frequency.setText(QCoreApplication.translate("MainWindow", u"Frequency", None))
        self.chkbox_manual_control_ac_source_coupling.setText(QCoreApplication.translate("MainWindow", u"AC", None))
        self.btn_manual_control_ac_source_turn_on.setText(QCoreApplication.translate("MainWindow", u"Turn On", None))
        self.btn_manual_control_ac_source_turn_off.setText(QCoreApplication.translate("MainWindow", u"Turn OFF", None))
        self.label_manual_control_eload.setText(QCoreApplication.translate("MainWindow", u"ELECTRONIC LOAD", None))
        self.cbx_manual_control_eload_type.setItemText(0, QCoreApplication.translate("MainWindow", u"CC", None))
        self.cbx_manual_control_eload_type.setItemText(1, QCoreApplication.translate("MainWindow", u"CR", None))
        self.cbx_manual_control_eload_type.setItemText(2, QCoreApplication.translate("MainWindow", u"CV", None))

        self.btn_manual_control_eload_a_b_swap.setText(QCoreApplication.translate("MainWindow", u"A / B", None))
        self.label_manual_control_eload_a.setText(QCoreApplication.translate("MainWindow", u"Level A", None))
        self.lineedit_manual_control_eload_a_level.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lineedit_manual_control_eload_a_level.setPlaceholderText("")
        self.label_manual_control_eload_a_level_unit.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.btn_manual_control_eload_set_A.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.label_manual_control_eload_b.setText(QCoreApplication.translate("MainWindow", u"Level B", None))
        self.lineedit_manual_control_eload_b_level.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lineedit_manual_control_eload_b_level.setPlaceholderText("")
        self.label_manual_control_eload_b_level_unit.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.btn_manual_control_eload_set_B.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.label_manual_control_electronic_load_fall.setText(QCoreApplication.translate("MainWindow", u"Fall", None))
        self.lineedit_manual_control_eload_slew_fall.setText(QCoreApplication.translate("MainWindow", u"150", None))
        self.lineedit_manual_control_eload_slew_fall.setPlaceholderText("")
        self.label_manual_control_eload_slew_fall_unit.setText(QCoreApplication.translate("MainWindow", u"mA / \u00b5s", None))
        self.label_manual_control_electronic_load_rise.setText(QCoreApplication.translate("MainWindow", u"Rise", None))
        self.lineedit_manual_control_eload_slew_rise.setText(QCoreApplication.translate("MainWindow", u"150", None))
        self.lineedit_manual_control_eload_slew_rise.setPlaceholderText("")
        self.label_manual_control_eload_slew_rise_unit.setText(QCoreApplication.translate("MainWindow", u"mA / \u00b5s", None))
        self.btn_manual_control_eload_set_slew.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.btn_manual_control_eload_turn_on.setText(QCoreApplication.translate("MainWindow", u"Load ON", None))
        self.btn_manual_control_eload_turn_off.setText(QCoreApplication.translate("MainWindow", u"Load OFF", None))
        self.label_usbpdsink.setText(QCoreApplication.translate("MainWindow", u"USB PD SINK", None))
        self.label_usbpdsink_connection_status.setText(QCoreApplication.translate("MainWindow", u"No PD Contract", None))
        self.label_usbpdsink_status.setText(QCoreApplication.translate("MainWindow", u"Sink Disconnected", None))
        self.label_usbpdsink_sourcecaps.setText(QCoreApplication.translate("MainWindow", u"SOURCE CAPABILITIES", None))
        self.chkbox_manual_control_no_usb_suspend.setText(QCoreApplication.translate("MainWindow", u"No USB Suspend", None))
        self.chkbox_manual_control_usb_comm_capable.setText(QCoreApplication.translate("MainWindow", u"USB Communication Capable", None))
        self.chkbox_manual_control_capability_mismatch.setText(QCoreApplication.translate("MainWindow", u"Capability Mismatch", None))
        self.chkbox_manual_control_enable_giveback.setText(QCoreApplication.translate("MainWindow", u"Enable Giveback", None))
        self.lineedit_manual_usbpd_request_param1.setText("")
        self.lineedit_manual_usbpd_request_param1.setPlaceholderText("")
        self.lineedit_manual_usbpd_request_param2.setText("")
        self.lineedit_manual_usbpd_request_param2.setPlaceholderText("")
        self.label_usbpdsink_request_param2.setText(QCoreApplication.translate("MainWindow", u"Operating Current (mA)", None))
        self.label_usbpdsink_request_param1.setText(QCoreApplication.translate("MainWindow", u"Maximum Current (mA)", None))
        self.btn_usbpdsink_request.setText(QCoreApplication.translate("MainWindow", u"REQUEST", None))
        self.btn_usbpdsink_epr_entry.setText(QCoreApplication.translate("MainWindow", u"EPR ENTRY", None))
        self.btn_usbpdsink_epr_exit.setText(QCoreApplication.translate("MainWindow", u"EPR EXIT", None))
        self.chkbox_add_tests_results_folder.setText(QCoreApplication.translate("MainWindow", u"Select Results Folder", None))
        self.label_add_tests_output_folder_location.setText(QCoreApplication.translate("MainWindow", u"Parent Folder", None))
        self.lineedit_add_tests_output_folder_location.setText("")
        self.lineedit_add_tests_output_folder_location.setPlaceholderText("")
        self.label_add_tests_results_folder.setText(QCoreApplication.translate("MainWindow", u"Results Folder", None))
        self.cbx_add_tests_results_folder.setCurrentText("")
        self.label_add_tests_output_folder_spacer.setText("")
        self.btn_add_tests_output_folder_location.setText(QCoreApplication.translate("MainWindow", u"Output Folder", None))
        self.label_add_tests_output_folder_spacer_2.setText("")
#if QT_CONFIG(tooltip)
        self.btn_add_tests_open_output_folder.setToolTip(QCoreApplication.translate("MainWindow", u"View results folder in explorer", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_open_output_folder.setText("")
        self.label_add_tests_testtype.setText(QCoreApplication.translate("MainWindow", u"Test Type", None))
        self.label_add_tests_line_range.setText(QCoreApplication.translate("MainWindow", u"Line Voltage Range", None))
#if QT_CONFIG(tooltip)
        self.btn_add_tests_line_range_add_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Add a line range setting", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_line_range_add_setting.setText("")
#if QT_CONFIG(tooltip)
        self.btn_add_tests_line_range_duplicate_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Duplicate selected line range setting", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_line_range_duplicate_setting.setText("")
#if QT_CONFIG(tooltip)
        self.btn_add_tests_line_range_remove_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Remove selected line range setting", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_line_range_remove_setting.setText("")
        ___qtablewidgetitem = self.table_add_tests_line_range.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Line Voltage", None));
        ___qtablewidgetitem1 = self.table_add_tests_line_range.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Frequency", None));

        __sortingEnabled = self.table_add_tests_line_range.isSortingEnabled()
        self.table_add_tests_line_range.setSortingEnabled(False)
        self.table_add_tests_line_range.setSortingEnabled(__sortingEnabled)

        self.btn_add_tests_line_range_add.setText(QCoreApplication.translate("MainWindow", u"Add to list", None))
        self.btn_add_tests_line_range_remove.setText(QCoreApplication.translate("MainWindow", u"Remove Selected", None))
        self.btn_add_tests_line_range_clear.setText(QCoreApplication.translate("MainWindow", u"Clear All", None))
        self.lineedit_add_tests_line_range_voltage_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Voltage (V)", None))
        self.widget_toggle_add_tests_line_range_coupling.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.lineedit_add_tests_line_range_voltage.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Voltage (V)", None))
        self.lineedit_add_tests_line_range_frequency.setText("")
        self.lineedit_add_tests_line_range_frequency.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Frequency (Hz)", None))
        self.label_add_tests_line_ramp.setText(QCoreApplication.translate("MainWindow", u"Line Voltage Steps", None))
#if QT_CONFIG(tooltip)
        self.btn_add_tests_line_ramp_add_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Add a line range setting", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_line_ramp_add_setting.setText("")
#if QT_CONFIG(tooltip)
        self.btn_add_tests_line_ramp_duplicate_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Duplicate selected line range setting", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_line_ramp_duplicate_setting.setText("")
#if QT_CONFIG(tooltip)
        self.btn_add_tests_line_ramp_remove_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Remove selected line range setting", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_line_ramp_remove_setting.setText("")
        ___qtablewidgetitem2 = self.table_add_tests_line_ramp.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Line Voltage", None));
        ___qtablewidgetitem3 = self.table_add_tests_line_ramp.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Slew Rate", None));

        __sortingEnabled1 = self.table_add_tests_line_ramp.isSortingEnabled()
        self.table_add_tests_line_ramp.setSortingEnabled(False)
        self.table_add_tests_line_ramp.setSortingEnabled(__sortingEnabled1)

        self.btn_add_tests_line_ramp_add.setText(QCoreApplication.translate("MainWindow", u"Add to list", None))
        self.btn_add_tests_line_ramp_remove.setText(QCoreApplication.translate("MainWindow", u"Remove Selected", None))
        self.btn_add_tests_line_ramp_clear.setText(QCoreApplication.translate("MainWindow", u"Clear All", None))
        self.lineedit_add_tests_line_ramp_frequency.setText("")
        self.lineedit_add_tests_line_ramp_frequency.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Frequency (Hz)", None))
        self.lineedit_add_tests_line_ramp_voltage.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Voltage (V)", None))
        self.widget_toggle_add_tests_line_ramp_coupling.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.lineedit_add_tests_line_ramp_slew_rate.setText("")
        self.lineedit_add_tests_line_ramp_slew_rate.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Slew Rate (V/s)", None))
#if QT_CONFIG(tooltip)
        self.frame_add_tests_load_range_top.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.frame_add_tests_load_range_top.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.frame_add_tests_load_range_top.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_add_tests_load_range.setText(QCoreApplication.translate("MainWindow", u"Load Current Range", None))
#if QT_CONFIG(tooltip)
        self.btn_add_tests_load_range_add_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Add a load current range setting", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.btn_add_tests_load_range_add_setting.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.btn_add_tests_load_range_add_setting.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.btn_add_tests_load_range_add_setting.setText("")
#if QT_CONFIG(tooltip)
        self.btn_add_tests_load_range_duplicate_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Duplicate selected load range setting", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_load_range_duplicate_setting.setText("")
#if QT_CONFIG(tooltip)
        self.btn_add_tests_load_range_remove_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Remove selected load range setting", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_load_range_remove_setting.setText("")
        ___qtablewidgetitem4 = self.table_add_tests_load_range.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Load Percentage", None));
        ___qtablewidgetitem5 = self.table_add_tests_load_range.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Load Current (A)", None));

        __sortingEnabled2 = self.table_add_tests_load_range.isSortingEnabled()
        self.table_add_tests_load_range.setSortingEnabled(False)
        self.table_add_tests_load_range.setSortingEnabled(__sortingEnabled2)

        self.label_add_tests_soak_per_load_4.setText(QCoreApplication.translate("MainWindow", u"Load Percentage", None))
        self.lineedit_add_tests_load_range_percent.setText("")
        self.lineedit_add_tests_load_range_percent.setPlaceholderText("")
        self.label_add_tests_soak_per_load_2.setText(QCoreApplication.translate("MainWindow", u"Direction", None))
        self.btn_add_tests_load_range_add.setText(QCoreApplication.translate("MainWindow", u"Add to list", None))
        self.btn_add_tests_load_range_remove.setText(QCoreApplication.translate("MainWindow", u"Remove Selected", None))
        self.btn_add_tests_load_range_clear.setText(QCoreApplication.translate("MainWindow", u"Clear All", None))
        self.label_add_tests_cvcc_settings.setText(QCoreApplication.translate("MainWindow", u"Constant Current Settings", None))
        self.chkbox_add_tests_cvcc_multi_setpoints.setText(QCoreApplication.translate("MainWindow", u"Multiple Setpoints", None))
        self.label_add_tests_cvcc_nom_voltage.setText(QCoreApplication.translate("MainWindow", u"Nominal Output Voltage (V)", None))
        self.label_add_tests_cvcc_max_current.setText(QCoreApplication.translate("MainWindow", u"Max Current (A)", None))
        self.lineedit_add_tests_cvcc_max_current.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.lineedit_add_tests_cvcc_max_current.setPlaceholderText("")
        self.lineedit_add_tests_cvcc_nom_voltage.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.lineedit_add_tests_cvcc_nom_voltage.setPlaceholderText("")
        self.lineedit_add_tests_cvcc_step_size.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.lineedit_add_tests_cvcc_step_size.setPlaceholderText("")
        self.label_add_tests_cvcc_step_size.setText(QCoreApplication.translate("MainWindow", u"Step Size (A)", None))
        self.lineedit_add_tests_cvcc_min_current.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.lineedit_add_tests_cvcc_min_current.setPlaceholderText("")
        self.label_add_tests_cvcc_min_current.setText(QCoreApplication.translate("MainWindow", u"Min Current (A)", None))
        self.label_add_tests_timing_params.setText(QCoreApplication.translate("MainWindow", u"Test Time Parameters", None))
#if QT_CONFIG(tooltip)
        self.btn_add_tests_timing_params_add_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Add a timing parameters setting", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_timing_params_add_setting.setText("")
#if QT_CONFIG(tooltip)
        self.btn_add_tests_timing_params_duplicate_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Duplicate selected timing parameters setting", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_timing_params_duplicate_setting.setText("")
#if QT_CONFIG(tooltip)
        self.btn_add_tests_timing_params_remove_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Remove selected timing parameters setting", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_timing_params_remove_setting.setText("")
        self.lineedit_add_tests_testtime_param1.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.lineedit_add_tests_testtime_param1.setPlaceholderText("")
        self.lineedit_add_tests_testtime_param2.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.lineedit_add_tests_testtime_param2.setPlaceholderText("")
        self.label_add_tests_testtime_param1.setText(QCoreApplication.translate("MainWindow", u"Initial Soak Time (s)", None))
        self.label_add_tests_testtime_param2.setText(QCoreApplication.translate("MainWindow", u"Soak per line (s)", None))
        self.label_add_tests_testtime_param3.setText(QCoreApplication.translate("MainWindow", u"Soak per load (s)", None))
        self.lineedit_add_tests_testtime_param3.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.lineedit_add_tests_testtime_param3.setPlaceholderText("")
        self.label_add_tests_testtime_param4.setText(QCoreApplication.translate("MainWindow", u"Integration Time (s)", None))
        self.lineedit_add_tests_testtime_param4.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.lineedit_add_tests_testtime_param4.setPlaceholderText("")
        self.chkbox_add_tests_usbpd_device.setText(QCoreApplication.translate("MainWindow", u"USBPD Device?", None))
#if QT_CONFIG(tooltip)
        self.btn_add_tests_usbpd_get_source_caps.setToolTip(QCoreApplication.translate("MainWindow", u"Get Source Capabilities of USB-PD Device", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_usbpd_get_source_caps.setText(QCoreApplication.translate("MainWindow", u"Get Source Caps", None))
        ___qtablewidgetitem6 = self.table_add_tests_source_caps.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Object Pos", None));
        ___qtablewidgetitem7 = self.table_add_tests_source_caps.horizontalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"PDO Type", None));
        ___qtablewidgetitem8 = self.table_add_tests_source_caps.horizontalHeaderItem(2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Voltage", None));
        ___qtablewidgetitem9 = self.table_add_tests_source_caps.horizontalHeaderItem(3)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Current", None));
        ___qtablewidgetitem10 = self.table_add_tests_source_caps.horizontalHeaderItem(4)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Power", None));

        __sortingEnabled3 = self.table_add_tests_source_caps.isSortingEnabled()
        self.table_add_tests_source_caps.setSortingEnabled(False)
        self.table_add_tests_source_caps.setSortingEnabled(__sortingEnabled3)

        self.label_add_tests_nominal_output_voltage.setText(QCoreApplication.translate("MainWindow", u"Nominal Vout (V)", None))
        self.lineedit_add_tests_nominal_output_voltage.setPlaceholderText("")
        self.label_add_tests_nominal_output_current.setText(QCoreApplication.translate("MainWindow", u"Nominal Iout (A)", None))
        self.lineedit_add_tests_nominal_output_current.setPlaceholderText("")
        self.chkbox_add_tests_proportional_current_request.setText(QCoreApplication.translate("MainWindow", u"Tracking PDO current requests", None))
        self.label_add_tests_i2c_settings.setText(QCoreApplication.translate("MainWindow", u"I2C Options", None))
        self.label_add_tests_i2c_param_2.setText(QCoreApplication.translate("MainWindow", u"Param 2", None))
        self.lineedit_add_tests_i2c_param_2.setText("")
        self.lineedit_add_tests_i2c_param_2.setPlaceholderText("")
        self.label_add_tests_i2c_param_4.setText(QCoreApplication.translate("MainWindow", u"Param 4", None))
        self.lineedit_add_tests_i2c_param_4.setText("")
        self.lineedit_add_tests_i2c_param_4.setPlaceholderText("")
        self.label_add_tests_i2c_param_1.setText(QCoreApplication.translate("MainWindow", u"Param 1", None))
        self.lineedit_add_tests_i2c_param_1.setText("")
        self.lineedit_add_tests_i2c_param_1.setPlaceholderText("")
        self.label_add_tests_i2c_cbxparam_4.setText(QCoreApplication.translate("MainWindow", u"CBX 4", None))
        self.label_add_tests_i2c_param_3.setText(QCoreApplication.translate("MainWindow", u"Param 3", None))
        self.lineedit_add_tests_i2c_param_3.setText("")
        self.lineedit_add_tests_i2c_param_3.setPlaceholderText("")
        self.label_add_tests_i2c_param_8.setText(QCoreApplication.translate("MainWindow", u"Param 8", None))
        self.lineedit_add_tests_i2c_param_8.setText("")
        self.lineedit_add_tests_i2c_param_8.setPlaceholderText("")
        self.label_add_tests_i2c_param_7.setText(QCoreApplication.translate("MainWindow", u"Param 7", None))
        self.lineedit_add_tests_i2c_param_7.setText("")
        self.lineedit_add_tests_i2c_param_7.setPlaceholderText("")
        self.label_add_tests_i2c_cbxparam_3.setText(QCoreApplication.translate("MainWindow", u"CBX 3", None))
        self.label_add_tests_i2c_cbxparam_2.setText(QCoreApplication.translate("MainWindow", u"CBX 2", None))
        self.label_add_tests_i2c_param_5.setText(QCoreApplication.translate("MainWindow", u"Param 5", None))
        self.lineedit_add_tests_i2c_param_5.setText("")
        self.lineedit_add_tests_i2c_param_5.setPlaceholderText("")
        self.label_add_tests_i2c_param_6.setText(QCoreApplication.translate("MainWindow", u"Param 5", None))
        self.lineedit_add_tests_i2c_param_6.setText("")
        self.lineedit_add_tests_i2c_param_6.setPlaceholderText("")
        self.label_add_tests_i2c_cbxparam_1.setText(QCoreApplication.translate("MainWindow", u"CBX 1", None))
        self.label_add_tests_i2c_param_9.setText(QCoreApplication.translate("MainWindow", u"Param 9", None))
        self.lineedit_add_tests_i2c_param_9.setText("")
        self.lineedit_add_tests_i2c_param_9.setPlaceholderText("")
        self.label_add_tests_i2c_param_10.setText(QCoreApplication.translate("MainWindow", u"Param 10", None))
        self.lineedit_add_tests_i2c_param_10.setText("")
        self.lineedit_add_tests_i2c_param_10.setPlaceholderText("")
        self.chkbox_add_tests_measure_scope_ripple.setText(QCoreApplication.translate("MainWindow", u"Measure scope ripple", None))
        self.label_add_tests_eload_type.setText(QCoreApplication.translate("MainWindow", u"Load Type", None))
        self.chkbox_add_tests_eload_measurement.setText(QCoreApplication.translate("MainWindow", u"Use ELoad Data", None))
        self.btn_add_tests_option_1.setText(QCoreApplication.translate("MainWindow", u"Test Single PDO", None))
        self.btn_add_tests_option_2.setText(QCoreApplication.translate("MainWindow", u"Test All Fixed PDO", None))
#if QT_CONFIG(tooltip)
        self.btn_add_tests_test_item_move_top.setToolTip(QCoreApplication.translate("MainWindow", u"Move selected test to the top of the list", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_test_item_move_top.setText("")
#if QT_CONFIG(tooltip)
        self.btn_add_tests_test_item_move_up.setToolTip(QCoreApplication.translate("MainWindow", u"Move up selected test in list", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_test_item_move_up.setText("")
#if QT_CONFIG(tooltip)
        self.btn_add_tests_test_item_move_down.setToolTip(QCoreApplication.translate("MainWindow", u"Move down selected test in list", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_test_item_move_down.setText("")
#if QT_CONFIG(tooltip)
        self.btn_add_tests_test_item_move_bottom.setToolTip(QCoreApplication.translate("MainWindow", u"Move selected test to the bottom of the list", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_test_item_move_bottom.setText("")
        self.label_add_tests_test_list.setText(QCoreApplication.translate("MainWindow", u"Test List", None))
#if QT_CONFIG(tooltip)
        self.btn_add_tests_save_test_plan.setToolTip(QCoreApplication.translate("MainWindow", u"Save Test Plan", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_save_test_plan.setText(QCoreApplication.translate("MainWindow", u"Save Plan", None))
#if QT_CONFIG(tooltip)
        self.btn_add_tests_load_test_plan.setToolTip(QCoreApplication.translate("MainWindow", u"Load Test Plan", None))
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_load_test_plan.setText(QCoreApplication.translate("MainWindow", u"Load Plan", None))
        ___qtablewidgetitem11 = self.table_add_tests_test_list.horizontalHeaderItem(0)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Item", None));
        ___qtablewidgetitem12 = self.table_add_tests_test_list.horizontalHeaderItem(1)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Details", None));

        __sortingEnabled4 = self.table_add_tests_test_list.isSortingEnabled()
        self.table_add_tests_test_list.setSortingEnabled(False)
        self.table_add_tests_test_list.setSortingEnabled(__sortingEnabled4)

#if QT_CONFIG(tooltip)
        self.btn_add_tests_restart_selected_test.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_add_tests_restart_selected_test.setText(QCoreApplication.translate("MainWindow", u"Restart Selected Test", None))
        self.btn_add_tests_update_selected_test.setText(QCoreApplication.translate("MainWindow", u"Update Selected Test", None))
        self.btn_add_tests_remove_selected_test.setText(QCoreApplication.translate("MainWindow", u"Remove Selected Test", None))
        self.btn_add_tests_skip_selected_test.setText(QCoreApplication.translate("MainWindow", u"Skip Selected Test", None))
        self.btn_add_tests_restart_all_test.setText(QCoreApplication.translate("MainWindow", u"Restart All Tests", None))
        self.btn_add_tests_clear_all_test.setText(QCoreApplication.translate("MainWindow", u"Clear Test List", None))
        self.btn_add_tests_run.setText(QCoreApplication.translate("MainWindow", u"RUN TESTS", None))
        self.btn_add_tests_stop.setText(QCoreApplication.translate("MainWindow", u"STOP TESTS", None))
        self.btn_test_results_show_plots.setText(QCoreApplication.translate("MainWindow", u"Show Plots", None))
        self.btn_test_results_show_data.setText(QCoreApplication.translate("MainWindow", u"Show Data", None))
        ___qtablewidgetitem13 = self.table_test_results_data.horizontalHeaderItem(0)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Vin", None));
        ___qtablewidgetitem14 = self.table_test_results_data.horizontalHeaderItem(1)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Iin", None));
        ___qtablewidgetitem15 = self.table_test_results_data.horizontalHeaderItem(2)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Pin", None));
        ___qtablewidgetitem16 = self.table_test_results_data.horizontalHeaderItem(3)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Vout", None));
        ___qtablewidgetitem17 = self.table_test_results_data.horizontalHeaderItem(4)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Iout", None));
        ___qtablewidgetitem18 = self.table_test_results_data.horizontalHeaderItem(5)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Pout", None));
        ___qtablewidgetitem19 = self.table_test_results_data.horizontalHeaderItem(6)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Efficiency ", None));
        self.label_test_results_test_list.setText(QCoreApplication.translate("MainWindow", u"Test List", None))
        ___qtablewidgetitem20 = self.table_test_results_test_list.horizontalHeaderItem(0)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Item", None));
        ___qtablewidgetitem21 = self.table_test_results_test_list.horizontalHeaderItem(1)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Details", None));

        __sortingEnabled5 = self.table_test_results_test_list.isSortingEnabled()
        self.table_test_results_test_list.setSortingEnabled(False)
        self.table_test_results_test_list.setSortingEnabled(__sortingEnabled5)

        self.cbx_i2c_controls_eload_type.setItemText(0, QCoreApplication.translate("MainWindow", u"CC", None))
        self.cbx_i2c_controls_eload_type.setItemText(1, QCoreApplication.translate("MainWindow", u"CR", None))
        self.cbx_i2c_controls_eload_type.setItemText(2, QCoreApplication.translate("MainWindow", u"CV", None))
        self.cbx_i2c_controls_eload_type.setItemText(3, QCoreApplication.translate("MainWindow", u"CP", None))

        self.label_i2c_controls_eload_b_level_unit.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.lineedit_i2c_controls_eload_b_level.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lineedit_i2c_controls_eload_b_level.setPlaceholderText("")
        self.label_i2c_controls_electronic_load_A.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_i2c_controls_eload_a_level_unit.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_i2c_controls_eload_b.setText(QCoreApplication.translate("MainWindow", u"B", None))
        self.lineedit_i2c_controls_eload_a_level.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lineedit_i2c_controls_eload_a_level.setPlaceholderText("")
        self.btn_i2c_controls_eload_set_B.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.btn_i2c_controls_eload_set_A.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.btn_i2c_controls_eload_turn_off.setText(QCoreApplication.translate("MainWindow", u"Load OFF", None))
        self.label_i2c_controls_eload.setText(QCoreApplication.translate("MainWindow", u"Electronic Load", None))
        self.btn_i2c_controls_eload_a_b_swap.setText(QCoreApplication.translate("MainWindow", u"A / B", None))
        self.label_i2c_controls_electronic_load_rise.setText(QCoreApplication.translate("MainWindow", u"Rise", None))
        self.label_i2c_controls_electronic_load_fall.setText(QCoreApplication.translate("MainWindow", u"Fall", None))
        self.lineedit_i2c_controls_eload_rise.setText(QCoreApplication.translate("MainWindow", u"150", None))
        self.lineedit_i2c_controls_eload_rise.setPlaceholderText("")
        self.label_i2c_controls_eload_fall_unit.setText(QCoreApplication.translate("MainWindow", u"mA / \u00b5s", None))
        self.lineedit_i2c_controls_eload_fall.setText(QCoreApplication.translate("MainWindow", u"150", None))
        self.lineedit_i2c_controls_eload_fall.setPlaceholderText("")
        self.label_i2c_controls_eload_rise_unit.setText(QCoreApplication.translate("MainWindow", u"mA / \u00b5s", None))
        self.btn_i2c_controls_eload_set_slew.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.btn_i2c_controls_eload_turn_on.setText(QCoreApplication.translate("MainWindow", u"Load ON", None))
        self.label_i2c_controls_pms_display_d.setText("")
        self.label_i2c_controls_pms_display_b.setText("")
        self.label_i2c_controls_power_meter_source.setText(QCoreApplication.translate("MainWindow", u"Power Meter Source", None))
        self.label_i2c_controls_pms_display_a.setText("")
        self.label_i2c_controls_pms_display_c.setText("")
        self.label_i2c_controls_epower_meter_load.setText(QCoreApplication.translate("MainWindow", u"Power Meter Load", None))
        self.label_i2c_controls_pml_display_c.setText("")
        self.label_i2c_controls_pml_display_a.setText("")
        self.label_i2c_controls_pml_display_b.setText("")
        self.label_i2c_controls_pml_display_d.setText("")
        self.btn_i2c_controls_setup_equipment.setText(QCoreApplication.translate("MainWindow", u"Setup \n"
"Equipment", None))
        self.btn_i2c_controls_ac_source_turn_on.setText(QCoreApplication.translate("MainWindow", u"ON", None))
        self.btn_i2c_controls_ac_source_turn_off.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.lineedit_i2c_controls_ac_source_voltage.setText(QCoreApplication.translate("MainWindow", u"90", None))
        self.lineedit_i2c_controls_ac_source_voltage.setPlaceholderText("")
        self.lineedit_i2c_controls_ac_source_frequency.setText(QCoreApplication.translate("MainWindow", u"60", None))
        self.lineedit_i2c_controls_ac_source_frequency.setPlaceholderText("")
        self.label_i2c_controls_ac_source_frequency.setText(QCoreApplication.translate("MainWindow", u"Frequency", None))
        self.label_i2c_controls_ac_source_voltage.setText(QCoreApplication.translate("MainWindow", u"Voltage", None))
        self.chkbox_i2c_controls_ac_source_coupling.setText(QCoreApplication.translate("MainWindow", u"AC", None))
        self.label_i2c_controls_ac_source.setText(QCoreApplication.translate("MainWindow", u"AC Supply", None))
        self.cbx_i2c_controls_inno_pro_family.setItemText(0, QCoreApplication.translate("MainWindow", u"Inno5-Pro", None))
        self.cbx_i2c_controls_inno_pro_family.setItemText(1, QCoreApplication.translate("MainWindow", u"Inno4-Pro", None))

        self.btn_i2c_controls_initialize.setText(QCoreApplication.translate("MainWindow", u"Initialize", None))
        self.btn_i2c_controls_set_nr.setText(QCoreApplication.translate("MainWindow", u"Set NR", None))
        self.btn_i2c_controls_registers.setText(QCoreApplication.translate("MainWindow", u"Registers", None))
        self.label_i2c_controls_common_commands.setText(QCoreApplication.translate("MainWindow", u"Common I2C commands", None))
        self.btn_i2c_controls_readback_registers.setText(QCoreApplication.translate("MainWindow", u"Readback\n"
"Registers", None))
        self.cbx_i2c_controls_message_type.setItemText(0, QCoreApplication.translate("MainWindow", u"I2C", None))
        self.cbx_i2c_controls_message_type.setItemText(1, QCoreApplication.translate("MainWindow", u"UVDM1", None))
        self.cbx_i2c_controls_message_type.setItemText(2, QCoreApplication.translate("MainWindow", u"UVDM2", None))

        self.btn_i2c_controls_command_load.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.btn_i2c_controls_command_run_all.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.btn_i2c_controls_command_run_single.setText(QCoreApplication.translate("MainWindow", u"Single", None))
        self.lineedit_i2c_controls_command_delay.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.lineedit_i2c_controls_command_delay.setPlaceholderText("")
        self.btn_i2c_controls_command_add_delay.setText(QCoreApplication.translate("MainWindow", u"Add Delay", None))
        self.btn_i2c_controls_command_save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.btn_i2c_controls_command_clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.label_i2c_controls_command_delay_unit.setText(QCoreApplication.translate("MainWindow", u"ms", None))
        self.btn_i2c_controls_command_delete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        ___qtablewidgetitem22 = self.table_i2c_controls_command_list.horizontalHeaderItem(0)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"Function", None));
        ___qtablewidgetitem23 = self.table_i2c_controls_command_list.horizontalHeaderItem(1)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"Value", None));
        self.labelBoxBlenderInstalation.setText(QCoreApplication.translate("MainWindow", u"BLENDER INSTALLATION", None))
        self.labelVersion_3.setText(QCoreApplication.translate("MainWindow", u"Ex: C:Program FilesBlender FoundationBlender 2.82 blender.exe", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Your Password", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Open Blender", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Test 1", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Test 2", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Test 3", None))

        self.commandLinkButton.setText(QCoreApplication.translate("MainWindow", u"CommandLinkButton", None))
        self.commandLinkButton.setDescription(QCoreApplication.translate("MainWindow", u"Open External Link", None))
        ___qtablewidgetitem24 = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"0", None));
        ___qtablewidgetitem25 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem26 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"2", None));
        ___qtablewidgetitem27 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"3", None));
        ___qtablewidgetitem28 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem29 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem30 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem31 = self.tableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem32 = self.tableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem33 = self.tableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem34 = self.tableWidget.verticalHeaderItem(6)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem35 = self.tableWidget.verticalHeaderItem(7)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem36 = self.tableWidget.verticalHeaderItem(8)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem37 = self.tableWidget.verticalHeaderItem(9)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem38 = self.tableWidget.verticalHeaderItem(10)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem39 = self.tableWidget.verticalHeaderItem(11)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem40 = self.tableWidget.verticalHeaderItem(12)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem41 = self.tableWidget.verticalHeaderItem(13)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem42 = self.tableWidget.verticalHeaderItem(14)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem43 = self.tableWidget.verticalHeaderItem(15)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("MainWindow", u"New Row", None));

        __sortingEnabled6 = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem44 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("MainWindow", u"Test", None));
        ___qtablewidgetitem45 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem45.setText(QCoreApplication.translate("MainWindow", u"Text", None));
        ___qtablewidgetitem46 = self.tableWidget.item(0, 2)
        ___qtablewidgetitem46.setText(QCoreApplication.translate("MainWindow", u"Cell", None));
        ___qtablewidgetitem47 = self.tableWidget.item(0, 3)
        ___qtablewidgetitem47.setText(QCoreApplication.translate("MainWindow", u"Line", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled6)

        self.label_credits.setText(QCoreApplication.translate("MainWindow", u"\u00a9 RN, RRI, CMC", None))
        self.label_version.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
    # retranslateUi

