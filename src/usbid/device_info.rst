prepare
=======

imports
-------

::
    >>> from usbid.usbinfo import USBINFO
    >>> from usbid.test_device import TestDevice
    >>> from usbid.device_info import DeviceInfo
 
    >>> #interact(locals()) 
 
    
setup
-----
 
::
   
    >>> device = TestDevice()
    >>> dev_info_obj = DeviceInfo(device)
    
    
get info
========

should a device object dont have proper attributes it will be pre catched in the 
get_devices module

::

    >>> USBINFO._parse_usbids()

    >>> dev_info_obj.print_info()
    ********************************************************************************
        idProduct: 0xc318
        Product Name: Illuminated Keyboard
        idVendor: 0x46d
        Vendor Name: Logitech, Inc.
        port_number: 2
        address: 14
        bus: 3
        iManufacturer: 1
        iProduct: 2
        iSerialNumber: 0

