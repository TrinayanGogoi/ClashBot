import traceback
from functools import partial
from modules.logger import Logger

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from bot.bot import Bot


class Worker(QThread):
    """
    Generic worker that can execute any Bot task.
    """

    # finished = Signal()
    error = Signal(str)
    log = Signal(str)

    def __init__(self, bot, task_name, *args, **kwargs):
        super().__init__()

        self.bot = bot
        self.task_name = task_name

        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            task = getattr(self.bot, self.task_name)
            task(
                *self.args,
                **self.kwargs,
            )
            # print(">>> Worker emitting finished")
            # self.finished.emit()

        except Exception:
            self.error.emit(traceback.format_exc())


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ClashBot Edu")
        self.resize(700, 500)

        self.worker = None

        self.logger = Logger(gui_callback=self.log)

        self.bot = Bot(logger=self.logger.log)

        # ------------------------
        # Widgets
        # ------------------------

        self.status = QLabel("Status: Idle")
        self.status.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("▶ Start Bot")
        self.screenshot_button = QPushButton("Capture Screenshot")
        self.zoom_button = QPushButton("Zoom Out")
        self.test_vision_button = QPushButton("Test Vision")

        self.bot_running = False

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        # ------------------------
        # Layout
        # ------------------------

        layout = QVBoxLayout()
        layout.addWidget(self.status)
        layout.addWidget(self.start_button)
        layout.addWidget(self.screenshot_button)
        layout.addWidget(self.zoom_button)
        layout.addWidget(self.test_vision_button)
        layout.addWidget(self.log_box)

        self.setLayout(layout)

        # ------------------------
        # Signals
        # ------------------------

        self.start_button.clicked.connect(self.toggle_bot) # not using Lambda here because we want to toggle the bot state
        self.screenshot_button.clicked.connect(self.capture_screenshot) # not using Lambda here because we want to capture a screenshot
        self.zoom_button.clicked.connect(lambda: self.run_task("zoom_out"))
        self.test_vision_button.clicked.connect(lambda: self.run_task("test_vision"))
        self.logger.log("Application started.")

    # ==========================================================
    # Logging
    # ==========================================================

    def log(self, text):
        self.log_box.append(text)

    # ==========================================================
    # Generic task runner
    # ==========================================================

    def run_task(self,task_name,*args, **kwargs,):
        worker = Worker(
            self.bot,
            task_name,
            *args,
            **kwargs,
        )
        worker.error.connect(self.bot_error)
        worker.finished.connect(
            partial(
                self.task_finished,
                worker,
            )
        )
        self.worker = worker
        worker.start()

    # ==========================================================
    # Button handlers
    # ==========================================================

    def start_bot(self):

        self.start_button.setEnabled(False)
        self.start_button.setText("Starting...")

        self.status.setText("Status: Starting...")

        self.run_task("start")

    def toggle_bot(self):

        if self.bot_running:
            self.stop_bot()
        else:
            self.start_bot()

    def capture_screenshot(self):

        self.screenshot_button.setEnabled(False)

        self.run_task("capture_screenshot")

    # ==========================================================
    # Worker callbacks  # print(">>> task_finished called")
    # ==========================================================

    def task_finished(self, worker):

        self.status.setText("Status: Running")
        # print(">>> task_finished called")
        self.bot_running = True

        self.start_button.setEnabled(True)
        self.start_button.setText("■ Stop Bot")

        self.screenshot_button.setEnabled(True)

        self.logger.log("Task completed.")

        worker.deleteLater()

        if self.worker is worker:
            self.worker = None


    def stop_bot(self):

        self.bot_running = False

        self.status.setText("Status: Stopped")

        self.start_button.setText("▶ Start Bot")

        self.logger.log("Bot stopped.")

    def bot_error(self, message):

        self.start_button.setEnabled(True)
        self.screenshot_button.setEnabled(True)

        self.status.setText("Status: Error")

        self.logger.log(message)

        if self.worker:
            self.worker.deleteLater()
            self.worker = None