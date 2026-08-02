import os

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

        home = os.path.expanduser('~')
        path = f'{home}\\dir1\\dir2'
        svc.log.info(f'xlat_dir_to_relative: {pyosal.xlat_dir_to_relative(path)}')
        path = f'{home}/dir1/dir2'
        svc.log.info(f'xlat_dir_to_relative: {pyosal.xlat_dir_to_relative(path)}')

        pyosal.stdout_flush()
        pyosal.stdout_flush(force=True)

        pyosal.stderr_flush()
        pyosal.stderr_flush(force=True)

        svc.log.info('run_cmd_timeout: running')
        timeout = 3  # seconds
        msys_tag = None
        if pyosal.os_name == 'ubuntu':
            cmd = ['gedit', 'out/abc.txt']
        elif pyosal.os_name == 'msys2':
            cmd = ['notepad']
            msys_tag = 'notepad.exe'
        elif pyosal.os_name == 'macos':
            cmd = ['open', '-a', 'TextEdit']
        rc = pyosal.run_cmd_timeout(timeout, cmd, msys_tag=msys_tag)
        svc.log.info(f'run_cmd_timeout rc={rc}')

        svc.log.info('run_cmd: running')
        cmd = ['pwd']
        rc, lines = pyosal.run_cmd(cmd)
        svc.log.info(f'run_cmd rc={rc}')
        for lineno, line in enumerate(lines):
            svc.log.info(f'  line {lineno}: {line}')

        # uncomment to test abort() empty message
        # pyosal.abort()
        pyosal.abort('test of abort')
