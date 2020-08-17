# -*- coding: utf-8 -*-

from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Sources.List import List
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen

from .SmartInfo import SmartInfo
from .SmartAttributes import SmartAttributes
from .SmartTestlogs import SmartTestlogs

class SmartDevice(Screen):
    skin = """
    <screen name="SmartControlDevice" position="0,0" size="1920,1080" title="[SmartControl] Festplatte Informationen" flags="wfNoBorder">
        <widget render="Listbox" source="deviceinfo" enableWrapAround="0"
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
        <widget name="key_red" position="225,1015" size="280,55" zPosition="1" font="Regular; 23" halign="left" valign="center" backgroundColor="#00b81c46" />
        <widget name="key_green" position="565,1015" size="280,55" zPosition="1" font="Regular; 23" halign="left" valign="center" foregroundColor="#10389416"  />
        <widget name="key_yellow" position="905,1015" size="280,55" zPosition="1" font="Regular; 23" halign="left" valign="center" foregroundColor="#109ca81b" />
        <widget name="key_blue" position="1245,1015" size="280,55" zPosition="1" font="Regular; 23" halign="left" valign="center" foregroundColor="#00b9c1ff" />
    </screen>
    """

    def __init__(self, session, device):
        self.session = session
        Screen.__init__(self, session)
        self.skinName = "SmartControlDevice"

        self["actions"] =  ActionMap(["ColorActions", "WizardActions"], {
                "back":    self.cancel,
                "ok":      self.ok,
                "red":     self.showAttributes,
                "green":   self.showSelftestsLog,
                "yellow":  self.showErrorLog,
                "blue":    self.startSelftest,
        }, -1)
        self["deviceinfo"] = List()
        self["key_red"] = Label("Attribute")
        self["key_green"] = Label()
        self["key_yellow"] = Label()
        self["key_blue"] = Label()

        self.device = device
        self.smartinfo = None
        self.hasErrorLog = False
        self.hasSelftestsLog = False
        self.canSelftest = False
        
        self.onLayoutFinish.append(self.displayDriveInformation)
        
    def cancel(self):
        self.close()

    def ok(self):
        pass

    def displayDriveInformation(self):
        self.smartinfo = SmartInfo(self.device["name"])
        deviceinfo = self.smartinfo.getDeviceInformation()
        self['deviceinfo'].setList(deviceinfo)
        
        capabilities = self.smartinfo.getCapabilities()
        if capabilities["self_tests_supported"]:
            self.hasSelftestsLog = True
            self["key_green"].setText("Selbsttest-Ergebnisse")

        if capabilities["error_logging_supported"]:
            self.hasErrorLog = True
            self["key_yellow"].setText("Errorlog auslesen")

        if capabilities["poll_short_test"]:
            self.canSelftest = capabilities["poll_short_test"]
            self["key_blue"].setText("Kurzer Selbsttest")

    def showAttributes(self):
        if self.smartinfo:
            self.session.open(SmartAttributes, self.smartinfo)
    
    def showSelftestsLog(self):
        if self.hasSelftestsLog:
            logs = self.smartinfo.getSelftestsLog()
            self.session.open(SmartTestlogs, logs)

    def showErrorLog(self):
        if self.hasErrorLog:
            logs = self.smartinfo.getErrorLog()
            self.session.open(SmartTestlogs, logs)

    def startSelftest(self):
        if self.canSelftest:
            msg = "Selbsttest wird gestartet; der Test dauert etwa %s Minuten. Danach kann er abgerufen werden." % (self.canSelftest,)
            self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
            self.smartinfo.startShortSelftest()
