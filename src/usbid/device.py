"""
USB file system (From http://www.linux-usb.org/FAQ.html)
--------------------------------------------------------

# ls  /sys/bus/usb/devices/
1-0:1.0      1-1.3        1-1.3.1:1.0  1-1:1.0
1-1          1-1.3.1      1-1.3:1.0    usb1

The names that begin with "usb" refer to USB controllers. More accurately, they
refer to the "root hub" associated with each controller. The number is the USB
bus number. In the example there is only one controller, so its bus is number
1. Hence the name "usb1".

"1-0:1.0" is a special case. It refers to the root hub's interface. This acts
just like the interface in an actual hub an almost every respect; see below.

All the other entries refer to genuine USB devices and their interfaces.
The devices are named by a scheme like this:

    bus-port.port.port ...

In other words, the name starts with the bus number followed by a '-'. Then
comes the sequence of port numbers for each of the intermediate hubs along the
path to the device.

For example, "1-1" is a device plugged into bus 1, port 1. It happens to be a
hub, and "1-1.3" is the device plugged into port 3 of that hub. That device is
another hub, and "1-1.3.1" is the device plugged into its port 1.

The interfaces are indicated by suffixes having this form:

    :config.interface

That is, a ':' followed by the configuration number followed by '.' followed
by the interface number. In the above example, each of the devices is using
configuration 1 and this configuration has only a single interface, number 0.
So the interfaces show up as;

    1-1:1.0        1-1.3:1.0        1-1.3.1:1.0

A hub will never have more than a single interface; that's part of the USB
spec. But other devices can and do have multiple interfaces (and sometimes
multiple configurations). Each interface gets its own entry in sysfs and can
have its own driver.

Examples
--------

idProduct: 6010
idVendor: 0403
Product Name: FT2232C Dual USB-UART/FIFO IC
Vendor Name: Future Technology Devices International, Ltd

# ls  /sys/bus/usb/devices/
3-2       -> ../../../devices/pci0000:00/0000:00:14.0/usb3/3-2
3-2:1.0   -> ../../../devices/pci0000:00/0000:00:14.0/usb3/3-2/3-2:1.0
3-2:1.1   -> ../../../devices/pci0000:00/0000:00:14.0/usb3/3-2/3-2:1.1

idProduct: 6001
idVendor: 0403
Product Name: FT232 USB-Serial (UART) IC
Vendor Name: Future Technology Devices International, Ltd

# ls  /sys/bus/usb/devices/
3-2       -> ../../../devices/pci0000:00/0000:00:14.0/usb3/3-2
3-2.1     -> ../../../devices/pci0000:00/0000:00:14.0/usb3/3-2/3-2.1
3-2:1.0   -> ../../../devices/pci0000:00/0000:00:14.0/usb3/3-2/3-2:1.0
3-2.1:1.0 -> ../../../devices/pci0000:00/0000:00:14.0/usb3/3-2/3-2.1/3-2.1:1.0
3-2.2     -> ../../../devices/pci0000:00/0000:00:14.0/usb3/3-2/3-2.2
3-2.2:1.0 -> ../../../devices/pci0000:00/0000:00:14.0/usb3/3-2/3-2.2/3-2.2:1.0
3-2.3     -> ../../../devices/pci0000:00/0000:00:14.0/usb3/3-2/3-2.3
3-2.3:1.0 -> ../../../devices/pci0000:00/0000:00:14.0/usb3/3-2/3-2.3/3-2.3:1.0
3-2.4     -> ../../../devices/pci0000:00/0000:00:14.0/usb3/3-2/3-2.4
3-2.4:1.0 -> ../../../devices/pci0000:00/0000:00:14.0/usb3/3-2/3-2.4/3-2.4:1.0
"""


import os
import re
from usbid.usbinfo import USBINFO


PARENT = re.compile("^\d{1}-{1}\d{1}$")
CHILD = re.compile("^[0-9\-\.]+$")
TTY = re.compile(".*:\d{1}.\d{1}")


USB_FS_ROOT = '/sys/bus/usb/devices'


def usb_roots(root_path=USB_FS_ROOT):
    """This returns a dict of the usb roots.
    """
    # XXX: try except when access on wrong key
    usb_roots = {}
    for root in os.listdir(root_path):
        if root.startswith('usb'):
            root_id = int(root[3:])
            usb_roots[root_id] = DeviceNode(
                root_id,
                os.path.join(root_path, root),
                None)
    return usb_roots


