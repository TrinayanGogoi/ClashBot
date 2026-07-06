import traceback

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from bot.bot import Bot


class BotWorker(QThread):
    finished = Signal()
    error = Signal(str)
    log = Signal(str)

    def run(self):
        try:
            bot = Bot(logger=self.log.emit)

            bot.start()

            self.finished.emit()

        except Exception:
            self.error.emit(traceback.format_exc())

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ClashBot Edu")

        self.resize(700, 500)

        self.status = QLabel("Status: Idle")
        self.status.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Start Bot")

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        layout = QVBoxLayout()

        layout.addWidget(self.status)
        layout.addWidget(self.start_button)
        layout.addWidget(self.log_box)

        self.setLayout(layout)

        self.worker = None

        self.start_button.clicked.connect(self.start_bot)

        self.log("Application started.")

    def log(self, text):
        self.log_box.append(text)

    def start_bot(self):

        self.start_button.setEnabled(False)

        self.status.setText("Status: Starting...")

        self.worker = BotWorker()

        self.worker.log.connect(self.log)

        self.worker.finished.connect(self.bot_started)

        self.worker.error.connect(self.bot_error)

        self.worker.start()

    def bot_started(self):

        self.status.setText("Status: Running")

        # self.log("Bot started successfully.")

    def bot_error(self, message):

        self.status.setText("Status: Error")

        self.log(message)

        self.start_button.setEnabled(True)