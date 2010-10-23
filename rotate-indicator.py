#!/usr/bin/python

import gobject
import gtk
import appindicator
import os
import subprocess

import dbus
import dbus.service
import dbus.mainloop.glib

from librotate import AutoRotateController,AutoRotateDaemonMonitor
import xrandr

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True);

class rotateindicator:
    controller=AutoRotateController.AutoRotateController(dbus.SystemBus(),"/rotate");
    monitor=AutoRotateDaemonMonitor.AutoRotateDaemonMonitor(dbus.SystemBus(),"/rotate");
    auto_menu_item = gtk.MenuItem("  Automatic")
    daemon_menu_item=gtk.MenuItem("Auto-Rotate Daemon");

    def setRotation(self,widget,direction):
        codes={"Normal":xrandr.RR_ROTATE_0,
	       "Left":xrandr.RR_ROTATE_90,
	       "Inverted":xrandr.RR_ROTATE_180,
	       "Right":xrandr.RR_ROTATE_270};
        self.controller.setRotation(codes[direction]);

    def refreshLabels(self):
        if(self.monitor.isDaemonRunning()):
            self.daemon_menu_item.set_label("Stop Auto-Rotate Daemon")
            self.auto_menu_item.set_sensitive(1);
        else:
            self.daemon_menu_item.set_label("Start Auto-Rotate Daemon")
            self.auto_menu_item.set_sensitive(0);

    def startStopDaemon(self,widget):
        if(self.monitor.isDaemonRunning()):
            self.monitor.killDaemon();
        else:
            os.system("auto-rotate.py -d");

    def serviceCheck(self,name):
        self.refreshLabels();
        
    def __init__(self):
        # Setup some callbacks to update the status of the buttons
        self.monitor.daemon_status_callback=self.serviceCheck;

        ind = appindicator.Indicator ("autorotate-client", "gsd-xrandr", appindicator.CATEGORY_APPLICATION_STATUS)
        ind.set_status (appindicator.STATUS_ACTIVE)
        ind.set_attention_icon ("indicator-messages-new")
        
        # create a menu
        menu = gtk.Menu()

        rotate_submenu = gtk.Menu();
        rotate_item=gtk.MenuItem("Rotate Screen")
        rotate_item.show()
        menu.append(rotate_item);

        # create some labels for the normal rotations
        directions=["Normal","Left","Inverted","Right"];
        for direction in directions:
            menu_item = gtk.MenuItem("  "+direction)
            menu.append(menu_item)
            menu_item.connect("activate",self.setRotation,direction)
            # show the items
            menu_item.show()
        
        # Add button to enable automatic rotation
        menu.append(self.auto_menu_item)
        self.auto_menu_item.connect("activate",self.setRotation,direction)
        self.auto_menu_item.show()

        # Autorotate configuration menu
        separator_item1=gtk.SeparatorMenuItem();
        separator_item1.show();
        menu.append(separator_item1);
            
        self.daemon_menu_item.connect("activate",self.startStopDaemon);
        menu.append(self.daemon_menu_item);
        self.daemon_menu_item.show();

        # Run the indicator!
        ind.set_menu(menu)

        gtk.main()

main=rotateindicator()
