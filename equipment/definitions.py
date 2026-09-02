from equipment.eload_specs import *
from equipment.ac_source_specs import *
from equipment.dc_source_specs import *
from equipment.power_meter_specs import *

class EquipmentType:
    AC_SOURCE = 1
    DC_SOURCE = 2
    ELECTRONIC_LOAD = 3
    ELECTRONIC_LOAD_MAINFRAME = 4
    POWER_METER = 5 
    OSCILLOSCOPE = 6
    USBPD_SINK = 7


################################################################################
#                           EQUIPMENT MODEL NUMBERS                            #
################################################################################


AC_SOURCE_LIST = {
    '6812A' :ACSourceAgilent,
    '6812B' :ACSourceAgilent,
    '6813B' :ACSourceAgilent,
    '6812C' :ACSourceAgilent,
    '61501' :ACSourceChroma,
    '61502' :ACSourceChroma,
    '61503' :ACSourceChroma,
    '61504' :ACSourceChroma,
    'IT7803J-350-30U' :ACSourceIT7800,
}

DC_SOURCE_LIST = {
    ' SL1000-1.5' :DCSourceMagnaPower,
}

POWER_METER_LIST = {
    '760401'    :PowerMeterWT210, #WY210
    '760503'    :PowerMeterWT210, #WT230
    'WT310'     :PowerMeterWT310, #WT310
    'WT310E'    :PowerMeterWT310, #WT310E
    '760202'    :PowerMeterWT500, #WT500
    'Chroma'    :PowerMeterChroma, #Need to update IDN
}

ELECTRONIC_LOAD_MAINFRAME_LIST = [
    '6310',
    '6314',
    '6314A',
    '6312',
    '6312A',
    '6332A',
    '6334A',
    '6632',
    '6334',
    '63600-2',
    '63203A-600-210'
]

# Group Eload module by same programming syntax
ELOAD_MODULE_GROUP1_LIST = [
    Chroma63113A,
    Chroma63108A,
    Chroma63108A,
    Chroma63110A,
    Chroma63110A,
    Chroma63103A,
    Chroma63103A,
    Chroma63303A,
    Chroma63303,
    Chroma63302,
]

ELOAD_MODULE_GROUP2_LIST = {
    Chroma63112A,
    Chroma63203A_600_210,
    Chroma63630_600_15,
    Chroma63640_80_80,
}

ELECTRONIC_LOAD_MODULES_PROG_LIST = {
    Chroma63113A            :Eload_Chroma_Prog_Group1,
    Chroma63113A            :Eload_Chroma_Prog_Group1,
    Chroma63108A            :Eload_Chroma_Prog_Group1,
    Chroma63108A            :Eload_Chroma_Prog_Group1,
    Chroma63110A            :Eload_Chroma_Prog_Group1,
    Chroma63110A            :Eload_Chroma_Prog_Group1,
    Chroma63103A            :Eload_Chroma_Prog_Group1,
    Chroma63103A            :Eload_Chroma_Prog_Group1,
    Chroma63303A            :Eload_Chroma_Prog_Group1,
    Chroma63303             :Eload_Chroma_Prog_Group1,
    Chroma63302             :Eload_Chroma_Prog_Group1,
    Chroma63112A            :Eload_Chroma_Prog_Group2,
    Chroma63640_80_80       :Eload_Chroma_Prog_Group2,
    Chroma63630_600_15      :Eload_Chroma_Prog_Group2,
    Chroma63203A_600_210    :Eload_Chroma_Prog_Group2,
}

ELECTRONIC_LOAD_MODULES_LIST = {
    '63113A'        :Chroma63113A,
    '63113'         :Chroma63113A,
    '63108A'        :Chroma63108A,
    '63108'         :Chroma63108A,
    '63110A'        :Chroma63110A,
    '63110'         :Chroma63110A,
    '63103A'        :Chroma63103A,
    '63103'         :Chroma63103A,
    '63303A'        :Chroma63303A,
    '63303'         :Chroma63303,
    '63302'         :Chroma63302,
    '63640-80-80'   :Chroma63640_80_80,
    '63630-600-15'   :Chroma63630_600_15,
    '63203A-600-210' :Chroma63203A_600_210,
    '63112A'         :Chroma63112A,
}

ELECTRONIC_LOAD_63600_MODULE_LIST = [
    Chroma63640_80_80,
    Chroma63630_600_15,
]

ELECTRONIC_LOAD_LIST = [

]

OSCILLOSCOPE_LIST = [
    'RTO2004',
    'RTO1004',
    'RTO6',
]

