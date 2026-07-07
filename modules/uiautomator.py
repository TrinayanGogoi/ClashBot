import uiautomator2 as u2
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
        Zoom out and center the village view using drag gestures.
        """
        if self.logger:
            self.logger("Zooming out and centering view...")

        if self.d is None:
            raise RuntimeError("UIAutomator2 is not connected. Call connect() first.")

        try:
            # Find the game stage element
            stage = self.d(resourceId="com.supercell.clashofclans:id/stage")
            
            if not stage.exists():
                if self.logger:
                    self.logger("Stage element not found!")
                raise RuntimeError("Cannot find game stage element")
            
            # Step 1: Zoom out
            if self.logger:
                self.logger("Zooming out...")
            
   
            for i in range(2):
                # Simple logging without modulo (since only 2 iterations)
                if self.logger:
                    self.logger(f"Zoom out {i+1}/2...")
                
                stage.pinch_in(percent=50, steps=30)
                time.sleep(0.12)
            
            if self.logger:
                self.logger("Zoom out successfully.")
                
        except Exception as e:
            error_msg = f"Zoom out failed: {str(e)}"
            if self.logger:
                self.logger(error_msg)
            raise RuntimeError(error_msg)
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