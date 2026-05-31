# TODO: normally this is imported using the published module
# import module_name
from falcon_logger import FalconLogger

from src.pyosal import pyosal
from tools.xplat_utils.os_specific import OsSpecific
from ver.helpers import svc


# --------------------
## helper functions for verification tests
class Helper:
    # --------------------
    ## constructor
    def __init__(self):
        OsSpecific.init()

    # --------------------
    ## initialize
    #
    # @return None
    def init(self):
        svc.log = FalconLogger(mode='mock')
        svc.mut = pyosal

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        pass

    # --------------------
    ## initialize
    # any actions at the start of each test
    #
    # @param ptobj  reference to the pytest object
    # @return None
    def init_each_test(self, ptobj):
        print('')
        svc.pytself = ptobj

    # --------------------
    ## terminate.
    # any actions at the end of each test
    #
    # @return None
    def term_each_test(self):
        pass
