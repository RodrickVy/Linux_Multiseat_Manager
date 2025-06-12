# view/components/device_list_item.py

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from model.data.device import Device  # Adjust if your Device class is elsewhere

class DeviceListItem(QWidget):
    def __init__(self, device: Device, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Name: {device.name}"))
        layout.addWidget(QLabel(f"Type: {device.type}"))
        layout.addWidget(QLabel(f"Path: {device.path}"))

        self.setLayout(layout)
