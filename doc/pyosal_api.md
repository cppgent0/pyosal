# pyosal API

This is a summary of the functions available for pyosal.

see ```sample/app.py``` for sample code.

> ## 📁 various OS values

### 🛠️ `os_name` (property)

get OS name/tag

* **Returns:** os_name

```python
if pyosal.os_name in ['ubuntu', 'macos']:
    svc.log.info(f'posix os: {pyosal.os_name}')
elif pyosal.os_name in ['msys2']:
    svc.log.info(f'win os  : {pyosal.os_name}')
else:
    svc.log.info(f'other   : {pyosal.os_name}')
```

### 🛠️ os_valid (property)

get list of recognized valid OS names. see ```os_name```

```python
svc.log.info(f'valid: {pyosal.os_valid}')
```

Output:

```text
valid: ['ubuntu', 'macos', 'msys2', 'psi', 'rpi']
```

### 🛠️  os_version (property)

get OS version info

* **Returns:** os_version

```python
svc.log.info(f'os_version: {pyosal.os_version}')
```

Output:

```text
os_version: Ubuntu 24.04 noble
```

### 🛠️  python_version (property)

get python version

* **Returns:** python_version

```python
svc.log.info(f'python_version: {pyosal.python_version}')
```

Output:

```text
python_version: Python 3.12
```

### 🛠️  userid (property)

get current userid

```python
svc.log.info(f'userid    : {pyosal.userid}')
```

Output:

```text
userid    : your-userid
```

* **Returns:** userid

### 🛠️  hostname (property)

get current PC's hostname

* **Returns:** hostname

```python
svc.log.info(f'hostname  : {pyosal.hostname}')
```

Output:

```text
hostname  : your-hostname
```

> ## 📁 ## various paths and repo info

### 🛠️  curr_repo_dir (property)

current repo directory converted to posix

* **Returns:** the repo dir path

```python
svc.log.info(f'curr_repo_dir : {pyosal.curr_repo_dir}')
```

Output:

```text
curr_repo_dir : /home/your-userid/projects/web/py-mods/pyosal
```

### 🛠️  curr_repo_name (property)

current repo name

* **Returns:** the repo name

```python
svc.log.info(f'curr_repo_name: {pyosal.curr_repo_name}')
```

Output:

```text
curr_repo_name: pyosal
```

### 🛠️  root_dir (property)

get path for root directory

* **Returns:** root_dir

```python
svc.log.info(f'root_dir : {pyosal.root_dir}')
```

Output:

```text
root_dir : ~
```

### 🛠️  root_dir_msys2 (property)

get root directory for msys2 shells

* **Returns:** root_dir_msys2

```python
svc.log.info(f'root_dir_msys2: {pyosal.root_dir_msys2}')
```

Output:

```text
root_dir_msys2: ~  # on msys2
root_dir_msys2: ~  # on ubuntu

```

> ## 📁 command runner functions

### 🛠️  run_cmd_timeout

run a command in a subprocess with a timeout

**Arguments:**

* `timeout`: (integer) max time to run cmd before terminating/killing the process
* `cmd`: the command to run
* `working_dir`: the working directory to run the command in; default is '.'
* `use_raw_log`: no prefix on line
* `log_file`: the log_file to write the lines to
* `print_cb`: callback function used to print output; default is None
* `env`: the environment variables to use
* `quiet`: if True, do not write to stdout
* `msys_tag`: used only for MSYS2 processes; matches command line content for PID to kill

* **Returns:** rc - return code, lines - the output as a list of lines

### 🛠️  run_cmd

run a command in a subprocess

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

### 🛠️  abort

abort the current script.

* **Arguments:**
`msg`: (optional) message to display

* **Returns:** does not return

> ## 📁 path translate functions

### 🛠️  xlat_to_win

convert a windows path to posix i.e. forward slashes

* **Arguments:**
`path`: the path to fix
`force`: force the conversion no matter what the OS is

* **Returns:** the unfixed path

### 🛠️  xlat_to_posix

convert a windows path to posix i.e. forward slashes

* **Arguments:**

* `path`: the path to fix
`force`: force the conversion no matter what the OS is

* **Returns:** the unfixed path

### 🛠️  xlat_dir_to_relative

convert a path to relative to home

* **Arguments:**
`path`: the path to fix

* **Returns:** the relative path

> ## 📁 misc functions

### 🛠️  stdout_flush

flush for stdout

* **Arguments:**
`force`: (optional) if True, do the buffer flush even if not msys2

### 🛠️  stderr_flush

flush for stderr

* **Arguments:**
`force`: (optional) if True, do the buffer flush even if not msys2

> ## 📁 UT and Debug functions

### 🛠️  ut_mode (getter)

get ut_mode

* **Returns:** ut_mode (true/false)

### 🛠️ ut_mode (setter)

set for ut_mode

* **Arguments:**
`val`: new value to use

* **Returns:** None
@ut_mode.setter

### 🛠️  ut_info

get set os_name

* **Arguments:**
`ut_os_name`: new value to use

* **Returns:** ut_mode (true/false)

### 🛠️  set_debug

set debug to print extra info.

* set()         : turn off debugging
* {'timed'}     : print()'s for run_cmd_timed
* {'run'}       : print()'s for run_cmd
* {'run', 'timed'} : for both

* **Arguments:**
`val`: the debug level to use

* **Returns:** None
