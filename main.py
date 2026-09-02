###############################################################################
# Base User interface design taken from 
# https://github.com/Wanderson-Magalhaes/Simple_PySide_Base
# By Wanderson Pimenta
###############################################################################

# Standard Library Imports
import os
import sys
import platform
import time
import traceback

class DualLogger(object):
    def __init__(self, filepath="app_log.txt"):
        self.terminal = sys.stdout
        self.logfile = open(filepath, "a", encoding="utf-8", buffering=1)

    def write(self, message):
        if self.terminal:
            try:
                self.terminal.write(message)
            except Exception:
                pass
        try:
            self.logfile.write(message)
            self.logfile.flush()
        except Exception:
            pass

    def flush(self):
        if self.terminal:
            try:
                self.terminal.flush()
            except Exception:
                pass
        try:
            self.logfile.flush()
        except Exception:
            pass

def log_uncaught_exceptions(ex_cls, ex, tb):
    err_msg = "".join(traceback.format_exception(ex_cls, ex, tb))
    print(f"\n[UNCAUGHT EXCEPTION] {time.strftime('%Y-%m-%d %H:%M:%S')}:\n{err_msg}\n")

sys.stdout = DualLogger()
sys.stderr = sys.stdout
sys.excepthook = log_uncaught_exceptions

