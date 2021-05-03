'''This will manage the flight logs. It will keep a register of them, 
store them all with unique names and read new logs from the sd card'''

import uuid
from glob import glob
import shutil
from flightdata import Flight
import os

import numpy as np
import pandas as pd
from typing import Tuple, Dict, List
import datetime

from pathlib import Path


class LogHandle:
    def __init__(self, data: pd.Series, folder: Path):
        self.folder = folder
        self.data = data
        self.name = self.data.name
        self.bin = self.folder / "{}.BIN".format(self.data.name)
        self.csv = self.folder / "{}.csv".format(self.data.name)
        self._flight = None
        
    def __getattr__(self, name: str):
        return self.data[name]

    def flight(self):
        if self._flight is None:
            if os.path.exists(self.csv):
                self._flight = Flight.from_csv(self.csv)
            else:
                self._flight = Flight.from_log(str(self.bin))
                self._flight.to_csv(self.csv)
        return self._flight


class LogRegister:
    privatecols = ['uid', 'stick_name', 'filesize', 'date_added']

    def __init__(self, data: pd.DataFrame, folder: Path):
        self.data = data
        self.folder = folder

    @staticmethod
    def from_folder(folder: Path):
        try:
            reg = LogRegister(
                pd.read_csv(folder / 'register.csv').set_index('uid'),
                folder
            )
        except FileNotFoundError:
            reg = LogRegister(
                pd.DataFrame(columns=LogRegister.privatecols).set_index('uid'),
                folder
            )
            reg.save()
        return reg

    def save(self):
        self.data.to_csv(self.folder / 'register.csv')

    def select_logs(self, conditions: dict):
        return self.data[eval(
            " & ".join(["(self.data['{0}'] == {1})".format(
                col,
                '"{}"'.format(cond) if isinstance(cond, str) else cond
            )
                for col, cond in conditions.items()])
        )]

    def get_handles(self, conditions: dict):
        rows = self.select_logs(conditions)
        return [LogHandle(row, self.folder) for row in rows]

    def check_log_exists(self, binfile: Path):
        assert(binfile.suffix == '.BIN')

        existinglogs = self.select_logs(dict(
            stick_name=binfile.name,
            filesize=binfile.stat().st_size
        ))

        if len(existinglogs) == 0:
            return False
        else:
            return True

    def register_log(self, binfile: Path, metadata: dict = {}):
        new_name = str(uuid.uuid4())
        shutil.copyfile(binfile, self.folder / '{}.BIN'.format(new_name))
        self.data = self.data.append(
            pd.DataFrame(dict(uid=new_name, stick_name=binfile.name,
                              filesize=binfile.stat().st_size,
                              date_added=datetime.datetime.now(),
                              **metadata), index=[0]).set_index('uid')
        )
        self.save()
        return self.data.loc[new_name]

    def save_log(self, file, metadata: dict = {}):
        existinglogs = self.select_logs(dict(
            stick_name=file.name,
            filesize=file.size
        ))
        if len(existinglogs) == 0:
            new_name = str(uuid.uuid4())
            with open(self.folder / "{}.BIN".format(new_name), 'wb') as f:
                f.write(file.read())
            self.data = self.data.append(
                pd.DataFrame(dict(uid=new_name, stick_name=file.name,
                                  filesize=file.size,
                                  date_added=datetime.datetime.now(),
                                  **metadata), index=[0]).set_index('uid')
            )
            self.save()
            return self.data.loc[new_name]

        else:
            return existinglogs.iloc[0]

    def append_metadata(self, conditions: dict, newmetadata: dict):
        logs = self.select_logs(conditions)
        return self.update_metadata(logs.index, newmetadata)

    def update_metadata(self, uids, newmetadata: dict):
        for key, val in newmetadata.items():
            if not key in LogRegister.privatecols:
                self.data.loc[uids, key] = val
        self.save()
        return self.data.loc[uids]


    def get_or_register_log(self, binfile: Path, metadata: dict = {}):
        if self.check_log_exists(binfile):
            return self.append_metadata(
                dict(
                    stick_name=binfile.name,
                    filesize=binfile.stat().st_size
                ), metadata).iloc[0]
        else:
            return self.register_log(binfile, metadata)

    def search_folder(self, folder: Path = Path('/media/')):
        uids = []
        for file in folder.glob("**/*.BIN"):
            uids.append(self.get_or_register_log(file).name)
        return self.data[uids]

    def latest_log(self):
        return self.data.loc[self.data.date_added == self.data.date_added.max()].iloc[0]

    def latest_log_handle(self):
        return LogHandle(self.latest_log(), self.folder)

    def handles(self, rows: pd.DataFrame):
        return [LogHandle(row, self.folder) for index, row in rows.iterrows()]

    def handle(self, row: pd.Series) -> LogHandle:
        return LogHandle(row, self.folder)
