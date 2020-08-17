# -*- coding: utf-8 -*-

from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Sources.List import List
from Screens.Screen import Screen

from .SmartInfo import SmartInfo

class SmartAttributes(Screen):
    skin = """
    <screen name="SmartControlAttributes" position="0,0" size="1920,1080" title="[SmartControl] Festplatte Attribute" flags="wfNoBorder">
        <widget render="Listbox" source="deviceinfo" enableWrapAround="0"
            position="0,100" size="1920,850" transparent="1"
            font="Regular;25" zPosition="5" scrollbarMode="showOnDemand"
            scrollbarSliderBorderWidth="0" scrollbarWidth="5">
            <convert type="TemplatedMultiContent">{
                "template": [
                    MultiContentEntryText(
                        pos = (10, 10),
                        size = (140, 50),
                        font = 0,
                        flags = RT_HALIGN_RIGHT | RT_VALIGN_CENTER,
                        text = 0),
                    MultiContentEntryText(
                        pos = (165, 10),
                        size = (500, 50),
                        font = 0,
                        flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER,
                        text = 1),
                    MultiContentEntryText(
                        pos = (670, 10),
                        size = (120, 50),
                        font = 0,
                        flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER,
                        text = 2),
                    MultiContentEntryText(
                        pos = (795, 10),
                        size = (220, 50),
                        font = 0,
                        flags = RT_HALIGN_RIGHT | RT_VALIGN_CENTER,
                        text = 3),
                    MultiContentEntryText(
                        pos = (1030, 10),
                        size = (240, 50),
                        font = 0,
                        flags = RT_HALIGN_RIGHT | RT_VALIGN_CENTER,
                        text = 4),
                    MultiContentEntryText(
                        pos = (1285, 10),
                        size = (240, 50),
                        font = 0,
                        flags = RT_HALIGN_RIGHT | RT_VALIGN_CENTER,
                        text = 5),
                    MultiContentEntryText(
                        pos = (1550, 10),
                        size = (365, 50),
                        font = 0,
                        flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER,
                        text = 6)
                    ],
                "fonts": [gFont("Regular", 36)],
                "itemHeight": 50 }
            </convert>
        </widget>
    </screen>
    """
    
    def __init__(self, session, smartinfo):
        self.session = session
        Screen.__init__(self, session)
        self.skinName = "SmartControlAttributes"
        self["actions"] =  ActionMap(["ColorActions", "WizardActions"], {
                "back": self.cancel,
                "ok":   self.ok,
        }, -1)
        
        self["deviceinfo"] = List()

        self.smartinfo = smartinfo

        self.onLayoutFinish.append(self.displayAttributes)
        
    def cancel(self):
        self.close()

    def ok(self):
        pass

    def displayAttributes(self):
        attributes = self.smartinfo.getAttributes()
        list = [ ("ID", "Name", "Status", "Value", "Worst", "Thresh", "Raw") ] + attributes
        self['deviceinfo'].setList(list)
