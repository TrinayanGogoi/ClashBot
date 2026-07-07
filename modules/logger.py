from pathlib import Path
from datetime import datetime


class Logger:

    def __init__(self, gui_callback=None):

        self.gui_callback = gui_callback

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        filename = datetime.now().strftime("%Y%m%d_%H%M%S.log")

        self.log_file = log_dir / filename

    def log(self, message):

        timestamp = datetime.now().strftime("%H:%M:%S")

        line = f"[{timestamp}] {message}"

        # Terminal
        print(line)

        # GUI
        if self.gui_callback:
            self.gui_callback(line)

        # File
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")