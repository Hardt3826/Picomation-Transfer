# ----------------------------------------------------------------------------
# Copyright (c) 2024 University of Alabama
# All rights reserved.
#
# Distributed under the terms of the BSD 3-clause license.
#
# The full license is in the LICENSE file, distributed with this software.
# ----------------------------------------------------------------------------

import os

from paramiko import AutoAddPolicy, SSHClient

def fetch_magData(Station):
    cwd= os.chdir("C:/Users/Evan Hardt/Desktop/Picomation Data")
    os.system("wsl -e wget -r -np -nH --cut-dirs=2 -R index.html --no-check- " + Station["Picomation Dir"])
    for file in os.listdir(cwd):
        if not file.endswith('.log'):
            os.remove(file)

    

def main():
    SERVER_ADDRESS= "10.116.35.24"
    USERNAME= "root"
    PASSWD= "root"
    
    client= SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    PSWS= client.connect(SERVER_ADDRESS, username=USERNAME, password=PASSWD)

    stations=[
        {'Name': "AB4EJ",
         'Picomation Dir': 'https://picomation.net/AB4EJ/',
         'PSWS dir': 'N000003',
         'Instrument': "Magnetometer2",
         'Local_Path': None,
         'Num_Files': 0}]
    
    for station in stations:
        fetch_magData(station)


if __name__ == "__main__":
    main()