USB file system abstraction API
===============================

This module provides a USB file system abstraction API which can be used
to gain information of the physical USB bus structure on a Linux System.

.. note::

    Version 2.0 of this package is a complete rewrite. If you are using version
    1.0.x of this package, you're encouraged adopting the new API.


The USB file system (Taken from http://www.linux-usb.org/FAQ.html)
------------------------------------------------------------------

::

    # ls  /sys/bus/usb/devices/
    1-0:1.0      1-1.3        1-1.3.1:1.0  1-1:1.0
    1-1          1-1.3.1      1-1.3:1.0    usb1

The names that begin with "usb" refer to USB controllers. More accurately, they
refer to the "root hub" associated with each controller. The number is the USB
bus number. In the example there is only one controller, so its bus is number
1. Hence the name "usb1".

"1-0:1.0" is a special case. It refers to the root hub's interface. This acts
just like the interface in an actual hub an almost every respect; see below.

All the other entries refer to genuine USB devices and their interfaces.
The devices are named by a scheme like this::

    bus-port.port.port ...

In other words, the name starts with the bus number followed by a '-'. Then
comes the sequence of port numbers for each of the intermediate hubs along the
path to the device.

For example, "1-1" is a device plugged into bus 1, port 1. It happens to be a
hub, and "1-1.3" is the device plugged into port 3 of that hub. That device is
another hub, and "1-1.3.1" is the device plugged into its port 1.

The interfaces are indicated by suffixes having this form::

    :config.interface

That is, a ':' followed by the configuration number followed by '.' followed
by the interface number. In the above example, each of the devices is using
configuration 1 and this configuration has only a single interface, number 0.
So the interfaces show up as::

    1-1:1.0        1-1.3:1.0        1-1.3.1:1.0

A hub will never have more than a single interface; that's part of the USB
spec. But other devices can and do have multiple interfaces (and sometimes
multiple configurations). Each interface gets its own entry in sysfs and can
have its own driver.


Usage
=====

The API consists of a USB root object, from which all children can be accessed
like python container types.

.. code-block:: pycon

    >>> from usbid import USB
    >>> usb = USB()
    >>> usb
    <usbid.fs.USB [/sys/bus/usb/devices] at ...>

    >>> usb.keys()
    ['1', '2']

Get a specific bus.

.. code-block:: pycon

    >>> bus = usb['1']
    >>> bus
    <usbid.fs.Bus [usb1] at ...>

Get port from bus.

.. code-block:: pycon

    >>> port = bus['1']
    >>> port
    <usbid.fs.Port [1-1] at ...>

Get interface from port.

.. code-block:: pycon

    >>> port.interfaces
    [<usbid.fs.Interface [1-1:1.0] at ...>]

Interfaces might have tty associated.

.. code-block:: pycon

    >>> port.interfaces[0].tty
    'ttyUSB0'

It's not a good idea to refer to a USB interface by its tty mount name. But
it's a good idea to remember the file system name for unique identification,
lookup interface by this name and then connect to corresponding tty.

.. code-block:: pycon

    >>> interface = usb.get_interface('1-1:1.0')
    >>> interface.tty
    'ttyUSB0'

For debugging you can print the USB structure.

.. code-block:: pycon

    >>> usb.printtree()
    <usbid.fs.USB [/sys/bus/usb/devices] at ...>
      <usbid.fs.Bus [usb1] at ...>
          - Linux 3.13.0-48-generic xhci_hcd
          - xHCI Host Controller
        <usbid.fs.Interface [1-0:1.0] at ...>
        <usbid.fs.Port [1-1] at ...>
            - FTDI
            - FT232R USB UART
          <usbid.fs.Interface [1-1:1.0] at ...>
            - ttyUSB0


Source Code
===========

The sources are in a GIT DVCS with its main branches at
`github <http://github.com/bluedynamics/usbid>`_.


Contributors
============

- Robert Niederreiter <rnix@squarewave.at>

- Jens W. Klein <jens@bluedynamics.com>

- Benjamin Stefaner <bs@kleinundpartner.at>
