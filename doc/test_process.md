# How to test pyosal

## Test process

Run the following in order:

1. **ensure xplat_utils is installed**

    The first time after cloning this project, or for any updates, run:

    ```bash
    zpm xplat-install
    ```

1. **remove out directory**

    This step ensures the output directory has no stale data in it.

    ```bash
    zpm clean       # to clean out directory
    zpm clean full  # to clean out pycaches, coverage, and other temp files
    ```

1. **run do_install**

    This step ensures additional utilities and python modules are installed correctly

    ```bash
    zpm install full   # to install any OS packages and virtualenv
    zpm install sync   # to install virtualenv only
    zpm install fast   # to do a quick check of virtualenv
    zpm install        # same as fast
    ```

    * **Expected**: no warnings or errors

1. **run doxygen**

    This step generates the low-level documentation

    ```bash
    zpm doc      # generate doxygen doc
    zpm check    # check Doxyfile content
    ```

    * **Expected**: out/doxygen.txt is empty, has no warnings or errors
    * **Expected**: the out/(project-name).pdf contains full low-level documentation

1. **run static analysis**

    This step runs various static analysis tests

    ```bash
    zpm lint       # run pylint linter
    zpm lint ruff  # run ruff linter
    ```

    * **Expected**: no warnings or errors

1. **run publish**

    This step ensures the public version matches the current tested version

    ```bash
    # if necessary, update xplat.cfg with a new version string
    zpm publish
    # for development; allow publish if even there are open git operations
    zpm publish allow
    ```

    * **Expected**: no warnings or errors to stdout/stderr
    * **Expected**: Pypi version should be the same the version as in lib/version.json
    * **Expected**: this module's installed version should be the same the version as in lib/version.json

1. **run the project**

    This step ensures sample tests of the module can be run

    ```bash
    zpm doit
    ```

    * **Expected**: no failures or other warnings, PASSED only

1. **run verification**

    ```bash
    zpm ver   # must be done first to clear coverage
    zpm ut
    ```

    * **Expected**: out/ver/summary.pdf shows all requirements tested and passed
    * **Expected**: out/ver directory is created
    * **Expected**: out/coverage/index.html shows high coverage, typically 95% or better

1. **repeat these steps on the other OS platforms**

    * **Expected**: all OS platforms should behave the same
