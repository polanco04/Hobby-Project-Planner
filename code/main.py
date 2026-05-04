import sys
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import setThemeColor
from PyQt6.QtGui import QColor
from mainWindow import MainWindow
from utils import hasOpenedBefore, markAsOpened


if __name__ == "__main__":
    app = QApplication(sys.argv)

    setThemeColor(QColor("#2B5CE6"))

    isFirstTime = not hasOpenedBefore()
    markAsOpened()
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())