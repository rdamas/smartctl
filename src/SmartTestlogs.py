# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Sources.List import List
from Screens.Screen import Screen

from SmartInfo import SmartInfo

class SmartTestlogs(Screen):
    skin = """
    <screen name="SmartControlTestlogs" position="0,0" size="1920,1080" title="[SmartControl] Festplatten-Logs" flags="wfNoBorder">
        <widget render="Listbox" source="logs" enableWrapAround="0"
            position="0,100" size="1920,850" transparent="1"
            font="Regular;25" zPosition="5" scrollbarMode="showOnDemand"
            scrollbarSliderBorderWidth="0" scrollbarWidth="5">
            <convert type="TemplatedMultiContent">{
                "template": [
                    MultiContentEntryText(
                        pos = (30, 10),
                        size = (440, 50),
                        font = 0,
                        flags = RT_HALIGN_RIGHT | RT_VALIGN_CENTER,
                        text = 0),
                    MultiContentEntryText(
                        pos = (500, 10),
                        size = (1300, 50),
                        font = 0,
                        flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER,
                        text = 1)
                    ],
                "fonts": [gFont("Regular", 36)],
                "itemHeight": 50 }
            </convert>
        </widget>
    </screen>
    """
    
    def __init__(self, session, logs):
        self.session = session
        Screen.__init__(self, session)
        self.skinName = "SmartControlTestlogs"
        self["actions"] =  ActionMap(["ColorActions", "WizardActions"], {
                "back": self.cancel,
                "ok":   self.ok,
        }, -1)
        
        self["logs"] = List()

        self.logs = logs

        self.onLayoutFinish.append(self.displayLog)
        
    def cancel(self):
        self.close()

    def ok(self):
        pass

    def displayLog(self):
        list = [ ("Typ", "Wert") ] + self.logs
        self['logs'].setList(list)
