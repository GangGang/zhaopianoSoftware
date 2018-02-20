#!/bin/bash
workdir=$(cd $(dirname $0); pwd)
echo $workdir
cd $workdir
python3 main.py