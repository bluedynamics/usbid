Linux USB structure
===================

Container::

    >>> from usbid.structure import Container
    >>> container = Container()
    >>> container.keys()
    Traceback (most recent call last):
      ...
    NotImplementedError

    >>> container['key']
    Traceback (most recent call last):
      ...
    NotImplementedError

    >>> class TestContainer(Container):
    ...     def __iter__(self):
    ...         return iter(['1', '2'])
    ...     def __getitem__(self, key):
    ...         return key

    >>> test_container = TestContainer()
    >>> test_container.keys()
    ['1', '2']

    >>> test_container['1']
    '1'

FileAttributes::

    >>> import os
    >>> import tempfile
    >>> tempdir = tempfile.mkdtemp()
    >>> with open(os.path.join(tempdir, 'file_attribute'), 'wt') as file:
    ...     file.write('File attribute value')

    >>> from usbid.structure import FileAttributes

    >>> class TestFileAttributes(FileAttributes):
    ...     __file_attributes__ = ['file_attribute']
    ...     fs_path = tempdir
    ...     class_attribute = 'Class Attribute'

    >>> test_file_attributes = TestFileAttributes()
    >>> test_file_attributes.class_attribute
    'Class Attribute'

    >>> test_file_attributes.file_attribute
    'File attribute value'

    >>> import shutil
    >>> shutil.rmtree(tempdir)

USB::

    >>> from usbid.structure import USB
    >>> usb = USB()
    >>> usb
    <usbid.structure.USB object at ...>

    >>> usb.keys()
    ['1', '2', '3', '4']

    >>> usb['0']
    Traceback (most recent call last):
      ...
    KeyError: '0'

    >>> usb['1']
    <usbid.structure.Bus object at ...>

    >>> usb.values()
    [<usbid.structure.Bus object at ...>, 
    <usbid.structure.Bus object at ...>, 
    <usbid.structure.Bus object at ...>, 
    <usbid.structure.Bus object at ...>]

    >>> usb.items()
    [('1', <usbid.structure.Bus object at ...>), 
    ('2', <usbid.structure.Bus object at ...>), 
    ('3', <usbid.structure.Bus object at ...>), 
    ('4', <usbid.structure.Bus object at ...>)]

    >>> MARKER = object()
    >>> usb.get('0', default=MARKER) is MARKER
    True

    >>> usb.get('1', default=MARKER) is MARKER
    False

Bus::

    >>> bus = usb['3']
    >>> bus
    <usbid.structure.Bus object at ...>

    >>> bus.name
    '3'

    >>> bus.keys()
    ['2', '4']

    >>> bus['1']
    Traceback (most recent call last):
      ...
    KeyError: '1'

    >>> bus['2']
    <usbid.structure.Port object at ...>

    >>> bus.values()
    [<usbid.structure.Port object at ...>, 
    <usbid.structure.Port object at ...>]

    >>> bus.items()
    [('2', <usbid.structure.Port object at ...>), 
    ('4', <usbid.structure.Port object at ...>)]

    >>> interfaces = bus.interfaces
    >>> interfaces
    [<usbid.structure.Interface object at ...>]

    >>> bus.authorized
    '1'

    >>> bus.authorized_default
    '1'

    >>> bus.avoid_reset_quirk
    '0'

    >>> bus.bcdDevice
    '0313'

    >>> bus.bConfigurationValue
    '1'

    >>> bus.bDeviceClass
    '09'

    >>> bus.bDeviceProtocol
    '01'

    >>> bus.bDeviceSubClass
    '00'

    >>> bus.bmAttributes
    'e0'

    >>> bus.bMaxPacketSize0
    '64'

    >>> bus.bMaxPower
    '0mA'

    >>> bus.bNumConfigurations
    '1'

    >>> bus.bNumInterfaces
    '1'

    >>> bus.busnum
    '3'

    >>> bus.dev
    '189:256'

    >>> bus.devnum
    '1'

    >>> bus.devpath
    '0'

    >>> bus.idProduct
    '0002'

    >>> bus.idVendor
    '1d6b'

    >>> bus.ltm_capable
    'no'

    >>> bus.manufacturer
    'Linux 3.13.0-48-generic xhci_hcd'

    >>> bus.maxchild
    '4'

    >>> bus.product
    'xHCI Host Controller'

    >>> bus.quirks
    '0x0'

    >>> bus.removable
    'unknown'

    >>> bus.serial
    '0000:00:14.0'

    >>> bus.speed
    '480'

    >>> bus.uevent.split('\n')
    ['MAJOR=189', 
    'MINOR=256', 
    'DEVNAME=bus/usb/003/001', 
    'DEVTYPE=usb_device', 
    'DRIVER=usb', 
    'PRODUCT=1d6b/2/313', 
    'TYPE=9/0/1', 
    'BUSNUM=003', 
    'DEVNUM=001']

    >>> bus.urbnum
    '833'

    >>> bus.version
    '2.00'
