from COCBot.functions.Vision.detect_attack_button import DetectAttackButton
from COCBot.functions.Vision.detect_gold_mines import DetectGoldMines
from modules import logger
from modules.emulator import LDPlayer
from modules.adb import ADB
from modules.uiautomator import UIAutomator
from COCBot.functions.Android.zoom_out import ZoomOut
from modules.vision import Vision
from COCBot.functions.Vision.draw_match import DrawMatches


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

        self.emulator = LDPlayer()
        self.adb = ADB()
        self.uiautomator = UIAutomator()
        self.vision = Vision()

        self.logger = logger
        self.emulator.logger = logger
        self.adb.logger = logger
        self.uiautomator.logger = logger
        self.vision.logger = logger

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
        self.uiautomator.connect()

        # self.log("Launching Clash of Clans...")

        self.emulator.launch_app()

        self.log("Bot started successfully.")
    
    def capture_screenshot(self):

        self.adb.screenshot(save=True)
    
    def device_info(self):
        self.uiautomator.device_info()

    def zoom_out(self):
        ZoomOut(self.uiautomator, self.logger).run()


    def test_vision(self, detector_name):

        image = self.adb.screenshot()

        detectors = {
            "Gold Mines": DetectGoldMines,
            "Attack Button": DetectAttackButton,
            # "Clan Castle": DetectClanCastle,
            # "Town Hall": DetectTownHall,
        }

        detector_class = detectors.get(detector_name)

        if detector_class is None:
            self.log(f"Unknown detector: {detector_name}")
            return

        detector = detector_class(
            self.vision,
            self.logger,
        )

        matches = detector.run(image)

        self.log(f"Detected {len(matches)} object(s).")

        if not matches:
            self.log("Nothing found.")
            return

        for match in matches:
            self.log(str(match))

        DrawMatches(self.logger).run(image, matches)

    # def test_vision(self, detector):
    #     image = self.adb.screenshot()

    #     # matches = DetectGoldMines(
    #     #     self.vision,
    #     #     self.logger,
    #     # ).run(image)

    #     matches = detector.run(image)
        
    #     self.log(f"Detected {len(matches)} Gold Mines.")

    #     if not matches:
    #         self.log("No Gold Mines found.")
    #         return

    #     for match in matches:
    #         self.log(str(match))
    #         # self.log("Attack button found. Clicking...")
    #         # self.adb.tap(
    #         #     result["center_x"],
    #         #     result["center_y"],
    #         # )
    #     if matches:    
    #         DrawMatches(self.logger).run(image, matches)
    #     else:
    #         self.log("No Gold Mines found.")



    # def test_gold_mines(self):
    #     self.test_vision(
    #         DetectGoldMines(
    #             self.vision,
    #             self.logger,
    #         )
    #     )

    # def test_attack_button(self):
    #     self.test_vision(
    #         DetectAttackButton(
    #             self.vision,
    #             self.logger,
    #         )
    #     )