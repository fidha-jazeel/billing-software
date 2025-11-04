# import sys
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
# )
# from PyQt6.QtGui import QFont, QColor, QPalette, QPixmap
# from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
import sys


# 🔹 Hello World Window
class HelloWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello World")
        self.resize(400, 250)
        self.setStyleSheet("background-color: #1f1f1f; color: #00bcd4;")
        
        layout = QVBoxLayout()
        label = QLabel("Hello World")
        label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)


# 🔹 Login Window
# class LoginWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Aronium Login")
#         self.resize(400, 300)
#         self.setStyleSheet("background-color: #2b2b2b; color: white;")

#         layout = QVBoxLayout()

#         # Welcome Label
#         label = QLabel("Welcome to Aronium")
#         label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
#         label.setStyleSheet("color: #00bcd4; margin-bottom: 10px;")
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(label)

#         # Logo
#         logo = QLabel()
#         pixmap = QPixmap("aronium.png")
#         if not pixmap.isNull():
#             scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
#             logo.setPixmap(scaled_pixmap)
#         else:
#             logo.setText("Logo not found")
#         logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(logo)

#         # Login Button
#         login_button = QPushButton("Login")
#         login_button.setFont(QFont("Arial", 14))
#         login_button.setStyleSheet("""
#             QPushButton {
#                 background-color: #00bcd4;
#                 color: white;
#                 border-radius: 6px;
#                 padding: 10px 20px;
#                 margin-top: 20px;
#             }
#             QPushButton:hover {
#                 background-color: #0097a7;
#             }
#         """)
#         login_button.clicked.connect(self.open_hello_window)
#         layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
#         self.setLayout(layout)

#     def open_hello_window(self):
#         self.hello_window = HelloWindow()
#         self.hello_window.show()
#         self.close()


# # 🔹 Main App Entry
# app = QApplication(sys.argv)
# window = LoginWindow()
# window.show()
# sys.exit(app.exec())

# from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
# from PyQt6.QtGui import QFont, QPixmap
# from PyQt6.QtCore import Qt
# import sys

# # Hello World Window
# class HelloWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Hello World")
#         self.resize(400, 250)
#         self.setStyleSheet("background-color: #f1f1f1; color: #00bcd4;")

#         layout = QVBoxLayout()
#         label = QLabel("Hello World!")
#         label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(label)
#         self.setLayout(layout)


# # Login Window
# class LoginWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Aronium Login")
#         self.resize(400, 300)
#         self.setStyleSheet("background-color: #e0e0e0; color: black;")

#         layout = QVBoxLayout()

#         # Welcome Text
#         title = QLabel("Welcome to Aronium")
#         title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
#         title.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(title)

#         # ✅ Logo ചേർക്കുന്നു
#         logo = QLabel()
#         pixmap = QPixmap("aronium.png")  # make sure filename is correct
#         logo.setPixmap(pixmap.scaled(150, 100, Qt.AspectRatioMode.KeepAspectRatio))
#         logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(logo)

#         # Login Button
#         self.login_button = QPushButton("Login")
#         self.login_button.setFont(QFont("Arial", 14))
#         self.login_button.clicked.connect(self.open_hello)
#         layout.addWidget(self.login_button)

#         self.setLayout(layout)

#     def open_hello(self):
#         self.hello = HelloWindow()
#         self.hello.show()


# # Run the app
# app = QApplication(sys.argv)
# window = LoginWindow()
# window.show()
# sys.exit(app.exec())


# from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit
# from PyQt6.QtGui import QFont, QPixmap
# from PyQt6.QtCore import Qt
# import sys

# class HelloWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Hello World")
#         self.resize(400, 250)
#         layout = QVBoxLayout()

#         label = QLabel("Hello World!")
#         label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         layout.addWidget(label)
#         self.setLayout(layout)


# class LoginWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Aronium Login")
#         self.resize(400, 300)
#         layout = QVBoxLayout()
#         self.setLayout(layout)


        # Title
        # title = QLabel("Welcome to Aronium")
        # title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        # title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(title)

        # Logo
        # logo = QLabel()
        # pixmap = QPixmap("aronium.png")
        # logo.setPixmap(pixmap.scaled(150, 100, Qt.AspectRatioMode.KeepAspectRatio))
        # logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(logo)

        # # Password textbox
        # self.password_box = QLineEdit()
        # self.password_box.setPlaceholderText("Enter Password")
        # self.password_box.setEchoMode(QLineEdit.EchoMode.Password)  # hides text with ●●●
        # layout.addWidget(self.password_box)

        # # Login button
        # login_button = QPushButton("Login")
        # login_button.setFont(QFont("Arial", 14))
        # login_button.clicked.connect(self.check_password)
        # layout.addWidget(login_button)

        # # Feedback message
        # self.feedback = QLabel("")
        # self.feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(self.feedback)

        # self.setLayout(layout)

    # def check_password(self):
    #     password = self.password_box.text()
    #     if password == "secret":  # Change 'secret' to your own password
    #         self.open_hello()
    #     else:
    #         self.feedback.setText("Invalid password! Try again.")
    #         self.feedback.setStyleSheet("color: red;")

    # def open_hello(self):
    #     self.hello = HelloWindow()
    #     self.hello.show()
    #     self.close()


# if __name__ == "__main__":
#  app = QApplication(sys.argv)
#  window = LoginWindow()
#  window.show()
#  sys.exit(app.exec())

# class LoginWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Aronium Login")
#         self.resize(400, 300)
#         self.setStyleSheet("background-color: #e0e0e0; color: black;")

#         layout = QVBoxLayout()

#         # Title
#         title = QLabel("Welcome to Aronium")
#         title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
#         title.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(title)

#         # Logo
#         logo = QLabel()
#         pixmap = QPixmap("aronium.png")
#         logo.setPixmap(pixmap.scaled(150, 100, Qt.AspectRatioMode.KeepAspectRatio))
#         logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(logo)

#         # Password textbox
#         self.password_box = QLineEdit()
#         self.password_box.setPlaceholderText("Enter Password")
#         self.password_box.setEchoMode(QLineEdit.EchoMode.Password)
#         layout.addWidget(self.password_box)

#         # Login button
#         login_button = QPushButton("Login")
#         login_button.setFont(QFont("Arial", 14))
#         login_button.clicked.connect(self.check_password)
#         layout.addWidget(login_button)

#         # Feedback label
#         self.feedback = QLabel("")
#         self.feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.feedback)

#         self.setLayout(layout)

#     def check_password(self):
#         password = self.password_box.text()
#         if password == "secret":  # 🔒 change this password if you want
#             self.feedback.setText("✅ Login successful!")
#             self.open_hello()  # ✅ Hello window തുറക്കാൻ ഇത് ചേർക്കണം
#         else:
#             self.feedback.setText("❌ Incorrect password.")


#     # def check_password(self):
#     #     password = self.password_box.text()
#     #     if password == "secret":  # 🔒 change this password if you want
#     #         self.feedback.setText("✅ Login successful!")
#     #     else:
#     #         self.feedback.setText("❌ Incorrect password.")
#     def open_hello(self):
#         self.hello = HelloWindow()
#         self.hello.show()
#         self.close()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = LoginWindow()
#     window.show()
#     sys.exit(app.exec())