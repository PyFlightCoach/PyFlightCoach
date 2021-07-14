from pyflightcoach.log_register.tables import create_db, Log, Sequence, BoxReg
from pathlib import Path
import numpy as np
import pandas as pd
import os
from datetime import datetime
from streamlit.uploaded_file_manager import UploadedFile
from typing import Union, List
import io
from geometry import GPSPosition
from flightanalysis.flightline import Box
class _Access:
    def __init__(self, engine, session):
        self.engine = engine
        self.session = session
        self.current = None

    def _summary(self, query):
       return pd.read_sql(
            query.with_entities(
            Log.id,
            Log.bin_file, 
            Log.csv_file, 
            Log.stick_name, 
            Log.added,
            Sequence.name,
            BoxReg.name,
            BoxReg.club).statement,
            con=self.session.bind
        )


    def summary(self):
        return self._summary(self.session.query(Log).join(Sequence, isouter=True).join(BoxReg, isouter=True))

    def _box_summary(self, query):
        return pd.read_sql(
            query.with_entities(BoxReg.id, BoxReg.name, BoxReg.club, BoxReg.country).statement,
            con=self.session.bind
        )

    def box_summary(self):
        return self._box_summary(self.session.query(BoxReg))

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

    def current_log(self):
        if self.current is None:
            try:
                with open(Log.rootfolder / "current_log.txt", "r") as f:
                    current_log = int(f.read())
                self.current = self.get_log(current_log)
            except FileNotFoundError:
                self.current = self.latest_log()
        return self.current

    def set_current(self, logid):
        self.current = self.get_log(logid)
        with io.open(Log.rootfolder / "current_log.txt", "w") as f:
            f.write(str(logid))

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

    def set_direction(self, log: Union[Log, List[Log]], sequence: str):
        raise NotImplementedError()
        
    def get_log(self, logid: int):
        return self.session.query(Log).filter(Log.id == logid).first()

    def get_box(self,boxid):
        return self.session.query(BoxReg).filter(BoxReg.id == boxid).first()

    def get_boxes(self, club:str=None, country:str=None):
        flightlines = self.session.query(BoxReg)
        if not club == None:
            flightlines = flightlines.filter(BoxReg.club==club)
        if not country == None:
            flightlines = flightlines.filter(BoxReg.country==country)
        return flightlines.all()

    def set_box(self, log: Union[Log, List[Log]], box: Union[Box, BoxReg, int]):
        if isinstance(box, Box):
            _box = BoxReg.from_box(self.session, box)
        elif isinstance(box, BoxReg):
            _box = BoxReg
        elif isinstance(box, int): 
            _box = self.get_box(box)
        else:
            raise TypeError("expected BoxReg or Box")
        log.boxreg = _box
        self.session.commit()

    def set_start_end(self, log: Log, start_index, end_index):
        log.start_index = start_index
        log.end_index = end_index
        self.session.commit()

def new_session(folder:str="data/private_logs/") -> _Access:
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

    Log.rootfolder = Path(folder)
    
    engine, Session = create_db("sqlite:///{}register.db".format(folder))

    return _Access(engine, Session())