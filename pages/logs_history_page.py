from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.adminBack import adminPageBack

class LogsAndHistoryPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backend = adminPageBack()
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("System Logs")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Table
        self.system_logs_table = self.create_system_logs_table()
        layout.addWidget(self.system_logs_table)

    def create_system_logs_table(self):
        table = QtWidgets.QTableWidget()
        table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #C9EBCB;
            }
            QHeaderView::section {
                background-color: #B2C8B2;
                padding: 8px;
                border: none;
                font-family: 'Roboto', sans-serif;
                font-weight: bold;
            }
        """)
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels([
            "Log ID", "Log Message", "Timestamp", "User"
        ])
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        table.verticalHeader().setVisible(False)

        logs_data = self.backend.fetch_system_logs()
        self.populate_table(table, logs_data)
        return table

    def populate_table(self, table, data):
        table.setRowCount(len(data))
        for row, data_row in enumerate(data):
            for col, value in enumerate(data_row):
                table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LogsAndHistoryPage()
    window.showMaximized()
    sys.exit(app.exec_())
