#!/bin/bash
cd /Users/shidanlifuhetian/All/Tdevelop/zhaopianoSoftware
py2applet --make-setup main.py --iconfile icon.icns
python3 setup.py py2app -A
