# view/components/session_list_item.py

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from model.data.session import Session


class SessionListItem(QWidget):
    def __init__(self, session: Session, on_click=None, parent=None):
        super().__init__(parent)
        self.session = session
        self.on_click = on_click

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"<b>Session ID:</b> {session.session_id}"))
        layout.addWidget(QLabel(f"<b>User:</b> {session.user}"))
        layout.addWidget(QLabel(f"<b>Seat:</b> {session.seat or 'None'}"))
        layout.addWidget(QLabel(f"<b>TTY:</b> {session.tty or 'None'}"))
        layout.addWidget(QLabel(f"<b>Class:</b> {session.class_type}"))
        layout.addWidget(QLabel(f"<b>State:</b> {session.state}"))
        layout.addWidget(QLabel(f"<b>Remote:</b> {'Yes' if session.remote else 'No'}"))
        layout.addWidget(QLabel(f"<b>Active:</b> {'Yes' if session.active else 'No'}"))
        self.setLayout(layout)



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.on_click:
            self.on_click(self.session)
