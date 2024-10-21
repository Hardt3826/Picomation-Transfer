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
from paramiko import AutoAddPolicy, SSHClient, SFTPClient



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
    SERVER_ADDRESS=  "pswsnetwork.caps.ua.edu" #"192.168.40.177"  #"pswsnetwork.caps.ua.edu" #"10.116.34.204"
    USERNAME= Station['PSWS dir']
    PASSWD= Station['Token'] #"Salad0CompSc!" #"H@rdtCompSc!"
    
    ssh= SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    try:
        ssh.connect(SERVER_ADDRESS, username=USERNAME, password=PASSWD)
    except:
        print("ssh connection could not be made for " + USERNAME)
        return
    transport = ssh.get_transport()
    session = transport.open_session()
    session.set_combine_stderr(True)
    

    sftp= SFTPClient.from_transport(transport)
    for file in os.listdir(Station['Local_Path']):
        try:
            filepath="/home/"+ Station['PSWS dir'] + "/magData/" + file
            localpath= Station['Local_Path'] + "/" + file
            sftp.put(localpath, filepath)


            date= str(file).split("-")[1]
            year= date[0:4]
            month= date[4:6]
            day= date[6:8]

            trigger= "mOBS"+ year +"-"+ month +"-"+ day +"T00:00_#" + Station['Instrument'] + "_#2024-10-21T00:00"
            triggerCMD= "/home/"+ Station['PSWS dir'] + "/" + trigger
            session = transport.open_session()
            session.exec_command('mkdir ' + triggerCMD)
        except:
            print("File: " + file + " could not be copied.")
    
    sftp.close()
    ssh.close()

def clean_Local_Storage(Station):
    try:
        os.chdir("/home/echardt/Documents/PicomationData")
        os.remove(Station['Local_Path'])
    except:
        print("Files could not be removed from local storage.")
        return

def main():

    stations=[
        {'Name': "JENNYJUMP",
         'Picomation Dir': 'https://picomation.net/JENNYJUMP/',
         'PSWS dir': 'S000033',
         'Token': 'a7831d7b5f4405a5dba0',
         'Instrument': "Magnetometer",
         'Local_Path': None},
         {'Name': "AC0G",
         'Picomation Dir': 'https://picomation.net/AC0G/',
         'PSWS dir': 'S000082',
         'Token': '497f198202b28421849b',
         'Instrument': "84",
         'Local_Path': None},
         {'Name': "K2KGJ",
         'Picomation Dir': 'https://picomation.net/K2KGJ/',
         'PSWS dir': 'S000165',
         'Token': 'd5b26574951fa7d0066d',
         'Instrument': "165",
         'Local_Path': None},
         {'Name': "KA2VLP",
         'Picomation Dir': 'https://picomation.net/KA2VLP/',
         'PSWS dir': 'S000132',
         'Token': '31d0b7d322cf5cf84f2b',
         'Instrument': "138",
         'Local_Path': None},
         {'Name': "KD8CGH",
         'Picomation Dir': 'https://picomation.net/KD8CGH/',
         'PSWS dir': 'S000167',
         'Token': '22964807c1a3a4091d09',
         'Instrument': "168",
         'Local_Path': None},
         {'Name': "KE8QEP",
         'Picomation Dir': 'https://picomation.net/KE8QEP/',
         'PSWS dir': 'S000168',
         'Token': '0df52ca7b947308e2ced',
         'Instrument': "169",
         'Local_Path': None},
         {'Name': "KV0S",
         'Picomation Dir': 'https://picomation.net/KV0S/',
         'PSWS dir': 'S000031',
         'Token': '812df753b96617010ab8',
         'Instrument': "38",
         'Local_Path': None},
         {'Name': "N5BRG",
         'Picomation Dir': 'https://picomation.net/N5BRG/',
         'PSWS dir': 'S000040',
         'Token': '762a05cfd957175769d9',
         'Instrument': "101",
         'Local_Path': None},
         {'Name': "W2NAF",
         'Picomation Dir': 'https://picomation.net/W2NAF/',
         'PSWS dir': 'S000028',
         'Token': '398fedebd9ec9d5f07e2',
         'Instrument': "31",
         'Local_Path': None},
         {'Name': "WB0VGI",
         'Picomation Dir': 'https://picomation.net/WB0VGI/',
         'PSWS dir': 'S000166',
         'Token': '49788b4a0d03ad8cb144',
         'Instrument': "166",
         'Local_Path': None}
         ]
    
    for station in stations:
        print(station['Name'])
        print("Fetching Data from Picomation.net")
        fetch_magData(station)
        print("Processing Data")
        process_data(station)
        print("Beginning Upload process to PSWS Network")
        upload_data(station)
        print("Upload Complete")
        clean_Local_Storage(station)
        choice= input("Next Station?")
        if choice == "N":
            return(0)
        else:
            continue


if __name__ == "__main__":
    main()