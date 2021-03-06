#!/bin/sh

cd meta
chmod +x postinst
version=$(grep Version control|cut -d " " -f 2)
package=$(grep Package control|cut -d " " -f 2)
mkdir -p usr/lib/enigma2/python/Plugins/Extensions/SmartControl
cp -r ../src/* usr/lib/enigma2/python/Plugins/Extensions/SmartControl
tar -cvzf data.tar.gz usr
tar -cvzf control.tar.gz control postinst

[ -d ../dist ] || mkdir ../dist
rm -f ../dist/${package}_${version}_all.ipk
ar -r ../dist/${package}_${version}_all.ipk debian-binary control.tar.gz data.tar.gz

rm -fr control.tar.gz data.tar.gz usr
