class ELoadTypes:
    """Types of loading that are available on the specific models."""
    CC = 'CC'
    CR = 'CR'
    CV = 'CV'
    CP = 'CP'
    LED = 'LED'

class EloadStatus:
    OFF = '0'
    ON = '1'
    
class Eload_Chroma_Prog_Group1():
    channel = "CHAN"
    config = "CONF"
    mode = "MODE"
    fetch = "FETC"
    load = "LOAD"
    level = "L"
    current_static = "CURR:STAT"
    current_dynamic = "CURR:DYN"
    current_dynamic_duration = "CURR:DYN:T"
    resistance = "RES"
    power = "POW:STAT"
    led = "LED"
    led_voltage = "LED:VO"
    led_current = "LED:IO"
    voltage = "VOLT"
    cv_current = "VOLT:CURR"
    rise = "RISE"
    fall = "FALL"
    short = 'SHOR'
    
class Eload_Chroma_Prog_Group2():
    channel = "CHAN"
    config = "CONF"
    mode = "MODE"
    fetch = "FETC"
    load = "LOAD"
    level = "L"
    current_static = "CURR:STAT"
    current_dynamic = "CURR:DYN"
    current_dynamic_duration = "CURR:DYN:T"
    resistance = "RES:STAT"
    power = "POW:STAT"
    led = "LED"
    led_voltage = "LED:VO"
    led_current = "LED:IO"
    voltage = "VOLT:STAT"
    cv_current = "VOLT:STAT:ILIM"
    rise = "RISE"
    fall = "FALL"
    short = 'SHOR'

class EloadModuleBaseClass():
    """ Used only for type hint
    """
    # Mode range count
    MODE_RANGE_COUNT = 3
    
    # CR Mode slew rate availability
    CR_SLEW_AVAILABLE = True
    
    # CP Mode slew rate unit
    CP_SLEW_UNIT = 'W / µs'
    
    # SLEW RATE LIMITS
    H_SLEW_MIN = 0
    H_SLEW_MAX = 0
    M_SLEW_MIN = 0
    M_SLEW_MAX = 0
    L_SLEW_MIN = 0
    L_SLEW_MAX = 0 

    # CCX MODE LIMITS
    CCH_MAX_A = 0
    CCM_MAX_A = 0
    CCL_MAX_A = 0
    CCH_MAX_POWER_W = 0
    CCM_MAX_POWER_W = 0
    CCL_MAX_POWER_W = 0

    # CR
    CRH_MIN_R = 0
    CRH_MAX_R = 0
    
    CRM_MIN_R = 0
    CRM_MAX_R = 0 

    CRL_MIN_R = 0
    CRL_MAX_R = 0 
    
    CRL_MAX_V = 0
    CRM_MAX_V = 0
    CRH_MAX_V = 0
    
    CRL_MAX_A = CCH_MAX_A
    CRM_MAX_A = CCM_MAX_A
    CRH_MAX_A = CCL_MAX_A
    
    # CP
    CPL_MIN_W = 0
    CPL_MAX_W = 0
    CPM_MIN_W = 0
    CPM_MAX_W = 0
    CPH_MIN_W = 0
    CPH_MAX_W = 0
    
    CPL_SLEW_MIN = 0
    CPL_SLEW_MAX = 0
    
    CPM_SLEW_MIN = 0
    CPM_SLEW_MAX = 0
    
    CPH_SLEW_MIN = 0
    CPH_SLEW_MAX= 0
    
    # CCD
    CCD_T_MIN_S = 0
    CCD_T_MAX_S = 0

    CV_MAX_V = 0

    MULTI_CHANNEL = False

    MODES = [ELoadTypes.CC,
            ELoadTypes.CR,
            ELoadTypes.CV,
            ELoadTypes.CP,
            ELoadTypes.LED]

class Chroma63113A():

    # Mode range count
    MODE_RANGE_COUNT = 2
    
    # CR Mode slew rate availability
    CR_SLEW_AVAILABLE = True
    
    # CP Mode slew rate unit
    CP_SLEW_UNIT = 'W / µs'
        
    # SLEW RATE LIMITS
    H_SLEW_MIN = 3.2E-3
    H_SLEW_MAX = 800E-3
    L_SLEW_MIN = 0.8E-3
    L_SLEW_MAX = 200E-3

    # CCX MODE LIMITS
    CCH_MAX_A = 20
    CCL_MAX_A = 5
    CCH_MAX_POWER_W = 300
    CCL_MAX_POWER_W = 300

    # CR
    CRH_MIN_R = 4
    CRH_MAX_R = 4000

    CRL_MIN_R = 0.2
    CRL_MAX_R = 200 
    
    CRL_MAX_V = 60
    CRH_MAX_V = 300
    
    CRL_MAX_A = CCH_MAX_A
    CRH_MAX_A = CCL_MAX_A
    
    # CCD
    CCD_T_MIN_S = 25E-6
    CCD_T_MAX_S = 50

    CV_MAX_V = 300

    MULTI_CHANNEL = False

    MODES = [ELoadTypes.CC,
            ELoadTypes.CR,
            ELoadTypes.CV,
            ELoadTypes.LED]
    
