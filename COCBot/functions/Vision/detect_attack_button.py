from pathlib import Path
from COCBot.functions.Vision.detector import Detector

class DetectAttackButton(Detector):

    def run(self, screenshot):

        return self.find_templates(
            screenshot,
            folder="templates/AttackBar",
            threshold=0.90,
        )

# class DetectAttackButton(Detector):
#     """
#     Detect the Attack button on the Home Village screen.
#     """

#     def __init__(self, vision, logger=None):
#         super().__init__(vision, logger)

#         self.template_folder = Path(
#             "templates/AttackBar"
#         )

#     def run(self, screenshot):

#         matches = []

#         templates = sorted(
#             self.template_folder.glob("*.png")
#         )

#         self.log(
#             f"Searching {len(templates)} Attack Button templates..."
#         )

#         for template in templates:

#             result = self.vision.find_template(
#                 screenshot,
#                 str(template),
#                 threshold=0.90,
#             )

#             if result["found"]:

#                 result["template"] = template.name

#                 matches.append(result)

#                 self.log(
#                     f"Attack Button found using {template.name}"
#                 )

#         self.log(
#             f"Detected {len(matches)} Attack Button(s)."
#         )

#         return matches




# from pathlib import Path
# from COCBot.functions.Vision.detector import Detector



# class DetectAttackButton(Detector):
#     """
#     Detect the Attack button on the Home Village screen.
#     """

#     def __init__(self, vision, logger=None):

#         # self.vision = vision
#         # self.logger = logger
#         super().__init__(vision, logger)

#         self.template_folder = Path(
#             "templates/AttackBar"
#         )

#     def log(self, message):

#         if self.logger:
#             self.logger(message)

#     def run(self, screenshot):

#         templates = sorted(
#             self.template_folder.glob("*.png")
#         )

#         self.log(
#             f"Searching {len(templates)} Attack Button templates..."
#         )

#         for template in templates:

#             result = self.vision.find_template(
#                 screenshot,
#                 str(template),
#                 threshold=0.90,
#             )

#             if result["found"]:

#                 result["template"] = template.name

#                 self.log(
#                     f"Attack Button found using {template.name}"
#                 )

#                 return result

#         self.log("Attack Button not found.")

#         return {
#             "found": False
#         }