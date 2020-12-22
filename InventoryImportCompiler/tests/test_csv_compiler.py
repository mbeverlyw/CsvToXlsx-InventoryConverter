import unittest

from re import sub
from pathlib import Path
import pandas as pd

from .. import (
    StageLoader,
    CsvToXlsxConverter,
    CSV,
    XLSX,
    )
from ..csv_compiler._base import SpreadsheetFile
from ..csv_compiler.exceptions import (
    NoFilesFoundInStage,
    NotCsvObject,
    ColumnNotFoundInMethodLink,
    NoTargetCsvObjectError,
)



class TestSpreadsheetFileObject(unittest.TestCase):
    def setUp(self):
        self.file = SpreadsheetFile('data/stage/generated_inventory.csv')

    def test_get_filename(self):
        # Test if filename gets expected filename
        self.assertEqual(self.file.get_filename(), "generated_inventory.csv")


class TestCsvObject(unittest.TestCase):
    def setUp(self):
        self.csv = CSV(
            'data/stage/generated_inventory.csv'
            )
    
    def test_csv_is_valid_filetype(self):
        # Test vs .csv
        self.assertTrue(self.csv.is_valid_filetype())
    
    def test_xlsx_is_invalid_filetype(self):
        # Test vs .xlsx
        self.csv.path = Path(sub(r'\.csv', '.xlsx', self.csv.path.as_posix()))
        self.assertFalse(self.csv.is_valid_filetype())


class TestXlsxObject(unittest.TestCase):
    def setUp(self):
        self.xlsx = XLSX(
            'data/stage/generated_inventory.xlsx'
            )

    def test_xlsx_is_valid_filetype(self):
        # Test vs .xlsx
        self.assertTrue(self.xlsx.is_valid_filetype())

    def test_csv_is_invalid_filetype(self):
        # Test vs .csv
        self.xlsx.path = Path(sub(r'\.xlsx', '.csv', self.xlsx.path.as_posix()))
        self.assertFalse(self.xlsx.is_valid_filetype())


class TestStageLoaderObject(unittest.TestCase):
    def setUp(self):
        self.stage = StageLoader()

    def test_for_stage_dir_exists(self):
        # Test if the stage directory exists
        self.assertTrue(self.stage._stage_exists())
    
    def test_for_exception_stage_dir_containing_no_files(self):
        staged_files = []
        with self.assertRaises(
            NoFilesFoundInStage
            ):
            self.stage._staged_files_exist(staged_files)
        
    def test_for_all_xlsx_in_stage_dir_get_staged_csv_files(self):
        staged_files = [
            Path('data/generated_inventory.xls')
        ]
        expected_list = []

        self.assertListEqual(
            self.stage.get_staged_csv_files(staged_files),
            expected_list
            )
        
    def test_for_csv_in_stage_dir_get_staged_csv_files(self):
        staged_files = [
            Path('data/generated_inventory.csv')
        ]
        expected_list_count = 1

        self.assertEqual(
            len(
                self.stage.get_staged_csv_files(staged_files)
            ),
            expected_list_count
            )