class Chroma63112A():

    # Mode range count
    MODE_RANGE_COUNT = 2
    
    # CR Mode slew rate availability
    CR_SLEW_AVAILABLE = True
    
    # CP Mode slew rate unit
    CP_SLEW_UNIT = 'W / µs'
        
    # SLEW RATE LIMITS
    H_SLEW_MIN = 40E-3
    H_SLEW_MAX = 10
    L_SLEW_MIN = 4E-3
    L_SLEW_MAX = 1

    # CCX MODE LIMITS
    CCH_MAX_A = 240
    CCL_MAX_A = 24
    CCH_MAX_POWER_W = 1200
    CCL_MAX_POWER_W = 120

    # CR
    CRH_MIN_R = 0.3125
    CRH_MAX_R = 1250

    CRL_MIN_R = 6.25E-3
    CRL_MAX_R = 25
    
    CRL_MAX_V = 16
    CRH_MAX_V = 80
    
    CRL_MAX_A = CCH_MAX_POWER_W/CRL_MAX_V
    CRH_MAX_A = CCH_MAX_POWER_W/CRH_MAX_V
    
    # CP
    CPL_MIN_W = 0
    CPL_MAX_W = 120
    CPH_MIN_W = 0
    CPH_MAX_W = 1200
    
    CPL_SLEW_MIN = 0.02
    CPL_SLEW_MAX = 5
    
    CPH_SLEW_MIN = 0.2
    CPH_SLEW_MAX= 50
    
    # CCD
    CCD_T_MIN_S = 25E-6
    CCD_T_MAX_S = 50

    CV_MAX_V = 80

    MULTI_CHANNEL = False

    MODES = [ELoadTypes.CC,
            ELoadTypes.CR,
            ELoadTypes.CV,
            ELoadTypes.CP]
    
class Chroma63203A_600_210():

     # Mode range count
    MODE_RANGE_COUNT = 3
    
    # CR Mode slew rate availability
    CR_SLEW_AVAILABLE = True
    
    # CP Mode slew rate unit
    CP_SLEW_UNIT = 'A / µs'
       
    # SLEW RATE LIMITS
    H_SLEW_MIN = 0.002
    H_SLEW_MAX = 9
    M_SLEW_MIN = 0.001
    M_SLEW_MAX = 4.5
    L_SLEW_MIN = 0.0002
    L_SLEW_MAX = 0.9

    # CCX MODE LIMITS
    CCH_MAX_A = 210
    CCM_MAX_A = 105
    CCL_MAX_A = 21
    CCH_MAX_POWER_W = 3000
    CCM_MAX_POWER_W = 3000
    CCL_MAX_POWER_W = 3000

    # CR
    CRH_MIN_R = 4
    CRH_MAX_R = 8000
    
    CRM_MIN_R = 0.4
    CRM_MAX_R = 4000

    CRL_MIN_R = 0.1
    CRL_MAX_R = 1000
    
    CRL_MAX_V = 80
    CRM_MAX_V = 150
    CRH_MAX_V = 600
    
    CRL_MAX_A = CCH_MAX_POWER_W/CRL_MAX_V
    CRM_MAX_A = CCH_MAX_POWER_W/CRL_MAX_V
    CRH_MAX_A = CCH_MAX_POWER_W/CRH_MAX_V
    
    # CP
    CPL_MIN_W = 0
    CPL_MAX_W = 300
    CPM_MIN_W = 0
    CPM_MAX_W = 1500
    CPH_MIN_W = 0
    CPH_MAX_W = 3000
    
    CPH_SLEW_MIN = 0.002
    CPH_SLEW_MAX = 9
    CPM_SLEW_MIN = 0.001
    CPM_SLEW_MAX = 4.5
    CPL_SLEW_MIN = 0.0002
    CPL_SLEW_MAX = 0.9
    
    # CCD
    CCD_T_MIN_S = 10E-6
    CCD_T_MAX_S = 99

    CV_MAX_V = 600

    MULTI_CHANNEL = False

    MODES = [ELoadTypes.CC,
            ELoadTypes.CR,
            ELoadTypes.CV,
            ELoadTypes.CP]

