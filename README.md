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

DiscJockey brings an authentic autorun experience to linux for GOG offline installers. Burn your installer to an optical disc alongside the discjockey file and autorun it like on a retro windows install. Once a game is installed, inserting the disc again will autolaunch the game. 

## Key Features

- Automatically launch installers
- Automatically run installed games
- Lives entirely in home
- Global configuration to overwrite on disc settings
- Each discjockey disc is also(optionally) a discjockey installer for true offline support

## Architecture

DiscJockey consists of a python daemon running under systemD, a launch script that handlesinstalling and running games from disc, a centralised location for launch scripts and gamemanagement, and a config folder. 

The daemon is a user daemon and starts on login. It watches for discs to be inserted, then calles the launch script if it finds the discjockey config file on disc. The launch script checks if the game is already installed and launches the game from your PC's storage, or the installer from disc, as appropriate. 

Discjockey uses UMU-launcher to run games, as it provides a standard environment that is consistent with other launchers and can be installed as a user application. A new prefix is created for each game. The location of the prefix is set in the on disc config, but can be overridden by the global config. 

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

`cd MDK/ && nano discjockey`

2. Test the config file by running launch.sh(located in DiscJockeyFiles in your Installation folder) and passing your working directory as an argument 

`./DiscJockeyFiles/launch.sh ../MDK`

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
We don't aim for compatibility with very old, unmaintained linux distros. While we won't deliberately break compatibility with them just for the sake of it, if there are clear benefits to making a breaking change we will make it. As a rough guideline we aim to work on distros released in the last decade.

### Compatibility with every distro
We don't aim to work with everything under the sun. For instance, DiscJockey has systemD as a hard dependency. 

### Being a launcher
DiscJockey launches games. It is not a launcher in the common sense, ie a gui program with lists of games, custom containers, wine runners and so on. There will never be a GUI*. There will never be online updates.

\*We may consider functional gui widgets to wrap functionality that doesn't work in windows installers running under wine, e.g choosing a wine prefix location, choosing to create desktop icons. But that's it.

### Looking pretty 
Sleek? Modern? Beautiful? All things we don't want to be. We want to be exactly like the experience of inserting a disc into a disc drive and hearing said drive slowly humm to life before a small grey box appears on your screen. 


## Roadmap

### 0.2

- Rewrite shell scripts in python with calls out to shell where necessary
- Remove bash 4.3 as a dependency. Aim for DiscJockey to run in all major shells(bash, dash, fish, zsh)
- Multi disc installer support for installers that don't support true multidisc support via archades gog workaround 
- Multi disc support for true multidisc installers  

### 0.3
- Installation of Umu-launcher from disc
- Per game wine dependency management through protontricks
- Installation of manuals, artwork, strategy guides etc 
- Uninstall games through discjockey
### 0.4

- Optional wrapper GUI for installer(choosing prefix location, better management of multidisc support)
- Optional wrapper GUI for launching games(uninstall, open manual, strategy guide)

### Longer Term
Possible support for other init systems
Support for windows autorun.inf files to allow it to run authentic commercial discs(this will be inherently more limited than actual discjockey disks)

