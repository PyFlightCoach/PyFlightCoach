import unittest
from pyflightcoach.log_register.tables import BoxReg, Log, create_db, Sequence
import os
import shutil
import numpy as np
import pandas as pd
from pathlib import Path
from flightdata import Flight
from io import open
from streamlit.uploaded_file_manager import UploadedFile, UploadedFileRec
from geometry import GPSPosition
from flightanalysis.flightline import Box
from sqlalchemy.exc import IntegrityError

class TestLog(unittest.TestCase):
    def setUp(self):
        self.path = Path('tests/temp/')
        Log.rootfolder = self.path
        try:
            shutil.rmtree(self.path)
        except FileNotFoundError:
            pass
        os.mkdir(self.path)
        self.engine, self.Session = create_db("sqlite:///:memory:")

    def tearDown(self) -> None:
        shutil.rmtree(self.path)
        return super().tearDown()

    def test_register_log(self):
        newlog = Log.register_bin(Path('data/logs/bins/00000150.BIN'))
        self.assertIsInstance(newlog, Log)
        #        self.assertEqual(path.bin_file, )
        allbins = [f for f in self.path.rglob('*.BIN')]
        self.assertEqual(len(allbins), 1)
        self.assertEqual(str(allbins[0]), newlog.bin_file)

        flight = newlog.flight()
        self.assertIsInstance(flight, Flight)

        allcsvs = [f for f in self.path.rglob('*.csv')]
        self.assertEqual(len(allcsvs), 1)
        self.assertEqual(str(allcsvs[0]), newlog.csv_file)

    def test_register_bin_uploaded(self):
        with open(Path('data/logs/bins/00000150.BIN'), 'rb') as f:
            newlog = Log.register_bin(UploadedFile(
                UploadedFileRec(0, f.name, 'BIN', f.read())))
        self.assertIsInstance(newlog, Log)
        allbins = [f for f in self.path.rglob('*.BIN')]
        self.assertEqual(len(allbins), 1)
        self.assertEqual(str(allbins[0]), newlog.bin_file)


class TestSequence(unittest.TestCase):
    def setUp(self):
        self.path = Path('tests/temp/')
        Log.rootfolder = self.path
        try:
            shutil.rmtree(self.path)
        except FileNotFoundError:
            pass
        os.mkdir(self.path)
        self.engine, self.Session = create_db("sqlite:///:memory:")

    def tearDown(self) -> None:
        shutil.rmtree(self.path)
        return super().tearDown()

    def test_get_or_create(self):
        sess = self.Session()
        p21 = Sequence.get_or_create(sess, 'P21')
        p212 = Sequence.get_or_create(sess, 'P21')
        self.assertEqual(p21.id, p212.id)


class TestBoxReg(unittest.TestCase):
    def setUp(self):
        self.path = Path('tests/temp/')
        Log.rootfolder = self.path
        try:
            shutil.rmtree(self.path)
        except FileNotFoundError:
            pass
        os.mkdir(self.path)
        self.engine, self.Session = create_db("sqlite:///:memory:")

    def tearDown(self) -> None:
        shutil.rmtree(self.path)
        return super().tearDown()

    def test_from_box(self):
        sess = self.Session()
        
        box = Box.from_json('data/flightlines/gordano_box.json')
        box1 = Box.from_json('data/flightlines/gordano_box.json')
        box1.pilot_position.latitude = 0.0
        box2 = Box.from_json('data/flightlines/buckminster.json')

        fl = BoxReg.from_box(sess,box)
        self.assertEqual(fl.pilot_lat, box.pilot_position.latitude)
        self.assertEqual(fl.pilot_long, box.pilot_position.longitude)
        with self.assertRaises(Exception):
            fl = BoxReg.from_box(sess,box1)

        fl2 = BoxReg.from_box(sess,box2)
        self.assertEqual(fl2.country, fl.country)

    def test_box(self):
        sess = self.Session()
        
        box = Box.from_json('data/flightlines/gordano_box.json')
        fl = BoxReg.from_box(sess,box)
        bx = fl.box
        self.assertEqual(box.pilot_position.latitude, bx.pilot_position.latitude)
