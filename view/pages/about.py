from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextBrowser

from view.components.page_wrapper import PageWrapper


class AboutPage(PageWrapper):
    """An About page describing the application."""

    def __init__(self, parent=None):
        content_widget = self.build_ui()
        super().__init__("About", content_widget)

    def build_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        about_text = QTextBrowser()
        about_text.setReadOnly(True)
        about_text.setOpenExternalLinks(True)
        about_text.setHtml("""
            <h2>🎛️ MultiSeat Manager</h2>
            <p>This is a lightweight Linux GUI tool for managing multiseat setups using <code>loginctl</code> from <code>systemd</code>.</p>

            <h3>📦 Features</h3>
            <ul>
                <li>🪑 View and manage system seats</li>
                <li>🖥️ Attach/detach devices to seats</li>
                <li>👤 View active sessions and user activity</li>
            </ul>

            <h3>🔧 Technologies</h3>
            <ul>
                <li>Python 3</li>
                <li>PyQt5 for the GUI</li>
                <li>Systemd's loginctl for backend operations</li>
            </ul>

            <h3>📝 Notes</h3>
            <p>I’ve done my best to make this tool functional and useful, but it’s not guaranteed to work perfectly in all situations or system configurations.</p>
            <p>Please use it responsibly and with care. 😊</p>

            <h3>🌐 Connect</h3>
            <p>
                <a href="https://github.com/RodrickVy" target="_blank">🐙 GitHub</a><br>
                <a href="https://www.youtube.com/@r%C3%B8dvy" target="_blank">📺 YouTube</a>
            </p>
        """)

        layout.addWidget(about_text)
        return widget