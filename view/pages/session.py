from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem

from model.multiseat_manager import MultiSeatManager
from view.components.page_wrapper import PageWrapper
from view.components.session_list_item import SessionListItem  # You'll create this


class SessionsPage(PageWrapper):
    """Page displaying a list of user sessions."""

    def __init__(self, manager: MultiSeatManager,parent=None):
        self.manager: MultiSeatManager = manager
        session_list_widget = self.build_ui()
        super().__init__("Session Management", session_list_widget)

    def build_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.session_list = QListWidget()
        layout.addWidget(self.session_list)

        self.refresh_sessions()

        return widget

    def refresh_sessions(self):
        self.session_list.clear()
        sessions = self.manager.get_all_sessions()
        for session in sessions:
            item = QListWidgetItem()
            widget = SessionListItem(session)  # You need to create this widget
            item.setSizeHint(widget.sizeHint())
            self.session_list.addItem(item)
            self.session_list.setItemWidget(item, widget)