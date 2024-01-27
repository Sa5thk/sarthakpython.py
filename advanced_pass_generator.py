import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QSlider, QMessageBox
import string
import random
import pyperclip


class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Widgets
        self.length_label = QLabel("Password Length:")
        self.length_slider = QSlider()
        self.length_slider.setOrientation(1)  # Vertical orientation
        self.length_slider.setRange(6, 20)
        self.length_slider.setValue(12)

        self.length_display = QLabel(str(self.length_slider.value()))

        self.include_numbers_check = QCheckBox("Include Numbers")
        self.include_special_check = QCheckBox("Include Special Characters")

        self.generate_button = QPushButton("Generate Password")
        self.copy_button = QPushButton("Copy to Clipboard")

        # Layout
        v_layout = QVBoxLayout()

        v_layout.addWidget(self.length_label)
        v_layout.addWidget(self.length_slider)
        v_layout.addWidget(self.length_display)
        v_layout.addWidget(self.include_numbers_check)
        v_layout.addWidget(self.include_special_check)
        v_layout.addWidget(self.generate_button)
        v_layout.addWidget(self.copy_button)

        h_layout = QHBoxLayout()
        h_layout.addLayout(v_layout)

        # Event Handling
        self.length_slider.valueChanged.connect(self.update_length_display)
        self.generate_button.clicked.connect(self.generate_password)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        # Set up the main layout
        self.setLayout(h_layout)

        self.setWindowTitle("Password Generator")
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def update_length_display(self):
        self.length_display.setText(str(self.length_slider.value()))

    def generate_password(self):
        length = self.length_slider.value()
        include_numbers = self.include_numbers_check.isChecked()
        include_special = self.include_special_check.isChecked()

        characters = string.ascii_letters
        if include_numbers:
            characters += string.digits
        if include_special:
            characters += string.punctuation

        password = ''.join(random.choice(characters) for _ in range(length))
        self.show_message("Password Generated", f"Your password is:\n{password}")

    def copy_to_clipboard(self):
        password = pyperclip.paste()
        pyperclip.copy(password)
        self.show_message("Clipboard", "Password copied to clipboard.")

    def show_message(self, title, text):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PasswordGeneratorApp()
    sys.exit(app.exec_())
