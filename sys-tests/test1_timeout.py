import sys

from src.pyosal import pyosal

scenario = 'normal'
if len(sys.argv) > 1:
    scenario = sys.argv[1]

if scenario == 'normal':
    print(f'running {scenario} scenario: app ends before timeout')
    timeout = 3
    exp_rc = 0
elif scenario == 'graceful':
    print(f'running {scenario} scenario: app ends gracefully when terminated')
    timeout = 1
    exp_rc = 0
elif scenario == 'killed':
    print(f'running {scenario} scenario: app must be killed after terminated')
    timeout = 1
    exp_rc = 0
elif scenario == 'bad1':
    print(f'running {scenario} scenario: timeout is 0s')
    timeout = 0
    exp_rc = 0
elif scenario == 'bad2':
    print(f'running {scenario} scenario: timeout is -1s')
    timeout = -1
    exp_rc = 0

cmd = [sys.executable, 'sys-tests/test1_timer.py', '2', scenario]

rc = pyosal.run_cmd_timeout(timeout, cmd)
print(f'expected rc={exp_rc} act rc={rc}')
