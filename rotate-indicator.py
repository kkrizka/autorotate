#!/usr/bin/python

import gobject
import gtk
import appindicator
import dbus

from librotate import AutoRotateController
import xrandr

class rotateindicator:
    controller=AutoRotateController.AutoRotateController(dbus.SystemBus(),"/rotate");

    def setRotation(self,widget,direction):
        codes={"Normal":xrandr.RR_ROTATE_0,
	       "Left":xrandr.RR_ROTATE_90,
	       "Inverted":xrandr.RR_ROTATE_180,
	       "Right":xrandr.RR_ROTATE_270};
        self.controller.setRotation(codes[direction]);

    def __init__(self):
        ind = appindicator.Indicator ("autorotate-client", "gsd-xrandr", appindicator.CATEGORY_APPLICATION_STATUS)
        ind.set_status (appindicator.STATUS_ACTIVE)
        ind.set_attention_icon ("indicator-messages-new")
        
        # create a menu
        menu = gtk.Menu()

        rotate_submenu = gtk.Menu();
        rotate_item=gtk.MenuItem("Rotate Screen")
        rotate_item.show()
        menu.append(rotate_item);

        # create some labels
        directions=["Normal","Left","Inverted","Right"];
        for direction in directions:
            menu_item = gtk.MenuItem("  "+direction)
            menu.append(menu_item)
            menu_item.connect("activate",self.setRotation,direction)
            # show the items
            menu_item.show()

        separator_item1=gtk.SeparatorMenuItem();
        separator_item1.show();
        menu.append(separator_item1);
            
        autorotate_item=gtk.MenuItem("Auto-Rotate Daemon");
        if(self.controller.isDaemonRunning()):
            autorotate_item.set_label("Automatic")
        else:
            autorotate_item.set_label("Stard Auto-Rotate Daemon")
        autorotate_item.show();
        menu.append(autorotate_item);
        
        ind.set_menu(menu)

        gtk.main()

main=rotateindicator()
