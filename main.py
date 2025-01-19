from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QListWidgetItem, QComboBox, QSpacerItem, QSizePolicy, QInputDialog, QMessageBox, QDialog, QLineEdit, QTextEdit, QFormLayout, QTableWidget, QTableWidgetItem
)
import sys
import sqlite3

class TaskLoggerHome(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up database
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.setup_database()

        # Set window title and dimensions
        self.setWindowTitle("Task Logger")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Top bar with buttons
        top_bar_layout = QHBoxLayout()

        self.add_task_button = QPushButton("+ Add New Task")
        self.statistics_button = QPushButton("View Statistics")
        self.delete_task_button = QPushButton("Delete Selected Task")

        top_bar_layout.addWidget(self.add_task_button)
        top_bar_layout.addWidget(self.statistics_button)
        top_bar_layout.addWidget(self.delete_task_button)

        # Spacer to push buttons to the left
        top_bar_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        main_layout.addLayout(top_bar_layout)

        # Task list and filter options
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter by:")
        self.filter_combo_box = QComboBox()
        self.filter_combo_box.addItems(["All", "Today", "This Week", "Category"])

        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo_box)
        filter_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        main_layout.addLayout(filter_layout)

        # Task list display
        self.task_list = QListWidget()
        main_layout.addWidget(self.task_list)

        # Load tasks from database
        self.load_tasks()

        # Connect signals to slots
        self.add_task_button.clicked.connect(self.open_add_task_dialog)
        self.statistics_button.clicked.connect(self.view_statistics)
        self.delete_task_button.clicked.connect(self.delete_selected_task)
        self.filter_combo_box.currentIndexChanged.connect(self.apply_filter)

    def setup_database(self):
        """Create the database table if it doesn't exist."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                time_spent INTEGER,
                category TEXT
            )
            """
        )
        self.conn.commit()

    def load_tasks(self):
        """Load tasks from the database into the task list."""
        self.task_list.clear()
        self.cursor.execute("SELECT id, name, time_spent, category FROM tasks")
        tasks = self.cursor.fetchall()
        for task in tasks:
            item = QListWidgetItem(f"{task[1]} - {task[2]} mins ({task[3]})")
            item.setData(1000, task[0])  # Store task ID in item data
            self.task_list.addItem(item)

    def open_add_task_dialog(self):
        """Open a dialog to add detailed task information."""
        dialog = AddTaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            task_name, task_description, time_spent, category = dialog.get_task_details()
            if task_name:
                self.cursor.execute(
                    "INSERT INTO tasks (name, description, time_spent, category) VALUES (?, ?, ?, ?)",
                    (task_name, task_description, int(time_spent), category)
                )
                self.conn.commit()
                self.load_tasks()

    def view_statistics(self):
        """Open the statistics dialog."""
        dialog = StatisticsDialog(self)
        dialog.exec()

    def delete_selected_task(self):
        """Delete the currently selected task."""
        selected_item = self.task_list.currentItem()
        if selected_item:
            reply = QMessageBox.question(
                self, "Delete Task", f"Are you sure you want to delete the task: '{selected_item.text()}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                task_id = selected_item.data(1000)  # Retrieve task ID from item data
                self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                self.conn.commit()
                self.load_tasks()
        else:
            QMessageBox.warning(self, "No Task Selected", "Please select a task to delete.")

    def apply_filter(self):
        """Apply the selected filter to the task list."""
        filter_option = self.filter_combo_box.currentText()
        if filter_option == "All":
            self.load_tasks()
        elif filter_option == "Category":
            category, ok = QInputDialog.getText(self, "Filter by Category", "Enter category:")
            if ok:
                self.cursor.execute("SELECT id, name, time_spent, category FROM tasks WHERE LOWER(category) = ?", (category.lower(),))
                tasks = self.cursor.fetchall()
                self.task_list.clear()
                for task in tasks:
                    item = QListWidgetItem(f"{task[1]} - {task[2]} mins ({task[3]})")
                    item.setData(1000, task[0])
                    self.task_list.addItem(item)

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Task Details")
        self.setGeometry(200, 200, 400, 300)

        # Layout and widgets
        layout = QFormLayout()

        self.task_name_input = QLineEdit()
        self.task_description_input = QTextEdit()
        self.time_spent_input = QLineEdit()
        self.category_input = QLineEdit()

        layout.addRow("Task Name:", self.task_name_input)
        layout.addRow("Description:", self.task_description_input)
        layout.addRow("Time Spent (mins):", self.time_spent_input)
        layout.addRow("Category:", self.category_input)

        # Buttons
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addRow(button_layout)
        self.setLayout(layout)

    def get_task_details(self):
        """Return task details entered by the user."""
        task_name = self.task_name_input.text()
        task_description = self.task_description_input.toPlainText()
        time_spent = self.time_spent_input.text()
        category = self.category_input.text()
        return task_name, task_description, time_spent, category

class StatisticsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Statistics")
        self.setGeometry(200, 200, 600, 400)

        # Layout and widgets
        layout = QVBoxLayout()

        self.statistics_table = QTableWidget()
        self.statistics_table.setColumnCount(3)
        self.statistics_table.setHorizontalHeaderLabels(["Task Name", "Time Spent (mins)", "Category"])

        layout.addWidget(self.statistics_table)

        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)
        self.load_statistics()

    def load_statistics(self):
        """Load statistics from the database."""
        self.parent().cursor.execute("SELECT name, time_spent, category FROM tasks")
        tasks = self.parent().cursor.fetchall()
        self.statistics_table.setRowCount(len(tasks))
        for row, task in enumerate(tasks):
            self.statistics_table.setItem(row, 0, QTableWidgetItem(task[0]))
            self.statistics_table.setItem(row, 1, QTableWidgetItem(str(task[1])))
            self.statistics_table.setItem(row, 2, QTableWidgetItem(task[2]))

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TaskLoggerHome()
    window.show()

    sys.exit(app.exec())
