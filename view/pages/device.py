from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from model.multiseat_manager import MultiSeatManager
from view.components.device_preview_title import DevicePreviewTile
from view.components.page_wrapper import PageWrapper


class DevicesPage(PageWrapper):
    on_device_selected = None
    def __init__(self, manager:MultiSeatManager,   parent=None):
        self.manager = manager
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
        devices = self.manager.get_all_devices()
        for device in devices:
            item = QListWidgetItem()

            tile = DevicePreviewTile(device, DevicesPage.on_device_selected)
            item.setSizeHint(tile.sizeHint())
            self.device_list.addItem(item)
            self.device_list.setItemWidget(item, tile)
