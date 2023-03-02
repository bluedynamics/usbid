from __future__ import print_function
import os
import re


USB_FS_ROOT = '/sys/bus/usb/devices'
IS_BUS = re.compile("^usb\d$")
IS_BUS_PORT = re.compile("^\d-\d$")
IS_SUB_PORT = re.compile("^\d-\d(\.\d)*$")
IS_INTERFACE = re.compile("^\d-\d(\.\d)*:\d.\d$")


class Container(object):
    """Mixin for container objects."""
    name = None
    parent = None

    def keys(self):
        return list(self.__iter__())

    def values(self):
        return [self[key] for key in self]

    def items(self):
        return [(key, self[key]) for key in self]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __iter__(self):
        raise NotImplementedError()

    def __getitem__(self, key):
        raise NotImplementedError()


class FSLocation(object):
    """Mixin for objects with a file system location."""
    fs_path = None

    @property
    def fs_name(self):
        if self.fs_path.find(os.path.sep) > -1:
            return self.fs_path[self.fs_path.rfind(os.path.sep) + 1:]

    @property
    def fs_parent(self):
        if self.fs_path.find(os.path.sep) > -1:
            return self.fs_path[:self.fs_path.rfind(os.path.sep)]


class FileAttributes(FSLocation):
    """Mixin for objects handling attributes stored in files. A single file
    represents a single attribute where the file name is the attribute name
    and the file content is the attribute value.
    """
    __file_attributes__ = []

    def __getattribute__(self, name):
        if name in object.__getattribute__(self, '__file_attributes__'):
            try:
                with open(os.path.join(self.fs_path, name), 'r') as file:
                    return file.read().strip('\n').strip()
            except IOError:
                return None
        return object.__getattribute__(self, name)


class ReprMixin(object):
    """Mixin for objects inside the USB filesystem tree for debugging."""

    def __repr__(self):
        return '<{0}.{1} [{2}] at {3}>'.format(
            self.__module__,
            self.__class__.__name__,
            self.fs_name,
            id(self)
        )

    def treerepr(self, indent=0, prefix=' '):
        res = '{0}{1}\n'.format(indent * prefix, repr(self))
        manufacturer = getattr(self, 'manufacturer', None)
        if manufacturer is not None:
            res += '{0}- {1}\n'.format((indent + 4) * prefix, manufacturer)
        product = getattr(self, 'product', None)
        if product is not None:
            res += '{0}- {1}\n'.format((indent + 4) * prefix, product)
        if isinstance(self, InterfaceProvider):
            for iface in sorted(self.interfaces, key=lambda x: x.fs_name):
                res += '{0}{1}\n'.format((indent + 2) * prefix, repr(iface))
                tty = iface.tty
                if tty:
                    res += '{0}- {1}\n'.format((indent + 4) * prefix, tty)
        for node in sorted(self.values(), key=lambda x: x.fs_name):
            res += node.treerepr(indent + 2, prefix)
        return res

    def printtree(self):  # pragma: no cover
        print(self.treerepr())


class InterfaceProvider(Container, FSLocation):
    """Mixin for objects providing USB interfaces."""

    @property
    def interfaces(self):
        ifaces = []
        for child in os.listdir(self.fs_path):
            if IS_INTERFACE.match(child):
                iface_path = os.path.join(self.fs_path, child)
                ifaces.append(Interface(parent=self, fs_path=iface_path))
        return ifaces


class InterfaceAggregator(object):
    """Mixin for objects providing USB interface aggregation."""

    def aggregated_interfaces(self, tty=False):
        def aggregate(node, ifaces):
            for child in node.values():
                if isinstance(child, InterfaceProvider):
                    for iface in child.interfaces:
                        if tty and iface.tty is None:
                            continue
                        ifaces.append(iface)
                aggregate(child, ifaces)
        ifaces = []
        aggregate(self, ifaces)
        return ifaces


class USB(Container, FSLocation, InterfaceAggregator, ReprMixin):
    """Object representing USB filsystem root."""

    def __init__(self, fs_path=USB_FS_ROOT):
        self.fs_path = fs_path

    def __iter__(self):
        for child in os.listdir(self.fs_path):
            if IS_BUS.match(child):
                yield child[3:]

    def __getitem__(self, key):
        bus_path = os.path.join(self.fs_path, 'usb{0}'.format(key))
        if not os.path.isdir(bus_path):
            raise KeyError(key)
        return Bus(name=key, parent=self, fs_path=bus_path)

    def __repr__(self):
        return '<{0}.{1} [{2}] at {3}>'.format(
            self.__module__,
            self.__class__.__name__,
            self.fs_path,
            id(self)
        )

    def get_interface(self, fs_name):
        port_path = list(reversed(
            fs_name.replace('-', '.').split(':')[0].split('.')
        ))
        node = self
        while port_path:
            node = node[port_path.pop()]
        for iface in node.interfaces:
            if iface.fs_name == fs_name:
                return iface


