from pyosal import pyosal
from sample.svc import svc


# --------------------
## sample App to set up a background process to run the OnelineServer and
# to run the OnelineClient locally
class App:
    # --------------------
    ## constructor
    def __init__(self):
        ## when done indicates all done with the bg process
        self._finished = False

    # --------------------
    ## initialize
    #
    # @return None
    def init(self):
        svc.log.info('App.init')

    # --------------------
    ## run the client for various scenarios
    #
    # @return None
    def run(self):
        svc.log.info('App.run')
        svc.log.info(f'os_name: {pyosal.os_name}')
