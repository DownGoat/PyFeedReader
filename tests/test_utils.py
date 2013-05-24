__author__ = 'sis13'

import unittest
from pyfeedreader.util import *


class UtilsTests(unittest.TestCase):
    def test_validate_url(self):
        try:
            validate_url("http://downgoat.net")
        except ValueError:
            self.fail("Exception raised.")

    def test_validate_url_bad(self):
        self.assertRaises(ValueError, validate_url, "downgoat.net")

if __name__ == '__main__':
    unittest.main()
