# -*- coding: utf-8 -*-
from Components.ActionMap import ActionMap
from Components.Console import Console
from Components.ScrollLabel import ScrollLabel
from Components.Sources.StaticText import StaticText   
from Screens.Screen import Screen

from __init__ import _

class SmartCtl(Screen):
    version = "2016-08-05 0.1"
    skin = """
        <screen name="E2SmartCtl" position="0,0" size="1920,1080" title="SmartCtl HDD Information" flags="wfNoBorder">
            <widget name="output" position="20,20" size="1880,920" transparent="1" font="Console;20" />
            <widget source="key_red" render="Label" position="20,1000" zPosition="1" size="400,50" font="Regular;20" halign="center" valign="center" backgroundColor="#f01010" foregroundColor="#ffffff" transparent="0" />
            <widget source="key_green" render="Label" position="500,1000" zPosition="1" size="400,50" font="Regular;20" halign="center" valign="center" backgroundColor="#10a010" foregroundColor="#ffffff" transparent="0" />
            <!-- widget source="key_yellow" render="Label" position="980,1000" zPosition="1" size="400,50" font="Regular;20" halign="center" valign="center" backgroundColor="#f0f010" foregroundColor="#303030" transparent="0" / -->
            <!-- widget source="key_blue" render="Label" position="1460,1000" zPosition="1" size="400,50" font="Regular;20" halign="center" valign="center" backgroundColor="#0000e0" foregroundColor="#ffffff" transparent="0" / -->
        </screen>
    """
    
    def __init__(self, session):
	Screen.__init__(self, session)
        self["actions"] =  ActionMap(["ColorActions", "WizardActions"], {
                "back":        self.cancel,
                "ok":          self.cancel,
                "up":          self.pageUp,
                "down":        self.pageDown,
                "left":        self.left,
                "right":       self.right,
                "red":         self.red,
                "green":       self.green,
                "yellow":      self.yellow,
                "blue":        self.blue,
        }, -1)
        
	self["key_red"] = StaticText(_("HDD INFO"))
	self["key_green"] = StaticText(_("HDD ATTR"))
	# self["key_yellow"] = StaticText(_("yellow"))
	# self["key_blue"] = StaticText(_("blue"))
        
        self["output"] = ScrollLabel()
        
        self.dict = {}
                
        self.console = Console()
        self.getSmartCtlInformation()

    def cancel(self):
        self.close()

    def pageUp(self):
            self["output"].pageUp()

    def pageDown(self):
            self["output"].pageDown()
    
    def left(self):
        pass
    
    def right(self):
        pass
    
    def red(self):
        self["output"].setText("\n".join(str(x) for x in self.dict["INFO"]))
    
    def green(self):
        self["output"].setText("\n".join(str(x) for x in self.dict["ATTR"]))
    
    def yellow(self):
        pass
    
    def blue(self):
        pass
    
    def getSmartCtlInformation(self):
        cmd = '/usr/sbin/smartctl -x /dev/sda'
        self.console.ePopen(cmd, self.cmdFinished)
    
    def cmdFinished(self, result, retval, extra=None):
        self.parseSmartInfo(result)
        self["output"].setText("\n".join(str(x) for x in self.dict["INFO"]))

    def parseInfoSection(self,line):
        words = map(str.strip,line.split(":"))
        if len(words) == 2:
            self.dict["INFO"].append(words)

    def parseAttrSection(self,line):
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
            elif section == "ATTR":
                # self.parseAttrSection(line)
                self.dict["ATTR"].append(line)

            if "START OF INFORMATION SECTION" in line:
                section = "INFO"
                self.dict["INFO"] = []

            if "Vendor Specific SMART Attributes" in line:
                section = "ATTR"
                self.dict["ATTR"] = []
