from PyQt5.QtWidgets import QApplication
from frameworks.gui.main_window import MainWindow
import sys

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
