'''command line tool to handle flight log input'''
import fire
from flightdata import Flight
from tkinter import filedialog


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

if __name__ == "__main__":
    fire.Fire({
        "convert": conv,
        "browse": brow
    })