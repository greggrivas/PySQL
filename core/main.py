"""
This file will contain the logic for starting the main window as well as all the methods required.
"""
import os
import sys
import logging
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtSql import  QSqlDatabase, QSqlQuery


class PySQL(QtWidgets.QApplication):
    """
    Main class that handles ui and methods probably
    """
    def __init__(self, parent=None):
        super(PySQL, self).__init__(parent)
        self.logger = logging.getLogger(__name__)
        resource_object = QtCore.QResource()
        resource_file = resource_object.registerResource(os.path.abspath("UI/resources.rcc"))        
        if resource_file.bit_length() == 0:
            self.logger.error("Resources file could not be loaded. Program is exiting.")

        self.main_window = QtWidgets.QMainWindow() # Create the main GUI window or any other windows
        self.main_ui = self.ui_loader(':/ui_file/AppWindow', self.main_window) # Loading the respective UI files
        # The next two lines handle the button events.
        self.main_window.button_add.clicked.connect(self.add_expense)
        self.main_window.button_del.clicked.connect(self.del_expense)

        self.load_table()

    def  load_table(self):
        """
        Function that fills the table with the database data on launch.
        """
        self.main_window.table.setRowCount(0)
        query = QSqlQuery("SELECT * FROM expense")
        row = 0
        while query.next(): #while there is another row in the table iterate
            expense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)

            # Load the values to the table
            self.main_window.table.insertRow(row)
            self.main_window.table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
            self.main_window.table.setItem(row, 1, QTableWidgetItem(date))
            self.main_window.table.setItem(row, 2, QTableWidgetItem(category))
            self.main_window.table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.main_window.table.setItem(row, 4, QTableWidgetItem(description))
            row += 1

    def add_expense(self):
        """
        This function handles the logic behind the add expense button.
        """
        # The following lines handle the input from the user.
        date = self.main_window.dateEdit.date().toString("dd-MM-yyyy")
        category = self.main_window.comboBox.currentText()
        amount = self.main_window.lineEdit_amount.text()
        description = self.main_window.lineEdit_description.text()

        # The following lines insert the given data to the database.
        query = QSqlQuery()
        query.prepare("""
                      INSERT INTO expense (Date, Category, Amount, Description) 
                      VALUES (?, ?, ?, ?)
                      """)
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)

        # The following lines are used as a debug method by printing the values inputed plus the number of placeholders created by the query.
        # print(f"Values being inserted: {date}, {category}, {amount}, {description}")
        # print(f"Number of placeholders: {len(query.boundValues())}") # We use len() because .boundvalues returns a dictionary and not a list

        if not query.exec_():
            print("Error inserting data:", query.lastError().text())

        # The following lines reset the input boxes values.
        self.main_window.dateEdit.setDate(QDate.currentDate())
        self.main_window.comboBox.setCurrentIndex(0)
        self.main_window.lineEdit_amount.clear()
        self.main_window.lineEdit_description.clear()

        # The code below uses the PRAGMA command to retrieve data about the structure of the table such as columns, data types, etc as a debug feature
        # query = QSqlQuery()
        # query.exec_("PRAGMA table_info(expense)")
        # while query.next():
        #     print(query.value(1))  # Print column names
        self.load_table()

    def del_expense(self):
        """
        This function handles the logic behind the delete expense button.
        """
        selected_row = self.main_window.table.currentRow()
        if selected_row == -1: # in case the user hasn't chosen a row from the table
            QMessageBox.warning(self.main_window, "warning", "No expense chosen. Please choose a row.") # NOTE:QMessageBox takes a widget as an argument, so the main window usually!!
            return

        expense_id = int(self.main_window.table.item(selected_row,0).text()) # Here we select the id coloumn of the selected row from the table
        confirm = QMessageBox.question(self.main_window, "Warning", "Are you sure?", QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.No:
            return

        query = QSqlQuery()
        query.prepare("DELETE FROM expense WHERE id=?")
        query.addBindValue(expense_id)
        query.exec_()
        self.load_table()


    def show_app(self):
        """
        The method that shoes the ui
        """
        self.main_ui.show()

    @staticmethod
    def ui_loader(ui_resource, base=None):
        """ 
        A method that just loads ui file of the app.
        NOTE: changing the names in Designer means you must recompile the .qrc file!!!
        """
        ui_file = QtCore.QFile(ui_resource)
        ui_file.open(QtCore.QFile.ReadOnly) # 
        try:
            parsed_ui = uic.loadUi(ui_file, base)
            return parsed_ui
        finally:
            ui_file.close()



# Creating the Database
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("expense.db")
if not database.open():
    QMessageBox.critical(None, "Error. Could not find database.")
    sys.exit(1)

# Initial query
query = QSqlQuery()
query.exec_("""
            CREATE TABLE IF NOT EXISTS expense (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Date TEXT,
                Category TEXT,
                Amount REAL,
                Description TEXT
            )
            """)

# Run the Application
if __name__ == "__main__":
    app = PySQL(sys.argv)
    app.show_app()
    sys.exit(app.exec())
