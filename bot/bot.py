from modules.emulator import LDPlayer


class Bot:
    """
    Main bot controller.

    This class coordinates all bot modules.
    """

    def __init__(self, logger=None):
        """
        Parameters
        ----------
        logger : callable, optional
            Function used for logging messages.
            Example:
                logger("Starting emulator...")
        """

        self.logger = logger

        self.emulator = LDPlayer()

        # Give the emulator access to the same logger
        self.emulator.logger = logger

    def log(self, message):
        """
        Send a log message if a logger exists.
        """

        if self.logger:
            self.logger(message)

    def start(self):
        """
        Start the bot.
        """

        self.log("Starting emulator...")

        self.emulator.start()

        # self.log("Waiting for emulator...")

        self.emulator.wait_for_device()

        # self.log("Waiting for Android boot...")

        self.emulator.wait_for_boot()

        # self.log("Launching Clash of Clans...")

        self.emulator.launch_app()

        self.log("Bot started successfully.")