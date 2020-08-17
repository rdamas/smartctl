# -*- coding: utf-8 -*-

from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.MenuList import MenuList
from Screens.Screen import Screen
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import resolveFilename, SCOPE_PLUGINS

from enigma import eListboxPythonMultiContent, gFont, BT_SCALE

import skin

from .Discover import Discover
from .SmartDevice import SmartDevice

def DevicesEntryComponent(device):
    png = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/SmartControl/icons/device.png"))
    x,y,w,h = (120,5,480,32)
    x1,y1,w1,h1 = (120,50,480,28)
    x2,y2,w2,h2 = (5,5,100,100)

    return [
        device,
        MultiContentEntryText(pos=(x, y), size=(w, h), font=0, text=device["name"]),
        MultiContentEntryText(pos=(x1, y1), size=(w1, h1), font=1, text=device["model"]),
        MultiContentEntryPixmapAlphaTest(pos=(x2, y2), size=(w2, h2), options = BT_SCALE, png = png)
    ]

class DevicesList(MenuList):
    def __init__(self, list, enableWrapAround=False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        font = skin.fonts.get("PluginBrowser0", ("Regular", 20, 50))
        self.l.setFont(0, gFont(font[0], font[1]))
        self.l.setItemHeight(115)
        font = skin.fonts.get("PluginBrowser1", ("Regular", 14))
        self.l.setFont(1, gFont(font[0], font[1]))


class Devices(Screen):
    skin = """
    <screen name="SmartControlDevices" position="0,0" size="1920,1080" title="[SmartControl] Festplatte auswählen" flags="wfNoBorder">
        <widget name="list" position="20,120" size="720,800" scrollbarWidth="10" scrollbarSliderBorderWidth="1" transparent="1" enableWrapAround="1" />
    </screen>
    """
    
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self.skinName = "SmartControlDevices"
        self["actions"] =  ActionMap(["ColorActions", "WizardActions"], {
                "back":        self.cancel,
                "ok":          self.ok,
        }, -1)
        
        self.list = []
        self["list"] = DevicesList(self.list)
        self.onLayoutFinish.append(self.updateList)

    def updateList(self):
        self.list = []
        self.deviceslist = Discover().devices()
        for device in self.deviceslist:
            self.list.append(DevicesEntryComponent(device))
        self["list"].l.setList(self.list)

    def cancel(self):
        self.close()

    def ok(self):
        selected = self["list"].l.getCurrentSelection()[0]
        if selected:
            self.session.open(SmartDevice, selected)

