import uiautomator2 as uiautomator
import yaml
import time
import threading


class UIAutomator:
    """
    Wrapper around the uiautomator2 library.

    Responsibilities:
        - Connect to Android
        - Advanced gestures
        - Multi-touch
        - Future UI interactions
    """

    def __init__(self, config_path="config/config.yaml"):

        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        self.serial = config["device"]["serial"]

        self.logger = None

        self.d = None

    def log(self, message):

        if self.logger:
            self.logger(message)

    def connect(self):
        """
        Connect to the Android device.
        """

        self.log("Connecting to UIAutomator2...")

        self.d = uiautomator.connect(self.serial)

        self.log("UIAutomator2 connected.")

    def device_info(self):
        """
        Print basic device information.
        """

        if self.d is None:
            raise RuntimeError("UIAutomator2 is not connected.")

        info = self.d.info

        self.log(f"Device info: {info}")

        return info
    
 
