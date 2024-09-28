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

def clean_Local_Storage(Station):
    os.remove(Station['Local_Path'])

def main():
    SERVER_ADDRESS= "10.116.35.24"
    USERNAME= "root"
    PASSWD= "root"
    
    client= SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    #PSWS= client.connect(SERVER_ADDRESS, username=USERNAME, password=PASSWD)

    stations=[
        {'Name': "AB4EJ",
         'Picomation Dir': 'https://picomation.net/AB4EJ/',
         'PSWS dir': 'N000003',
         'Instrument': "Magnetometer2",
         'Local_Path': None,
         'Num_Files': 0}]
    
    for station in stations:
        print(station['Name'])
        #fetch_magData(station)
        #process_data(station)

if __name__ == "__main__":
    main()