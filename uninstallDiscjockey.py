import subprocess
from utilities import *

def UninstallDiscJockey():
        print('Uninstall started!')
        #Stop daemon
        print('Stopping daemon')
        subprocess.run('systemctl --user stop discjockey.service', capture_output=True, text=True, shell = True, executable='/bin/bash')
        subprocess.run('systemctl --user disable discjockey.service', capture_output=True, text=True, shell = True, executable='/bin/bash')
       
        print('Deleting files')
        for file in expected_files:
            try:
                os.remove(os.path.join(home_directory,file))
            except Exception as e:
                print('An error ocurred trying to delete ', os.path.join(home_directory,file))
                print(e)
        subprocess.run('systemctl --user daemon-reload', capture_output=True, text=True, shell = True, executable='/bin/bash')

        print('Deleting directories') 
        for directory in expected_directories:
                directory = os.path.join(home_directory, directory)
                try:
                    os.rmdir(directory)
                except Exception as e:
                    print('An error ocurred trying to delete', directory)
                    print(e)


confirm_uninstall = Get_Input('Are you sure you want to uninstall discjockey, including your config files and any automatic backups? Proceeding is irreversible. Y/N: ', valid_inputs_Yes_No)
if confirm_uninstall == 'Y' or confirm_uninstall == 'y':
    confirm_uninstall = Get_Input('Last chance! Proceed with full uninstall? Y/N: ', valid_inputs_Yes_No)
    if confirm_uninstall == 'Y' or confirm_uninstall == 'y':
        UninstallDiscJockey()
    else:
        print('Uninstall cancelled. exiting')
else:
    print('Uninstall cancelled. exiting')
