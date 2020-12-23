from .migrator_rules import Rule


class Migrator:
    reference_file = None
    target_file = None
    column_rules = None

    def __init__(self):
        pass
    
    def execute(self):
        pass

    def __get_column_rules()
        return self.column_rules

    def set_column_rules(self, rules):
        self.column_rules = self.__create_rules_from_list(rules)
    
    def __create_rules_from_list(self, rules)
        rules = []

        for target_col, ref_cols in rules.items():
            rules.append(Rule(target_col, ref_cols))
        
        return rules
    
