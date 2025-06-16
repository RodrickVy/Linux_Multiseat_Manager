from abc import abstractmethod
from typing import List

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from model.app_feedback import AppFeedback
from view.components.feedback_banner import FeedbackBanner  # Assume we have this





class NavigationPage(QWidget):
    def __init__(self, icon:str, name: str, title: str, content_widget: QWidget, is_subpage:bool=False, parent_page:str=None, parent=None):
        super().__init__(parent)
        self.icon = icon
        self.name = name
        self.title = title
        self.app_navigator = None
        self.content_widget = content_widget
        self.is_subpage = is_subpage
        self.parent_page = parent_page



        self.layout = QVBoxLayout(self)
        self.feedback_banner = None
        self.back_button = None

        # Title area with optional back button
        self.title_layout = QHBoxLayout()
        self.title_label = QLabel(f"<h2 style='width:100%; text-align:center'>{self.title}</h2>")
        self.title_label.setTextFormat(Qt.RichText)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_layout.addWidget(self.title_label)

        self.layout.addLayout(self.title_layout)
        self.layout.addWidget( self.content_widget )



    # Initializes the navigator
    def initialize_navigator(self,navigator):
        self.app_navigator = navigator
        if self.app_navigator.navigator_has_history():
            self.add_back_button()
        else:
            self.remove_back_button()

    def add_back_button(self):
        if not self.back_button:
            self.back_button = QPushButton("← Back")
            self.back_button.clicked.connect(self.app_navigator.go_back)
            self.title_layout.insertWidget(0, self.back_button)

    def remove_back_button(self):
        if self.back_button:
            self.title_layout.removeWidget(self.back_button)
            self.back_button.deleteLater()
            self.back_button = None

    def show_feedback(self, feedback: AppFeedback):
        # Remove old banner if it exists
        if self.feedback_banner:
            self.layout.removeWidget(self.feedback_banner)
            self.feedback_banner.deleteLater()
            self.feedback_banner = None

        # Add new banner at top
        self.feedback_banner = FeedbackBanner()
        self.feedback_banner.display_feedback(feedback)
        self.layout.insertWidget(0, self.feedback_banner)

    @abstractmethod
    def refresh_ui(self):
        """Refreshes this pages UI"""
        pass