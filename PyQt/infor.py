import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFormLayout, QHBoxLayout, QVBoxLayout,
    QLabel, QLineEdit, QRadioButton, QCheckBox, QComboBox, QPushButton, QMessageBox, QButtonGroup
)
from PyQt6.QtCore import Qt

app = QApplication(sys.argv)
win = QMainWindow()
win.setWindowTitle("Information Form")
central_widget = QWidget()
layout = QVBoxLayout(central_widget)
win.setCentralWidget(central_widget)

label_name = QLabel("Name:")
input_name = QLineEdit()

label_gender = QLabel("Gender:")
radio_male = QRadioButton("Male")
radio_female = QRadioButton("Female")
radio_other = QRadioButton("Other")

label_hobbies = QLabel("Hobbies:")
checkbox_reading = QCheckBox("Reading")
checkbox_traveling = QCheckBox("Traveling")
checkbox_sports = QCheckBox("Sports")
checkbox_coding = QCheckBox("Coding")

label_class = QLabel("Class:")
combo_class = QComboBox()
combo_class.addItems(["Class A", "Class B", "Class C", "Class D"])
button_submit = QPushButton("Submit")
layout.addWidget(label_name)
layout.addWidget(input_name)
layout.addWidget(label_gender)
layout.addWidget(radio_male)
layout.addWidget(radio_female)
layout.addWidget(radio_other)
layout.addWidget(label_hobbies)
layout.addWidget(checkbox_reading)
layout.addWidget(checkbox_traveling)
layout.addWidget(checkbox_sports)
layout.addWidget(checkbox_coding)
layout.addWidget(label_class)
layout.addWidget(combo_class)
layout.addWidget(button_submit)

win.resize(300, 400)
win.show()
sys.exit(app.exec())
