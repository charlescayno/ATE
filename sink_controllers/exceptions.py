# Exceptions 
from pd.pd_types import EPR_AVS_APDO


class PDSinkException(Exception):
    def __init__(self, msg=''):
        self.msg = msg

class FixedPDORequestError(PDSinkException):
    def __init__(self, msg=''):
        self.msg = msg

class NoMatchingFixedPDOFoundError(FixedPDORequestError):
    def __init__(self, msg=''):
        self.msg = msg

class NotEnoughFPDOMaxCurrentError(FixedPDORequestError):
    def __init__(self, msg=''):
        self.msg = msg


################################################################################
#                                   PPS Exceptions
################################################################################

class PPSRequestError(PDSinkException):
    def __init__(self, msg=''):
        self.msg = msg

class NoPPSSourceCapFoundError(PPSRequestError):
    def __init__(self, msg=''):
        self.msg = msg

class PPSSourceCapNotSufficientError(PPSRequestError):
    def __init__(self, msg=''):
        self.msg = msg

################################################################################
#                                   AVS Exceptions
################################################################################

class AVSRequestError(PDSinkException):
    def __init__(self, msg=''):
        self.msg = msg

class NoAVSSourceCapFoundError(AVSRequestError):
    def __init__(self, msg=''):
        self.msg = msg

class AVSSourceCapNotSufficientError(AVSRequestError):
    def __init__(self, msg=''):
        self.msg = msg