from InventoryImportCompiler import (
    StageLoader, CsvToXlsxConverter, XLSX
)

import datetime


def main():
    stage = StageLoader()
    file_processor = CsvToXlsxConverter()

    for index, file in enumerate(stage.get_staged_csv_files()):
        file_processor.set_csv(file)
        generated_xlsx_data = file_processor.generate_xlsx_data()

        create_importable_file(index, generated_xlsx_data)


def create_importable_file(index, generated_xlsx_data):
    timestamp = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
    filepath = f'data/importable_spreadsheets/{timestamp}-{index}-importable_spreadsheet.xlsx'

    file = XLSX(filepath)
    file.set_data(generated_xlsx_data)
    file.create_file()


if __name__ == "__main__":
    main()
