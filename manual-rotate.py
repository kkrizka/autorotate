#!/usr/bin/python
##
## manual-rotate.py
## Karol Krizka <kkrizka@gmail.com>
## Started on  Sat Jun 14 16:35:55 2008 Karol Krizka
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

import sys
import dbus
import pynotify
from traceback import print_exc

from libautorotate import *

def main():
    system_bus = dbus.SystemBus()
    system_services = system_bus.list_names()

    # Attempt to contact auto-rotate.py on the system bus. If it fails, just perform manual rotation
    if("net.krizka.autorotate" in system_services):
        remote_state = system_bus.get_object("net.krizka.autorotate",
                                             "/rotate")

        # Connect to notification daemon, if possible
        notify_enabled=pynotify.init("Manual Rotation");
        
        # you can either specify the dbus_interface in each call...
        mode = remote_state.GetMode(dbus_interface = "net.krizka.autorotate.GetMode");
        if(mode=='laptop'): # Don't do anything in laptop mode
            if(notify_enabled):
                pynotify.Notification("Screen is in laptop mode, rotation is disabled","","dialog-error").show();
            return;

        rotation=remote_state.GetRotation(dbus_interface = "net.krizka.autorotate.GetRotation");
        disabled=remote_state.IsDisabled(dbus_interface = "net.krizka.autorotate.IsDisabled");

        # After we reach 180 and we are in manual rotation, we want to go back to automatic rotation
        if(rotation==xrandr.RR_ROTATE_180 and disabled==True):
            remote_state.SetDisabled(False,dbus_interface = "net.krizka.autorotate.SetDisabled");
            if(notify_enabled):
                pynotify.Notification("Enabling automatic rotation","","video-display").show();
        else: # Otherwise go to next rotation in list
            remote_state.SetNextRotation(dbus_interface = "net.krizka.autorotate.SetNextRotation");
            if(notify_enabled and disabled==False):
                pynotify.Notification("Disabling automatic rotation","","video-display").show();

    else:
        # No autorotate service, meaning that we rotate the screen manually..
        rotate=AutoRotate();
        rotate.SetNextRotation();

main()
