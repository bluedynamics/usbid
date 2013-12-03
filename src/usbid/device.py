import os
import re
from usbid.usbinfo import USBINFO


def usb_roots(root_path='/sys/bus/usb/devices'):
    #todo try except wenn zugriff af falschen key
    usb_roots = {}  
    for root in os.listdir(root_path):
        if root.startswith('usb'): 
            root_id = int(root[3:])
            usb_roots[root_id] = DeviceNode(os.path.join(root_path,root), root_id, True)
    return usb_roots

    """
    habs nit so mit der gschachtelten walker rekursion,
    im fs bei usb devices is auf dem 
    sys/bus/usb/devices/usb2/2-1/2-1.2/2-1.2.1/2-1.2.1:1.0/ttyUSB0/
    nur sehr wenig info drauf -.-  evtl man anschaun
    
    bei key_to_fs_dir - in ttyusb1 key zb mitgebn und dann suchn wos liegt?


    """
#mal testn aba geht nit so wirklich
def traverse(data):
    results = []
    def inner(data):
        
        if isinstance(data, dict):
            for item in data.values():
                inner(item)
        elif isinstance(data, list) or isinstance(data, tuple):
            for item in data:
                inner(item)
        else:
            results.append(data)
    inner(data)
    return results

 

class DeviceNode(object):
    
    def __init__(self, path, parent, is_root=False, usbinfo=USBINFO):
        self.path = path 
        self.parent = parent
        self.is_root = is_root


    def device_by_path(self):
        # find a endpoint and look if it has a ttyusb folder inside
        #needs some love and return obj and not only path?
        #import pdb;pdb.set_trace()
        for dir in os.listdir(self.path):
            #^[0-9\-\.]+:[\d.\d]+$
            if re.match("^[0-9\-\.]+:[\d.\d]+$", dir):
                #new dir is ...:1.0
                #import pdb;pdb.set_trace()
                deep_dir = os.path.join(self.path, dir)
                for dir in os.listdir(deep_dir):
                    if re.match("^ttyUSB[\d]+$", dir):
                        dir = os.path.join(deep_dir, dir)
                        return dir
                    
# da is ttyUSB0 sys/bus/usb/devices/usb2/2-1/2-1.2/2-1.2.1/2-1.2.1:1.0    
# da is es ttyUSB1 /sys/bus/usb/devices/usb2/2-1/2-1.2/2-1.2.6/2-1.2.6:1.0   




    # 3-2.2.4:1.0              
    #de regex u alle keys(children) de nit mit :1.0 auhean griagn
    #^[0-9\-\.]+$

    def keys(self):
        res = []
        for dir in os.listdir(self.path):
            #
            #wenn root dann 3-1 daher split bei '-'
            if self.is_root:
                if re.match("^\d{1}-{1}\d{1}$", dir):
                    dir_l, dir_r = dir.rsplit("-", 1)
                    res.append(int(dir_r))
                    continue
                
            if re.match("^[0-9\-\.]+$", dir):
                dir_l, dir_r = dir.rsplit(".", 1)
                res.append(int(dir_r))
        return res

    def values(self):
        #da is objekt was dann af dem pfad liegt. mit regexp zambaun?
        # bei __items__ gib i na is objekt zum entsprechenden key zrug
        res = []
        for dir in os.listdir(self.path):
            if re.match("^\d{1}-{1}\d{1}$", dir):
                #import pdb;pdb.set_trace()
                dev = DeviceNode(os.path.join(self.path, dir), self.path)
                res.append(dev)
                continue
            
            if re.match("^[0-9\-\.]+$", dir):
                dev = DeviceNode(os.path.join(self.path, dir), self.path)
                res.append(dev)
        return res  
    
    def items(self):
        #return tuples of key value 1: <object at..blablapath2-1> and so on
        res = {}
        for dir in os.listdir(self.path):
            #wenn root dann 3-1 daher split bei -
            if self.is_root:
                if re.match("^\d{1}-{1}\d{1}$", dir):
                    dir_l, dir_r = dir.rsplit("-", 1)
                    dev = DeviceNode(os.path.join(self.path, dir), self.path)
                    
                    res[int(dir_r)] = dev
                    # old res.append(int(dir_r))
                    continue
                
            if re.match("^[0-9\-\.]+$", dir):
                dir_l, dir_r = dir.rsplit(".", 1)
                dev = DeviceNode(os.path.join(self.path, dir), self.path)
                res[int(dir_r)] = dev
        return res
    
    
    def __getitem__(self, key):

        for dir in os.listdir(self.path):
            #if a wrong index is given raise custom value error
            try:
                #extra check if is root-dir. needed???
                if re.match("^\d{1}-{1}\d{1}$", dir):
                    dir_l, dir_r = dir.rsplit("-", 1)
                    if key == int(dir_r):
                        dev = DeviceNode(os.path.join(self.path, dir), self.path)
                        return dev

                if re.match("^[0-9\-\.]+$", dir):                    
                    dir_l, dir_r = dir.rsplit(".", 1)
                    if key == int(dir_r):
                        dev = DeviceNode(os.path.join(self.path, dir), self.path)
                        return dev
            except ValueError:
                return "key not found"






                
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
 
