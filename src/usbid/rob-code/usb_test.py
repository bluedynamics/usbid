import os
import urllib2
import usb.core

"""
install pyusb

sudo easy_install pyusb

https://pypi.python.org/pypi/pyusb

USB device classes:

  bDeviceClass            0 (Defined at Interface level)
  bDeviceClass            9 Hub
  bDeviceClass          239 Miscellaneous Device
  bDeviceClass          255 Vendor Specific Class

"""


DATABASE_FILENAME = 'usb.ids'
DATABASE_FILE_URL = 'http://www.linux-usb.org/usb.ids'

# http://www.linux-usb.org/usb.devices.txt

class USBIDParser(object):
    _db = dict()

    def __init__(self):
        if not os.path.exists(DATABASE_FILENAME):
            db_in = urllib2.urlopen(DATABASE_FILE_URL)
            with open(DATABASE_FILENAME, 'w') as db_out:
                db_out.write(db_in.read())
            db_in.close()
        if not self._db:
            self._parse()

    def _parse(self):
        with open(DATABASE_FILENAME, 'r') as raw:
            line = raw.readline()
            while line != '':
                line = line.strip('\n')
                if not line or line[0] == '#':
                    line = raw.readline()
                    continue
                self._parse_vendor(raw, line)
                self._parse_device_class(raw, line)
                self._parse_audio_class_terminal_type(raw, line)
                self._parse_hid_descriptor_type(raw, line)
                self._parse_hid_descriptor_item_type(raw, line)
                self._parse_physical_descriptor_bias_type(raw, line)
                self._parse_physical_descriptor_item_type(raw, line)
                self._parse_hid_usage(raw, line)
                self._parse_language(raw, line)
                self._parse_hid_descriptor_country_code(raw, line)
                self._parse_video_class_terminal_type(raw, line)
                line = raw.readline()

    def _parse_vendor(self, raw, line):
        """
        # Vendors, devices and interfaces. Please keep sorted.
        # vendor  vendor_name
        #    device  device_name                <-- single tab
        #        interface  interface_name        <-- two tabs
        0001  Fry's Electronics
            142b  Arbiter Systems, Inc.
        """
        if line[0] == '\t':
            return
        try:
            vendor_id = int(line[:4], 16)
        except:
            return
        vendors = self._db.setdefault('vendors', dict())
        vendor = vendors[vendor_id] = {
            'name': line[4:].strip(),
            'devices': dict(),
        }
        last_pos = raw.tell()
        device_line = raw.readline()
        while device_line.startswith('\t'):
            interfaces = dict()
            if device_line.startswith('\t\t'):
                interface_line = device_line
                while interface_line.startswith('\t\t'):
                    interface_line = interface_line.strip('\t\t')
                    interface_id = int(
                        interface_line[:interface_line.find(' ')], 16)
                    interfaces[interface_id] = \
                        interface_line[interface_line.find(' '):].strip()
                    last_pos = raw.tell()
                    interface_line = raw.readline()
                raw.seek(last_pos)
            device_line = device_line.strip('\t')
            device_id = int(device_line[:4], 16)
            vendor['devices'][device_id] = {
                'name': device_line[4:].strip(),
                'interfaces': interfaces,
            }
            last_pos = raw.tell()
            device_line = raw.readline()
        raw.seek(last_pos)

    def _parse_device_class(self, raw, line):
        """
        # List of known device classes, subclasses and protocols
        # C class  class_name
        #    subclass  subclass_name            <-- single tab
        #        protocol  protocol_name        <-- two tabs
        C 02  Communications
            01  Direct Line
            02  Abstract (modem)
                00  None
                01  AT-commands (v.25ter)
        """
        if line[0] != 'C':
            return
        class_id = int(line[2:4], 16)
        device_classes = self._db.setdefault('device_classes', dict())
        device_class = device_classes[class_id] = {
            'name': line[4:].strip(),
            'sub_classes': dict(),
        }
        last_pos = raw.tell()
        sub_class_line = raw.readline()
        while sub_class_line.startswith('\t'):
            protocols = dict()
            if sub_class_line.startswith('\t\t'):
                protocol_line = sub_class_line
                while protocol_line.startswith('\t\t'):
                    protocol_line = protocol_line.strip('\t\t')
                    protocol_id = int(
                        protocol_line[:protocol_line.find(' ')], 16)
                    protocols[protocol_id] = \
                        protocol_line[protocol_line.find(' '):].strip()
                    last_pos = raw.tell()
                    protocol_line = raw.readline()
                raw.seek(last_pos)
            sub_class_line = sub_class_line.strip('\t')
            sub_class_id = int(sub_class_line[:sub_class_line.find(' ')], 16)
            device_class['sub_classes'][sub_class_id] = {
                'name': sub_class_line[sub_class_line.find(' '):].strip(),
                'protocols': protocols,
            }
            last_pos = raw.tell()
            sub_class_line = raw.readline()
        raw.seek(last_pos)

    def _parse_audio_class_terminal_type(self, raw, line):
        """
        # List of Audio Class Terminal Types
        # AT terminal_type  terminal_type_name
        AT 0100  USB Undefined
        """

    def _parse_hid_descriptor_type(self, raw, line):
        """
        # List of HID Descriptor Types
        # HID descriptor_type  descriptor_type_name
        HID 21  HID
        """

    def _parse_hid_descriptor_item_type(self, raw, line):
        """
        # List of HID Descriptor Item Types
        # Note: 2 bits LSB encode data length following
        # R item_type  item_type_name
        R 04  Usage Page
        """

    def _parse_physical_descriptor_bias_type(self, raw, line):
        """
        # List of Physical Descriptor Bias Types
        # BIAS item_type  item_type_name
        BIAS 0  Not Applicable
        """

    def _parse_physical_descriptor_item_type(self, raw, line):
        """
        # List of Physical Descriptor Item Types
        # PHY item_type  item_type_name
        PHY 00  None
        """

    def _parse_hid_usage(self, raw, line):
        """
        # List of HID Usages
        # HUT hi  _usage_page  hid_usage_page_name
        #    hid_usage  hid_usage_name
        HUT 01  Generic Desktop Controls
            000  Undefined
            001  Pointer
        """

    def _parse_language(self, raw, line):
        """
        # List of Languages
        # L language_id  language_name
        #    dialect_id  dialect_name
        L 0001  Arabic
            01  Saudi Arabia
        """

    def _parse_hid_descriptor_country_code(self, raw, line):
        """
        # HID Descriptor bCountryCode
        # HID Specification 1.11 (2001-06-27) page 23
        # HCC country_code keymap_type
        HCC 00  Not supported
        """

    def _parse_video_class_terminal_type(self, raw, line):
        """
        # List of Video Class Terminal Types
        # VT terminal_type  terminal_type_name
        VT 0100  USB Vendor Specific
        """

    def vendor(self, vendor_id):
        """Return vendor name and vendor devices by vendor id. vendor id must
        be hex or int value.
        """
        for line in self._db:
            if not line.strip() or line[0] in ['#', '\t']:
                continue
        if isinstance(vendor_id, basestring):
            vendor_id = int(vendor_id, 16)


