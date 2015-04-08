from interlude import interact
from pkg_resources import resource_filename
from pprint import pprint

import os
import doctest
import unittest
import tempfile
import tarfile


TEST_USBIDS_FILE = resource_filename(__name__, 'data/testusb.ids')
TEST_DATA = resource_filename(__name__, 'data/mocktree.tgz')


TEST_DATA_1 = resource_filename(__name__, 'data/test_1.tgz')


optionflags = doctest.NORMALIZE_WHITESPACE | \
              doctest.ELLIPSIS | \
              doctest.REPORT_ONLY_FIRST_FAILURE


TESTFILES = [
    'usbinfo.rst',
    'device.rst',
    'structure.rst',
]


TEMPDIR = tempfile.mkdtemp()

test_data_dir = os.path.join(TEMPDIR, 'mocktree')
tgz = tarfile.open(TEST_DATA)
tgz.extractall(test_data_dir)

test_data_1_dir = os.path.join(TEMPDIR, 'test_1')
tgz = tarfile.open(TEST_DATA_1)
tgz.extractall(test_data_1_dir)

# define the testing root path
MOCK_SYS = test_data_dir + '/sys/bus/usb/devices'


def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite(
            filename,
            optionflags=optionflags,
            globs={'interact': interact,
                   'pprint': pprint,
                   'TEST_USBIDS_FILE': TEST_USBIDS_FILE,
                   'MOCK_SYS': MOCK_SYS,
                   'TEMPDIR': TEMPDIR
                   },
        ) for filename in TESTFILES
    ])

if __name__ == '__main__':  # pragma NO COVERAGE
    unittest.main(defaultTest='test_suite')  # pragma NO COVERAGE
