import os
import shutil
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from cfg.database import Database
from gspread.utils import ExportFormat
import xlwings as xw
import openpyxl

db = Database('cfg/database')


def overwriting_data():
    link = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    my_creds = ServiceAccountCredentials.from_json_keyfile_name("cfg/CarDpAPI.json", link)
    client = gspread.authorize(my_creds)

    all_values_sheet = client.open('Car_dp').get_worksheet(0).get_all_values()[1::]
    db.del_all_users()
    db.add_dada_sheet(all_values_sheet)

    shutil.rmtree("all_file_excel")
    os.mkdir("all_file_excel")
    
    all_sheets = client.open("Car_dp").export(format=ExportFormat.EXCEL)
    with open('all_file_excel/output.xlsx', 'wb') as f:
        f.write(all_sheets)


    # try:
    with xw.App(visible=False) as excel_app:
        wb = excel_app.books.open('all_file_excel/output.xlsx')
        for sheet in wb.sheets:
            if sheet.name != "Настройки":
                wb_new = xw.Book()
                sheet.copy(after=wb_new.sheets[0])
                wb_new.sheets[0].delete()
                wb_new.save(f'all_file_excel/{sheet.name} Всё время.xlsx')
                wb_new.close()
        excel_app.quit()
    # except Exception as ex:
        # print(ex)

    os.remove("all_file_excel/output.xlsx")

    all_file = os.listdir("all_file_excel")
    for file in all_file:
        if file[-14:-1] == "Всё время.xls":
            # Неделя
            wb = openpyxl.load_workbook(f"all_file_excel/{file}")
            sheet = wb.active

            rows_to_delete = list(range(6, sheet.max_row - 1))

            for row in reversed(rows_to_delete):
                if sheet.cell(row, 1).value is not None:
                    if row != sheet.max_row:
                        if row - 1 > 5:
                            sheet.delete_rows(row - 1)

            wb.save(f'all_file_excel/{file[:-15]} Неделя.xlsx')

            # Месяц
            wb = openpyxl.load_workbook(f"all_file_excel/{file}")
            sheet = wb.active

            rows_to_delete = list(range(6, sheet.max_row - 4))

            for row in reversed(rows_to_delete):
                if sheet.cell(row, 1).value is not None:
                    if row != sheet.max_row:
                        if row - 4 > 5:
                            sheet.delete_rows(row - 4)

            wb.save(f'all_file_excel/{file[:-15]} Месяц.xlsx')


if __name__ == '__main__':
    overwriting_data()
