from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, \
	QWidget, QGridLayout, QLineEdit, QPushButton

import sys
from datetime import datetime

class AgeCalculator(QWidget):
	def __init__(self):
		super().__init__() #super accesses the parent class, here QWidget
		self.setWindowTitle("Age Calculator")
		
		grid = QGridLayout()
		
		# Create widgets
		name_label = QLabel("Name:")
		self.name_line_edit = QLineEdit()
		
		dob_label = QLabel("Date of Birth (mm/dd/yyyy):")
		self.dob_line_edit = QLineEdit()
		# initiate as instance as we need to access it across the class
		
		calculate_button = QPushButton("Calculate Age")
		calculate_button.clicked.connect(self.calculate_age)
		
		self.output_label = QLabel("")
		
		# Add widgets to grid
		grid.addWidget(name_label, 0, 0) # (name, row, column)
		grid.addWidget(self.name_line_edit, 0, 1)
		
		grid.addWidget(dob_label, 1, 0)
		grid.addWidget(self.dob_line_edit, 1, 1)
		
		grid.addWidget(calculate_button, 2, 0, 1, 2) # (name, row, column, row_span, column_span)
		grid.addWidget(self.output_label, 3, 0, 1, 2)
		
		self.setLayout(grid)
		
	def calculate_age(self):
		curr_year = datetime.now().year
		dob_year = self.dob_line_edit.text()
		
		birth_year = datetime.strptime(dob_year, "%m/%d/%Y").date().year
		
		age = curr_year - birth_year
		self.output_label.setText(f"{self.name_line_edit.text()} is {age} years old.")
		
		
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	age_calculator = AgeCalculator()
	age_calculator.show()
	sys.exit(app.exec())