from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QListWidgetItem, QComboBox, QSpacerItem, QSizePolicy, QInputDialog, QMessageBox, QDialog, QLineEdit, QTextEdit, QFormLayout, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import QTimer
import sys

class TaskLoggerHome(QMainWindow):
    def __init__(self):
        super().__init__()

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

        # Example task items (these will be dynamic later)
        for i in range(5):
            item = QListWidgetItem(f"Task {i + 1}: Example Task")
            self.task_list.addItem(item)

        # Bottom live timer (placeholder)
        self.live_timer_label = QLabel("Active Task: None")
        main_layout.addWidget(self.live_timer_label)

        # Connect signals to slots
        self.add_task_button.clicked.connect(self.open_add_task_dialog)
        self.statistics_button.clicked.connect(self.view_statistics)
        self.delete_task_button.clicked.connect(self.delete_selected_task)
        self.task_list.itemClicked.connect(self.start_stop_task)

        # Timer for active task tracking
        self.active_task = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_seconds = 0

    def open_add_task_dialog(self):
        """Open a dialog to add detailed task information."""
        dialog = AddTaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            task_name, task_description, estimated_time = dialog.get_task_details()
            if task_name:
                item = QListWidgetItem(f"{task_name} - {estimated_time} mins")
                self.task_list.addItem(item)

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
                if self.active_task == selected_item:
                    self.timer.stop()
                    self.live_timer_label.setText("Active Task: None")
                    self.active_task = None
                self.task_list.takeItem(self.task_list.row(selected_item))
        else:
            QMessageBox.warning(self, "No Task Selected", "Please select a task to delete.")

    def start_stop_task(self, item):
        """Start or stop timing for the selected task."""
        if self.active_task is None:
            # Start timing
            self.active_task = item
            self.live_timer_label.setText(f"Active Task: {item.text()}")
            self.elapsed_seconds = 0
            self.timer.start(1000)  # Update every second
        elif self.active_task == item:
            # Stop timing
            self.timer.stop()
            self.live_timer_label.setText("Active Task: None")
            print(f"Task '{item.text()}' tracked for {self.elapsed_seconds} seconds.")
            self.active_task = None

    def update_timer(self):
        """Update the timer for the active task."""
        self.elapsed_seconds += 1
        self.live_timer_label.setText(f"Active Task: {self.active_task.text()} - {self.elapsed_seconds} seconds")

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Task Details")
        self.setGeometry(200, 200, 400, 300)

        # Layout and widgets
        layout = QFormLayout()

        self.task_name_input = QLineEdit()
        self.task_description_input = QTextEdit()
        self.estimated_time_input = QLineEdit()

        layout.addRow("Task Name:", self.task_name_input)
        layout.addRow("Description:", self.task_description_input)
        layout.addRow("Estimated Time (mins):", self.estimated_time_input)

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
        estimated_time = self.estimated_time_input.text()
        return task_name, task_description, estimated_time

class StatisticsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Statistics")
        self.setGeometry(200, 200, 600, 400)

        # Layout and widgets
        layout = QVBoxLayout()

        self.statistics_table = QTableWidget()
        self.statistics_table.setRowCount(5)  # Placeholder row count
        self.statistics_table.setColumnCount(3)
        self.statistics_table.setHorizontalHeaderLabels(["Task Name", "Time Spent (mins)", "Category"])

        # Populate with example data (dynamic content will be added later)
        for i in range(5):
            self.statistics_table.setItem(i, 0, QTableWidgetItem(f"Task {i + 1}"))
            self.statistics_table.setItem(i, 1, QTableWidgetItem(str((i + 1) * 10)))
            self.statistics_table.setItem(i, 2, QTableWidgetItem("Example Category"))

        layout.addWidget(self.statistics_table)

        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TaskLoggerHome()
    window.show()

    sys.exit(app.exec())

