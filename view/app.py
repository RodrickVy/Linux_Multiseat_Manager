from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel

from model.app_feedback import AppFeedback
from model.data.device import Device
from model.multiseat_manager import MultiSeatManager
from view.navigation.navigation import NavigationApp
from view.navigation.navigation_page import NavigationPage
from view.pages.about import AboutPage
from view.pages.devices import DevicesPage
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



        self.navApp = NavigationApp([
                     SeatsPage(self.manager),
                     DevicesPage(self.manager),
                     SessionsPage(self.manager),
                     NavigationPage("ℹ️", "about","About The Tool",AboutPage(),None)
                ])

        self.manager.feedback_listener = self.navApp.on_feedback


        main_layout.addWidget(self.navApp)
 





