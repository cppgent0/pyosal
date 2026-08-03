import sys

from src.pyosal import pyosal

scenario = 'normal'
if len(sys.argv) > 1:
    scenario = sys.argv[1]

gui = None
cmd_tag = None
if scenario == 'normal':
    print(f'running {scenario} scenario: app ends before timeout')
    timeout = 3
    exp_rc = 0
    cmd_tag = 'normal'
elif scenario == 'graceful':
    print(f'running {scenario} scenario: app ends gracefully when terminated')
    timeout = 1
    exp_rc = 0
    cmd_tag = 'graceful'
elif scenario == 'killed':
    print(f'running {scenario} scenario: app must be killed after terminated')
    timeout = 1
    exp_rc = 0
    cmd_tag = 'killed'
elif scenario == 'gui':
    if pyosal.os_name == 'ubuntu':
        gui = ['gedit', 'out/abc.txt']
    elif pyosal.os_name == 'msys2':
        gui = ['notepad']
        cmd_tag = 'notepad.exe'
    elif pyosal.os_name == 'macos':
        gui = ['open', '-a', 'TextEdit']
        cmd_tag = 'TextEdit'
    print(f'running {scenario} scenario: timeout is 3s but the app is gui: "{gui}"')
    timeout = 3
    exp_rc = 0
elif scenario == 'bad1':
    print(f'running {scenario} scenario: timeout is 0s')
    timeout = 0
    exp_rc = 0
    cmd_tag = 'bad1'
elif scenario == 'bad2':
    print(f'running {scenario} scenario: timeout is -1s')
    timeout = -1
    exp_rc = 0
    cmd_tag = 'bad2'
else:
    pyosal.abort(f'unknown scenario; "{scenario}", use normal,graceful,killed,gui,bad1,bad2')

if gui:
    cmd = gui
else:
    cmd = [pyosal.xlat_to_posix(sys.executable), 'sys-tests/test1_timer.py', '2', scenario]
    cmd_tag = 'test1_timer.py'

rc = pyosal.run_cmd_timeout(timeout, cmd, cmd_tag=cmd_tag)
print(f'expected rc={exp_rc} act rc={rc}')
