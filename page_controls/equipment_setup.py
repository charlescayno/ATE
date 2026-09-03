

from typing import TYPE_CHECKING
from equipment.handler import EquipmentHandler
from sink_controllers.pat_tool import SMBUS_STATE
import sink_controllers.pi_epr_sink as PI_EPR_SINK
from sink_controllers.definitions import SINK_STATE

from PySide2.QtWidgets import QMessageBox, QPushButton
from PySide2.QtCore import QSize

from user_settings.save_load import (write_to_default_config, read_from_default_config,
                                     save_equipment_setup, load_equipment_setup) 
from user_settings.keys import *

if TYPE_CHECKING:
    from main import MainWindow, Ui_MainWindow


# Indicate the availability of the AC source output by changing something in the ui
red_frame = "QFrame{border:2px solid red;	border-radius: 5px;};"
green_frame = "QFrame{border:2px solid green;	border-radius: 5px;};"

class EquipmentSetupPageHandler():
    """ Handles the page for setting up the equipment
    
    """
    def __init__(self, parent):
        self.parent:MainWindow = parent
        self.ui:Ui_MainWindow = self.parent.ui

        self.equipment:EquipmentHandler = self.parent.equipment
        # User Interface Lists
        self.ui_usbpd_sink_list = []
        self.ongoing_sink_update = False
        self.ongoing_ac_source_update = False
        self.ongoing_dc_source_update = False
        self.ongoing_power_meter_update = False
        self.ongoing_eload_update = False

        self.bind_ui_elements()

        self.initialize_ui_values()

        self.check_equipment_availability()
    
    ################################################################################
    #                           USER INTERFACE BINDINGS                            #
    ################################################################################    
    def bind_ui_elements(self):
        self.bind_buttons()
        self.bind_ui_change_events()

    def bind_buttons(self):
        # Detect all GPIB equipment
        self.ui.btn_equip_setup_detect_equipment.clicked.connect(self.detect_equipment)
        
        # Check oscilloscope availability
        self.ui.btn_equip_setup_oscilloscope_check_availability.clicked.connect(
            self.check_oscilloscope_availability)

        # Check USB PD Sink availability
        self.ui.btn_equip_setup_sinkcontroller_check_availability.clicked.connect(
            self.check_usbpd_sink_availability)

        # Default Setup Buttons
        self.btn_equip_setup_save_default = QPushButton("Save as Default Setup", self.ui.frame_equip_setup_settings_contents)
        self.btn_equip_setup_save_default.setMinimumSize(QSize(0, 40))
        self.btn_equip_setup_save_default.setFont(self.ui.btn_equip_setup_previous_pag.font())
        self.btn_equip_setup_save_default.setStyleSheet(self.ui.btn_equip_setup_previous_pag.styleSheet())
        self.btn_equip_setup_save_default.clicked.connect(self.save_default_equipment_setup)

        self.btn_equip_setup_reload_default = QPushButton("Reload Default Setup", self.ui.frame_equip_setup_settings_contents)
        self.btn_equip_setup_reload_default.setMinimumSize(QSize(0, 40))
        self.btn_equip_setup_reload_default.setFont(self.ui.btn_equip_setup_previous_pag.font())
        self.btn_equip_setup_reload_default.setStyleSheet(self.ui.btn_equip_setup_previous_pag.styleSheet())
        self.btn_equip_setup_reload_default.clicked.connect(self.load_default_equipment_setup)

        self.ui.verticalLayout_64.insertWidget(0, self.btn_equip_setup_save_default)
        self.ui.verticalLayout_64.insertWidget(1, self.btn_equip_setup_reload_default)
        self.ui.label_equip_setup_settings_contents.setText("Default Setup & Navigation")
    
    def bind_ui_change_events(self):
        
        self.ui.cbx_equip_setup_sources_acsource.currentIndexChanged.connect(
            self.update_ac_source_info)
        
        self.ui.cbx_equip_setup_sources_dcsource.currentIndexChanged.connect(
            self.update_dc_source_info)
        
        self.ui.cbx_equip_setup_sinkcontroller.currentIndexChanged.connect(
            self.update_sink_controller_info)
        
        self.ui.cbx_equip_setup_i2ccontroller.currentIndexChanged.connect(
            self.update_i2c_controller_info)
        
        self.ui.cbx_equip_setup_power_meter_source.currentIndexChanged.connect(
            self.update_power_meter_roles
        )
        self.ui.cbx_equip_setup_power_meter_load_1.currentIndexChanged.connect(
            self.update_power_meter_roles
        )
        self.ui.cbx_equip_setup_power_meter_load_2.currentIndexChanged.connect(
            self.update_power_meter_roles
        )
        self.ui.cbx_equip_setup_power_meter_load_3.currentIndexChanged.connect(
            self.update_power_meter_roles
        )
        self.ui.cbx_equip_setup_power_meter_load_4.currentIndexChanged.connect(
            self.update_power_meter_roles
        )
        self.ui.cbx_equip_setup_power_meter_load_5.currentIndexChanged.connect(
            self.update_power_meter_roles
        )
        self.ui.cbx_equip_setup_eloads_load_1.currentIndexChanged.connect(
            self.update_eload_roles
        )
        self.ui.cbx_equip_setup_eloads_load_2.currentIndexChanged.connect(
            self.update_eload_roles
        )
        self.ui.cbx_equip_setup_eloads_load_3.currentIndexChanged.connect(
            self.update_eload_roles
        )
        self.ui.cbx_equip_setup_eloads_load_4.currentIndexChanged.connect(
            self.update_eload_roles
        )
        self.ui.cbx_equip_setup_eloads_load_5.currentIndexChanged.connect(
            self.update_eload_roles
        )
        self.ui.cbx_equip_setup_eloads_load_6.currentIndexChanged.connect(
            self.update_eload_roles
        )


    def initialize_ui_values(self):

        oscilloscope_addr = read_from_default_config(
            key=SaveFileKeys.OSCILLOSCOPE_ADDRESS, default_value="")

        if not oscilloscope_addr == "":
            self.ui.lineedit_equip_setup_oscilloscope.setText(oscilloscope_addr)

    def get_current_equipment_setup_dict(self) -> dict:
        """Collect current selections from the UI into a dictionary."""
        config = {
            "ac_source": self.ui.cbx_equip_setup_sources_acsource.currentText(),
            "dc_source": self.ui.cbx_equip_setup_sources_dcsource.currentText(),
            "oscilloscope_address": self.ui.lineedit_equip_setup_oscilloscope.text().strip(),
            "power_meters": {
                "source": self.ui.cbx_equip_setup_power_meter_source.currentText(),
                "load_1": self.ui.cbx_equip_setup_power_meter_load_1.currentText(),
                "load_2": self.ui.cbx_equip_setup_power_meter_load_2.currentText(),
                "load_3": self.ui.cbx_equip_setup_power_meter_load_3.currentText(),
                "load_4": self.ui.cbx_equip_setup_power_meter_load_4.currentText(),
                "load_5": self.ui.cbx_equip_setup_power_meter_load_5.currentText(),
            },
            "electronic_loads": {
                "load_1": self.ui.cbx_equip_setup_eloads_load_1.currentText(),
                "load_2": self.ui.cbx_equip_setup_eloads_load_2.currentText(),
                "load_3": self.ui.cbx_equip_setup_eloads_load_3.currentText(),
                "load_4": self.ui.cbx_equip_setup_eloads_load_4.currentText(),
                "load_5": self.ui.cbx_equip_setup_eloads_load_5.currentText(),
                "load_6": self.ui.cbx_equip_setup_eloads_load_6.currentText(),
            },
            "sink_controller": self.ui.cbx_equip_setup_sinkcontroller.currentText(),
            "i2c_controller": self.ui.cbx_equip_setup_i2ccontroller.currentText(),
        }
        return config

    def save_default_equipment_setup(self):
        """Save the current equipment setup as the persistent default."""
        config = self.get_current_equipment_setup_dict()

        # Save oscilloscope address if present
        if config["oscilloscope_address"]:
            write_to_default_config(
                key=SaveFileKeys.OSCILLOSCOPE_ADDRESS,
                value=config["oscilloscope_address"]
            )

        # Save full setup to shelve and JSON
        save_equipment_setup(config)

        # Update roles in equipment handler
        self.equipment.apply_saved_equipment_roles(config)

        # Provide feedback to user
        msg = QMessageBox(self.parent)
        msg.setWindowTitle("Equipment Setup")
        msg.setText("Default equipment setup has been saved successfully.\nThese settings will be automatically restored on startup.")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def load_default_equipment_setup(self):
        """Load and apply the saved default equipment setup."""
        saved_config = load_equipment_setup()
        if saved_config:
            self.equipment.apply_saved_equipment_roles(saved_config)
            self.ui_update_equipment_combo_boxes()
            if "oscilloscope_address" in saved_config and saved_config["oscilloscope_address"]:
                self.ui.lineedit_equip_setup_oscilloscope.setText(saved_config["oscilloscope_address"])
                self.check_oscilloscope_availability()
            msg = QMessageBox(self.parent)
            msg.setWindowTitle("Equipment Setup")
            msg.setText("Default equipment setup has been loaded and applied.")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
        else:
            msg = QMessageBox(self.parent)
            msg.setWindowTitle("Equipment Setup")
            msg.setText("No saved default equipment setup was found.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def detect_equipment(self):
        """ Check all equipment in all interfaces

        Automatically populate the fields in the UI with the available equipment        
        """
        # Check all equipment in all interfaces
        # Automatically populate the AC source, Power Meters, Eloads 
        # with the available equipment
        self.equipment.update_accessible_equipment()

        self.check_equipment_availability()
    
    def check_equipment_availability(self):
       
        self.check_oscilloscope_availability()
        
        self.check_usbpd_sink_availability()

        saved_config = load_equipment_setup()
        if saved_config:
            applied = self.equipment.apply_saved_equipment_roles(saved_config)
            if not applied:
                self.equipment.auto_set_equipment_roles()
        else:
            self.equipment.auto_set_equipment_roles()

        # Update the combo boxes according to the equipment roles
        self.ui_update_equipment_combo_boxes()

    def ui_update_equipment_combo_boxes(self):
        """ 
        """
        
        self.ui_update_eloads_combo_boxes()
        # self.ui_update_usbpd_sink_combo_box()
        self.ui_update_power_meters_combo_boxes()

        self.ui_update_ac_source_combo_box()

        self.ui_update_dc_source_combo_box()
        
        
    def ui_update_usbpd_sink_combo_box(self):
        if self.equipment.usbpd_sink.status == SINK_STATE.USBPD_SOURCE_CONNECTED:
            pass
        else:
            self.ui_usbpd_sink_list = []

    def ui_update_ac_source_combo_box(self):
        frame = self.ui.frame_equip_setup_sources_acsource
        combo_box = self.ui.cbx_equip_setup_sources_acsource
        
        self.ongoing_ac_source_update = True
        
        combo_box.clear()
        frame.setStyleSheet(red_frame)
        
        for ac_source in self.equipment.ac_sources:
            if ac_source is not None:
                frame.setStyleSheet(green_frame)
                combo_box.addItem(ac_source.description)
        if self.equipment.ac_source is not None:          
            combo_box.setCurrentIndex(self.equipment.ac_sources.index(self.equipment.ac_source))
        
        self.ongoing_ac_source_update = False
                
            
    def update_ac_source_info(self):
        cbx = self.ui.cbx_equip_setup_sources_acsource
        selection = cbx.currentIndex()
        
        # If no item selected
        if selection == -1:
            return
        if self.ongoing_ac_source_update:
            return
        try:
            self.equipment.ac_source = self.equipment.ac_sources[selection]
        except Exception as e:
            print(e)

    def ui_update_dc_source_combo_box(self):
        frame = self.ui.frame_equip_setup_sources_dcsource
        combo_box = self.ui.cbx_equip_setup_sources_dcsource
        
        self.ongoing_dc_source_update = True

        combo_box.clear()
        frame.setStyleSheet(red_frame)
            
        for dc_source in self.equipment.dc_sources:
            if dc_source is not None:
                frame.setStyleSheet(green_frame)
                combo_box.addItem(dc_source.description)
        if self.equipment.dc_source is not None:        
            combo_box.setCurrentIndex(self.equipment.dc_sources.index(self.equipment.dc_source))
        
        self.ongoing_dc_source_update = False
            
    def update_dc_source_info(self):
        cbx = self.ui.cbx_equip_setup_sources_dcsource
        selection = cbx.currentIndex()
        
        # If no item selected
        if selection == -1:
            return
        if self.ongoing_dc_source_update:
            return
        try:
            self.equipment.dc_source = self.equipment.dc_sources[selection]
        except Exception as e:
            print(e)
        
    def ui_update_power_meters_combo_boxes(self):
        """Populate the power meter combo boxes."""
        self.ongoing_power_meter_update = True
        # Group the UI elements
        power_meters_combo_boxes = [
            self.ui.cbx_equip_setup_power_meter_source,
            self.ui.cbx_equip_setup_power_meter_load_1,
            self.ui.cbx_equip_setup_power_meter_load_2,
            self.ui.cbx_equip_setup_power_meter_load_3,
            self.ui.cbx_equip_setup_power_meter_load_4,
            self.ui.cbx_equip_setup_power_meter_load_5,
        ]
        power_meters_frames = [
            self.ui.frame_equip_setup_power_meter_source,
            self.ui.frame_equip_setup_power_meter_load_1,
            self.ui.frame_equip_setup_power_meter_load_2,
            self.ui.frame_equip_setup_power_meter_load_3,
            self.ui.frame_equip_setup_power_meter_load_4,
            self.ui.frame_equip_setup_power_meter_load_5
        ]
        
        # Create a list of the descriptions of all detected power meters
        cbx_items = [pm.description for pm in self.equipment.power_meters if pm is not None]

        current_assigned = [
            self.equipment.power_meter_source,
            self.equipment.power_meter_load_1,
            self.equipment.power_meter_load_2,
            self.equipment.power_meter_load_3,
            self.equipment.power_meter_load_4,
            self.equipment.power_meter_load_5,
        ]
        
        # Populate the combo boxes and select assigned item
        for i, (combo_box, frame) in enumerate(zip(power_meters_combo_boxes, power_meters_frames)):
            combo_box.clear()
            combo_box.addItem('-')
            combo_box.addItems(cbx_items)

            assigned = current_assigned[i]
            if assigned is not None and assigned.description in cbx_items:
                target_idx = cbx_items.index(assigned.description) + 1
                combo_box.setCurrentIndex(target_idx)
                frame.setStyleSheet(green_frame)
            else:
                combo_box.setCurrentIndex(0)
                frame.setStyleSheet(red_frame)

        self.ongoing_power_meter_update = False

    def ui_update_eloads_combo_boxes(self):
        """Populate the Eload combo boxes."""
        self.ongoing_eload_update = True
        # Group the UI elements
        e_loads_combo_boxes = [
            self.ui.cbx_equip_setup_eloads_load_1,
            self.ui.cbx_equip_setup_eloads_load_2,
            self.ui.cbx_equip_setup_eloads_load_3,
            self.ui.cbx_equip_setup_eloads_load_4,
            self.ui.cbx_equip_setup_eloads_load_5,
            self.ui.cbx_equip_setup_eloads_load_6,
        ]
        e_loads_frames = [
            self.ui.frame_equip_setup_eloads_load_1,
            self.ui.frame_equip_setup_eloads_load_2,
            self.ui.frame_equip_setup_eloads_load_3,
            self.ui.frame_equip_setup_eloads_load_4,
            self.ui.frame_equip_setup_eloads_load_5,
            self.ui.frame_equip_setup_eloads_load_6
        ]

        cbx_items = [el.description for el in self.equipment.e_loads if el is not None]

        current_assigned = [
            self.equipment.electronic_load_1,
            self.equipment.electronic_load_2,
            self.equipment.electronic_load_3,
            self.equipment.electronic_load_4,
            self.equipment.electronic_load_5,
            self.equipment.electronic_load_6,
        ]
                
        # Populate the combo boxes and select assigned item
        for i, (combo_box, frame) in enumerate(zip(e_loads_combo_boxes, e_loads_frames)):
            combo_box.clear()
            combo_box.addItem('-')
            combo_box.addItems(cbx_items)

            assigned = current_assigned[i]
            if assigned is not None and assigned.description in cbx_items:
                target_idx = cbx_items.index(assigned.description) + 1
                combo_box.setCurrentIndex(target_idx)
                frame.setStyleSheet(green_frame)
            else:
                combo_box.setCurrentIndex(0)
                frame.setStyleSheet(red_frame)

        self.ongoing_eload_update = False


    
    def check_oscilloscope_availability(self)->bool:
        """Check if the IP address in the UI links to a scope.
        """
        address: str = self.ui.lineedit_equip_setup_oscilloscope.text()
        scope_available: bool = self.equipment.check_scope_availability(address)

        frame = self.ui.frame_equip_setup_oscilloscope_contents
        
        # If scope is available
        if scope_available:
            # Change the border to green
            frame.setStyleSheet(green_frame)
            # Save the oscilloscope to default settings
            write_to_default_config(
                key=SaveFileKeys.OSCILLOSCOPE_ADDRESS, 
                value=address)

            # Get the scope details
            details = self.equipment.oscilloscope.device_id
            self.ui.label_equip_setup_oscilloscope_details.setText(details)
        else:
            # Change the border to red
            frame.setStyleSheet(red_frame)

    def check_usbpd_sink_availability(self):
        self.equipment.update_accessible_sink_controllers()
        self.update_sink_and_i2c_controller_roles()
    
    def update_sink_and_i2c_controller_roles(self):
        # UI
        self.ongoing_sink_update = True
        sink_label_details = self.ui.label_equip_setup_sinkcontrollerdetails
        sink_cbx = self.ui.cbx_equip_setup_sinkcontroller
        i2c_controller_label_details = self.ui.label_equip_setup_i2ccontrollerdetails
        i2c_cbx = self.ui.cbx_equip_setup_i2ccontroller
        frame = self.ui.frame_equip_setup_sinkcontroller_contents
        self.equipment.reset_sink_controller_roles()
        # List of assigned roles
        self.equipment.sink_controller_roles = [
            self.equipment.sink_controller_1,
            self.equipment.sink_controller_2,
            self.equipment.sink_controller_3,
            self.equipment.sink_controller_4,
        ]
        self.equipment.auto_set_sink_controller_roles()
        
        
        # I2C Controllers
        self.equipment.reset_i2c_controller_roles()
        # List of assigned roles
        self.equipment.i2c_controller_roles = [
            self.equipment.i2c_controller_1,
            self.equipment.i2c_controller_2,
            self.equipment.i2c_controller_3,
            self.equipment.i2c_controller_4,
        ]
        self.equipment.auto_set_i2c_controller_roles()
        
        # try:
        #     i2c_controller = self.equipment.i2c_controller
        #     if i2c_controller is not None:
        #         i2c_controller.reset()
        #         i2c_controller.close()
            
        # except Exception as e:
        #     print(e)
        #     pass
        
        sink_controller_available = False
        i2c_controller_available = False
        self.sink_controller_details = []
        sink_cbx.clear()
        # Check EPR Sink Availability
        if len(self.equipment.sink_controllers) > 0:
            sink_controller_available = True
            for sink_controller in self.equipment.sink_controllers:
                self.sink_controller_details.append(sink_controller.details)
                sink_cbx.addItem(sink_controller.description)
            if self.equipment.usbpd_sink is not None:
                idx = sink_cbx.findText(self.equipment.usbpd_sink.description)
                if idx >= 0:
                    sink_cbx.setCurrentIndex(idx)
            
        self.i2c_controller_details = []
        i2c_cbx.clear()

        # Check I2C Controller Availability
        if len(self.equipment.i2c_controllers) > 0: 
            i2c_controller_available = True
            for i2c_controller in self.equipment.i2c_controllers:
                if i2c_controller.connection_status == SMBUS_STATE.CONNECTED:
                    self.i2c_controller_details.append(i2c_controller.details)
                    i2c_cbx.addItem(i2c_controller.description)
            if self.equipment.i2c_controller is not None:
                idx = i2c_cbx.findText(self.equipment.i2c_controller.description)
                if idx >= 0:
                    i2c_cbx.setCurrentIndex(idx)

        # Update the UI frame depending on availability
        if sink_controller_available:
            frame.setStyleSheet(green_frame)
        else:
            frame.setStyleSheet(red_frame)
        self.ongoing_sink_update = False
        
    # def check_usbpd_sink_availability(self):
    #     """Check if USBPD sink is connected"""
    #     usbpd_sink = self.equipment.usbpd_sink
    #     label_details = self.ui.label_equip_setup_sinkcontrollerdetails
    #     cbx_description = self.ui.cbx_equip_setup_sinkcontroller
    #     frame = self.ui.frame_equip_setup_sinkcontroller_contents
    #     usbpd_sink.ping_sink_controller_device()

    #     # If USB PD sink controller is found
    #     if usbpd_sink.usb_pd_sink_connection_ok:
    #         # Show the description of the sink controller
    #         label_details.setText(usbpd_sink.details)
    #         cbx_description.clear()
    #         cbx_description.addItem(usbpd_sink.description)
    #         # Change the border of the frame to green
    #         frame.setStyleSheet(green_frame)
        
    #     # If USB PD sink is not found
    #     else:
    #         # Clear the label
    #         label_details.clear()
    #         # Set the frame to red
    #         frame.setStyleSheet(red_frame)
        
    # def check_i2c_controller_availability(self):
    #     """Check if I2C controller is connected"""
    #     i2c_controller = self.equipment.i2c_controller
    #     label_details = self.ui.label_equip_setup_sinkcontrollerdetails
    #     cbx_description = self.ui.cbx_equip_setup_sinkcontroller

    #     frame = self.ui.frame_equip_setup_sinkcontroller_contentB
    #     i2c_controller.open()

    #     if i2c_controller.connection_status == SMBUS_STATE.CONNECTED:
    #         cbx_description.addItem(i2c_controller.description)

    def update_sink_controller_info(self):
        cbx = self.ui.cbx_equip_setup_sinkcontroller
        label_details = self.ui.label_equip_setup_sinkcontrollerdetails
        selection = cbx.currentIndex()
        
        # If no item selected
        if selection == -1:
            label_details.setText("")
            return
        
        label_details.setText(self.sink_controller_details[selection])
        
        if self.ongoing_sink_update:
            return
        try:
            # Change active sink controller
            self.equipment.usbpd_sink.close()
        except Exception as e:
            print(e)
        try:
            new_sink_controller = self.equipment.sink_controllers.pop(selection)
            self.equipment.sink_controllers.insert(0,new_sink_controller)
            self.equipment.usbpd_sink = self.equipment.sink_controllers[0]
            self.update_sink_and_i2c_controller_roles()
            self.equipment.usbpd_sink.usb_pd_initialize()
            if self.equipment.usbpd_sink.status == SINK_STATE.SINK_DISCONNECTED:
                raise ConnectionError('USB-PD Sink is not connected')
            self.equipment.usbpd_sink.close()   
        except Exception as e:
            print(e)
            self.equipment.usbpd_sink = None
            self.check_usbpd_sink_availability()
        else:
            label_details.setText(self.sink_controller_details[0])   
        
    def update_i2c_controller_info(self):
        cbx = self.ui.cbx_equip_setup_i2ccontroller
        label_details = self.ui.label_equip_setup_i2ccontrollerdetails
        selection = cbx.currentIndex()
        
        # If no item selected
        if selection == -1:
            label_details.setText("")
            return
        
        label_details.setText(self.i2c_controller_details[selection])
        
        if self.ongoing_sink_update:
            return     
        try: 
            # Change active i2c controller
            self.equipment.i2c_controller.close()
        except Exception as e:
            print(e)
        try:
            new_i2c_controller = self.equipment.i2c_controllers.pop(selection)
            self.equipment.i2c_controllers.insert(0,new_i2c_controller)
            self.equipment.i2c_controller = self.equipment.i2c_controllers[0]
            self.update_sink_and_i2c_controller_roles()
            self.equipment.i2c_controller.reset()
            self.equipment.i2c_controller.close()
        except Exception as e:
            print(e)
            self.equipment.i2c_controller = None
            self.check_usbpd_sink_availability()
        else:
            label_details.setText(self.i2c_controller_details[0])
        
    def update_power_meter_roles(self):
        if self.ongoing_power_meter_update:
            return

        power_meters_combo_boxes = [
            self.ui.cbx_equip_setup_power_meter_source,
            self.ui.cbx_equip_setup_power_meter_load_1,
            self.ui.cbx_equip_setup_power_meter_load_2,
            self.ui.cbx_equip_setup_power_meter_load_3,
            self.ui.cbx_equip_setup_power_meter_load_4,
            self.ui.cbx_equip_setup_power_meter_load_5,
        ]
        power_meters_frames = [
            self.ui.frame_equip_setup_power_meter_source,
            self.ui.frame_equip_setup_power_meter_load_1,
            self.ui.frame_equip_setup_power_meter_load_2,
            self.ui.frame_equip_setup_power_meter_load_3,
            self.ui.frame_equip_setup_power_meter_load_4,
            self.ui.frame_equip_setup_power_meter_load_5
        ]

        self.equipment.reset_power_meter_roles()
        self.power_meter_roles = [None] * 6

        for i, (combo_box, frame) in enumerate(zip(power_meters_combo_boxes, power_meters_frames)):
            text = combo_box.currentText()
            assigned_pm = None
            if text and text != '-':
                for pm in self.equipment.power_meters:
                    if pm is not None and pm.description == text:
                        assigned_pm = pm
                        break

            self.power_meter_roles[i] = assigned_pm
            if assigned_pm is not None:
                frame.setStyleSheet(green_frame)
            else:
                frame.setStyleSheet(red_frame)

        self.equipment.power_meter_source = self.power_meter_roles[0]
        self.equipment.power_meter_load_1 = self.power_meter_roles[1]
        self.equipment.power_meter_load_2 = self.power_meter_roles[2]
        self.equipment.power_meter_load_3 = self.power_meter_roles[3]
        self.equipment.power_meter_load_4 = self.power_meter_roles[4]
        self.equipment.power_meter_load_5 = self.power_meter_roles[5]
        self.equipment.power_meter_roles = self.power_meter_roles
        
    def update_eload_roles(self):
        if self.ongoing_eload_update:
            return

        e_loads_combo_boxes = [
            self.ui.cbx_equip_setup_eloads_load_1,
            self.ui.cbx_equip_setup_eloads_load_2,
            self.ui.cbx_equip_setup_eloads_load_3,
            self.ui.cbx_equip_setup_eloads_load_4,
            self.ui.cbx_equip_setup_eloads_load_5,
            self.ui.cbx_equip_setup_eloads_load_6,
        ]
        e_loads_frames = [
            self.ui.frame_equip_setup_eloads_load_1,
            self.ui.frame_equip_setup_eloads_load_2,
            self.ui.frame_equip_setup_eloads_load_3,
            self.ui.frame_equip_setup_eloads_load_4,
            self.ui.frame_equip_setup_eloads_load_5,
            self.ui.frame_equip_setup_eloads_load_6
        ]

        self.equipment.reset_electronic_load_roles()
        self.eload_roles = [None] * 6

        for i, (combo_box, frame) in enumerate(zip(e_loads_combo_boxes, e_loads_frames)):
            text = combo_box.currentText()
            assigned_el = None
            if text and text != '-':
                for el in self.equipment.e_loads:
                    if el is not None and el.description == text:
                        assigned_el = el
                        break

            self.eload_roles[i] = assigned_el
            if assigned_el is not None:
                frame.setStyleSheet(green_frame)
            else:
                frame.setStyleSheet(red_frame)

        self.equipment.electronic_load_1 = self.eload_roles[0]
        self.equipment.electronic_load_2 = self.eload_roles[1]
        self.equipment.electronic_load_3 = self.eload_roles[2]
        self.equipment.electronic_load_4 = self.eload_roles[3]
        self.equipment.electronic_load_5 = self.eload_roles[4]
        self.equipment.electronic_load_6 = self.eload_roles[5]
        self.equipment.electronic_load_roles = self.eload_roles
        
        