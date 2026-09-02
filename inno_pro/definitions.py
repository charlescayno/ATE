from inno_pro.inno4_pro.controller import Inno4ProI2CController
from inno_pro.inno5_pro.controller import Inno5ProI2CController

InnoProI2CControllers = [
    Inno5ProI2CController,
    Inno4ProI2CController,
]

class InnoPro_MessageType():
    I2C = 'I2C'
    UVDM_PDC1 = 'UVDM1'
    UVDM_PDC2 = 'UVDM2'

class InnoProFamily():
    Inno5Pro = 'Inno5-Pro'
    Inno4Pro = 'Inno4-Pro'
    
InnoProFamilyList = [
    InnoProFamily.Inno5Pro,
    InnoProFamily.Inno4Pro,
]

InnoProMessageUVDMList = [
    InnoPro_MessageType.UVDM_PDC1,
    InnoPro_MessageType.UVDM_PDC2,
]