# -*- coding: utf-8 -*-
# Depends: smartctl

import json
import subprocess
import sys

def sub_process(cmd):
    if sys.version_info.major == 2:
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    else:
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding='utf-8').communicate()[0]
    return out

def deunicodify_hook(pairs):
    new_pairs = []
    for key, value in pairs:
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        new_pairs.append((key, value))
    return dict(new_pairs)

def json_loads(obj):
    if sys.version_info.major == 2:
        out = json.loads(obj, object_pairs_hook=deunicodify_hook)
    else:
        out = json.loads(obj)
    return out

if __name__ == "__main__":
    out = sub_process(["ls", "-l"])
    print(out)
