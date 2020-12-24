import unittest
import pandas as pd

from ..file_types import (
    Csv,
    Xlsx
)
from ..migrator import (
    Migrator,
    Rule
)



class TestRule(unittest.TestCase):
    def setUp(self):
        self.target_df = pd.DataFrame(
            {'Column A': []}
        )
        self.reference_df = pd.DataFrame(
            {
                'Column 1': ['1', '', '1', '1', ''],
                'Column 2': ['2', '', '2', '', '2'],
                'Column 3': ['3', '', '', '3', '3']
            }
        )
        self.rule = Rule('Column A', 'Column 1')
        self.rule_with_priority = Rule(
            'Column A', ['Column 1', 'Column 2', 'Column 3']
        )
    
    def test_get_target_column(self):
        pass

    def test_get_reference_columns(self):
        pass
    
    def test_get_reference_columns_str_arg(self):
        pass

    def test_get_reference_column_list_arg(self):
        pass

    def test_apply_ref_col_not_exist(self):
        pass

    def test_apply_ref_col_val_is_none(self):
        pass

    def test_apply_ref_col_val_is_populated(self):
        pass


class TestMigrator(unittest.TestCase):
    def setUp(self):
        pass

    