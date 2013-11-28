
infos
=====

::

Dealing with multiple identical devices

Sometimes you may have two identical devices connected to the computer. How can 
you differentiate them? Device objects come with two additional attributes which 
are not part of the USB Spec, but are very useful: bus and address attributes. 
First of all, it is worth to say that these attributes come from the backend 
and a backend is free to not support them, in which case they are set to None. 
That said, these attributes represent the bus number and bus address of the device 
and, as you might already have imagined, can be used to differentiate two devices 
with the same idVendor and idProduct attributes.





Robert Niederreiter: und was von den angaben definiert den physikalischen anschluss?
Robert Niederreiter: bus, address, port?
Robert Niederreiter: was da drauf jetzt noch fehlt ist eben das zugewiesenen character device
da funky bennybunny: muss mas no anschaun, des woa ja task 2 =)  also i tip schwar das bus + adress des is
Robert Niederreiter: steck den hub mal aus und wieder ein
Robert Niederreiter: bzw verwende andere anschlüsse, dann siehst eh was sich ändert
Robert Niederreiter: ich tipp mal fast auf port und address
da funky bennybunny: passt da des wenn i afs device und bei da ausgabe, iatz no da was bastel das er eben charakterdevice a glei findet und als property draufpack bzw ausgib?
Robert Niederreiter: eine property function wäre gut, die das on access ausliest
Robert Niederreiter: weil ich das sogar wenns ganz blöd her geht im laufenden betrieb ändern kann
Robert Niederreiter: z.b. wenn ein solcher converter abkackt im laufenden prozess, und dann wieder connected dann bekommt er ein neues character device
da funky bennybunny: des weat iatz bisl trickier aba passt i schau wia weit i kim. ja propertys sein via sowas alm feini =)
Robert Niederreiter: glaub ich gar nicht das das tricky wird
Robert Niederreiter: das device hast ja
Robert Niederreiter: und du brauchst das gerechnete ergebnis einfach nicht auf der wrapper instanz speichern, sondern einfach wenn das property aufgerufen wird immer neu vom device lesen
da funky bennybunny: okay,na tua i mal basteln xD so iatz hab i wida infos iatz lass i di wida =)



in shell dmesg is intressant



I'm no expert in this field, but these are my interpretation of those numbers:

/devices/pci0000:00/0000:00:0f.5/usb1/1-3/1-3.1/1-3.1.1/1-3.1.1:1.0/ttyUSB0

    pci0000:00: This is your PCI controller.
    0000:00:0f.5: This is the PCI identifier of your USB controller.
    usb1: The usb controller itself.
    1-3: The identifier of the USB hub. It may be an internal hub, or it may be absent.
    1-3.1: Device connected to the first port of that hub.
    1-3.1:1.0: Configuration #1, Interface #0 in that device.

So, my guess is that the physical port is identified by 1-3.1, that is the string to the left of the colon in the last piece of the device path.

I don't have a hub around but I'd bet that if you connect it via a hub you'll get something like:



The physical port would be 1-3.1.1, and that last 1 would be the port used in that hub.



#attr for keyboard deviceobject 
'address',
'attach_kernel_driver',
'bDescriptorType',
'bDeviceClass',
'bDeviceProtocol',
'bDeviceSubClass',
'bLength',
'bMaxPacketSize0',
'bNumConfigurations',
'bcdDevice',
'bcdUSB',
'bus',
'ctrl_transfer',
'default_timeout',
'detach_kernel_driver',
'get_active_configuration',
'iManufacturer',
'iProduct',
'iSerialNumber',
'idProduct',
'idVendor',
'is_kernel_driver_active',
'port_number',
'read',
'reset',
'set_configuration',
'set_interface_altsetting',
'write'






