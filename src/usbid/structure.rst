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

    >>> test_file_attributes.no_attribute
    Traceback (most recent call last):
      ...
    AttributeError: 'TestFileAttributes' object has no attribute 'no_attribute'

    >>> def get_file_attribues(obj):
    ...    ret = []
    ...    for attr_name in obj.__file_attributes__:
    ...        ret.append((attr_name, getattr(obj, attr_name)))
    ...    return ret

    >>> get_file_attribues(test_file_attributes)
    [('file_attribute', 'File attribute value')]

    >>> import shutil
    >>> shutil.rmtree(tempdir)

USB::

    >>> from usbid.structure import USB
    >>> usb = USB()
    >>> usb
    <usbid.structure.USB object at ...>

    >>> usb.fs_path
    '/sys/bus/usb/devices'

    >>> usb.fs_name
    'devices'

    >>> usb.fs_parent
    '/sys/bus/usb'

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

    >>> get_file_attribues(bus)
    [('authorized', '1'), 
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
    ('urbnum', '833'), 
    ('version', '2.00')]

    >>> bus.interfaces
    [<usbid.structure.Interface object at ...>]

    >>> interface = bus.interfaces[0]
    >>> get_file_attribues(interface)
    [('bAlternateSetting', '0'), 
    ('bInterfaceClass', '09'), 
    ('bInterfaceNumber', '00'), 
    ('bInterfaceProtocol', '00'), 
    ('bInterfaceSubClass', '00'), 
    ('bNumEndpoints', '01'), 
    ('interface', None), 
    ('modalias', 'usb:v1D6Bp0002d0313dc09dsc00dp01ic09isc00ip00in00'), 
    ('supports_autosuspend', '1'), 
    ('uevent', 'DEVTYPE=usb_interface\nDRIVER=hub\nPRODUCT=1d6b/2/313\nTYPE=9/0/1\nINTERFACE=9/0/0\nMODALIAS=usb:v1D6Bp0002d0313dc09dsc00dp01ic09isc00ip00in00')]

Port::

    >>> port = bus['2']
    >>> port
    <usbid.structure.Port object at ...>

    >>> port.fs_path
    '/sys/bus/usb/devices/usb3/3-2'

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
    ('dev', '189:372'), 
    ('devnum', '117'), 
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
    ('uevent', 'MAJOR=189\nMINOR=372\nDEVNAME=bus/usb/003/117\nDEVTYPE=usb_device\nDRIVER=usb\nPRODUCT=409/5a/100\nTYPE=9/0/1\nBUSNUM=003\nDEVNUM=117'), 
    ('urbnum', '47'), 
    ('version', '2.00')]

    >>> port.interfaces
    [<usbid.structure.Interface object at ...>]

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

    >>> port.keys()
    ['1', '2', '3', '4']

    >>> port['0']
    Traceback (most recent call last):
      ...
    KeyError: '0'

    >>> sub_port = port['1']
    >>> sub_port
    <usbid.structure.Port object at ...>

    >>> sub_port.fs_path
    '/sys/bus/usb/devices/usb3/3-2/3-2.1'

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
    ('dev', '189:373'), 
    ('devnum', '118'), 
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
    ('uevent', 'MAJOR=189\nMINOR=373\nDEVNAME=bus/usb/003/118\nDEVTYPE=usb_device\nDRIVER=usb\nPRODUCT=403/6001/600\nTYPE=0/0/0\nBUSNUM=003\nDEVNUM=118'), 
    ('urbnum', '15'), 
    ('version', '2.00')]

    >>> sub_port.interfaces
    [<usbid.structure.Interface object at ...>]

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
