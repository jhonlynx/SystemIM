import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets
from backend.adminBack import adminPageBack


class MetersPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.all_meters_data = []  # Store all meter data
        self.current_page = 1
        self.records_per_page = 10  # Number of records per page
        self.total_pages = 1
        self.setup_ui()
        self.showMaximized()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header Panel
        header_panel = QtWidgets.QWidget()
        header_panel.setStyleSheet("background-color: #f5f5f5; border-bottom: 1px solid #ddd;")
        header_layout = QtWidgets.QVBoxLayout(header_panel)
        header_layout.setContentsMargins(20, 15, 20, 15)

        # Header with title, search bar, and dropdown
        controls_layout = QtWidgets.QHBoxLayout()

        # Title
        title = QtWidgets.QLabel("METERS LIST")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        controls_layout.addWidget(title)
        controls_layout.addStretch()  # Pushes everything after title to the right

        # Filter Combo Box
        self.filter_combo = QtWidgets.QComboBox()
        self.filter_combo.addItems(["Meter ID", "Serial Number", "Meter Code", "Last Read"])
        self.filter_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 150px;
                background-color: white;
            }
        """)
        controls_layout.addWidget(self.filter_combo)

        # Search Input Field
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search meters...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 250px;
                background-color: white;
            }
        """)
        self.search_input.textChanged.connect(self.filter_table)
        controls_layout.addWidget(self.search_input)

        # Add the horizontal layout to the header
        header_layout.addLayout(controls_layout)
        layout.addWidget(header_panel)

        # Table Widget (unchanged)
        self.meter_table = QtWidgets.QTableWidget()
        self.meter_table.setAlternatingRowColors(True)
        self.meter_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: #E8F5E9;
                alternate-background-color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #B2C8B2;
                padding: 8px;
                border: none;
                font-family: 'Roboto', sans-serif;
                font-weight: bold;
                font-size: 15px;
            }
            QTableWidget::item:selected {
                background-color: transparent;
                color: black;
            }
            QTableWidget::item:hover {
                background-color: transparent;
            }
        """)
        self.meter_table.setColumnCount(4)
        self.meter_table.setHorizontalHeaderLabels([
            "METER ID", "SERIAL NUMBER", "METER CODE", "LAST READ"
        ])
        self.meter_table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.meter_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.meter_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.meter_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.meter_table.verticalHeader().setVisible(False)

        layout.addWidget(self.meter_table)

        # Fetch all meters data
        IadminPageBack = adminPageBack()
        self.all_meters_data = IadminPageBack.fetch_meters()
        self.populate_table(self.all_meters_data)

        # Pagination Controls
        pagination_layout = QtWidgets.QHBoxLayout()
        pagination_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.first_page_btn = QtWidgets.QPushButton("⏮ First")
        self.prev_page_btn = QtWidgets.QPushButton("◀ Previous")
        self.page_indicator = QtWidgets.QLabel("Page 1 of 1")
        self.next_page_btn = QtWidgets.QPushButton("Next ▶")
        self.last_page_btn = QtWidgets.QPushButton("Last ⏭")

        self.first_page_btn.clicked.connect(self.go_to_first_page)
        self.prev_page_btn.clicked.connect(self.go_to_prev_page)
        self.next_page_btn.clicked.connect(self.go_to_next_page)
        self.last_page_btn.clicked.connect(self.go_to_last_page)

        btn_style = """
            QPushButton {
                background-color: #81C784;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
            QPushButton:disabled {
                background-color: #E0E0E0;
                color: #9E9E9E;
            }
        """
        self.first_page_btn.setStyleSheet(btn_style)
        self.prev_page_btn.setStyleSheet(btn_style)
        self.next_page_btn.setStyleSheet(btn_style)
        self.last_page_btn.setStyleSheet(btn_style)
        self.page_indicator.setStyleSheet("font-weight: bold; min-width: 150px;")

        pagination_layout.addWidget(self.first_page_btn)
        pagination_layout.addWidget(self.prev_page_btn)
        pagination_layout.addWidget(self.page_indicator)
        pagination_layout.addWidget(self.next_page_btn)
        pagination_layout.addWidget(self.last_page_btn)

        # Records per page selector
        self.page_size_label = QtWidgets.QLabel("Records per page:")
        self.page_size_combo = QtWidgets.QComboBox()
        self.page_size_combo.addItems(["5", "10", "20", "50", "100"])
        self.page_size_combo.setCurrentText(str(self.records_per_page))
        self.page_size_combo.currentTextChanged.connect(self.change_page_size)
        pagination_layout.addWidget(self.page_size_label)
        pagination_layout.addWidget(self.page_size_combo)

        layout.addLayout(pagination_layout)

        self.update_pagination()

    def update_pagination(self):
        visible_rows = 0
        for row in range(len(self.all_meters_data)):
            if not self.is_row_filtered(row):
                visible_rows += 1
        self.total_pages = max(1, math.ceil(visible_rows / self.records_per_page))
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
        self.page_indicator.setText(f"Page {self.current_page} of {self.total_pages}")
        self.first_page_btn.setEnabled(self.current_page > 1)
        self.prev_page_btn.setEnabled(self.current_page > 1)
        self.next_page_btn.setEnabled(self.current_page < self.total_pages)
        self.last_page_btn.setEnabled(self.current_page < self.total_pages)
        self.populate_table(self.all_meters_data)

    def is_row_filtered(self, row_index):
        if not hasattr(self, 'search_input') or self.search_input is None:
            return False

        if row_index >= len(self.all_meters_data):
            return True

        meter = self.all_meters_data[row_index]
        search_text = self.search_input.text().lower()
        if not search_text:
            return False

        # Map combo box selection to column index
        field_mapping = {
            "Meter ID": 0,
            "Serial Number": 1,
            "Meter Code": 2,
            "Last Read": 3
        }

        filter_by = self.filter_combo.currentText()
        field_index = field_mapping.get(filter_by, -1)

        if field_index == -1:
            return True  # Invalid field

        field_value = str(meter[field_index]).lower()
        return search_text not in field_value

    def go_to_first_page(self):
        if self.current_page != 1:
            self.current_page = 1
            self.update_pagination()

    def go_to_prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination()

    def go_to_next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_pagination()

    def go_to_last_page(self):
        if self.current_page != self.total_pages:
            self.current_page = self.total_pages
            self.update_pagination()

    def change_page_size(self, size):
        self.records_per_page = int(size)
        self.current_page = 1
        self.update_pagination()

    def populate_table(self, data):
        self.meter_table.setRowCount(0)
        visible_row_counter = 0
        rows_to_show = []

        for row_index, meter in enumerate(data):
            if not self.is_row_filtered(row_index):
                visible_row_counter += 1
                start_index = (self.current_page - 1) * self.records_per_page + 1
                end_index = self.current_page * self.records_per_page
                if start_index <= visible_row_counter <= end_index:
                    rows_to_show.append(meter)

        self.meter_table.setRowCount(len(rows_to_show))

        for table_row, meter in enumerate(rows_to_show):
            try:
                meter_id, serial_number, meter_code, last_read = meter
            except ValueError as e:
                print("Error unpacking meter data:", meter, e)
                continue

            self.meter_table.setItem(table_row, 0, QtWidgets.QTableWidgetItem(str(meter_id)))
            self.meter_table.setItem(table_row, 1, QtWidgets.QTableWidgetItem(serial_number))
            self.meter_table.setItem(table_row, 2, QtWidgets.QTableWidgetItem(meter_code))
            self.meter_table.setItem(table_row, 3, QtWidgets.QTableWidgetItem(str(last_read)))

    def filter_table(self):
        self.current_page = 1
        self.update_pagination()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MetersPage()
    window.show()
    sys.exit(app.exec_())