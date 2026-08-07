#!/bin/bash

#DiscJockey - Automatically runs windows installers from removeable media 
#    Copyright (C) 2026  InsufferablyUseful

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


echo "start"
#Make sure we're not getting the whole disk
disk="$1"
if [ -z $(echo "$disk" | grep '[0-9]') ] ; then
   exit
fi
echo "Disk name $disk"
echo "Disk name $disk" >> /tmp/udev.log
#Wait until partition appears
while ! lsblk -ln "$disk" | grep -q rom; do
        echo "sleep"
        #echo "sleep" >> /tmp/udev.log
        sleep 0.2
done
sleep 5
echo "leaving sleep"
partition=$(findmnt -rno TARGET  "$disk")
#partition=$(mount | grep "$disk" | awk '{print $3}')
echo "$partition"
cd "$partition"
"launch.sh" "$partition"
echo "finish"


