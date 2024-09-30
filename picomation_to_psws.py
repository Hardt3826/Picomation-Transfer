# ----------------------------------------------------------------------------
# Copyright (c) 2024 University of Alabama
# All rights reserved.
#
# Distributed under the terms of the BSD 3-clause license.
#
# The full license is in the LICENSE file, distributed with this software.
# ----------------------------------------------------------------------------

import os
import shutil
from paramiko import AutoAddPolicy, SSHClient



def fetch_magData(Station):
    ROOT_DIR= "/home/echardt/Documents/PicomationData/"
    os.chdir(ROOT_DIR)
    os.mkdir(Station['Name'])
    cwd= os.chdir(ROOT_DIR + Station['Name'])
    Station['Local_Path']= os.getcwd()
    os.system("wget -r -np -nH --cut-dirs=2 -R index.html --no-check- " + Station["Picomation Dir"])
    for file in os.listdir(cwd):
        if not file.endswith('.log'):
            os.remove(file)

def process_data(Station):
    DIR="/home/echardt/Documents/PicomationData/" + Station['Name']
    os.chdir(DIR)
    for file in os.listdir(DIR):
        date= str(file).split("-")[1]
        year= date[0:4]
        month= date[4:6]
        day= date[6:8]

        filename= "OBS"+year+"-"+month+"-"+day+"T00:00"
        os.mkdir(filename)
        shutil.move(file, filename)
        try:
            os.system("zip -r " + filename + " " + filename)
            os.system("rm -rf " + filename)
        except FileExistsError:
            continue

def upload_data(Station):
    SERVER_ADDRESS= "10.116.34.204"
    USERNAME= "root"
    PASSWD= "root"
    
    client= SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(SERVER_ADDRESS, username=USERNAME, password=PASSWD)
    client.close()

def clean_Local_Storage(Station):
    os.chdir("/home/echardt/Documents/PicomationData")
    os.remove(Station['Local_Path'])

def main():

    stations=[
        {'Name': "AB4EJ",
         'Picomation Dir': 'https://picomation.net/AB4EJ/',
         'PSWS dir': 'N000003',
         'Instrument': "Magnetometer2",
         'Local_Path': None},
         {'Name': "AC0G",
         'Picomation Dir': 'https://picomation.net/AC0G/',
         'PSWS dir': 'S000082',
         'Instrument': "84",
         'Local_Path': None},
         {'Name': "JENNYJUMP",
         'Picomation Dir': 'https://picomation.net/JENNYJUMP/',
         'PSWS dir': 'S000033',
         'Instrument': "Magnetometer",
         'Local_Path': None},
         {'Name': "K2KGJ",
         'Picomation Dir': 'https://picomation.net/K2KGJ/',
         'PSWS dir': 'S000165',
         'Instrument': "165",
         'Local_Path': None},
         {'Name': "K4BSE",
         'Picomation Dir': 'https://picomation.net/K4BSE/',
         'PSWS dir': 'S000075',
         'Instrument': "", #Station DOES NOT have a magnetometer attached. Need one created
         'Local_Path': None},
         {'Name': "KA2VLP",
         'Picomation Dir': 'https://picomation.net/KA2VLP/',
         'PSWS dir': 'S000132',
         'Instrument': "138",
         'Local_Path': None}]
    
    for station in stations[0:1]:
        print(station['Name'])
        #fetch_magData(station)
        #process_data(station)
        #upload_data(station)
        #clean_Local_Storage(station)
        input("Next Station?")


if __name__ == "__main__":
    main()