class Chroma63108A():
    
    # Mode range count
    MODE_RANGE_COUNT = 2
    
    # CR Mode slew rate availability
    CR_SLEW_AVAILABLE = True
    
    # CP Mode slew rate unit
    CP_SLEW_UNIT = 'W / µs'
       
    # SLEW RATE LIMITS
    H_SLEW_MIN = 3.2E-3
    H_SLEW_MAX = 800E-3
    L_SLEW_MIN = 0.32E-3
    L_SLEW_MAX = 80E-3

    # CCX MODE LIMITS
    CCH_MAX_A = 20
    CCL_MAX_A = 5
    CCH_MAX_POWER_W = 600
    CCL_MAX_POWER_W = 60

    # CR
    CRH_MIN_R = 4
    CRH_MAX_R = 4000

    CRL_MIN_R = 0.2
    CRL_MAX_R = 200 
    
    CRL_MAX_V = 125
    CRH_MAX_V = 500
    
    CRL_MAX_A = CCH_MAX_A
    CRH_MAX_A = CCL_MAX_A
    
    # CP
    CPL_MIN_W = 0
    CPL_MAX_W = 60
    CPH_MIN_W = 0
    CPH_MAX_W = 600
    
    CPL_SLEW_MIN = 0.0096
    CPL_SLEW_MAX = 2.4
    
    CPH_SLEW_MIN = 0.096
    CPH_SLEW_MAX= 24
    
    # CCD
    CCD_T_MIN_S = 25E-6
    CCD_T_MAX_S = 50

    CV_MAX_V = 300

    MULTI_CHANNEL = False

    MODES = [ELoadTypes.CC,
            ELoadTypes.CR,
            ELoadTypes.CV,
            ELoadTypes.CP]

class Chroma63110A():
    
    # Mode range count
    MODE_RANGE_COUNT = 2
    
    # CR Mode slew rate availability
    CR_SLEW_AVAILABLE = True
    
    # CP Mode slew rate unit
    CP_SLEW_UNIT = 'W / µs'

    # SLEW RATE LIMITS
    H_SLEW_MIN = 0
    H_SLEW_MAX = 0
    L_SLEW_MIN = 0
    L_SLEW_MAX = 0 

    # CCX MODE LIMITS
    CCH_MAX_A = 2
    CCL_MAX_A = 0.6
    CCH_MAX_POWER_W = 100
    CCL_MAX_POWER_W = 100

    # CR
    CRH_MIN_R = 10
    CRH_MAX_R = 10000

    CRL_MIN_R = 3
    CRL_MAX_R = 4000
    
    CRL_MAX_V = 100
    CRH_MAX_V = 500
    
    CRL_MAX_A = CCH_MAX_A
    CRH_MAX_A = CCL_MAX_A
    
    # CCD
    CCD_T_MIN_S = 25E-6
    CCD_T_MAX_S = 50

    CV_MAX_V = 500

    MULTI_CHANNEL = True

    MODES = [ELoadTypes.CC,
            ELoadTypes.CR,
            ELoadTypes.CV,
            ELoadTypes.LED]

class Chroma63103A():

    # Mode range count
    MODE_RANGE_COUNT = 2
    
    # CR Mode slew rate availability
    CR_SLEW_AVAILABLE = True
    
    # CP Mode slew rate unit
    CP_SLEW_UNIT = 'W / µs'
       
    # SLEW RATE LIMITS
    H_SLEW_MIN = 0.01
    H_SLEW_MAX = 2.5
    L_SLEW_MIN = 0.001
    L_SLEW_MAX = 0.25

    # CCX MODE LIMITS
    CCH_MAX_A = 60
    CCL_MAX_A = 6
    CCH_MAX_POWER_W = 300
    CCL_MAX_POWER_W = 30

    # CR
    CRH_MIN_R = 1.25
    CRH_MAX_R = 5000

    CRL_MIN_R = 0.025
    CRL_MAX_R = 100
    
    CRL_MAX_V = 16
    CRH_MAX_V = 80 
    
    CRL_MAX_A = CCH_MAX_A
    CRH_MAX_A = CCL_MAX_A
    
    # CCD
    CCD_T_MIN_S = 25E-6
    CCD_T_MAX_S = 50

    CV_MAX_V = 80

    MULTI_CHANNEL = False

    MODES = [ELoadTypes.CC,
            ELoadTypes.CR,
            ELoadTypes.CV,
            ]

