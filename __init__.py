from PyQt5.QtWidgets import QApplication

from controllers.systemd_multiseater_manager_impl import SystemdMultiSeatManager
from view.main_window import MultiseatManagerApp
import sys

app = QApplication(sys.argv)
window = MultiseatManagerApp(SystemdMultiSeatManager())
window.show()
sys.exit(app.exec_())
