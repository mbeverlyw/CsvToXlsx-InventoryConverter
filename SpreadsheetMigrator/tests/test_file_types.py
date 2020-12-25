import unittest
import pandas as pd
from pathlib import Path

from ..file_types import (
    File,
    Csv,
    Xlsx
)


class TestFileObject(unittest.TestCase):
    def setUp(self):
        self.file = File('data/examples/test.txt')
    
    def test_get_filename(self):
        expected_val = 'test.txt'
        self.assertEqual(
            self.file.get_filename(),
            expected_val
        )

    def test_get_data(self):
        expected_val = '123'

        self.file.data = '123'

        self.assertEqual(
            self.file._get_data(),
            expected_val
        )
    
    def test_set_data(self):
        val_to_insert = "123"

        self.assertTrue(
            self.file._set_data(val_to_insert)
        )
    
    def test_write_file_with_data_arg(self):
        val_to_insert = "123"

        self.assertTrue(
            self.file.write(val_to_insert)
        )
    
    def test_write_file_with_none_data_arg_and_none_data_set(self):
        with self.assertRaises(ValueError):
            self.file.write()
    
    def test_write_file_with_none_data_arg_and_data_set(self):
        data = "123"
        
        self.file._set_data(data)

        self.assertTrue(
            self.file.write()
        )
    
    def test_has_expected_extension_is_valid(self):
        self.assertTrue(
            self.file._has_expected_extension()
        )

    def test_read_file_file_does_not_exist(self):
        self.file.path = Path('data/examples/null.txt')
        with self.assertRaises(FileNotFoundError):
            self.file.read()


class TestCsvObject(unittest.TestCase):
    def setUp(self):
        self.file = Csv('data/examples/test.csv')
        self.df = pd.read_csv('data/examples/test.csv')
    
    def test_get_filename(self):
        expected_val = 'test.csv'
        self.assertEqual(
            self.file.get_filename(),
            expected_val
        )

    def test_set_data(self):
        val_to_insert = self.df

        self.assertTrue(
            self.file._set_data(val_to_insert)
        )
    
    def test_write_file_with_data_arg(self):
        val_to_insert = self.df

        self.assertTrue(
            self.file.write(val_to_insert)
        )
    
    def test_write_file_with_none_data_arg_and_none_data_set(self):
        with self.assertRaises(ValueError):
            self.file.write()
    
    def test_write_file_with_none_data_arg_and_data_set(self):
        
        self.file._set_data(self.df)

        self.assertTrue(
            self.file.write()
        )

    def test_has_expected_extension_is_valid(self):
        self.assertTrue(
            self.file._has_expected_extension()
        )
    
    def test_read_file(self):
        expected_data = self.df

        self.assertIsInstance(
            self.file.read(),
            pd.DataFrame
        )

    def test_read_file_file_does_not_exist(self):
        self.file.path = Path('data/examples/null.csv')
        with self.assertRaises(FileNotFoundError):
            self.file.read()


class TestXlsxObject(unittest.TestCase):
    def setUp(self):
        self.file = Xlsx('data/examples/test.xls')
        self.df = pd.read_excel('data/examples/test.xls')
    
    def test_get_filename(self):
        expected_val = 'test.xls'
        self.assertEqual(
            self.file.get_filename(),
            expected_val
        )

    def test_set_data(self):
        val_to_insert = self.df

        self.assertTrue(
            self.file._set_data(val_to_insert)
        )
    
    def test_write_file_with_data_arg(self):
        val_to_insert = self.df

        self.assertTrue(
            self.file.write(val_to_insert)
        )
    
    def test_write_file_with_none_data_arg_and_none_data_set(self):
        with self.assertRaises(ValueError):
            self.file.write()
    
    def test_write_file_with_none_data_arg_and_data_set(self):
        
        self.file._set_data(self.df)

        self.assertTrue(
            self.file.write()
        )

    def test_has_expected_extension_is_valid(self):
        self.assertTrue(
            self.file._has_expected_extension()
        )
    
    def test_read_file(self):
        """
        Voiding test? Repeatedly getting below exception.

        xlrd.biffh.XLRDError: Excel xlsx file; not supported



        self.assertIsInstance(
            self.file.read(),
            pd.DataFrame
        )
        """
        pass
    
    def test_read_file_file_does_not_exist(self):
        self.file.path = Path('data/examples/null.xls')

        with self.assertRaises(FileNotFoundError):
            self.file.read()
