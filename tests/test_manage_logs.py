import unittest
from pyflightcoach.manage_logs import *
import os
import shutil
import numpy as np
import pandas as pd
from pathlib import Path

class TestLogRegister(unittest.TestCase):
    def setUp(self):
        self.path = Path('tests/temp/')
        try:
            shutil.rmtree(self.path)
        except FileNotFoundError:
            pass
        os.mkdir(self.path)
        self.reg = LogRegister.from_folder(self.path)


    def tearDown(self) -> None:
        shutil.rmtree(self.path)
        return super().tearDown()

    
    def test_get_log_register_create(self):
        self.assertEqual(len(self.reg.data), 0)

        self.assertEqual(self.reg.folder, self.path)

        files = os.listdir(self.path)
        self.assertEqual(len(files),1)

    def test_register_log(self):
        newlog = self.reg.register_log(Path('data/logs/00000150.BIN'))
        self.assertIsInstance(newlog, pd.Series)
        self.assertEqual(len(newlog.name),36)
        self.assertEqual(len([f for f in self.reg.folder.rglob('*.BIN')]), 1)
        self.assertEqual(len([f for f in self.reg.folder.rglob('*.csv')]), 1)

    def test_check_log_exists(self):
        self.assertFalse(self.reg.check_log_exists(Path('data/logs/00000150.BIN')))
        nlog  = self.reg.register_log(Path('data/logs/00000150.BIN'))
        self.assertEqual(len(self.reg.data), 1)
        self.assertTrue(self.reg.check_log_exists(Path('data/logs/00000150.BIN')))
        self.assertFalse(self.reg.check_log_exists(Path('data/logs/00000130.BIN')))
        with self.assertRaises(AssertionError):
            self.reg.check_log_exists(Path('data/logs/00000150.csv'))

    def test_append_metadata(self):
        self.reg.register_log(Path('data/logs/00000150.BIN'))
        self.reg.register_log(Path('data/logs/00000130.BIN'))
        self.reg.register_log(Path('data/logs/00000100.BIN'))
        self.reg.append_metadata(
            dict(stick_name='00000130.BIN'),
            dict(sequence='P21', standard='rubbish')
        )
        log = self.reg.select_logs(dict(stick_name='00000130.BIN'))
        self.assertEqual(log.iloc[0].sequence, 'P21')
        self.assertEqual(log.iloc[0].standard, 'rubbish')
        

    def test_get_or_register_log(self):
        newlog = self.reg.get_or_register_log(Path('data/logs/00000150.BIN'))
        self.assertEqual(len(self.reg.data), 1)
        newlog2 = self.reg.get_or_register_log(Path('data/logs/00000150.BIN'))
        self.assertEqual(newlog.all(), newlog2.all())
        self.assertEqual(len(self.reg.data), 1)

    def test_latest(self):
        self.reg.register_log(Path('data/logs/00000150.BIN'))
        self.assertEqual(self.reg.latest_log().stick_name, '00000150.BIN')
        self.reg.register_log(Path('data/logs/00000130.BIN'))
        self.assertEqual(self.reg.latest_log().stick_name, '00000130.BIN')
        self.reg.register_log(Path('data/logs/00000100.BIN'))
        self.assertEqual(self.reg.latest_log().stick_name, '00000100.BIN')

    def test_handles(self):
        self.reg.register_log(Path('data/logs/00000150.BIN'))
        self.reg.register_log(Path('data/logs/00000130.BIN'))
        self.reg.register_log(Path('data/logs/00000100.BIN'))

        hands = self.reg.handles(self.reg.data.iloc[:2])
        self.assertEqual(hands[0].csv, self.reg.folder / '{}.csv'.format(hands[0].name))

    def test_save_log(self):
        with open('data/logs/00000150.BIN', 'rb') as fp:
            log = self.reg.save_log(fp)
        self.assertEqual(len(self.reg.data), 1)
