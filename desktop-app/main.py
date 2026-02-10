# main.py
import sys
import requests

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QFileDialog,
    QTextEdit,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class EquipmentApp(QWidget):
    """Desktop app for the Chemical Equipment Visualizer.

    Features:
    - Upload CSV file to backend
    - Show summary and data table
    - Show charts (equipment type distribution)
    - Show history of last 5 uploads
    - Download PDF report for latest upload
    """

    def __init__(self):
        super().__init__()
        # Django backend base URL (config/config.urls.py -> path('api/', include('equipment.urls')))
        self.backend_url = "http://127.0.0.1:8000/api"

        # ID of the most recently uploaded history record (for PDF download)
        self.uploaded_record_id = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.resize(1000, 700)

        layout = QVBoxLayout()

        # --- Upload section ---
        self.label = QLabel("Upload CSV of Chemical Equipment")
        layout.addWidget(self.label)

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)
        layout.addWidget(self.upload_btn)

        # --- Summary text ---
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        layout.addWidget(self.summary_text)

        # --- Matplotlib chart (equipment type distribution) ---
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # --- Detailed table for uploaded data ---
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        # --- Upload history (last 5 files) ---
        self.history_label = QLabel("Last 5 uploads")
        layout.addWidget(self.history_label)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Filename", "Total Equipment", "Uploaded At"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.history_table)

        # --- PDF download button ---
        self.download_pdf_btn = QPushButton("Download PDF Report for Latest Upload")
        self.download_pdf_btn.clicked.connect(self.download_pdf)
        layout.addWidget(self.download_pdf_btn)

        self.setLayout(layout)

        # Load existing history (if backend is running)
        self.load_history(silent=True)

    # ------------------------------------------------------------------
    # Backend calls
    # ------------------------------------------------------------------
    def upload_csv(self):
        """Upload a CSV file to the backend and display results."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)",
        )
        if not file_path:
            return

        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                # NOTE: backend URL is /api/upload/ (see backend/equipment/urls.py)
                response = requests.post(f"{self.backend_url}/upload/", files=files)

            if response.status_code == 200:
                data = response.json()
                # Show summary, table, charts
                self.show_summary(data)
                self.populate_table(data.get("table_data", []))
                self.show_charts(data)

                # Refresh history and set latest record ID for PDF download
                self.load_history(silent=False)
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Upload failed (status {response.status_code}): {response.text}",
                )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Exception while uploading: {str(e)}")

    def load_history(self, silent: bool = False):
        """Fetch and display last 5 uploads from the backend."""
        try:
            # backend/equipment/urls.py -> path('history/', upload_history)
            response = requests.get(f"{self.backend_url}/history/")
            if response.status_code == 200:
                history = response.json() or []
                self.populate_history(history)

                # Most recent record is first in the list (views: order_by('-uploaded_at'))
                if history:
                    self.uploaded_record_id = history[0].get("id")
            else:
                if not silent:
                    QMessageBox.warning(
                        self,
                        "Error",
                        f"Failed to load history (status {response.status_code}): {response.text}",
                    )
        except Exception as e:
            if not silent:
                QMessageBox.critical(self, "Error", f"Exception while loading history: {str(e)}")

    def download_pdf(self):
        """Download PDF report for the latest uploaded record."""
        if not self.uploaded_record_id:
            QMessageBox.warning(
                self,
                "Error",
                "No uploaded record found. Upload a file first.",
            )
            return

        try:
            # backend/equipment/urls.py -> path('download-pdf/', download_pdf)
            response = requests.get(
                f"{self.backend_url}/download-pdf/?id={self.uploaded_record_id}"
            )
            if response.status_code == 200:
                save_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Save PDF",
                    f"report_{self.uploaded_record_id}.pdf",
                    "PDF Files (*.pdf)",
                )
                if save_path:
                    with open(save_path, "wb") as f:
                        f.write(response.content)
                    QMessageBox.information(
                        self,
                        "Success",
                        f"PDF saved: {save_path}",
                    )
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"PDF download failed (status {response.status_code}): {response.text}",
                )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Exception while downloading PDF: {str(e)}")

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------
    def show_summary(self, data: dict):
        text = f"Total Equipment: {data.get('total_equipment')}\n"
        text += f"Average Flowrate: {data.get('average_flowrate')}\n"
        text += f"Average Pressure: {data.get('average_pressure')}\n"
        text += f"Average Temperature: {data.get('average_temperature')}\n\n"

        text += "Equipment Type Distribution:\n"
        for etype, count in data.get("equipment_type_distribution", {}).items():
            text += f"{etype}: {count}\n"

        self.summary_text.setText(text)

    def populate_table(self, table_data):
        # Clear table if no data
        if not table_data:
            self.table_widget.clear()
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)
            return

        headers = list(table_data[0].keys())
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setRowCount(len(table_data))

        for row_idx, row_data in enumerate(table_data):
            for col_idx, header in enumerate(headers):
                item = QTableWidgetItem(str(row_data.get(header, "")))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table_widget.setItem(row_idx, col_idx, item)

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def populate_history(self, history):
        """Fill the history table with last 5 uploads."""
        self.history_table.setRowCount(len(history))

        for row_idx, record in enumerate(history):
            filename_item = QTableWidgetItem(str(record.get("filename", "")))
            total_item = QTableWidgetItem(str(record.get("total_equipment", "")))
            uploaded_item = QTableWidgetItem(str(record.get("uploaded_at", "")))

            for item in (filename_item, total_item, uploaded_item):
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            self.history_table.setItem(row_idx, 0, filename_item)
            self.history_table.setItem(row_idx, 1, total_item)
            self.history_table.setItem(row_idx, 2, uploaded_item)

        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def show_charts(self, data: dict):
        """Render charts using matplotlib (currently: equipment type distribution)."""
        dist = data.get("equipment_type_distribution", {}) or {}

        # Clear the figure and draw a new chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if dist:
            types = list(dist.keys())
            counts = list(dist.values())
            ax.bar(types, counts, color="skyblue")
            ax.set_xlabel("Equipment Type")
            ax.set_ylabel("Count")
            ax.set_title("Equipment Type Distribution")
            ax.tick_params(axis="x", rotation=45)
        else:
            ax.text(
                0.5,
                0.5,
                "No chart data available",
                ha="center",
                va="center",
                transform=ax.transAxes,
            )

        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Global violet/blue theme for the whole app
    app.setStyleSheet(
        """
        QWidget {
            background-color: #1b1233;            /* deep violet */
            color: #E4E7F5;                       /* light text */
            font-family: "Segoe UI", sans-serif;
            font-size: 10pt;
        }

        QLabel {
            color: #E4E7F5;
            font-weight: 600;
        }

        QPushButton {
            background-color: #3f51b5;           /* indigo/blue */
            color: #ffffff;
            border-radius: 6px;
            padding: 6px 12px;
            border: 1px solid #5c6bc0;
        }

        QPushButton:hover {
            background-color: #5c6bc0;
        }

        QPushButton:pressed {
            background-color: #283593;
        }

        QTextEdit {
            background-color: #241944;           /* slightly lighter violet */
            border: 1px solid #3949ab;
            border-radius: 4px;
        }

        QTableWidget {
            background-color: #241944;
            gridline-color: #3949ab;
            border: 1px solid #3949ab;
            border-radius: 4px;
            selection-background-color: #3949ab;
            selection-color: #ffffff;
        }

        QHeaderView::section {
            background-color: #303f9f;
            color: #E4E7F5;
            padding: 4px;
            border: 1px solid #1b1233;
        }

        QScrollBar:vertical {
            background: #1b1233;
            width: 10px;
            margin: 0px;
        }

        QScrollBar::handle:vertical {
            background: #3949ab;
            min-height: 20px;
            border-radius: 4px;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }
        """
    )

    window = EquipmentApp()
    window.show()
    sys.exit(app.exec_())
