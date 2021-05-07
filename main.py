'''command line tool to handle flight log input'''
import fire
from pyflightcoach.log_register.access import new_session
from pathlib import Path
import sys
from streamlit import cli as stcli
from tkinter import filedialog
from flightdata import Flight


access = new_session()

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


def usb():
    '''finds all the bin files on memory stick (linux), copies them to the data/private_logs
    folder with a uuid name, registers them in the DB'''
    access.register_folder()


def folder(folder: str):
    '''copies all bin files in the folder in the data/private_logs, registers them in the DB'''
    access.register_folder(Path(folder))

def webapp():
    '''serves a web app to plot flight data'''

    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())


  

if __name__ == "__main__":
    fire.Fire({
        "convert": conv,
        "browse": brow,
        "folder": folder,
        "usb": usb,
        "app": webapp
    })