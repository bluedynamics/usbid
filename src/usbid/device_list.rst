prepare
=======

imports
-------

::

    >>> from usbid.usbinfo import USBINFO
    >>> from usbid.device_info import DeviceInfo      
    >>> from usbid.device_list import GetDevices

    >>> #interact(locals()) 

    
setup
-----
 
::

    >>> devices = GetDevices()
    >>> pprint(devices.get_connected_devices())
    [<usb.core.Device object at 0x...>,
     <usb.core.Device object at 0x...>,
     <usb.core.Device object at 0x...>,
     <usb.core.Device object at 0x...>]

    
get info
========

::

    >>> USBINFO._parse_usbids()
    >>> #interact(locals())
    >>> devices.get_infos()


    ********************************************************************************
    ********************************************************************************
    Found 6 devices,(hubs are being ignored)
    ********************************************************************************
        idProduct: 0x1001
        Product Name: TCS5B Fingerprint sensor
        idVendor: 0x147e
        Vendor Name: Upek
        port_number: 5
        address: 3
        bus: 2
        iManufacturer: 1
        iProduct: 2
        iSerialNumber: 0
    ********************************************************************************
        idProduct: 0x308
        Product Name: UNKNOWN
        idVendor: 0x5986
        Vendor Name: Acer, Inc
        port_number: 6
        address: 4
        bus: 2
        iManufacturer: 1
        iProduct: 2
        iSerialNumber: 0
    ********************************************************************************
        idProduct: 0xc318
        Product Name: Illuminated Keyboard
        idVendor: 0x46d
        Vendor Name: Logitech, Inc.
        port_number: 2
        address: 5
        bus: 3
        iManufacturer: 1
        iProduct: 2
        iSerialNumber: 0
    ********************************************************************************
        idProduct: 0x7
        Product Name: DeathAdder Mouse
        idVendor: 0x1532
        Vendor Name: Razer USA, Ltd
        port_number: 4
        address: 7
        bus: 3
        iManufacturer: 1
        iProduct: 2
        iSerialNumber: 0
    ********************************************************************************
        idProduct: 0x2303
        Product Name: PL2303 Serial Port
        idVendor: 0x67b
        Vendor Name: Prolific Technology, Inc.
        port_number: 2
        address: 8
        bus: 3
        iManufacturer: 1
        iProduct: 2
        iSerialNumber: 0
    ********************************************************************************
        idProduct: 0x2303
        Product Name: PL2303 Serial Port
        idVendor: 0x67b
        Vendor Name: Prolific Technology, Inc.
        port_number: 5
        address: 9
        bus: 3
        iManufacturer: 1
        iProduct: 2
        iSerialNumber: 0

    
     
#mit lsusb:
Bus 002 Device 003: ID 147e:1001 Upek TCS5B Fingerprint sensor
Bus 002 Device 004: ID 5986:0308 Acer, Inc 
Bus 003 Device 005: ID 046d:c318 Logitech, Inc. Illuminated Keyboard
Bus 003 Device 007: ID 1532:0007 Razer USA, Ltd DeathAdder Mouse
Bus 003 Device 008: ID 067b:2303 Prolific Technology, Inc. PL2303 Serial Port
Bus 003 Device 009: ID 067b:2303 Prolific Technology, Inc. PL2303 Serial Port
       
    