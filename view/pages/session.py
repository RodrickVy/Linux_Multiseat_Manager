from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QScrollArea
from model.multiseat_manager import MultiSeatManager
from view.components.session_list_item import SessionListItem
from view.components.session_details_page import SessionDetailPage
from view.navigation.navigation_page import NavigationPage
from view.navigation.navigation_pages import AppPages


class SessionsPage(NavigationPage):
    """Page displaying a list of user sessions, scrollable and navigable."""

    def __init__(self, manager: MultiSeatManager, parent=None):
        self.manager = manager

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.list_widget = self.build_ui()
        scroll_area.setWidget(self.list_widget)

        super().__init__(
            icon="👤",
            name=AppPages.SESSIONS.value,
            title="Session Management",
            content_widget=scroll_area,
            parent=parent
        )

    def build_ui(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)

        self.session_list = QListWidget()
        layout.addWidget(self.session_list)

        self.refresh_sessions()

        return container

    def refresh_sessions(self):
        self.session_list.clear()
        sessions = self.manager.get_all_sessions()
        for session in sessions:
            item = QListWidgetItem()
            widget = SessionListItem(session, self.on_session_clicked)
            item.setSizeHint(widget.sizeHint())
            self.session_list.addItem(item)
            self.session_list.setItemWidget(item, widget)

    def on_session_clicked(self, session):
        if self.app_navigator:
            details = SessionDetailPage(session, AppPages.SESSIONS.value, self.app_navigator)
            self.app_navigator.go_to_subpage(AppPages.SESSIONS.value, session.session_id, details)


    def refresh_ui(self):
        self.build_ui()