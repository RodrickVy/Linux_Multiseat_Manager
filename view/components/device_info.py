from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from model.data.device_info import DeviceInfo


class DeviceInfoWidget(QWidget):
    def __init__(self, device_info: DeviceInfo, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        context_label = QLabel(f"<b>{device_info.context}</b>")
        content_text = QTextEdit()
        content_text.setPlainText(device_info.info)
        content_text.setReadOnly(True)
        content_text.setMinimumHeight(60)

        layout.addWidget(context_label)
        layout.addWidget(content_text)
