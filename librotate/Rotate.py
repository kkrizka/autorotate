##
## libautorotate.py
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

from xrandr import xrandr

class Rotate:
    def __init__(self):
        screen=xrandr.get_current_screen();

    def GetRotation(self):
        return self.screen.get_current_rotation();

    def SetRotation(self,rotation):
        # There is not point in resetting and existing rotation
        if(rotation!=self.screen.get_current_rotation()): 
            self.screen.set_rotation(rotation);
            self.screen.apply_config();
            self.rotateWacom(rotation);
            self.rotateButtons(rotation);

    def SetNextRotation(self):
        current_rotation=self.GetRotation();

        # The codes go up as powers of two: 1,2,4,8
        #so we log2 it and increment by 1.
        next_rotation=int((math.log(current_rotation)/math.log(2)+1)%4);
        
        self.SetRotation(2**next_rotation);
