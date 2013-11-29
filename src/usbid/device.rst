prepare
=======

imports
-------

::
    >>> import os
    >>> from usbid.usbinfo import USBINFO
    >>> from usbid.device import DeviceNode
    >>> from usbid.device import usb_roots

    
setup
-----
 
::
    >>> USBINFO._parse_usbids()
    

 
get info
========

::

    >>> pprint(usb_roots(MOCK_SYS))
    {2: <usbid.device.DeviceNode object at 0x...>,
     3: <usbid.device.DeviceNode object at 0x...>, 
     4: <usbid.device.DeviceNode object at 0x...>}
     
    >>> usb_roots(MOCK_SYS)[2].print_info()
    ********************************************************************************
        idProduct: 0002
        idVendor: 1d6b
        Product Name: 2.0 root hub
        Vendor Name: Linux Foundation
    
    >>> roots = usb_roots(MOCK_SYS)
    >>> dev = DeviceNode(os.path.join(MOCK_SYS, "usb3"), roots[3], is_root=True)
    >>> interact(locals())       



In [12]: os.listdir(MOCK_SYS)
Out[12]: 
['2-1.6',
 '3-2.2.1:1.0',
 '2-0:1.0',
 '3-2.4:1.0',
 '2-1.5',
 '1-1:1.0',
 'usb4',
 '3-2.4',
 '2-1:1.0',
 '2-1.2:1.1',
 '3-2.2.6',
 '3-0:1.0',
 '2-1.2',
 '2-1',
 '2-1.6:1.0',
 '3-2.2.1',
 '3-2',
 '3-2.2.4:1.0',
 '2-1.2:1.2',
 '1-1',
 '3-2.2.6:1.0',
 '3-2.2.4',
 '3-2.2.4:1.1',
 '3-2.2:1.0',
 '3-2.2',
 '2-1.5:1.0',
 '2-1.2:1.3',
 '1-0:1.0',
 '3-2:1.0',
 '2-1.6:1.1',
 '2-1.2:1.0',
 '4-0:1.0',
 'usb3']
 
 os.listdir(MOCK_SYS + "/usb3/")
 nur di attrs drauf koane children











