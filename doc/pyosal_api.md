# pyosal API

This is a summary of the functions available for pyosal.

see ```sample/app.py``` for sample code.

> ## 📁 various OS values

### 🛠️ `os_name` (property)

* **Desc:** get OS name/tag

* **Returns:** os_name

* Sample code:

    ```python
    if pyosal.os_name in ['ubuntu', 'macos']:
        svc.log.info(f'posix os: {pyosal.os_name}')
    elif pyosal.os_name in ['msys2']:
        svc.log.info(f'win os  : {pyosal.os_name}')
    else:
        svc.log.info(f'other   : {pyosal.os_name}')
    ```

* Output:

    ```text
    posix os: ubuntu
    ```

### 🛠️ os_valid (property)

* **Desc:** get list of recognized valid OS names. see ```os_name```

* Sample code:

    ```python
    svc.log.info(f'valid: {pyosal.os_valid}')
    ```

* Output:

    ```text
    valid: ['ubuntu', 'macos', 'msys2', 'psi', 'rpi']
    ```

### 🛠️  os_version (property)

* **Desc:** get OS version info

* **Returns:** os_version

* Sample code:

    ```python
    svc.log.info(f'os_version: {pyosal.os_version}')
    ```

* Output:

    ```text
    os_version: Ubuntu 24.04 noble
    ```

### 🛠️  python_version (property)

* **Desc:** get python version

* **Returns:** python_version

* Sample code:

    ```python
    svc.log.info(f'python_version: {pyosal.python_version}')
    ```

* Output:

    ```text
    python_version: Python 3.12
    ```

### 🛠️  userid (property)

* **Desc:** get current userid

* Sample code:

    ```python
    svc.log.info(f'userid    : {pyosal.userid}')
    ```

* Output:

    ```text
    userid    : your-userid
    ```

* **Returns:** userid

### 🛠️  hostname (property)

* **Desc:** get current PC's hostname

* **Returns:** hostname

* Sample code:

    ```python
    svc.log.info(f'hostname  : {pyosal.hostname}')
    ```

* Output:

    ```text
    hostname  : your-hostname
    ```

> ## 📁 various paths and repo info

### 🛠️  curr_repo_dir (property)

* **Desc:** get current repo directory converted to posix

* **Returns:** the repo dir path

* Sample code:

    ```python
    svc.log.info(f'curr_repo_dir : {pyosal.curr_repo_dir}')
    ```

* Output:

    ```text
    curr_repo_dir : /home/your-userid/projects/web/py-mods/pyosal
    ```

### 🛠️  curr_repo_name (property)

* **Desc:** get current repo name

* **Returns:** the repo name

* Sample code:

    ```python
    svc.log.info(f'curr_repo_name: {pyosal.curr_repo_name}')
    ```

* Output:

    ```text
    curr_repo_name: pyosal
    ```

### 🛠️  root_dir (property)

* **Desc:** get path for root directory

* **Returns:** root_dir

* Sample code:

    ```python
    svc.log.info(f'root_dir : {pyosal.root_dir}')
    ```

* Output:

    ```text
    root_dir : ~                     # on ubuntu
    root_dir : C:/Users/your-userid  # on MSYS2
    root_dir : ~                     # on macos
    ```

### 🛠️  root_dir_msys2 (property)

* **Desc:** get root directory for msys2 shells

* **Returns:** root_dir_msys2

* Sample code:

    ```python
    svc.log.info(f'root_dir_msys2: {pyosal.root_dir_msys2}')
    ```

* Output:

    ```text
    root_dir_msys2: ~                     # on ubuntu
    root_dir_msys2: /c/Users/your-userid  # on MSYS2 (note path is posix)
    root_dir_msys2: ~                     # on macos
    ```

> ## 📁 command runner functions

### 🛠️  run_cmd_timeout

* **Desc:** run a command in a subprocess with a timeout

* **Arguments:**

    * `timeout`: (integer) max time to run cmd before terminating/killing the process
    * `cmd`: the command to run
    * `working_dir`: the working directory to run the command in; default is '.'
    * `use_raw_log`: no prefix on line
    * `log_file`: the log_file to write the lines to
    * `print_cb`: callback function used to print output; default is None
    * `env`: the environment variables to use
    * `quiet`: if True, do not write to stdout
    * `msys_tag`: used only for MSYS2 processes; matches command line content for PID to kill

* **Returns:** rc - return code

* Sample code:

    ```python
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
    ```

