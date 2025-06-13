from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from controllers.systemd_multiseater_manager_impl import SystemdMultiSeatManager
from model.data.device import Device


class DevicePreviewTile(QWidget):
    def __init__(self, device: Device, on_click_callback, parent=None):
        super().__init__(parent)
        self.device = device
        self.on_click_callback = on_click_callback
        self.manager = SystemdMultiSeatManager()

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        pixmap = QPixmap(f"assets/{device.type}.png")
        icon = QLabel()
        icon.setPixmap(pixmap.scaledToWidth(32))
        layout.addWidget(icon)

        layout.addWidget(QLabel(f"{device.name}"))

        seat_id = self.manager.get_device_seat(device.path)
        layout.addWidget(QLabel(f"Seat: {seat_id or 'Unassigned'}"))

        if device.children:
            layout.addWidget(QLabel(f"Children: {len(device.children)}"))

        layout.addStretch()
        self.setLayout(layout)

        self.mousePressEvent = lambda event: self.on_click_callback(self.device)
