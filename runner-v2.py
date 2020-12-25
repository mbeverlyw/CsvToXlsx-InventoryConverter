import SpreadsheetMigrator as sm


def main():
    """
    Intended Usage for SpreadsheetMigrator:

    migrator = sm.Migrator()

    reference_spreadsheet = Csv(<filepath>)
    target_spreadsheet = Xlsx(<filepath>)

    rules = {
        <target_column_name>: [
            <reference_column_name(s) (prioritized by order)>,
        ]
    }
    migrator.set_column_rules(rules)

    migrator.execute()
    """
    reference = sm.Csv('data/examples/test.csv')
    target = sm.Csv('data/examples/test_result.csv')
    
    migrator = sm.Migrator(reference, target)

    rules = {
        'Column A': 'Column 1',
        'Column B': ['Column 2', 'Column 3'],
    }
    migrator.set_column_rules(rules)
    migrator.execute()

    


if __name__ == "__main__":
    main()
