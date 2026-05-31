import unittest

from falcon_logger import FalconLogger

from src.pyosal import pyosal

log = FalconLogger(mode='ut')
log.set_format('none')


# -------------------
## UT for TODO ...
class TestTodo(unittest.TestCase):
    # --------------------
    ## done once at start of the unit test suite
    @classmethod
    def setUpClass(cls):
        pass

    # -------------------
    ## done once at start of each unit test in the suite
    def setUp(self):
        print('')
        self.mut = pyosal

    # -------------------
    ## done once at end of each unit test in the suite
    def tearDown(self):
        pass

    # --------------------
    ## done once at end of the unit test suite
    @classmethod
    def tearDownClass(cls):
        pass

    # -------------------
    # @pytest.mark.skip(reason='skip')
    def test_todo_1(self):
        log.ut_clear()
        log.info('line1')
        log.info('line2')
        self.assertEqual(2, len(log.ut_lines))
        self.assertEqual('line1', log.ut_lines[0])
        self.assertEqual('line2', log.ut_lines[1])

        # self.assertTrue(self.mut.do_ut_true())
        # self.assertFalse(self.mut.do_ut_false())
