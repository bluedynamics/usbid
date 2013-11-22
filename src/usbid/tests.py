from pkg_resources import resource_filename
TEST_USBIDS_FILE = resource_filename(__name__, 'data/testusb.ids')
import unittest
import doctest 
from pprint import pprint
from interlude import interact

optionflags = doctest.NORMALIZE_WHITESPACE | \
              doctest.ELLIPSIS | \
              doctest.REPORT_ONLY_FIRST_FAILURE

TESTFILES = [
    'usbinfo.rst',
    'test_device.rst',
]


def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite(
            filename, 
            optionflags=optionflags,
            globs={'interact': interact,
                   'pprint': pprint,
                   'TEST_USBIDS_FILE': TEST_USBIDS_FILE,
                   },
        ) for filename in TESTFILES
    ])

if __name__ == '__main__':                                   #pragma NO COVERAGE
    unittest.main(defaultTest='test_suite')                  #pragma NO COVERAGE