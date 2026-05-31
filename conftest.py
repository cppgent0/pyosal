from medver_pytest import pth


# -------------------
def pytest_addoption(parser):
    pth.cfg.cli_addoption(parser)


# -------------------
def pytest_configure(config):
    pth.cfg.cli_configure(config)
