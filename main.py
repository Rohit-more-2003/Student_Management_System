from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QPushButton, \
	QMainWindow, QTableWidget, \
	QTableWidgetItem, QDialog, QComboBox, QToolBar, QStatusBar, QMessageBox

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3

class DatabaseConnection:
	def __init__(self, database_file="database.db"):
		self.database_file = database_file
		
	def connect(self):
		connection = sqlite3.connect(self.database_file)
		return connection


# QMainWindow allows to create multiple interconnected windows
# While QWidget only allows us to create a single one
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Student Management System")
		self.setMinimumSize(500, 500)
		
		file_menu_item = self.menuBar().addMenu("&File")
		help_menu_item = self.menuBar().addMenu("&Help")
		edit_menu_item = self.menuBar().addMenu("&Edit")
		
		add_student_action = QAction(QIcon("icons/icons/add.png"), "Add Student", self)
		add_student_action.triggered.connect(self.insert)
		file_menu_item.addAction(add_student_action)
		
		about_action = QAction("About", self)
		help_menu_item.addAction(about_action)
		about_action.triggered.connect(self.about)
		
		# Do this if and only if you do not see help menu (for macOS users)
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
		
		# Create a toolbar and toolbar elements
		toolbar = QToolBar()
		self.addToolBar(toolbar)
		
		toolbar.addAction(add_student_action)
		toolbar.addAction(search_action)
		
		# Create status bar and status bar elements
		self.status_bar = QStatusBar()
		self.setStatusBar(self.status_bar)
		
		# Detect if a cell of the table was chosen
		self.table.cellClicked.connect(self.cell_clicked)
	
	def cell_clicked(self):
		# Create status bar widgets
		edit_button = QPushButton("Edit Record")
		edit_button.clicked.connect(self.edit)
		
		delete_button = QPushButton("Delete Record")
		delete_button.clicked.connect(self.delete)
		
		# If there are already status bar buttons present, we want to delete the previous ones
		# so that buttons do not appear more than one time.
		children = self.findChildren(QPushButton)
		if children:
			for child in children:
				self.status_bar.removeWidget(child)
		
		# Add buttons to status bar
		self.status_bar.addWidget(edit_button)
		self.status_bar.addWidget(delete_button)
	
	def load_data(self):
		connection = DatabaseConnection().connect()
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
		
	def edit(self):
		dialog = EditDialog()
		dialog.exec()
		
	def delete(self):
		dialog = DeleteDialog()
		dialog.exec()
	
	
	def about(self):
			dialog = AboutDialog()
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
		connection = DatabaseConnection().connect()
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
		
		connection = DatabaseConnection().connect()
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
			
			
class EditDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Update Student Data")
		self.setFixedWidth(300)
		self.setFixedHeight(300)
		
		layout = QVBoxLayout()
		
		# Get the details of the student whose data is to be edited
		index = main_window.table.currentRow()
		name = main_window.table.item(index, 1).text()
		course = main_window.table.item(index, 2).text()
		mob = main_window.table.item(index, 3).text()
		
		# Get the id of the student
		self.student_id = main_window.table.item(index,0).text()
		
		# Add student name widget
		self.student_name = QLineEdit(name)
		self.student_name.setPlaceholderText("Name")
		layout.addWidget(self.student_name)
		
		# Add combo box of courses
		self.course_name = QComboBox()
		courses = ["Biology", "Maths", "Astronomy", "Physics", "Chemistry"]
		self.course_name.addItems(courses)
		self.course_name.setCurrentText(course)
		layout.addWidget(self.course_name)
		
		# Add mobile widget
		self.mobile = QLineEdit(mob)
		self.mobile.setPlaceholderText("Mobile")
		layout.addWidget(self.mobile)
		
		# Add a submit button
		button = QPushButton("Register")
		button.clicked.connect(self.update_student)
		layout.addWidget(button)
		
		self.setLayout(layout)
		
	def update_student(self):
		# Update the student data of selected student
		connection = DatabaseConnection().connect()
		cursor = connection.cursor()
		cursor.execute("UPDATE students SET name=?, course=?, mobile=? WHERE id=?",
		               (self.student_name.text(), self.course_name.currentText(),
		                self.mobile.text(), self.student_id))
		connection.commit()
		cursor.close()
		connection.close()
		
		# Display the updated data
		main_window.load_data()
		

class DeleteDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Delete Student Data")
		
		# Create the layout and add the widgets to the layout
		layout = QGridLayout()
		confirmation = QLabel("Are you sure you want to delete?")
		yes = QPushButton("Yes")
		no = QPushButton("No")
		
		layout.addWidget(confirmation, 0, 0, 1, 2)
		layout.addWidget(yes, 1, 0)
		layout.addWidget(no, 1, 1)
		self.setLayout(layout)
	
		yes.clicked.connect(self.delete)
		
	def delete(self):
		# Get index and student id from selected row
		index = main_window.table.currentRow()
		student_id = main_window.table.item(index, 0).text()
		
		# Delete the student data from the database
		connection = DatabaseConnection().connect()
		cursor = connection.cursor()
		cursor.execute("DELETE from students WHERE id=?", (student_id, ))
		connection.commit()
		cursor.close()
		connection.close()
		
		# Refresh the database
		main_window.load_data()
		
		# Close the delete window
		self.close()
		
		# Delete confirmation window
		confirmation_widget = QMessageBox()
		confirmation_widget.setWindowTitle("Success")
		confirmation_widget.setText("The record was deleted successfully.")
		confirmation_widget.exec()
		
		
class AboutDialog(QMessageBox):
	def __init__(self):
		super().__init__()
		
		self.setWindowTitle("About")
		
		content = """
This app was created to manage student database.
Feel free to use this app.
		"""
		self.setText(content)
		


if __name__ == "__main__":
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	main_window.load_data()
	sys.exit(app.exec())
