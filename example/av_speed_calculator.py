from PyQt6.QtWidgets import QApplication, QLabel, QWidget,\
	QGridLayout, QLineEdit, QPushButton, QComboBox

import sys

class AverageSpeed(QWidget):
	def __init__(self):
		# must call for parent class constructor
		super().__init__()
		
		# Set window title
		self.setWindowTitle("Average Speed Calculator")
		
		# Create a window
		grid = QGridLayout()
		
		# Create widgets
		dis_label = QLabel("Distance:")
		self.dis_line_edit = QLineEdit()
		
		self.dis_unit = QComboBox()
		self.dis_unit.addItems([
			"Metric (km)", "Imperial (miles)"
		])
		
		time_label = QLabel("Time (hours):")
		self.time_line_edit = QLineEdit()
		
		calculate_button = QPushButton("Calculate")
		calculate_button.clicked.connect(self.calculate)
		
		self.output_label = QLabel("")
		
		# Add widgets to grid
		grid.addWidget(dis_label, 0, 0)
		grid.addWidget(self.dis_line_edit, 0 ,1)
		grid.addWidget(self.dis_unit, 0, 2)
		
		grid.addWidget(time_label, 1, 0)
		grid.addWidget(self.time_line_edit, 1, 1)
		
		grid.addWidget(calculate_button, 2, 1)
		grid.addWidget(self.output_label, 3, 0, 1, 2)
		
		# Set the layout
		self.setLayout(grid)
		
	def calculate(self):
		# Get the distance and time
		dis = float(self.dis_line_edit.text())
		time = float(self.time_line_edit.text())
		
		# Calculate speed in unit/hr
		speed = float(dis)/float(time)
		
		# Set the unit
		unit = self.dis_unit.currentText()
		if unit == "Metric (km)":
			speed = round(speed, 2)
			unit = "km/h"
		else:
			speed = round(speed * 0.621371, 2)
			unit = "mph"
			
		# Display the result
		self.output_label.setText(f"Average Speed: {speed} {unit}l")
		
		
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	speed_calculator = AverageSpeed()
	speed_calculator.show()
	sys.exit(app.exec())