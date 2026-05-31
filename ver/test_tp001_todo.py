import unittest

from medver_pytest import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp001Todo(unittest.TestCase):
    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()
        svc.helper = Helper()
        svc.helper.init()

    # -------------------
    def setUp(self):
        svc.helper.init_each_test(self)

    # -------------------
    def tearDown(self):
        svc.helper.term_each_test()

    # --------------------
    @classmethod
    def tearDownClass(cls):
        svc.helper.term()
        pth.term()

    # --------------------
    # @pytest.mark.skip(reason='skip')
    def test_tp001(self):
        pth.proto.protocol('tp-001', 'todo')
        pth.proto.add_objective('todo')
        pth.proto.add_precondition('do_install has been run')

        pth.proto.step('check current version')
        # pth.ver.verify_equal('0.1.0', svc.mut.version)

        pth.proto.step('first step')
        # pth.ver.verify_true(svc.mut.do_something_true(), reqids='SRS-001')
        # pth.ver.verify_false(svc.mut.do_something_false(), reqids='SRS-001')
