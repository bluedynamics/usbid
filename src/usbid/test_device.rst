
prepare
=======

imports
-------

::

    >>> from usbid.test_device import TestDevice
 
 
set up test keyboard
--------------------
::   


    >>> keyboard = TestDevice()


get values
----------
::
    access the values with keyboard.foo just like a real device object

    idProduct
    idVendor
    port_number
    address
    bus
    iManufacturer
    iProduct
    iSerialNumber
    bDescriptorType
    bDeviceClass
    bDeviceProtocol
    bDeviceSubClass
    bLength
    bMaxPacketSize0
    bNumConfigurations
    bcdDevice
  
    >>> #interact(locals()) 
    
