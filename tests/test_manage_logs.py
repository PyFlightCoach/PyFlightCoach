import unittest
from scripts.manage_logs import *
import os
import shutil
import numpy as np
import pandas as pd

class TestManageLogs(unittest.TestCase):
    def setUp(self):
        try:
            shutil.rmtree('tests/temp')
        except FileNotFoundError:
            pass
        os.mkdir('tests/temp')
    
    def tearDown(self) -> None:
        shutil.rmtree('tests/temp')
        return super().tearDown()

    
    def test_get_log_register_create(self):
        folder, reg = get_log_register('tests/temp/')
        self.assertEqual(len(reg), 0)
        self.assertEqual(folder, 'tests/temp/')
        files = os.listdir('tests/temp/')
        self.assertEqual(len(files),1)

    def test_find_logs(self):
        logs = find_logs('data/logs')
        self.assertEqual(len(logs), 9)


    def test_add_log(self):
        logstorage = get_log_register('tests/temp/')
        new_logs = add_logs(['data/logs/00000150.BIN'], logstorage)
        self.assertEqual(len(new_logs), 1)
        files = os.listdir('tests/temp/')
        self.assertEqual(len(files),3)
        
        logstorage = get_log_register('tests/temp/')
        new_logs = add_logs(['data/logs/00000150.BIN'], logstorage)
        self.assertEqual(len(new_logs), 0)
        files = os.listdir('tests/temp/')
        self.assertEqual(len(files),3)

