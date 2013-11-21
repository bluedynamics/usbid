from pkg_resources import resource_filename
DEFAULT_USBIDS_FILE = resource_filename(__name__, 'data/usb.ids')

LISTOF_MAP = {
    '': '_usb_ids',
    'C': '_device_classes',
    'AT': '_audio_class_terminal_types',
    'HID': '_hid_descriptor_types',
    'R': '_hid_descriptor_item_types',
    'BIAS': '._physical_descriptor_bias_types',
    'PHY': '_physical_descriptor_item_types',
    'HUT': '_hid_usages',
    'L': '_languages',
    'HCC': '_country_codes',
    'VT': '_video_class_terminal_types',
}

BLOCK_WITH_3_LEVELS = ['C']


class USBInfo(object):

    def __init__(self):
        for value in LISTOF_MAP.values():
            setattr(self, value, None)
      
    def _parse_usbids(self, filename=DEFAULT_USBIDS_FILE):
        self.filename = filename
        block_0 = None
        block_1 = None
        block_2 = None
        block_type_key = None
        
        with open(filename, 'r') as raw:
            for line in raw:     
                line = line.strip('\n')  
                if not line or line[0] == '#':
                    continue
                          
                if not line[0] == '\t':
                    #lvl 0
                    left, right = line.split('  ', 1)
                    
                    if not ' ' in left:
                        #check usb_ids
                        block_id = left
                        block_type_key = '' 
                    else:
                        block_type_key, block_id  = left.split(' ')
                        
                    block_type = LISTOF_MAP[block_type_key]  
                    block_0 = getattr(self, block_type)
                    if block_0 is None:
                        block_0 = {}
                        setattr(self, block_type, block_0)
                        
                    block_1 = {}
                    block_0[block_id] = (right, block_1)
                    continue
                               
                if line.startswith('\t\t'):
                    #lvl2
                    line = line.strip('\t\t')
                    left, right = line.split('  ', 1)
                    block_2[left] = right
                    continue
                
                if not line.startswith('\t'):
                    raise ValueError("File corrupt")
                
                #lvl1
                line = line.strip('\t')
                left, right = line.split('  ', 1) 
                if block_type_key in BLOCK_WITH_3_LEVELS:
                    block_2 = {}
                    block_1[left] = (right, block_2)
                else:
                    block_1[left] = right

        @property
        def usb_ids(self):
            """
            dict of usbids with key as vendor id and value as a tuple consisting of 
            vendor name and dict of key as device id and value as device name
            """
            if self._usb_ids is None:
                self._parse_usbids()
            return self._usb_ids
        
        
        @property
        def device_classes(self):
            """
            dict of device classes with key as class id and value as a tuple consisting of 
            class name and dict of key as subclass id and value as a tuple consisting of
            subclass name and dict of key as protocol id and value as protocol name
            
            example::
            
                '09': ('Hub',
                    {'00': ('Unused',
                        {'00': 'Full speed (or root) hub',
                         '01': 'Single TT',
                         '02': 'TT per port'})})
            """
            if self._device_classes is None:
                self._parse_usbids()
            return self._device_classes

        
        @property
        def audio_class_terminal_types(self):
            """
            dict of audio class terminal types with key as terminal type and 
            value as terminal name
            """
            if self._audio_class_terminal_types is None:
                self._parse_usbids()
            return self._audio_class_terminal_types
        
   
        @property
        def hid_descriptor_types(self):
            """
            dict of HID descriptor types with key as HID descriptor type and 
            value as descriptor type name
            """
            if self._hid_descriptor_types is None:
                self._parse_usbids()
            return self._hid_descriptor_types
        
        
        @property
        def hid_descriptor_item_types(self):
            """
            dict of HID descriptor item types with key as item type and 
            value as item type name            
            """
            if self._hid_descriptor_item_types is None:
                self._parse_usbids()
            return self._hid_descriptor_item_types
        
        
        @property
        def physical_descriptor_bias_types(self):
            """
            dict of BIAS item types with key as BIAS item type and 
            value as item type name 
            """
            if self._physical_descriptor_bias_types is None:
                self._parse_usbids()
            return self._physical_descriptor_bias_types
        
            
        @property
        def physical_descriptor_item_types(self):
            """
            dict of PHY item types with key as PHY item type and 
            value as item type name             
            """
            if self._physical_descriptor_item_types is None:
                self._parse_usbids()
            return self._physical_descriptor_item_types
        
     
        @property
        def hid_usages(self):
            """
            dict of HID usages with key as HID id and value as a tuple consisting of 
            HID usage page name and a dict of key as hid usage and value as hid usage name
            """
            if self._hid_usages is None:
                self._parse_usbids()
            return self._hid_usages
        
   
        @property
        def languages(self):
            """
            dict of languages with key as language id and value as a tuple consisting of
            language name and a dict of key as dialect id and value as dialect name   
            """
            if self._languages is None:
                self._parse_usbids()
            return self._languages


        @property
        def video_class_terminal_types(self):
            """
            dict of video class terminal types with key as terminal type and
            value as terminal type name
            """
            if self._video_class_terminal_types is None:
                self._parse_usbids()
            return self._video_class_terminal_types

    