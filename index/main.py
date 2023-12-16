import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bootstrap import Bootstrap

class MainWindow(QMainWindow):

    button = None
    timePressed = 0
    def __init__(self):
        super().__init__()
        bootstrap = Bootstrap()
        bootstrap.bootstrap()
        self.setWindowTitle("My App")

        self.button = QPushButton("Press Me!")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.the_button_was_clicked)

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        self.timePressed += 1
        self.button.setText(f'Pressed {self.timePressed} times')


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()