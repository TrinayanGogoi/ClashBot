from modules.emulator import LDPlayer
from modules.adb import ADB
from modules.uiautomator import UIAutomator

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
        self.adb = ADB()    
        self.u2 = UIAutomator()

        
        # Give the emulator access to the same logger
        self.emulator.logger = logger
        self.u2.logger = logger
        self.adb.logger = logger

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
        self.u2.connect()

        # self.log("Launching Clash of Clans...")

        self.emulator.launch_app()

        self.log("Bot started successfully.")
    
    def capture_screenshot(self):

        self.adb.screenshot(save=True)
    
    def device_info(self):
        self.u2.device_info()

    # def available_methods(self):
    #     self.u2.available_methods()

    # def dump_hierarchy(self):
    #     self.u2.dump_hierarchy()

    def zoom_out(self):
        self.u2.zoom_out()


