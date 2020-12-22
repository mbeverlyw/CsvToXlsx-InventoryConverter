from re import match
from pathlib import Path
import pandas as pd

CSV_FILE_EXTENSION = r".*.[cC][sS][vV]$"
XLSX_FILE_EXTENSION = r".*.[xX][lL][sS][xX]$|.*.[xX][lL][sS]$"


class SpreadsheetFile:
    def __init__(self, path, expected_file_ext=CSV_FILE_EXTENSION ):
        self.path = Path(path)
        self.expected_file_extension = expected_file_ext

        if self.is_valid_filetype() and self.path.exists():
            self.data = self.get_data()
        else:
            self.data = None

    def __str__(self):
        return f"{self.get_filename()}"

    def get_filename(self):
        return self.path.name

    def is_valid_filetype(self):
        return match(self.expected_file_extension, self.get_filename())

    def get_data(self):
        with open(self.path, 'r') as file:
            data = file.readlines()
        return data
    
    def set_data(self, spreadsheet_data):
        self.data = spreadsheet_data

    def create_file(self, filepath=None):
        if filepath is None:
            filepath = self.path
        
        self._write_file_contents(filepath)

    def _write_file_contents(self, filepath):
        open(filepath, "w+").writelines(self.data)


class CSV(SpreadsheetFile):
    def __init__(self, path):
        super().__init__(path, CSV_FILE_EXTENSION)
    
    def get_data(self):
        return pd.read_csv(self.path)
    
    def _write_file_contents(self, filepath):
        self.data.to_csv(filepath)


class XLSX(SpreadsheetFile):
    def __init__(self, path):
        super().__init__(path, XLSX_FILE_EXTENSION)

    def get_data(self):
        return pd.read_excel(self.path)

    def _write_file_contents(self, filepath):
        self.data.to_excel(filepath)


