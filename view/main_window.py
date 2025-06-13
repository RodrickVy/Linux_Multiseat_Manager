from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel

from model.data.device import Device
from model.multiseat_manager import MultiSeatManager
from view.components.device_list_item_details import DeviceDetailsPage
from view.components.side_nav import SideNavWidget
from view.pages.about import AboutPage
from view.pages.device import DevicesPage
from view.pages.seats import SeatsPage
from view.pages.session import SessionsPage

class MultiseatManagerApp(QWidget):
    """
     Entry point for the application, Takes in an instance of MultiseatManager service.
    """

    # Signal to listen for navigation state changes (e.g., "devices", "seats", "sessions")
    navigationChanged = pyqtSignal(str)


    def __init__(self, multiseat_manager: MultiSeatManager):
        super().__init__()
        self.setWindowTitle("Multiseat Manager")
        self.setGeometry(100, 100, 1280, 1100)
        self.manager = multiseat_manager

        main_layout = QHBoxLayout(self)
        # Connect the signal to the handler
        self.navigationChanged.connect(self.on_navigation_changed)


        def show_device_details(device: Device):

            DeviceDetailsPage.device = device
            print(DeviceDetailsPage.device.name + 'Clicked')
            device_details_page = DeviceDetailsPage()
            device_details_page.set_back_callback(lambda: self.navigationChanged.emit("devices"))

            self.stack.addWidget(device_details_page)
            self.stack.setCurrentWidget(device_details_page)

        DevicesPage.on_device_selected = show_device_details

        # Main stack of pages
        self.stack = QStackedWidget()



        self.clear_stack_and_restack()



        # Side navigation
        self.sidebar = SideNavWidget(self.stack)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)


    def clear_stack_and_restack (self):
        while self.stack.count() > 0:
            widget = self.stack.widget(0)
            self.stack.removeWidget(widget)
            widget.deleteLater()
        self.stack.addWidget(SeatsPage(self.manager))
        self.stack.addWidget(DevicesPage(self.manager))
        self.stack.addWidget(SessionsPage(self.manager))
        self.stack.addWidget(AboutPage(self.manager))


    def on_navigation_changed(self, target: str):
        """Switch the stack index based on the string emitted."""
        if target == "devices":
            self.stack.setCurrentIndex(1)
        elif target == "seats":
            self.stack.setCurrentIndex(0)
        elif target == "sessions":
            self.stack.setCurrentIndex(2)
        else:
            print(f"[WARN] Unknown navigation target: {target}")

