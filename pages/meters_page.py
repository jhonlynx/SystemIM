import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets
from backend.adminBack import adminPageBack
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


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
        self.filter_combo.addItems(["Meter Code", "Client Name", "Serial Number", "Last Read"])
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
        self.meter_table.setColumnCount(5)
        self.meter_table.setHorizontalHeaderLabels([
            "METER CODE", "CLIENT NAME", "SERIAL NUMBER", "LAST READ", "ACTION"
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
            return False  # No search input, show all rows

        if row_index >= len(self.all_meters_data):
            return True  # Invalid row index

        meter = self.all_meters_data[row_index]
        search_text = self.search_input.text().strip().lower()

        if not search_text:
            return False  # No search text, show all rows

        # Map combo box selection to correct column index
        field_mapping = {
            "Meter Code": 0,
            "Client Name": 1,   # now contains full name
            "Serial Number": 2,
            "Last Read": 3
        }

        filter_by = self.filter_combo.currentText()
        field_index = field_mapping.get(filter_by, -1)

        if field_index == -1:
            return True  # Invalid field selected

        try:
            field_value = str(meter[field_index]).lower()
        except IndexError:
            print("Invalid meter data structure:", meter)
            return True  # Skip invalid rows

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
        start_index = (self.current_page - 1) * self.records_per_page
        end_index = start_index + self.records_per_page

        # Filter rows based on search input
        filtered_data = [meter for i, meter in enumerate(data) if not self.is_row_filtered(i)]

        # Paginate filtered data
        paginated_data = filtered_data[start_index:end_index]

        for table_row, meter in enumerate(paginated_data):
            try:
                meter_code, full_name, serial_number, last_read, meter_id = meter
            except ValueError as e:
                print("Error unpacking meter data:", meter, e)
                continue

            self.meter_table.insertRow(table_row)

            self.meter_table.setItem(table_row, 0, QtWidgets.QTableWidgetItem(str(meter_code)))
            self.meter_table.setItem(table_row, 1, QtWidgets.QTableWidgetItem(full_name))
            self.meter_table.setItem(table_row, 2, QtWidgets.QTableWidgetItem(str(serial_number)))
            self.meter_table.setItem(table_row, 3, QtWidgets.QTableWidgetItem(str(last_read)))

            # Create a centered QPushButton with an icon
            view_button = QtWidgets.QPushButton()
            view_button.setIcon(QtGui.QIcon("../images/view.png"))
            view_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    padding: 5px;
                }
            """)
            view_button.clicked.connect(lambda _, mid=meter_id: self.view_meter_details(mid))

            # Center the button in the cell
            self.meter_table.setCellWidget(table_row, 4, view_button)

    def filter_table(self):
        self.current_page = 1
        self.update_pagination()

    def view_meter_details(self, meter_id):

        # Fetch detailed meter information
        meter_data = next((m for m in self.all_meters_data if m[4] == meter_id), None)

        if not meter_data:
            QtWidgets.QMessageBox.warning(self, "Error", "Meter data not found.")
            return

        # Get readings for this meter only
        IadminPageBack = adminPageBack()
        readings = IadminPageBack.fetch_readings_by_meter_id(meter_id)

        # Create dialog window
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Meter Readings - ID: {meter_id}")
        dialog.resize(900, 600)  # Set initial dialog size

        layout = QVBoxLayout(dialog)

        # Info Label
        info_label = QLabel(f"<b>Meter ID:</b> {meter_id}")
        info_label.setStyleSheet("font-size: 16px; padding-bottom: 10px;")
        layout.addWidget(info_label)

        if not readings:
            # Show message if no readings
            no_data_label = QLabel("No reading history found for this meter.")
            no_data_label.setStyleSheet("font-size: 14px; color: #555;")
            no_data_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_data_label)
        else:
            # Table setup
            table = QTableWidget()
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(["Reading ID", "Date", "Previous Reading", "Current Reading", "Meter ID"])
            table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
            table.verticalHeader().setVisible(False)

            # Populate table
            table.setRowCount(len(readings))
            for row, reading in enumerate(readings):
                try:
                    reading_id, reading_date, prev_reading, current_reading, _ = reading
                    table.setItem(row, 0, QTableWidgetItem(str(reading_id)))
                    table.setItem(row, 1, QTableWidgetItem(str(reading_date)))
                    table.setItem(row, 2, QTableWidgetItem(str(prev_reading)))
                    table.setItem(row, 3, QTableWidgetItem(str(current_reading)))
                    table.setItem(row, 4, QTableWidgetItem(str(meter_id)))
                except Exception as e:
                    print("Error unpacking reading:", reading, e)
                    continue

            layout.addWidget(table)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #81C784;
                color: white;
                padding: 8px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

        # Show dialog
        dialog.exec_() 


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MetersPage()
    window.show()
    sys.exit(app.exec_())