class TestCsvToXlsxConverter(unittest.TestCase):
    def setUp(self):
        self.ctx = CsvToXlsxConverter()
        self.csv_obj = CSV(
            'data/stage/generated_inventory.csv'
        )
        self.csv_df = pd.DataFrame({
            'Product Title': ['test1', 'test2'],
            'upc': ['0123', '0124'],
            'sku': ['0011', '0022'],
            'Manufacturer Product Id': ['a1', 'a2'],
            })

    def test_not_empty_is_empty(self):
        cell_val = "not empty"
        self.assertFalse(self.ctx._is_empty(cell_val))

    def test_is_None_is_empty(self):
        cell_val = None
        self.assertTrue(self.ctx._is_empty(cell_val))

    def test_empty_is_empty(self):
        cell_val = ""
        self.assertTrue(self.ctx._is_empty(cell_val))
    
    def test_is_csv_object_instance_set_csv(self):
        self.assertTrue(
            self.ctx.set_csv(self.csv_obj))
    
    def test_not_csv_object_instance_set_csv(self):
        with self.assertRaises(NotCsvObject):
            self.ctx.set_csv(
                'data/stage/generated_inventory.csv')

    def test_is_csv_object_not_csv_file_set_csv(self):
        self.csv_obj = CSV(
            'data/stage/generated_inventory.xls'
        )
        with self.assertRaises(NotCsvObject):
            self.ctx.set_csv(self.csv_obj)
        
    def test_no_csv_set_data_extract_csv_data(self):
        with self.assertRaises(NoTargetCsvObjectError):
            self.ctx.extract_csv_data()
        
    def test_is_csv_data_extract_csv_data(self):
        self.ctx.set_csv(self.csv_obj)

        self.assertTrue(
            self.ctx.extract_csv_data()
        )

    def test_csv_data_not_available_generate_xlsx_data(self):
        with self.assertRaises(NoTargetCsvObjectError):
            self.ctx.generate_xlsx_data()

    def test_xlsx_data_created_generate_xlsx_data(self):
        self.ctx.set_csv(self.csv_obj)

        self.assertIsInstance(
            self.ctx.generate_xlsx_data(),
            pd.DataFrame
        )

    def test_create_blank_xlsx_dataframe(self):
        columns = ['A', 'B']

        self.assertIsInstance(
            self.ctx._create_blank_xlsx(columns),
            pd.DataFrame
        )

    def test_correct_blank_generated_row(self):
        columns = ['A', 'B']
        expected_result = {
            'A': None,
            'B': None,
        }

        self.assertDictEqual(
            self.ctx._get_blank_generated_row(columns),
            expected_result
        )

    def test_csv_row_blank_insert_extracted_row_data(self):
        csv_row = {
            'Product Title': '',
            'upc': '',
            'sku': '',
            'Manufacturer Product Id': '',
        }
        blank_row = self.ctx._get_blank_generated_row(
            ['TITLE', 'BARCODE']
        )
        expected_output = {
            'TITLE': '',
            'BARCODE': '',
        }

        self.assertDictEqual(
            self.ctx._insert_extracted_row_data(
                blank_row, csv_row
            ),
            expected_output
        )

    def test_csv_row_contains_null_cell_insert_extracted_row_data(self):
        csv_row = {
            'Product Title': 'title',
            'upc': '',
            'sku': '',
            'Manufacturer Product Id': '',
        }
        blank_row = self.ctx._get_blank_generated_row(
            ['TITLE', 'BARCODE']
        )
        expected_output = {
            'TITLE': 'title',
            'BARCODE': '',
        }

        self.assertDictEqual(
            self.ctx._insert_extracted_row_data(
                blank_row, csv_row
            ),
            expected_output
        )

    def test_csv_row_populated_insert_extracted_row_data(self):
        csv_row = {
            'Product Title': 'title',
            'upc': 'upc',
            'sku': 'sku',
            'Manufacturer Product Id': 'manu_id',
        }
        blank_row = self.ctx._get_blank_generated_row(
            ['TITLE', 'BARCODE']
        )
        expected_output = {
            'TITLE': 'title',
            'BARCODE': 'upc',
        }

        self.assertDictEqual(
            self.ctx._insert_extracted_row_data(
                blank_row, csv_row
            ),
            expected_output
        )

    def test_no_method_links_get_method_to_get_column_val(self):
        self.ctx.column_to_method_link = {}
        column_label = 'BARCODE'

        with self.assertRaises(ColumnNotFoundInMethodLink):
            self.ctx._get_method_to_get_column_val(column_label)
    
    def test_linked_methods_get_method_to_get_column_val(self):
        column_label = 'BARCODE'

        self.assertEqual(
            self.ctx._get_method_to_get_column_val(column_label),
            self.ctx._get_barcode_from_row
        )
        
    def test_title_empty_get_title_from_row(self):
        self.csv_df = pd.DataFrame({
            'Product Title': ['test1', ''],
            'upc': ['0123', '0124'],
            'sku': ['0011', '0022'],
            'Manufacturer Product Id': ['a1', 'a2'],
            })
            
        for index, row in self.csv_df.iterrows():
            self.assertEqual(
                self.ctx._get_title_from_row(row),
                row['Product Title']
            )

    def test_title_present_get_title_from_row(self):
        for index, row in self.csv_df.iterrows():
            self.assertEqual(
                self.ctx._get_title_from_row(row),
                row['Product Title']
            )

    def test_no_csv_barcodes_available_get_barcode_from_row(self):
        barcode_set = {
            'upc': '',
            'sku': '',
            'Manufacturer Product Id': '',
            }
        self.assertEqual(
            self.ctx._get_barcode_from_row(barcode_set), 
            ''
        )

    def test_upc_available_get_barcode_from_row(self):
        barcode_set = {
            'upc': '0123upc',
            'sku': '',
            'Manufacturer Product Id': '',
            }
        self.assertEqual(
            self.ctx._get_barcode_from_row(barcode_set), 
            '0123upc'
        )

    def test_sku_available_get_barcode_from_row(self):
        barcode_set = {
            'upc': '',
            'sku': '0011sku',
            'Manufacturer Product Id': '',
            }
        self.assertEqual(
            self.ctx._get_barcode_from_row(barcode_set), 
            '0011sku'
        )

    def test_manu_id_available_get_barcode_from_row(self):
        barcode_set = {
            'upc': '',
            'sku': '',
            'Manufacturer Product Id': 'a1manuID',
            }
        self.assertEqual(
            self.ctx._get_barcode_from_row(barcode_set), 
            'a1manuID'
        )

    def test_upc_sku_available_get_barcode_from_row(self):
        barcode_set = {
            'upc': '0123upc',
            'sku': '0011sku',
            'Manufacturer Product Id': '',
            }
        self.assertEqual(
            self.ctx._get_barcode_from_row(barcode_set), 
            '0123upc'
        )

    def test_upc_manu_id_available_get_barcode_from_row(self):
        barcode_set = {
            'upc': '0123upc',
            'sku': '',
            'Manufacturer Product Id': 'a1manuID',
            }
        self.assertEqual(
            self.ctx._get_barcode_from_row(barcode_set), 
            '0123upc'
        )

    def test_sku_manu_id_available_get_barcode_from_row(self):
        barcode_set = {
            'upc': '',
            'sku': '0011sku',
            'Manufacturer Product Id': 'a1manuID',
            }
        self.assertEqual(
            self.ctx._get_barcode_from_row(barcode_set), 
            'a1manuID'
        )

    def test_all_available_get_barcode_from_row(self):
        barcode_set = {
            'upc': '0123upc',
            'sku': '0011sku',
            'Manufacturer Product Id': 'a1manuID',
            }
        self.assertEqual(
            self.ctx._get_barcode_from_row(barcode_set), 
            '0123upc'
        )


