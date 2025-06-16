from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QListWidget,
    QListWidgetItem
)
from controllers.systemd_multiseater_manager_impl import SystemdMultiSeatManager
from model.data.device import Device
from view.navigation.navigation import NavigationApp
from view.components.device_info import DeviceInfoWidget
from view.navigation.navigation_pages import AppPages


class DeviceDetailsPage(QWidget):
    def __init__(self, device: Device, parent_page: str = None,
                 app_navigation: NavigationApp = None, parent=None):
        super().__init__(parent)
        self.manager = SystemdMultiSeatManager()
        self.device = device
        self.parent_page = parent_page
        self.app_navigation = app_navigation

        self.layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.seat_selector = QComboBox()
        self.seat_selector.setMinimumHeight(35)
        self.build_ui()
        self.setLayout(self.layout)

    def build_ui(self):
        def add_label_item(text: str):
            item = QListWidgetItem()
            widget = QLabel(text)
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)

        self.list_widget.clear()
        add_label_item(f"<b>Name:</b> {self.device.name}")
        add_label_item(f"<b>Type:</b> {self.device.type}")
        add_label_item(f"<b>Path:</b> {self.device.path}")
        add_label_item(f"<b>Seat:</b> {self.manager.get_device_seat(self.device.path)}")
        parent_device = self.manager.get_parent_device(self.device.path)
        add_label_item(f"<b>Parent:</b> {parent_device.name if parent_device else 'None'}")
        add_label_item(f" ")
        # Children
        if self.device.children:
            children = self.manager.get_children_devices(self.device.children)
            for child in children:
                seat = self.manager.get_device_seat(child.path)
                btn = QPushButton(f"{child.name} (Seat: {seat or 'Unassigned'})")
                btn.clicked.connect(lambda _, d=child: self.go_to_device_sub_page(d))
                item = QListWidgetItem()
                self.list_widget.addItem(item)
                self.list_widget.setItemWidget(item, btn)

        # Seat selector
        self.populate_seat_selector()
        selector_item = QListWidgetItem()
        self.list_widget.addItem(selector_item)
        self.list_widget.setItemWidget(selector_item, self.seat_selector)

        # Add spacing before the button
        self.list_widget.addItem(QListWidgetItem())  # empty spacer

        # Create styled attach button
        attach_btn = QPushButton("Attach Device to Seat")
        attach_btn.setMinimumHeight(35)

        attach_btn.clicked.connect(lambda: self.attach_device_to_seat(self.seat_selector))

        # Add the button to the list
        btn_item = QListWidgetItem()

        self.list_widget.addItem(btn_item)
        btn_item.setSizeHint(QSize(0, 30))
        self.list_widget.setItemWidget(btn_item, attach_btn)

        # Add spacing after the button
        self.list_widget.addItem(QListWidgetItem())

        # More Device Info heading
        heading_item = QListWidgetItem()
        heading_label = QLabel("<b>More Device Info</b>")
        self.list_widget.addItem(heading_item)
        self.list_widget.setItemWidget(heading_item, heading_label)

        for info in self.device.device_information:
            info_widget = DeviceInfoWidget(info)
            item = QListWidgetItem()
            item.setSizeHint(info_widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, info_widget)

        self.layout.addWidget(self.list_widget)

    def populate_seat_selector(self):
        self.seat_selector.clear()
        self.seat_selector.addItem("Select seat to attach...")
        for seat in self.manager.get_seats():
            self.seat_selector.addItem(seat.seat_id)
        self.seat_selector.addItem("➕ New Seat")

    def attach_device_to_seat(self, seat_selector: QComboBox):
        seat_id = seat_selector.currentText()

        if seat_id == "➕ New Seat":
            self.manager.add_seat(self.device.path)
            self.app_navigation.refresh_ui()
            return

        if seat_id != "Select seat to attach...":
            seat = next((s for s in self.manager.get_seats() if s.seat_id == seat_id), None)
            if seat:
                self.manager.add_device_to_seat(seat, self.device)
                self.app_navigation.refresh_ui()

    def go_to_device_sub_page(self, device: Device):
        details = DeviceDetailsPage(device, self.device.name, self.app_navigation)
        self.app_navigation.go_to_subpage(self.parent_page, device.name, details)
