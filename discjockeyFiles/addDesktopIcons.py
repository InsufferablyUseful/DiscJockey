import os
import sys
import glob
import shutil
from utilities import *

desktopEntry = ""
stringbuilder = []

desktop_entry_name = sys.argv[1]
launch_script = sys.argv[2] 
desktop_icon=""
print(home_directory)
if os.path.isfile("../icon.png"):
        desktop_icon = os.path.join(home_directory,".local","share","icons",f"{desktop_entry_name}.png")
        try:
                shutil.copyfile(os.path.join("..","icon.png"),desktop_icon)
                desktop_icon = f"{desktop_entry_name}.png"
        except Exception as e:
                print("An error ocurred trying to copy the icon png to",desktop_icon)
else:
        print("No icon found. Desktop icon will be blank")
stringbuilder.append("[Desktop Entry]\nEncoding=UTF-8")
stringbuilder.append(f"Name={desktop_entry_name}")
stringbuilder.append(f"Exec={launch_script}")
stringbuilder.append(f"Icon={desktop_icon}")
stringbuilder.append("Type=Application")
stringbuilder.append("Categories=Games;")

finalString = "\n".join(stringbuilder)

print(finalString)

try:
        with open(os.path.join(home_directory,".local","share","applications",f"{desktop_entry_name}.desktop"),'w',encoding="utf-8") as icon:
                icon.write(finalString)
except Exception as e:
                    print('An error ocurred trying to create an icon for', desktop_entry_name)
                    print(e)

