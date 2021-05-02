'''command line tool to handle flight log input'''
import fire
from pyflightcoach.manage_logs import LogRegister
from pathlib import Path
import sys
from streamlit import cli as stcli


reg = LogRegister.from_folder(Path('data/private_logs'))


def usb():
    '''finds all the bin files on memory stick (linux), copies them to the data/private_logs
    folder with a uuid name, appends the register.csv'''
    reg.search_folder()



def webapp():
    '''serves a web app to plot flight data'''

    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())


def folder(folder: str):
    reg.search_folder(Path(folder))
  

if __name__ == "__main__":
    fire.Fire({
        "folder": folder,
        "usb": usb,
        "app": webapp
    })