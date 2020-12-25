from .datatype_handler import (
    to_str, to_list
)

# TODO rework Rule to be a namedtuple and move to migrator.Migrator() class.
class Rule:
    target_column = None
    reference_columns = None


    def __init__(self, target_column, reference_columns):
        self._set_target_column(target_column)
        self._set_reference_columns(reference_columns)

    def _set_target_column(self, target_column):
        self.target_column = to_str(target_column)

    def _set_reference_columns(self, reference_columns):
        self.reference_columns = to_list(reference_columns)

    def _get_target_column(self):
        return self.target_column

    def _get_reference_columns(self):
        return self.reference_columns

    def apply(self, row):
        for column in self._get_reference_columns():
            cell = self.__get_cell_value(row, column)

            if not self.__is_empty(cell):
                return cell

        else:
            return None

    @staticmethod
    def __get_cell_value(row, column):
        try:
            return row[column]
        except KeyError:
            raise KeyError(f"{column} is not found in reference.")

    @staticmethod
    def __is_empty(val):
        if val == '':
            return True
        else:
            return False
    
    