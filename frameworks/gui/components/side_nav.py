from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QStackedWidget
from PyQt5.QtCore import QSize


def create_menu_item(icon: str, label: str):
    return QListWidgetItem(f"{icon}  {label}")


class SideNavWidget(QListWidget):
    def __init__(self, stack: QStackedWidget, parent=None):
        super().__init__(parent)
        self.stack = stack
        self.setFixedWidth(180)
        self.setIconSize(QSize(24, 24))

        self.addItem(create_menu_item("🪑", "Seats"))
        self.addItem(create_menu_item("🖱️", "Devices"))
        self.addItem(create_menu_item("🧑‍💻", "Sessions"))
        self.addItem(create_menu_item("ℹ️", "About"))

        self.currentRowChanged.connect(self.stack.setCurrentIndex)
