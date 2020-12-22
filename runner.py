from InventoryImportCompiler import (
    StageLoader, CsvToXlsxConverter, XLSX
)

import datetime


def main():
    stage = StageLoader()

    if stage._staged_files_exist():
        process_staged_files(stage.staged_files)


def process_staged_files(staged_files):
    file_processor = Processor()

    for index, file in enumerate(staged_files):
        print(f"File Found: {file}")
        file_processor.set_csv(file)
        file_processor.generate_xlsx_data()

        create_importable_file(index, file_processor.generated_xlsx_data)


def create_importable_file(index, generated_xlsx_data):
    timestamp = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
    filepath = f'data/importable_spreadsheets/{timestamp}-{index}-importable_spreadsheet.xlsx'

    file = XLSX(filepath)
    file.set_data(generated_xlsx_data)
    file.create_file()


if __name__ == "__main__":
    main()
