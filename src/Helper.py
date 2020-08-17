# -*- coding: utf-8 -*-
# Depends: smartctl

import subprocess
import sys

def sub_process(cmd):
    if sys.version_info.major == 2:
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    else:
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding='utf-8').communicate()[0]
    return out

if __name__ == "__main__":
    out = sub_process(["ls", "-l"])
    print(out)
