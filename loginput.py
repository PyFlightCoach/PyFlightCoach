'''command line tool to handle flight log input'''
from os.path import splitext
import fire
from flightdata import Flight
from tkinter import filedialog
from glob import glob
import os
import shutil
from scripts.manage_logs import LogRegister
from pathlib import Path

reg = LogRegister.from_folder(Path('data/private_logs'))

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
    '''finds all the bin files on memory stick (linux), copies them to the data/private_logs
    folder with a uuid name, appends the register.csv'''
    reg.search_folder()

def folder(folder: str):
    reg.search_folder(Path(folder))
  

if __name__ == "__main__":
    fire.Fire({
        "convert": conv,
        "browse": brow,
        "batch": batch,
        "usb": usb,
        "folder": folder
    })