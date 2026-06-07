# -------------------
def pytest_addoption(parser):
    from medver_pytest import pth

    pth.cfg.cli_addoption(parser)


# -------------------
def pytest_configure(config):
    from medver_pytest import pth

    pth.cfg.cli_configure(config)


# -------------------
##  Forces a newline on the terminal reporter right before printing PASSED/FAILED.
def pytest_report_teststatus(report, config):
    if report.when == 'call':
        # Get the standard pytest terminal reporter plugin
        terminal_reporter = config.pluginmanager.get_plugin('terminalreporter')
        if terminal_reporter:
            # Inject a literal newline directly onto the active pytest terminal stream
            terminal_reporter._tw.write('\n')  # pylint: disable=protected-access
