#!/usr/bin/python
##
## auto-rotate.py
## Karol Krizka <kkrizka@gmail.com>
## Started on  Sat Jun 14 16:05:48 2008 Karol Krizka
## $Id$
## 
## Copyright (C) 2008 Karol Krizka
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##

from librotate import AutoRotateDaemon

import os,time,re,sys,stat;
from xrandr import xrandr

import dbus
import dbus.service
import dbus.mainloop.glib

import gobject

def main():
    # Setup DBus connection for remote control
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    system_bus = dbus.SystemBus()

    system_services = system_bus.list_names()
    if(not "net.krizka.autorotate" in system_services): # Don't bother starting several instances of the autorotate daemon
        busname = dbus.service.BusName("net.krizka.autorotate",system_bus);
        
        autorotate=AutoRotateDaemon.AutoRotateDaemon(system_bus,"/rotate")
        
        # Start loop
        glib.timeout_add(2000,autorotate.run)
        
        mainloop = gobject.MainLoop()
        mainloop.run()

main()
