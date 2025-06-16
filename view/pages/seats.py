from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QComboBox, QPushButton, QHBoxLayout,  QMessageBox, QScrollArea
)
from model.multiseat_manager import MultiSeatManager
from view.components.seat_details import SeatDetailsPage
from view.components.seat_list_item import SeatListItem
from view.navigation.navigation_page import NavigationPage
from view.navigation.navigation_pages import AppPages


class SeatsPage(NavigationPage):
    """Scrollable page displaying a list of seats, using the NavigationPage layout."""

    def __init__(self, manager: MultiSeatManager, parent=None):
        self.seat_list = None
        self.device_selector = None
        self.manager = manager

        # Build the main scrollable widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.devices = []
        self.content_widget = self.build_ui()
        scroll_area.setWidget(self.content_widget)

        super().__init__(
            icon="💺",
            name=AppPages.SEATS.value,
            title="Seat Management",
            content_widget=scroll_area,
            parent=parent
        )

    def build_ui(self) -> QWidget:
        self.devices = self.manager.get_all_devices()
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

        refresh_btn = QPushButton("Refresh Seats")
        refresh_btn.setStyleSheet("background-color: #007BFF; color: white;")
        refresh_btn.clicked.connect(self.refresh_seats)
        top_controls.addWidget(refresh_btn)

        flush_btn = QPushButton("Flush All Devices")
        flush_btn.setToolTip("Flush devices back to seat0 and remove other seats")
        flush_btn.setStyleSheet("background-color: red; color: white;")
        flush_btn.clicked.connect(self.reset_all_devices)
        top_controls.addWidget(flush_btn)

        layout.addLayout(top_controls)

        # === Seat List ===
        self.seat_list = QListWidget()
        layout.addWidget(self.seat_list)

        self.refresh_seats()

        return widget

    def populate_device_selector(self):
        self.device_selector.clear()
        all_devices = self.devices

        for device in all_devices:
            icon_path = f"assets/{device.type}.png"
            label = f"{device.name} ({device.path})"
            self.device_selector.addItem(QIcon(icon_path), label, userData=device.path)

    def refresh_seats(self):
        self.seat_list.clear()

        seats = self.manager.get_seats()
        self.devices = self.manager.get_all_devices()

        for seat in seats:
            item = QListWidgetItem()

            # Pass go_to_seat_details as a callback to be triggered when clicked
            widget = SeatListItem(
                seat,
                refresh_callback=self.refresh_seats,
                click_callback=lambda _, s=seat: self.go_to_seat_details(s)
            )

            item.setSizeHint(widget.sizeHint())
            self.seat_list.addItem(item)
            self.seat_list.setItemWidget(item, widget)

    def create_seat_from_selected_device(self):
        selected_index = self.device_selector.currentIndex()
        if selected_index < 0:
            return

        device_path = self.device_selector.itemData(selected_index)
        self.manager.add_seat(device_path)
        self.app_navigator.refresh_ui()
        return


    def reset_all_devices(self):
        confirm = QMessageBox.question(
            self,
            "Confirm Flush",
            "⚠️ This will detach all devices from all seats and reset them to seat0. "
            "All custom seats will be removed.\n\nProceed?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.manager.flush_all_devices()
            self.refresh_seats()

    def go_to_seat_details(self, seat):
        details_page = SeatDetailsPage(seat, self.app_navigator)
        self.app_navigator.go_to_subpage(AppPages.SEATS.value, f"Seat {seat.seat_id}", details_page)

    def refresh_ui(self):
        self.refresh_seats()