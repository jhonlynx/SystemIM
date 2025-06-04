import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets

class LogsAndHistoryPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title
        header_layout = QtWidgets.QHBoxLayout()
        
        # Title label
        title = QtWidgets.QLabel("Logs and History")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)

        # Add stretch to push the dropdown to the right
        header_layout.addStretch()

        # Dropdown to select between Transaction History and System Logs
        self.view_selector = QtWidgets.QComboBox()
        self.view_selector.addItems(["Transaction History", "System Logs"])
        self.view_selector.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
            }
        """)
        self.view_selector.currentIndexChanged.connect(self.switch_view)
        header_layout.addWidget(self.view_selector)

        layout.addLayout(header_layout)

        # Stack widget to hold the different tables
        self.table_stack = QtWidgets.QStackedWidget()
        
        # Create tables
        self.transaction_history_table = self.create_transaction_history_table()
        self.system_logs_table = self.create_system_logs_table()
        
        # Add tables to the stack
        self.table_stack.addWidget(self.transaction_history_table)
        self.table_stack.addWidget(self.system_logs_table)

        layout.addWidget(self.table_stack)

        # Show Transaction History by default
        self.table_stack.setCurrentIndex(0)

    def create_transaction_history_table(self):
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
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "Log ID", "Transaction ID", "Action", "Timestamp", "User", "Old Status", "New Status"
        ])
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        table.verticalHeader().setVisible(False)

        # Sample transaction history data
        history_data = [
            (1, "TR001", "Status Update", "2023-10-15 14:30:00", "John Doe", "PENDING", "COMPLETED"),
            (2, "TR002", "Status Update", "2023-10-15 15:00:00", "Jane Smith", "COMPLETED", "PENDING"),
            (3, "TR003", "Updated", "2023-10-15 16:00:00", "John Doe", "FAILED", "COMPLETED"),
        ]
        self.populate_table(table, history_data)
        return table

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

        # Sample system logs data
        logs_data = [
            (1, "User John Doe logged in", "2023-10-15 14:00:00", "John Doe"),
            (2, "Transaction TR001 completed", "2023-10-15 14:30:00", "John Doe"),
            (3, "Error: Failed to load transaction", "2023-10-15 16:30:00", "System"),
        ]
        self.populate_table(table, logs_data)
        return table

    def populate_table(self, table, data):
        table.setRowCount(len(data))
        for row, data_row in enumerate(data):
            for col, value in enumerate(data_row):
                table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

    def switch_view(self, index):
        self.table_stack.setCurrentIndex(index)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LogsAndHistoryPage()
    window.showMaximized()
    sys.exit(app.exec_())