class Chroma63303A():
    
    # Mode range count
    MODE_RANGE_COUNT = 2
    
    # CR Mode slew rate availability
    CR_SLEW_AVAILABLE = True
    
    # CP Mode slew rate unit
    CP_SLEW_UNIT = 'W / µs'
       
    # SLEW RATE LIMITS
    H_SLEW_MIN = 0.01
    H_SLEW_MAX = 2.5
    L_SLEW_MIN = 0.001
    L_SLEW_MAX = 0.25

    # CCX MODE LIMITS
    CCH_MAX_A = 60
    CCL_MAX_A = 6
    CCH_MAX_POWER_W = 300
    CCL_MAX_POWER_W = 30

    # CR
    CRH_MIN_R = 1.25
    CRH_MAX_R = 5000

    CRL_MIN_R = 0.025
    CRL_MAX_R = 100 
    
    CRL_MAX_V = 16
    CRH_MAX_V = 80 
    
    CRL_MAX_A = CCH_MAX_A
    CRH_MAX_A = CCL_MAX_A
    
    # CCD
    CCD_T_MIN_S = 25E-6
    CCD_T_MAX_S = 50

    CV_MAX_V = 80

    MULTI_CHANNEL = False

    MODES = [ELoadTypes.CC,
            ELoadTypes.CR,
            ELoadTypes.CV,
            ]
    
class Chroma63303():
    
    # Mode range count
    MODE_RANGE_COUNT = 2
    
    # CR Mode slew rate availability
    CR_SLEW_AVAILABLE = True
    
    # CP Mode slew rate unit
    CP_SLEW_UNIT = 'W / µs'
       
    # SLEW RATE LIMITS
    H_SLEW_MIN = 0.01
    H_SLEW_MAX = 2.5
    L_SLEW_MIN = 0.001
    L_SLEW_MAX = 0.25

    # CCX MODE LIMITS
    CCH_MAX_A = 60
    CCL_MAX_A = 6
    CCH_MAX_POWER_W = 300
    CCL_MAX_POWER_W = 30

    # CR
    CRH_MIN_R = 1.25
    CRH_MAX_R = 5000

    CRL_MIN_R = 0.025
    CRL_MAX_R = 100 
    
    CRL_MAX_V = 16
    CRH_MAX_V = 80 
    
    CRL_MAX_A = CCH_MAX_A
    CRH_MAX_A = CCL_MAX_A
    
    # CCD
    CCD_T_MIN_S = 25E-6
    CCD_T_MAX_S = 30

    CV_MAX_V = 80

    MULTI_CHANNEL = False

    MODES = [ELoadTypes.CC,
            ELoadTypes.CR,
            ELoadTypes.CV,
            ]
    
class Chroma63302():
    
    # Mode range count
    MODE_RANGE_COUNT = 2
    
    # CR Mode slew rate availability
    CR_SLEW_AVAILABLE = True
    
    # CP Mode slew rate unit
    CP_SLEW_UNIT = 'W / µs'
       
    # SLEW RATE LIMITS
    H_SLEW_MIN = 3.2E-3
    H_SLEW_MAX = 800E-3
    L_SLEW_MIN = 0.32E-3
    L_SLEW_MAX = 80E-3

    # CCX MODE LIMITS
    CCH_MAX_A = 20
    CCL_MAX_A = 2
    CCH_MAX_POWER_W = 100
    CCL_MAX_POWER_W = 20

    # CR
    CRH_MIN_R = 3.75
    CRH_MAX_R = 15000

    CRL_MIN_R = 0.075
    CRL_MAX_R =300 
    
    CRL_MAX_V = 16
    CRH_MAX_V = 80 
    
    CRL_MAX_A = CCH_MAX_A
    CRH_MAX_A = CCL_MAX_A
    
    # CCD
    CCD_T_MIN_S = 25E-6
    CCD_T_MAX_S = 30

    CV_MAX_V = 80

    MULTI_CHANNEL = True

    MODES = [ELoadTypes.CC,
            ELoadTypes.CR,
            ELoadTypes.CV,
            ]
    
    
# Eload modules for 63600 Mainframe
    
