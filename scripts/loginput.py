'''command line tool to handle flight log input'''
from os.path import splitext
import fire
from flightdata import Flight
from tkinter import filedialog
from glob import glob
import os
import shutil

def conv(a: str, b: str):
    """reads an ardupilot bin file and writes it to a csv.

    Args:
        a (str): the input ardupilot log file
        b (str): the target csv file

    Returns:
        [type]: [description]
    """
    return Flight.from_log(a).to_csv(b)


def brow():
    """reads an ardupilot bin file and writes it to a csv.
    opens a file dialog to select the log file and target

    Returns:
        [type]: [description]
    """

    a = filedialog.askopenfilename()
    b = filedialog.asksaveasfile()
    conv(a, b)


def batch():
    '''asks for a list of bin files, converts them all to csvs in the same folder'''
    a = filedialog.askopenfilenames()
    for f in a:
        try:
            conv(f, f.replace('.BIN', '.csv'))
            print(f)
        except Exception as ex:
            print("failed to read ", f)


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
    

if __name__ == "__main__":
    fire.Fire({
        "convert": conv,
        "browse": brow,
        "batch": batch,
        "usb": usb,
    })