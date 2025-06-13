from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from controllers.systemd_multiseater_manager_impl import SystemdMultiSeatManager


class SeatListItem(QWidget):
    def __init__(self, seat, refresh_callback=None, parent=None):
        super().__init__(parent)
        self.seat = seat
        self.manager = SystemdMultiSeatManager()
        self.refresh_callback = refresh_callback  # Optional callback to refresh the list

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"<b>Seat:</b> {seat.seat_id}"))
        layout.addWidget(QLabel(f"<b>Sessions:</b> {len(seat.sessions)}"))
        layout.addWidget(QLabel(f"<b>Devices:</b> {len(seat.devices)} connected"))

        delete_btn = QPushButton("Delete Seat")
        delete_btn.setStyleSheet("background-color: orange; color: white;border-radius:20px")
        delete_btn.clicked.connect(self.confirm_delete)
        layout.addWidget(delete_btn)

    def confirm_delete(self):
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete seat '{self.seat.seat_id}'?\nThis will detach all devices.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.manager.remove_seat(self.seat.seat_id)
            if self.refresh_callback:
                self.refresh_callback()
