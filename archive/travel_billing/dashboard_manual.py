from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
import sys

class DashboardManual(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manual Billing Dashboard")
        self.setGeometry(200, 100, 900, 600)

        # Main layout
        layout = QVBoxLayout()

        title = QLabel("🧾 Travel Billing System (Manual UI)")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        new_bill_btn = QPushButton("New Bill")
        view_bills_btn = QPushButton("View Bills")

        layout.addWidget(title)
        layout.addWidget(new_bill_btn)
        layout.addWidget(view_bills_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


# Run the window directly (for testing)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardManual()
    window.show()
    sys.exit(app.exec_())
