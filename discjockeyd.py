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
