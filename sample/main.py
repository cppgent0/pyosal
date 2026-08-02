from falcon_logger import FalconLogger

from sample.app import App
from sample.svc import svc


# --------------------
## mainline
def main():
    svc.log = FalconLogger(mode='immediate')
    svc.log.set_format('none')

    app = App()
    app.init()
    app.run()


# --------------------
if __name__ == '__main__':
    main()
