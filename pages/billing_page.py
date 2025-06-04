import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
import math  # Add this import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog

from backend.adminBack import adminPageBack

class EmployeeBillingPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        
        # Initialize pagination variables before setup_ui
        self.rows_per_page = 10
        self.current_page = 1
        self.total_pages = 1
        self.all_data = []  # Store all data for pagination
        self.filtered_data = []  # Store filtered data for pagination
        
        # Now call setup_ui after initializing variables
        self.setup_ui()

    def create_scrollable_cell(self, row, column, text):
        scrollable_widget = ScrollableTextWidget(text)
        self.billing_table.setCellWidget(row, column, scrollable_widget)

    def create_action_cell(self, row, billing_data):
        """Create action cell with print button"""
        action_widget = QtWidgets.QWidget()
        action_layout = QtWidgets.QHBoxLayout(action_widget)
        action_layout.setContentsMargins(5, 5, 5, 5)
        action_layout.setAlignment(QtCore.Qt.AlignCenter)
        
        # Print button - Handle missing icon gracefully
        print_btn = QtWidgets.QPushButton()
        
        # Try to set icon, but don't fail if file doesn't exist
        try:
            if os.path.exists("images/print.png"):
                print_btn.setIcon(QtGui.QIcon("images/print.png"))
            else:
                print_btn.setText("🖨")  # Use emoji as fallback
        except:
            print_btn.setText("Print")  # Text fallback
        
        print_btn.setToolTip("Print Bill")
        print_btn.setFixedSize(30, 30)
        print_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # Connect print button to print function
        print_btn.clicked.connect(lambda: self.print_bill(billing_data))
        
        action_layout.addWidget(print_btn)
        self.billing_table.setCellWidget(row, 8, action_widget)

    def print_bill(self, billing_data):
        """Print bill with preview"""
        try:
            # Create printer with better settings
            printer = QPrinter(QPrinter.HighResolution)
            printer.setPageSize(QPrinter.A4)
            printer.setOrientation(QPrinter.Portrait)
            printer.setPageMargins(10, 10, 10, 10, QPrinter.Millimeter)  # Set margins
            
            # Create print preview dialog
            preview_dialog = QPrintPreviewDialog(printer, self)
            preview_dialog.setWindowTitle("Print Preview - Bill")
            preview_dialog.resize(800, 600)
            
            # Connect paint request to print function
            preview_dialog.paintRequested.connect(lambda p: self.paint_bill(p, billing_data))
            
            # Show preview dialog
            result = preview_dialog.exec_()
            
            if result == QtWidgets.QDialog.Accepted:
                print("Print job completed or sent to printer")
            
        except Exception as e:
            error_msg = f"Failed to print bill: {str(e)}"
            print(error_msg)  # For debugging
            QtWidgets.QMessageBox.warning(self, "Print Error", error_msg)

    def paint_bill(self, printer, billing_data):
        """Paint the bill content for printing"""
        painter = QtGui.QPainter(printer)
        
        if not painter.isActive():
            print("Painter is not active")
            return
        
        try:
            # Get billing data
            billing_code, issued_date, billing_due, client_name, client_lname, client_location, billing_total, status = billing_data
            
            # Set up fonts
            title_font = QtGui.QFont("Arial", 18, QtGui.QFont.Bold)
            header_font = QtGui.QFont("Arial", 14, QtGui.QFont.Bold)
            subheader_font = QtGui.QFont("Arial", 12, QtGui.QFont.Bold)
            content_font = QtGui.QFont("Arial", 11)
            small_font = QtGui.QFont("Arial", 9)
            
            # Get page dimensions
            page_rect = printer.pageRect()
            margin = 80
            content_width = page_rect.width() - (2 * margin)
            
            # Starting position
            y_pos = margin
            line_height = 30
            section_spacing = 40
            
            # Helper function to draw centered text
            def draw_centered_text(text, font, y_position, height=30):
                painter.setFont(font)
                text_rect = QtCore.QRect(margin, y_position, content_width, height)
                painter.drawText(text_rect, QtCore.Qt.AlignCenter, text)
                return y_position + height
            
            # Helper function to draw left-aligned text
            def draw_left_text(text, font, y_position, height=25):
                painter.setFont(font)
                text_rect = QtCore.QRect(margin, y_position, content_width, height)
                painter.drawText(text_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, text)
                return y_position + height
            
            # Helper function to draw right-aligned text
            def draw_right_text(text, font, y_position, height=25):
                painter.setFont(font)
                text_rect = QtCore.QRect(margin, y_position, content_width, height)
                painter.drawText(text_rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, text)
                return y_position + height
            
            # Title
            y_pos = draw_centered_text("WATER BILLING STATEMENT", title_font, y_pos, 40)
            y_pos += 20
            
            # Company info
            y_pos = draw_centered_text("WATER UTILITY COMPANY", header_font, y_pos, 35)
            y_pos += section_spacing
            
            # Draw a horizontal line
            painter.drawLine(margin, y_pos, margin + content_width, y_pos)
            y_pos += 20
            
            # Bill Information Section
            y_pos = draw_left_text("BILL INFORMATION", subheader_font, y_pos, 30)
            y_pos += 10
            
            painter.setFont(content_font)
            
            # Create two columns for bill info
            left_column_x = margin
            right_column_x = margin + (content_width // 2)
            
            # Left column
            current_y = y_pos
            painter.drawText(left_column_x, current_y, f"Billing Code: {billing_code}")
            current_y += line_height
            painter.drawText(left_column_x, current_y, f"Issue Date: {issued_date}")
            current_y += line_height
            
            # Right column
            current_y = y_pos
            painter.drawText(right_column_x, current_y, f"Due Date: {billing_due}")
            current_y += line_height
            painter.drawText(right_column_x, current_y, f"Status: {status}")
            current_y += line_height
            
            y_pos = current_y + 20
            
            # Customer Information Section
            y_pos = draw_left_text("CUSTOMER INFORMATION", subheader_font, y_pos, 30)
            y_pos += 10
            
            painter.setFont(content_font)
            painter.drawText(margin, y_pos, f"Name: {client_name} {client_lname}")
            y_pos += line_height
            painter.drawText(margin, y_pos, f"Location: {client_location}")
            y_pos += section_spacing
            
            # Billing Details Section
            y_pos = draw_left_text("BILLING DETAILS", subheader_font, y_pos, 30)
            y_pos += 10
            
            # Create table
            table_top = y_pos
            table_height = 80
            table_rect = QtCore.QRect(margin, table_top, content_width, table_height)
            
            # Draw table border
            painter.drawRect(table_rect)
            
            # Draw table header
            header_height = 25
            painter.setFont(subheader_font)
            
            # Table headers
            desc_rect = QtCore.QRect(margin + 10, table_top + 5, content_width - 200, header_height)
            amount_rect = QtCore.QRect(margin + content_width - 180, table_top + 5, 170, header_height)
            
            painter.drawText(desc_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, "Description")
            painter.drawText(amount_rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, "Amount")
            
            # Draw horizontal line under header
            header_line_y = table_top + header_height + 5
            painter.drawLine(margin, header_line_y, margin + content_width, header_line_y)
            
            # Table content
            painter.setFont(content_font)
            content_y = header_line_y + 10
            
            desc_content_rect = QtCore.QRect(margin + 10, content_y, content_width - 200, 20)
            amount_content_rect = QtCore.QRect(margin + content_width - 180, content_y, 170, 20)
            
            painter.drawText(desc_content_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, "Water Consumption")
            painter.drawText(amount_content_rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, f"₱{billing_total}")
            
            y_pos = table_top + table_height + 30
            
            # Total Section
            painter.setFont(header_font)
            total_rect = QtCore.QRect(margin + content_width - 250, y_pos, 240, 30)
            painter.drawText(total_rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, f"TOTAL AMOUNT: ₱{billing_total}")
            
            # Footer
            footer_y = page_rect.height() - margin - 60
            painter.setFont(small_font)
            
            # Draw footer line
            painter.drawLine(margin, footer_y - 10, margin + content_width, footer_y - 10)
            
            footer_rect = QtCore.QRect(margin, footer_y, content_width, 30)
            painter.drawText(footer_rect, QtCore.Qt.AlignCenter, "Thank you for your payment!")
            
            # Add payment instructions
            payment_y = footer_y + 25
            payment_rect = QtCore.QRect(margin, payment_y, content_width, 20)
            painter.drawText(payment_rect, QtCore.Qt.AlignCenter, "Please pay on or before the due date to avoid penalties.")
            
        except Exception as e:
            print(f"Error painting bill: {str(e)}")
            # Draw error message on the page
            painter.setFont(QtGui.QFont("Arial", 12))
            error_rect = QtCore.QRect(margin, margin, content_width, 50)
            painter.drawText(error_rect, QtCore.Qt.AlignCenter, f"Error generating bill: {str(e)}")
        
        # Note: Don't call painter.end() here - QPrintPreviewDialog handles it

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Define input style at the beginning
        input_style = """
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 250px;
            }
        """

        # Header with title and search
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("BILLING LIST")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Search and Add button container
        search_add_layout = QtWidgets.QHBoxLayout() 
        
        # Search container
        search_container = QtWidgets.QHBoxLayout()
        
        # Search criteria dropdown
        self.search_criteria = QtWidgets.QComboBox()
        self.search_criteria.addItems(["BILLING CODE", "CLIENT NAME", "CLIENT LOCATION"])
        self.search_criteria.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 120px;
                background-color: white;
            }
        """)
        search_container.addWidget(self.search_criteria)
        
        # Search input
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search billings...")
        self.search_input.setStyleSheet(input_style)
        search_container.addWidget(self.search_input)
        self.search_input.textChanged.connect(self.filter_table)
        
        # Add status filter dropdown
        self.status_filter = QtWidgets.QComboBox()
        self.status_filter.addItems(["ALL", "TO BE PRINTED", "PRINTED", "VOID", "PENDING PAYMENT", "PAID"])
        self.status_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 150px;
                background-color: white;
            }
        """)
        self.status_filter.currentTextChanged.connect(self.filter_table)
        search_container.addWidget(self.status_filter)
        
        # Add search container to search_add_layout
        search_add_layout.addLayout(search_container)
        
        # Add button with icon
        add_btn = QtWidgets.QPushButton("ADD BILLING", icon=QtGui.QIcon("images/add.png"))
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(229, 115, 115);
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
            }
            QPushButton:hover {
                background-color: rgb(200, 100, 100);
            }
        """)
        add_btn.clicked.connect(self.show_add_billing)
        search_add_layout.addWidget(add_btn)
        
        # Add search_add_layout to header_layout
        header_layout.addLayout(search_add_layout)
        layout.addLayout(header_layout)
        
        # Create billing table before accessing it
        self.billing_table = QtWidgets.QTableWidget()
        self.billing_table.setAlternatingRowColors(True)
        self.billing_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #E8F5E9;
                alternate-background-color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #B2C8B2;
                padding: 8px;
                border: none;
                font-family: 'Roboto', sans-serif;
                font-weight: bold;
            }
        """)
        
        # Set up table columns - Added ACTION column
        self.billing_table.setColumnCount(9)  # Increased from 8 to 9
        self.billing_table.setHorizontalHeaderLabels([
            "BILLING CODE", "ISSUED DATE", "BILLING DUE", 
            "NAME", "LAST NAME","LOCATION", "BILLING TOTAL", "STATUS", "ACTION"
        ])

        # Set the table to fill all available space
        self.billing_table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.billing_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        # Set ACTION column to fixed width
        self.billing_table.horizontalHeader().setSectionResizeMode(8, QtWidgets.QHeaderView.Fixed)
        self.billing_table.setColumnWidth(8, 80)
        
        # Enable horizontal scrollbar
        self.billing_table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.billing_table.setWordWrap(False)

        billing_back = adminPageBack()
        self.all_data = billing_back.fetch_billing()
        self.filtered_data = self.all_data.copy()  # Initialize filtered data with all data
        
        # Now we can safely adjust table properties
        self.billing_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # Reset ACTION column to fixed width after stretch
        self.billing_table.horizontalHeader().setSectionResizeMode(8, QtWidgets.QHeaderView.Fixed)
        self.billing_table.setColumnWidth(8, 80)
        
        self.billing_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.billing_table.verticalHeader().setVisible(False)
        self.billing_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
        # Create a custom delegate for text elision with tooltip
        delegate = TextEllipsisDelegate(self.billing_table)
        self.billing_table.setItemDelegate(delegate)

        # Add table to the main layout with full expansion
        layout.addWidget(self.billing_table)
        
        # Add pagination controls
        pagination_layout = QtWidgets.QHBoxLayout()
        pagination_layout.setAlignment(QtCore.Qt.AlignCenter)
        
        # First page button
        self.first_page_btn = QtWidgets.QPushButton("⏮ First")
        self.first_page_btn.clicked.connect(self.go_to_first_page)
        
        # Previous page button
        self.prev_page_btn = QtWidgets.QPushButton("◀ Previous")
        self.prev_page_btn.clicked.connect(self.go_to_prev_page)
        
        # Page indicator
        self.page_indicator = QtWidgets.QLabel("Page 1 of 1")
        self.page_indicator.setAlignment(QtCore.Qt.AlignCenter)
        self.page_indicator.setStyleSheet("font-weight: bold; min-width: 150px;")
        
        # Next page button
        self.next_page_btn = QtWidgets.QPushButton("Next ▶")
        self.next_page_btn.clicked.connect(self.go_to_next_page)
        
        # Last page button
        self.last_page_btn = QtWidgets.QPushButton("Last ⏭")
        self.last_page_btn.clicked.connect(self.go_to_last_page)
        
        # Records per page selector
        self.page_size_label = QtWidgets.QLabel("Records per page:")
        self.rows_per_page_combo = QtWidgets.QComboBox()
        self.rows_per_page_combo.addItems(["5", "10", "20", "50", "100"])
        self.rows_per_page_combo.setCurrentText(str(self.rows_per_page))
        self.rows_per_page_combo.currentTextChanged.connect(self.change_rows_per_page)
        
        # Style for pagination buttons
        pagination_btn_style = """
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
        
        self.first_page_btn.setStyleSheet(pagination_btn_style)
        self.prev_page_btn.setStyleSheet(pagination_btn_style)
        self.next_page_btn.setStyleSheet(pagination_btn_style)
        self.last_page_btn.setStyleSheet(pagination_btn_style)
        
        # Add pagination controls to layout
        pagination_layout.addWidget(self.first_page_btn)
        pagination_layout.addWidget(self.prev_page_btn)
        pagination_layout.addWidget(self.page_indicator)
        pagination_layout.addWidget(self.next_page_btn)
        pagination_layout.addWidget(self.last_page_btn)
        pagination_layout.addSpacing(20)
        pagination_layout.addWidget(self.page_size_label)
        pagination_layout.addWidget(self.rows_per_page_combo)
        
        layout.addLayout(pagination_layout)
        
        # Calculate total pages and update table
        self.update_pagination()

    def update_pagination(self):
        # Calculate total pages based on filtered data
        visible_rows = len(self.filtered_data)
        self.total_pages = max(1, math.ceil(visible_rows / self.rows_per_page))
        
        # Adjust current page if it's beyond the new total
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
        
        # Update page indicator
        self.page_indicator.setText(f"Page {self.current_page} of {self.total_pages}")
        
        # Enable/disable navigation buttons
        self.first_page_btn.setEnabled(self.current_page > 1)
        self.prev_page_btn.setEnabled(self.current_page > 1)
        self.next_page_btn.setEnabled(self.current_page < self.total_pages)
        self.last_page_btn.setEnabled(self.current_page < self.total_pages)
        
        # Update table with current page data
        self.populate_table_for_page()

    def populate_table_for_page(self):
        data_to_display = self.filtered_data
        
        # Calculate start and end indices for the current page
        start_idx = (self.current_page - 1) * self.rows_per_page
        end_idx = min(start_idx + self.rows_per_page, len(data_to_display))
        
        # Get data for current page
        page_data = data_to_display[start_idx:end_idx]
        
        # Set the table row count
        self.billing_table.setRowCount(len(page_data))
        
        # Fill the table with data
        for i, billing in enumerate(page_data):
            # Unpack values
            billing_code, issued_date, billing_due, client_name, client_lname,  client_location, billing_total, status = billing
            
            # Add billing data to the table
            self.create_scrollable_cell(i, 0, str(billing_code))
            self.create_scrollable_cell(i, 1, str(issued_date))
            self.create_scrollable_cell(i, 2, str(billing_due))
            self.create_scrollable_cell(i, 3, client_name)
            self.create_scrollable_cell(i, 4, client_lname)
            self.create_scrollable_cell(i, 5, client_location)
            self.create_scrollable_cell(i, 6, str(billing_total))
            
            # Status with color coding
            status_item = QtWidgets.QTableWidgetItem(status)
            status_item.setForeground(
                QtGui.QColor("#64B5F6") if status == "PAID" else QtGui.QColor("#E57373")
            )
            self.billing_table.setItem(i, 7, status_item)
            
            # Add action cell with print button
            self.create_action_cell(i, billing)

    def populate_table(self, data):
        # Update all data and repopulate
        self.all_data = data
        self.filtered_data = data.copy()
        self.current_page = 1  # Reset to first page when data changes
        self.update_pagination()

    def filter_table(self):
        search_by = self.search_criteria.currentText()
        search_text = self.search_input.text().lower()
        status_filter = self.status_filter.currentText()

        column_mapping = {
            "CLIENT NAME": 3,
            "CLIENT LAST NAME": 4,
            "CLIENT LOCATION": 5
        }
        
        col_index = column_mapping.get(search_by, 0)
        
        # Filter the data based on search criteria and status
        self.filtered_data = self.all_data.copy()
        
        # Apply search text filter
        if search_text:
            self.filtered_data = [
                row for row in self.filtered_data 
                if search_text in str(row[col_index]).lower()
            ]
        
        # Apply status filter
        if status_filter != "ALL":
            self.filtered_data = [
                row for row in self.filtered_data
                if row[7] == status_filter  # Status is at index 7
            ]
        
        # Reset to first page and update
        self.current_page = 1
        self.update_pagination()

    def change_rows_per_page(self, value):
        self.rows_per_page = int(value)
        self.current_page = 1  # Reset to first page
        self.update_pagination()
    
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

    def show_add_billing(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Add New Bill")
        dialog.setFixedSize(1000, 700)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #C9EBCB;
            }
            QLabel {
                font-family: 'Arial', sans-serif;
                font-weight: bold;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.setSpacing(10)

        # Section Title
        title = QtWidgets.QLabel("BILLING INFORMATION FORM")
        title.setStyleSheet("""
            font-size: 20px;
            padding: 10px;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Form Layout
        form_layout = QtWidgets.QGridLayout()
        form_layout.setHorizontalSpacing(40)
        form_layout.setVerticalSpacing(20)

        input_style = """
            QLineEdit, QDateEdit, QComboBox {
                font-family: 'Arial';
                font-size: 14px;
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #ffffff;
            }
        """

        readonly_style = """
        QLineEdit {
            font-family: 'Arial';
            font-size: 14px;
            padding: 8px;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            background-color: #e0e0e0;
            color: #555555;
        }
    """


        # --- LEFT COLUMN ---

        def create_labeled_widget(label_text, widget):
            layout = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel(label_text)
            label.setFont(QtGui.QFont("Arial", 10))
            layout.addWidget(label)
            layout.addWidget(widget)
            return layout

        
        client = QtWidgets.QComboBox()
        client.setStyleSheet(input_style)

        reading_date = QtWidgets.QDateEdit()
        reading_date.setCalendarPopup(True)
        reading_date.setStyleSheet(input_style)
        reading_date.setMaximumDate(QtCore.QDate.currentDate())
        reading_date.setDate(QtCore.QDate.currentDate())  # Set current date as default
         

        previous_reading = QtWidgets.QLineEdit()
        previous_reading.setReadOnly(True)
        previous_reading.setStyleSheet(readonly_style)

        present_reading = QtWidgets.QLineEdit()
        present_reading.setEnabled(False)
        present_reading.setStyleSheet(readonly_style)

        cubic_meter_consumed = QtWidgets.QLineEdit()
        cubic_meter_consumed.setReadOnly(True)
        cubic_meter_consumed.setStyleSheet(readonly_style)

        amount = QtWidgets.QLineEdit()
        amount.setReadOnly(True)
        amount.setStyleSheet(readonly_style)

        due_date = QtWidgets.QDateEdit()
        due_date.setCalendarPopup(True)
        due_date.setStyleSheet(input_style)
        due_date.setMinimumDate(QtCore.QDate.currentDate())

        # Bold centered section header
        additional_charge_label = QtWidgets.QLabel("ADDITIONAL CHARGE")
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(11)
        additional_charge_label.setFont(font)
        additional_charge_label.setAlignment(QtCore.Qt.AlignCenter)
        form_layout.addWidget(additional_charge_label, 0, 1)

        subscribe_capital = QtWidgets.QLineEdit()
        subscribe_capital.setStyleSheet(input_style)

        late_payment = QtWidgets.QLineEdit()
        late_payment.setStyleSheet(input_style)

        penalty = QtWidgets.QLineEdit()
        penalty.setStyleSheet(input_style)

        total_charge = QtWidgets.QLineEdit()
        total_charge.setStyleSheet(input_style)
        total_charge.setReadOnly(True)
        total_charge.setStyleSheet(readonly_style)

        total_bill = QtWidgets.QLineEdit()
        total_bill.setStyleSheet(input_style)
        total_bill.setReadOnly(True)
        total_bill.setStyleSheet(readonly_style)

        form_layout.addLayout(create_labeled_widget("SUBSCRIBE CAPITAL:", subscribe_capital), 1, 1)
        form_layout.addLayout(create_labeled_widget("LATE PAYMENT:", late_payment), 2, 1)
        form_layout.addLayout(create_labeled_widget("PENALTY:", penalty), 3, 1)
        form_layout.addLayout(create_labeled_widget("TOTAL CHARGE:", total_charge), 4, 1)
        form_layout.addLayout(create_labeled_widget("TOTAL BILL:", total_bill), 6, 1)

        # Add form_layout to main layout
        layout.addLayout(form_layout)


        # Button Container
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setAlignment(QtCore.Qt.AlignRight)

        # Cancel Button
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)

        # Save Button
        save_btn = QtWidgets.QPushButton("Save Bill")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        """)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addWidget(button_container)
        


        form_layout.addLayout(create_labeled_widget("CLIENT:", client), 0, 0)
        form_layout.addLayout(create_labeled_widget("READING DATE:", reading_date), 1, 0)
        form_layout.addLayout(create_labeled_widget("PREVIOUS READING:", previous_reading), 2, 0)
        form_layout.addLayout(create_labeled_widget("PRESENT READING:", present_reading), 3, 0)
        form_layout.addLayout(create_labeled_widget("CUBIC METER CONSUMED:", cubic_meter_consumed), 4, 0)
        form_layout.addLayout(create_labeled_widget("AMOUNT:", amount), 5, 0)
        form_layout.addLayout(create_labeled_widget("DUE DATE:", due_date), 6, 0)

                
        IadminPageBack = adminPageBack()

        client.setEditable(True)
        client.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        client.setStyleSheet(input_style)
        client.lineEdit().setReadOnly(False)

        client_entries = []
        client_data_map = {}

        clients = IadminPageBack.fetch_clients()
        client.clear()

        # Populate client ComboBox
        for client_data in clients:
            client_id = client_data[0]
            client_number = client_data[1]
            first_name = client_data[2]
            last_name = client_data[4]
            display_text = f"{client_number} - {first_name} {last_name}"
            client.addItem(display_text, client_id)
            client_entries.append(display_text)
            client_data_map[display_text] = client_id

        #Completer for client ComboBox
        completer = QtWidgets.QCompleter(client_entries)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        client.setCompleter(completer)

        client.setCurrentText("Select Client")

        def update_total_bill():
            try:
                amt_text = amount.text().strip()
                charge_text = total_charge.text().strip()

                amt = float(amt_text) if amt_text else 0
                charge = float(charge_text) if charge_text else 0

                total = amt + charge
                total_bill.setText(f"{total:.2f}")
            except ValueError:
                total_bill.setText("0.00")


        #connect signal to handle selection changes
        def on_client_selected(index):
            selected_id = client.itemData(index)
            if selected_id is None:
                present_reading.setEnabled(False)
                present_reading.setStyleSheet(readonly_style)
                return
            IadminPageBack = adminPageBack()
            client_info = IadminPageBack.fetch_client_by_id(selected_id)[0] # get client info by id
            meter_id = client_info[5] # meter id
            client_categ_id = client_info[7] # category id
            previous_reading.setText(str(IadminPageBack.fetch_meter_by_id(meter_id)[0][1])) # get previous reading from meter id
            # Fetch rate blocks
            #self.rate_blocks = IadminPageBack.fetch_rate_blocks_by_categ(client_categ_id)
            self.rate_blocks = [
                    (123,True, 0, 10, None,111, 150.0),                # Minimum charge for 0–10 cu.m.
                    (123,False, 10, 20, 16.50,111, None),                   # 11–20 cu.m.
                    (123,False, 20, 30, 18.70,111, None),                   # 21–30 cu.m.
                    (123,False, 30, 40, 21.70,111, None),                   # 31–40 cu.m.
                    (123,False, 40, 50, 25.50,111, None),                   # 41–50 cu.m.
                    (123,False, 50, None, 30.00,111, None),                 # 51+ cu.m.
                ] # tanggala ning self.rate_blocks kung napagana na nimo ang kanang self.rate_blocks sa taas nga nigamit og IadminPageBack
                # naka set up nasad ko didto og function para ana mao sad na nga ngalan palihug lang sad ko pasa og import sa repo ani than
                # sa mga existing lang nga functions pag base dali raman to mura rag pasa pasa nmos repo og controller


            # Store categ_id for use in bill creation
            self.categ_id = client_categ_id
            present_reading.setEnabled(True)
            present_reading.setStyleSheet(input_style)
            

        client.currentIndexChanged.connect(on_client_selected)

        def on_present_reading_changed():
            try:
                prev = float(previous_reading.text())
                pres = float(present_reading.text())
                if pres < prev:
                    cubic_meter_consumed.setText("0")
                    amount.setText("0.00")
                    return

                consumed = pres - prev
                cubic_meter_consumed.setText(str(consumed))

                total_amount = 0
                has_applied_minimum = False

                for block in self.rate_blocks:
                    is_minimum = block[1]           # bool: True if it's the minimum block
                    min_c = block[2]                # min cubmic meter for this block (None if is_minimum)
                    max_c = block[3] if block[3] is not None else float('inf') # max cubic meter for this block (None if is_minimum)
                    rate = block[4]                 # rate per cu.m (None if is_nimum)
                    fixed_fee = block[6]            # fixed fee for is_minimum (None if not is_minimum)

                    if is_minimum and consumed > 0 and not has_applied_minimum:
                        total_amount += fixed_fee
                        has_applied_minimum = True

                    elif not is_minimum and consumed > min_c:
                        applied_volume = max(0, min(consumed, max_c) - min_c)
                        total_amount += applied_volume * rate

                amount.setText(f"{total_amount:.2f}")
                update_total_bill()

            except ValueError:
                cubic_meter_consumed.setText("0")
                amount.setText("0.00")

        present_reading.textChanged.connect(on_present_reading_changed)

        def update_total_charge():
            try:
                sub = float(subscribe_capital.text()) if subscribe_capital.text() else 0
                late = float(late_payment.text()) if late_payment.text() else 0
                pen = float(penalty.text()) if penalty.text() else 0
                total = sub + late + pen
                total_charge.setText(f"{total:.2f}")
                update_total_bill()
            except ValueError:
                total_charge.setText("0.00")
        
        subscribe_capital.textChanged.connect(update_total_charge)
        late_payment.textChanged.connect(update_total_charge)
        penalty.textChanged.connect(update_total_charge)

        def validate_billing_data():
                error_style = """
                    QLineEdit, QDateEdit, QComboBox {
                        padding: 8px;
                        border: 1px solid red;
                        border-radius: 4px;
                        font-family: 'Roboto', sans-serif;
                        min-width: 250px;
                    }
                """
                normal_style = input_style
                errors = []
                has_empty_fields = False
                
                # Reset all styles
                for widget in [client, reading_date, present_reading, due_date, 
                              subscribe_capital, late_payment, penalty]:
                    widget.setStyleSheet(normal_style)
                
                # Check for empty fields first
                if client.currentData() is None:
                    client.setStyleSheet(error_style)
                    has_empty_fields = True
                
                if not present_reading.text().strip():
                    present_reading.setStyleSheet(error_style)
                    has_empty_fields = True
                
                for field in [subscribe_capital, late_payment, penalty]:
                    if not field.text().strip():
                        field.setStyleSheet(error_style)
                        has_empty_fields = True
                
                if has_empty_fields:
                    msg = QtWidgets.QMessageBox(dialog)
                    msg.setWindowTitle("Validation Error")
                    msg.setText("All fields are needed to be filled")
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setStyleSheet("QMessageBox { background-color: white; }")
                    msg.exec_()
                    return False
                
                # Continue with other validations only if no empty fields
                try:
                    prev = float(previous_reading.text() or 0)
                    pres = float(present_reading.text() or 0)
                    if pres <= prev:
                        present_reading.setStyleSheet(error_style)
                        errors.append("\nPresent reading must be greater than previous reading\n")
                except ValueError:
                    present_reading.setStyleSheet(error_style)
                    errors.append("\nInvalid present reading value\n")
                
                if reading_date.date() > QtCore.QDate.currentDate():
                    reading_date.setStyleSheet(error_style)
                    errors.append("\nReading date cannot be in the future\n")
                
                if due_date.date() <= reading_date.date():
                    due_date.setStyleSheet(error_style)
                    errors.append("\nDue date must be after reading date\n")
                
                # Additional charges validation for non-empty fields
                for field, field_name in [(subscribe_capital, "Subscribe Capital"), 
                                        (late_payment, "Late Payment"), 
                                        (penalty, "Penalty")]:
                    try:
                        value = float(field.text())
                        if value < 0:
                            field.setStyleSheet(error_style)
                            errors.append(f"\n{field_name} cannot be negative\n")
                    except ValueError:
                        field.setStyleSheet(error_style)
                        errors.append(f"\nInvalid {field_name} amount\n")
                
                if errors:
                    msg = QtWidgets.QMessageBox(dialog)
                    msg.setWindowTitle("Validation Error")
                    msg.setText("\n\n".join(errors))
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setStyleSheet("QMessageBox { background-color: white; }")
                    msg.exec_()
                    return False
                return True

        def save_bill():
                if not validate_billing_data():
                        return
                try:
                    
                    #backend style
                    #kung kani imo gamiton make sure lang sad nga dapat masave sila tulo dungan walay usa ma fail
                    # akong paabot sat ulo kay ang create reading, create billing, update meter sa iyang reading og last reading date
                    client_id = client.currentData()  # get selected client_id from comboBox
                    prev_read = float(previous_reading.text())
                    pres_read = float(present_reading.text())
                    read_date = reading_date.date().toPyDate()
                    meter_id = IadminPageBack.fetch_client_by_id(client_id)[0][5]  # get meter id from client id

                    reading_id = IadminPageBack.add_reading(read_date, prev_read, pres_read, meter_id) # uncomment ig ready, himog add reading nga function nya e return ang reading id, paki edit nlng pd sa adminback para matest nmo
                    IadminPageBack.update_meter_latest_reading(pres_read, read_date, meter_id) # uncomment sad ig ready, bali maupdate ang last reading sa meter og ang last reading date
                    billing_data = {
                        "billing_due": due_date.date().toPyDate(),
                        "billing_total": float(total_bill.text()) if total_bill.text() else 0,
                        "billing_consumption": float(cubic_meter_consumed.text()) if cubic_meter_consumed.text() else 0,
                        "reading_id": reading_id, # ilisi ang none og reading id kung successfully maka create na
                        "client_id": client_id,
                        "categ_id": self.categ_id,
                        "billing_date": read_date,
                        "billing_status": "TO BE PRINTED",
                        "billing_amount": float(amount.text()) if amount.text() else 0,
                        "billing_sub_capital": float(subscribe_capital.text()) if subscribe_capital.text() else 0,
                        "billing_late_payment": float(late_payment.text()) if late_payment.text() else 0,
                        "billing_penalty": float(penalty.text()) if penalty.text() else 0,
                        "billing_total_charge": float(total_charge.text()) if total_charge.text() else 0
                    }

                    print("READY TO SAVE:", billing_data) # testing rani para check if naget ba ang tanan
                    print(pres_read)
                    IadminPageBack.add_billing(billing_data['billing_due'],
                                            billing_data['billing_total'],
                                            billing_data['billing_consumption'],
                                            billing_data['reading_id'],
                                            billing_data['client_id'],
                                            billing_data['categ_id'],
                                            billing_data['billing_date'],
                                            billing_data['billing_status'],
                                            billing_data['billing_amount'],
                                            billing_data['billing_sub_capital'],
                                            billing_data['billing_late_payment'],
                                            billing_data['billing_penalty'],
                                            billing_data['billing_total_charge'],) # tanggala ang comment kung ready na ang billing repo


                    QtWidgets.QMessageBox.information(dialog, "Success", "Billing information saved successfully.")
                    dialog.accept()
                    updated_data = IadminPageBack.fetch_billing()
                    self.populate_table(updated_data)

                #maka update bisag error
                except Exception as e:
                    QtWidgets.QMessageBox.warning(dialog, "Error", f"Failed to save billing: {str(e)}")

        save_btn.clicked.connect(save_bill)

        dialog.exec_()

class ScrollableTextWidget(QtWidgets.QWidget):
    
    def __init__(self, text, parent=None):
        super(ScrollableTextWidget, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scrollable text area
        self.text_area = QtWidgets.QScrollArea()
        self.text_area.setWidgetResizable(True)
        self.text_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  
        self.text_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        
        # Create a label with the text
        self.label = QtWidgets.QLabel(text)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        
        # Add label to scroll area
        self.text_area.setWidget(self.label)
        
        # Add scroll area to layout
        layout.addWidget(self.text_area)
        
        # Set the widget's style
        self.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
            }
            QLabel {
                background-color: transparent;
                padding-left: 4px;
                padding-right: 4px;
            }
            QScrollBar:horizontal {
                height: 10px;
                background: transparent;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #c0c0c0;
                min-width: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
        
        # Add tooltip for the full text
        self.setToolTip(text)

        # Install event filter to track mouse events
        self.installEventFilter(self)
        
    def text(self):
        return self.label.text()
    
    def eventFilter(self, obj, event):
        if obj is self:
            if event.type() == QtCore.QEvent.Enter:
                # Show scrollbar when mouse enters
                self.text_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
                return True
            elif event.type() == QtCore.QEvent.Leave:
                # Hide scrollbar when mouse leaves
                self.text_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                return True
        return super(ScrollableTextWidget, self).eventFilter(obj, event)


class TextEllipsisDelegate(QtWidgets.QStyledItemDelegate):
    
    def __init__(self, parent=None):
        super(TextEllipsisDelegate, self).__init__(parent)
        
    def paint(self, painter, option, index):
        # Use default painting
        super(TextEllipsisDelegate, self).paint(painter, option, index)
        
    def helpEvent(self, event, view, option, index):
        # Show tooltip when hovering if text is truncated
        if not event or not view:
            return False
            
        if event.type() == QtCore.QEvent.ToolTip:
            # Get the cell widget
            cell_widget = view.cellWidget(index.row(), index.column())
            
            if cell_widget and isinstance(cell_widget, ScrollableTextWidget):
                # Show tooltip for ScrollableTextWidget
                QtWidgets.QToolTip.showText(event.globalPos(), cell_widget.text(), view)
                return True
            else:
                # For standard items
                item = view.itemFromIndex(index)
                if item:
                    text = item.text()
                    width = option.rect.width()
                    metrics = QtGui.QFontMetrics(option.font)
                    elidedText = metrics.elidedText(text, QtCore.Qt.ElideRight, width)
                    
                    # If text is truncated, show tooltip
                    if elidedText != text:
                        QtWidgets.QToolTip.showText(event.globalPos(), text, view)
                    else:
                        QtWidgets.QToolTip.hideText()
                    
                    return True
                
        return super(TextEllipsisDelegate, self).helpEvent(event, view, option, index)        
        

          


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EmployeeBillingPage()
    window.show()
    sys.exit(app.exec_())
