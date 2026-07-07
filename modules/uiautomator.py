import uiautomator2 as u2
import yaml


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

        self.device = None

    def log(self, message):

        if self.logger:
            self.logger(message)

    def connect(self):
        """
        Connect to the Android device.
        """

        self.log("Connecting to UIAutomator2...")

        self.device = u2.connect(self.serial)

        self.log("UIAutomator2 connected.")

    def device_info(self):
        """
        Print basic device information.
        """

        if self.device is None:
            raise RuntimeError("UIAutomator2 is not connected.")

        info = self.device.info

        self.log(f"Device info: {info}")

        return info