from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from model.app_feedback import AppFeedback


class FeedbackBanner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVisible(False)

        # Stretch across width
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.message_label = QLabel()
        self.message_label.setWordWrap(True)
        self.message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.close_button = QPushButton("✖")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("border: none; background: transparent;")
        self.close_button.clicked.connect(self.hide)

        layout = QHBoxLayout()
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(10)
        layout.addWidget(self.message_label)
        layout.addStretch()
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def display_feedback(self, feedback: AppFeedback):
        colors = {
            "success": "#d4edda",  # light green
            "warning": "#fff3cd",  # light orange
            "error": "#f8d7da",    # light red
        }
        borders = {
            "success": "#155724",
            "warning": "#856404",
            "error": "#721c24",
        }

        bg = colors.get(feedback.feedback_type, "#e2e3e5")
        border = borders.get(feedback.feedback_type, "#383d41")

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg};
                border-left: 6px solid {border};
                padding: 10px;
                border-radius: 0px;
            }}
            QLabel {{
                color: #000;
                font-size: 10pt;
            }}
        """)

        self.message_label.setText(f"{feedback}")
        self.setVisible(True)
