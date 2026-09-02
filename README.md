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

An authentic autorun experience to linux for GOG offline installers(and others!). Burn your installer to an optical disc alongside the discjockey file and autorun it like on a retro windows install. Once a game is installed, inserting the disc again will autolaunch the game. 

## Contents
- [Introduction](#discjockey)
  - [Key Features](#key-features)
  - [Architecture](#architecture)
  - [System Requirements](#system-requirements)
- [How to Use](#how-to-use)
  - [Install DiscJockey](#install-discjockey)
  - [Create a DiscJockey Disc](#create-a-discjockey-disc)
  - [Uninstall DiscJockey](#uninstall-discjockey)
- [Project Goals](#project-goals)
- [Non Goals](#non-goals)
- [Roadmap](#Roadmap)

## Key Features

- Automatically launch installers
- Automatically run installed games
- Lives entirely in home
- Global configuration to overwrite on disc settings
- Each discjockey disc is also(optionally) a discjockey installer for true offline support

## Architecture

DiscJockey consists of a python daemon running under systemD, a launch script that handles installing and running games from disc, a folder to store launch scripts and a config folder. 

The daemon is a user daemon and starts on login. It watches for discs to be inserted, then calls the launch script if it finds a discjockey config file on disc. The launch script checks if the game is already installed and launches the game from your PC's storage, or the installer from disc, as appropriate. 

Discjockey uses UMU-launcher to run games, as it provides a standard environment that is consistent with other launchers and can be installed as a user application. A new prefix is created for each game. The location of the prefix is set in the on disc config, but can be overridden by the global config. 
Discjockey maintains a folder with launch scripts for each installed game. When you insert a disc for a game that you've previously installed, discjockey checks for a launch script. If it exists it will run it and launch the game instead of running the installer. 

## System Requirements

The current system requirements are

- SystemD
- Bash 4.3 or greater(Future versions will remove bash as a dependency)
- UMU-Runner installed via system or user install(Future versions will include the option to create a local UMU-runner installation)
- Python 3
- An XDG base directory compliant home directory(Currently assumes default locations, future updates will use XDG env vars if available)

## How to Use

Clone this repo or download the latest release

`git clone https://github.com/InsufferablyUseful/DiscJockey.git &&
cd DiscJockey`

### Install DiscJockey

#### From your computer

1. Navigate to your copy of the discjockey repo or latest discjockey release
`cd DiscJockey`
2. Run `python3 firstTimeSetup.py`
3. Discjockey will install automatically.
4. Check and adjust global configuration settings. The global config file is located at ~/.config/discjockey/config

#### From a DiscJockey disc

1. Insert the disc into your disc drive. Open a terminal and navigate to the mount location of the disc.
2. Run `python3 firstTimeSetup.py`
3. Discjockey will install automatically.
4. Check and adjust global configuration settings. The global config file is located at ~/.config/discjockey/config


### Create a DiscJockey disc

First, make sure that DiscJockey is installed.

#### Prepare the working directory

1. Run createInstallerSkeleton.sh "Path/To/WorkingDirectory". This will copy the required files into a working directory.

`./createInstallerSkeleton.sh MDK`

3. Copy your installer files into the working directory.

`cp ~/Downloads/setupMDK.exe MDK.bin MDK/`

3. Optionally copy a .png into the folder for use as a desktop icon. It must be called icon.png. 

`cp ~/Pictures/MDK.png MDK/icon.png`

> [!IMPORTANT]
.ICO files from windows will not work. Convert them to png with an image editor first.  

#### Configure DiscJockey 

1. Enter your working directory. Open discjockey with your favourite text editor. Fill out the configuration options as desired. You must set all the mandatory options. The default values are a working configuration for the gog release of [MDK](https://www.gog.com/en/game/mdk) . Use these as a guide and adapt them as needed.  

`cd MDK/ && nano discjockey`

2. Test the config file by running ~/.local/bin/discjockey/launch.sh and passing your working directory as an argument 

`./~/.local/bin/discjockey/launch.sh ~/DiscJockey/MDK`

If your configuration is correct the installer will start. Complete the installation and run launch again as above. This time the game should start. 

> [!NOTE]
> If you have set autostartInstalledPrograms to False in .config/discjockey/config then installed games will not autostart


#### Create a physical disk
1. Make a .iso file from your working directory. Discjockey includes makeiso.sh, a one line wrapper around mkisofs that sets flags for maximum compatibility. Depending on your distro you may have to install mkisofs. In general any iso creation tool should work. 

`makeiso.sh MDK/ MDK`

The second argument is the label to assign to the .iso

2. Test the iso. Assuming you have installed the DiscJockey service, mounting the iso should autorun the installer.   

3. Burn the iso to a disk with whatever tool you want. Brasero is a solid choice.

Congratulations! You have a working DiscJockey disc.  

### Uninstall DiscJockey

1. Navigate to .local/bin/discjockey and run python3 uninstallDiscjockey.py

`cd ~/.local/bin/discjockey/uninstallDiscjockey.py &&
python3 uninstallDiscjockey.py`

2. Follow the prompts to confirm uninstallation

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
DiscJockey doesn't aim for compatibility with very old, unmaintained linux distros. While we won't deliberately break compatibility with them just for the sake of it, if there are clear benefits to making a breaking change we will make it. As a rough guideline we aim to work on distros released in the last decade.

### Compatibility with every distro
DiscJockey doesn't aim to work with every distro under the sun, especially ones which deliberately don't comply with standards like XDG, or use less used software like SysVInit. This isn't a knock against those distros, or that software, I just have limited time and experience developing software for a larger audience than myself, and distro's which cover the majority of users will be the priority. Hopefully the project is simple enough that anyone who wants to can adapt it to work with their software stack.   

### Being a launcher
DiscJockey launches games. It is not a launcher in the common sense, ie a gui program with lists of games, custom containers, wine runners and so on. There will never be a GUI*. There will never be online updates.

\*We may consider functional gui widgets to wrap functionality that doesn't work in windows installers running under wine, e.g choosing a wine prefix location, choosing to create desktop icons. But that's it.

### Looking pretty 
Sleek? Modern? Beautiful? All things DiscJockey doesn't want to be. DiscJockey want to be exactly like the experience of inserting a disc into a disc drive and hearing said drive slowly humm to life before a small grey box appears on your screen. 


## Roadmap

### 0.2
- Rewrite shell scripts in python with calls out to shell where necessary
- Use XDG base directory env vars instead of assuming the common defaults
- Remove bash 4.3 as a dependency. 
- Multi disc installer support for installers that don't support true multidisc support via archades gog workaround 
- Uninstall games

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

