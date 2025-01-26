from PyQt6.QtWidgets import QApplication 

import sys
from ui import main


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = main.TaskLoggerHome()
    window.show()

    sys.exit(app.exec())
