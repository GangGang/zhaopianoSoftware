#!/bin/bash
workdir=$(cd $(dirname $0); pwd)
echo $workdir
cd $workdir
py2applet --make-setup main.py --iconfile icon.icns
python3 setup.py py2app -A
