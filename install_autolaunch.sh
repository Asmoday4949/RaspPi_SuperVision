#!/bin/bash

directory=$(realpath "./")
file="/etc/rc.local"

totalLines=$(wc -l < $file)
lineInsert=$((totalLines-1))

sed -i "$lineInsert a cd $directory && python3 ./Program/Run.py &" $file

echo "Added Raspberry Pi Motion Capture at startup of the system"
