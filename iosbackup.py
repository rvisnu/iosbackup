'''
This code is based on netmiko to take back up (show running-config) from cisco ios devices every 30 days
Accepts input (Device names/ip) as text file.
Output will be txt file for every device with time stamp

Netmiko can be found on GitHub at https://github.com/ktbyers/netmiko
'''

import argparse
import getpass
import time

from netmiko import ConnectHandler


class IosBackup:
    def __init__(self, username, password, input_file):
        '''
        class initialization
        '''
        self.username = username
        self.password = password
        self.input_file = input_file
        self.ip = list()

    def reader(self):
        '''
        Reads from the text file to return a list
        '''
        with open(self.input_file) as lines:
            for line in lines:
                self.ip.append(line)
        return self.ip

    def writer(self,ip,output,date):
        '''
        Write the show run outputs to a text file
        '''

        file_name = '{}-{}.txt'.format(ip,date)

        with open(
                file_name,
                'w') as the_file:
            for line in output:
                the_file.write(line+'\n')
        return True

    def login(self,device):
        '''
        Logs in to the ios device; change device_type to 'cisco_nxos' if device is nexus. Refer netmiko git link above
        :return:
        '''
        self.session = ConnectHandler(device_type='cisco_ios',
                                      ip=device,
                                      username=self.username,
                                      password=self.password)
        return True
    
    def logout(self):
        '''
        logs out of device
        '''
        self.session.disconnect()
        return True
    
    def run(self):
        '''
        Runs show runn command and returns output as list
        '''

        output = self.session.send_command('show runn')
        output = output.split('\n')
        return output


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', "--username", help="Login Username",
                        action="store")
    parser.add_argument('-p', "--password", help="Login password",
                        action="store")
    parser.add_argument('-f', "--in_file", help="Input txt file with device list",
                        action="store")
    args = parser.parse_args()

    if not args.username:
        args.username = raw_input("Login Username: ")
    if not args.password:
        args.password = getpass.getpass("Login Password: ")
    if not args.in_file:
        args.in_file = raw_input("txt file with device names: ")

    return (args.username,args.password,args.in_file)

# main
if __name__ == "__main__":
    (username, password, in_file) = arguments()
    backup = IosBackup(username, password, in_file)
    routers = backup.reader()

    while True:
        calender = time.strftime("%Y-%m-%d")  # Year Month Date
        for router in routers:
            router = router.strip()
            backup.login(router)
            show_run = backup.run()
            backup.logout()
            backup.writer(router,show_run,calender)
            print 'Recent Back up: {}'.format(calender)
        time.sleep(2600000) # Approx a month 60X60X24X30 = 2600000



