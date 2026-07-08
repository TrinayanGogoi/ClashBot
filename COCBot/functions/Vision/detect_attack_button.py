import cv2
from pathlib import Path
from modules.vision import Vision

class DetectAttackButton:

    def __init__(self, vision, logger=None):
        self.vision = vision
        self.logger = logger

    def run(self, screenshot):

        return self.vision.find_template(
            screenshot,
            "templates/AttackBar/Attack_Button_HomeVillage.png",
            threshold=0.90,
        )