parser = USBIDParser()
print parser._db['vendors'][0xf4ec]
print ''
print parser._db['device_classes'][0xe0]

"""
devs = usb.core.find(find_all=True)


print 'Found %i devices' % len(devs)

for dev in devs:
    # ignore hubs
    if dev.bDeviceClass == 9:
        continue

    print 80 * '*'

    print '    idProduct: ' + str(dev.idProduct)
    print '    idVendor: ' + str(dev.idVendor)

    print '    port_number: ' + str(dev.port_number)

    print '    address: ' + str(dev.address)
    print '    bus: ' + str(dev.bus)

    print '    iManufacturer: ' + str(dev.iManufacturer)
    print '    iProduct: ' + str(dev.iProduct)
    print '    iSerialNumber: ' + str(dev.iSerialNumber)

    #print '    bDescriptorType: ' + str(dev.bDescriptorType)
    #print '    bDeviceClass: ' + str(dev.bDeviceClass)
    #print '    bDeviceProtocol: ' + str(dev.bDeviceProtocol)
    #print '    bDeviceSubClass: ' + str(dev.bDeviceSubClass)
    #print '    bLength: ' + str(dev.bLength)
    #print '    bMaxPacketSize0: ' + str(dev.bMaxPacketSize0)
    #print '    bNumConfigurations: ' + str(dev.bNumConfigurations)

    #print '    bcdDevice: ' + str(dev.bcdDevice)
    #print '    bcdUSB: ' + str(dev.bcdUSB)

    #ctrl_transfer
    #default_timeout

    #attach_kernel_driver
    #detach_kernel_driver
    #is_kernel_driver_active
    #set_interface_altsetting

    #get_active_configuration
    #set_configuration

    #read
    #write
    #reset
"""
