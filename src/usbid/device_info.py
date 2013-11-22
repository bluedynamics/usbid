import usb.core
from usbid.usbinfo import USBINFO


class DeviceInfo(object):

    def __init__(self, device_obj):
        self.device = device_obj
        
        if self.device is None:
            raise ValueError('Device not found')



    def get_info(self):
        #da no statt print iwas return,
        #wia af di werte vum parser zuagreifn?
        print 80 * '*'
    
        print '    idProduct: ' + str(self.device.idProduct)
        print '    idVendor: ' + str(self.device.idVendor)
    
        print '    port_number: ' + str(self.device.port_number)
    
        print '    address: ' + str(self.device.address)
        print '    bus: ' + str(self.device.bus)
    
        print '    iManufacturer: ' + str(self.device.iManufacturer)
        print '    iProduct: ' + str(self.device.iProduct)
        print '    iSerialNumber: ' + str(self.device.iSerialNumber)


        # zb _usb_id dann aus USBINFO.usbids rauslesen mit dictmatch iwas
        
        #import pickle und  pickle load von zb der maus
