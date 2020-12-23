from pathlib import Path
from re import match


class File:
    path = None
    data = None
    expected_file_extension = None

    def __init__(self, filepath, expected_file_extension=None):
        self.path = Path(filepath)
        self.expected_file_extension = expected_file_extension

    def __str__(self):
        return f"{self.get_filename()}"

    def get_filename(self):
        return self.path.name

    def _has_expected_extension(self):
        """
        Uses a regex pattern to test if the 
            file extension is contained in filename
        """
        if self.__filename_contains_expected_extension():
            return True
        else:
            return False

    def __filename_contains_expected_extension(self):
        regex = self.__get_regex_for_file_extension()

        if match(regex, self.get_filename()):
            return True
        else:
            return False

    def __get_regex_for_file_extension(self):
        default_pattern = r".*"

        if self.expected_file_extension is None:
            return default_pattern
        else:
            return self.expected_file_extension

    def _get_data(self):
        return self.data
    
    def _set_data(self, data):
        if data is None:
            raise ValueError("Nonetype cannot be set for file")

        self.data = data
        return True
    
    def __set_data_is_empty(self):
        if self.data is None:
            return True
        else:
            return False

    def read(self):
        return self._read_data_from_file()
    
    def _read_data_from_file(self):
        with open(self.path, 'r+') as f:
            data = f.read()
        
        return data

    def write(self, data=None):
        try:
            self._set_data(data)

        except ValueError as e:
            if self.__set_data_is_empty():
                raise ValueError from e
            
        self._write_data_to_file()
        return True

    def _write_data_to_file(self):
        with open(self.path, 'w+') as f:
            f.write(self.data)
    