* Output:

    ```text
    # on ubuntu: displays GUI app (e.g. gedit) for 3s, then automatically closes
    run_cmd_timeout: running
    [timeout] exceeded 3s, terminating process...
    [timeout] rc=-15 process terminated gracefully
    [timeout] rc=0   process ended due to timeout
    run_cmd_timeout rc=0

    # on MSYS2 : displays GUI app (e.g. notepad) for 3s, then automatically closes
    run_cmd_timeout: running
    [timeout] exceeded 3s, terminating process...
    [timeout] msys2 detected...
    [timeout] rc=0   process terminated gracefully
    [timeout] rc=0   process ended due to timeout

    # on macos : displays GUI app (e.g. TextEdit) for 3s, then automat
    run_cmd_timeout: running
    [timeout] exceeded 3s, terminating process...
    [timeout] macos detected...
    [timeout] rc=0   process terminated gracefully
    [timeout] rc=0   process ended due to timeout
    run_cmd_timeout rc=0
    ```

Also see ```sys-tests/test1.sh``` and ```test1-timeout.py``` for more examples:

```bash
sys-tests/test1.sh normal
# typical output:
running normal scenario: app ends before timeout
  -- test1_timer: scenario:normal max_time=2
  -- 00:00.000      elapsed=0.0
  -- 00:00.300      awake
  -- 00:00.300      elapsed=0.3
  -- 00:00.600      awake
  -- 00:00.600      elapsed=0.6
  -- 00:00.900      awake
  -- 00:00.900      elapsed=0.9
  -- 00:01.200      awake
  -- 00:01.200      elapsed=1.2
  -- 00:01.501      awake
  -- 00:01.501      elapsed=1.5
  -- 00:01.801      awake
  -- 00:01.801      elapsed=1.8
  -- 00:02.101      awake
  -- 00:02.101      elapsed=2.1
  -- 00:02.101      exiting at: 2.1
[timeout] rc=0   process finished before timeout
expected rc=0 act rc=0
test1: rc=0
```

### 🛠️  run_cmd

* **Desc:** run a command in a subprocess

* **Arguments:**

    * `cmd`: the command to run
    * `working_dir`: the working directory to run the command in; default is '.'
    * `use_raw_log`: no prefix on line
    * `log_file`: the log_file to write the lines to
    * `print_cb`: callback function used to print output; default is None
    * `env`: the environment variables to use
    * `quiet`: if True, do not write to stdout
    * `shared_container`: used by run_cmd_container to receive the proc value

* **Returns:** rc - return code, lines - the output as a list of lines

* Sample code:

    ```python
    svc.log.info('run_cmd: running')
    cmd = ['pwd']
    rc, lines = pyosal.run_cmd(cmd)
    svc.log.info(f'run_cmd rc={rc}')
    for lineno, line in enumerate(lines):
        svc.log.info(f'  line {lineno}: {line}')
    ```

* Output:

    ```text
    # on ubuntu
    run_cmd: running
    -- /home/your-userid/projects/web/py-mods/pyosal
    run_cmd rc=0

    # on MSYS2
    run_cmd: running
      -- C:/Users/your-userid/projects/web/py-mods/pyosal
    run_cmd rc=0

    # on macos
    run_cmd: running
      -- /Users/your-userid/projects/web/py-mods/pyosal
    run_cmd rc=0
    ```

### 🛠️  abort

* **Desc:** abort the current script. Does a sys.exit(1)
    so the script will have a return code of 1.

* **Arguments:**
`msg`: (optional) message to display

* **Returns:** does not return

* Sample code:

    ```python
    pyosal.abort('test of abort')
    pyosal.abort()
    ```

* Output:

    ```text
    # note: only one of these lines is output
    ABRT test of abort
    ABRT abort occurred, exiting
    ```

> ## 📁 path translate functions

### 🛠️  xlat_to_win

* **Desc:** convert a windows path to posix i.e. forward slashes

* **Arguments:**
    * `path`: the path to fix
    * `force`: force the conversion no matter what the OS is

* **Returns:** the unfixed path

* Sample code:

    ```python
    path = '/c/dir1/dir2'
    svc.log.info(f'xlat_to_win  : {pyosal.xlat_to_win(path)}')
    svc.log.info(f'xlat_to_win  : {pyosal.xlat_to_win(path, force=True)}')
    ```

* Output:

    ```text
    # on ubuntu
    xlat_to_win  : \c\dir1\dir2
    xlat_to_win  : C:\dir1\dir2   # with force
   
    # on MSYS2
    xlat_to_win  : C:\dir1\dir2
    xlat_to_win  : C:\dir1\dir2   # with force
    ```

### 🛠️  xlat_to_posix

* **Desc:** convert a windows path to posix i.e. forward slashes

* **Arguments:**
    * `path`: the path to fix
    * `force`: force the conversion no matter what the OS is

* **Returns:** the unfixed path

