##
## AutoRotateDaemonMonitor.py
## Karol Krizka <kkrizka@gmail.com>
## Started on  Sun Oct 14 14:28:20 2010 Karol Krizka
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

import xrandr

import dbus

class AutoRotateDaemonMonitor:
    object_path = "/remote";
    daemon_status_callback=0;

    def __init__(self,bus=0,object_path=''):
        self.bus=bus;
        self.object_path=object_path;
        
        bus.watch_name_owner("net.krizka.autorotate",self.handleDaemonStatus);

    def handleDaemonStatus(self,name):
        if(self.daemon_status_callback):
            self.daemon_status_callback(name);

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

    def killDaemon(self):
        if(not self.isDaemonRunning()):
            return; # Cannot kill a non existent daemon
        
        remote_state=self.bus.get_object("net.krizka.autorotate",self.object_path);
        remote_state.kill(dbus_interface = "net.krizka.autorotate.kill");
