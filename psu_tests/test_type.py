from psu_tests.test_load_reg import LoadRegulationTest
from psu_tests.test_line_reg import LineRegulationTest
from psu_tests.test_efficiency import EfficiencyTest
from psu_tests.test_efficiency_2port import EfficiencyTest_2Port
from psu_tests.test_efficiency_3port import EfficiencyTest_3Port
from psu_tests.test_no_load import NoLoadPowerTest
from psu_tests.test_cvcc import CVCCTest
from psu_tests.test_input_harmonics import InputHarmonicsTest
from psu_tests.test_input_line_ramp import InputLineRampTest
from psu_tests.test_i2c_cv_sweep import I2C_CVSweepTest
from psu_tests.test_i2c_vkp_test import I2C_VKPTest
from psu_tests.test_i2c_cc_test import I2C_CCTest
from psu_tests.test_file_template import TemplateTest
from psu_tests.test_i2c_load_reg import I2C_LoadRegTest
from psu_tests.test_i2c_line_reg import I2C_LineRegTest
from psu_tests.test_i2c_efficiency import I2C_EfficiencyTest
from psu_tests.test_i2c_line_sense import I2C_LineSenseTest
from psu_tests.test_pfc_load_reg import PFC_LoadRegTest
from psu_tests.test_load_reg_2port import LoadRegulationTest_2Port
from psu_tests.test_light_load import LightLoad
from psu_tests.test_vds_ids_steady_state import VdsIdsSteadyStateTest, SteadyStateWaveformCaptureTest
from psu_tests.test_efficiency_modern import ModernEfficiencyTest
from psu_tests.test_efficiency_2port_waveform import EfficiencyWaveformTest_2Port
from psu_tests.test_steady_state_poll_2port_waveform import SteadyStatePollWaveformTest_2Port
from psu_tests.test_startup_2port_waveform import StartupWaveformTest_2Port
from psu_tests.test_startup_ac_turnon_waveform import StartupWaveformTest_ACTurnOn

###############################################################################
# Add each test to this list to include it in the setup
###############################################################################
I2C_TestTypes = [
#     I2C_LoadRegTest,
#     I2C_LineRegTest,
#     I2C_EfficiencyTest,
#     I2C_CVSweepTest,
#     I2C_VKPTest,
#     I2C_CCTest,
#     I2C_LineSenseTest,
#     PFC_LoadRegTest,
]

InnoPro_TestTypes = [
#     I2C_LoadRegTest,
#     I2C_LineRegTest,
#     I2C_EfficiencyTest,
#     I2C_CVSweepTest,
#     I2C_VKPTest,
#     I2C_CCTest,
#     I2C_LineSenseTest,
]

TestTypes = [
    # Dual-output / 2-port tests (grouped at top of Add Tests dropdown)
    EfficiencyWaveformTest_2Port,
    SteadyStatePollWaveformTest_2Port,
    StartupWaveformTest_2Port,
    StartupWaveformTest_ACTurnOn,
    EfficiencyTest_2Port,
    EfficiencyTest_3Port,
    LoadRegulationTest,
    LineRegulationTest,
    EfficiencyTest,
    NoLoadPowerTest,
    CVCCTest,
    # TransientsTest,
    InputHarmonicsTest,
    InputLineRampTest,
    VdsIdsSteadyStateTest,
    # ModernEfficiencyTest,
    # LoadRegulationTest_2Port,
    # LightLoad,
]
# ] + I2C_TestTypes



CVCC_TestTypes = [
    CVCCTest,
    # I2C_VKPTest,
    # I2C_CCTest,
]


def get_test_type(index):
    """Return the TestType that corresponds to the input index."""
    return TestTypes[index]

def get_test_title_list():
    """Return a list of titles of the defined test types"""
    test_title_list = []
    for test in TestTypes:
        test_title_list.append(test.title)
    
    return test_title_list

def get_test_title(index):
    """Return the test title of the TestType that corresponds to the input index"""
    return TestTypes[index].title


def resolve_test_type_index(stored_index: int, test_title: str | None = None) -> int:
    """Map a saved index and/or title to the current TestTypes order."""
    titles = get_test_title_list()
    if test_title:
        legacy = {
            "Primary Vds & Ids Steady-State": "Steady-State Waveform Capture",
            "Efficiency 2 Port (Waveform)": "Steady-State Waveform 2 Port",
        }
        test_title = legacy.get(test_title, test_title)
        if test_title in titles:
            return titles.index(test_title)
    if 0 <= stored_index < len(TestTypes):
        return stored_index
    return 0
