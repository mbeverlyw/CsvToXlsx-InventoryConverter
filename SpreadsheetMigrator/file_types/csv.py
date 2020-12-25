import pandas as pd

from . import File


FILE_EXTENSION_REGEX = r".*.[cC][sS][vV]$"


class Csv(File):
    #TODO insert type hints for functions 
    def __init__(self, filepath):
        super().__init__(filepath, FILE_EXTENSION_REGEX)

    def _read_data_from_file(self):
        return pd.read_csv(self.path)

    def _write_data_to_file(self):
        self.data.to_csv(self.path, index=False)
    