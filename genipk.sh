#!/bin/sh

cd meta
mkdir -p usr/lib/enigma2/python/Plugins/Extensions/SmartCtl
cp -r ../SmartCtl/* usr/lib/enigma2/python/Plugins/Extensions/SmartCtl
tar -cvzf data.tar.gz usr
tar -cvzf control.tar.gz control

rm -f ../smartctl_0.1_all.ipk
ar -r ../smartctl_0.1_all.ipk debian-binary control.tar.gz data.tar.gz

rm -fr control.tar.gz data.tar.gz usr
