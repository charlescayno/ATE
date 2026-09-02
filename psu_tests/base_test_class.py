# from psu_tests.ui_definitions import *
# from psu_tests.definitions import *

from psu_tests.test_object_imports import *

from PySide2.QtCore import Signal, Slot, QObject

class BaseTestObject(QObject):
    title = "Base"
    i2c_test = False

    # Signals
    message = Signal(str,str,MessageType)
    progress = Signal(float)
    estimated_time = Signal(float)
    status_update = Signal(TestStatus)

    # Signal for sending test data needed by test results page
    test_data_update = Signal(list)

   # General UI Definitions
    ui_definitions = General_UI_Definitions()


class TableHeader():
    def __init__(self):
        self.columns = []
        self.header_list = []

    def add_columns(self, fl:str, sl:list):
        """Add a column
        
        fl = first_level_txt
        sl = second_level_txt

        First row with merged cells based on number of second level items"""


        col = [fl, sl]
        self.columns.append(col)
    
    def get_header_list(self):
        """Get a list of all headers"""
        self.header_list = []

        for col in self.columns:
            sl = col[1]
            for item in sl:
                self.header_list.append(item)
        
        return self.header_list

    def add_header_to_sheet(self, worksheet, workbook, data_file_path):
        
        ws:Worksheet = worksheet
        wb:Workbook = workbook

        row_index = 4
        col_start_index = 2

        for col in self.columns:
            fl = col[0]
            sl = col[1]
            col_count = len(sl)
            col_end_index = col_start_index + col_count

            # Merge cells based on the number of second level cells under first level
            ws.merge_cells(
                start_row = row_index, end_row = row_index,
                start_col = col_start_index, end_col = col_end_index)

            ws.cell(row = row_index, column = col_start_index).value = fl
            
            # Loop through second level items to also place the second level headers
            for i, item in enumerate(sl):
                ws.cell(row=row_index, column=col_start_index+i).value = item

            col_start_index = col_end_index+1
            
            
        wb.save(self.data_file_path)
        wb.close

