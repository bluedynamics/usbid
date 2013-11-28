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
     
    
    
    >>> #testpath = "/sys/bus/usb/devices/usb3/3-1/3-1.6/3-1.6"
    >>> #devicenode = DeviceNode(testpath)
    >>> #devicenode.idVendor
    


    >>> #interact(locals())
      
    >>> pprint(usb_roots(MOCK_SYS))
    {3: <usbid.device.DeviceNode object at 0x...>, 
     4: <usbid.device.DeviceNode object at 0x...>}
     
    >>> usb_roots()[3].print_info()
    ********************************************************************************
        idProduct: 0002
        idVendor: 1d6b
        Product Name: 2.0 root hub
        Vendor Name: Linux Foundation


    
    
get info
========

::

    

