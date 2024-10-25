import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

import sqlite3

# Connect to the SQLite database (.db file)
conn = sqlite3.connect('expense.db')

# Create a cursor object
cursor = conn.cursor()

# Execute a SQL query to fetch all rows from a table
cursor.execute("SELECT * FROM expense")

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)
    print("\n")

# Close the connection
conn.close()






# class MyApp(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle('QMessageBox Example')
#         self.setGeometry(100, 100, 300, 200)

#         self.button = QPushButton('Show Message', self)
#         self.button.clicked.connect(self.show_message)
#         self.button.setGeometry(100, 80, 100, 30)

#     def show_message(self):
#         # Create a QMessageBox instance
#         msg = QMessageBox()
#         msg.setIcon(QMessageBox.Information)  # Set the icon
#         msg.setText("Hello! This is a message box.")  # Set the text
#         msg.setWindowTitle("Message Box Title")  # Set the title
#         msg.setStandardButtons(QMessageBox.Ok)  # Add an OK button

#         # Show the message box and wait for the user to close it
#         msg.exec_()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MyApp()
#     window.show()
#     sys.exit(app.exec_())
