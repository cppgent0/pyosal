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
        if pyosal.os_name in ['ubuntu', 'macos']:
            svc.log.info(f'posix os: {pyosal.os_name}')
        elif pyosal.os_name in ['msys2']:
            svc.log.info(f'win os    : {pyosal.os_name}')
        else:
            svc.log.info(f'other     : {pyosal.os_name}')

        svc.log.info(f'os_valid  : {pyosal.os_valid}')
        svc.log.info(f'os_version: {pyosal.os_version}')
        svc.log.info(f'python_version: {pyosal.python_version}')

        svc.log.info(f'userid    : {pyosal.userid}')
        svc.log.info(f'hostname  : {pyosal.hostname}')

        svc.log.info(f'curr_repo_dir : {pyosal.curr_repo_dir}')
        svc.log.info(f'curr_repo_name: {pyosal.curr_repo_name}')

        svc.log.info(f'root_dir : {pyosal.root_dir}')
        svc.log.info(f'root_dir_msys2: {pyosal.root_dir_msys2}')
