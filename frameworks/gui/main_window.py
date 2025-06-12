from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QHBoxLayout, QStackedWidget, QLabel
from frameworks.gui.components.side_nav import SideNavWidget
from frameworks.gui.pages.seats import SeatsPage


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multiseat Manager")
        self.setGeometry(100, 100, 780, 700)

        main_layout = QHBoxLayout(self)

        # Main stack of pages
        self.stack = QStackedWidget()
        self.stack.addWidget(SeatsPage())
        self.stack.addWidget(self.page("Device Management"))
        self.stack.addWidget(self.page("Session Viewer"))
        self.stack.addWidget(self.page("About this App"))

        # Side navigation
        self.sidebar = SideNavWidget(self.stack)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

    def page(self, title):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel(f"<h2>{title}</h2>"))
        return page