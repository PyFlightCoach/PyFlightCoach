from pyflightcoach.log_register.tables import create_db, Log, Sequence
from pathlib import Path
import numpy as np
import pandas as pd
import os
from datetime import datetime
from streamlit.uploaded_file_manager import UploadedFile
from typing import Union, List


class _Access:
    def __init__(self, engine, session):
        self.engine = engine
        self.session = session

    def _summary(self, query):
       return pd.read_sql(
            query.with_entities(
            Log.id,
            Log.bin_file, 
            Log.csv_file, 
            Log.stick_name, 
            Log.added,
            Sequence.name).statement,
            con=self.session.bind
        )


    def summary(self):
        return self._summary(self.session.query(Log).join(Sequence, isouter=True))

    def register_log(self, bin_file: Union[str, Path, UploadedFile]):
        if isinstance(bin_file, str):
            bin_file = Path(bin_file)
        if isinstance(bin_file, Path):
            log = self.session.query(Log).filter(Log.stick_name==bin_file.name, Log.filesize == bin_file.stat().st_size).first()
            if log is not None:
                return log
            else:
                log = Log.register_bin(bin_file)
        elif isinstance(bin_file, UploadedFile):
            log = self.session.query(Log).filter(Log.stick_name==Path(bin_file.name).name, Log.filesize == bin_file.size).first()
            if log is not None:
                return log
            else:
                log = Log.register_bin(bin_file)
        self.session.add(log)
        self.session.commit()
        return log

    def latest_log(self):
        return self.session.query(Log).order_by(Log.id.desc()).first()

    def _todays_logs(self):
        start_of_day = datetime.now().date()
        return self.session.query(Log).filter(Log.added>=start_of_day)

    def todays_logs(self):
        return self._todays_logs().all()

    def register_folder(self, folder: Path = Path('/media/')):
        return [self.register_log(file) for file in folder.glob("**/*.BIN")]
    
    def set_sequence(self, log: Union[Log, List[Log]], sequence: str):
        seq = Sequence.get_or_create(self.session, sequence)
        if isinstance(log, list):
            for lg in log:
                lg.sequence=seq
        else:
            log.sequence=seq
        self.session.commit()

def new_session(folder:str="data/private_logs/"):
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

    Log.rootfolder = Path(folder)
    
    engine, Session = create_db("sqlite:///{}register.db".format(folder))

    return _Access(engine, Session())