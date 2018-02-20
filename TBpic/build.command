#!/bin/bash
cd /Users/shidanlifuhetian/All/Tdevelop/zhaopianoSoftware/TBpic
py2applet --make-setup main.py -p ./utils.py
python3 setup.py py2app -A
