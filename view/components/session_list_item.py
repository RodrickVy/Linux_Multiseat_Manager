# view/components/session_list_item.py

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from model.data.session import Session  # Adjust if your Session class is elsewhere

class SessionListItem(QWidget):
    def __init__(self, session: Session, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Session ID: {session.session_id}"))
        layout.addWidget(QLabel(f"User: {session.user}"))
        layout.addWidget(QLabel(f"Seat: {session.seat}"))
        layout.addWidget(QLabel(f"TTY: {session.tty}"))
        layout.addWidget(QLabel(f"State: {session.state}"))
        layout.addWidget(QLabel(f"Remote: {'Yes' if session.remote else 'No'}"))
        layout.addWidget(QLabel(f"Active: {'Yes' if session.active else 'No'}"))

        self.setLayout(layout)
