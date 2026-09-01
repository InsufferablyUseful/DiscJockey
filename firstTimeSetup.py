# Check for dependencies. If some are missing, explain what's missing and exit
# Check if a version of discjockey is already installed
# Check if it's older than the one on disk
# Offer to install if not installed, or update if it is
#
# Dependencies
# Bash greater than 4.3
# Systemd
# Python 3
# Umu-launcher
#
#
# Installation procedure
# Copy discjockeyd.py, launch and autostart.sh to ~/.local/bin/discjockey
# Copy globalconfig to ~/.config/discjockey/config.txt
# Copy discjockey.service to ~/.config/systemd/user/discjockey.service
# Run systemctl --user start discjockey.service and systemctl --user enable discjockey.service
#
import subprocess
import operator
import os
import shutil
import sys
from time import localtime, strftime

from discjockeyFiles/utilities import *

with open('discjockeyFiles/version', 'r') as version_file:
        ondisc_version = version_file.readline()

def CheckDependency(message, command, operator, expected_output, numeric):
        print(message, end = ' ')
        result = subprocess.run(command, capture_output=True, text=True, shell = True, executable='/bin/bash')
        stdout = result.stdout
        if numeric:
                stdout = int(stdout)
        if operator(stdout,expected_output):
                print('OK')
                return True
        else:
                print('Not found')
                return False

def CheckForExistingInstall(file_locations, home_directory):
        missing_files = []
        for file_location in file_locations:
                print(os.path.join(home_directory,file_location))
                if not os.path.isfile(os.path.join(home_directory,file_location)): 
                        missing_files.append(file_location)
        print(len(missing_files))
        return missing_files 

def Install_DiscJockey():
        print('Install started!')
        #backup config file
        #create directories
        print('Creating directories')
        for destination in expected_directories:
                directory = os.path.join(home_directory, os.path.dirname(destination))
                print(directory)
                os.makedirs(directory, exist_ok = True)

        print('Creating config file')
        config_path = os.path.join(home_directory,'.config/discjockey/config')
        if os.path.isfile(config_path):
                keep_config = Get_Input('Existing config file found. Do you want to replace it? This will wipe any changes to the defaults. In most cases it\'s easier to copy new values from the example config in discjockeyFiles/config. Y/N: ', valid_inputs_Yes_No)
                if keep_config == 'Y' or keep_config == 'y':
                        print('Replacing config file. The old config file will be preserved in the config directory. You will need to update the default settings.')
                        time = strftime('%H_%M_%S',localtime())
                        if not os.path.isfile(config_path + '_backup_' + time):
                                shutil.move(config_path,config_path + '_backup_' + time)
                        else:
                                print('Backup config file name already taken. Could not create backup config')
                                sys.exit(1)
                        shutil.copyfile(os.path.join('discjockeyFiles',"globalconfig"),os.path.join(home_directory,".config","discjockey","globalconfig"))
                if keep_config == 'N' or keep_config == 'n': 
                        print('Keeping existing config file. You should review the example config at discjockeyFiles/globalconfig for any new options you may want to change.')
        else:
                shutil.copyfile(os.path.join('discjockeyFiles',"globalconfig"),os.path.join(home_directory,".config","discjockey","globalconfig"))
        #create files
        print('Creating files')
        for destination in expected_files:
                fileName = os.path.basename(destination)
                shutil.copyfile(os.path.join('discjockeyFiles',fileName),os.path.join(home_directory,destination))
        #Setup daemon
        subprocess.run('systemctl --user daemon-reload', capture_output=True, text=True, shell = True, executable='/bin/bash')
        subprocess.run('systemctl --user enable discjockey.service', capture_output=True, text=True, shell = True, executable='/bin/bash')
        subprocess.run('systemctl --user start discjockey.service', capture_output=True, text=True, shell = True, executable='/bin/bash')


print('Checking dependencies...')
dependencies_met = True
if not CheckDependency('Bash version >= 4:', 'echo $BASH_VERSINFO', operator.gt, 4,True):
        dependencies_met = False
if not CheckDependency('Systemd:','ps --no-headers -o comm 1' , operator.eq, 'systemd\n', False):
        dependencies_met = False
if not CheckDependency('Umu-launcher:','umu-run -v', operator.ne, '', False): 
        dependencies_met = False

if not dependencies_met:
        print('Your system is missing dependencies that DiscJockey needs to run properly. DiscJockey cannot be installed. See the documentation for troubleshooting steps.')
        print('The installer will now exit...')
        sys.exit(1)
print('Checking for an existing DiscJockey installation...')

missing_files = CheckForExistingInstall(expected_files, home_directory)

install_permission = ''
if len(missing_files) == len(expected_files):
        install_permission = Get_Input('No install of DiscJockey found. Do you want to install Y/N: ', valid_inputs_Yes_No)
if len(missing_files) > 0 and len(missing_files) < len(expected_files):
        print('Traces of an existing install were found, but it seems to be incomplete.')
        print('The following files are missing: ')
        for missing_file in missing_files:
                print(missing_file)
        install_permission = Get_Input('Do you want to reinstall DiscJockey? Your global configuration file will be preserved. Y/N: ', valid_inputs_Yes_No)
if len(missing_files) == 0: 
        print('Existing DiscJockey installation found. Checking if the version on disc is more recent.')
        with open(os.path.join(home_directory, '.config/discjockey/version'), 'r') as version_file:
                installed_version = version_file.readline()
        if installed_version < ondisc_version:
                  install_permission = Get_Input('This version is newer than the installed version. Do you want to upgrade? Y/N: ', valid_inputs_Yes_No)
        elif installed_version > ondisc_version:
                  install_permission = Get_Input('This version is older than the installed version. Do you want to downgrade? Y/N: ', valid_inputs_Yes_No)
        elif installed_version == ondisc_version:
                  install_permission = Get_Input('This version is already installed. Do you want to reinstall? Y/N: ', valid_inputs_Yes_No)
if install_permission == 'N' or install_permission == 'n':
        print('Exiting installer')
        sys.exit(0)
if install_permission == 'Y' or install_permission == 'y':
        Install_DiscJockey()
