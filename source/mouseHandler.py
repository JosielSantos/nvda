#mouseHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import pyHook
import core
import api
import debug
import audio
import NVDAObjects
import globalVars
import config

#Internal mouse event

def internal_mouseEvent(event):
	if not config.conf["mouse"]["reportObjectUnderMouse"]:
		return True
	try:
		if event.MessageName=="mouse move":
			core.executeFunction(core.EXEC_MOUSE,executeMouseMoveEvent,event.Position[0],event.Position[1])
		elif event.MessageName.endswith("down"):
			core.executeFunction(core.EXEC_SPEECH,audio.cancel)
		return True
	except:
		debug.writeException("mouseHandler.internal_mouseEvent")

def executeMouseMoveEvent(x,y):
	obj=NVDAObjects.IAccessible.getNVDAObjectFromPoint(x,y)
	if not obj:
		return
	if obj==api.getFocusObject():
		mouseObject=api.getFocusObject()
		globalVars.mouseObject=None
	elif obj==globalVars.mouseObject: 
		mouseObject=globalVars.mouseObject
	else:
		globalVars.mouseObject=mouseObject=obj
	if hasattr(mouseObject,"event_mouseMove"):
		try:
			mouseObject.event_mouseMove(x,y,globalVars.mouseOldX,globalVars.mouseOldY)
		except:
			debug.writeException("api.notifyMouseMoved")
	globalVars.mouseOldX=x
	globalVars.mouseOldY=y

#Register internal mouse event

def initialize():
	hookManager=pyHook.HookManager()
	hookManager.MouseAll=internal_mouseEvent
	hookManager.HookMouse()
