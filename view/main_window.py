from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel
from view.components.side_nav import SideNavWidget
from view.pages.about import AboutPage
from view.pages.device import DevicesPage
from view.pages.seats import SeatsPage
from view.pages.session import SessionsPage


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multiseat Manager")
        self.setGeometry(100, 100, 780, 700)

        main_layout = QHBoxLayout(self)

        # Main stack of pages
        self.stack = QStackedWidget()
        self.stack.addWidget(SeatsPage())
        self.stack.addWidget(DevicesPage())
        self.stack.addWidget(SessionsPage())
        self.stack.addWidget(AboutPage())

        # Side navigation
        self.sidebar = SideNavWidget(self.stack)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

    def page(self, title):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel(f"<h2>{title}</h2>"))
        return page