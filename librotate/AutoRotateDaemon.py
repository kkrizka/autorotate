##
## libautorotate.py
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

import glib

import os,time,re,sys,stat;
import math;

import subprocess;

from xrandr import xrandr

from librotate import Rotate

class AutoRotateDaemon(dbus.service.Object):
    ## Setup important paths
    # Contains the calibration of the accelerometer
    caliPath='/sys/devices/platform/hdaps/calibrate';
    # Contains the position of the accelerometer
    accelPath='/sys/devices/platform/hdaps/position';
    # Contains the position of the screen
    # 0 - laptop mode
    # 1 - tablet mode
    tabletModePath='/sys/devices/platform/thinkpad_acpi/hotkey_tablet_mode';

    disabled=False;
    
    # Calibration
    xCal=0;
    yCal=0;

    # The last mode registered by autorotate
    currentMode='';

    # Codes for rotation
    rotate=Rotate.Rotate();

    def __init__(self,bus=0,object_path=''):
        if(bus!=0):
            dbus.service.Object.__init__(self,bus,object_path);

        # Setup calibration
        if(os.path.exists(self.caliPath)):
            cali_fh=open(self.caliPath,'r');
        else:
            self.log("Cannot find calibration file...");
            self.log("Make sure hdaps is loaded.");
            self.log("EXITING");
            exit(1);
            
        line=cali_fh.readline().replace("\n","").replace("\r","");
        m=re.search('.(-?[0-9]*),(-?[0-9]*).',line);
        self.xCal=int(m.group(1));
        self.yCal=int(m.group(2));



    @dbus.service.method("net.krizka.autorotate.IsDisabled",
                         in_signature='', out_signature='b')
    def IsDisabled(self):
        return self.disabled;

    @dbus.service.method("net.krizka.autorotate.SetDisabled",
                         in_signature='b', out_signature='')
    def SetDisabled(self,disabled):
        self.disabled=disabled;

    @dbus.service.method("net.krizka.autorotate.GetMode",
                         in_signature='', out_signature='s')
    def GetMode(self):
        return self.currentMode;

    @dbus.service.method("net.krizka.autorotate.GetRotation",
                         in_signature='', out_signature='i')
    def GetRotation(self):
        return self.rotate.GetRotation();

    @dbus.service.method("net.krizka.autorotate.SetRotation",
                         in_signature='i', out_signature='')
    def SetRotation(self,rotation):
        self.rotate.SetRotation();

    @dbus.service.method("net.krizka.autorotate.SetNextRotation",
                         in_signature='', out_signature='')
    def SetNextRotation(self):
        self.rotate.SetNextRotation();
        self.SetDisabled(True); # Disable automatic rotation

    def log(self,txt):
        pass;
	#print "Autorotate: "+txt

    # This code is run every 2 seconds
    def run(self):
        try:
            # Check mode
            if(os.path.exists(self.tabletModePath)):
                tabletmode_fh=open(self.tabletModePath,'r');
            else:
                self.log("Cannot find tablet-mode file... "+self.tabletModePath);
                return True;

            line=tabletmode_fh.readline();
            line=line.strip();
            if(line=='0'):
                mode='laptop';
            else:
                mode='tablet';

            self.log("Mode: "+mode+" Disabled: "+str(bool(self.IsDisabled())))
            if(mode == "tablet" and self.disabled==False):
                #Tabled mode, open position file...
                accel_fh=open(self.accelPath,'r')
                
                line=accel_fh.readline()
                m=re.search('.(-?[0-9]*),(-?[0-9]*).',line)
                if(m.lastindex!=2): # If there weren't two matches, something is wrong!
                    self.log("Not enough matches, skipping iteration")
                    return True

                #Find position, after calibration
                x=int(m.group(2))+self.xCal
                y=int(m.group(1))+self.yCal
                self.log("pos x: "+str(m.group(2))+" y:"+str(m.group(1)))
                self.log("cal x: "+str(self.xCal)+" y:"+str(self.yCal))
                self.log("res x: "+str(x)+" y:"+str(y))

                # Sensityvity setting. Only rotate if above this treshhold
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
                        nextMode=xrandr.RR_ROTATE_270
                    else:
                        nextMode=xrandr.RR_ROTATE_90
                else:
                    if(x<0):
                        nextMode=xrandr.RR_ROTATE_0
                    else:
                        nextMode=xrandr.RR_ROTATE_180

                self.SetRotation(nextMode);
            elif(self.currentMode=='tablet' and mode=='laptop'):
                # Go back to laptop mode
                self.SetRotation(xrandr.RR_ROTATE_0)
                self.SetDisabled(False)

            # Update current mode
            self.currentMode=mode;
                            
        except:
            print "Unexpected error: ",sys.exc_info()[0]
            raise

        return True;
