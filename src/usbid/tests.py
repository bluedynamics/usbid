from pkg_resources import resource_filename
import doctest
import os
import shutil
import sys
import tarfile
import tempfile
import unittest
from usbid.fs import Container
from usbid.fs import FileAttributes
from usbid import USB
from usbid import Bus


def get_file_attribues(obj):
    ret = []
    for attr_name in obj.__file_attributes__:
        ret.append((attr_name, getattr(obj, attr_name)))
    return ret


class Example(object):

    def __init__(self, want):
        self.want = want + '\n'


class Failure(Exception):
    pass


class TestUsbid(unittest.TestCase):

    def __init__(self, *args, **kw):
        unittest.TestCase.__init__(self, *args, **kw)
        self._checker = doctest.OutputChecker()
        self._optionflags = (
            doctest.NORMALIZE_WHITESPACE |
            doctest.ELLIPSIS |
            doctest.REPORT_ONLY_FIRST_FAILURE
        )

    def checkOutput(self, want, got, optionflags=None):
        if optionflags is None:
            optionflags = self._optionflags
        success = self._checker.check_output(want, got, optionflags)
        if not success:
            raise Failure(self._checker.output_difference(
                Example(want),
                got, optionflags
            ))

    @classmethod
    def setUpClass(cls):
        test_data_1 = resource_filename(__name__, 'testing/1.tgz')
        test_data_2 = resource_filename(__name__, 'testing/2.tgz')
        test_data_3 = resource_filename(__name__, 'testing/3.tgz')

        cls.tempdir = tempfile.mkdtemp()

        test_data_1_dir = os.path.join(cls.tempdir, '1')
        tgz = tarfile.open(test_data_1)
        tgz.extractall(test_data_1_dir)

        test_data_2_dir = os.path.join(cls.tempdir, '2')
        tgz = tarfile.open(test_data_2)
        tgz.extractall(test_data_2_dir)

        test_data_3_dir = os.path.join(cls.tempdir, '3')
        tgz = tarfile.open(test_data_3)
        tgz.extractall(test_data_3_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tempdir)

    def test_Container(self):
        container = Container()
        with self.assertRaises(NotImplementedError):
            container.keys()
        with self.assertRaises(NotImplementedError):
            container['key']

        class TestContainer(Container):
            def __iter__(self):
                return iter(['1', '2'])
            def __getitem__(self, key):
                return key

        test_container = TestContainer()
        self.assertEqual(test_container.keys(), ['1', '2'])
        self.assertEqual(test_container['1'], '1')

    def test_FileAttributes(self):
        with open(os.path.join(self.tempdir, 'file_attribute'), 'wt') as file:
            file.write('File attribute value')

        class TestFileAttributes(FileAttributes):
            __file_attributes__ = ['file_attribute']
            fs_path = self.tempdir
            class_attribute = 'Class Attribute'

        test_file_attributes = TestFileAttributes()
        self.assertEqual(
            test_file_attributes.class_attribute,
            'Class Attribute'
        )
        self.assertEqual(
            test_file_attributes.file_attribute,
            'File attribute value'
        )
        with self.assertRaises(AttributeError):
            test_file_attributes.no_attribute

        self.assertEqual(
            get_file_attribues(test_file_attributes),
            [('file_attribute', 'File attribute value')]
        )

    def test_USB(self):
        test_data_1_dir = os.path.join(
            self.tempdir, '1', 'sys', 'bus', 'usb', 'devices')

        usb = USB(fs_path=test_data_1_dir)
        self.checkOutput(
            '<usbid.fs.USB [/.../1/sys/bus/usb/devices] at ...>',
            str(usb)
        )
        self.assertTrue(usb.fs_path.endswith('/1/sys/bus/usb/devices'))
        self.assertEqual(usb.fs_name, 'devices')
        self.assertTrue(usb.fs_parent.endswith('/1/sys/bus/usb'))
        self.assertEqual(sorted(usb.keys()), ['1', '2', '3', '4'])
        with self.assertRaises(KeyError):
            usb['0']
        self.checkOutput('<usbid.fs.Bus [usb1] at ...>', str(usb['1']))

        self.checkOutput("""
        [<usbid.fs.Bus [usb1] at ...>,
        <usbid.fs.Bus [usb2] at ...>,
        <usbid.fs.Bus [usb3] at ...>,
        <usbid.fs.Bus [usb4] at ...>]
        """, str(sorted(usb.values(), key=lambda x: x.fs_name)))

        self.checkOutput("""
        [('1', <usbid.fs.Bus [usb1] at ...>),
        ('2', <usbid.fs.Bus [usb2] at ...>),
        ('3', <usbid.fs.Bus [usb3] at ...>),
        ('4', <usbid.fs.Bus [usb4] at ...>)]
        """, str(sorted(usb.items())))

        MARKER = object()
        self.assertTrue(usb.get('0', default=MARKER) is MARKER)
        self.assertFalse(usb.get('1', default=MARKER) is MARKER)

    def test_Bus(self):
        with self.assertRaises(ValueError) as arc:
            Bus(name=None, parent=None, fs_path='inexistent')
        self.assertEqual(str(arc.exception), 'Invalid path given')

        test_data_1_dir = os.path.join(
            self.tempdir, '1', 'sys', 'bus', 'usb', 'devices')
        usb = USB(fs_path=test_data_1_dir)

        bus = usb['3']
        self.checkOutput('<usbid.fs.Bus [usb3] at ...>', str(bus))
        self.assertEqual(bus.name, '3')
        self.assertEqual(sorted(bus.keys()), ['2', '4'])
        with self.assertRaises(KeyError):
            bus['1']
        self.checkOutput('<usbid.fs.Port [3-2] at ...>', str(bus['2']))

        self.checkOutput("""
        [<usbid.fs.Port [3-2] at ...>,
        <usbid.fs.Port [3-4] at ...>]
        """, str(sorted(bus.values(), key=lambda x: x.name)))

        self.checkOutput("""
        [('2', <usbid.fs.Port [3-2] at ...>),
        ('4', <usbid.fs.Port [3-4] at ...>)]
        """, str(sorted(bus.items(), key=lambda x: x[0])))

        self.assertEqual(get_file_attribues(bus), [
            ('authorized', '1'),
            ('authorized_default', '1'),
            ('avoid_reset_quirk', '0'),
            ('bcdDevice', '0313'),
            ('bConfigurationValue', '1'),
            ('bDeviceClass', '09'),
            ('bDeviceProtocol', '01'),
            ('bDeviceSubClass', '00'),
            ('bmAttributes', 'e0'),
            ('bMaxPacketSize0', '64'),
            ('bMaxPower', '0mA'),
            ('bNumConfigurations', '1'),
            ('bNumInterfaces', '1'),
            ('busnum', '3'),
            ('dev', '189:256'),
            ('devnum', '1'),
            ('devpath', '0'),
            ('idProduct', '0002'),
            ('idVendor', '1d6b'),
            ('ltm_capable', 'no'),
            ('manufacturer', 'Linux 3.13.0-48-generic xhci_hcd'),
            ('maxchild', '4'),
            ('product', 'xHCI Host Controller'),
            ('quirks', '0x0'),
            ('removable', 'unknown'),
            ('serial', '0000:00:14.0'),
            ('speed', '480'),
            ('uevent', 'MAJOR=189\nMINOR=256\nDEVNAME=bus/usb/003/001\nDEVTYPE=usb_device\nDRIVER=usb\nPRODUCT=1d6b/2/313\nTYPE=9/0/1\nBUSNUM=003\nDEVNUM=001'),
            ('urbnum', '884'),
            ('version', '2.00')
        ])

        self.checkOutput('[<usbid.fs.Interface [3-0:1.0] at ...>]', str(bus.interfaces))
        interface = bus.interfaces[0]
        self.assertEqual(get_file_attribues(interface), [
            ('bAlternateSetting', '0'),
            ('bInterfaceClass', '09'),
            ('bInterfaceNumber', '00'),
            ('bInterfaceProtocol', '00'),
            ('bInterfaceSubClass', '00'),
            ('bNumEndpoints', '01'),
            ('interface', None),
            ('modalias', 'usb:v1D6Bp0002d0313dc09dsc00dp01ic09isc00ip00in00'),
            ('supports_autosuspend', '1'),
            ('uevent', 'DEVTYPE=usb_interface\nDRIVER=hub\nPRODUCT=1d6b/2/313\nTYPE=9/0/1\nINTERFACE=9/0/0\nMODALIAS=usb:v1D6Bp0002d0313dc09dsc00dp01ic09isc00ip00in00')
        ])

