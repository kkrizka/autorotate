##
## AutoRotateDaemon.py
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

import dbus
import dbus.service

import sys;
import math;

from xrandr import xrandr

from . import Rotate
from . import TabletInfo

class AutoRotateDaemon(dbus.service.Object):
    disabled=False;

    # Codes for tablet information
    tabletInfo=TabletInfo.TabletInfo();
    
    # The last mode registered by autorotate
    currentMode='';

    # Codes for rotation
    rotate=Rotate.Rotate();

    def __init__(self,bus=0,object_path=''):
        if(bus!=0):
            dbus.service.Object.__init__(self,bus,object_path);   

    @dbus.service.method("net.krizka.autorotate.isDisabled",
                         in_signature='', out_signature='b')
    def isDisabled(self):
        return self.disabled;

    @dbus.service.method("net.krizka.autorotate.setDisabled",
                         in_signature='b', out_signature='')
    def setDisabled(self,disabled):
        self.disabled=disabled;

    @dbus.service.method("net.krizka.autorotate.getMode",
                         in_signature='', out_signature='s')
    def getMode(self):
        return self.currentMode;

    @dbus.service.method("net.krizka.autorotate.getRotation",
                         in_signature='', out_signature='i')
    def getRotation(self):
        return self.rotate.getRotation();

    @dbus.service.method("net.krizka.autorotate.setRotation",
                         in_signature='i', out_signature='')
    def setRotation(self,rotation):
        self.rotate.setRotation(rotation);

    @dbus.service.method("net.krizka.autorotate.setNextRotation",
                         in_signature='', out_signature='')
    def setNextRotation(self):
        self.rotate.setNextRotation();
        self.setDisabled(True); # Disable automatic rotation

    def log(self,txt):
	print "Autorotate: "+txt

    # This code is run every 2 seconds
    def run(self):
        try:
            # Check mode
            mode=self.tabletInfo.getTabletMode()

            self.log("Mode: "+mode+" Disabled: "+str(bool(self.isDisabled())))
            if(mode == "tablet" and self.disabled==False):
                #Tablet mode, get orientaiton
                (x,y)=self.tabletInfo.getAccelerometerOrientation();
                self.log("x: "+str(x)+" y:"+str(y))

                # Sensitivity setting. Only rotate if above this treshhold
                if(abs(x)<70 and abs(y)<70):
                    self.log(self.currentMode+" to "+mode)
                    # It is possible that we went into table mode while sitting at a desk.
                    # In that case, it is most convenient to rotate the screen so bottom is still facing the user
                    if(self.currentMode=='laptop' and mode=='tablet'): # we switched modes!
                        nextMode=xrandr.RR_ROTATE_180
                    else:
                        return True;
                elif(abs(y)>abs(x)):
                    if(y>0):
                        nextMode=xrandr.RR_ROTATE_180
                    else:
                        nextMode=xrandr.RR_ROTATE_0
                else:
                    if(x<0):
                        nextMode=xrandr.RR_ROTATE_90
                    else:
                        nextMode=xrandr.RR_ROTATE_270

                self.setRotation(nextMode);
            elif(self.currentMode=='tablet' and mode=='laptop'):
                # Go back to laptop mode
                self.setRotation(xrandr.RR_ROTATE_0)
                self.setDisabled(False)

            # Update current mode
            self.currentMode=mode;
                            
        except:
            print "Unexpected error: ",sys.exc_info()[0]
            raise

        return True;
