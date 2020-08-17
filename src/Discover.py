# -*- coding: utf-8 -*-
# Depends: util-linux

from __future__ import print_function, unicode_literals

import subprocess
import re

class Discover(object):

    def __init__(self):
        self.__devices = []
        cmd = [ "/usr/bin/lsblk", "-SP" ]
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        self.__parse(out)

        
    def __parse(self, lsblkOutput):
        for line in lsblkOutput.splitlines():
            device = {}
            for item in re.finditer(rb'(\w+)="(.*?)"', line):
                key = item.group(1).decode('utf-8').lower()
                val = item.group(2).decode('utf-8').strip()
                device[key] = val
            self.__devices.append(device)
    
    def devices(self):
        return self.__devices

if __name__ == "__main__":
    d = Discover()
    print(d.devices())
