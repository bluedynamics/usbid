USB devices and information API
===============================

This module helps to get infos for your connected usb devices, and find out
where they are mounted on your fs. it basically consists of two parts.

usbinfo
-------

Get information about USB-devices from identifiers based on the
`Linux USB information file <http://www.linux-usb.org/usb.ids>`_

In the data folder there is this file named ``usb.ids`` containing different
information about usb devices.

usage::
    
    >>> from usbid.usbinfo import USBINFO
    >>> USBINFO

On ``USBINFO`` the following properties are providing information

``usb_ids``
    dict of usbids with key as vendor id and value as a tuple
    consisting of vendor name and dict of key as device id and value
    as device name.

``device_classes``
    dict of device classes with key as class id and value as a tuple
    consisting of class name and dict of key as subclass id and value
    as a tuple consisting of subclass name and dict of key as protocol
    id and value as protocol name.

    example::

        '09': ('Hub',
            {'00': ('Unused',
                {'00': 'Full speed (or root) hub',
                 '01': 'Single TT',
                 '02': 'TT per port'})})

``audio_class_terminal_types``
    dict of audio class terminal types with key as terminal type and
    value as terminal name.

``hid_descriptor_types``
    dict of HID descriptor types with key as HID descriptor type and
    value as descriptor type name.

``hid_descriptor_item_types``
    dict of HID descriptor item types with key as item type and
    value as item type name.

``physical_descriptor_bias_types``
    dict of BIAS item types with key as BIAS item type and
    value as item type name.

``physical_descriptor_item_types``
    dict of PHY item types with key as PHY item type and
    value as item type name.

``hid_usages``
    dict of HID usages with key as HID id and value as a tuple
    consisting of  HID usage page name and a dict of key as hid usage
    and value as hid usage name (i.e. a ``Magic Carpet Simulation Device``).

``languages``
    dict of languages with key as language id and value as a tuple
    consisting of language name and a dict of key as dialect id and
    value as dialect name

``country_codes``
    dict of codes with key as code id and value as a tuple
    consisting of language name and a dict of key as dialect id and
    value as dialect name.

``video_class_terminal_types``
    dict of video class terminal types with key as terminal type and
    value as terminal type name.

For further details lookup the ``usbinfo.py`` and ``usbinfo.rst`` to see how
it can be used.


device
------

Devices are read from the Linux sys-fs. So this work only with Linux or any OS
that provides the same sys-fs. Its tested with Debian based systems like Ubuntu
and Linux-Mint and aims to work on Raspbian.

The USB devices are provides in a tree like they are connected to the computer.
Each USB root hub is an own tree in the virtual ``usb_roots()`` dict.
If another external hub is connected to the  root hub, it is a subtree as a
node of the root hub. Actual devices are the  leafs, i.e a mouse, keyboard,
serial adapter or magic carpet.

The roots object is a simple dict and all below are ``usbid.device.DeviceNode``
objects. A ``DeviceNode`` is itself a read-only dict-like object.

Example tree::

    .
    ├── 1 root hub A
    │   └── 1 external hub E1 
    │       ├── 1 Mouse
    │       ├── 2 Keyboard
    │       └── 3 Audio 
    │
    ├── 2 root hub B
    │   ├── 1 Magic Carpet
    │   └── 2 Hard Disk
    │ 
    └── 3 root hub C
        └── 1 external hub E2
            └── 1 external hub E3
                ├── 1 Serial Adapter S1 (ttyUSB1)
                └── 2 Serial Adapter S2 (ttyUSB0)    

Import::

    >>> from usbid.device import usb_roots
    
Get roots::
    
    >>> roots = usb_roots()

Fetch one device by path::    
    
    >>> serial_s2 = roots[3][1][2]

Look up info::

    >>> print serial_s2
    idProduct: 2303
    idVendor: 067b
    Product Name: PL2303 Serial Port
    Vendor Name: Prolific Technology, Inc.

    >>> serial_s2.idVendor
    067b

    >>> serial_s2.nameVendor
    Prolific Technology, Inc.

    >>> serial_s2.idProduct
    2303

    >>> serial_s2.nameProduct
    PL2303 Serial Port

Get the usb device path::

    >>> serial_s2.path
    [3, 1, 2]
    
Its also possible to traverse up::

    >>> serial_s2.parent.path
    [3, 1]

Check if its a root hub:: 

    >>> serial_s2.is_root
    False
    
    >>> roots[0].is_root
    True
    
A special case is built in for serial devices. The number and type of a tty
is assigned in plugin order. So a serial device named ``/dev/ttyUSB0`` can be
next time ``/dev/ttyUSB1`` if there are two almost same device are connected.

As a human you now its connected to port 1 and port 2 of a usb hub. Now knowing
the ``path`` allows us to store this information in application logic.

``DeviceNode`` provides the actual name of the serial character device in the
system::   

    >>> serial_s2.tty
    ttyUSB0
    
In order ot make filtering of devices easier all devices are available as a
flat list::

     >>> from usbid.device import devicelist
     
This allows easy filtering i.e. by ``vendorId`` or for all available ttys as
shown here::       

    >>> ttys = [_ for _ in devicelist() if _.tty]


For testing purposes there is a ``mocktree.tgz`` inside the data folder,
which acts like like a real linux sys-fs filesystem with several usb devices
connected.

Lookup the ``device.py`` and ``device.rst`` to get a deeper insight.


Source Code
===========

The sources are in a GIT DVCS with its main branches at
`github <http://github.com/bluedynamics/usbid>`_.

We'd be happy to see many forks and pull-requests to make usbid even better.

Contributors
============

- Jens W. Klein <jens@bluedynamics.com>
- Benjamin Stefaner <bs@kleinundpartner.at>
- Robert Niederreiter <rnix@squarewave.at>
