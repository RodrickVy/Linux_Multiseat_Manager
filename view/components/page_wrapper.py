from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class PageWrapper(QWidget):
    def __init__(self, title: str, content_widget: QWidget, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        title_label = QLabel(f"<h2 style='width:100%;text-align:center'>{title}</h2>")
        layout.addWidget(title_label)
        layout.addWidget(content_widget)
