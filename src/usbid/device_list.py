from usbid.usbinfo import USBINFO      
from usbid.device import usb_roots, DeviceNode


class GetDevices(object):

    
    #alles unnotig?       
    def get_devices(self):
        for root in usb_roots():

                self.devices.append(dev)

        return self.devices

        
        
    def get_infos(self):
        print '*' * 80
        #print 'Found %i devices' % len(self.devices)
        
        for dev in self.devices:
            #print infos for each device
            dev_node = DeviceNode(dev)            
            dev_node.print_info()                    

"""
        idProduct: 0x2303
        Product Name: PL2303 Serial Port
        idVendor: 0x67b
        Vendor Name: Prolific Technology, Inc.
        port_number: 2
        address: 6
        bus: 2

    ********************************************************************************
        idProduct: 0x2303
        Product Name: PL2303 Serial Port
        idVendor: 0x67b
        Vendor Name: Prolific Technology, Inc.
        port_number: 5
        address: 7
        bus: 2
 
"""