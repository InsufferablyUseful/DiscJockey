DiscJockey - Automatically runs windows installers from removeable media 
    Copyright (C) 2026  InsufferablyUseful

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# DiscJockey

DiscJockey is a project aimed at bringing an authentic autorun experience to linux desktops. Using Umu-Runner, it autoruns game installers when you insert an optical disk. 

## Key Features

- Install detection
- Global configuration to overwrite on disc settings
- Autostart installed games on disc insert for a console like experience

## How to Use

### Create a DiscJockey disc

1. Clone this repo or download the latest release

`git clone https://github.com/InsufferablyUseful/DiscJockey.git`

#### Prepare the working directory
1. Copy the folder SingleDiscInstaller to a location of your choice. This copy is the working directory which will become your ISO. Naming it after the program you're going to burn is a good idea. For this example I'll use MDK  

`cp -r SingleDiscInstaller MDK `

2. For a self contained DiscJockey installation, copy DiscJockeyFiles, firstTimeSetup.py, utilities.py and uninstallDiscjockey.py to your copy of the working directory. This is optional, but your disc will not be able to install/uninstall DiscJockey unless you do this.

`cp DiscJockeyFiles firstTimeSetup.py utilities.py uninstallDiscjockey.py MDK/`

3. Copy your installer and any data files into your working directory.

`cp ~/Downloads/setupMDK.exe MDK.bin MDK/`

3. Optionally, copy an icon image to the working directory. This will be used for desktop /launcher icons. For GOG games the best way to get icons is to install the game and grab them from the game directory, unfortunately. For physical disks the icons are usually in the root directory on the disk. 

`cp ~/Pictures/MDK.png MDK/`

Note! 
The XDG specification requires a .png image. .ICO files from windows will NOT work. Convert them to png with an image editor first.  

#### Configure DiscJockey 

1. Enter your working directory. Open the discjockey file inside SingleDiscInstaller with your favourite text editor. Fill out the configuration options as desired. You must set all the mandatory options. The file contains example values and comments to guide you. 

`cd MDK/&& nano discjockey`

2. Test the config file by running launch.sh(located in DiscJockeyFiles in your Installation folder) and passing your working directory as an argument 

./DiscJockeyFiles/launch.sh ../MDK

If your configuration is correct the installer will start. Complete the installation and run launch again as above. This time the game should start. 

Note! If you have a global config file at ~/.config/discjockey/config and autostartInstalledPrograms is set to False then installed games will not autostart


#### Create a physical disk
1. Make a .iso file from your working directory. Discjockey includes makeiso.sh, a one line wrapper around mkisofs that sets flags for maximum compatibility. mkisofs isn't installed by default on every distro, so you might have to install it, or find an alternative. 

Searching for mkisofs "distro name" is usually informative...

`makeiso.sh MDK/ MDK`

The second argument is the label to assign to the .iso

You can also use GUI programs like ...

2. Test the iso. Assuming you have installed the DiscJockey service, mounting the iso should autorun the installer.   

3. Burn the iso to a disk with whatever tool you want. Brasero is a solid choice.

Congratulations! You have a working DiscJockey disc.  

### Installing DiscJockey

#### From a DiscJockey disc

1. Insert the disc into your disc drive. Open a terminal and navigate to the location of ythe disc.
2. Run python firstTimeSetup.py
3. Discjockey will install automatically.
4. Check and adjust global configuration settings. The global config file is located at ~/.config/discjockey/config

#### From your computer.

1. Navigate to your copy of the discjockey repo or latest discjockey release
2. Run python firstTimeSetup.py
3. Discjockey will install automatically.
4. Check and adjust global configuration settings. The global config file is located at ~/.config/discjockey/config



## Project Goals

### Self Contained
DiscJockey aims to abstract away the complexity of installing and launching games from disc on linux. Each DiscJockey disk should contain everything needed to install and run the game on it, without internet access or third party tools like wine, lutris etc. We love those projects, but they get in the way of the authentic physical media experience.

### Self deploying

DiscJockey discs should be able to fully install DiscJockey on all popular linux distros with a single script. A guiding goal of the project is that you can gift a disc to a friend who doesn't have DiscJockey and, after running the setup script once, they will have a working installation which will work with all future DiscJockey discs they use.

### Widely compatible
DiscJockey aims to run on a wide variety of linux distros. As part of the goal of being self contained, it is important that DiscJockey can work without being officially packaged by a distro. To that end it aims to keep dependencies minimal and install entirely within the users home directory.

### Simple
The process of creating DiscJockey discs should be simple and require no specialist skills beyond the ability to edit text. For some tricky games, and programs, basic knowledge of wine and installing windows dependencies will also be required. 

### Backwards Compatible
Once a disc is burned, you want to keep it forever. Disjockey should work with any DiscJockey disc, even if it's years out of date. New features must preserve old behaviour for older discs. 
## Non Goals

### Compatibility with retro linux distros
We don't aim for compatibility with very old, unmaintained linux distros. While we won't deliberately break compatibility with them just for the sake of it, if there are clear benefits to making a breaking change, and this change will only affect very old distro's we will make it. As a rough guideline we aim to work on distros released in the last decade.

### Being a launcher
DiscJockey launches games. It is not a launcher in the common sense, ie a gui program with lists of games, custom containers, wine runners and so on. There will never be a GUI*. There will never be online updates.

\*We may consider functional gui widgets to wrap functionality that doesn't work in windows installers running under wine, e.g choosing a wine prefix location, choosing to create desktop icons. But that's it.

### Looking pretty 
Sleek? Modern? Beautiful? All things we don't want to be. We want to be exactly like the experience of inserting a disc into a disc drive and hearing said drive slowly humm to life before a small grey box appears on your screen. 



How to create a bootable .iso

1. Copy the folder named after the type of install you want to a new location e.g SingleDiscInstaller to MDKInstaller. This will become your .iso
2. Copy the gog offline installer files to this new folder
3. Open config.text in a text editor. This is the equivalent to autorun.inf in windows. The autorun script reads these values to perform the install. Set the MANDATORY variables to appropriate values.
4. If your game has fixes authored by valve or the umu team, set the OPTIONAL variables as well. This tells umu to apply the fixes. You can also choose a custom proton version here if you want. 
5. Create an .iso from the folder using the makeISO script. You may need to install makeisofs. Feel free to use another option, all that matters is that the contents of MDKInstaller(or whatever) are turned into an .iso  
6. Mount the .iso and test it. The autorun script should launch it as though it's a real disk. Check that 
	- the installer autostarts
	- the install finishes successfully
	- the game starts from the autostart script 
	- the game starts upon disk insertion(remount the .iso). 
7. Once you have a working .iso, burn it to a disk!
8. Optionally, create a fancy case and print a custom label for the disk(Who am I kidding? If you think that this whole thing is a good idea it's not optional for you). 
