import os
import sys
import glob
import shutil
from utilities import *

join = os.path.join

desktopEntry = ""
stringbuilder = []

desktop_entry_name = sys.argv[1]
launch_script = sys.argv[2] 
icon = sys.argv[3]


have_icon = False

desktop_icon=""
#Unfortunately even supposedly XDG compliant distros often don't set the XDG env vars correctly, so we have to do this bull****. 
#Thanks linux for teaching everyone the value of defensive programming
data_home=""
try:
        data_home_directory=os.environ["XDG_DATA_HOME"]
except: 
        print("Non XDG compliant distro. XDG_DATA_HOME not set. Assuming HOME/.local/share.")
        data_home_directory = join(home_directory, ".local","share") 

create_icon = True

if not os.path.isdir(join(data_home_directory,"icons")):
        create_icon = False
        print(f"Could not find XDG compliant directory for icons at {join(data_home_directory,"icons")}")

if os.path.isfile(icon) and create_icon:
        desktop_icon = join(data_home_directory,"icons",f"{desktop_entry_name}.png")
        try:
                shutil.copyfile(icon,desktop_icon)
                desktop_icon = f"{desktop_entry_name}.png"
                have_icon=True
        except Exception as e:
                print("An error ocurred trying to copy the icon png to",desktop_icon)
else:
        print("No icon found. Desktop icon will be blank")

#How did creating an icon pic take so much space? Maybe I just need to git gud at python...

if desktop_entry_name == '' and desktop_icon == '':
        print("No icon and no icon name provided. Cannot create icon. Exiting...")
        sys.exit()
print("Generating desktop file")
stringbuilder.append("[Desktop Entry]\nEncoding=UTF-8")
stringbuilder.append(f"Name={desktop_entry_name}")
stringbuilder.append(f"Exec=\"{launch_script}\"")
stringbuilder.append(f"Icon={desktop_icon}")
stringbuilder.append("Type=Application")
stringbuilder.append("Categories=Games;")

finalString = "\n".join(stringbuilder)

try:
        print("writing desktop file")
        print(join(data_home_directory,"applications",f"{desktop_entry_name}.desktop"))
        with open(join(data_home_directory,"applications",f"{desktop_entry_name}.desktop"),'w',encoding="utf-8") as icon:
                icon.write(finalString)
except Exception as e:
                    print('An error ocurred trying to create an icon for', desktop_entry_name)
                    print(e)
print("Finished adding desktop file")

