import os
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
        self.is_root = is_root
        self.parent = parent

    @property
    def idVendor(self):
        """
        get the vendor id as hex
        evtl zerofill, testen? res = res.zfill(4)
        """
        with open(os.path.join(self.path, "idVendor") ,"r") as fio:
            res = fio.read().strip()
        return res

    @property
    def idProduct(self):
        """
        get the product id as hex
        """
        with open(os.path.join(self.path, "idProduct") ,"r") as fio:
            res = fio.read().strip()
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


    @property    
    def children(self):
        #des als dict und mit keys alle nodes rausfinden port1,2,3...
        #__getitem__ umbaun 
        for filename in os.listdir(self.path):
            import pdb;pdb.set_trace()
            if ":" in filename or filename[0] not in "0123456789":
                continue
            yield DeviceNode(os.path.join(self.path, filename))
            
    # 3-2.2.4:1.0              
    """
    ^\d{1}-{1} = 1x 3-2
    (\d{1}.\d{1}) = group 2.2
    .{1}\d{1} = mind 1x 2.4
    
    """


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
 

