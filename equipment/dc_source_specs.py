class DCSourceBaseClass():
    def __init__(self):
        self.output_on = 'OUTPUT ON'
        self.output_off = 'OUTPUT OFF'
        self.measure = 'MEASURE'
        self.volt = 'VOLTAGE'
        self.curr = 'CURRENT'
        self.output = 'OUTPUT'
        self.state = 'STATE'
        self.sequence = 'OUTPUT:SEQUENCE'
        
class DCSourceMagnaPower(DCSourceBaseClass):
    def __init__(self):
        super().__init__()
        self.output_on = 'OUTP:START'
        self.output_off = 'OUTP:STOP'
        self.measure = 'MEAS'
        self.volt = 'VOLT'
        self.curr = 'CURR'
        self.output = 'OUTP'
        self.state = 'STAT'
        self.sequence = 'OUTP:ARM'
        
class DCSourceChroma(DCSourceBaseClass):
    def __init__(self):
        super().__init__()
        self.output_on = 'OUTP ON'
        self.output_off = 'OUTP OFF'
        self.measure = 'MEAS'
        self.volt = 'VOLT'
        self.curr = 'CURR'
        self.output = 'OUTP'
        self.state = 'STAT'
        self.sequence = 'OUTP:SEQ'