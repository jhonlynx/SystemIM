#on and off status

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from backend.adminBack import adminPageBack
from repositories.category_repository import CategoryRepository

class CategoryPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def create_scrollable_cell(self, row, column, text):
        scrollable_widget = ScrollableTextWidget(text)
        self.categorys_table.setCellWidget(row, column, scrollable_widget)    

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title and search
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("CATEGORIES LIST")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()

        search_add_layout = QtWidgets.QHBoxLayout()
        
        # Search container
        search_container = QtWidgets.QHBoxLayout()
        
        # Search input
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search address by name...")
        
        # Apply same styling to both widgets
        input_style = """
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 250px;
            }
        """
        self.search_input.setStyleSheet(input_style)
        self.search_input.textChanged.connect(self.filter_table)
        
        # Add widgets to container
        search_container.addWidget(self.search_input)

        search_add_layout.addLayout(search_container)
        
        
        # Add button with icon
        add_btn = QtWidgets.QPushButton("ADD ADDRESS", icon=QtGui.QIcon("images/add.png"))
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
        add_btn.clicked.connect(self.show_add_category_page)
        search_add_layout.addWidget(add_btn)
        
        header_layout.addLayout(search_add_layout)
        layout.addLayout(header_layout)


        # Table setup
        self.categorys_table = QtWidgets.QTableWidget()
        self.categorys_table.setAlternatingRowColors(True)
        self.categorys_table.setStyleSheet("""
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
        
        # Set up columns (10 columns)
        self.categorys_table.setColumnCount(4)
        self.categorys_table.verticalHeader().setVisible(False)
        self.categorys_table.setHorizontalHeaderLabels([
            "NAME", "DATE", "STATUS", "ACTION"
        ])

        # Set the table to fill all available space
        self.categorys_table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.categorys_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        # Enable horizontal scrollbar
        self.categorys_table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.categorys_table.setWordWrap(False)
        
        IadminPageBack = adminPageBack()
        
        self.populate_table(IadminPageBack.fetch_categories())
        
        # Adjust table properties
        self.categorys_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.categorys_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.categorys_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
        # Create a custom delegate for text elision with tooltip
        delegate = TextEllipsisDelegate(self.categorys_table)
        self.categorys_table.setItemDelegate(delegate)

        # Add table to the main layout with full expansion
        layout.addWidget(self.categorys_table)


    def populate_table(self, data):
        self.categorys_table.setRowCount(0)
        self.categorys_table.setRowCount(len(data))

        for row, category in enumerate(data):
            category_id, category_name, category_status, category_date  = category

            self.create_scrollable_cell(row, 0, category_name)
            self.create_scrollable_cell(row,1, str(category_date))

             # Create status layout with label + toggle button
            status_layout = QtWidgets.QHBoxLayout()
            status_layout.setContentsMargins(5, 0, 5, 0)

            # Status label
            status_label = QtWidgets.QLabel(category_status)
            status_label.setStyleSheet(f"color: {'#4CAF50' if category_status == 'Active' else '#E57373'}; font-weight: bold;")

            # Toggle button for status
            toggle_button = QtWidgets.QPushButton()
            toggle_button.setCheckable(True)
            toggle_button.setChecked(category_status == "Active")
            toggle_button.setFixedSize(40, 20)
            toggle_button.setProperty("category_id", category_id)

            toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: red;
                    border: 1px solid #aaa;
                    border-radius: 10px;
                }
                QPushButton:checked {
                    background-color: green;
                }
            """)
            toggle_button.pressed.connect(lambda r=row, lbl=status_label: self.toggle_status(r, lbl))

            # Add label and button to layout
            status_layout.addWidget(status_label)
            status_layout.addStretch()
            status_layout.addWidget(toggle_button)

            # Set the layout into a QWidget
            status_container = QtWidgets.QWidget()
            status_container.setLayout(status_layout)
            self.categorys_table.setCellWidget(row, 2, status_container)

            # Action widget with deactivate and edit buttons
            actions_widget = QtWidgets.QWidget()
            actions_layout = QtWidgets.QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(30)
            actions_layout.setAlignment(QtCore.Qt.AlignCenter)

            # Edit button
            edit_btn = QtWidgets.QPushButton(icon=QtGui.QIcon("images/edit.png"))
            edit_btn.setIconSize(QtCore.QSize(24, 24))
            edit_btn.setStyleSheet("""
                QPushButton {
                    padding: 5px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
            """)
            edit_btn.clicked.connect(lambda _, row=row: self.show_edit_category_page(row))

            actions_layout.addWidget(edit_btn)
            self.categorys_table.setCellWidget(row, 3, actions_widget)
 


    def show_add_category_page(self):
        add_dialog = QtWidgets.QDialog(self)
        add_dialog.setWindowTitle("New Category")
        add_dialog.setModal(True)
        add_dialog.setFixedSize(600, 200)
        add_dialog.setStyleSheet("""
            QDialog {
                background-color: #C9EBCB;
            }
            QLabel {
                font-family: 'Arial', sans-serif;
                font-weight: bold;
            }
        """)

        layout = QtWidgets.QVBoxLayout(add_dialog)
        layout.setContentsMargins(30, 10, 30, 10)
        layout.setSpacing(10)

        # Title
        title = QtWidgets.QLabel("ADD NEW CATEGORY")
        title.setStyleSheet("""
            font-size: 20px;
            padding: 10px;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Form layout
        form_layout = QtWidgets.QGridLayout()
        form_layout.setHorizontalSpacing(40)
        form_layout.setVerticalSpacing(20)

        input_style = """
            QLineEdit {
                font-family: 'Arial';
                font-size: 14px;
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #ffffff;
            }
        """

        # Create reusable label+input block
        def create_labeled_widget(label_text, widget):
            wrapper = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel(label_text)
            label.setFont(QtGui.QFont("Arial", 10))
            wrapper.addWidget(label)
            wrapper.addWidget(widget)
            return wrapper

        # Category input
        category_name_input = QtWidgets.QLineEdit()
        category_name_input.setStyleSheet(input_style)

        form_layout.addLayout(create_labeled_widget("CATEGORY NAME:", category_name_input), 0, 0)

        layout.addLayout(form_layout)
        layout.addStretch()

        # Button container
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setAlignment(QtCore.Qt.AlignRight)

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
        cancel_btn.clicked.connect(add_dialog.reject)

        save_btn = QtWidgets.QPushButton("Save")
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

        def save_action():
            if not category_name_input.text().strip():
                QMessageBox.warning(add_dialog, "Validation Error", "Category name cannot be empty.")
                return
            
            # Get the category name from input
            category_name = category_name_input.text().strip()
            
            # Create a new category in the database
            IadminPageBack = adminPageBack()
            category_repository = CategoryRepository()
            category_repository.create_category(category_name, "Active")
            
            # Show success message
            QMessageBox.information(add_dialog, "Success", f"Category '{category_name}' has been successfully added.")
            
            # Refresh the table with updated data
            self.populate_table(IadminPageBack.fetch_categories())
            
            # Close the dialog
            add_dialog.accept()
        # After defining save_action function
        save_btn.clicked.connect(save_action)  # Add this line
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addWidget(button_container)

        add_dialog.exec_()



    def show_edit_category_page(self, row):
        # Get the category name from the ScrollableTextWidget
        cell_widget = self.categorys_table.cellWidget(row, 0)
        if cell_widget and isinstance(cell_widget, ScrollableTextWidget):
            current_name = cell_widget.text()
        else:
            current_name = ""  # Default value if widget not found

        edit_dialog = QtWidgets.QDialog(self)
        edit_dialog.setWindowTitle("Edit Category")
        edit_dialog.setFixedSize(600, 250)
        edit_dialog.setStyleSheet("""
            QDialog {
                background-color: #C9EBCB;
            }
            QLabel {
                font-family: 'Arial', sans-serif;
                font-weight: bold;
            }
        """)

        layout = QtWidgets.QVBoxLayout(edit_dialog)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        # Title
        title = QtWidgets.QLabel("EDIT CATEGORY")
        title.setStyleSheet("""
            font-size: 20px;
            padding: 10px;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Input styles
        input_style = """
            QLineEdit {
                font-family: 'Arial';
                font-size: 14px;
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #ffffff;
            }
        """

        # Create labeled widget helper
        def create_labeled_widget(label_text, widget):
            container = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel(label_text)
            label.setFont(QtGui.QFont("Arial", 10))
            container.addWidget(label)
            container.addWidget(widget)
            return container

        # Form layout
        form_layout = QtWidgets.QGridLayout()
        form_layout.setHorizontalSpacing(30)
        form_layout.setVerticalSpacing(15)

        name_input = QtWidgets.QLineEdit(current_name)
        name_input.setStyleSheet(input_style)

        form_layout.addLayout(create_labeled_widget("CATEGORY NAME:", name_input), 0, 0)

        layout.addLayout(form_layout)

        # Buttons
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setAlignment(QtCore.Qt.AlignRight)

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
        cancel_btn.clicked.connect(edit_dialog.reject)

        save_btn = QtWidgets.QPushButton("Save")
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

        def save_action():
            if not name_input.text().strip():
                QMessageBox.warning(edit_dialog, "Validation Error", "Category name cannot be empty.")
                return
            
            # Get the category name from input
            new_category_name = name_input.text().strip()
            
            # Check if the name is unchanged
            if new_category_name == current_name:
                QMessageBox.information(edit_dialog, "No Changes", "The category name is unchanged.")
                edit_dialog.accept()
                return
            
            # Get the category ID from the table
            status_container = self.categorys_table.cellWidget(row, 2)
            if status_container:
                toggle_button = status_container.findChild(QtWidgets.QPushButton)
                if toggle_button:
                    category_id = toggle_button.property("category_id")
                    
                    # Update the category in the database
                    IadminPageBack = adminPageBack()
                    category_repository = CategoryRepository()
                    category_repository.update_category(category_id, new_category_name)
                    
                    # Show success message
                    QMessageBox.information(edit_dialog, "Success", f"Category '{new_category_name}' has been successfully updated.")
                    
                    # Refresh the table with updated data
                    self.populate_table(IadminPageBack.fetch_categories())
            
            # Close the dialog
            edit_dialog.accept()
        save_btn.clicked.connect(save_action)
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addWidget(button_container)

        edit_dialog.exec_()



    def deactivate_category(self, row):
        # Get the category name from the ScrollableTextWidget
        cell_widget = self.categorys_table.cellWidget(row, 0)
        if cell_widget and isinstance(cell_widget, ScrollableTextWidget):
            category_name = cell_widget.text()
            
            # Get the status widget to find the category_id
            status_container = self.categorys_table.cellWidget(row, 2)
            if status_container:
                toggle_button = status_container.findChild(QtWidgets.QPushButton)
                if toggle_button:
                    category_id = toggle_button.property("category_id")
                    
                    reply = QtWidgets.QMessageBox.question(
                        self, 'Deactivate Category',
                        f"Are you sure you want to deactivate category {category_name}?",
                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                        QtWidgets.QMessageBox.No
                    )
                    
                    if reply == QtWidgets.QMessageBox.Yes:
                        IadminPageBack = adminPageBack()
                        IadminPageBack.toggle_category_status(category_id, 'Inactive')
                        # Refresh the table
                        self.populate_table(IadminPageBack.fetch_categories())

    def toggle_search_input(self, text):
            if text == "Category":
                self.search_input.hide()
                self.search_input_combo.show()
            else:
                self.search_input.show()
                self.search_input_combo.hide() 

    def filter_table(self, text):
        # Filter rows based on the search text
        for row in range(self.categorys_table.rowCount()):
            cell_widget = self.categorys_table.cellWidget(row, 0)  # Get the NAME column widget
            if cell_widget and isinstance(cell_widget, ScrollableTextWidget):
                category_name = cell_widget.text().lower()
                if text.lower() in category_name:
                    self.categorys_table.setRowHidden(row, False)  # Show row if name matches
                else:
                    self.categorys_table.setRowHidden(row, True)  # Hide row if name doesn't match             

    def toggle_status(self, row, label):
        table = self.categorys_table
        container = table.cellWidget(row, 2)
        if container:
            toggle_button = container.findChild(QtWidgets.QPushButton)
            if toggle_button:
                category_id = toggle_button.property("category_id")
                IadminPageBack = adminPageBack()
                category_info = IadminPageBack.get_category_by_id(category_id)
                current_status = category_info[0][2]  # 'Active' or 'Inactive'
                next_status = 'Inactive' if current_status == 'Active' else 'Active'

                # Block toggle auto-switch
                toggle_button.blockSignals(True)

                reply = QMessageBox.question(
                    self,
                    "Confirm Status Change",
                    f"Are you sure you want to change the status to {next_status}?",
                    QMessageBox.Yes | QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    # Update DB
                    IadminPageBack.toggle_category_status(category_id, next_status)
                    # Update label and toggle state
                    label.setText(next_status)
                    label.setStyleSheet(f"color: {'#4CAF50' if next_status == 'Active' else '#E57373'}; font-weight: bold;")
                    toggle_button.setChecked(next_status == "Active")  # Convert to boolean
                else:
                    # Keep original state
                    toggle_button.setChecked(current_status == "Active")  # Convert to boolean

                toggle_button.blockSignals(False)

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
    window = CategoryPage()
    window.show()
    sys.exit(app.exec_())
