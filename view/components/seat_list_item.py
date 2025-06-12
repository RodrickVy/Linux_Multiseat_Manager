from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class SeatListItem(QWidget):
    def __init__(self, seat, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"<b>Seat:</b> {seat.seat_id}"))
        layout.addWidget(QLabel(f"<b>Sessions:</b> {len(seat.sessions)}"))
        layout.addWidget(QLabel(f"<b>Devices:</b> {len(seat.devices)} connected"))
