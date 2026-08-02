* website: [Website](https://arrizza.com/pyosal.html)
* installation: [Common Setup](https://arrizza.com/setup-common.html)

## Summary

pyosal is an Operating System Abstraction Layer written in Python.
It contains various functions help write cross-platform python code.

see ```doc/pyosal_api.md``` or the website above for more information about these functions.

Over time, I will be searching through my projects looking for code like:

```python
if  pyosal.os_name == 'ubuntu':
    do_some_thing_ubu()
elif  pyosal.os_name == 'msys2':
    do_some_thing_msys2()
```

It might be possible that do_some_thing() is a viable OSAL function to be added to pyosal.

## Function Summary

A summary of the functions available are:

| Name | Type | Description |
| :--- | :--- | :--- |
| `os_name` | property | get OS name/tag |
| `os_version` | property | get OS version info |
| `python_version` | property | get python version info |
| `root_dir` | property | get path for root directory |
| `root_dir_msys2` | property | get root directory for msys2 shells |
| `userid` | property | get current userid |
| `hostname` | property | get current PC's hostname |
| `os_valid` | property | get list of recognized valid OS names |
| `curr_repo_dir` | property | current repo directory converted to posix |
| `curr_repo_name` | property | current repo name |
| `run_cmd_timeout` | function | run a command in a subprocess, terminate after a timeout |
| `run_cmd` | function | run a command in a subprocess |
| `stdout_flush` | function | flush for stdout |
| `stderr_flush` | function | flush for stderr |
| `xlat_to_win` | function | convert a path to windows i.e. backslashes |
| `xlat_to_posix` | function | convert a path to posix i.e. forward slashes |
| `xlat_dir_to_relative` | function | convert a path to relative to home |
| `abort` | function | abort the current script |
