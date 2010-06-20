##
## TabletInfo.py
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

import os.path
import re

class TabletInfo:
    ## Tablet Paths
    # Contains the position of the screen
    # 0 - laptop mode
    # 1 - tablet mode
    tabletModePath='/sys/devices/platform/thinkpad_acpi/hotkey_tablet_mode'
    
    ## Accelerometer Related Variables
    # The driver Being used
    accelerometer='hdaps'
    # Contains the calibration of the accelerometer
    caliPath='/sys/devices/platform/hdaps/calibrate';
    # Contains the position of the accelerometer
    accelPath='/sys/devices/platform/hdaps/position';
    # Calibration
    xCal=0
    yCal=0

    def __init__(self):
        supportedAccelerometers=self.listSupportedAccelerometers()
        if(len(supportedAccelerometers)>0):
            self.setAccelerometer(supportedAccelerometers[0]);
        
    def listSupportedAccelerometers(self):
        return ['hdaps'];

    def listAvailableAccelerometers(self):
        supported=self.listSupportedAccelerometers();
        available=[];
        for accel in supported:
            if(os.path.exists('/sys/devices/platform/'+accel+'/position')):
                available.append(accel);
        return available;

    def setAccelerometer(self,accel):
        self.accelerometer=accel;
        self.accelPath='/sys/devices/platform/'+accel+'/position'
        self.caliPath='/sys/devices/platform/'+accel+'/calibrate'
        self.calibrateAccelerometer()

    def getAccelerometerCalibration(self):
        return self._readAccelerometerCoordinates(self.caliPath)
    
    def getAccelerometerRawOrientation(self):
        return self._readAccelerometerCoordinates(self.accelPath)

    def getAccelerometerOrientation(self):
        (x,y)=self.getAccelerometerRawOrientation()
        return (x-self.xCal,y-self.yCal);

    def calibrateAccelerometer(self):
        (self.xCal,self.yCal)=self.getAccelerometerCalibration()

    def getTabletMode(self):
        if(not os.path.exists(self.tabletModePath)):
            return "laptop"
        
        tabletmode_fh=open(self.tabletModePath,'r')
        line=tabletmode_fh.readline().strip();
        if(line=='0'):
            mode='laptop';
        else:
            mode='tablet';
        return mode


    ## Private functions
    def _readAccelerometerCoordinates(self,path):
        if(not os.path.exists(path)):
            return (0,0)
        fh=open(path,"r")
        line=fh.readline().replace("\n","").replace("\r","");
        m=re.search('.(-?[0-9]*),(-?[0-9]*).',line);
        x=int(m.group(1));
        y=int(m.group(2));
        return (x,y);

        
