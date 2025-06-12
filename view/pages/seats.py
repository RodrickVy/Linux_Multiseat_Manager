from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem

from controllers.systemd_multiseater_manager_impl import SystemdMultiSeatManager
from view.components.page_wrapper import PageWrapper
from view.components.seat_list_item import SeatListItem  # This is a custom widget you create


class SeatsPage(PageWrapper):
    """Page displaying a list of seats using the PageWrapper layout."""

    def __init__(self, parent=None):
        self.controller = SystemdMultiSeatManager()
        seat_list_widget = self.build_ui()
        super().__init__("Seat Management", seat_list_widget)

    def build_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.seat_list = QListWidget()
        layout.addWidget(self.seat_list)

        self.refresh_seats()

        return widget

    def refresh_seats(self):
        self.seat_list.clear()
        seats = self.controller.get_seats()
        for seat in seats:
            item = QListWidgetItem()
            widget = SeatListItem(seat)  # Convert Seat data model to visual representation
            item.setSizeHint(widget.sizeHint())
            self.seat_list.addItem(item)
            self.seat_list.setItemWidget(item, widget)
