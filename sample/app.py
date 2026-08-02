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

        path = '/c/dir1/dir2'
        svc.log.info(f'xlat_to_win  : {pyosal.xlat_to_win(path)}')
        svc.log.info(f'xlat_to_win  : {pyosal.xlat_to_win(path, force=True)}')

        path = 'c:\\dir1\\dir2'
        svc.log.info(f'xlat_to_posix: {pyosal.xlat_to_posix(path)}')
        svc.log.info(f'xlat_to_posix: {pyosal.xlat_to_posix(path, force=True)}')

        path = '/home/arrizza\\dir1\\dir2'
        svc.log.info(f'xlat_dir_to_relative: {pyosal.xlat_dir_to_relative(path)}')
        path = '/home/arrizza/dir1/dir2'
        svc.log.info(f'xlat_dir_to_relative: {pyosal.xlat_dir_to_relative(path)}')

        pyosal.stdout_flush()
        pyosal.stdout_flush(force=True)

        pyosal.stderr_flush()
        pyosal.stderr_flush(force=True)

        # TODO run_cmd_timeout
        # TODO run_cmd

        # uncomment to test abort() empty message
        # pyosal.abort()
        pyosal.abort('test of abort')
