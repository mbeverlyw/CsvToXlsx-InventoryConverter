import pandas as pd
from re import sub

from . import CSV
from .exceptions import (
    NotCsvObject,
    ColumnNotFoundInMethodLink,
    NoTargetCsvObjectError,
)


# XLSX Columns
XLSX_PRODUCT_TITLE = 'TITLE'
XLSX_BARCODE = 'BARCODE'
XLSX_COLUMNS = [
    XLSX_PRODUCT_TITLE, 
    XLSX_BARCODE
    ]

# Noteworthy CSV Columns 
CSV_PRODUCT_TITLE = 'Product Title'
CSV_UPC = 'upc'
CSV_SKU = 'sku'
CSV_MANU_ID = 'Manufacturer Product Id'

COLUMNS_TO_EXTRACT = [
    CSV_PRODUCT_TITLE, 
    CSV_UPC, 
    CSV_SKU, 
    CSV_MANU_ID
    ]

CSV_BARCODES_PER_PRIORITY = [CSV_UPC, CSV_MANU_ID, CSV_SKU]


class CsvToXlsxConverter:
    csv_file = None
    extracted_csv_data = None
    generated_xlsx_data = None
    column_to_method_link = None

    def __init__(self):
        self.column_to_method_link = {
            XLSX_PRODUCT_TITLE: self._get_title_from_row,
            XLSX_BARCODE: self._get_barcode_from_row,
        }
    
    def set_csv(self, csv_file):
        def _is_CSV_instance():
            return isinstance(csv_file, CSV)
        
        def _is_valid_CSV():
            return csv_file.is_valid_filetype()

        def _save_set_action():
            self.csv_file = csv_file
            return True

        if _is_CSV_instance() and _is_valid_CSV():
            return _save_set_action()

        else:
            raise NotCsvObject("Object type is not compatible")

    def extract_csv_data(self):            
        try:
            self.extracted_csv_data = pd.DataFrame(
                self.csv_file.data, 
                columns=COLUMNS_TO_EXTRACT
                )

        except AttributeError:
            raise NoTargetCsvObjectError
        
        return True  
    
    def generate_xlsx_data(self):
        self.extract_csv_data()

        generated_xlsx_data = self._create_blank_xlsx(XLSX_COLUMNS)

        for index, csv_row in self.extracted_csv_data.iterrows():
            generated_row = self._get_blank_generated_row(XLSX_COLUMNS)
            
            generated_row = self._insert_extracted_row_data(generated_row, csv_row)
            
            generated_xlsx_data = generated_xlsx_data.append(
                generated_row, ignore_index=True
                )

        return generated_xlsx_data

    @staticmethod
    def _get_blank_generated_row(column_labels):
        blank_row = {
            column_label: None for column_label in column_labels
            }
        return blank_row

    @staticmethod
    def _create_blank_xlsx(column_labels):
        blank_xlsx = pd.DataFrame(columns=column_labels)
        return blank_xlsx

    def _insert_extracted_row_data(self, generated_row, csv_row):
        populated_row = generated_row.copy()

        for column_label, value in generated_row.items():
            get_column_val_method = self._get_method_to_get_column_val(column_label)
            value = get_column_val_method(csv_row)

            populated_row[column_label] = value
        
        return populated_row

    def _get_method_to_get_column_val(self, column_label):
        try:
            return self.column_to_method_link[column_label]
        except KeyError:
            raise ColumnNotFoundInMethodLink

    @staticmethod
    def _get_title_from_row(row):
        return row[CSV_PRODUCT_TITLE]

    @classmethod
    def _get_barcode_from_row(cls, row):
        def cleaned_data(__row):
            return sub(r"\"|=", "", __row)

        for barcode_type in CSV_BARCODES_PER_PRIORITY:
            barcode_val = cleaned_data(row[barcode_type])

            if not cls._is_empty(barcode_val):
                return barcode_val
        else:
            return ""

    @staticmethod
    def _is_empty(cell_value):
        if (cell_value == "" or cell_value is None):
            return True
        else:
            return False