"""
Port
----

::

    >>> from usbid import Port
    >>> Port(name=None, parent=None, fs_path='inexistent')
    Traceback (most recent call last):
      ...
    ValueError: Invalid path given

    >>> port = bus['2']
    >>> port
    <usbid.fs.Port [3-2] at ...>

    >>> port.fs_path
    '.../1/sys/bus/usb/devices/usb3/3-2'

    >>> port.fs_name
    '3-2'

    >>> get_file_attribues(port)
    [('authorized', '1'),
    ('avoid_reset_quirk', '0'),
    ('bcdDevice', '0100'),
    ('bConfigurationValue', '1'),
    ('bDeviceClass', '09'),
    ('bDeviceProtocol', '01'),
    ('bDeviceSubClass', '00'),
    ('bmAttributes', 'e0'),
    ('bMaxPacketSize0', '64'),
    ('bMaxPower', '100mA'),
    ('bNumConfigurations', '1'),
    ('bNumInterfaces', '1'),
    ('busnum', '3'),
    ('dev', '189:378'),
    ('devnum', '123'),
    ('devpath', '2'),
    ('idProduct', '005a'),
    ('idVendor', '0409'),
    ('ltm_capable', 'no'),
    ('manufacturer', None),
    ('maxchild', '4'),
    ('product', None),
    ('quirks', '0x0'),
    ('removable', 'removable'),
    ('serial', None),
    ('speed', '480'),
    ('uevent', 'MAJOR=189\nMINOR=378\nDEVNAME=bus/usb/003/123\nDEVTYPE=usb_device\nDRIVER=usb\nPRODUCT=409/5a/100\nTYPE=9/0/1\nBUSNUM=003\nDEVNUM=123'),
    ('urbnum', '47'),
    ('version', '2.00')]

    >>> port.interfaces
    [<usbid.fs.Interface [3-2:1.0] at ...>]

    >>> interface = port.interfaces[0]
    >>> get_file_attribues(interface)
    [('bAlternateSetting', '0'),
    ('bInterfaceClass', '09'),
    ('bInterfaceNumber', '00'),
    ('bInterfaceProtocol', '00'),
    ('bInterfaceSubClass', '00'),
    ('bNumEndpoints', '01'),
    ('interface', None),
    ('modalias', 'usb:v0409p005Ad0100dc09dsc00dp01ic09isc00ip00in00'),
    ('supports_autosuspend', '1'),
    ('uevent', 'DEVTYPE=usb_interface\nDRIVER=hub\nPRODUCT=409/5a/100\nTYPE=9/0/1\nINTERFACE=9/0/0\nMODALIAS=usb:v0409p005Ad0100dc09dsc00dp01ic09isc00ip00in00')]

    >>> sorted(port.keys())
    ['1', '2', '3', '4']

    >>> port['0']
    Traceback (most recent call last):
      ...
    KeyError: '0'

    >>> sub_port = port['1']
    >>> sub_port
    <usbid.fs.Port [3-2.1] at ...>

    >>> sub_port.fs_path
    '.../1/sys/bus/usb/devices/usb3/3-2/3-2.1'

    >>> sub_port.fs_name
    '3-2.1'

    >>> get_file_attribues(sub_port)
    [('authorized', '1'),
    ('avoid_reset_quirk', '0'),
    ('bcdDevice', '0600'),
    ('bConfigurationValue', '1'),
    ('bDeviceClass', '00'),
    ('bDeviceProtocol', '00'),
    ('bDeviceSubClass', '00'),
    ('bmAttributes', 'a0'),
    ('bMaxPacketSize0', '8'),
    ('bMaxPower', '90mA'),
    ('bNumConfigurations', '1'),
    ('bNumInterfaces', '1'),
    ('busnum', '3'),
    ('dev', '189:379'),
    ('devnum', '124'),
    ('devpath', '2.1'),
    ('idProduct', '6001'),
    ('idVendor', '0403'),
    ('ltm_capable', 'no'),
    ('manufacturer', 'FTDI'),
    ('maxchild', '0'),
    ('product', 'FT232R USB UART'),
    ('quirks', '0x0'),
    ('removable', 'unknown'),
    ('serial', 'A7022OOQ'),
    ('speed', '12'),
    ('uevent', 'MAJOR=189\nMINOR=379\nDEVNAME=bus/usb/003/124\nDEVTYPE=usb_device\nDRIVER=usb\nPRODUCT=403/6001/600\nTYPE=0/0/0\nBUSNUM=003\nDEVNUM=124'),
    ('urbnum', '15'),
    ('version', '2.00')]

    >>> sub_port.interfaces
    [<usbid.fs.Interface [3-2.1:1.0] at ...>]

    >>> interface = sub_port.interfaces[0]
    >>> get_file_attribues(interface)
    [('bAlternateSetting', '0'),
    ('bInterfaceClass', 'ff'),
    ('bInterfaceNumber', '00'),
    ('bInterfaceProtocol', 'ff'),
    ('bInterfaceSubClass', 'ff'),
    ('bNumEndpoints', '02'),
    ('interface', 'FT232R USB UART'),
    ('modalias', 'usb:v0403p6001d0600dc00dsc00dp00icFFiscFFipFFin00'),
    ('supports_autosuspend', '1'),
    ('uevent', 'DEVTYPE=usb_interface\nDRIVER=ftdi_sio\nPRODUCT=403/6001/600\nTYPE=0/0/0\nINTERFACE=255/255/255\nMODALIAS=usb:v0403p6001d0600dc00dsc00dp00icFFiscFFipFFin00')]


Interface
---------

::

    >>> from usbid import Interface
    >>> Interface(parent=None, fs_path='inexistent')
    Traceback (most recent call last):
      ...
    ValueError: Invalid path given

    >>> port = usb['3']['2']['1']
    >>> port.interfaces
    [<usbid.fs.Interface [3-2.1:1.0] at ...>]

    >>> interface = port.interfaces[0]
    >>> interface.parent
    <usbid.fs.Port [3-2.1] at ...>

    >>> interface.fs_name
    '3-2.1:1.0'

    >>> interface.manufacturer
    'FTDI'

    >>> interface.product
    'FT232R USB UART'

    >>> interface = usb.get_interface(interface.fs_name)
    >>> interface
    <usbid.fs.Interface [3-2.1:1.0] at ...>

    >>> interface.parent
    <usbid.fs.Port [3-2.1] at ...>

    >>> interface.manufacturer
    'FTDI'

    >>> interface.product
    'FT232R USB UART'


Test data tree 1
----------------

::

    >>> usb.printtree()
    <usbid.fs.USB [/.../1/sys/bus/usb/devices] at ...>
      <usbid.fs.Bus [usb1] at ...>
          - Linux 3.13.0-48-generic ehci_hcd
          - EHCI Host Controller
        <usbid.fs.Interface [1-0:1.0] at ...>
        <usbid.fs.Port [1-1] at ...>
          <usbid.fs.Interface [1-1:1.0] at ...>
          <usbid.fs.Port [1-1.2] at ...>
              - USB Optical Mouse
            <usbid.fs.Interface [1-1.2:1.0] at ...>
          <usbid.fs.Port [1-1.3] at ...>
              - Auth
              - Biometric Coprocessor
            <usbid.fs.Interface [1-1.3:1.0] at ...>
          <usbid.fs.Port [1-1.4] at ...>
              - Broadcom Corp
              - BCM20702A0
            <usbid.fs.Interface [1-1.4:1.0] at ...>
            <usbid.fs.Interface [1-1.4:1.1] at ...>
            <usbid.fs.Interface [1-1.4:1.2] at ...>
            <usbid.fs.Interface [1-1.4:1.3] at ...>
          <usbid.fs.Port [1-1.6] at ...>
              - SunplusIT INC.
              - Integrated Camera
            <usbid.fs.Interface [1-1.6:1.0] at ...>
            <usbid.fs.Interface [1-1.6:1.1] at ...>
      <usbid.fs.Bus [usb2] at ...>
          - Linux 3.13.0-48-generic ehci_hcd
          - EHCI Host Controller
        <usbid.fs.Interface [2-0:1.0] at ...>
        <usbid.fs.Port [2-1] at ...>
          <usbid.fs.Interface [2-1:1.0] at ...>
      <usbid.fs.Bus [usb3] at ...>
          - Linux 3.13.0-48-generic xhci_hcd
          - xHCI Host Controller
        <usbid.fs.Interface [3-0:1.0] at ...>
        <usbid.fs.Port [3-2] at ...>
          <usbid.fs.Interface [3-2:1.0] at ...>
          <usbid.fs.Port [3-2.1] at ...>
              - FTDI
              - FT232R USB UART
            <usbid.fs.Interface [3-2.1:1.0] at ...>
              - ttyUSB0
          <usbid.fs.Port [3-2.2] at ...>
              - FTDI
              - FT232R USB UART
            <usbid.fs.Interface [3-2.2:1.0] at ...>
              - ttyUSB1
          <usbid.fs.Port [3-2.3] at ...>
              - FTDI
              - FT232R USB UART
            <usbid.fs.Interface [3-2.3:1.0] at ...>
              - ttyUSB2
          <usbid.fs.Port [3-2.4] at ...>
              - FTDI
              - FT232R USB UART
            <usbid.fs.Interface [3-2.4:1.0] at ...>
              - ttyUSB3
        <usbid.fs.Port [3-4] at ...>
            - Lenovo
            - H5321 gw
          <usbid.fs.Interface [3-4:1.0] at ...>
          <usbid.fs.Interface [3-4:1.1] at ...>
            - ttyACM0
          <usbid.fs.Interface [3-4:1.2] at ...>
          <usbid.fs.Interface [3-4:1.3] at ...>
            - ttyACM1
          <usbid.fs.Interface [3-4:1.4] at ...>
          <usbid.fs.Interface [3-4:1.5] at ...>
          <usbid.fs.Interface [3-4:1.6] at ...>
          <usbid.fs.Interface [3-4:1.7] at ...>
          <usbid.fs.Interface [3-4:1.8] at ...>
          <usbid.fs.Interface [3-4:1.9] at ...>
            - ttyACM2
      <usbid.fs.Bus [usb4] at ...>
          - Linux 3.13.0-48-generic xhci_hcd
          - xHCI Host Controller
        <usbid.fs.Interface [4-0:1.0] at ...>

    >>> sorted(usb.aggregated_interfaces(), key=lambda x: x.fs_path)
    [<usbid.fs.Interface [1-0:1.0] at ...>,
    <usbid.fs.Interface [1-1.2:1.0] at ...>,
    <usbid.fs.Interface [1-1.3:1.0] at ...>,
    <usbid.fs.Interface [1-1.4:1.0] at ...>,
    <usbid.fs.Interface [1-1.4:1.1] at ...>,
    <usbid.fs.Interface [1-1.4:1.2] at ...>,
    <usbid.fs.Interface [1-1.4:1.3] at ...>,
    <usbid.fs.Interface [1-1.6:1.0] at ...>,
    <usbid.fs.Interface [1-1.6:1.1] at ...>,
    <usbid.fs.Interface [1-1:1.0] at ...>,
    <usbid.fs.Interface [2-0:1.0] at ...>,
    <usbid.fs.Interface [2-1:1.0] at ...>,
    <usbid.fs.Interface [3-0:1.0] at ...>,
    <usbid.fs.Interface [3-2.1:1.0] at ...>,
    <usbid.fs.Interface [3-2.2:1.0] at ...>,
    <usbid.fs.Interface [3-2.3:1.0] at ...>,
    <usbid.fs.Interface [3-2.4:1.0] at ...>,
    <usbid.fs.Interface [3-2:1.0] at ...>,
    <usbid.fs.Interface [3-4:1.0] at ...>,
    <usbid.fs.Interface [3-4:1.1] at ...>,
    <usbid.fs.Interface [3-4:1.2] at ...>,
    <usbid.fs.Interface [3-4:1.3] at ...>,
    <usbid.fs.Interface [3-4:1.4] at ...>,
    <usbid.fs.Interface [3-4:1.5] at ...>,
    <usbid.fs.Interface [3-4:1.6] at ...>,
    <usbid.fs.Interface [3-4:1.7] at ...>,
    <usbid.fs.Interface [3-4:1.8] at ...>,
    <usbid.fs.Interface [3-4:1.9] at ...>,
    <usbid.fs.Interface [4-0:1.0] at ...>]

    >>> tty_ifaces = sorted(
    ...     usb.aggregated_interfaces(tty=True),
    ...     key=lambda x: x.fs_path
    ... )
    >>> ['{0} - {1}'.format(iface.fs_path, iface.tty) for iface in tty_ifaces]
    ['/.../1/sys/bus/usb/devices/usb3/3-2/3-2.1/3-2.1:1.0 - ttyUSB0',
    '/.../1/sys/bus/usb/devices/usb3/3-2/3-2.2/3-2.2:1.0 - ttyUSB1',
    '/.../1/sys/bus/usb/devices/usb3/3-2/3-2.3/3-2.3:1.0 - ttyUSB2',
    '/.../1/sys/bus/usb/devices/usb3/3-2/3-2.4/3-2.4:1.0 - ttyUSB3',
    '/.../1/sys/bus/usb/devices/usb3/3-4/3-4:1.1 - ttyACM0',
    '/.../1/sys/bus/usb/devices/usb3/3-4/3-4:1.3 - ttyACM1',
    '/.../1/sys/bus/usb/devices/usb3/3-4/3-4:1.9 - ttyACM2']


Test data tree 2
----------------

::

    >>> test_data_2_dir = os.path.join(
    ...     self.tempdir, '2', 'sys', 'bus', 'usb', 'devices')

    >>> usb = USB(fs_path=test_data_2_dir)
    >>> usb.printtree()
    <usbid.fs.USB [/.../2/sys/bus/usb/devices] at ...>
      ...
      <usbid.fs.Bus [usb3] at ...>
          - Linux 3.13.0-48-generic xhci_hcd
          - xHCI Host Controller
        <usbid.fs.Interface [3-0:1.0] at ...>
        <usbid.fs.Port [3-2] at ...>
            - FTDI
            - USB <-> Serial Cable
          <usbid.fs.Interface [3-2:1.0] at ...>
            - ttyUSB0
          <usbid.fs.Interface [3-2:1.1] at ...>
            - ttyUSB1
      ...

    >>> tty_ifaces = sorted(
    ...     usb.aggregated_interfaces(tty=True),
    ...     key=lambda x: x.fs_path
    ... )
    >>> ['{0} - {1}'.format(iface.fs_path, iface.tty) for iface in tty_ifaces]
    ['.../2/sys/bus/usb/devices/usb3/3-2/3-2:1.0 - ttyUSB0',
    '/.../2/sys/bus/usb/devices/usb3/3-2/3-2:1.1 - ttyUSB1',
    '/.../2/sys/bus/usb/devices/usb3/3-4/3-4:1.1 - ttyACM0',
    '/.../2/sys/bus/usb/devices/usb3/3-4/3-4:1.3 - ttyACM1',
    '/.../2/sys/bus/usb/devices/usb3/3-4/3-4:1.9 - ttyACM2']


Test data tree 3
----------------

::

    >>> test_data_3_dir = os.path.join(
    ...     self.tempdir, '3', 'sys', 'bus', 'usb', 'devices')

    >>> usb = USB(fs_path=test_data_3_dir)
    >>> usb.printtree()
    <usbid.fs.USB [/.../3/sys/bus/usb/devices] at ...>
      <usbid.fs.Bus [usb3] at ...>
          - Linux 3.13.0-48-generic xhci_hcd
          - xHCI Host Controller
        <usbid.fs.Interface [3-0:1.0] at ...>
        <usbid.fs.Port [3-2] at ...>
          <usbid.fs.Interface [3-2:1.0] at ...>
          <usbid.fs.Port [3-2.2] at ...>
              - DMX4ALL
              - NanoDMX Interface
            <usbid.fs.Interface [3-2.2:1.0] at ...>
              - ttyACM3
            <usbid.fs.Interface [3-2.2:1.1] at ...>
          <usbid.fs.Port [3-2.4] at ...>
              - Prolific Technology Inc.
              - USB-Serial Controller D
            <usbid.fs.Interface [3-2.4:1.0] at ...>
              - ttyUSB0
          <usbid.fs.Port [3-2.6] at ...>
            <usbid.fs.Interface [3-2.6:1.0] at ...>
            <usbid.fs.Port [3-2.6.1] at ...>
                - FTDI
                - FT232R USB UART
              <usbid.fs.Interface [3-2.6.1:1.0] at ...>
                - ttyUSB3
            <usbid.fs.Port [3-2.6.2] at ...>
                - FTDI
                - FT232R USB UART
              <usbid.fs.Interface [3-2.6.2:1.0] at ...>
                - ttyUSB4
            <usbid.fs.Port [3-2.6.3] at ...>
                - FTDI
                - FT232R USB UART
              <usbid.fs.Interface [3-2.6.3:1.0] at ...>
                - ttyUSB5
            <usbid.fs.Port [3-2.6.4] at ...>
                - FTDI
                - FT232R USB UART
              <usbid.fs.Interface [3-2.6.4:1.0] at ...>
                - ttyUSB6
          <usbid.fs.Port [3-2.7] at ...>
              - FTDI
              - USB <-> Serial Cable
            <usbid.fs.Interface [3-2.7:1.0] at ...>
              - ttyUSB1
            <usbid.fs.Interface [3-2.7:1.1] at ...>
              - ttyUSB2
      ...

    >>> tty_ifaces = sorted(
    ...     usb.aggregated_interfaces(tty=True),
    ...     key=lambda x: x.fs_path
    ... )
    >>> ['{0} - {1}'.format(iface.fs_path, iface.tty) for iface in tty_ifaces]
    ['/.../3/sys/bus/usb/devices/usb3/3-2/3-2.2/3-2.2:1.0 - ttyACM3',
    '/.../3/sys/bus/usb/devices/usb3/3-2/3-2.4/3-2.4:1.0 - ttyUSB0',
    '/.../3/sys/bus/usb/devices/usb3/3-2/3-2.6/3-2.6.1/3-2.6.1:1.0 - ttyUSB3',
    '/.../3/sys/bus/usb/devices/usb3/3-2/3-2.6/3-2.6.2/3-2.6.2:1.0 - ttyUSB4',
    '/.../3/sys/bus/usb/devices/usb3/3-2/3-2.6/3-2.6.3/3-2.6.3:1.0 - ttyUSB5',
    '/.../3/sys/bus/usb/devices/usb3/3-2/3-2.6/3-2.6.4/3-2.6.4:1.0 - ttyUSB6',
    '/.../3/sys/bus/usb/devices/usb3/3-2/3-2.7/3-2.7:1.0 - ttyUSB1',
    '/.../3/sys/bus/usb/devices/usb3/3-2/3-2.7/3-2.7:1.1 - ttyUSB2',
    '/.../3/sys/bus/usb/devices/usb3/3-4/3-4:1.1 - ttyACM0',
    '/.../3/sys/bus/usb/devices/usb3/3-4/3-4:1.3 - ttyACM1',
    '/.../3/sys/bus/usb/devices/usb3/3-4/3-4:1.9 - ttyACM2']

"""

if __name__ == '__main__':
    from usbid import tests

    suite = unittest.TestSuite()
    suite.addTest(unittest.findTestCases(tests))
    runner = unittest.TextTestRunner(failfast=True)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())
