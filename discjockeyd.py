import pyudev
import subprocess, sys
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
#monitor.filter_by('block')
print('Monitoring!')
for device in iter(monitor.poll, None):
    print('Event Happened!')
    for attribute in iter(device.properties):
        print(attribute)
        #print(device.get(attribute))
    if device.get('ID_CDROM') and device.get('DISK_MEDIA_CHANGE'):
        print('CDROM inserted!')
        print(device.get('DEVNAME'))
        subprocess.run(f'autorun.sh {device.get('DEVNAME')}', shell = True, executable="/bin/bash")
    #if 'ENV{ID_CDROM}' in device and 'ENV{DISK_MEDIA_CHANGE}' in device:
     #   print('Disk inserted!')
