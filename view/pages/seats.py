from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QComboBox, QPushButton, QHBoxLayout, QInputDialog, QMessageBox
)
from model.multiseat_manager import MultiSeatManager
from view.components.page_wrapper import PageWrapper
from view.components.seat_list_item import SeatListItem


class SeatsPage(PageWrapper):
    """Page displaying a list of seats using the PageWrapper layout."""

    def __init__(self, manager: MultiSeatManager, parent=None):
        self.manager = manager
        seat_list_widget = self.build_ui()
        super().__init__("Seat Management", seat_list_widget)

    def build_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # === Device Selector & Action Buttons ===
        top_controls = QHBoxLayout()

        self.device_selector = QComboBox()
        self.populate_device_selector()
        top_controls.addWidget(self.device_selector)

        create_btn = QPushButton("Create Seat")
        create_btn.clicked.connect(self.create_seat_from_selected_device)
        top_controls.addWidget(create_btn)

        reset_btn = QPushButton("Reset All Devices")
        reset_btn.setStyleSheet("background-color: red; color: white;")
        reset_btn.clicked.connect(self.reset_all_devices)
        top_controls.addWidget(reset_btn)

        layout.addLayout(top_controls)

        # === Seat List ===
        self.seat_list = QListWidget()
        layout.addWidget(self.seat_list)

        self.refresh_seats()

        return widget

    def populate_device_selector(self):
        self.device_selector.clear()
        all_devices = self.manager.get_all_devices()
        for device in all_devices:
            icon_path = f"assets/{device.type}.png"
            label = f"{device.name} ({device.path})"
            self.device_selector.addItem(QIcon(icon_path), label, userData=device.path)

    def refresh_seats(self):
        self.seat_list.clear()
        seats = self.manager.get_seats()
        for seat in seats:
            item = QListWidgetItem()
            widget = SeatListItem(seat, refresh_callback=self.refresh_seats)
            item.setSizeHint(widget.sizeHint())
            self.seat_list.addItem(item)
            self.seat_list.setItemWidget(item, widget)

    def create_seat_from_selected_device(self):
        selected_index = self.device_selector.currentIndex()
        if selected_index < 0:
            return

        device_path = self.device_selector.itemData(selected_index)
        seat_id, ok = QInputDialog.getText(self, "Enter Seat ID", "Seat ID:")

        if ok and seat_id:
            self.manager.add_seat(device_path, seat_id)
            self.refresh_seats()

    def reset_all_devices(self):
        confirm = QMessageBox.question(
            self,
            "Confirm Reset",
            "⚠️ This will detach all devices from all seats. Proceed?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.manager.flush_all_devices()
            self.refresh_seats()
