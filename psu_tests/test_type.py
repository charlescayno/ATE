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
    LoadRegulationTest,
    LineRegulationTest,
    EfficiencyTest,
    EfficiencyTest_2Port,
    EfficiencyTest_3Port,
    NoLoadPowerTest,
    CVCCTest,
    # TransientsTest,
    InputHarmonicsTest,
    InputLineRampTest,
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
