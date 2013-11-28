from usbid.usbinfo import USBINFO      
from usbid.device_info import DeviceInfo


class GetDevices(object):
             
    def get_connected_devices(self):
        all_devices = usb.core.find(find_all=True)
        self.devices = []
        self.devices = all_devices
        for dev in all_devices:
            # ignore hubs
            if dev.bDeviceClass != 9:
                self.devices.append(dev)
                
        """
        (Pdb) self.devices[0].idVendor
        5246
        (Pdb) self.devices[0].idProduct
        4097
        """
        #self.devices[dev]._unicque_id = 1
        # dev = usb.core.find(idVendor=0x67b, idProduct=0x2303)
        return self.devices

        
        
    def get_infos(self):
        print '*' * 80
        print '*' * 80
        print 'Found %i devices,(hubs are being ignored)' % len(self.devices)
        
        for dev in self.devices:
            #print infos for each device
            dev_info_obj = DeviceInfo(dev)            
            dev_info_obj.print_info()                    

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