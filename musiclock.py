#!/usr/bin/python
"""
Toggles the pause button for Clementine on screensaver lock/unlock.

Inspired from: 
 https://code.google.com/p/clementine-player/wiki/MPRIS

"""

import time
import gtk
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

dbus_loop = DBusGMainLoop()
session_bus = dbus.SessionBus(mainloop = dbus_loop)

player = session_bus.get_object('org.mpris.clementine','/Player')
clementine = dbus.Interface(player, dbus_interface='org.freedesktop.MediaPlayer')

paused = False

def screensaverLocked():
	global clementine, paused
	print "Screensaver locked"
	playback, two, three, four = clementine.GetStatus()
	if playback == 0:
		print "Clementine found playing... pausing"
		clementine.Pause()
		paused = True

def screensaverUnlocked():
	global clementine, paused
	print "Screensaver unlocked" 	
	if paused:
		print "Clementine playback resumed..."
		clementine.Pause()
		paused = False

def screensaver(locked):
	global clementine, paused
	if locked:
		screensaverLocked()
	else:
		screensaverUnlocked()

session_bus.add_signal_receiver(screensaver, dbus_interface='org.gnome.ScreenSaver')

gtk.main()
