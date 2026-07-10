from pathlib import Path
from COCBot.functions.Vision.detector import Detector

class DetectAttackButton(Detector):

    def run(self, screenshot):

        return self.find_templates(
            screenshot,
            folder="templates\\Buttons\\Attack",
            threshold=0.80,
        )

