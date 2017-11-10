import unittest
from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner


class Test(unittest.TestCase):

    runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)
