import itertools
import signal
import sys
import time

from falcon_logger import FalconLogger


class GracefulShutdown(Exception):
    pass


def handle_sigterm(signum, frame):
    # This forces Python to raise an exception when SIGTERM is received
    raise GracefulShutdown('Received SIGTERM from parent process')


if not hasattr(signal, 'SIGTERM'):
    print('HUH!! NO SIGTERM')
    sys.stdout.flush()

signal.signal(signal.SIGTERM, handle_sigterm)

max_time = int(sys.argv[1])
scenario = sys.argv[2]
print(f'test1_timer: scenario:{scenario} max_time={max_time}')

log = FalconLogger(mode='immediate')
colors = ['red', 'yellow', 'green', 'blue']
color = itertools.cycle(colors)
start_time = time.time()
try:
    while True:
        elapsed = time.time() - start_time
        log.line(f'elapsed={round(elapsed, 1)}')
        sys.stdout.flush()
        if elapsed >= max_time:
            break
        time.sleep(0.300)
        log.line('awake', color=next(color))
except Exception as excp:
    print(f'exception occurred: {excp}')
    if scenario == 'killed':
        max_time = int(sys.argv[1])
        time.sleep(max_time)

elapsed = time.time() - start_time
log.line(f'exiting at: {round(elapsed, 1)}')
