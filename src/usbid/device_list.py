
              
    def get_connected_devices(self):
        self.devices = usb.core.find(find_all=True)
        return self.devices



    def get_info(self):
        print 'Found %i devices' % len(self.devices)
        
        for dev in self.devices:
            # ignore hubs
            if dev.bDeviceClass == 9:
                continue
            
            #deviceinfo method aufrufen