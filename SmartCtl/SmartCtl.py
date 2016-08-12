# -*- coding: utf-8 -*-
from Components.ActionMap import ActionMap
from Components.Console import Console
from Components.Label import Label
from Components.ChoiceList import ChoiceList, ChoiceEntryComponent
from Components.ScrollLabel import ScrollLabel
from Screens.Screen import Screen

from __init__ import _

class SmartCtl(Screen):
    version = "2016-08-06 0.2"
    skin = """
        <screen name="SmartCtl" position="0,0" size="1920,1080" title="SmartCtl HDD Information" flags="wfNoBorder">
            <widget name="output" position="20,20" size="1880,920" font="Console;20" zPosition="1" />
            <widget name="chooseDevice" position="20,80" size="400,500" scrollbarMode="showOnDemand" zPosition="2" />
            <widget name="key_red" position="20,1000" zPosition="1" size="400,50" font="Regular;20" halign="center" valign="center" backgroundColor="#f01010" foregroundColor="#ffffff" transparent="0" />
            <widget name="key_green" position="500,1000" zPosition="1" size="400,50" font="Regular;20" halign="center" valign="center" backgroundColor="#10a010" foregroundColor="#ffffff" transparent="0" />
            <widget name="key_yellow" position="980,1000" zPosition="1" size="400,50" font="Regular;20" halign="center" valign="center" backgroundColor="#f0f010" foregroundColor="#303030" transparent="0" />
            <!-- widget source="key_blue" position="1460,1000" zPosition="1" size="400,50" font="Regular;20" halign="center" valign="center" backgroundColor="#0000e0" foregroundColor="#ffffff" transparent="0" / -->
        </screen>
    """
    
    def __init__(self, session):
        self.session = session
	Screen.__init__(self, session)
        self["actions"] =  ActionMap(["ColorActions", "WizardActions"], {
                "back":        self.cancel,
                "ok":          self.ok,
                "up":          self.pageUp,
                "down":        self.pageDown,
                "left":        self.left,
                "right":       self.right,
                "red":         self.red,
                "green":       self.green,
                "yellow":      self.chooseDevice,
                "blue":        self.blue,
        }, -1)
        
	self["key_red"] = Label(_("HDD INFO"))
	self["key_green"] = Label(_("SHOW ATTR"))
	self["key_yellow"] = Label(_("CHOOSE DEVICE"))
	# self["key_blue"] = Label(_("blue"))
        
        self["output"] = ScrollLabel()
        
        self.getDevices()
        self.chooseMenuList = ChoiceList(self.devicesMenu)
        self["chooseDevice"] = self.chooseMenuList
        self.chooseMenuList.hide()
        
        self.dict = {}
        self.hasPotentialFailure = False
        self.showAttr = True
                
        self.console = Console()
        self.selectedDevice = None
        
        if len(self.devices) > 1:
            self.chooseDevice()
        elif len(self.devices) == 1:
            self["key_yellow"].hide()
            self.selectedDevice = self.devices[0]

        if self.selectedDevice:
            self.getSmartCtlInformation(self.selectedDevice)

    def cancel(self):
        self.close()

    def ok(self):
        if self.selectedDevice is None:
            self.selectedDevice = self.chooseMenuList.l.getCurrentSelection()[0][0]
            self.chooseMenuList.hide()
            self.getSmartCtlInformation(self.selectedDevice)
    
    def chooseDevice(self):
        self["output"].setText("")
        self.dict = {}
        self.hasPotentialFailure = False
        self.showAttr = True
        self.selectedDevice = None
        self.chooseMenuList.show()

    def pageUp(self):
        if self.selectedDevice:
            self["output"].pageUp()
        else:
            self.chooseMenuList.pageUp()

    def pageDown(self):
        if self.selectedDevice:
            self["output"].pageDown()
        else:
            self.chooseMenuList.pageDown()
    
    def left(self):
        pass
    
    def right(self):
        pass
    
    def red(self):
        if self.dict["INFO"]:
            text = "\n".join(str(x) for x in self.dict["INFO"])
            if self.dict["DATA"]:
                text += "\n\n" + "\n".join(str(x) for x in self.dict["DATA"])
            self["output"].setText(text)
            self["key_green"].setText(_("SHOW ATTR"))
            self.showAttr = True
    
    def green(self):
        if self.dict["ATTR"]:
            if self.showAttr:
                self["output"].setText("\n".join(str(x) for x in self.dict["ATTR"]))
                self["key_green"].setText(_("SHOW CRITICAL ATTR"))
                self.showAttr = False
            else:
                self["output"].setText("\n".join(str(x) for x in self.dict["FATTR"]))
                self["key_green"].setText(_("SHOW ATTR"))
                self.showAttr = True
    
    def yellow(self):
        pass
    
    def blue(self):
        pass
    
    def getDevices(self):
        self.devices = []
        self.devicesMenu = []
        mounted = open("/proc/mounts","r")
        for part in mounted:
            words = part.split()
            if words[0].startswith("/dev/sd"):
                device = words[0]
                device = device[0:8]
                if not device in self.devices:
                    self.devices.append( device )
                    self.devicesMenu.append( ChoiceEntryComponent(key=device, text=[device]) )
        
    def getSmartCtlInformation(self,device):
        cmd = '/usr/sbin/smartctl -x %s' % (device,)
        self.console.ePopen(cmd, self.cmdSmartctlFinished)
    
    def cmdSmartctlFinished(self, result, retval, extra=None):
        self.parseSmartInfo(result)
        self.red()

    def parseInfoSection(self,line):
        words = map(str.strip,line.split(":"))
        if len(words) == 2:
            self.dict["INFO"].append(words)

    def parseAttrSection(self,line):
        self.dict["ATTR"].append(line)
        try:
            id = int(line[0:3].strip())
            if id in (5,10,183,184,187,188,196,197,198,201,230):
                raw_value = int(line[61:].strip())
                if raw_value > 0:
                    self.hasPotentialFailure = True
                self.dict["FATTR"].append(line)
        except:
            self.dict["FATTR"].append(line)
        
    def parseAttrSectionTest(self,line):
        try:
            id = line[0:3].strip()
            attribute = line[4:27].strip()
            flags = line[28:36].strip()
            value = line[37:42].strip()
            worst = line[43:48].strip()
            tresh = line[49:55].strip()
            fail = line[56:60].strip()
            raw_value = line[61:].strip()

            if int(id) > 0:
                self.dict["ATTR"].append([id,attribute,flags,value,worst,tresh,fail,raw_value])
        except:
            pass

    def parseSmartInfo(self,smartInfo):
        section = False
        for line in smartInfo.split("\n"):
            if not line.strip():
                section = False

            if section == "INFO":
                # self.parseInfoSection(line)
                self.dict["INFO"].append(line)
            elif section == "DATA":
                # self.parseInfoSection(line)
                self.dict["DATA"].append(line)
            elif section == "ATTR":
                self.parseAttrSection(line)

            if "START OF INFORMATION SECTION" in line:
                section = "INFO"
                self.dict["INFO"] = []
            
            if "START OF READ SMART DATA SECTION" in line:
                section = "DATA"
                self.dict["DATA"] = []

            if "Vendor Specific SMART Attributes" in line:
                section = "ATTR"
                self.dict["ATTR"] = []
                self.dict["FATTR"] = []
        
        try:
            if self.hasPotentialFailure:
                self.dict["FATTR"].append("\nHDD has potential indicators of imminent electromechanical failure")
            else:
                self.dict["FATTR"].append("\nHDD seems ok.")
        except:
            pass

