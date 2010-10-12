##
## AutoRotateController.py
## Karol Krizka <kkrizka@gmail.com>
## Started on  Sun Jun 13 10:40:30 2010 Karol Krizka
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

from . import Rotate
from . import TabletInfo

import xrandr

import dbus
import pynotify

class AutoRotateController:
    rotate=Rotate.Rotate();
    tabletinfo=TabletInfo.TabletInfo();
    object_path = "/remote";
    notify_enabled=pynotify.init("Manual Rotation");

    def __init__(self,bus=0,object_path=''):
        self.bus=bus;
        self.object_path=object_path;

    def isDaemonRunning(self):
        system_services = self.bus.list_names();
        return ("net.krizka.autorotate" in system_services);

    def isDaemonDisabled(self):
        if(not self.isDaemonRunning()):
            return False;
        else:
            remote_state=bus.get_object("net.krizka.autorotate",self.object_path)
            return remote_state.isDisabled(dbus_interface = "net.krizka.autorotate.isDisabled");

    def setDaemonDisabled(self,disabled):
        if(not self.isDaemonRunning()):
            return;
        else:
            remote_state=bus.get_object("net.krizka.autorotate",self.object_path);
            remote_state.setDisabled(disabled,dbus_interface = "net.krizka.autorotate.setDisabled");

    def getRotation(self):
        if(not self.isDaemonRunning()):
            return self.rotate.getRotation();
        else:
            remote_state=bus.get_object("net.krizka.autorotate",self.object_path)
            return remote_state.getRotation(dbus_interface = "net.krizka.autorotate.getRotation");

    def setRotation(self,rotation):
        if(not self.isDaemonRunning()):
            self.rotate.setRotation(rotation);
        else:
            remote_state=bus.get_object("net.krizka.autorotate",self.object_path)
            remote_state.setRotation(rotation,dbus_interface = "net.krizka.autorotate.setRotation");

    def setNextRotation(self):
        if(not self.isDaemonRunning()):
            self.rotate.setNextRotation();
        else:
            remote_state=bus.get_object("net.krizka.autorotate",self.object_path)
            mode=self.tabletinfo.getTabletMode();
            if(mode=='laptop'):
                if(self.notify_enabled):
                    pynotify.Notification("Screen is in laptop mode, rotation is disabled","","dialog-error").show();
                return;

            disabled=self.isDaemonDisabled();
            rotation=self.getRotation()
            # After we reach 180 and we are in manual rotation, we want to go back to automatic rotation
            if(rotation==xrandr.RR_ROTATE_180 and disabled==True):
                self.setDaemonDisabled(False)
                if(self.notify_enabled):
                    pynotify.Notification("Enabling automatic rotation","","video-display").show();
            else: # Otherwise go to next rotation in list
                remote_state.setNextRotation(dbus_interface = "net.krizka.autorotate.setNextRotation");
                self.setDaemonDisabled(True); # Disable automatic rotation
                if(self.notify_enabled):
                    pynotify.Notification("Disabling automatic rotation","","video-display").show();
