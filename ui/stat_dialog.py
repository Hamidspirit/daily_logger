from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton

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