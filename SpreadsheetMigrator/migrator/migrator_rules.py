



class Rule:
    target_column = None
    reference_columns = None


    def __init__(self, target_column, reference_columns):
        self.target_column = target_column
        self.reference_columns = reference_columns

    def __get_target_column(self):
        return self.target_column

    def __get_reference_columns(self):
        return self.reference_columns

    def apply(self, row):

        for r_col in self.__get_reference_columns():
            pass

    