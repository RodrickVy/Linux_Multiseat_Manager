from numbers import Number

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem, QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy


class NavigationItem(QListWidgetItem):
    def __init__(self, label: str, icon: str = "", indent: bool = False,
                 is_parent_page: bool = False ):
        """
        A QListWidgetItem that holds metadata, with optional clear button support via paired widget.
        """
        display_text = f"{'   ' if indent else ''}{icon}  {label}"
        super().__init__(display_text)

        self.label = label
        self.icon = icon
        self.indent = indent
        self.is_parent_page = is_parent_page



from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from typing import Callable, Optional
from numbers import Number

class NavigationItemWidget(QWidget):
    def __init__(self, page_name: str, icon: str = "", is_parent_page: bool = False,
                 is_subpage: bool = False, clear_subpages_callback: Optional[Callable] = None,
                 indent_level: Number = 1, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(1)

        # Apply indentation using indent_level
        indent = "  →" * max(0, int(indent_level))
        label_text = f"{indent} {icon}  {page_name}" if icon else f"{indent} {page_name}"

        label_widget = QLabel(label_text)
        label_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(label_widget)

        # Optional clear button
        if is_parent_page and clear_subpages_callback:
            clear_button = QPushButton("🧹")
            clear_button.setFixedSize(24, 24)
            clear_button.setStyleSheet("QPushButton { border: none; background: none; }")
            clear_button.setToolTip("Clear sub-pages")
            clear_button.clicked.connect(lambda: clear_subpages_callback(page_name))
            layout.addWidget(clear_button)

        self.setLayout(layout)
        self.setMinimumHeight(12)
