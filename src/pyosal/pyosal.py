import getpass
import os
import platform
import re
import subprocess
import sys
import threading
import time

import psutil


# -------------------
## Meta class for pyosal; ensures it is a singleton
class _PyOsalMeta(type):
    ## holds instances of this class (should be 1)
    _instances = {}
    ## ensure creation is thread safe
    _lock = threading.Lock()

    # -------------------
    ## handle getting the instance of the class.
    # @param args    the arguments
    # @param kwargs  the kw arguments
    def __call__(cls, *args, **kwargs):
        # Double-checked locking for performance and thread safety
        if cls not in cls._instances:  # pragma: no cover
            with cls._lock:
                if cls not in cls._instances:  # pragma: no cover
                    # super().__call__ handles object creation AND initialization
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


# -------------------
## holds OS specific info; there are currently four recognized OS:
#    OS      os_name
#  -------   ----------
#  Ubuntu  : ubuntu
#  Mac     : macos
#  Windows : win (msys2)
#  Windows : psi (powershell) note: future support
#  RPI     : rpi              note: future support
class PyOsal(metaclass=_PyOsalMeta):
    # -------------------
    ## initialize
    def __init__(self):
        ## holds the OS name
        self._os_name: str = None
        ## holds the OS version info
        self._os_version: str
        ## holds the python version
        self._python_version: str = None
        ## root directory of projects directory
        # note returns windows format C:/xx/xx
        self._root_dir: str = None
        ## root directory of projects directory in msys2 format /c/xx/xx
        self._root_dir_msys2: str = None
        ## current userid
        self._userid: str = None
        ## hostname of the pc
        self._hostname: str = None
        ## list of valid OS
        self._os_valid = ['ubuntu', 'macos', 'msys2', 'psi', 'rpi']
        ## for debug
        self._debug = set()

        # === UT related

        ## used by UTs only
        self._ut_mode = False
        ## used by UTs only
        self.ut_curr_dir = None

        # === initialize
        self._get_os_name()
        self._set_all_data()

    # -------------------
    ## set debug to print extra info.
    # * set()         : turn off debugging
    # * {'timed'}     : print()'s for run_cmd_timed
    # * {'run'}       : print()'s for run_cmd
    # * {'run', 'timed'} : for both
    # @param val   the debug level to use
    # @return None
    def set_debug(self, val: set):
        self._debug = set(val)

    # -------------------
    ## get OS name/tag
    # @return os_name
    @property
    def os_name(self):
        return self._os_name

    # -------------------
    ## get OS version info
    # @return os_version
    @property
    def os_version(self):
        return self._os_version

    # -------------------
    ## get python version
    # @return python_version
    @property
    def python_version(self):
        return self._python_version

    # -------------------
    ## get path for root directory
    # @return root_dir
    @property
    def root_dir(self):
        return self._root_dir

    # -------------------
    ## get root directory for msys2 shells
    # @return root_dir_msys2
    @property
    def root_dir_msys2(self):
        return self._root_dir_msys2

    # -------------------
    ## get current userid
    # @return userid
    @property
    def userid(self):
        return self._userid

    # -------------------
    ## get current PC's hostname
    # @return hostname
    @property
    def hostname(self):
        return self._hostname

    # -------------------
    ## get list of recognized valid OS names
    # @return os_valid
    @property
    def os_valid(self):
        return self._os_valid

    # -------------------
    ## selects the current platform and sets impl to it
    #
    # @return None
    def _set_all_data(self):
        if self._os_name == 'rpi':
            # TODO confirm this is correct
            self._os_version = f'RPI {platform.system()} {platform.release()}'
            self._root_dir = '~'
            self._root_dir_msys2 = self._root_dir
        elif self._os_name == 'msys2':
            self._os_version = f'win32 {platform.system()} {platform.release()}'
            self._root_dir = os.path.expanduser('~')
            self._root_dir = self._root_dir.replace('\\', '/')
            self._root_dir_msys2 = '/' + self._root_dir[0].lower() + self._root_dir[2:]
        elif self._os_name == 'macos':
            if self._ut_mode:  # pragma: no cover
                self._os_version = 'ut macOS 14.5'
            else:
                self._os_version = f'macOS {platform.mac_ver()[0]}'  # pragma: no cover
            self._root_dir = '~'
            self._root_dir_msys2 = self._root_dir
        elif self._os_name == 'ubuntu':
            if self._ut_mode:
                self._os_version = 'ut Ubuntu 24.04 noble'
            else:
                self._os_version = self._ubuntu_os_version()
            self._root_dir = '~'
            self._root_dir_msys2 = self._root_dir
        else:
            self.abort(f'PyOsal.set_all_data: unrecognized OS: "{sys.platform}"')

        ## holds python version e.g. "Python 3.10"
        self._python_version = f'Python {sys.version_info.major}.{sys.version_info.minor}'

        self._hostname = platform.uname().node
        self._hostname = self._hostname.lower().replace('.local', '')

        self._userid = getpass.getuser()

    # -------------------
    ## get the current OS tag
    # @return None
    def _get_os_name(self):  # pragma: no cover
        if os.path.isfile('/sys/firmware/devicetree/base/model'):
            self._os_name = 'rpi'
        elif sys.platform == 'win32':
            # TODO check if it's a cygwin?
            if 'MSYSTEM' in os.environ:
                self._os_name = 'msys2'
            elif 'PSModulePath' in os.environ or 'POWERSHELL_DISTRIBUTION_CHANNEL' in os.environ:
                self._os_name = 'psi'
            else:
                self._os_name = 'win-unknown'
        elif sys.platform == 'darwin':
            self._os_name = 'macos'
        elif sys.platform == 'linux':
            self._os_name = 'ubuntu'
        else:
            self._os_name = 'unknown'

    # -------------------
    ## holds OS information for Ubuntu
    #
    # @return string indicating OS info
    def _ubuntu_os_version(self):
        proc = subprocess.Popen(  # pylint: disable=consider-using-with
            ['lsb_release', '-a'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        (out, _) = proc.communicate()
        out = out.decode('utf-8')

        version = 'notset'
        codename = 'notset'
        for line in out.split('\n'):
            # sys.stdout.write(f'line: "{line}"')
            args = line.split('\t')
            if args[0] == 'Release:':
                version = args[1]
            elif args[0] == 'Codename:':
                codename = args[1]
        return f'Ubuntu {version} {codename}'

    # === cmd invocation from here on

    ## exception keywords
    _excp_keywords = [
        'Traceback (most recent call last):',
        'Error:',
        'Permission denied',
        'command not found',
    ]

    # -------------------
    ## run a command in a subprocess with a timeout
    #
    # @param timeout       (integer) max time to run cmd before terminating/killing the process
    # @param cmd           the command to run
    # @param working_dir   the working directory to run the command in; default is '.'
    # @param use_raw_log   no prefix on line
    # @param log_file      the log_file to write the lines to
    # @param print_cb      callback function used to print output; default is None
    # @param env           the environment variables to use
    # @param quiet         if True, do not write to stdout
    # @param cmd_tag       used for MSYS2/macos processes; matches command line content for PID to kill
    # @return rc - return code, lines - the output as a list of lines
    def run_cmd_timeout(
        self,
        timeout,
        cmd,
        working_dir='.',
        use_raw_log=False,
        log_file=None,
        print_cb=None,
        env=None,
        quiet=False,
        cmd_tag='NOTEPAD',
    ):  # pylint: disable=too-many-locals
        if not isinstance(timeout, int):
            self.abort('PyOsal.run_cmd_timeout: timeout must be an integer')

        if not isinstance(cmd, list):
            self.abort('PyOsal.run_cmd_timeout: cmd must be a list')

        # Run your existing function in a background thread
        shared_container = {}
        t = threading.Thread(target=self.run_cmd, args=(cmd, working_dir, use_raw_log, log_file, print_cb, env, quiet, shared_container))
        t.daemon = True
        t.start()

        # Wait briefly for the subprocess to actually initialize and populate the container
        while not shared_container:
            time.sleep(0.01)
        start_time = time.time()

        if 'timed' in self._debug:
            cmd_str = ' '.join(shared_container['cmd'][2:])
            print(f'pyosal.run_cmd_timeout: pids={shared_container["pids"]} cmd="{cmd_str}"')

        rc = 0
        timed_out = False
        state = 'start'
        while True:
            # wait here so that the bash terminal in MSYS2/macos can end
            time.sleep(0.3)
            state = self._check_timer(t, start_time, timeout, shared_container, cmd_tag)
            if state in ['cmd-dead', 'timer_expired']:
                break

            # at this point: command is still running

        if state == 'timer_expired':
            self._check_processes(timeout, shared_container)
            timed_out = True
            rc = 0  # override rc since timeout is expected

        t.join(timeout=0.25)
        rc_str = f'rc={rc}'
        if shared_container['proc'] is None:
            sys.stdout.write(f'[timeout] {rc_str: <6} process ended due to exception\n')
        elif timed_out:
            sys.stdout.write(f'[timeout] {rc_str: <6} process ended due to timeout\n')
        else:
            rc = shared_container['proc'].poll()
            sys.stdout.write(f'[timeout] {rc_str: <6} process finished before timeout\n')
        sys.stdout.flush()
        return rc

    # -------------------
    ## terminate/kill processes in the tree
    #
    # @param timeout       (integer) max time to run cmd before terminating/killing the process
    # @param shared_container used by run_cmd_container to receive the proc value
    # @return None
    def _check_processes(self, timeout, shared_container):
        sys.stdout.write(f'\n[timeout] exceeded {timeout}s, terminating process...\n')
        sys.stdout.flush()

        try:
            rc = self._kill_process_tree(shared_container, 'terminate')
            rc_str = f'rc={rc}'
            sys.stdout.write(f'[timeout] {rc_str: <6} process terminated gracefully\n')
        except subprocess.TimeoutExpired:
            sys.stdout.write('[timeout] process did not terminate, killing process...\n')
            sys.stdout.flush()
            rc = self._kill_process_tree(shared_container, 'kill')
            rc_str = f'rc={rc}'
            sys.stdout.write(f'[timeout] {rc_str: <6} process forcefully killed\n')

        sys.stdout.flush()

    # -------------------
    ## check if timer has expired and if so terminate/kill the process
    #
    # @param thread_ptr       the bg thread running the sleep/wait
    # @param start_time       the time the bg thread started
    # @param timeout          the max time the thread should run
    # @param shared_container used by run_cmd_container to receive the proc value
    # @param msys_tag         used only for MSYS2/macos processes; matches command line content for PID to kill
    # @return 'timer_expired' when the expected timeout has been reached,
    #          'cmd-dead' when the process has died,
    #          'cmd-running' when the process is still running and timeout has not been
    def _check_timer(self, thread_ptr, start_time, timeout, shared_container, msys_tag):
        elapsed = time.time() - start_time
        if elapsed > timeout:
            return 'timer_expired'

        if self._os_name in ['msys2', 'macos']:
            if 'timed' in self._debug:
                print(f'pyosal.check_timer_msys2:  {round(elapsed, 1)} {round(time.time(), 1)} ==================================')
            return self._check_timer_alt(shared_container, msys_tag)

        # handle macos and ubuntu
        if not thread_ptr.is_alive():
            return 'cmd-dead'
        return 'cmd-running'

    # -------------------
    ## for MSYS2/macos: check the process is still running.
    # the cmd_tag is used to get the correct PID for killing.
    # at this point: in msys2/macos session and timer has not expired
    # the initial msys2/macos thread will immediately die
    # but the current processes are strill running
    #
    # @param shared_container used by run_cmd_container to receive the proc value
    # @param cmd_tag          used only for msys2/macos processes; matches command line content for PID to kill
    # @return 'timer_expired' when the expected timeout has been reached,
    #          'cmd-dead' when the process has died,
    #          'cmd-running' when the process is still running and timeout has not been
    def _check_timer_alt(self, shared_container, cmd_tag):
        process_list = []
        # psutil.process_iter fetches all running processes efficiently in a single sweep
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                info = proc.info
                cmdline_str = ' '.join(info['cmdline']) if info['cmdline'] else ''
                process_list.append({'PID': info['pid'], 'Name': info['name'], 'CommandLine': cmdline_str})
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # skip processes that die mid-flight or reject access permissions
                pass

        state = 'cmd-not-found'
        state_pid = 0
        # search for command match in PID sorted order.
        # This will find the most recent process last
        for info in sorted(process_list, key=lambda x: x['PID']):
            # skip lines with missing data or irrelevant processes
            if info['CommandLine'] is None:
                continue
            if info['Name'] in [
                'backgroundTaskHost.exe',
                'conhost.exe',
                'Code.exe',
                'dllhost.exe',
                'dasHost.exe',
                'FileCoAuth.exe',
                'RuntimeBroker.exe',
                'svchost.exe',
                'SystemSettings.exe',
                'SystemOptimizer.exe',
                'OneDrive.exe',
                'OpenConsole.exe',
            ]:
                continue

            if not isinstance(info['PID'], int):
                info['PID'] = int(info['PID'])

            # capitalization is not relevant
            cmd_line = info['CommandLine'].lower()
            pfx = '  '
            if cmd_tag.lower() in cmd_line:
                pfx = '**'
                state = 'cmd-running'
                state_pid = info['PID']
                if state_pid not in shared_container['pids']:
                    shared_container['pids'].append(state_pid)

            if pfx == '**' and 'timed' in self._debug:
                print(f'w:{pfx}{info["PID"]: <5} {info["Name"]: <20} {cmd_line}')

        if shared_container['state'] == 'cmd-not-found' and state == 'cmd-running':
            shared_container['state'] = 'cmd-running'
        elif shared_container['state'] == 'cmd-running' and state == 'cmd-not-found':
            shared_container['state'] = 'cmd-dead'
        elif 'timed' in self._debug:
            print(f'pyosal.check_timer_alt: state:{state} shared:{shared_container["state"]}')

        sys.stdout.flush()
        return state

    # -------------------
    ## kill all processes for the gived parent pid
    # @param shared_container used by run_cmd_container to receive the proc value
    # @param action     if "kill", kills the processes, otherwise terminates the prcesses
    # @return None
    def _kill_process_tree(self, shared_container, action):
        if self._os_name in ['msys2', 'macos']:
            rc = self._kill_alt_process_tree(shared_container)
        else:  # macos and ubuntu
            rc = self._kill_posix_process_tree(shared_container, action)
        return rc

    # -------------------
    ## kill the MSYS2 process.
    # Note there is no equivalent of "terminate" in MSYS2/windows
    #
    # @param shared_container used by run_cmd_container to receive the proc value
    # @return the return code
    def _kill_alt_process_tree(self, shared_container):
        rc = 0
        print(f'[timeout] {self.os_name} detected...')
        if 'timed' in self._debug:
            cmd_str = ' '.join(shared_container['cmd'])
            print(f'pyosal._kill_alt_process_tree: pids={shared_container["pids"]} cmd="{cmd_str}"')

        for pid in shared_container['pids']:
            if not psutil.pid_exists(pid):
                if 'timed' in self._debug:
                    print(f'pyosal._kill_alt_process_tree: pid={pid} does not exist')
                continue
            proc = psutil.Process(pid)
            # terminate does not work in windows
            proc.kill()
            if 'timed' in self._debug:
                print(f'pyosal._kill_alt_process_tree: pid={pid} killed')
            time.sleep(0.010)
        return rc

    # -------------------
    ## kill the process tree
    # @param shared_container used by run_cmd_container to receive the proc value
    # @param action           "terminate" to ask process to terminate itself.
    #                         "kill" to terminate the process externally
    # @return the return code
    def _kill_posix_process_tree(self, shared_container, action):
        proc = shared_container['proc']
        ppid_num = shared_container['pids'][0]
        rc = 0
        try:
            parent_pid = psutil.Process(ppid_num)
            children = list(reversed(parent_pid.children(recursive=True)))

            # kill children first
            for pid in children:
                self._kill_process(pid, action)

            # kill parent
            self._kill_process(parent_pid, action)
        except psutil.NoSuchProcess:
            # parent/child processes may already be dead
            pass
        except psutil.AccessDenied:
            cmd = ['sudo', 'kill', '-9' if action == 'kill' else '-15', str(parent_pid.pid)]
            subprocess.run(cmd, check=False)

        # wait for the terminate to take effect
        if action == 'terminate':
            try:
                rc = proc.wait(timeout=1.0)
            except subprocess.TimeoutExpired as excp:
                # Manually raise it to force execution into the hard-kill block
                raise subprocess.TimeoutExpired(proc.args, 1.0) from excp
        else:
            rc = proc.wait()
        return rc

    # -------------------
    ## kill a POSIX process
    # @param pid       the process id to kill
    # @param action    "terminate" to ask process to terminate itself.
    #                         "kill" to terminate the process externally
    # @return None
    def _kill_process(self, pid, action):
        try:
            if action == 'kill':
                pid.kill()
            else:
                pid.terminate()
        except psutil.NoSuchProcess:
            # child processes may already be dead
            pass
        except psutil.AccessDenied:
            # If no permission to kill the root child, escalate the kill command using sudo
            cmd = ['sudo', 'kill', '-9' if action == 'kill' else '-15', str(pid.pid)]
            subprocess.run(cmd, check=False)

    # -------------------
    ## run a command in a subprocess
    #
    # @param cmd           the command to run
    # @param working_dir   the working directory to run the command in; default is '.'
    # @param use_raw_log   no prefix on line
    # @param log_file      the log_file to write the lines to
    # @param print_cb      callback function used to print output; default is None
    # @param env           the environment variables to use
    # @param quiet         if True, do not write to stdout
    # @param shared_container used by run_cmd_container to receive the proc value
    # @return rc - return code, lines - the output as a list of lines
    def run_cmd(  # pylint: disable=too-many-branches,too-many-statements
        self,
        cmd,
        working_dir='.',
        use_raw_log=False,
        log_file=None,
        print_cb=None,
        env=None,
        quiet=False,
        shared_container=None,
    ):  # pylint: disable=too-many-locals
        if not isinstance(cmd, list):
            self.abort('PyOsal.run_cmd: cmd must be a list')

        ## os_name: see above
        if self._os_name == 'msys2':
            # need to invoke msys2 bash
            pfx = ['c:/msys64/usr/bin/bash', '-c']
            # the current cmd is a single string at the end
            pfx.append(' '.join(cmd))
            cmd = pfx

            # msys2 can cause truncations and wrapping of text if the lines are long
            if env is None:
                env = os.environ.copy()

        fp = None
        if log_file is not None:
            fp = open(log_file, 'w', encoding='utf-8', newline='\n')  # pylint: disable=consider-using-with

        # TODO set to 127 and then set specifically to rc == 0 below
        rc = 0
        lineno = 0
        lines = []

        # ensure all output is printed, so any stdin done by the cmd is visible in the right order
        self.stdout_flush()
        try:
            proc = subprocess.Popen(  # pylint: disable=consider-using-with
                cmd,
                cwd=working_dir,
                bufsize=0,
                universal_newlines=True,
                errors='replace',
                text=True,
                stdin=None,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env,
                shell=False,
            )
        except Exception as excp:  # pylint: disable=broad-exception-caught
            rc += 1
            err_type = excp.__class__.__name__
            line = f'EXCP pyosal.run_cmd: rc:{rc} {err_type}: {excp}'
            self._save_line(line, lineno, lines, fp, print_cb, use_raw_log, quiet)
            # indicate to callers that there is no proc
            if shared_container is not None:
                shared_container['proc'] = None
                shared_container['pids'] = []
                shared_container['cmd'] = cmd
                shared_container['state'] = 'cmd-not-found'
            return rc, lines

        if shared_container is not None:
            shared_container['proc'] = proc
            shared_container['pids'] = [proc.pid]
            shared_container['cmd'] = cmd
            shared_container['state'] = 'cmd-not-found'

        # buffer contains the current set of bytes read from proc.stdout so far
        buffer = ''
        while True:
            char = proc.stdout.read(1)
            if not char:
                # it's ''
                break

            # append the current chunk
            # Some apps use linefeeds to do "progress" lines (e.g. 10% 11% etc), so replace any linefeeds with nothing
            if char == '\r':
                char = ' '

            buffer += char

            # if there is a newline in the buffer, then we have at least a full line of characters
            if '\n' not in buffer:
                continue

            # split the buffer at the newline(s)
            buff_lines = buffer.split('\n')
            # save the remaining bytes in buffer
            buffer = buff_lines.pop()

            # at this point buff_lines contains one or more lines (as bytes)
            for line in buff_lines:
                if 'run' in self._debug:
                    if not line.isprintable():
                        sys.stdout.write('has hex: ' + ascii(line) + '\n')

                # check for exceptions and other script failures
                if any(keyword in line for keyword in self._excp_keywords):
                    excp_msg = '@@>>@@ Exception detected'
                    if excp_msg in line:
                        rc += 1
                        continue
                    sys.stdout.write(f'  -- {excp_msg}: "{line}"\n')
                    rc += 1

                if '!DEPRECATE!' in line:
                    dep_msg = '@@>>@@ Deprecation detected'
                    if dep_msg in line:
                        rc += 1
                        continue
                    rc += 1
                    sys.stdout.write(f'  -- {dep_msg} {rc}: "{line}"\n')

                if self._skip_line(line):
                    line2 = line.encode('utf-8', errors='ignore')
                    sys.stdout.write(f'@@>>@@ line skipped: {line2}' + '\n')
                    continue

                # it has text, so add it to the buffer and do the callback if defined
                lineno += 1
                self._save_line(line, lineno, lines, fp, print_cb, use_raw_log, quiet)

        # at this point: chunk was empty
        if len(buffer) > 0:
            lines = buffer.split('\n')
            for line in lines:
                lineno += 1
                self._save_line(line, lineno, lines, fp, print_cb, use_raw_log, quiet)

        if fp:
            fp.flush()
            fp.close()

        rc += proc.wait()

        if proc.stdout:
            self.stdout_flush()
            proc.stdout.close()
        if proc.stderr:
            self.stderr_flush()
            proc.stderr.close()

        return rc, lines

    # -------------------
    ## skip lines with ansi escape sequeces, etc.
    # @param line   the line to check
    # @return True if line should be skipped, False otherwise
    def _skip_line(self, line: str) -> bool:
        if line == '\x1b[?25l':  # hide mouse cursor
            return True
        if line == '\x1b[?25h':  # hide mouse cursor
            return True
        if re.search(r'^\x1b.*\d+%', line):  # skip percent lines
            return True

        if re.search(r'[\u2580-\u259F]', line):
            return True

        # Catch carriage returns (common in curl/wget across Linux/macOS/MSYS2)
        if '\r' in line:
            return True

        # catch ANSI Escape Sequences (used for colors/moving cursors in bash/ps1)
        # This strips \x1b[..., \033[..., etc.
        # ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        # cleaned_line = ansi_escape.sub('', line)

        # TODO fix; causes problems with coverage reports that has % in them
        # e.g.  functions: 100.0% (2 out of 2)
        # Match progress percentages (e.g., 10%, 10.5%)
        # if re.search(r'\d+(?:\.\d+)?%', cleaned_line):
        #     return True

        # # Match interactive spinners (\ | / -)
        # if re.search(r'(?:[\s\[\(\]{}]|^)([\\/|-]+)(?:[\s\]\)\}{}]|$)', cleaned_line):
        #     return True

        return False

    # -------------------
    ## save the current line (if it's not empty)
    # @param line          the line to save
    # @param lineno        the line#
    # @param lines         the current list of lines
    # @param fp            file pointer to write line to; default is None
    # @param print_cb      callback function used to print output; default is None
    # @param use_raw_log   no prefix on line
    # @param quiet         if True, don't print to stdout, but still add to returned line
    # @return None
    def _save_line(self, line, lineno, lines, fp, print_cb, use_raw_log, quiet):
        if not line:
            # skip empty lines
            return

        # always save the line to the returned list
        lines.append(line)

        if use_raw_log:
            line_to_save = line
        else:
            line_to_save = f'  -- {line}'
        line_to_save = line_to_save.replace('←', '\x1b')

        # quiet is used for stdout verbosity
        if not quiet:
            sys.stdout.write(line_to_save + '\n')
            self.stdout_flush()

        # fp is used for writing to the file or not
        if fp:
            fp.write(line_to_save)
            fp.write('\n')

        # print_cb is used for writing to the callback or not
        if print_cb:
            print_cb(lineno, line)

    # --------------------
    ## flush for stdout
    # @param force   (optional) if True, do the buffer flush even if not msys2
    def stdout_flush(self, force=False):
        sys.stdout.flush()
        if force or self._os_name == 'msys2':
            if hasattr(sys.stdout, 'buffer'):
                sys.stdout.buffer.flush()

    # --------------------
    ## flush for stderr
    # @param force   (optional) if True, do the buffer flush even if not msys2
    def stderr_flush(self, force=False):
        sys.stderr.flush()
        if force or self._os_name == 'msys2':
            if hasattr(sys.stderr, 'buffer'):
                sys.stderr.buffer.flush()

    # --------------------
    ## convert a path to windows i.e. backslashes
    # @param path    the path to fix
    # @param force   force the conversion no matter what the OS is
    # @return the unfixed path
    def xlat_to_win(self, path, force=False):
        if not path:
            # defensive. Should not occur
            return None

        path = os.path.expanduser(path)
        if force or self._os_name == 'msys2':
            # assumes there is only one character and it is for a drive letter
            # can only be done at the start of the path
            m = re.search(r'^/(.)/(.*)', path)
            if m:
                drive = m.group(1).upper()
                path = f'{drive}:/{m.group(2)}'
        path = path.replace('/', '\\')
        path = path.replace('//', '\\')
        return path

    # --------------------
    ## convert a windows path to posix i.e. forward slashes
    # @param path    the path to fix
    # @param force   force the conversion no matter what the OS is
    # @return the unfixed path
    def xlat_to_posix(self, path, force=False):
        if not path:
            # defensive. Should not occur
            return None

        path = os.path.expanduser(path)
        if force or self._os_name == 'msys2':
            m = re.search(r'^(.):(.*)', path)
            if m:
                drive = m.group(1).lower()
                path = f'/{drive}{m.group(2)}'
        path = path.replace('\\', '/')
        path = path.replace('//', '/')
        return path

    # -------------------
    ## convert a path to relative to home
    # @param path    the path to fix
    # @return the relative path
    def xlat_dir_to_relative(self, path):
        if not path:
            # defensive. Should not occur
            return None

        path = self.xlat_to_posix(path)
        path = path.replace(self.xlat_to_posix(os.path.expanduser('~')), '~')
        path = path.replace('\\', '/')
        return path

    # -------------------
    ## current repo directory converted to posix
    # @return the repo dir path
    @property
    def curr_repo_dir(self):
        if self.ut_curr_dir is None:
            repo_dir = os.getcwd()
            repo_dir = repo_dir.replace('\\', '/')
            repo_dir = repo_dir.replace('//', '/')
        else:
            repo_dir = self.ut_curr_dir
        return repo_dir

    # -------------------
    ## current repo name
    # @return the repo name
    @property
    def curr_repo_name(self):
        return os.path.basename(os.path.normpath(os.getcwd()))

    # --------------------
    ## abort the current script.
    # Note: do not use logging here since it may fail to write correctly
    #
    # @param msg  (optional) message to display
    # @return does not return
    def abort(self, msg='abort occurred, exiting'):
        # flush all other output first
        self.stdout_flush()
        self.stderr_flush()

        sys.stdout.write('\n')
        sys.stdout.write(f'ABRT {msg}\n')

        # flush the new lines
        self.stdout_flush()
        self.stderr_flush()

        if not self._ut_mode:
            sys.exit(1)

    # === UT functions

    # -------------------
    ## get ut_mode
    # @return ut_mode (true/false)
    @property
    def ut_mode(self):
        return self._ut_mode

    # -------------------
    ## set for ut_mode
    # @param  val   new value to use
    # @return None
    @ut_mode.setter
    def ut_mode(self, val):
        self._ut_mode = val
        if self._ut_mode:
            # set the values again for ut_mode
            self._set_all_data()

    # -------------------
    ## get set os_name
    # @param ut_os_name new value to use
    # @return ut_mode (true/false)
    def ut_info(self, ut_os_name):
        self._os_name = ut_os_name
        self._set_all_data()
