# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
# import sys

# class DashboardFull(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Travel Agency - Billing Software")
#         self.resize(1200, 700)

#         # Central widget
#         central = QWidget()
#         self.setCentralWidget(central)

#         # Layout
#         layout = QVBoxLayout()
#         central.setLayout(layout)

#         # Example widgets
#         self.label = QLabel("Welcome to Travel Agency Billing!")
#         self.btn_newBill = QPushButton("New Invoice")
#         self.btn_save = QPushButton("Save Invoice")

#         layout.addWidget(self.label)
#         layout.addWidget(self.btn_newBill)
#         layout.addWidget(self.btn_save)

#         # Connections
#         self.btn_newBill.clicked.connect(self.new_invoice)
#         self.btn_save.clicked.connect(self.save_invoice)

#     def new_invoice(self):
#         print("🧾 New Invoice clicked")

#     def save_invoice(self):
#         print("💾 Save Invoice clicked")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = DashboardFull()
#     window.show()
#     sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from travel_billing import dashboard_full as dashboard_ui


# import dashboard_ui
# from travel_billing import dashboard_full as dashboard_ui
import dashboard_full as dashboard_ui

  # this is the converted file

class DashboardWindow(QMainWindow, dashboard_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Connect buttons (if any)
        # self.btn_newBill.clicked.connect(self.new_invoice)
        self.add_bill_button.clicked.connect(self.new_invoice)

        # self.btn_saveInvoice.clicked.connect(self.save_invoice)

    def new_invoice(self):
        print("🧾 New Invoice clicked")

    def save_invoice(self):
        print("💾 Save Invoice clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec_())
