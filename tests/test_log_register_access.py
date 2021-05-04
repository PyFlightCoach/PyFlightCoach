from pyflightcoach.log_register.access import new_session
from pyflightcoach.log_register.tables import Log
import unittest
from pathlib import Path
import shutil
import os
from streamlit.uploaded_file_manager import UploadedFile, UploadedFileRec
import numpy as np
import pandas as pd


class TestAccess(unittest.TestCase):
    def setUp(self):
        self.path = Path('tests/temp/')
        try:
            shutil.rmtree(self.path)
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree('tests/temp2/')
        except FileNotFoundError:
            pass
        

        self.access = new_session('tests/temp/') 


    def tearDown(self) -> None:
        shutil.rmtree(self.path)
        return super().tearDown()

    def test_from_folder(self):
        self.assertTrue(os.path.exists(self.path))
        self.assertTrue(os.path.exists(self.path / "register.db"))


    def test_register_log(self):
        new_log = self.access.register_log(Path('data/logs/00000150.BIN'))
        with open(Path('data/logs/00000150.BIN'), 'rb') as f:
            same_log = self.access.register_log(UploadedFile(
                UploadedFileRec(0, f.name, 'BIN', f.read())))
        self.assertEqual(new_log.bin_file, same_log.bin_file)

    def test_last_log(self):
        l1 = self.access.register_log(Path('data/logs/00000150.BIN'))
        l2 = self.access.register_log(Path('data/logs/00000130.BIN'))
        l3 = self.access.register_log(Path('data/logs/00000100.BIN'))
        llog = self.access.latest_log()
        self.assertEqual(llog.bin_file, l3.bin_file)

    def test_todays_logs(self):
        l1 = self.access.register_log(Path('data/logs/00000150.BIN'))
        l2 = self.access.register_log(Path('data/logs/00000130.BIN'))
        l3 = self.access.register_log(Path('data/logs/00000100.BIN'))

        llog = self.access.todays_logs()
        self.assertEqual(len(llog), 3)

    def test_register_folder(self):
        logs = self.access.register_folder(Path('data/logs/'))
        self.assertEqual(len(logs), 9)

    def test_set_sequence(self):
        self.access.register_folder(Path('data/logs/'))
        p21s = self.access.session.query(Log).filter(Log.stick_name.like("%000%")).all()
        self.access.set_sequence(p21s, "P21")
        p21 = self.access.session.query(Log).filter(Log.stick_name == "00000150.BIN").first()
        self.assertEqual(p21.sequence.name, "P21")


    def test_summary(self):
        self.access.register_folder(Path('data/logs/'))
        summary = self.access.summary()
        self.assertIsInstance(summary, pd.DataFrame)
        