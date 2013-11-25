prepare
=======

imports
-------

::

    >>> import usb.core
    >>> from usbid.usbinfo import USBINFO
    >>> from usbid.device_info import DeviceInfo      
    >>> from usbid.device_list import GetDevices

    >>> #interact(locals()) 

    
setup
-----
 
::

    >>> devices = GetDevices()
    >>> pprint(devices._get_connected_devices())
    [<usb.core.Device object at 0x...>,
     <usb.core.Device object at 0x...>,
     <usb.core.Device object at 0x...>,
     <usb.core.Device object at 0x...>]

    
get info
========

::

    >>> USBINFO._parse_usbids()
    >>> #interact(locals())
    >>> devices._get_infos()



    
    
    