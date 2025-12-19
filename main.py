from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, \
	QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget

from PyQt6.QtGui import QAction

import sys

# QMainWindow allows to create multiple interconnected windows
# While QWidget only allows us to create a single one
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Student Management System")
		
		file_menu_item = self.menuBar().addMenu("&File")
		help_menu_item = self.menuBar().addMenu("&Help")

		add_student_action = QAction("Add Student", self)
		file_menu_item.addAction(add_student_action)
		
		about_action = QAction("About", self)
		help_menu_item.addAction(about_action)
		# Do this if and only if you do not see help menu
		# about_action.setMenuRole(QAction.MenuRole.NoRole)
	
		# Create table to display student database
		self.table = QTableWidget()
		self.table.setColumnCount(4)
		self.table.setHorizontalHeaderLabels((
			"ID", "Name", "Course", "Mobile"
		))
		self.setCentralWidget(self.table)
		
	def load_data(self):
		pass
		

if __name__ == "__main__":
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	sys.exit(app.exec())