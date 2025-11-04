from PyQt6.QtWidgets import QApplication, QLabel, QWidget
import sys

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Hello World App")
    window.setGeometry(100, 100, 300, 200)

    label = QLabel("Hello World!", parent=window)
    label.move(120, 80)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
