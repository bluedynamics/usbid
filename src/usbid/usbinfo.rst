prepare
-------

imports::

    >>> from usbid.usbinfo import USBInfo
    >>> FAKE_FILE = '/i/dontexist'

set up parser::
   
    >>> info = USBInfo(FAKE_FILE)


parser
------

open a nonexisting file::

    >>> info._parse_usbids()
    Traceback (most recent call last):
    ...
    IOError: Can't open file /i/dontexist in order to parse usbinfo.

open test usb info file and parse the individual lists::

    >>> info = USBInfo(TEST_USBIDS_FILE)
    >>> info._parse_usbids()

    >>> pprint(info._usb_ids)
    {'0079': ('DragonRise Inc.',
              {'0006': 'Generic USB Joystick', '0011': 'Gamepad'}),
     '0105': ('Trust International B.V.',
              {'145f': 'NW-3100 802.11b/g 54Mbps Wireless Network Adapter [zd1211]'}),
     '0460': ('Ace Cad Enterprise Co., Ltd', {'0004': 'Tablet (5x3.75)'}),
     '0d8d': ('Promotion & Display Technology, Ltd',
              {'0234': 'V-234 Composite Device'})}

    >>> pprint(info._device_classes)
    {'01': ('Audio', {'01': ('Control Device', {})}),
     '06': ('Imaging',
            {'01': ('Still Image Capture',
                    {'01': 'Picture Transfer Protocol (PIMA 15470)'})}),
     '09': ('Hub', {'00': ('Unused', {'00': 'Full speed (or root) hub'})})}

    >>> pprint(info._audio_class_terminal_types)
    {'0707': 'Analog Tape', '0708': 'Phonograph', '0709': 'VCR Audio'}

    >>> pprint(info._hid_descriptor_types)
    {'21': 'HID', '22': 'Report', '23': 'Physical'}

    >>> pprint(info._hid_descriptor_item_types)
    {'08': 'Usage', '14': 'Logical Minimum', '18': 'Usage Minimum'}

    >>> pprint(info._physical_descriptor_bias_types)
    {'0': 'Not Applicable', '1': 'Right Hand', '2': 'Left Hand'}

    >>> pprint(info._physical_descriptor_item_types)
    {'00': 'None', '01': 'Hand', '02': 'Eyeball', '03': 'Eyebrow'}

    >>> pprint(info._hid_usages)
    {'00': ('Undefined', {}),
     '01': ('Generic Desktop Controls',
            {'000': 'Undefined',
             '001': 'Pointer',
             '002': 'Mouse',
             '004': 'Joystick'})}

    >>> pprint(info._languages)
    {'0001': ('Arabic', {'01': 'Saudi Arabia', '02': 'Iraq'}),
     '0002': ('Bulgarian', {}),
     '0003': ('Catalan', {}),
     '0004': ('Chinese', {'01': 'Traditional', '02': 'Simplified'})}

    >>> pprint(info._country_codes)
    {'00': 'Not supported',
     '01': 'Arabic',
     '03': 'Canadian-Bilingual',
     '08': 'French',
     '09': 'German'}

    >>> pprint(info._video_class_terminal_types)
    {'0100': 'USB Vendor Specific',
     '0101': 'USB Streaming',
     '0202': 'Sequential Media',
     '0403': 'Component Video'}


Public API
----------

Property access with on-demand parsing::

    >>> info = USBInfo(TEST_USBIDS_FILE)
    >>> pprint(info.usb_ids)
    {'0079': ('DragonRise Inc.',
              {'0006': 'Generic USB Joystick', '0011': 'Gamepad'}),
     '0105': ('Trust International B.V.',
              {'145f': 'NW-3100 802.11b/g 54Mbps Wireless Network Adapter [zd1211]'}),
     '0460': ('Ace Cad Enterprise Co., Ltd', {'0004': 'Tablet (5x3.75)'}),
     '0d8d': ('Promotion & Display Technology, Ltd',
              {'0234': 'V-234 Composite Device'})}

    >>> info = USBInfo(TEST_USBIDS_FILE)
    >>> pprint(info.device_classes)
    {'01': ('Audio', {'01': ('Control Device', {})}),
     '06': ('Imaging',
            {'01': ('Still Image Capture',
                    {'01': 'Picture Transfer Protocol (PIMA 15470)'})}),
     '09': ('Hub', {'00': ('Unused', {'00': 'Full speed (or root) hub'})})}

    >>> info = USBInfo(TEST_USBIDS_FILE)
    >>> pprint(info.audio_class_terminal_types)
    {'0707': 'Analog Tape', '0708': 'Phonograph', '0709': 'VCR Audio'}

    >>> info = USBInfo(TEST_USBIDS_FILE)
    >>> pprint(info.hid_descriptor_types)
    {'21': 'HID', '22': 'Report', '23': 'Physical'}

    >>> info = USBInfo(TEST_USBIDS_FILE)
    >>> pprint(info.hid_descriptor_item_types)
    {'08': 'Usage', '14': 'Logical Minimum', '18': 'Usage Minimum'}

    >>> info = USBInfo(TEST_USBIDS_FILE)
    >>> pprint(info.physical_descriptor_bias_types)
    {'0': 'Not Applicable', '1': 'Right Hand', '2': 'Left Hand'}

    >>> info = USBInfo(TEST_USBIDS_FILE)
    >>> pprint(info.physical_descriptor_item_types)
    {'00': 'None', '01': 'Hand', '02': 'Eyeball', '03': 'Eyebrow'}

    >>> info = USBInfo(TEST_USBIDS_FILE)
    >>> pprint(info.hid_usages)
    {'00': ('Undefined', {}),
     '01': ('Generic Desktop Controls',
            {'000': 'Undefined',
             '001': 'Pointer',
             '002': 'Mouse',
             '004': 'Joystick'})}

    >>> info = USBInfo(TEST_USBIDS_FILE)
    >>> pprint(info.languages)
    {'0001': ('Arabic', {'01': 'Saudi Arabia', '02': 'Iraq'}),
     '0002': ('Bulgarian', {}),
     '0003': ('Catalan', {}),
     '0004': ('Chinese', {'01': 'Traditional', '02': 'Simplified'})}

    >>> info = USBInfo(TEST_USBIDS_FILE)
    >>> pprint(info.country_codes)
    {'00': 'Not supported',
     '01': 'Arabic',
     '03': 'Canadian-Bilingual',
     '08': 'French',
     '09': 'German'}

    >>> info = USBInfo(TEST_USBIDS_FILE)
    >>> pprint(info.video_class_terminal_types)
    {'0100': 'USB Vendor Specific',
     '0101': 'USB Streaming',
     '0202': 'Sequential Media',
     '0403': 'Component Video'}
