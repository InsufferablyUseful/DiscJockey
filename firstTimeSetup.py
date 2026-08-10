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

print('Checking for an existing DiscJockey installation...')
