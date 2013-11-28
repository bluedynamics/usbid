from pkg_resources import resource_filename
TEST_USBIDS_FILE = resource_filename(__name__, 'data/testusb.ids')

TEST_DATA = resource_filename(__name__, 'data/mocktree.tgz')
import unittest
import doctest
from pprint import pprint
from interlude import interact
import tempfile
import tarfile

optionflags = doctest.NORMALIZE_WHITESPACE | \
              doctest.ELLIPSIS | \
              doctest.REPORT_ONLY_FIRST_FAILURE

TESTFILES = [
    #'usbinfo.rst',
    'device.rst',
    #'device_list.rst',
]

TEMPDIR = tempfile.mkdtemp()

tgz = tarfile.open(TEST_DATA)
tgz.extractall(TEMPDIR)

#define the testing root path
MOCK_SYS = TEMPDIR + '/mocktree/sys/bus/usb/devices'

def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite(
            filename, 
            optionflags=optionflags,
            globs={'interact': interact,
                   'pprint': pprint,
                   'TEST_USBIDS_FILE': TEST_USBIDS_FILE,
                   'MOCK_SYS': MOCK_SYS,
                   },
        ) for filename in TESTFILES
    ])

if __name__ == '__main__':                                   #pragma NO COVERAGE
    unittest.main(defaultTest='test_suite')                  #pragma NO COVERAGE