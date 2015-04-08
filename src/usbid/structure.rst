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

    >>> test_data_1_dir = os.path.join(
    ...     TEMPDIR, 'test_1', 'sys', 'bus', 'usb', 'devices')

    >>> usb = USB(fs_path=test_data_1_dir)
    >>> usb
    <usbid.structure.USB [/.../test_1/sys/bus/usb/devices] at ...>

    >>> usb.fs_path
    '.../test_1/sys/bus/usb/devices'

    >>> usb.fs_name
    'devices'

    >>> usb.fs_parent
    '.../test_1/sys/bus/usb'

    >>> sorted(usb.keys())
    ['1', '2', '3', '4']

    >>> usb['0']
    Traceback (most recent call last):
      ...
    KeyError: '0'

    >>> usb['1']
    <usbid.structure.Bus [usb1] at ...>

    >>> sorted(usb.values(), key=lambda x: x.fs_name)
    [<usbid.structure.Bus [usb1] at ...>, 
    <usbid.structure.Bus [usb2] at ...>, 
    <usbid.structure.Bus [usb3] at ...>, 
    <usbid.structure.Bus [usb4] at ...>]

    >>> sorted(usb.items())
    [('1', <usbid.structure.Bus [usb1] at ...>), 
    ('2', <usbid.structure.Bus [usb2] at ...>), 
    ('3', <usbid.structure.Bus [usb3] at ...>), 
    ('4', <usbid.structure.Bus [usb4] at ...>)]

    >>> MARKER = object()
    >>> usb.get('0', default=MARKER) is MARKER
    True

    >>> usb.get('1', default=MARKER) is MARKER
    False

Bus::

    >>> bus = usb['3']
    >>> bus
    <usbid.structure.Bus [usb3] at ...>

    >>> bus.name
    '3'

    >>> bus.keys()
    ['2', '4']

    >>> bus['1']
    Traceback (most recent call last):
      ...
    KeyError: '1'

    >>> bus['2']
    <usbid.structure.Port [3-2] at ...>

    >>> bus.values()
    [<usbid.structure.Port [3-2] at ...>, 
    <usbid.structure.Port [3-4] at ...>]

    >>> bus.items()
    [('2', <usbid.structure.Port [3-2] at ...>), 
    ('4', <usbid.structure.Port [3-4] at ...>)]

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
    ('urbnum', '884'), 
    ('version', '2.00')]

    >>> bus.interfaces
    [<usbid.structure.Interface [3-0:1.0] at ...>]

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
    <usbid.structure.Port [3-2] at ...>

    >>> port.fs_path
    '.../test_1/sys/bus/usb/devices/usb3/3-2'

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
    [<usbid.structure.Interface [3-2:1.0] at ...>]

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
    <usbid.structure.Port [3-2.1] at ...>

    >>> sub_port.fs_path
    '.../test_1/sys/bus/usb/devices/usb3/3-2/3-2.1'

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
    [<usbid.structure.Interface [3-2.1:1.0] at ...>]

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

