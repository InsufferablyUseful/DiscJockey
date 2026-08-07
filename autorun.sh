#!/bin/bash
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


