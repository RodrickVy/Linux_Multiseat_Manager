from PyQt5.QtWidgets import (
    QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QTabWidget, QLabel,
    QScrollArea, QSizePolicy, QLineEdit
)
from PyQt5.QtCore import Qt

from controllers.systemd_multiseater_manager_impl import SystemdMultiSeatManager
from model.multiseat_manager import MultiSeatManager
from view.components.device_preview_title import DevicePreviewTile
from view.navigation.navigation_page import NavigationPage
from view.navigation.navigation_pages import AppPages
from view.components.device_list_item_details import DeviceDetailsPage


class DevicesPage(NavigationPage):
    def __init__(self, manager: MultiSeatManager, parent=None):
        self.manager = manager
        self.tab_widget = QTabWidget()

        # === Device List Tab ===
        self.device_list = QListWidget()
        self.tab_widget.addTab(self.device_list, "Device List")

        # === Device Tree Tab ===
        self.device_tree_scroll_area = QScrollArea()
        self.device_tree_scroll_area.setWidgetResizable(True)
        self.device_tree_container = QWidget()
        self.device_tree_layout = QVBoxLayout(self.device_tree_container)
        self.device_tree_scroll_area.setWidget(self.device_tree_container)
        self.tab_widget.addTab(self.device_tree_scroll_area, "Device Tree")

        # === Device Search Tab ===
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, path, or type...")
        self.search_input.textChanged.connect(self.update_search_results)
        self.devices = []
        self.search_results = QListWidget()
        search_tab = QWidget()
        search_layout = QVBoxLayout(search_tab)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_results)
        self.tab_widget.addTab(search_tab, "Search")

        # === Final Layout ===
        super().__init__(
            icon="🖥️",
            name=AppPages.DEVICES.value,
            title="Device Management",
            content_widget=self.tab_widget,
            parent=parent
        )

        self.refresh_devices_list()
        self.refresh_device_tree()

    def refresh_devices_list(self):
        self.device_list.clear()
        self.devices = self.manager.get_all_devices()
        for device in self.devices:
            item = QListWidgetItem()
            tile = DevicePreviewTile(device, self.on_device_selected)
            item.setSizeHint(tile.sizeHint())
            self.device_list.addItem(item)
            self.device_list.setItemWidget(item, tile)

    def refresh_device_tree(self):
        while self.device_tree_layout.count():
            child = self.device_tree_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.device_tree_layout.setSpacing(2)
        self.device_tree_layout.setContentsMargins(5, 5, 5, 5)

        all_devices = self.devices
        root_devices = [d for d in all_devices if not d.parent_path]

        for device in root_devices:
            self._add_device_recursive(device, 0)

    def _add_device_recursive(self, device, depth):
        indent = " -> " * depth
        is_parent = bool(device.children)
        bullet = "🔵 " if is_parent else ""

        label = QLabel()
        label.setTextFormat(Qt.RichText)
        label.setOpenExternalLinks(False)
        label.setText(
            f"""{indent}{bullet}<span style='font-size:10pt'>{device.name}</span> 
            <a href="{device.path}" style="font-size:9pt;">({device.path})</a>"""
        )
        label.linkActivated.connect(self.on_device_path_clicked)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        label.setContentsMargins(0, 0, 0, 0)
        self.device_tree_layout.addWidget(label)

        if is_parent:
            children = self.manager.get_children_devices(device.children)
            for child in children:
                self._add_device_recursive(child, depth + 1)

    def go_to_device_sub_page(self, device):
        detailsWidget = DeviceDetailsPage(device, device.name, self.app_navigator)
        self.app_navigator.go_to_subpage(AppPages.DEVICES.value, device.name, detailsWidget)

    def on_device_selected(self, device):
        self.go_to_device_sub_page(device)

    def on_device_path_clicked(self, path: str):
        device = next((d for d in self.devices if d.path == path), None)
        if device:
            self.go_to_device_sub_page(device)

    def update_search_results(self, query: str):
        self.search_results.clear()
        query = query.strip().lower()
        if not query:
            return

        matches = [
                      d for d in self.devices
                      if query in d.name.lower() or query in d.path.lower() or query in d.type.lower()
                  ][:10]  # Limit to first 10 matches

        for device in matches:
            item = QListWidgetItem()
            tile = DevicePreviewTile(device, self.on_device_selected)
            item.setSizeHint(tile.sizeHint())
            self.search_results.addItem(item)
            self.search_results.setItemWidget(item, tile)

    def refresh_ui(self):
        self.refresh_devices_list()
        self.refresh_device_tree()