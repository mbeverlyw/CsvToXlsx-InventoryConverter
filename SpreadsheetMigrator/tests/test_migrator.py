import unittest
import pandas as pd

from ..migrator.datatype_handler import (
    to_str, 
    to_list
)
from ..file_types import (
    Csv,
    Xlsx
)
from ..migrator import (
    Migrator,
    Rule
)



class TestDataTypeHandler(unittest.TestCase):
    def test_to_str_arg_types(self):
        expected_output = "12"
        # Test Int
        x = 12

        self.assertEqual(
            to_str(x),
            expected_output
        )

        # Test Str
        x = "12"

        self.assertEqual(
            to_str(x),
            expected_output
        )

        # Test Bool 
        x = True

        with self.assertRaises(TypeError):
            to_str(x)

        # Test None
        x = None

        with self.assertRaises(TypeError):
            to_str(x)

        # Test List
        x = [12]

        with self.assertRaises(TypeError):
            to_str(x)

        # Test Tuple
        x = (12, )

        with self.assertRaises(TypeError):
            to_str(x)

        # Test Dict
        x = {12: ''}

        with self.assertRaises(TypeError):
            to_str(x)
    
    def test_to_list_arg_types(self):
        expected_output = ["12"]
        # Test Int
        x = 12

        self.assertListEqual(
            to_list(x),
            expected_output
        )

        # Test Str
        x = "12"

        self.assertListEqual(
            to_list(x),
            expected_output
        )

        # Test Bool 
        x = True

        with self.assertRaises(TypeError):
            to_list(x)

        # Test None
        x = None

        with self.assertRaises(TypeError):
            to_list(x)

        # Test List
        x = [12]

        self.assertListEqual(
            to_list(x),
            expected_output
        )

        # Test Tuple
        x = (12, )

        self.assertListEqual(
            to_list(x),
            expected_output
        )

        # Test Dict
        x = {12: ''}

        with self.assertRaises(TypeError):
            to_list(x)
     

class TestRule(unittest.TestCase):
    def setUp(self):
        self.target_df = pd.DataFrame(
            {'Column A': []}
        )
        self.reference_df = Csv('data/examples/test.csv').read()
        self.rule = Rule(
            self.target_df.columns[0], 
            self.reference_df.columns[0]
            )
        self.rule_with_priority_list = Rule(
            self.target_df.columns[0], 
            [c for c in self.reference_df.columns]
        )
    

       
    def test_get_target_column(self):
        expected_output = self.target_df.columns[0]
        self.assertEqual(
            self.rule._get_target_column(),
            expected_output
        )
    
    def test_set_target_column_nonetype_arg(self):
        self.rule.reference_columns = None
        with self.assertRaises(TypeError):
            self.rule._set_target_column(None)

    def test_set_reference_columns_nonetype_arg(self):
        self.rule.reference_columns = None
        with self.assertRaises(TypeError):
            self.rule._set_reference_columns(None)
    
    def test_get_reference_columns_str_arg(self):
        expected_output = [self.reference_df.columns[0]]

        self.assertListEqual(
            self.rule._get_reference_columns(),
            expected_output
        )

    def test_get_reference_column_list_arg(self):
        expected_output = [str(c) for c in self.reference_df.columns]

        self.assertListEqual(
            self.rule_with_priority_list._get_reference_columns(),
            expected_output
        )

    def test_apply_ref_col_label_does_not_exist(self):
        self.rule.reference_columns = ['Imaginary Column']
        example_row = self.reference_df.iloc(0)[0]

        with self.assertRaises(KeyError):
            self.rule.apply(example_row)

    def test_apply_ref_col_val_is_nonetype(self):
        example_row = {
            'Column 1': None,
        }
        expected_output = None

        self.assertEqual(
            self.rule.apply(example_row),
            expected_output
        )

    def test_apply_ref_col_val_is_populated(self):
        example_row = self.reference_df.iloc(0)[0]
        expected_output = self.reference_df.get(
            self.reference_df.columns[0]
        )[0]

        self.assertEqual(
            self.rule.apply(example_row),
            expected_output
        )


class TestMigrator(unittest.TestCase):
    def setUp(self):
        self.csv_ref = Csv('data/test.csv')
        self.xlsx_ref = Xlsx('data/test.xls')
        self.csv_tar = Csv('data/test_result.csv')
        self.xlsx_tar = Xlsx('data/test_result.xls')

        self.migrator = Migrator(self.csv_ref, self.csv_tar)

        self.rules_arg = {
            'Column A': 'Column 3',
            'Column B': ['Column 1', 'Column 2'],
        }

    def test_set_column_rules(self):
        pass

    def test_set_column_rules_list_arg(self):
        rules_arg = ['Column A', 'Column B']


    def test_execute(self):
        pass