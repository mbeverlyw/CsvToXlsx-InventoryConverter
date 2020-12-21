import unittest

from re import sub
from pathlib import Path

from .. import csv_compiler


class TestCsvObject(unittest.TestCase):
    def setUp(self):
        self.csv = csv_compiler._base.CSV('data\\stage\\generated_inventory.csv')

    def test_get_filename(self):
        # Test if filename gets expected filename
        self.assertEqual(self.csv.get_filename(), "generated_inventory.csv")

    def test_is_valid_filetype(self):
        # Test not .xlsx
        self.csv.path = Path(sub(r'\.csv', '.xlsx', self.csv.path.as_posix()))
        self.assertFalse(self.csv.is_valid_filetype())


class TestXlsxObject(unittest.TestCase):
    def setUp(self):
        self.xlsx = csv_compiler._base.XLSX('data\\stage\\generated_inventory.xlsx')

    def test_get_filename(self):
        # Test if filename gets expected filename
        self.assertEqual(self.xlsx.get_filename(), "generated_inventory.xlsx")

    def test_is_valid_filetype(self):
        # Test not .csv
        self.xlsx.path = Path(sub(r'\.xlsx', '.csv', self.xlsx.path.as_posix()))
        self.assertFalse(self.xlsx.is_valid_filetype())


class TestStageLoaderObject(unittest.TestCase):
    def setUp(self):
        self.stage = csv_compiler.stage_loader.StageLoader()

    def test_no_files_are_staged(self):
        self.assertRaises()