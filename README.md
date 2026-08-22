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

Discjockey is a project aimed at bringing an authentic autorun experience to linux desktops. Using Umu-Runner, it autoruns game installers when you insert an optical disk. 

## Key Features

- Install detection
- Global configuration to overwrite on disc settings
- Autostart installed games on disc insert for a console like experience

## Project Goals

### Self Contained
Discjockey aims to abstract away the complexity of installing and launching games from disc on linux. Each discjockey disk should contain everything needed to install and run the game on it, without internet access or third party tools like wine, lutris etc. We love those projects, but they get in the way of the authentic physical media experience.

### Self deploying

Discjockey discs should be able to fully install discjockey on all popular linux distros with a single script. A guiding goal of the project is that you can gift a disc to a friendwho doesn't have discjockey and, after running the setup script once, they will have a working installation which will work with all future discjockey discs they use.

### Widely compatible
Discjockey aims to run on a wide variety of linux distros. As part of the goal of being self contained, it is important that discjockey can work without being officially packaged by a distro. To that end it aims to keep dependencies minimal and install entirely within the users home directory.

### Simple
The process of creating discjockey discs should be simple and require no specialist skills beyond the ability to edit text. For some tricky games, and programs, basic knowledge of wine and installing windows dependencies will also be required. 

## Backwards Compatible
Once a disc is burned, you want to keep it forever. Disjockey should work with any discjockey disc, even if it's years out of date. New features must preserve old behaviour for older discs. 
## Non Goals

### Compatibility with retro linux distros
We don't aim for compatibility with very old, unmaintained linux distros. While we won't deliberately break compatibility with them just for the sake of it, if there are clear benefits to making a breaking change, and this change will only affect very old distro's we will make it. As a rough guideline we aim to work on distros released in the last decade.

### Being a launcher
Discjockey launches games. It is not a launcher in the common sense, ie a gui program with lists of games, custom containers, wine runners and so on. There will never be a GUI*. There will never be online updates.

\*We may consider functional gui widgets to wrap functionality that doesn't work in windwos installers running under wine, e.g choosing a wine prefix location, choosing to create desktop icons. But that's it.

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
