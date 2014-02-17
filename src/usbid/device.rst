prepare
=======

imports::

    >>> import os
    >>> from usbid.usbinfo import USBINFO
    >>> from usbid.device import DeviceNode
    >>> from usbid.device import usb_roots
    >>> from usbid.device import devicelist

setup::

    >>> USBINFO._parse_usbids()
    >>> roots = usb_roots(MOCK_SYS)

get the root nodes::

    >>> pprint(roots)
    {2: <usbid.device.DeviceNode object at 0x...>,
     3: <usbid.device.DeviceNode object at 0x...>, 
     4: <usbid.device.DeviceNode object at 0x...>}

print info for root2::

    >>> print roots[2]
    idProduct: 0002
    idVendor: 1d6b
    Product Name: 2.0 root hub
    Vendor Name: Linux Foundation 

set a device root by hand for the test. fs location is
``/tmp/tmp27WLl9/sys/bus/usb/devices/usb2``::

    >>> root_dev = DeviceNode(
    ...     2, os.path.join(MOCK_SYS, "usb2"), None)

lookup the methods for root::

    >>> root_dev.keys()
    [1]
    >>> root_dev.values()
    [<usbid.device.DeviceNode object at 0x...>]

    >>> root_dev.items()
    [(1, <usbid.device.DeviceNode object at 0x...>)]

    >>> root_dev[1]
    <usbid.device.DeviceNode object at 0x...>

    >>> root_dev.path
    [2]


first node
----------

setup first node. just for info: dev1.fs_path
``'/tmp/tmp27WLl9/sys/bus/usb/devices/usb2/2-1``::    

    >>> dev1 = DeviceNode(1, os.path.join(root_dev.fs_path, "2-1"), root_dev)  
 
lookup the methods for first node. The results should be '2-1.6', '2-1.5',
'2-1.2', and leave out this'2-1:1.0'::

    >>> sorted(dev1.keys())
    [2, 5, 6]

    >>> pprint(dev1.values())
    [<usbid.device.DeviceNode object at 0x...>, 
     <usbid.device.DeviceNode object at 0x...>, 
     <usbid.device.DeviceNode object at 0x...>]

    >>> pprint(sorted(dev1.items()))
    [(2, <usbid.device.DeviceNode object at 0x...>),
     (5, <usbid.device.DeviceNode object at 0x...>),
     (6, <usbid.device.DeviceNode object at 0x...>)]

    >>> dev1[6]
    <usbid.device.DeviceNode object at 0x...>

    >>> dev1.path
    [2, 1]

Check for non existent::

    >>> dev1[9]
    Traceback (most recent call last):
    ...
    KeyError: 'No such Device with 9 with in path 2/1'


second node
-----------

setup second node. Just for info: dev2.fs_path
``'/tmp/tmpUCRk4t/sys/bus/usb/devices/usb2/2-1/2-1.2'``::

    >>> dev2 = DeviceNode(2, os.path.join(dev1.fs_path,"2-1.2"), dev1)

    >>> sorted(dev2.keys())
    [1, 6]

lookup the methods for second node::

    >>> pprint(dev2.values())
    [<usbid.device.DeviceNode object at 0x...>,
     <usbid.device.DeviceNode object at 0x...>]

    >>> pprint(sorted(dev2.items()))
    [(1, <usbid.device.DeviceNode object at 0x...>),
     (6, <usbid.device.DeviceNode object at 0x...>)]

    >>> dev2[1]
    <usbid.device.DeviceNode object at 0x...>

    >>> dev2.path
    [2, 1, 2]


end node
--------

setup end node. Just for info: dev3.fs_path
``'/tmp/tmpUCRk4t/sys/bus/usb/devices/usb2/2-1/2-1.2/2-1.2.1'``::

    >>> dev3 = DeviceNode(1, os.path.join(dev2.fs_path, "2-1.2.1"), dev2)

 
lookup the methods for end node. The next 3 ones should evaluate to false,
because there are no more children::

    >>> bool(dev3.keys())
    False

    >>> bool(dev3.values())
    False

    >>> bool(dev3.items())
    False

check path for end device::
 
    >>> dev3.path
    [2, 1, 2, 1]

print end device info::

    >>> print dev3
    idProduct: 2303
    idVendor: 067b
    Product Name: PL2303 Serial Port
    Vendor Name: Prolific Technology, Inc.


devicelist
----------

get all usbdevices::

    >>> len(devicelist(MOCK_SYS))
    13

check ttys. Here we iterate over the the devicelist and only show the ones that
are ttys::

    >>> ttys = [_ for _ in devicelist(MOCK_SYS) if _.tty]

two connected tty should be found::

    >>> len(ttys)
    2

print info for the first tty::

    >>> print ttys[0]
    idProduct: 2303
    idVendor: 067b
    Product Name: PL2303 Serial Port
    Vendor Name: Prolific Technology, Inc.

read node path::

    >>> ttys[0].path
    [2, 1, 2, ...]

get filesystem path for the tty::

    >>> ttys[0].fs_path
    '/tmp/...sys/bus/usb/devices/usb2/2-1/2-1.2/2-...'
