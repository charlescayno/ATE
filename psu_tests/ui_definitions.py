from page_controls.definitions import *

class I2C_UI_Definitions:
    """
    
    Multiple Line Edits
    Multiple combo boxes
    
    """
    
    # Dependent on how many are defined in UI
    num_line_edit = 10
    num_cbx = 4

    def __init__(self):
        
        self.lineedit_visibility_flags = [False]*self.num_line_edit
        self.lineedit_label_texts = ['']*self.num_line_edit
        
        self.cbx_visibility_flags = [False]*self.num_cbx
        self.cbx_label_texts = ['']*self.num_cbx
        self.cbx_contents = [None]*self.num_cbx

    def add_lineedit(self, label: str, param_index: int):
        """ Configure a lineedit to show on the UI params widget

        Keyword Arguments:
        label       :       Label associated with line edit
        param_index :       (1-10)
        """
        self.lineedit_visibility_flags[param_index-1] = True
        self.lineedit_label_texts[param_index-1] = label

    def add_cbx(self, label, contents, param_index):
        """ Configure a combo box to show on the UI params widget

        Keyword Arguments:
        label       :       Label associated with line edit
        contents    :       items of the combo box
        param_index :       (1-4)
        """
        self.cbx_visibility_flags[param_index-1] = True
        self.cbx_label_texts[param_index-1] = label
        self.cbx_contents[param_index-1] = contents
    
    def sub_lineedit(self,param_index: int):
        """ Configure a lineedit to be hidden on the UI params widget

        Keyword Arguments:
        param_index :       (1-10)
        """
        self.lineedit_visibility_flags[param_index-1] = False
        self.lineedit_label_texts[param_index-1] = ''

    def sub_cbx(self, param_index):
        """ Configure a combo box to be hidden on the UI params widget

        Keyword Arguments:
        label       :       Label associated with line edit
        contents    :       items of the combo box
        param_index :       (1-4)
        """
        self.cbx_visibility_flags[param_index-1] = False
        self.cbx_label_texts[param_index-1] = ''
        self.cbx_contents[param_index-1] = None


class General_UI_Definitions:
    """
    Definition of the UI values to be used per test
    """
    # Stacked widget
    stack_page_1 = StackWidget1Pages.EmptyPage  # Upper Stackable Widget
    stack_page_2 = StackWidget2Pages.EmptyPage  # Lower Stackable Widget
    stack_page_3 = StackWidget3Pages.EmptyPage  # Middle Stackable Widget

    # Frames Visibility
    test_time_params_frame_visible = True

    # Test time parameters
    test_time_param1_label = 'Initial Soak (s)'
    test_time_param2_label = 'Soak Per Line (s)'
    test_time_param3_label = 'Soak Per Load (s)'
    test_time_param4_label = 'Integration Time (s)'
    test_time_param1_visible = True
    test_time_param2_visible = True
    test_time_param3_visible = True
    test_time_param4_visible = True

    # USB PD Page
    usb_pd_device_toggle_visible = False
    nominal_vout_visible = True
    nominal_vout_enable = False
    nominal_iout_visible = False
    usbpd_getsourcecaps_btn_visible = False
    usbpd_sourcecaps_table_visible = False
    usbpd_tracking_pdo_chk_visible = False

    # General Options
    load_type_visible = False
    measure_ripple_visible = False
    use_eload_data_toggle_visible = True
    coupling_visible = True

    # Add test buttons
    add_test_button_1_txt = 'Add Test'
    add_test_button_2_txt = 'Add Test'
    add_test_button_1_visible = True
    add_test_button_2_visible = False

    # Load Range options
    load_range_selection_enabled = True
    load_direction_cbx_enabled = True
    
    # CVCC field multiple setpoint button
    multiple_cvcc_setpoints_enable = False

class UIChangeFlags:
    """Container class for the flags used for UI modification."""
    usb_pd_device_toggle_checked = False
    

class General_UI_Update_Definitions:
    """
    Definition of the UI values to be used when updating the test conditions during test item selection
    """
    
    line_settings_update = True
    load_settings_update = True
    soaktime_settings_update = True
    cvcc_settings_update = False
    line_ramp_settings_update = False
    
    nominal_output_settings_update = True
    
    usbpd_options_update = True
    tracking_pdo_request_update = True
    
    measure_ripple_update = False
    load_direction_update = True
    eload_type_update = True
    use_eload_data_update = True
    coupling_update = True
    
    i2c_params_update = False
    



