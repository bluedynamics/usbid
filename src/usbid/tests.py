import os
import doctest
import unittest
import tempfile
import tarfile
from interlude import interact
from pkg_resources import resource_filename
from pprint import pprint


optionflags = doctest.NORMALIZE_WHITESPACE | \
              doctest.ELLIPSIS | \
              doctest.REPORT_ONLY_FIRST_FAILURE

TEST_DATA_1 = resource_filename(__name__, 'testing/1.tgz')
TEST_DATA_2 = resource_filename(__name__, 'testing/2.tgz')
TEST_DATA_3 = resource_filename(__name__, 'testing/3.tgz')

TESTFILES = ['fs.rst']
TEMPDIR = tempfile.mkdtemp()

test_data_1_dir = os.path.join(TEMPDIR, '1')
tgz = tarfile.open(TEST_DATA_1)
tgz.extractall(test_data_1_dir)

test_data_2_dir = os.path.join(TEMPDIR, '2')
tgz = tarfile.open(TEST_DATA_2)
tgz.extractall(test_data_2_dir)

test_data_3_dir = os.path.join(TEMPDIR, '3')
tgz = tarfile.open(TEST_DATA_3)
tgz.extractall(test_data_3_dir)


def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite(
            filename,
            optionflags=optionflags,
            globs={'interact': interact,
                   'pprint': pprint,
                   'TEMPDIR': TEMPDIR
                   },
        ) for filename in TESTFILES
    ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')                 #pragma NO COVERAGE
