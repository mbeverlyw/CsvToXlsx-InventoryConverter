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
    pass


if __name__ == "__main__":
    main()