class Chroma63640_80_80():
    
    # Mode range count
    MODE_RANGE_COUNT = 3
    
    # CR Mode slew rate availability
    CR_SLEW_AVAILABLE = False
    
    # CP Mode slew rate unit
    CP_SLEW_UNIT = 'A / µs'
       
    # SLEW RATE LIMITS
    H_SLEW_MIN = 8
    H_SLEW_MAX = 16
    M_SLEW_MIN = 0.8
    M_SLEW_MAX = 1.6
    L_SLEW_MIN = 0.16
    L_SLEW_MAX = 0.08

    # CCX MODE LIMITS
    CCH_MAX_A = 80
    CCM_MAX_A = 8
    CCL_MAX_A = 0.8
    CCH_MAX_POWER_W = 400
    CCM_MAX_POWER_W = 60
    CCL_MAX_POWER_W = 60

    # CR
    CRH_MIN_R = 1.45
    CRH_MAX_R = 2900
    
    CRM_MIN_R = 0.36
    CRM_MAX_R = 720

    CRL_MIN_R = 0.01
    CRL_MAX_R = 20 
    
    CRL_MAX_V = 6
    CRM_MAX_V = 16
    CRH_MAX_V = 80
    
    CRL_MAX_A = CCH_MAX_POWER_W/CRL_MAX_V
    CRM_MAX_A = CCH_MAX_POWER_W/CRL_MAX_V
    CRH_MAX_A = CCH_MAX_POWER_W/CRH_MAX_V
    
    # CP
    CPL_MIN_W = 0
    CPL_MAX_W = 8
    CPM_MIN_W = 0
    CPM_MAX_W = 40
    CPH_MIN_W = 0
    CPH_MAX_W = 400
    
    CPL_SLEW_MIN = 0.08E-3
    CPL_SLEW_MAX = 0.002
    
    CPM_SLEW_MIN = 0.8E-3
    CPM_SLEW_MAX = 0.02
    
    CPH_SLEW_MIN = 0.008
    CPH_SLEW_MAX= 0.2
    
    
    # CCD
    CCD_T_MIN_S = 0.2E-6
    CCD_T_MAX_S = 99

    CV_MAX_V = 80

    MULTI_CHANNEL = False

    MODES = [ELoadTypes.CC,
            ELoadTypes.CR,
            ELoadTypes.CV,
            ELoadTypes.CP]
    
class Chroma63630_600_15():
    
    # Mode range count
    MODE_RANGE_COUNT = 3
    
    # CR Mode slew rate availability
    CR_SLEW_AVAILABLE = False
    
    # CP Mode slew rate unit
    CP_SLEW_UNIT = 'A / µs'
       
    # SLEW RATE LIMITS
    H_SLEW_MIN = 8
    H_SLEW_MAX = 16
    M_SLEW_MIN = 0.8
    M_SLEW_MAX = 1.6
    L_SLEW_MIN = 0.16
    L_SLEW_MAX = 0.08

    # CCX MODE LIMITS
    CCH_MAX_A = 15
    CCM_MAX_A = 1.5
    CCL_MAX_A = 0.15
    CCH_MAX_POWER_W = 300
    CCM_MAX_POWER_W = 300
    CCL_MAX_POWER_W = 90

    # CR
    CRH_MIN_R = 200E3
    CRH_MAX_R = 208
    
    CRM_MIN_R = 4E3
    CRM_MAX_R = 1.92

    CRL_MIN_R = 270
    CRL_MAX_R = 0.133 
    
    CRL_MAX_V = 80
    CRM_MAX_V = 150
    CRH_MAX_V = 600
    
    CRL_MAX_A = CCH_MAX_POWER_W/CRL_MAX_V
    CRM_MAX_A = CCH_MAX_POWER_W/CRM_MAX_V
    CRH_MAX_A = CCH_MAX_POWER_W/CRH_MAX_V
    
    # CP
    CPL_MIN_W = 0
    CPL_MAX_W = 6
    CPM_MIN_W = 0
    CPM_MAX_W = 30
    CPH_MIN_W = 0
    CPH_MAX_W = 300
    
    CPL_SLEW_MIN = 0.375E-3
    CPL_SLEW_MAX= 0.015E-3
    
    CPM_SLEW_MIN = 3.75E-3
    CPM_SLEW_MAX= 0.15E-3
    
    CPH_SLEW_MIN = 37.5E-3
    CPH_SLEW_MAX= 1.5E-3
    
    
    # CCD
    CCD_T_MIN_S = 0.2E-6
    CCD_T_MAX_S = 99

    CV_MAX_V = 600

    MULTI_CHANNEL = False

    MODES = [ELoadTypes.CC,
            ELoadTypes.CR,
            ELoadTypes.CV,
            ELoadTypes.CP]



