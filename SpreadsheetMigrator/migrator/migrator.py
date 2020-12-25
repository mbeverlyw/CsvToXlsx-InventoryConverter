import pandas as pd 

from .migrator_rules import Rule
from ..file_types import Csv, Xlsx



class Migrator:
    reference = None
    target = None
    column_rules = None

    def __init__(self, reference, target):
        self.__verify_args([reference, target])
        self._set_reference(reference)
        self._set_target(target)

    def _set_reference(self, reference):
        self.reference = reference

    def _set_target(self, target):
        self.target = target

    def set_column_rules(self, rules):
        self.column_rules = self.__extract_rules(rules)
    
    def __get_column_rules(self):
        return self.column_rules

    @staticmethod
    def __extract_rules(rules):
        rules_list = []

        for target_col, ref_cols in rules.items():
            rules_list.append(
                Rule(target_col, ref_cols)
                )
        
        return rules_list
    
    def execute(self):
        
        target_columns = [
            rule.target_column for rule in self.column_rules
            ]

        target_data = pd.DataFrame(
            columns=target_columns
            )

        reference_data = self.reference.read()

        for index, row in reference_data.iterrows():
            target_row = {}

            for rule in self.column_rules:
                target_row[rule.target_column] = rule.apply(row)

            target_data = target_data.append(target_row, ignore_index=True)

        print(target_data)

    @staticmethod
    def __verify_args(args):
        for obj in args:
            if not isinstance(obj, (Csv, Xlsx)):
                raise TypeError(f"{obj} is not a Csv or Xlsx object.")
    
