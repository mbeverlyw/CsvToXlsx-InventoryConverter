import pandas as pd 

from .migrator_rules import Rule
from ..file_types import Csv, Xlsx


class Migrator:
    #TODO insert type hints for functions 
    reference = None
    target = None
    column_rules = None  # set as a list of namedtuples

    def __init__(self, reference_file: (Csv, Xlsx), target_file: (Csv, Xlsx)):
        self.__verify_args([reference_file, target_file])
        self._set_reference(reference_file)
        self._set_target(target_file)

    def _set_reference(self, reference):
        self.reference = reference

    def _set_target(self, target):
        self.target = target

    def set_column_rules(self, rules):
        self.column_rules = self.__extract_rules_from_dict(rules)
    
    def __get_column_rules(self):
        return self.column_rules

    @staticmethod
    def __extract_rules_from_dict(rules):
        # TODO Have the Rule class assignment be replaced with a namedtuple assignment
        rules_list = []

        for target_col, ref_cols in rules.items():
            rules_list.append(
                Rule(target_col, ref_cols)
                )
        
        return rules_list
    
    def execute(self):
        # TODO extract target_columns as a function or find a better way.
        target_columns = [
            rule.target_column for rule in self.column_rules
            ]

        #TODO extract _target_data as a function
        target_data = pd.DataFrame(
            columns=target_columns
            )

        # TODO extract reference_data as a function
        reference_data = self.reference.read()

        # TODO extract processing as a function
        for index, row in reference_data.iterrows():
            # TODO refactor as a generator
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
    
