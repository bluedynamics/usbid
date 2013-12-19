Tree of/ Info about Linux USB Device
====================================

This module helps to get infos for your connected usb devices, and find out
where they are mounted on your fs. it basically consists of two parts.

usbinfo
-------

Get information about USB-devices from identifiers based on the
`Linux USB information file <http://www.linux-usb.org/usb.ids>`_

In the data folder theres a file named ``usb.ids``, which contains the
information.

usage::
    
    from usbid import USBID

Lookup the ``usbinfo.py`` and ``usbinfo.rst`` to see how it can be used.


device
------

For testing theres a ``mocktree.tgz`` inside the data folder, which acts like
like  a real unix filesystem with several usb devices connected. Some of the
methods and properties use the usbinfo from above, to access infos for the
devices.

Lookup the ``device.py`` and ``device.rst`` to see how it can be used.

basically you just run this.
The default root_path is::
    root_path='/sys/bus/usb/devices'  
     
    ttys = [_ for _ in devicelist(root_path) if _.tty]


and afterwards print the info and fs path of the tty devices.
print info for first tty

::
    
    >>> print ttys[0]
    idProduct: 2303
    idVendor: 067b
    Product Name: PL2303 Serial Port
    Vendor Name: Prolific Technology, Inc. 


get filesystem path for the first tty

::
    >>> ttys[0].fs_path
    '.../sys/bus/usb/devices/usb2/2-1/2-1.2/2-1.2.1'


Source Code
===========

The sources are in a GIT DVCS with its main branches at
`github <http://github.com/bluedynamics/usbid>`_.

We'd be happy to see many forks and pull-requests to make usbid even better.

Contributors
============

- Jens W. Klein <jens@bluedynamics.com>
- Benjamin Stefaner <bs@kleinundpartner.at>
