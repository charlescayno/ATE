class ACSourceBaseClass():
    def __init__(self):
        self.volt_ac = 'VOLTAGE'
        self.volt_dc = 'VOLTAGE:OFFSET'
        self.freq = 'FREQUENCY'
        self.coupling = 'OUTPUT:COUPLING'
        self.output = 'OUTPUT'
        self.state = 'STATE'
        self.shape = 'FUNCTION:SHAPE'
        self.volt_ac_slew_rate = 'VOLT:SLEW'
        self.volt_dc_slew_rate = 'VOLT:OFFS:SLEW'
        self.freq_slew_rate = 'FREQ:SLEW'
        
class ACSourceAgilent(ACSourceBaseClass):
    def __init__(self):
        super().__init__()
        self.volt_ac = 'VOLT'
        self.volt_dc = 'VOLT:OFFS'
        self.freq = 'FREQ'
        self.coupling = 'OUTP:COUP'
        self.output = 'OUTP'
        self.state = 'STAT'
        self.shape = 'FUNC:SHAP'
        self.volt_ac_slew_rate = 'VOLT:SLEW'
        self.volt_dc_slew_rate = 'VOLT:OFFS:SLEW'
        self.freq_slew_rate = 'FREQ:SLEW'
        
class ACSourceIT7800(ACSourceBaseClass):
    def __init__(self):
        super().__init__()
        self.volt_ac = 'VOLT:AC'
        self.volt_dc = 'VOLT:DC'
        self.freq = 'FREQ'
        self.coupling = 'FUNC'
        self.output = 'OUTP'
        self.state = 'STAT'
        self.shape = ''
        self.volt_ac_slew_rate = 'VOLT:SLOP' 
        self.volt_dc_slew_rate = 'VOLT:SLOP:DC'
        self.freq_slew_rate = 'FREQ:SLOP'

class ACSourceChroma(ACSourceBaseClass):
    def __init__(self):
        super().__init__()
        self.volt_ac = 'VOLT'
        self.volt_dc = 'VOLT:DC'
        self.freq = 'FREQ'
        self.coupling = 'OUTP:COUP'
        self.output = 'OUTP'
        self.state = 'STAT'
        self.shape = 'FUNC:SHAP'
        self.volt_ac_slew_rate = 'OUTP:SLEW:VOLTAGE:AC' 
        self.volt_dc_slew_rate = 'OUTP:SLEW:VOLTAGE:DC'
        self.freq_slew_rate = 'OUTP:SLEW:FREQ'
        
class ACSourceKikusui(ACSourceBaseClass):
    def __init__(self):
        super().__init__()
    