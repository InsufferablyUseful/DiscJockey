#!/bin/bash

installerDirectory=$1

if [[ -z "$installerDirectory" ]]; then
        printf "No installer directory provided. Try something like createInstallerSkeleton \"BaldursGate\". Exiting... "
        exit 0
fi

cp -r "SingleDiscOnlineInstaller" "$installerDirectory"
cp -r "discjockeyFiles/" "$installerDirectory/"
cp firstTimeSetup.py "$installerDirectory/"

printf "Skeleton created!\n"
printf "Next steps\n"
printf "Copy your installer files and an icon into the skeleton directory\n"
printf "Enter the skeletons config with appropriate values\n"
printf "Test the installer, create an iso and burn to disc\n"

