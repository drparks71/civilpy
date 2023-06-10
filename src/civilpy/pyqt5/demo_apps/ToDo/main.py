from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(100, 100, 200, 300)
    window.setWindowTitle("Hello App")

    label = QLabel(window)
    label.setText("Hello World!")
    label.setFont(QFont("Arial", 16))
    label.move(50, 100)

    window.show()
    app.exec_()


if __name__ == "__main__":
    main()

