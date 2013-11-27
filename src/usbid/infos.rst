
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





[09:46:52] Robert Niederreiter: und was von den angaben definiert den physikalischen anschluss?
[09:47:10] Robert Niederreiter: bus, address, port?
[09:47:33] Robert Niederreiter: was da drauf jetzt noch fehlt ist eben das zugewiesenen character device
[09:48:04] da funky bennybunny: muss mas no anschaun, des woa ja task 2 =)  also i tip schwar das bus + adress des is
[09:48:36] Robert Niederreiter: steck den hub mal aus und wieder ein
[09:48:57] Robert Niederreiter: bzw verwende andere anschlüsse, dann siehst eh was sich ändert
[09:49:07] Robert Niederreiter: ich tipp mal fast auf port und address
[09:49:08] da funky bennybunny: passt da des wenn i afs device und bei da ausgabe, iatz no da was bastel das er eben charakterdevice a glei findet und als property draufpack bzw ausgib?
[09:50:20] Robert Niederreiter: eine property function wäre gut, die das on access ausliest
[09:50:45] Robert Niederreiter: weil ich das sogar wenns ganz blöd her geht im laufenden betrieb ändern kann
[09:51:51] Robert Niederreiter: z.b. wenn ein solcher converter abkackt im laufenden prozess, und dann wieder connected dann bekommt er ein neues character device
[09:52:10] da funky bennybunny: des weat iatz bisl trickier aba passt i schau wia weit i kim. ja propertys sein via sowas alm feini =)
[09:52:37] Robert Niederreiter: glaub ich gar nicht das das tricky wird
[09:52:41] Robert Niederreiter: das device hast ja
[09:53:19] Robert Niederreiter: und du brauchst das gerechnete ergebnis einfach nicht auf der wrapper instanz speichern, sondern einfach wenn das property aufgerufen wird immer neu vom device lesen
[09:55:30] da funky bennybunny: okay,na tua i mal basteln xD so iatz hab i wida infos iatz lass i di wida =)



in shell dmesg is intressant



 0 down vote accepted
    

I'm no expert in this field, but these are my interpretation of those numbers:

    pci0000:00: This is your PCI controller.
    0000:00:0f.5: This is the PCI identifier of your USB controller.
    usb1: The usb controller itself.
    1-3: The identifier of the USB hub. It may be an internal hub, or it may be absent.
    1-3.1: Device connected to the first port of that hub.
    1-3.1:1.0: Configuration #1, Interface #0 in that device.

So, my guess is that the physical port is identified by 1-3.1, that is the string to the left of the colon in the last piece of the device path.

I don't have a hub around but I'd bet that if you connect it via a hub you'll get something like:

/devices/pci0000:00/0000:00:0f.5/usb1/1-3/1-3.1/1-3.1.1/1-3.1.1:1.0/ttyUSB0

The physical port would be 1-3.1.1, and that last 1 would be the port used in that hub.
