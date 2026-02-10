
from PyQt5.QtWidgets import QApplication, QPushButton
import sys

app = QApplication(sys.argv)
btn = QPushButton("Upload CSV")
btn.show()
sys.exit(app.exec_())
