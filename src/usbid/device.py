import os
import re
from usbid.usbinfo import USBINFO


PARENT = re.compile("^\d{1}-{1}\d{1}$")
CHILD = re.compile("^[0-9\-\.]+$")
TTY = re.compile(".*:\d{1}.\d{1}")



def usb_roots(root_path='/sys/bus/usb/devices'):
    #todo try except when access on wrong key
    usb_roots = {}  
    for root in os.listdir(root_path):
        if root.startswith('usb'): 
            root_id = int(root[3:])
            usb_roots[root_id] = DeviceNode(
                root_id, 
                os.path.join(root_path,root), 
                root_id, 
                True
            )
    return usb_roots


class DeviceNode(object):
    
    def __init__(self, own_id, fs_path, parent, is_root=False, usbinfo=USBINFO):
        self.own_id = own_id
        self.fs_path = fs_path 
        self.parent = parent
        self.is_root = is_root
        self.usbinfo = usbinfo
        
    @property
    def path(self):
        #import pdb;pdb.set_trace()
        current = self
        path = [self.own_id]
        while not current.is_root:
            current = current.parent
            path.insert(0, current.own_id)
        return path 



    # 3-2.2.4:1.0              
    #de regex u alle keys(children) de nit mit :1.0 auhean griagn
    #^[0-9\-\.]+$

    def keys(self):
        res = []
        for node in os.listdir(self.fs_path):
            # wenn root dann 3-1 daher split bei '-'
            if self.is_root and PARENT.match(node): # re.compile module level"
                node_r = node.rsplit("-", 1)[1]
                res.append(int(node_r))
            elif CHILD.match(node):
                node_r = node.rsplit(".", 1)[1]
                res.append(int(node_r))
        return res

    def values(self):
        return [_[1] for _ in self.items()]
    
    def items(self):
        res = []
        for node in os.listdir(self.fs_path):
            #wenn root dann 3-1 daher split bei -
            if self.is_root and PARENT.match(node):
                child_id = int(node.rsplit("-", 1)[1])
                dev = DeviceNode(child_id, os.path.join(self.fs_path, node), 
                                 self.fs_path)                    
                res.append( (child_id, dev) )
            elif CHILD.match(node):
                child_id = int(node.rsplit(".", 1)[1])
                dev = DeviceNode(child_id, os.path.join(self.fs_path, node), 
                                 self.fs_path)
                res.append( (child_id, dev) )
        return res
        
    def __getitem__(self, key):

        for node in os.listdir(self.fs_path):
            #if a wrong index is given raise custom value error
            try:
                #extra check if is root-dir. needed?
                if PARENT.match(node):
                    node_r = node.rsplit("-", 1)[1]
                    if key == int(node_r):
                        dev = DeviceNode(key, os.path.join(self.fs_path, node), self.fs_path)
                        return dev

                if CHILD.match(node):                    
                    node_r = node.rsplit(".", 1)[1]
                    if key == int(node_r):
                        dev = DeviceNode(key, os.path.join(self.fs_path, node), self.fs_path)
                        return dev
            except ValueError:
                return "key not found"
                
    @property
    def idVendor(self):
        """
        get the vendor id as hex
        test if zerofill needed? res = res.zfill(4)
        """
        with open(os.path.join(self.fs_path, "idVendor") ,"r") as fio:
            res = fio.read().strip("\n\x00")
        return res

    @property
    def idProduct(self):
        """
        get the product id as hex
        """
        with open(os.path.join(self.fs_path, "idProduct") ,"r") as fio:
            res = fio.read().strip("\n\x00")
        return res

    @property
    def nameVendor(self):
        """
        get vendor name from USBINFO db file
        """
        try:
            return self.usbinfo._usb_ids[self.idVendor][0]
        except:  # TODO catch specific
            return "UNKNOWN"
        
    @property
    def nameProduct(self):
        """
        get product name from USBINFO db file
        """
        try:
            return self.usbinfo._usb_ids[self.idVendor][1][self.idProduct]
        except:  # TODO catch specific
            return "UNKNOWN" 
        
    @property
    def tty(self):
        """
        return name of serial device or None if its not a serail device
        """
        for filename in os.listdir(self.fs_path):
            #import pdb;pdb.set_trace()
            if TTY.match(filename):
                for filename in os.listdir(os.path.join(self.fs_path, filename)):
                    if filename.startswith("tty"):
                        return filename
            

    def __str__(self):
        """
         __str__ return string with information nicely formatted
         """
        result = ""             
        result += "idProduct: " + self.idProduct + "\n"
        result += "idVendor: " + self.idVendor + "\n"
        result += "Product Name: " + self.nameProduct + "\n"
        result += "Vendor Name: " + self.nameVendor
        return result 

        
        # other useful stats:
        # port_number, address, bus, bDeviceClass,bDeviceProtocol,
        # bDeviceSubClass,bcdDevice,bcdUSB,


        
def devicelist(root_path='/sys/bus/usb/devices'):
    res = []
    def walk(parent):     
        for child in parent.values():
            res.append(child)
            walk(child)
    walk(usb_roots(root_path=root_path))
    return res
        
        