def device_list(root_path=USB_FS_ROOT):
    """This returns a list of DeviceNode objects.
    """
    res = []
    def walk(parent):
        for child in parent.values():
            res.append(child)
            walk(child)
    walk(usb_roots(root_path=root_path))
    return res

# B/C
devicelist = device_list


def device_by_path(path, root_path=USB_FS_ROOT):
    """Return device node by path.
    """
    node = usb_roots(root_path=root_path)
    for name in path:
        node = node[name]
    return node


class DeviceNode(object):

    def __init__(self, own_id, fs_path, parent, usbinfo=USBINFO):
        self.own_id = own_id
        self.fs_path = fs_path
        self.parent = parent
        self.usbinfo = usbinfo

    @property
    def path(self):
        """Returns path of this device node as list of integers.
        """
        current = self
        path = [self.own_id]
        while current.parent is not None:
            current = current.parent
            path.insert(0, current.own_id)
        return path

    def keys(self):
        res = []
        for node in os.listdir(self.fs_path):
            if self.parent is None and PARENT.match(node):
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
            if self.parent is None and PARENT.match(node):
                child_id = int(node.rsplit("-", 1)[1])
                dev = DeviceNode(child_id,
                                 os.path.join(self.fs_path, node),
                                 self)
                res.append((child_id, dev))
            elif CHILD.match(node):
                # XXX: node might not contain '.'
                #      (happened at a USB3 controller)
                child_id = int(node.rsplit(".", 1)[1])
                dev = DeviceNode(child_id,
                                 os.path.join(self.fs_path, node),
                                 self)
                res.append((child_id, dev))
        return res

    def __getitem__(self, key):
        for node in os.listdir(self.fs_path):
            if PARENT.match(node):
                node_r = node.rsplit("-", 1)[1]
                if key == int(node_r):
                    dev = DeviceNode(key,
                                     os.path.join(self.fs_path, node),
                                     self)
                    return dev

            if CHILD.match(node):
                node_r = node.rsplit(".", 1)[1]
                if key == int(node_r):
                    dev = DeviceNode(key,
                                     os.path.join(self.fs_path, node),
                                     self)
                    return dev
        raise KeyError("No such Device with %s with in path %s" %
                       (key, '/'.join([str(_) for _ in self.path])))

    @property
    def idVendor(self):
        """Get the vendor id as hex
        test if zerofill needed? res = res.zfill(4)
        """
        with open(os.path.join(self.fs_path, "idVendor"), "r") as fio:
            res = fio.read().strip("\n\x00")
        return res

    @property
    def idProduct(self):
        """Get the product id as hex.
        """
        with open(os.path.join(self.fs_path, "idProduct"), "r") as fio:
            res = fio.read().strip("\n\x00")
        return res

    @property
    def nameVendor(self):
        """Get vendor name from USBINFO db file.
        """
        try:
            return self.usbinfo.usb_ids[self.idVendor][0]
        except KeyError:
            return "UNKNOWN"

    @property
    def nameProduct(self):
        """Get product name from USBINFO db file.
        """
        try:
            return self.usbinfo.usb_ids[self.idVendor][1][self.idProduct]
        except KeyError:
            return "UNKNOWN"

    @property
    def tty(self):
        """Return name of serial device or None if its not a serial device.
        """
        def match_tty(path):
            for filename in os.listdir(path):
                if filename.startswith("tty"):
                    # final tty device
                    if filename != 'tty':
                        return filename
                    # search in tty sub directory
                    return match_tty(os.path.join(path, filename))
        for filename in os.listdir(self.fs_path):
            if TTY.match(filename):
                return match_tty(os.path.join(self.fs_path, filename))

    def __str__(self):
        """Return string with information nicely formatted.
        """
        # other useful stats which can be accessed:
        # port_number, address, bus, bDeviceClass,bDeviceProtocol,
        # bDeviceSubClass,bcdDevice,bcdUSB
        result = ""
        result += "idProduct: " + self.idProduct + "\n"
        result += "idVendor: " + self.idVendor + "\n"
        result += "Product Name: " + self.nameProduct + "\n"
        result += "Vendor Name: " + self.nameVendor
        return result
