from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit,QPushButton, QTextEdit, QHBoxLayout
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
