from COCBot.functions.Vision.detector import Detector
from pathlib import Path

class DetectElixirCollectors(Detector):

    def run(self, screenshot):

        return self.find_templates(
            screenshot,
            folder="templates\\Collectors\\Elixir_Collectors",
            threshold=0.80,
        )

