import usb.core
from usbid.usbinfo import USBINFO


class DeviceInfo(object):
    
    def __init__(self, device_obj, usbinfo = USBINFO):
        self.device = device_obj  
        if self.device is None:
            raise ValueError('Device not found')

    @property
    def _vendor_id(self):
        """
        strip the 0x, because in usb file are only hex values, then zerofill
        to be in valid format for the usbid file
        """
        res = hex(self.device.idVendor)
        res = res[2:].replace(r'x', ' ')
        res = res.zfill(4)
        return res

    @property
    def _product_id(self):
        """
        strip the 0x, because in usb file are only hex values, then zerofill
        to be in valid format for the usbid file
        """
        res = hex(self.device.idProduct)
        res = res[2:].replace(r'x', ' ') 
        res = res.zfill(4)   
        return res

    @property
    def _vendor_name(self):
        """
        get vendor name
        """
        try:
            res = USBINFO._usb_ids[self._vendor_id][0]
            return res
        except:
            return "UNKNOWN"

        
    @property
    def _product_name(self):
        #get product name
        """
        except alles is nit toll, aber brings nur so zam, das er mir
        trotzdem die anderen attrs ausgibt - ansonsten kommts leer zrug
        """
        try:
            res = USBINFO._usb_ids[self._vendor_id][1][self._product_id]
            return res
        except:
            return "UNKNOWN"



    """    
    @property
    def _unicque_id(self, count=None):
        if count:
            return count
        else:
            return None
    """
        

    def print_info(self):               
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
        print 80 * '*'
        print '    idProduct: ' + hex(self.device.idProduct)
        print '    Product Name: ' + str(self._product_name)
        print '    idVendor: ' + hex(self.device.idVendor)
        print '    Vendor Name: ' + str(self._vendor_name)   
        print '    port_number: ' + str(self.device.port_number)   
        print '    address: ' + str(self.device.address)
        print '    bus: ' + str(self.device.bus)
    
        #print unicqe id if it is set
        #if hasattr(self.device, '_unicque_id'):
        #    print '    UnicqeId: ' + str(self.device._unicque_id)
    
        print '    iManufacturer: ' + str(self.device.iManufacturer)
        print '    iProduct: ' + str(self.device.iProduct)
        print '    iSerialNumber: ' + str(self.device.iSerialNumber)

        # de noch intressant??? 'bDeviceClass','bDeviceProtocol','bDeviceSubClass','bcdDevice','bcdUSB',
        # noch checken welche werte needed, und mockupklasse checken obs richtig returnt
        

