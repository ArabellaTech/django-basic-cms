"""Django page CMS test suite module"""
import unittest
from basic_cms.tests.test_functionnal import FunctionnalTestCase
from basic_cms.tests.test_unit import UnitTestCase
from basic_cms.tests.test_regression import RegressionTestCase
from basic_cms.tests.test_auto_render import AutoRenderTestCase


def suite():
    suite = unittest.TestSuite()
    from basic_cms import settings
    if not settings.PAGE_ENABLE_TESTS:
        return suite
    suite.addTest(unittest.makeSuite(UnitTestCase))
    suite.addTest(unittest.makeSuite(RegressionTestCase))
    suite.addTest(unittest.makeSuite(AutoRenderTestCase))
    # being the slower test I run it at the end
    suite.addTest(unittest.makeSuite(FunctionnalTestCase))
    return suite
