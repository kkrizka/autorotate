##
## Rotate.py
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

import subprocess
import os
import math

import xrandr

class Rotate:
    screen=xrandr.get_current_screen();

    def getRotation(self):
        return self.screen.get_current_rotation();

    def setRotation(self,rotation):
        # There is not point in resetting and existing rotation
        if(rotation!=self.screen.get_current_rotation()): 
            self.screen.set_rotation(rotation);
            self.screen.apply_config();
            self.rotateWacom(rotation);
            self.rotateButtons(rotation);

    def setNextRotation(self):
        current_rotation=self.getRotation();

        # The codes go up as powers of two: 1,2,4,8
        #so we log2 it and increment by 1.
        next_rotation=int((math.log(current_rotation)/math.log(2)+1)%4);
        
        self.setRotation(2**next_rotation);

    def listDevices(self):
        process=subprocess.Popen(["xsetwacom","--list"],stdout=subprocess.PIPE)
        process.wait()

        devices=[]
        for line in process.stdout:
            line=line.strip();
            # Line has format "device name with spaces TYPE"
            # We do not want the TYPE part..
            parts=line.split(' ');
            dev_type=parts.pop();
            dev_name=' '.join(parts);
            devices.append(dev_name)

        return devices

        # Correct the rotation of the stylus input
    def rotateWacom(self,rotation):
	codes={xrandr.RR_ROTATE_0:"none",
	       xrandr.RR_ROTATE_90:"ccw",
	       xrandr.RR_ROTATE_180:"half",
	       xrandr.RR_ROTATE_270:"cw"};
	for i in self.listDevices():
            os.system("xsetwacom set \""+i+"\" Rotate "+codes[rotation]);

    # Correct the rotation of the arrow buttons.
    def rotateButtons(self,rotation):
        keysim=["71","6d","6f","6e"];
        keycodes={xrandr.RR_ROTATE_0:[105,108,106,103],
                  xrandr.RR_ROTATE_90:[103,105,108,106],
                  xrandr.RR_ROTATE_180:[106,103,105,108],
                  xrandr.RR_ROTATE_270:[108,106,103,105]};
	for i in keysim:
            toCode=keycodes[rotation].pop();
            os.system("setkeycodes "+str(i)+" "+str(toCode));
