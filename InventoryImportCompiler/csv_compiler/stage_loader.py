from pathlib import Path

from ._base import CSV


STAGE_DIR = Path('data/stage/')


class StageLoader:
    staged_files = []

    def __init__(self):
        self._stage_exists()

        if self._staged_files_exist():
            self.staged_files = self.get_staged_csv_files()
            

    def _get_staged_files(self):
        return STAGE_DIR.glob('*')

    def _stage_exists(self):
        try:
            STAGE_DIR.mkdir()
        except FileExistsError:
            pass

        return True

    def _staged_files_exist(self):
        files_in_stage_dir = list(self._get_staged_files())
        
        if len(files_in_stage_dir) > 0:
            return True
        else:    
            return False

    def get_staged_csv_files(self):
        valid_staged_files = []
        files_in_stage_dir = self._get_staged_files()

        for file in files_in_stage_dir:
            f = CSV(file)

            if f.is_valid_filetype():
                valid_staged_files.append(f)
            else:
                print(f"{f} is not a valid filetype - skipping file.")

        return valid_staged_files


