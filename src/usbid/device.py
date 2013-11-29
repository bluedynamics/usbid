import os
import re
from usbid.usbinfo import USBINFO


def usb_roots(root_path='/sys/bus/usb/devices'):
    usb_roots = {}
    for root in os.listdir(root_path):
        if root.startswith('usb'): 
            root_id = int(root[3:])
            usb_roots[root_id] = DeviceNode(os.path.join(root_path,root), root_id, True)
    return usb_roots


class DeviceNode(object):
    
    def __init__(self, path, parent, is_root=False, usbinfo=USBINFO):
        self.path = path 
        self.parent = parent
        self.is_root = is_root


    @property
    def idVendor(self):
        """
        get the vendor id as hex
        evtl zerofill, testen? res = res.zfill(4)
        """
        #vorher res.strip() jetzt mit testfs is aber alles voll mit \x00
        with open(os.path.join(self.path, "idVendor") ,"r") as fio:
            res = fio.read().strip("\n\x00")
        return res

    @property
    def idProduct(self):
        """
        get the product id as hex
        """
        with open(os.path.join(self.path, "idProduct") ,"r") as fio:
            res = fio.read().strip("\n\x00")
        return res
    
    
    
    # nit toll bei di negstn 2
    # except alles is nit toll, aber brings nur so zam, das er mir
    # trotzdem die anderen attrs ausgibt - ansonsten kommts leer zrug

    @property
    def nameVendor(self):
        """
        get vendor name from USBINFO db file
        """
        try:
            res = USBINFO._usb_ids[self.idVendor][0]
            return res
        except:
            return "UNKNOWN"

        
    @property
    def nameProduct(self):
        """
        get product name from USBINFO db file
        """
        try:
            res = USBINFO._usb_ids[self.idVendor][1][self.idProduct]
            return res
        except:
            return "UNKNOWN"



    # 3-2.2.4:1.0              
    #de regex u alle keys(children) de nit mit :1.0 auhean griagn
    #^[0-9\-\.]+$


    def keys(self):
        res = []
        for dir in os.listdir(self.path):
            #import pdb;pdb.set_trace()
            if re.match("^[0-9\-\.]+$", dir):
                dir_l, dir_r = dir.rsplit(".", 1)
                res.append(int(dir_r))
        return res
             #da basteln


    def print_info(self):               
        print 80 * '*'
        print '    idProduct: ' + self.idProduct
        print '    idVendor: ' + self.idVendor
        print '    Product Name: ' + self.nameProduct
        print '    Vendor Name: ' + self.nameVendor  
        #print '    port_number: ' + str(self.path.port_number)   
        #print '    address: ' + str(self.path.address)
        #print '    bus: ' + str(self.path.bus)

        #print parent
        #if hasattr(self.device, 'parent'):
        #    print '    Parent: ' + str(self.device.parent)
    

        # de noch intressant??? 'bDeviceClass','bDeviceProtocol','bDeviceSubClass','bcdDevice','bcdUSB',
        # noch checken welche werte needed, und mockupklasse checken obs richtig returnt
 

