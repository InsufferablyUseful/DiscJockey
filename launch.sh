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
autostartPath=${configuration["autostartPath"]}
autostartScript=${configuration["autostartScript"]}
gameDirectory=${configuration["gameDirectory"]}
gamePath=${configuration["gamePath"]}
gameExe=${configuration["gameExe"]}
installerExe=${configuration["installerExe"]}

gameID=${configuration["gameID"]}
store=${configuration["store"]}
proton=${configuration["proton"]}

#Check if game is already installed
autostartFullPath=${autostartPath}/${autostartScript}

if [[ -e "${autostartFullPath}" ]]; then
	#Run the launch script 
	${autostartFullPath} 
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
