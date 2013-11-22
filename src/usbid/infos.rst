
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


