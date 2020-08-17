# -*- coding: utf-8 -*-
# Depends: util-linux

from __future__ import print_function

import subprocess
import re
import sys

class Discover(object):

    def __init__(self):
        self.__devices = []
        cmd = [ "/usr/bin/lsblk", "-SP" ]
        if sys.version_info.major == 2:
            out = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        else:
            out = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding='utf-8').communicate()[0]
        self.__parse(out)

        
    def __parse(self, lsblkOutput):
        for line in lsblkOutput.splitlines():
            device = {}
            for item in re.finditer('(\w+)="(.*?)"', line):
                key = item.group(1).lower()
                val = item.group(2).strip()
                device[key] = val
            self.__devices.append(device)
    
    def devices(self):
        return self.__devices

if __name__ == "__main__":
    d = Discover()
    print(d.devices())