* Sample code:

    ```python
    path = 'c:\\dir1\\dir2'
    svc.log.info(f'xlat_to_posix: {pyosal.xlat_to_posix(path)}')
    svc.log.info(f'xlat_to_posix: {pyosal.xlat_to_posix(path, force=True)}')
    ```

* Output:

    ```text
    # on ubuntu 
    xlat_to_posix: c:/dir1/dir2
    xlat_to_posix: /c/dir1/dir2  # with force

    # on MSYS2
    xlat_to_posix: /c/dir1/dir2
    xlat_to_posix: /c/dir1/dir2  # with force
    ```

### 🛠️  xlat_dir_to_relative

* **Desc:** convert a path to relative to home

* **Arguments:**
    * `path`: the path to fix

* **Returns:** the relative path

* Sample code:

    ```python
    path = '/home/your-userid\\dir1\\dir2'
    svc.log.info(f'xlat_dir_to_relative: {pyosal.xlat_dir_to_relative(path)}')
    path = '/c/Users/your-userid/dir1/dir2'
    svc.log.info(f'xlat_dir_to_relative: {pyosal.xlat_dir_to_relative(path)}')
    ```

* Output:

    ```text
    # on ubuntu, MSYS2
    xlat_dir_to_relative: ~/dir1/dir2
    xlat_dir_to_relative: ~/dir1/dir2
    ```

> ## 📁 misc functions

### 🛠️  stdout_flush

* **Desc:** flush for stdout

* **Arguments:**
    * `force`: (optional) if True, do the buffer flush even if not msys2

* Sample code:

    ```python
    pyosal.stdout_flush()
    pyosal.stdout_flush(force=True)
    ```

* Output:

    ```text
    # no output for this command
    ```

### 🛠️  stderr_flush

* **Desc:**  flush for stderr

* **Arguments:**
    * `force`: (optional) if True, do the buffer flush even if not msys2

* Sample code:

    ```python
    pyosal.stderr_flush()
    pyosal.stderr_flush(force=True)
    ```

* Output:

    ```text
    # no output for this command
    ```

> ## 📁 UT and Debug functions

### 🛠️ ut_mode (setter/getter)

* **Desc:** set for ut_mode.
  if set to False (default) then it behaves as per the actual OS.
  if set to True, then it returns specific values for ```os_version```

Note: this may change as UT needs are met.

* **Arguments:**
    * `val`: new value to use

* **Returns:** None

* Sample code:

    ```python
    pyosal.ut_mode = False
    svc.log.info(f'ut_mode:{str(pyosal.ut_mode): <5} name:{pyosal.os_name} vers:{pyosal.os_version}')
    pyosal.ut_mode = True
    svc.log.info(f'ut_mode:{str(pyosal.ut_mode): <5} name:{pyosal.os_name} vers:{pyosal.os_version}')  
    ```

* Output:

    ```text
    # on ubuntu: (may change)
    ut_mode:False name:ubuntu vers:Ubuntu 24.04 noble
    ut_mode:True  name:ubuntu vers:ut Ubuntu 24.04 noble

    # on msys2: (may change)
    ut_mode:False name:msys2 vers:win32 Windows 11
    ut_mode:True  name:msys2 vers:ut win32 Windows 11

    # on macos: (may change)
    ut_mode:False name:macos vers:macOS 26.6
    ut_mode:True  name:macos vers:ut macOS 26.6
    ```

### 🛠️  ut_info

* **Desc:** set os_name to use

* **Arguments:**
    * `ut_os_name`: new value to use

* **Returns:** ut_mode (true/false)

* Sample code:

    ```python
    if pyosal.os_name == 'ubuntu':
        ut_os = 'macos'
    elif pyosal.os_name == 'macos':
        ut_os = 'msys2'
    elif pyosal.os_name == 'msys2':
        ut_os = 'ubuntu'
    real_os = pyosal.os_name
    svc.log.info(f'on {real_os}: {pyosal.os_name}')
    pyosal.ut_info(ut_os)
    svc.log.info(f'on {real_os}: {pyosal.os_name}')
    ```

* Output:

    ```text
    # on ubuntu
    on ubuntu before: ubuntu
    on ubuntu after : macos

    # on msys2
    on msys2 before: msys2
    on msys2 after : ubuntu

    # on macos
    on macos before: macos 
    on macos after : msys2
    ```

### 🛠️  set_debug

* **Desc:** set debug to print extra info.
  see ```run_cmd_timeout()``` and ```run_cmd``` code.

* **Arguments:**
    * `val`: the debug level to use
        * set()         : turn off debugging
        * {'timed'}     : print()'s for run_cmd_timed
        * {'run'}       : print()'s for run_cmd
        * {'run', 'timed'} : for both

* **Returns:** None
