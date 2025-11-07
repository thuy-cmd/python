import sys
import random

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt

app = QApplication(sys.argv)

win = QWidget()
win.setWindowTitle("Chao mung den voi PyQt!")

wishes =[
    "Chuc ban mot ngay tot lanh!",
    "Chuc ban thanh cong va hanh phuc!",
    "Chuc ban suc khoe va may man!",
]

layout = QVBoxLayout(win)

label = QLabel("Hello, PyQt!")
label.setAlignment(Qt.AlignmentFlag.AlignCenter)

button = QPushButton("Click Me")
btn = QPushButton("Show Wish")


def on_button_click():
    random_index = random.randint(0, len(wishes) - 1)
    label.setText(wishes[random_index])

button.clicked.connect(on_button_click)
layout.addWidget(label)
layout.addWidget(button)

win.resize(400, 200)
win.show()
sys.exit(app.exec())
