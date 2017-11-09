import unittest
from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner

class Test(unittest.TestCase):

    if __name__ == '__main__':
        if is_running_under_teamcity():
            runner = TeamcityTestRunner()
        else:
            runner = unittest.TextTestRunner()
        unittest.main(testRunner=runner)
