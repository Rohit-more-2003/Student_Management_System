from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, \
	QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, \
	QTableWidgetItem, QDialog, QComboBox, QToolBar

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3


# QMainWindow allows to create multiple interconnected windows
# While QWidget only allows us to create a single one
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Student Management System")
		
		file_menu_item = self.menuBar().addMenu("&File")
		help_menu_item = self.menuBar().addMenu("&Help")
		edit_menu_item = self.menuBar().addMenu("&Edit")
		
		add_student_action = QAction(QIcon("icons/icons/add.png"), "Add Student", self)
		add_student_action.triggered.connect(self.insert)
		file_menu_item.addAction(add_student_action)
		
		about_action = QAction("About", self)
		help_menu_item.addAction(about_action)
		# Do this if and only if you do not see help menu
		# about_action.setMenuRole(QAction.MenuRole.NoRole)
		
		search_action = QAction(QIcon("icons/icons/search.png"), "Search", self)
		edit_menu_item.addAction(search_action)
		search_action.triggered.connect(self.search)
		
		# Create table to display student database
		self.table = QTableWidget()
		self.table.setColumnCount(4)
		self.table.setHorizontalHeaderLabels((
			"ID", "Name", "Course", "Mobile"
		))
		self.table.verticalHeader().setVisible(False)
		self.setCentralWidget(self.table)
		
		# Create a toolbar
		toolbar = QToolBar()
		self.addToolBar(toolbar)
		
		# Create toolbar elements
		toolbar.addAction(add_student_action)
		toolbar.addAction(search_action)
	
	def load_data(self):
		connection = sqlite3.connect("database.db")
		result = connection.execute("SELECT * FROM students")
		
		self.table.setRowCount(0)
		for row_number, row_data in enumerate(result):
			self.table.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				# print(row_data)
				self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
		
		connection.close()
	
	def insert(self):
		dialog = InsertDialog()
		dialog.exec()
		
	def search(self):
		dialog = SearchDialog()
		dialog.exec()


class InsertDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Insert Student Data")
		self.setFixedWidth(300)
		self.setFixedHeight(300)
		
		layout = QVBoxLayout()
		
		# Add student name widget
		self.student_name = QLineEdit()
		self.student_name.setPlaceholderText("Name")
		layout.addWidget(self.student_name)
		
		# Add combo box of courses
		self.course_name = QComboBox()
		courses = ["Biology", "Maths", "Astronomy", "Physics", "Chemistry"]
		self.course_name.addItems(courses)
		layout.addWidget(self.course_name)
		
		# Add mobile widget
		self.mobile = QLineEdit()
		self.mobile.setPlaceholderText("Mobile")
		layout.addWidget(self.mobile)
		
		# Add a submit button
		button = QPushButton("Register")
		button.clicked.connect(self.add_student)
		layout.addWidget(button)
		
		self.setLayout(layout)
	
	def add_student(self):
		# Get data
		name = self.student_name.text()
		course = self.course_name.itemText(self.course_name.currentIndex())
		mobile = self.mobile.text()
		
		# Insert the data in database
		connection = sqlite3.connect("database.db")
		cursor = connection.cursor()
		cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
		               (name, course, mobile))
		connection.commit()
		cursor.close()
		connection.close()
		
		# To show the current database
		main_window.load_data()
		

class SearchDialog(QDialog):
	def __init__(self):
		super().__init__()
		# Set window title and size
		self.setWindowTitle("Search Student")
		self.setFixedWidth(300)
		self.setFixedHeight(300)
		
		# Create layout and input widget
		layout = QVBoxLayout()
		
		self.student_name = QLineEdit()
		self.student_name.setPlaceholderText("Name")
		layout.addWidget(self.student_name)
		
		# Create button
		button = QPushButton("Search")
		button.clicked.connect(self.search)
		layout.addWidget(button)
		
		self.setLayout(layout)
		
	def search(self):
		name = self.student_name.text()
		
		connection = sqlite3.connect("database.db")
		cursor = connection.cursor()
		
		result = cursor.execute("SELECT * FROM students WHERE name = ?", (name, ))
		
		rows = list(result)
		print(rows)
		
		items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
		for item in items:
			print(item)
			main_window.table.item(item.row(), 1).setSelected(True)
			
			cursor.close()
			connection.close()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	main_window.load_data()
	sys.exit(app.exec())
