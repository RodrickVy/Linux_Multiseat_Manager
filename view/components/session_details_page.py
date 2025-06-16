from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QScrollArea
from model.data.session import Session
from view.navigation.navigation_page import NavigationPage

class SessionDetailPage(NavigationPage):
    def __init__(self, session: Session, parent_page: str, app_navigation, parent=None):
        self.session = session

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        layout = QVBoxLayout(container)

        layout.addWidget(QLabel(f"<b>User:</b> {session.user}"))
        layout.addWidget(QLabel(f"<b>Session ID:</b> {session.session_id}"))
        layout.addWidget(QLabel(f"<b>Seat:</b> {session.seat}"))
        layout.addWidget(QLabel(f"<b>TTY:</b> {session.tty}"))
        layout.addWidget(QLabel(f"<b>Class:</b> {session.class_type}"))
        layout.addWidget(QLabel(f"<b>State:</b> {session.state}"))
        layout.addWidget(QLabel(f"<b>Remote:</b> {'Yes' if session.remote else 'No'}"))
        layout.addWidget(QLabel(f"<b>Active:</b> {'Yes' if session.active else 'No'}"))

        scroll_area.setWidget(container)

        super().__init__(
            icon="📋",
            name=f"session-{session.session_id}",
            title=f"Session: {session.user}",
            content_widget=scroll_area,
            parent=parent,
            parent_page=parent_page
        )
