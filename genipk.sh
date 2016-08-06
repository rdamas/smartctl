#!/bin/sh

cd meta
chmod +x postinst
version=$(grep Version control|cut -d " " -f 2)
mkdir -p usr/lib/enigma2/python/Plugins/Extensions/SmartCtl
cp -r ../SmartCtl/* usr/lib/enigma2/python/Plugins/Extensions/SmartCtl
tar -cvzf data.tar.gz usr
tar -cvzf control.tar.gz control postinst

rm -f ../smartctl_${version}_all.ipk
ar -r ../smartctl_${version}_all.ipk debian-binary control.tar.gz data.tar.gz

rm -fr control.tar.gz data.tar.gz usr
