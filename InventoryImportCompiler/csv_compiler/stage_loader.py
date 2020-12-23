from pathlib import Path

from ._base import CSV
from .exceptions import NoFilesFoundInStage


STAGE_DIR = Path('data/stage/')


class StageLoader:
    staged_files = []

    def __init__(self):
        if self._stage_exists():
            files = list(
                self._get_staged_files()
            )

        if self._staged_files_exist(files):
            self.staged_files = self.get_staged_csv_files(files)
        

    def _get_staged_files(self):
        return STAGE_DIR.glob('*')

    def _stage_exists(self):
        try:
            STAGE_DIR.mkdir()
        except FileExistsError:
            # Stage Exists, returning True
            pass

        return True

    def _staged_files_exist(self, files_in_stage_dir):        
        if len(files_in_stage_dir) > 0:
            return True
        else:    
            raise NoFilesFoundInStage

    def get_staged_csv_files(self, files_in_stage_dir=None):
        def _knows_files_in_stage_dir():
            if files_in_stage_dir is None:
                return False
            else:
                return True
        
        if not _knows_files_in_stage_dir():
            files_in_stage_dir = self._get_staged_files()

        valid_staged_files = []

        for file in files_in_stage_dir:
            f = CSV(file)

            if f.is_valid_filetype():
                valid_staged_files.append(f)
            else:
                print(f"{f} is not a valid filetype - skipping file.")

        return valid_staged_files


