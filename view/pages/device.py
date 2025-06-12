from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem

from controllers.systemd_multiseater_manager_impl import SystemdMultiSeatManager
from model.multiseat_manager import MultiSeatManager
from view.components.page_wrapper import PageWrapper
from view.components.device_list_item import DeviceListItem  # You'll create this


class DevicesPage(PageWrapper):
    """Page displaying a list of devices across all seats."""

    def __init__(self, parent=None):
        self.controller: MultiSeatManager = SystemdMultiSeatManager()
        device_list_widget = self.build_ui()
        super().__init__("Device Management", device_list_widget)

    def build_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.device_list = QListWidget()
        layout.addWidget(self.device_list)

        self.refresh_devices()

        return widget

    def refresh_devices(self):
        self.device_list.clear()
        devices = self.controller.get_all_devices()
        for device in devices:
            item = QListWidgetItem()
            widget = DeviceListItem(device)  # You need to create this widget
            item.setSizeHint(widget.sizeHint())
            self.device_list.addItem(item)
            self.device_list.setItemWidget(item, widget)