class Bus(FileAttributes, InterfaceProvider, ReprMixin):
    """Object representing a USB bus."""
    __file_attributes__ = [
        'authorized',
        'authorized_default',
        'avoid_reset_quirk',
        'bcdDevice',
        'bConfigurationValue',
        'bDeviceClass',
        'bDeviceProtocol',
        'bDeviceSubClass',
        'bmAttributes',
        'bMaxPacketSize0',
        'bMaxPower',
        'bNumConfigurations',
        'bNumInterfaces',
        'busnum',
        'dev',
        'devnum',
        'devpath',
        'idProduct',
        'idVendor',
        'ltm_capable',
        'manufacturer',
        'maxchild',
        'product',
        'quirks',
        'removable',
        'serial',
        'speed',
        'uevent',
        'urbnum',
        'version',
    ]

    def __init__(self, name, parent, fs_path):
        if not os.path.isdir(fs_path):
            raise ValueError('Invalid path given')
        self.name = name
        self.parent = parent
        self.fs_path = fs_path

    def __iter__(self):
        for child in os.listdir(self.fs_path):
            if IS_BUS_PORT.match(child):
                yield child[child.find('-') + 1:]

    def __getitem__(self, key):
        port_path = os.path.join(
            self.fs_path,
            '{0}-{1}'.format(self.name, key)
        )
        if not os.path.isdir(port_path):
            raise KeyError(key)
        return Port(name=key, parent=self, fs_path=port_path)


class Port(FileAttributes, InterfaceProvider, ReprMixin):
    """Object representing a USB port."""
    __file_attributes__ = [
        'authorized',
        'avoid_reset_quirk',
        'bcdDevice',
        'bConfigurationValue',
        'bDeviceClass',
        'bDeviceProtocol',
        'bDeviceSubClass',
        'bmAttributes',
        'bMaxPacketSize0',
        'bMaxPower',
        'bNumConfigurations',
        'bNumInterfaces',
        'busnum',
        'dev',
        'devnum',
        'devpath',
        'idProduct',
        'idVendor',
        'ltm_capable',
        'manufacturer',
        'maxchild',
        'product',
        'quirks',
        'removable',
        'serial',
        'speed',
        'uevent',
        'urbnum',
        'version',
    ]

    def __init__(self, name, parent, fs_path):
        if not os.path.isdir(fs_path):
            raise ValueError('Invalid path given')
        self.name = name
        self.parent = parent
        self.fs_path = fs_path

    def __iter__(self):
        for child in os.listdir(self.fs_path):
            if IS_SUB_PORT.match(child):
                yield child[child.rfind('.') + 1:]

    def __getitem__(self, key):
        port_path = os.path.join(
            self.fs_path,
            '{0}.{1}'.format(self.fs_name, key)
        )
        if not os.path.isdir(port_path):
            raise KeyError(key)
        return Port(name=key, parent=self, fs_path=port_path)


class Interface(FileAttributes, ReprMixin):
    """Object representing a USB interface."""
    __file_attributes__ = [
        'bAlternateSetting',
        'bInterfaceClass',
        'bInterfaceNumber',
        'bInterfaceProtocol',
        'bInterfaceSubClass',
        'bNumEndpoints',
        'interface',
        'modalias',
        'supports_autosuspend',
        'uevent',
    ]

    def __init__(self, parent, fs_path):
        if not os.path.isdir(fs_path):
            raise ValueError('Invalid path given')
        self.parent = parent
        self.fs_path = fs_path

    @property
    def manufacturer(self):
        return self.parent.manufacturer

    @property
    def product(self):
        return self.parent.product

    @property
    def tty(self):
        def match_tty(path):
            for child in os.listdir(path):
                if not child.startswith("tty"):
                    continue
                # final tty device
                if child != 'tty':
                    return child
                # search in tty sub directory
                return match_tty(os.path.join(path, child))
        return match_tty(self.fs_path)