USB Tree::

    >>> usb.printtree()
    <usbid.structure.USB [/.../test_1/sys/bus/usb/devices] at ...>
      <usbid.structure.Bus [usb1] at ...>
          - Linux 3.13.0-48-generic ehci_hcd
          - EHCI Host Controller
        <usbid.structure.Interface [1-0:1.0] at ...>
        <usbid.structure.Port [1-1] at ...>
          <usbid.structure.Interface [1-1:1.0] at ...>
          <usbid.structure.Port [1-1.2] at ...>
              - USB Optical Mouse
            <usbid.structure.Interface [1-1.2:1.0] at ...>
          <usbid.structure.Port [1-1.3] at ...>
              - Auth
              - Biometric Coprocessor
            <usbid.structure.Interface [1-1.3:1.0] at ...>
          <usbid.structure.Port [1-1.4] at ...>
              - Broadcom Corp
              - BCM20702A0
            <usbid.structure.Interface [1-1.4:1.0] at ...>
            <usbid.structure.Interface [1-1.4:1.1] at ...>
            <usbid.structure.Interface [1-1.4:1.2] at ...>
            <usbid.structure.Interface [1-1.4:1.3] at ...>
          <usbid.structure.Port [1-1.6] at ...>
              - SunplusIT INC.
              - Integrated Camera
            <usbid.structure.Interface [1-1.6:1.0] at ...>
            <usbid.structure.Interface [1-1.6:1.1] at ...>
      <usbid.structure.Bus [usb2] at ...>
          - Linux 3.13.0-48-generic ehci_hcd
          - EHCI Host Controller
        <usbid.structure.Interface [2-0:1.0] at ...>
        <usbid.structure.Port [2-1] at ...>
          <usbid.structure.Interface [2-1:1.0] at ...>
      <usbid.structure.Bus [usb3] at ...>
          - Linux 3.13.0-48-generic xhci_hcd
          - xHCI Host Controller
        <usbid.structure.Interface [3-0:1.0] at ...>
        <usbid.structure.Port [3-2] at ...>
          <usbid.structure.Interface [3-2:1.0] at ...>
          <usbid.structure.Port [3-2.1] at ...>
              - FTDI
              - FT232R USB UART
            <usbid.structure.Interface [3-2.1:1.0] at ...>
              - ttyUSB0
          <usbid.structure.Port [3-2.2] at ...>
              - FTDI
              - FT232R USB UART
            <usbid.structure.Interface [3-2.2:1.0] at ...>
              - ttyUSB1
          <usbid.structure.Port [3-2.3] at ...>
              - FTDI
              - FT232R USB UART
            <usbid.structure.Interface [3-2.3:1.0] at ...>
              - ttyUSB2
          <usbid.structure.Port [3-2.4] at ...>
              - FTDI
              - FT232R USB UART
            <usbid.structure.Interface [3-2.4:1.0] at ...>
              - ttyUSB3
        <usbid.structure.Port [3-4] at ...>
            - Lenovo
            - H5321 gw
          <usbid.structure.Interface [3-4:1.0] at ...>
          <usbid.structure.Interface [3-4:1.1] at ...>
            - ttyACM0
          <usbid.structure.Interface [3-4:1.2] at ...>
          <usbid.structure.Interface [3-4:1.3] at ...>
            - ttyACM1
          <usbid.structure.Interface [3-4:1.4] at ...>
          <usbid.structure.Interface [3-4:1.5] at ...>
          <usbid.structure.Interface [3-4:1.6] at ...>
          <usbid.structure.Interface [3-4:1.7] at ...>
          <usbid.structure.Interface [3-4:1.8] at ...>
          <usbid.structure.Interface [3-4:1.9] at ...>
            - ttyACM2
      <usbid.structure.Bus [usb4] at ...>
          - Linux 3.13.0-48-generic xhci_hcd
          - xHCI Host Controller
        <usbid.structure.Interface [4-0:1.0] at ...>

    >>> sorted(usb.aggregated_interfaces(), key=lambda x: x.fs_path)
    [<usbid.structure.Interface [1-0:1.0] at ...>, 
    <usbid.structure.Interface [1-1.2:1.0] at ...>, 
    <usbid.structure.Interface [1-1.3:1.0] at ...>, 
    <usbid.structure.Interface [1-1.4:1.0] at ...>, 
    <usbid.structure.Interface [1-1.4:1.1] at ...>, 
    <usbid.structure.Interface [1-1.4:1.2] at ...>, 
    <usbid.structure.Interface [1-1.4:1.3] at ...>, 
    <usbid.structure.Interface [1-1.6:1.0] at ...>, 
    <usbid.structure.Interface [1-1.6:1.1] at ...>, 
    <usbid.structure.Interface [1-1:1.0] at ...>, 
    <usbid.structure.Interface [2-0:1.0] at ...>, 
    <usbid.structure.Interface [2-1:1.0] at ...>, 
    <usbid.structure.Interface [3-0:1.0] at ...>, 
    <usbid.structure.Interface [3-2.1:1.0] at ...>, 
    <usbid.structure.Interface [3-2.2:1.0] at ...>, 
    <usbid.structure.Interface [3-2.3:1.0] at ...>, 
    <usbid.structure.Interface [3-2.4:1.0] at ...>, 
    <usbid.structure.Interface [3-2:1.0] at ...>, 
    <usbid.structure.Interface [3-4:1.0] at ...>, 
    <usbid.structure.Interface [3-4:1.1] at ...>, 
    <usbid.structure.Interface [3-4:1.2] at ...>, 
    <usbid.structure.Interface [3-4:1.3] at ...>, 
    <usbid.structure.Interface [3-4:1.4] at ...>, 
    <usbid.structure.Interface [3-4:1.5] at ...>, 
    <usbid.structure.Interface [3-4:1.6] at ...>, 
    <usbid.structure.Interface [3-4:1.7] at ...>, 
    <usbid.structure.Interface [3-4:1.8] at ...>, 
    <usbid.structure.Interface [3-4:1.9] at ...>, 
    <usbid.structure.Interface [4-0:1.0] at ...>]

    >>> tty_ifaces = sorted(
    ...     usb.aggregated_interfaces(tty=True),
    ...     key=lambda x: x.fs_path
    ... )
    >>> ['{0} - {1}'.format(iface.fs_path, iface.tty) for iface in tty_ifaces]
    ['/.../test_1/sys/bus/usb/devices/usb3/3-2/3-2.1/3-2.1:1.0 - ttyUSB0', 
    '/.../test_1/sys/bus/usb/devices/usb3/3-2/3-2.2/3-2.2:1.0 - ttyUSB1', 
    '/.../test_1/sys/bus/usb/devices/usb3/3-2/3-2.3/3-2.3:1.0 - ttyUSB2', 
    '/.../test_1/sys/bus/usb/devices/usb3/3-2/3-2.4/3-2.4:1.0 - ttyUSB3', 
    '/.../test_1/sys/bus/usb/devices/usb3/3-4/3-4:1.1 - ttyACM0', 
    '/.../test_1/sys/bus/usb/devices/usb3/3-4/3-4:1.3 - ttyACM1', 
    '/.../test_1/sys/bus/usb/devices/usb3/3-4/3-4:1.9 - ttyACM2']
