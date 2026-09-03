import os 

home_directory = os.path.expanduser("~")
expected_files = [
'.config/discjockey/version',
'.local/bin/discjockey/launch.sh',
'.local/bin/discjockey/autorun.sh',
'.local/bin/discjockey/addDesktopIcons.py',
'.local/bin/discjockey/uninstallDiscjockey.py',
'.local/bin/discjockey/utilities.py',
'.local/bin/discjockey/discjockeyd.py',
'.config/systemd/user/discjockey.service' ]
expected_directories = [
'.config/discjockey',
'.local/bin/discjockey',
'.config/systemd/user' ]

deletion_directories = [
'.config/discjockey',
'.local/bin/discjockey']

deletion_files = [
'.config/systemd/user/discjockey.service' ]

valid_inputs_Yes_No = ['Y','N','y','n']

def Get_Input(message, valid_inputs):
        valid_input_received = False
        user_input = ''
        while valid_input_received == False:
                user_input = input(message)
                if len(valid_inputs) == 0:
                        valid_input_received = True
                        break
                for valid_input in valid_inputs:
                        if user_input == valid_input:
                                valid_input_received = True
                if valid_input_received == False:
                        print('Invalid response. Please try again')
        return user_input

