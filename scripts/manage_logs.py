'''This will manage the flight logs. It will keep a register of them, 
store them all with unique names and read new logs from the sd card'''

import uuid
from glob import glob
import shutil
from flightdata import Flight
import os

import numpy as np
import pandas as pd
from typing import Tuple
import datetime

def get_log_register(logfolder = 'data/private_logs/'):
    logreg = logfolder + 'register.csv'
    try:
        logregister = pd.read_csv(logreg)
    except:
        logregister = pd.DataFrame(columns=['uid', 'stick_name', 'filesize', 'date_added'])
        logregister.to_csv(logreg, index=False)
    return logfolder, logregister


def conv(a: str, b: str):
    return Flight.from_log(a).to_csv(b)


def find_logs(folder="/media/"):
    return glob(folder + "**/*.BIN", recursive = True)


def check_log(register, stick_name, filesize):
    existinglogs = register[(register.stick_name==stick_name) & (register.filesize==filesize)]
    if len(existinglogs) == 0:
        return False
    else:
        return True

def latest_log(logstorage: Tuple[str, pd.DataFrame] = None):
    if logstorage is None:
        folder, register=get_log_register()
    else:
        folder = logstorage[0]
        register = logstorage[1]
    return register.iloc[-1].uid + '.csv'


def add_logs(log_files, logstorage: Tuple[str, pd.DataFrame] = None):
    print("{0} files in folder".format(len(log_files)))
    if logstorage is None:
        folder, register=get_log_register()
    else:
        folder = logstorage[0]
        register = logstorage[1]
    new_logs = []
    
    for i, fpath in enumerate(log_files):
        name = os.path.basename(fpath)
        size = os.path.getsize(fpath)
        if not check_log(register, name, size):
            print("copying file {0} of {1}".format(i+1, len(log_files)))
            new_name = str(uuid.uuid4())
            shutil.copyfile(fpath, folder + new_name + '.BIN')
            register=register.append(dict(
                uid = new_name,
                stick_name = name,
                filesize = size,
                date_added = datetime.datetime.now()
            ), ignore_index=True)
            conv(folder + new_name + '.BIN', folder + new_name + '.csv')
            new_logs.append(folder + new_name + '.csv')
    os.remove(folder + 'register.csv')
    register.to_csv(folder + 'register.csv', index=False)
    return new_logs


def usb():
    return add_logs(find_logs('/media/'))


if __name__ == '__main__':
    pass
#unique_filename = str(uuid.uuid4())