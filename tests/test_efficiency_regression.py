import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
from psu_tests.test_efficiency import EfficiencyTest

class MockEquipment:
    def __init__(self):
        self.ac_source = MagicMock()
        self.dc_source = MagicMock()
        self.power_meter_source = MagicMock()
        self.power_meter_load_1 = MagicMock()
        self.electronic_load_1 = MagicMock()
        self.usbpd_sink = MagicMock()
        self.oscilloscope = MagicMock()

@pytest.fixture
def mock_equipment():
    return MockEquipment()

@pytest.fixture
def mock_efficiency_test(mock_equipment):
    # Minimal initial kwargs to pass __init__ in BaseTestObject
    test = EfficiencyTest(
        test_item=MagicMock(),
        equipment=mock_equipment,
        parent=MagicMock()
    )
    # Assign necessary attributes
    test.vout_V = 5.0
    test.nominal_load_current_A = 2.0
    test.i_max_A = 2.0
    test.vin_list = [(115, 60), (230, 50)]
    test.iout_list_A = [2.0, 1.5, 1.0, 0.5, 0.2]
    test.load_pct_list = [100, 75, 50, 25, 10]
    test.coupling = 1 # AC coupling enum value
    test.use_eload_data = False
    test.usbpd_test = False
    test.tracking_pdo_requests = False
    test.eload_type = "CC"
    test.soak_time = MagicMock()
    
    # Mock methods that interact with UI or Excel
    test.status_report = MagicMock()
    test.update_status_log = MagicMock()
    test.create_new_plot_series = MagicMock()
    test.correct_source_output = MagicMock()
    test.process_data_row = MagicMock(return_value=[115,60,5.0,2.0,10.0,0.5,12.0,83.3,1.0])
    test.update_output_data = MagicMock()
    test.save_temp_data = MagicMock()
    
    # Mock dataframes
    test.output_dataframe = pd.DataFrame(columns=['Vin(V)','Freq(Hz)','Vout(V)','Iout(A)','Pout(W)','PF','Pin(W)','Efficiency','THD'])
    test.efficiency_dataframe = pd.DataFrame(columns=['Avg_Eff','DOE6 Limit', 'COC5 T2 Limit', 'COC5_T2_10%','Pass/Fail'])
    test.test_data_table = MagicMock()
    
    return test

def test_efficiency_run_with_missing_equipment(mock_efficiency_test):
    # Test setting missing equipment to None to verify AttributeError regression (TST-306)
    mock_efficiency_test.equipment.power_meter_load_1 = None
    mock_efficiency_test.equipment.power_meter_source = None
    mock_efficiency_test.equipment.electronic_load_1 = None
    
    # Run setup
    mock_efficiency_test.setup_equipment()
    mock_efficiency_test.setup_data_file()
    
    # This should not raise an AttributeError due to NoneType object not having a method
    # It might hit other snags down the line depending on how far the loop goes without equipment,
    # but we are verifying it doesn't crash specifically on `auto_range_enable` or `set_load` calls.
    
    try:
        mock_efficiency_test.test_loop()
    except Exception as e:
        if isinstance(e, AttributeError) and "NoneType" in str(e):
            pytest.fail(f"Regression failed: Hit NoneType AttributeError: {e}")
        # We expect some logic to fail if we go deep because we stubbed things heavily,
        # but as long as it's not the AttributeError on NoneType for equipment, the fix works.
