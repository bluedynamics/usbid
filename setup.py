import os
from setuptools import setup
from setuptools import find_packages


version = '1.0.1'
shortdesc = \
'API to get information about USB devices'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()
tests_require = ['interlude', 'ipython']


setup(
    name='usbid',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'License :: OSI Approved :: BSD License',
    ],
    keywords='usb python',
    author='BlueDynamics Alliance',
    author_email='dev@bluedynamics.com',
    url="http://pypi.python.org/pypi/usbid",
    license='Simplified BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'setuptools',
    ],
    tests_require=tests_require,
    test_suite="usbid.tests.test_suite",
    extras_require=dict(
        test=tests_require,
    ),
    entry_points={},
)
