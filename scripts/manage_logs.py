'''This will manage the flight logs. It will keep a register of them, 
store them all with unique names and read new logs from the sd card'''

import uuid
from glob import glob
import shutil
from flightdata import Flight
import os

import numpy as np
import pandas as pd


def get_log_register(access='private'):
    logreg = 'data/{0}_logs/register.csv'.format(access)
    try:
        logregister = pd.read_csv(logreg)
    except:
        logregister = pd.DataFrame(columns=['uid', 'stick_name'])
    return logregister


def conv(a: str, b: str):
    return Flight.from_log(a).to_csv(b)


def find_logs(folder="/media/"):
    return glob(folder + "**/*.BIN", recursive = True)


def usb():
    USB_DRIVES = "/media/"
    LOG_DRIVE = "/home/tom/Desktop/logs/"

    usb_files = glob(USB_DRIVES + "**/*.BIN", recursive = True)
    disk_files = glob(LOG_DRIVE + "*.BIN")

    disk_filenames = [os.path.basename(file) for file in disk_files]
    files_to_copy = [file for file in usb_files if not os.path.basename(file) in disk_filenames]
    print("{0} files to copy".format(len(files_to_copy)))
    for i, file in enumerate(files_to_copy):
        print("copying file {0} of {1}".format(i+1, len(files_to_copy)))
        shutil.copyfile(file, LOG_DRIVE + os.path.basename(file))
    
    disk_csvs = glob(LOG_DRIVE + "*.csv")
    disk_files = glob(LOG_DRIVE + "*.BIN")
    csv_names = [os.path.splitext(os.path.basename(file))[0] for file in disk_csvs]
    files_to_convert = [file for file in disk_files if not os.path.splitext(os.path.basename(file))[0] in csv_names]

    print("{0} files to convert".format(len(files_to_convert)))
    for i, file in enumerate(files_to_copy):
        print("converting file {0} to {1}".format(i+1, len(files_to_copy)))
        try:
            conv(LOG_DRIVE + os.path.basename(file), LOG_DRIVE + os.path.basename(file).replace(".BIN", ".csv"))
        except Exception as ex:
            print(str(ex))

#unique_filename = str(uuid.uuid4())