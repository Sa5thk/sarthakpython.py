import sys
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QTextCursor, QPixmap
from PyQt5.QtCore import Qt
from cryptography.fernet import Fernet  # Install cryptography library

class ChatApplication(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

        # Simulate user authentication
        self.username = self.authenticate_user()

        # Generate a key for symmetric encryption (Fernet)
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def init_ui(self):
        self.setWindowTitle('Chat Application')
        self.setGeometry(100, 100, 800, 600)

        self.message_history = QTextEdit()
        self.message_history.setReadOnly(True)

        self.message_input = QLineEdit()
        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_message)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.attach_button = QPushButton('Attach Image')
        self.attach_button.clicked.connect(self.attach_image)

      
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.message_history)
        main_layout.addWidget(self.message_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.image_label)

        attachment_layout = QHBoxLayout()
        attachment_layout.addWidget(self.attach_button)

        main_layout.addLayout(button_layout)
        main_layout.addLayout(attachment_layout)

        self.setLayout(main_layout)

    def authenticate_user(self):
        username, ok_pressed = QInputDialog.getText(self, "User Authentication", "Enter your username:")
        if ok_pressed and username:
            return username
        else:
            sys.exit(0)  # Exit if the user cancels authentication

    def send_message(self):
        message = self.message_input.text()
        if message:
            encrypted_message = self.encrypt_message(message)
            self.message_history.append(f'{self.username}: {encrypted_message}')
            self.message_input.clear()

    def attach_image(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, 'Attach Image', '', 'Images (*.png *.jpg *.jpeg *.gif)')
        if image_path:
            self.display_image(image_path)

    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)

    def encrypt_message(self, message):
        encrypted_message = self.cipher_suite.encrypt(message.encode('utf-8'))
        return encrypted_message.decode('utf-8')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_app = ChatApplication()
    chat_app.show()
    sys.exit(app.exec_())