prepare
=======

imports
-------

::
    >>> import os
    >>> from usbid.usbinfo import USBINFO
    >>> from usbid.device import DeviceNode
    >>> from usbid.device import usb_roots
    >>> from usbid.device import traverse
    
setup
-----
 
::
    >>> USBINFO._parse_usbids()
    >>> roots = usb_roots(MOCK_SYS)  

 
get info
========

get the root nodes

::

    >>> pprint(roots)
    {2: <usbid.device.DeviceNode object at 0x...>,
     3: <usbid.device.DeviceNode object at 0x...>, 
     4: <usbid.device.DeviceNode object at 0x...>}
 
     
    >>> roots[2].print_info()
    ********************************************************************************
        idProduct: 0002
        idVendor: 1d6b
        Product Name: 2.0 root hub
        Vendor Name: Linux Foundation
 
 
 set a device root
 
 ::   
    >>> #'/tmp/tmp27WLl9/sys/bus/usb/devices/usb2    
    >>> root_dev = DeviceNode(os.path.join(MOCK_SYS, "usb2"), roots[2], is_root=True)
    >>> root_dev.keys()
    [1]
    >>> root_dev.values()
    [<usbid.device.DeviceNode object at 0x...>]
    
    >>> root_dev.items()
    {1: <usbid.device.DeviceNode object at 0x...>}
    
    >>> root_dev[1]
    <usbid.device.DeviceNode object at 0x...>
    

    >>> #dev1.path '/tmp/tmp27WLl9/sys/bus/usb/devices/usb2/2-1
    >>> dev1 = DeviceNode(os.path.join(root_dev.path,root_dev[1].path), root_dev)   
    >>> #erg soll '2-1.6', '2-1.5', '2-1.2', und des auslassn'2-1:1.0',
    >>> dev1.keys()
    [6, 5, 2]
    
    >>> pprint(dev1.values())
    [<usbid.device.DeviceNode object at 0x...>, 
     <usbid.device.DeviceNode object at 0x...>, 
     <usbid.device.DeviceNode object at 0x...>]
    
    >>> pprint(dev1.items())
    {2: <usbid.device.DeviceNode object at 0x...>, 
     5: <usbid.device.DeviceNode object at 0x...>, 
     6: <usbid.device.DeviceNode object at 0x...>}
     
    >>> dev1[6]   
    <usbid.device.DeviceNode object at 0x...>
    
    
    >>> dev2 = DeviceNode(os.path.join(dev1.path,dev1[2].path), dev1)
    >>> #dev2.path '/tmp/tmpUCRk4t/sys/bus/usb/devices/usb2/2-1/2-1.2'
    >>> dev2.keys()
    [1, 6]
    
    >>> pprint(dev2.values())
    [<usbid.device.DeviceNode object at 0x...>,
     <usbid.device.DeviceNode object at 0x...>]
    
    >>> pprint(dev2.items())
    {1: <usbid.device.DeviceNode object at 0x...>,
     6: <usbid.device.DeviceNode object at 0x...>}   
      
    >>> dev2[1]
    <usbid.device.DeviceNode object at 0x...>
       
    >>> dev3 = DeviceNode(os.path.join(dev2.path, dev2[1].path), dev2)
    >>> #dev3.path '/tmp/tmpUCRk4t/sys/bus/usb/devices/usb2/2-1/2-1.2/2-1.2.1'
 
    
    >>> # de 3 sein empty weil enddevice. iwas no basteln???
    >>> #dev3.keys()
    >>> #dev3.values()    
    >>> #dev3.items()
    
    >>> dev3.print_info()
    ********************************************************************************
       idProduct: 2303
       idVendor: 067b
       Product Name: PL2303 Serial Port
       Vendor Name: Prolific Technology, Inc.   
       



    >>> #dev3.device_by_path()
    >>> #'/tmp/tmpRRJ3vN/sys/bus/usb/devices/usb2/2-1/2-1.2/2-1.2.1/2-1.2.1:1.0/ttyUSB0'

       
    >>> interact(locals())    
           


os.listdir(roots[2].path)
root = '/tmp/tmp27WLl9/sys/bus/usb/devices/usb2


1 vewrzweigung
os.listdir('/tmp/tmp27WLl9/sys/bus/usb/devices/usb2/2-1')



darunter liegende =

 '2-1.5',
 '2-1.6',
 '2-1.2',
 '2-1:1.0',


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










