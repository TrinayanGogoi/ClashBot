import uiautomator2 as u2
import yaml
import time


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

        self.d = u2.connect(self.serial)

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
    

    def zoom_out(self):
        """
        Zoom the Clash of Clans village to maximum.
        """

        if self.logger:
            self.logger("Zooming out...")

        if not hasattr(self, "_stage"):
            self._stage = self.d(resourceId="com.supercell.clashofclans:id/stage")

        for _ in range(6):
            self._stage.pinch_out(percent=100, steps=50)
            time.sleep(0.2)

        if self.logger:
            self.logger("Zoom completed.")
    
    # # temporary method to show all public methods of the device
    # def available_methods(self):
    #     """
    #     Show gesture-related methods supported by uiautomator2.
    #     """

    #     keywords = (
    #         "pinch",
    #         "gesture",
    #         "swipe",
    #         "drag",
    #         "touch",
    #         "multi",
    #     )

    #     methods = sorted(
    #         name
    #         for name in dir(self.d)
    #         if not name.startswith("_")
    #     )

    #     found = False

    #     for method in methods:
    #         if any(k in method.lower() for k in keywords):
    #             self.log(method)
    #             found = True

    #     if not found:
    #         self.log("No matching gesture methods found.")

    # def dump_hierarchy(self):
    #     xml = self.d.dump_hierarchy()

    #     with open("hierarchy.xml", "w", encoding="utf-8") as f:
    #         f.write(xml)

    #     if self.logger:
    #         self.logger("UI hierarchy saved to hierarchy.xml")