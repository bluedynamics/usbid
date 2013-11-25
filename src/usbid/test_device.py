
"""
#attr for keyboard deviceobject 
 'address',
 'attach_kernel_driver',
 'bDescriptorType',
 'bDeviceClass',
 'bDeviceProtocol',
 'bDeviceSubClass',
 'bLength',
 'bMaxPacketSize0',
 'bNumConfigurations',
 'bcdDevice',
 'bcdUSB',
 'bus',
 'ctrl_transfer',
 'default_timeout',
 'detach_kernel_driver',
 'get_active_configuration',
 'iManufacturer',
 'iProduct',
 'iSerialNumber',
 'idProduct',
 'idVendor',
 'is_kernel_driver_active',
 'port_number',
 'read',
 'reset',
 'set_configuration',
 'set_interface_altsetting',
 'write'
"""

#keyboard = usb.core.find(idVendor=0x46d, idProduct=0xc318)
#bei mia dev9 logitech keyboard
class TestDevice(object):
    
    @property
    def  idProduct(self):
        return 0xc318
    
    @property
    def idVendor(self):
        return 0x46d
 
    @property
    def port_number(self):
        return 2
    
    @property
    def address(self):
        return 14
    
    @property
    def bus(self):
        return 3

    @property
    def iManufacturer(self):
        return 1
    
    @property
    def iProduct(self):
        return 2
    
    @property
    def iSerialNumber(self):
        return 0

    @property
    def bDescriptorType(self):
        return 1
    
    @property
    def bDeviceClass(self):
        return 0

    @property
    def bDeviceProtocol(self):
        return ''
    
    @property
    def bDeviceSubClass(self):
        return 0
    
    @property
    def bLength(self):
        return 18
    
    @property
    def bMaxPacketSize0(self):
        return 8
    
    @property
    def bNumConfigurations(self):
        return 1
    
    @property
    def bcdDevice(self):
        return 0x5501
