#!/usr/bin/python
##
## tabletinfo.py
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

import dbus

from librotate import TabletInfo

def main():
    info=TabletInfo.TabletInfo()
    print "Information About Your Tablet"
    print "Tablet Mode: %s"%info.getTabletMode()
    print ""
    availableAccelerometers=info.listAvailableAccelerometers()
    print "ACCELEROMETERS"
    for accel in info.listSupportedAccelerometers():
        availString="Not Available"
        if(accel in availableAccelerometers):
            availString="Available"

        print "Name: %s\t%s"%(accel,availString)
        if(accel in availableAccelerometers):
            info.setAccelerometer(accel);
            print "\tCalibration File: %s"%info.caliPath
            print "\tOrientation File: %s"%info.accelPath
            print "\tCalibration: (%d,%d)"%(info.xCal,info.yCal)
            print "\tRaw Orientation: (%d,%d)"%info.getAccelerometerRawOrientation()
            print "\tCalibrated Orientation: (%d,%d)"%info.getAccelerometerOrientation()



main()
