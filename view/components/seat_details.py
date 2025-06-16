from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QScrollArea
)
from PyQt5.QtCore import Qt
from view.navigation.navigation_page import NavigationPage
from view.navigation.navigation_pages import AppPages
from model.data.seat import Seat
from model.data.device import Device
from model.data.session import Session


class SeatDetailsPage(NavigationPage):
    def __init__(self, seat: Seat, app_navigation, parent=None):
        self.seat = seat
        self.app_navigation = app_navigation
        self.devices = seat.devices
        self.sessions = seat.sessions

        self.list_widget = QListWidget()
        self.populate_ui()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.list_widget)

        super().__init__(
            icon="💺",
            name=AppPages.SEATS.value,
            title=f"Seat Details - {seat.seat_id}",
            content_widget=scroll_area,
            parent=parent
        )

    def populate_ui(self):
        def add_label_item(text: str):
            item = QListWidgetItem()
            label = QLabel(text)
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            label.setWordWrap(True)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, label)

        add_label_item(f"<b>Seat ID:</b> {self.seat.seat_id}")

        # Devices
        if self.devices:
            add_label_item("<b>Devices:</b>")
            for device in self.devices:
                link = QPushButton(f"{device.name} ({device.path})")
                link.setStyleSheet("text-align: left; padding: 2px 4px;")
                link.clicked.connect(lambda _, d=device: self.go_to_device_sub_page(d))
                item = QListWidgetItem()
                self.list_widget.addItem(item)
                self.list_widget.setItemWidget(item, link)
        else:
            add_label_item("No devices attached to this seat.")

        # Sessions
        if self.sessions:
            add_label_item("<b>Sessions:</b>")
            for session in self.sessions:
                label = f"{session.user} (TTY: {session.tty}, State: {session.state}, ID: {session.session_id})"
                link = QPushButton(label)
                link.setStyleSheet("text-align: left; padding: 2px 4px;")
                link.clicked.connect(lambda _, s=session: self.go_to_session_sub_page(s))
                item = QListWidgetItem()
                self.list_widget.addItem(item)
                self.list_widget.setItemWidget(item, link)
        else:
            add_label_item("No active sessions on this seat.")

    def go_to_device_sub_page(self, device: Device):
        from view.components.device_list_item_details import DeviceDetailsPage
        details = DeviceDetailsPage(device, AppPages.SEATS.value, self.app_navigation)
        self.app_navigation.go_to_subpage(AppPages.SEATS.value, device.name, details)

    def go_to_session_sub_page(self, session: Session):
        from view.components.session_detail_page import SessionDetailsPage
        details = SessionDetailsPage(session, AppPages.SEATS.value, self.app_navigation)
        self.app_navigation.go_to_subpage(AppPages.SEATS.value, f"Session {session.session_id}", details)
