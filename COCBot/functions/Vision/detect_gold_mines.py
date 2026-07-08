from COCBot.functions.Vision.detector import Detector
from pathlib import Path

class DetectGoldMines(Detector):

    def run(self, screenshot):

        return self.find_templates(
            screenshot,
            folder="templates/Storages/Collectors/GoldMines",
            threshold=0.40,
        )


# from pathlib import Path
# from COCBot.functions.Vision.detector import Detector


# class DetectGoldMines(Detector):
#     """
#     Detect all Gold Mines on the current screen.
#     """

#     def __init__(self, vision, logger=None):

#         # self.vision = vision
#         # self.logger = logger
#         super().__init__(vision, logger)

#         self.template_folder = Path(
#             "templates/Storages/Collectors/GoldMines"
#         )

#     def log(self, message):

#         if self.logger:
#             self.logger(message)

#     def run(self, screenshot):

#         gold_mines = []

#         templates = sorted(
#             self.template_folder.glob("*.png")
#         )

#         self.log(
#             f"Searching {len(templates)} Gold Mine templates..."
#         )

#         for template in templates:

#             result = self.vision.find_template(
#                 screenshot,
#                 str(template),
#                 threshold=0.40,
#             )

#             if result["found"]:

#                 result["template"] = template.name

#                 gold_mines.append(result)

#         self.log(
#             f"Detected {len(gold_mines)} Gold Mines."
#         )

#         return gold_mines