from re import match
from pathlib import Path
import pandas as pd

CSV_FILE_EXTENSION = r".*.[cC][sS][vV]$"
XLSX_FILE_EXTENSION = r".[xX][lL][sS][xX]$"


class CSV:
    def __init__(self, path, expected_file_ext=CSV_FILE_EXTENSION ):
        self.path = Path(path)
        self.expected_file_extension = expected_file_ext
        self.data = self.get_data() if self.is_valid_filetype() else None

    def get_filename(self):
        return self.path.name

    def is_valid_filetype(self):
        return match(self.expected_file_extension, self.get_filename())

    def get_data(self):
        return pd.read_csv(self.path)


class XLSX(CSV):
    def __init__(self, path):
        super().__init__(path, XLSX_FILE_EXTENSION)

