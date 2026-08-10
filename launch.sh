#DiscJockey - Automatically runs windows installers from removeable media 
#    Copyright (C) 2026  InsufferablyUseful
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

#!/bin/bash
discDirectory="$1"
cd "$discDirectory"
#Grab the config file
declare -A configuration
while read -r line; do
  if [[ $line == \#* ]]; then 
    continue 
  fi
  key="$(echo "$line" | awk -F'=' '{print $1}')"
  value=$(echo "$line" | awk -F'=' '{print $2}')
  configuration["$key"]="$value"
done < "config.txt"
#Fill out the config values into named variables for access
#TODO impractical in the long run. Break the whole thing up into functions/new scripts which setup just the vars they need
autostartPath=${configuration["autostartPath"]}
autostartScript=${configuration["autostartScript"]}
gameDirectory=${configuration["gameDirectory"]}
gamePath=${configuration["gamePath"]}
gameExe=${configuration["gameExe"]}
installerExe=${configuration["installerExe"]}

gameID=${configuration["gameID"]}
store=${configuration["store"]}
proton=${configuration["proton"]}

#Grab the global config file
#TODO This should be a function that I call twice, but passing arrays into functions is hard. Figure something out.
declare -A globalconfiguration
while read -r line; do
  if [[ $line == \#* ]]; then 
    continue 
  fi
  key="$(echo "$line" | awk -F'=' '{print $1}')"
  value=$(echo "$line" | awk -F'=' '{print $2}')
  globalconfiguration["$key"]="$value"
done < "${HOME}/.config/discjockey/config.txt"

globalInstallDirectory=${globalconfiguration["globalInstallDirectory"]}
globalAutostartDirectory=${globalconfiguration["globalAutostartDirectory"]}
autostartInstalledPrograms=${globalconfiguration["autostartInstalledPrograms"]}
installerCreatesDesktopIcons=${globalconfiguration["installerCreatesDesktopIcons"]}
installerCreatesMenuEntries=${globalconfiguration["installerCreatesMenuEntries"]}

if [[ ! -z "$globalInstallDirectory" ]]; then
	gamePath="$globalInstallDirectory"
fi

if [[ ! -z "$globalAutostartDirectory" ]]; then
	autostartPath="$globalAutostartDirectory"
fi

#Check if game is already installed
autostartFullPath="${autostartPath}/${autostartScript}"

if [[ -e "$autostartFullPath" ]]; then
	
	if [[ "$autostartInstalledPrograms" = "true" ]]; then
		#Run the launch script 
		$autostartFullPath &
	fi

else
	#Run the installer
	prefixDirectoryFullPath=${gamePath}/${gameDirectory}
 	#Check the path to the install folder exists
	if [[ ! -d "$(dirname "$prefixDirectoryFullPath")" ]]; then
		printf "$parentdir doesn't exist. Exiting...\n"
		exit 1
	fi
	
	printf "You're installing to: $prefixDirectoryFullPath \n"
	printf "==========WARNING==========\n"
	printf "DO NOT change the default install location in the installer. This is not supported. \n" 
	printf "If you do, autostart will not work, and the install script will think the installation has failed. \n"
	printf "The script will wait to verify installation success before creating the autorun script. Once the installation is complete, close the installer to finish the installation.\n"
	printf "==========WARNING==========\n"
	printf "The installer will now start.\n" 
	mkdir -p $prefixDirectoryFullPath
	WINEPREFIX=$prefixDirectoryFullPath GAMEID=$gameID STOREID=$store umu-run "${installerExe}" > /dev/null 2>&1
	#Check if the install succeeded
	if [[ ! -f "${prefixDirectoryFullPath}/drive_c/GOG Games/${gameDirectory}/${gameExe}" ]]; then
		printf "Could not find the game executable at ${prefixDirectoryFullPath}/drive_c/GOG Games/${gameDirectory}/${gameExe} \n"
		printf "It looks like the installation failed. \n"
		printf "Please double check that all parameters are correct. If they are, please file a bug report to help improve discjockey for everyone.\n";
		printf "Exiting..."
		exit 1
	fi

	#Create the autostart script
	mkdir -p $autostartPath	
	touch $autostartFullPath
	chmod +x $autostartFullPath
	echo "cd \"${prefixDirectoryFullPath}/drive_c/GOG Games/${gameDirectory}\"" >> "${autostartFullPath}"
	echo "WINEPREFIX='$prefixDirectoryFullPath' GAMEID=$gameID STOREID=$store umu-run '${prefixDirectoryFullPath}/drive_c/GOG Games/${gameDirectory}/${gameExe}' > /dev/null 2>&1" >> "${autostartFullPath}" 
	printf "Installation finished successfully. Eject and reinsert the disc to launch the game.\n"
fi
#TODO
