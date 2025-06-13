from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QFormLayout, QGroupBox, QListWidget, QListWidgetItem, QHBoxLayout
)
from controllers.systemd_multiseater_manager_impl import SystemdMultiSeatManager
from model.data.device import Device
from view.pages.device import DevicesPage


class DeviceDetailsPage(QWidget):

    device = Device("Test", "Test", "Test", "Test", [])

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = SystemdMultiSeatManager()
        self._back_callback = None  # Placeholder for back handler

        layout = QVBoxLayout(self)

        # Back Button (top of page)
        back_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(self.go_back)
        back_layout.addWidget(back_btn)
        back_layout.addStretch()
        layout.addLayout(back_layout)

        list_widget = QListWidget()

        nameItem = QListWidgetItem()
        nameItemWidget = QLabel(f"<b>Name:</b> {DeviceDetailsPage.device.name}")
        list_widget.addItem(nameItem)
        list_widget.setItemWidget(nameItem, nameItemWidget)

        typeItem = QListWidgetItem()
        typeItemWidget = QLabel(f"<b>Type:</b> {DeviceDetailsPage.device.type}")
        list_widget.addItem(typeItem)
        list_widget.setItemWidget(typeItem, typeItemWidget)

        pathItem = QListWidgetItem()
        pathItemWidget = QLabel(f"<b>Path:</b> {DeviceDetailsPage.device.path}")
        list_widget.addItem(pathItem)
        list_widget.setItemWidget(pathItem, pathItemWidget)

        parent_device = self.manager.get_parent_device(DeviceDetailsPage.device.path)
        parentItem = QListWidgetItem()
        parentItemWidget = QLabel(f"<b>Parent:</b> {parent_device.name if parent_device else 'None'}")
        list_widget.addItem(parentItem)
        list_widget.setItemWidget(parentItem, parentItemWidget)

        if DeviceDetailsPage.device.children:
            children_devices = self.manager.get_children_devices(DeviceDetailsPage.device.children)
            for child in children_devices:
                seat = self.manager.get_device_seat(child.path)
                child_btn = QPushButton(f"{child.name} (Seat: {seat or 'Unassigned'})")
                child_btn.clicked.connect(lambda _, d=child: DevicesPage.on_device_selected(d))
                item = QListWidgetItem()
                list_widget.addItem(item)
                list_widget.setItemWidget(item, child_btn)

        all_seats = self.manager.get_seats()
        seat_selector = QComboBox()
        seat_selector.addItem("Select seat to attach...")
        for seat in all_seats:
            seat_selector.addItem(seat.seat_id)

        attach_btn = QPushButton("Attach Device to Seat")
        attach_btn.clicked.connect(lambda: self.attach_device_to_seat(seat_selector))

        selectorItem = QListWidgetItem()
        selectorItemWidget = seat_selector
        list_widget.addItem(selectorItem)
        list_widget.setItemWidget(selectorItem, selectorItemWidget)

        btnItem = QListWidgetItem()
        btnItemItemWidget = attach_btn
        list_widget.addItem(btnItem)
        list_widget.setItemWidget(btnItem, btnItemItemWidget)

        layout.addWidget(list_widget)
        self.setLayout(layout)

    def attach_device_to_seat(self, seat_selector: QComboBox):
        seat_id = seat_selector.currentText()
        if seat_id != "Select seat to attach...":
            seat = next((s for s in self.manager.get_seats() if s.seat_id == seat_id), None)
            if seat:
                self.manager.add_device_to_seat(seat, self.device)

    def set_back_callback(self, callback):
        """Set a callback function that should be called when back is pressed."""
        self._back_callback = callback

    def go_back(self):
        if self._back_callback:
            self._back_callback()
