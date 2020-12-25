import pandas as pd

from . import File


FILE_EXTENSION_REGEX = r".*.[xX][lL][sS][xX]$|.*.[xX][lL][sS]$"


class Xlsx(File):
    def __init__(self, filepath):
        super().__init__(filepath, FILE_EXTENSION_REGEX)

    def _read_data_from_file(self):
        return pd.read_excel(self.path)

    def _write_data_to_file(self):
        self.data.to_excel(self.path, index=False)
    