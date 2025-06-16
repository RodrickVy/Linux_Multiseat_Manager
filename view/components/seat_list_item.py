from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from controllers.systemd_multiseater_manager_impl import SystemdMultiSeatManager


class SeatListItem(QWidget):
    def __init__(self, seat, refresh_callback=None, click_callback=None):
        super().__init__()
        self.seat = seat
        self.refresh_callback = refresh_callback
        self.click_callback = click_callback

        self.manager = SystemdMultiSeatManager()
        self.refresh_callback = refresh_callback  # Optional callback to refresh the list

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"<b>Seat:</b> {seat.seat_id}"))
        layout.addWidget(QLabel(f"<b>Sessions:</b> {len(seat.sessions)}"))
        layout.addWidget(QLabel(f"<b>Devices:</b> {len(seat.devices)} connected"))



    def mousePressEvent(self, event):
        if callable(self.click_callback):
            self.click_callback(event, self.seat)