from sqlalchemy import (create_engine, ForeignKey, Column,
                        Integer, String, DateTime, Float)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from typing import Union
from pathlib import Path
from uuid import uuid4
from shutil import copyfile
from flightdata import Flight
import io
from streamlit.uploaded_file_manager import UploadedFile
import os
from geometry import GPSPosition
from flightanalysis.flightline import Box

Base = declarative_base()


class Log(Base):
    __tablename__ = "log"
    rootfolder = Path("data/private_logs")
    id = Column(Integer, primary_key=True)
    added = Column(DateTime, server_default=func.now())
    filesize = Column(Integer)
    stick_name = Column(String)
    bin_file = Column(String)
    csv_file = Column(String)
    sequence_id = Column(Integer, ForeignKey('sequence.id'))
    sequence = relationship("Sequence")
    boxreg_id = Column(Integer, ForeignKey('boxreg.id'))
    boxreg = relationship("BoxReg")

    @staticmethod
    def register_bin(bin_file: Union[str, Path, UploadedFile]):
        if isinstance(bin_file, (str, Path)):  # or isinstance(bin_file, Path):
            return Log._register_bin_path(bin_file)
        elif isinstance(bin_file, UploadedFile):
            return Log._register_bin_uploaded(bin_file)

    @staticmethod
    def _register_bin_uploaded(file: UploadedFile):
        new_name = str(uuid4())
        binpath = Log.rootfolder / '{}.BIN'.format(new_name)
        with io.open(binpath, 'wb') as f:
            f.write(file.read())
        return Log(
            filesize=file.size,
            stick_name=Path(file.name).name,
            bin_file=str(binpath),
            csv_file=str(Log.rootfolder / '{}.csv'.format(new_name))
        )

    @staticmethod
    def _register_bin_path(file: Union[str, Path]):
        if isinstance(file, str):
            file = Path(file)

        new_name = str(uuid4())
        return Log(
            filesize=file.stat().st_size,
            stick_name=file.name,
            bin_file=str(copyfile(file, Log.rootfolder /
                         '{}.BIN'.format(new_name))),
            csv_file=str(Log.rootfolder / '{}.csv'.format(new_name))
        )

    def flight(self):
        if os.path.exists(self.csv_file):
            return Flight.from_csv(self.csv_file)
        else:
            flight = Flight.from_log(str(self.bin_file))
            flight.to_csv(self.csv_file)
            return flight


class Sequence(Base):
    __tablename__ = "sequence"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    logs = relationship("Log", back_populates="sequence")

    @staticmethod
    def get_or_create(sess, name: str):
        seq = sess.query(Sequence).filter(Sequence.name == name).first()
        if seq is None:
            seq = Sequence(name=name)
            sess.add(seq)
            sess.commit()
        return seq


class BoxReg(Base):
    __tablename__ = "boxreg"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    club = Column(String)
    country = Column(String)
    pilot_lat = Column(Float)
    pilot_long = Column(Float)
    pilot_heading = Column(Float)
    logs = relationship("Log", back_populates="boxreg")

    @staticmethod
    def from_box(sess, box: Box):
        fl = sess.query(BoxReg).filter(
                BoxReg.club == box.club,
                BoxReg.country == box.country,
                BoxReg.name == box.name,
                BoxReg.pilot_lat == box.pilot_position.latitude,
                BoxReg.pilot_long == box.pilot_position.longitude,
                BoxReg.pilot_heading == box.heading
            ).first()
        

        if fl is None:
            try:
                fl = BoxReg(
                    name=box.name,
                    club=box.club,
                    country=box.country,
                    pilot_lat=box.pilot_position.latitude,
                    pilot_long=box.pilot_position.longitude,
                    pilot_heading=box.heading
                )
                sess.add(fl)
                sess.commit()
            except IntegrityError:
                sess.rollback()
                raise Exception("club name already exists")
        return fl

    @property
    def box(self) -> Box:
        return Box(
            self.name,
            GPSPosition(self.pilot_lat, self.pilot_long),
            self.pilot_heading, self.club, self.country)


def create_db(path="sqlite:///data/private_logs/register.db"):
    Session = sessionmaker()
    engine = create_engine(path)
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)
    return engine, Session
