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

from librotate import AutoRotateController
from librotate import TabletInfo

def main():
    system_bus = dbus.SystemBus()

    controller=AutoRotateController.AutoRotateController(system_bus,"/rotate");
    
    controller.setNextRotation();

main()