# Third party imports
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (
    QTimer, QCoreApplication, QPropertyAnimation, QDate, 
    QDateTime, QMetaObject, QObject, QPoint, QRect, 
    QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (
    QPixmap, QBrush, QColor, QConicalGradient, QCursor, QFont, 
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, 
    QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from qtwidgets import Toggle

import pyqtgraph as pg

# Local Imports
from page_controls import (
    manual_control, add_test, equipment_setup, test_results, i2c_controls)

from psu_tests.tests import TestPlan
from psu_tests.definitions import (
    MessageType, LineSettings, LoadSettings, SoaktimeSettings, LineRampSettings,TestConditionSettings)

from sink_controllers.epr_sink_control import STM32SinkController
from equipment.handler import EquipmentHandler

# GUI FILES
from app.app_modules import *
from ui.ui_main import Ui_MainWindow
from ui.splash_screen import Ui_SplashScreen
from ui.ui_styles import *

SOFTWARE_VERSION =  'DIG-236 C314 December 3, 2025'

run_settings = {'debug': False}

class STACK_PAGE():
    """Defines the pages of the main user interface.
    These values should match with the GUI_BASE.ui file in /ui"""
    HOME                    = 0
    EQUIPMENT_SETUP         = 1
    MANUAL_CONTROL          = 2
    ADD_TESTS               = 3
    TEST_RESULTS            = 4
    # I2C_CONTROLS            = 5
    # VIEW_LOGS               = 6
    # SAVE_LOAD_CONFIG        = 7
    # SETTINGS                = 8


class MainWindow(QMainWindow):
    """The MainWindow holds the main user interface and
    runs the main event loop."""
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initialize_ui()

        self.initialize_objects()
        self.initialize_page_handlers()
        self.initialize_ui_states()


        # Since the window title bar is removed, the title bar
        # defined in the UI will be set as the replacement
        # This method controls that movement
        def moveWindow(event):
            """Move the window""" 
            
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunctions.returnStatus() == 1:
                UIFunctions.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.setWindowIcon(QtGui.QIcon('ui\icons\pi-ate-logo.png'))
            
        # WIDGET TO MOVE
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        
    
    def show_display(self):
        # Show the user interface and maximize it
        self.show()
        UIFunctions.maximize_restore(self)
    
    
    def initialize_objects(self):
        """Initialize the objects that will be used."""
        # Message box that will be used by all pages
        self.msg_box = QMessageBox()
        self.input_box = QInputDialog()

        self.test_plan = TestPlan(self)
        self.line_settings = LineSettings()
        self.load_settings = LoadSettings()
        self.soaktime_settings = SoaktimeSettings()
        self.line_ramp_settings = LineRampSettings()
        self.equipment = EquipmentHandler(self)
        self.test_condition_settings = TestConditionSettings()

        self.run_settings = run_settings

    def initialize_page_handlers(self):
        """Initialize the page handlers before opening so that
        the pages will be ready before they are accessed."""
        self.equipment_setup_page_handler \
            = equipment_setup.EquipmentSetupPageHandler(self)
        self.manual_control_handler \
            = manual_control.ManualControlPageHandler(self)
        self.add_test_pagehandler = add_test.AddTestPageHandler(self)
        self.test_results_page_handler \
            = test_results.TestResultsPageHandler(self)
        # self.i2c_controls_page_handler \
        #     = i2c_controls.I2CControlsPageHandler(self)

    def initialize_ui_states(self):
        self.previous_stackwidget_index = 0

    def initialize_ui(self):
        
        # Print the system and version
        print('System: ' + platform.system())
        print('Version: ' + platform.release())
        self.ui.label_version.setText(SOFTWARE_VERSION)

        # Remove the standard title bar
        UIFunctions.removeTitleBar(True)

        # Set the window title
        self.setWindowTitle('PI ATE & USB-PD Tester')
        UIFunctions.labelTitle(self, 'PI ATE & USB-PD Tester')
        UIFunctions.labelDescription(self, 'Power Integrations')

        # Set the size of the window at startup
        # Set close to 1080p
        startSize = QSize(1900, 1000)
        self.resize(startSize)
        self.setMinimumSize(startSize)

        ## ==> TOGGLE MENU SIZE
        self.ui.btn_toggle_menu.clicked.connect(
            lambda: UIFunctions.toggleMenu(self, 220, True))
        ## ==> END ##

        ## ==> ADD CUSTOM MENUS
        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(
            self, "Home", "btn_home",
            "url(:/16x16/icons/16x16/cil-home.png)", True)
        UIFunctions.addNewMenu(
            self, "Equipment Setup", "btn_equipment_setup", 
            "url(:/20x20/icons/20x20/cil-equalizer.png)", True)
        UIFunctions.addNewMenu(
            self, "Manual Control", "btn_manual_control",
            "url(:/20x20/icons/20x20/cil-touch-app.png)", True)
        UIFunctions.addNewMenu(
            self, "Add Tests", "btn_add_tests", 
            "url(:/20x20/icons/20x20/cil-library-add.png)", True)
        UIFunctions.addNewMenu(
            self, "Test Results", "btn_test_results", 
            "url(:/20x20/icons/20x20/cil-library.png)", True)
        # UIFunctions.addNewMenu(
        #     self, "I2C Controls", "btn_i2c_controls", 
        #     "url(:/20x20/icons/20x20/cil-lightbulb.png)", True)
        # UIFunctions.addNewMenu(
        #     self, "View Logs", "btn_view_logs", 
        #     "url(:/20x20/icons/20x20/cil-notes.png)", True)
        # UIFunctions.addNewMenu(
        #     self, "Save/Load Configuration", "btn_save_load_configs", 
        #     "url(:/20x20/icons/20x20/cil-save.png)", False)
        # UIFunctions.addNewMenu(
        #     self, "Settings", "btn_settings", 
        #     "url(:/20x20/icons/20x20/cil-settings.png)", False)
        
       
        ## ==> END ##

        # START MENU => SELECTION
        # Set the default page of the UI
        UIFunctions.selectStandardMenu(self, "btn_home")
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

        # Set the username's initials as the user icon
        user_name = os.getlogin()[0:2]
        UIFunctions.userIcon(self, user_name, "", True)

        # Run a handler for when the page of the UI changes
        self.ui.stackedWidget.currentChanged.connect(
            self.stacked_widget_page_change)

        UIFunctions.uiDefinitions(self)
        self.ui.btn_page_equipment_setup.clicked.connect(self.Button)
        self.ui.btn_page_manual_control.clicked.connect(self.Button)
        # self.ui.btn_page_i2c_controls.clicked.connect(self.Button)
        self.ui.btn_page_i2c_controls.setVisible(False)
        self.ui.btn_page_add_tests.clicked.connect(self.Button)
        self.ui.btn_page_test_results.clicked.connect(self.Button)


    # Handler for page change
    def stacked_widget_page_change(self):
        current_index  = self.ui.stackedWidget.currentIndex()

        match self.previous_stackwidget_index:
            case STACK_PAGE.MANUAL_CONTROL:
                print("End Manual Control")
                self.manual_control_handler.stop()
            case STACK_PAGE.TEST_RESULTS:
                print("End Test Results")
                self.test_results_page_handler.stop()
            # case STACK_PAGE.I2C_CONTROLS:
            #     print("End I2C Controls")
            #     self.i2c_controls_page_handler.stop()

        match current_index:
            case STACK_PAGE.MANUAL_CONTROL:
                print("Start Manual Control Page Handler")
                self.manual_control_handler.start()
            
            case STACK_PAGE.ADD_TESTS:
                print("Start Add Tests Page Handler")
                self.add_test_pagehandler.start()
            
            # case STACK_PAGE.I2C_CONTROLS:
            #     print("Start I2C Controls Page Handler")
            #     self.i2c_controls_page_handler.start()
            
            case STACK_PAGE.TEST_RESULTS:
                print("Start Test Results Page Handler")
                self.test_results_page_handler.start()
            


        self.previous_stackwidget_index = current_index

    
    def msg_box_info(self, title, message, message_type):
        """Create a message box with title and message.
        """
        match message_type:
            case MessageType.INFO:
                self.msg_box.setIcon(QMessageBox.Information)
            case MessageType.WARNING:
                self.msg_box.setIcon(QMessageBox.Warning)
            case MessageType.ABORT:
                self.msg_box.setIcon(QMessageBox.Abort)
            
        
        self.msg_box.setText(message)
        self.msg_box.setWindowTitle(title)
        self.msg_box.setStandardButtons(QMessageBox.Ok)
        self.msg_box.exec_()

    def msg_box_input(self, title, message):
        text, _ = QInputDialog.getText(self, title, message, QLineEdit.Normal)
        return text
    
    def msg_box_pick(self, title, message):
        """ Create message box that prompts user to pick an option"""
        self.msg_box.setText(message)
        self.msg_box.setWindowTitle(title)
        self.msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return self.msg_box.exec_()


    ########################################################################
    ## MENUS ==> DYNAMIC MENUS FUNCTIONS
    ########################################################################
    def Button(self):
        # GET BT CLICKED
        btnWidget = self.sender()

        # PAGE HOME
        if btnWidget.objectName() == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_home")
            UIFunctions.labelPage(self, "Home")
            btnWidget.setStyleSheet(
                UIFunctions.selectMenu(btnWidget.styleSheet()))
        
        
        # PAGE EQUIPMENT SETUP
        elif btnWidget.objectName() in ["btn_equipment_setup","btn_page_equipment_setup"]:
            self.ui.stackedWidget.setCurrentWidget(
                self.ui.page_equipment_setup)
            UIFunctions.resetStyle(self, "btn_equipment_setup")
            UIFunctions.labelPage(self, "EQUIPMENT SETUP")
            btnWidget.setStyleSheet(
                UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE MANUAL EQUIPMENT CONTROL
        elif btnWidget.objectName() in ["btn_manual_control","btn_page_manual_control"]:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_manual_control)
            UIFunctions.resetStyle(self, "btn_manual_control")
            UIFunctions.labelPage(self, "Manual Equipment Control")
            btnWidget.setStyleSheet(
                UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE ADD TESTS
        elif btnWidget.objectName() in ["btn_add_tests","btn_page_add_tests"]:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_add_tests)
            UIFunctions.resetStyle(self, "btn_add_tests")
            UIFunctions.labelPage(self, "Add Tests")
            btnWidget.setStyleSheet(
                UIFunctions.selectMenu(btnWidget.styleSheet()))
        
        # PAGE TEST RESULTS
        elif btnWidget.objectName() in ["btn_test_results","btn_page_test_results"]:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_test_results)
            UIFunctions.resetStyle(self, "btn_test_results")
            UIFunctions.labelPage(self, "Test List")
            btnWidget.setStyleSheet(
                UIFunctions.selectMenu(btnWidget.styleSheet()))
        
        # PAGE I2C CONTROLS
        # elif btnWidget.objectName() in ["btn_i2c_controls","btn_page_i2c_controls"]:
        #     self.ui.stackedWidget.setCurrentWidget(self.ui.page_i2c_controls)
        #     UIFunctions.resetStyle(self, "btn_i2c_controls")
        #     UIFunctions.labelPage(self, "I2C Controls")
        #     btnWidget.setStyleSheet(
        #         UIFunctions.selectMenu(btnWidget.styleSheet()))
        
        # PAGE VIEW LOGS
        # elif btnWidget.objectName() == "btn_view_logs":
        #     self.ui.stackedWidget.setCurrentWidget(self.ui.page_view_logs)
        #     UIFunctions.resetStyle(self, "btn_view_logs")
        #     UIFunctions.labelPage(self, "View Logs")
        #     btnWidget.setStyleSheet(
        #         UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE SAVE / LOAD CONFIGS
        # elif btnWidget.objectName() == "btn_save_load_configs":
        #     self.ui.stackedWidget.setCurrentWidget(
        #         self.ui.page_save_load_configs)
        #     UIFunctions.resetStyle(self, "btn_save_load_configs")
        #     UIFunctions.labelPage(self, "Save / Load Configs")
        #     btnWidget.setStyleSheet(
        #         UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE SETTINGS
        # elif btnWidget.objectName() == "btn_settings":
        #     self.ui.stackedWidget.setCurrentWidget(self.ui.page_settings)
        #     UIFunctions.resetStyle(self, "btn_settings")
        #     UIFunctions.labelPage(self, "Settings")
        #     btnWidget.setStyleSheet(
        #         UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE WIDGETS
        elif btnWidget.objectName() == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_widgets)
            UIFunctions.resetStyle(self, "btn_widgets")
            UIFunctions.labelPage(self, "Custom Widgets")
            btnWidget.setStyleSheet(
                UIFunctions.selectMenu(btnWidget.styleSheet()))

    def resizeFunction(self):
        print('Height: ' + str(self.height()) +\
              ' | Width: ' + str(self.width()))
    
    def mousePressEvent(self, event):
        """Handles updating the drag position"""
        self.dragPos = event.globalPos()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    pixmap = QPixmap("ui\powi_logo_transparent.png")
    splash = QSplashScreen(pixmap)
    splash.show()
    QtGui.QFontDatabase.addApplicationFont('ui/fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('ui/fonts/segoeuib.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/DSEG14ClassicMini-LightItalic.ttf')
    window = MainWindow()
    splash.close()
    window.show_display()
    sys.exit(app.exec_())
